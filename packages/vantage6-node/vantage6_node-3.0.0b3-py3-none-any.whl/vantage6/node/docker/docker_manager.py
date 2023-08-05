""" Docker manager

The docker manager is responsible for communicating with the docker-
daemon and is a wrapper arround the docker module. It has methods
for creating docker networks, docker volumes, start containers
and retreive results from finished containers
"""
import os
import time
import logging
import docker
import re
import shutil

from typing import Dict, List, NamedTuple, Union
from pathlib import Path

from vantage6.common.globals import APPNAME
from vantage6.node.docker.vpn_manager import VPNManager
from vantage6.node.util import logger_name
from vantage6.node.docker.network_manager import IsolatedNetworkManager
from vantage6.node.docker.task_manager import DockerTaskManager

log = logging.getLogger(logger_name(__name__))


class Result(NamedTuple):
    """ Data class to store the result of the docker image."""
    result_id: int
    logs: str
    data: str
    status_code: int


class DockerManager(object):
    """ Wrapper for the docker module, to be used specifically for vantage6.

        It handles docker images names to results `run(image)`. It manages
        docker images, files (input, output, token, logs). Docker images run
        in detached mode, which allows to run multiple docker containers at
        the same time. Results (async) can be retrieved through
        `get_result()` which returns the first available result.
    """
    log = logging.getLogger(logger_name(__name__))

    def __init__(self, ctx, isolated_network_mgr: IsolatedNetworkManager,
                 vpn_manager: VPNManager) -> None:
        """ Initialization of DockerManager creates docker connection and
            sets some default values.

            Parameters
            ----------
            ctx: DockerNodeContext or NodeContext
                Context object from which some settings are obtained
            isolated_network_mgr: IsolatedNetworkManager
                Manager for the isolated network
            vpn_manager: VPNManager
                VPN Manager object
        """
        self.log.debug("Initializing DockerManager")
        self.data_volume_name = ctx.docker_volume_name
        config = ctx.config
        self.algorithm_env = config.get('algorithm_env', {})
        self.vpn_manager = vpn_manager

        # Connect to docker daemon
        self.docker = docker.from_env()

        # keep track of the running containers
        self.active_tasks: List[DockerTaskManager] = []

        # before a task is executed it gets exposed to these regex
        self._allowed_images = config.get("allowed_images")

        # isolated network to which algorithm containers can attach
        self.isolated_network_mgr = isolated_network_mgr

        # node name is used to identify algorithm containers belonging
        # to this node. This is required as multiple nodes may run at
        # a single machine sharing the docker daemon while using a
        # different server. Using a different server means that there
        # could be duplicate result_id's running at the node at the same
        # time.
        self.node_name = ctx.name

        # login to the registries
        docker_registries = ctx.config.get("docker_registries", [])
        self.login_to_registries(docker_registries)

        # set (and possibly create) the task directories
        self._set_task_dir(ctx)

        # set database uri and whether or not it is a file
        self._set_database(config)

    def _set_task_dir(self, ctx) -> None:
        """
        Set the task dir

        Parameters
        ----------
        ctx: DockerNodeContext or NodeContext
            Context object containing settings
        """
        # If we're in a 'regular' context, we'll copy the dataset to our data
        # dir and mount it in any algorithm container that's run; bind mounts
        # on a folder will work just fine.
        #
        # If we're running in dockerized mode we *cannot* bind mount a folder,
        # because the folder is in the container and not in the host. We'll
        # have to use a docker volume instead. This means:
        #  1. we need to know the name of the volume so we can pass it along
        #  2. need to have this volume mounted so we can copy files to it.
        #
        #  Ad 1: We'll use a default name that can be overridden by an
        #        environment variable.
        #  Ad 2: We'll expect `ctx.data_dir` to point to the right place. This
        #        is OK, since ctx will be a DockerNodeContext.
        #
        #  This also means that the volume will have to be created & mounted
        #  *before* this node is started, so we won't do anything with it here.

        # We'll create a subfolder in the data_dir. We need this subfolder so
        # we can easily mount it in the algorithm containers; the root folder
        # may contain the private key, which which we don't want to share.
        # We'll only do this if we're running outside docker, otherwise we
        # would create '/data' on the data volume.
        if not ctx.running_in_docker:
            self.__tasks_dir = ctx.data_dir / 'data'
            os.makedirs(self.__tasks_dir, exist_ok=True)
        else:
            self.__tasks_dir = ctx.data_dir

    def _set_database(self, config: Dict) -> None:
        """"
        Set database location and whether or not it is a file

        Parameters
        ----------
        config: Dict
            Configuration of the app
        """
        # If we're running in a docker container, database_uri would point
        # to a path on the *host* (since it's been read from the config
        # file). That's no good here. Therefore, we expect the CLI to set
        # the environment variable for us. This has the added bonus that we
        # can override the URI from the command line as well.
        default_uri = config['databases']['default']
        self.database_uri = os.environ.get('DATABASE_URI', default_uri)

        self.database_is_file = False
        if Path(self.database_uri).exists():
            # We'll copy the file to the folder `data` in our task_dir.
            self.log.info(f'Copying {self.database_uri} to {self.__tasks_dir}')
            shutil.copy(self.database_uri, self.__tasks_dir)

            # Since we've copied the database to the folder 'data' in the root
            # of the volume: '/data/<database.csv>'. We'll just keep the
            # basename (i.e. filename + ext).
            self.database_uri = os.path.basename(self.database_uri)
            self.database_is_file = True

    def create_volume(self, volume_name: str) -> None:
        """
        Create a temporary volume for a single run.

        A single run can consist of multiple algorithm containers. It is
        important to note that all algorithm containers having the same run_id
        have access to this container.

        Parameters
        ----------
        volume_name: str
            Name of the volume to be created
        """
        try:
            self.docker.volumes.get(volume_name)
            self.log.debug(f"Volume {volume_name} already exists.")

        except docker.errors.NotFound:
            self.log.debug(f"Creating volume {volume_name}")
            self.docker.volumes.create(volume_name)

    def is_docker_image_allowed(self, docker_image_name: str) -> bool:
        """
        Checks the docker image name.

        Against a list of regular expressions as defined in the configuration
        file. If no expressions are defined, all docker images are accepted.

        Parameters
        ----------
        docker_image_name: str
            uri to the docker image

        Returns
        -------
        bool
            Whether docker image is allowed or not
        """

        # if no limits are declared
        if not self._allowed_images:
            self.log.warn("All docker images are allowed on this Node!")
            return True

        # check if it matches any of the regex cases
        for regex_expr in self._allowed_images:
            expr_ = re.compile(regex_expr)
            if expr_.match(docker_image_name):
                return True

        # if not, it is considered an illegal image
        return False

    def is_running(self, result_id: int) -> bool:
        """
        Check if a container is already running for <result_id>.

        Parameters
        ----------
        result_id: int
            result_id of the algorithm container to be found

        Returns
        -------
        bool
            Whether or not algorithm container is running already
        """
        running_containers = self.docker.containers.list(filters={
            "label": [
                f"{APPNAME}-type=algorithm",
                f"node={self.node_name}",
                f"result_id={result_id}"
            ]
        })
        return bool(running_containers)

    def run(self, result_id: int,  image: str, docker_input: bytes,
            tmp_vol_name: str, token: str) -> Union[int, None]:
        """
        Checks if docker task is running. If not, creates DockerTaskManager to
        run the task

        Parameters
        ----------
        result_id: int
            Server result identifier
        image: str
            Docker image name
        docker_input: bytes
            Input that can be read by docker container
        tmp_vol_name: str
            Name of temporary docker volume assigned to the algorithm
        token: str
            Bearer token that the container can use

        Returns
        -------
        int or None:
            Port number assigned for VPN communication. None if VPN is inactive
        """
        # Verify that an allowed image is used
        if not self.is_docker_image_allowed(image):
            msg = f"Docker image {image} is not allowed on this Node!"
            self.log.critical(msg)
            return None

        # Check that this task is not already running
        if self.is_running(result_id):
            self.log.warn("Task is already being executed, discarding task")
            self.log.debug(f"result_id={result_id} is discarded")
            return None

        task = DockerTaskManager(
            image=image,
            result_id=result_id,
            vpn_manager=self.vpn_manager,
            node_name=self.node_name,
            tasks_dir=self.__tasks_dir,
            isolated_network_mgr=self.isolated_network_mgr,
            database_uri=self.database_uri,
            database_is_file=self.database_is_file,
            docker_volume_name=self.data_volume_name
        )
        vpn_port = task.run(
            docker_input=docker_input, tmp_vol_name=tmp_vol_name, token=token,
            algorithm_env=self.algorithm_env
        )

        # keep track of the active container
        self.active_tasks.append(task)

        return vpn_port

    def get_result(self) -> Result:
        """
        Returns the oldest (FIFO) finished docker container.

        This is a blocking method until a finished container shows up. Once the
        container is obtained and the results are read, the container is
        removed from the docker environment.

        Returns
        -------
        Result
            result of the docker image
        """

        # get finished results and get the first one, if no result is available
        # this is blocking
        finished_tasks = []
        while not finished_tasks:
            finished_tasks = [t for t in self.active_tasks if t.is_finished()]
            time.sleep(1)

        # at least one task is finished
        finished_task = finished_tasks.pop()
        self.log.debug(f"Result id={finished_task.result_id} is finished")

        # Check exit status and report
        logs = finished_task.report_status()

        # Cleanup containers
        finished_task.cleanup()

        # Retrieve results from file
        results = finished_task.get_results()

        # remove finished tasks from active task list
        self.active_tasks.remove(finished_task)

        return Result(
            result_id=finished_task.result_id,
            logs=logs,
            data=results,
            status_code=finished_task.status_code
        )

    def login_to_registries(self, registries: list = []) -> None:
        """
        Login to the docker registries

        Parameters
        ----------
        registries: list
            list of registries to login to
        """
        for registry in registries:
            try:
                self.docker.login(
                    username=registry.get("username"),
                    password=registry.get("password"),
                    registry=registry.get("registry")
                )
                self.log.info(f"Logged in to {registry.get('registry')}")
            except docker.errors.APIError as e:
                self.log.warn(f"Could not login to {registry.get('registry')}")
                self.log.debug(e)
