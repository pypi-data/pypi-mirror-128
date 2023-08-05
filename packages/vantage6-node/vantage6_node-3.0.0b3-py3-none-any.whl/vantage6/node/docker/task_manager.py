""" TODO the task folder is also created by this class. This folder needs
to be cleaned at some point. """
import logging
import docker
import os

from docker.models.containers import Container
from typing import Dict
from pathlib import Path

from vantage6.common.globals import APPNAME
from vantage6.node.util import logger_name
from vantage6.node.docker.vpn_manager import VPNManager
from vantage6.node.docker.network_manager import IsolatedNetworkManager
from vantage6.node.docker.utils import running_in_docker
from vantage6.common.docker_addons import pull_if_newer


class DockerTaskManager(object):
    """
    Manager for running a Vantage6 algorithm container within docker.

    Ensures that the environment is properly set up (docker volumes,
    directories, environment variables, etc). Then runs the algorithm as a
    docker container. Finally, it monitors the container state and can return
    it's results when the algorithm finished.
    """
    log = logging.getLogger(logger_name(__name__))

    def __init__(self, image: str, vpn_manager: VPNManager, node_name: str,
                 result_id: int, tasks_dir: Path,
                 isolated_network_mgr: IsolatedNetworkManager,
                 database_uri: str, database_is_file: bool,
                 docker_volume_name: str):
        """
        Initialization creates DockerTaskManager instance

        Parameters
        ----------
        image: str
            Name of docker image to be run
        vpn_manager: VPNManager
            VPN manager required to set up traffic forwarding via VPN
        node_name: str
            Name of the node, to track running algorithms
        result_id: int
            Server result identifier
        tasks_dir: Path
            Directory in which this task's data are stored
        isolated_network_mgr: IsolatedNetworkManager
            Manager of isolated network to which algorithm needs to connect
        database_uri: str
            Location of the database
        database_is_file: bool
            Whether or not the database is a file
        docker_volume_name: str
            Name of the docker volume
        """
        self.image = image
        self.__vpn_manager = vpn_manager
        self.result_id = result_id
        self.__tasks_dir = tasks_dir
        self.__isolated_network_mgr = isolated_network_mgr
        self.__database_uri = database_uri
        self.database_is_file = database_is_file
        self.data_volume_name = docker_volume_name

        self.docker = docker.from_env()
        self.container = None
        self.status_code = None

        self.labels = {
            f"{APPNAME}-type": "algorithm",
            "node": node_name,
            "result_id": str(result_id)
        }
        self.helper_labels = self.labels
        self.helper_labels[f"{APPNAME}-type"] = "algorithm-helper"

        # FIXME: these values should be retrieved from DockerNodeContext
        #   in some way.
        self.tmp_folder = "/mnt/tmp"
        self.data_folder = "/mnt/data"

    def is_finished(self) -> bool:
        """
        Checks if algorithm container is finished

        Returns
        -------
        bool:
            True if algorithm container is finished
        """
        self.container.reload()
        return self.container.status == 'exited'

    def report_status(self) -> str:
        """
        Checks if algorithm has exited successfully. If not, it prints an
        error message

        Returns
        -------
        logs: str
            Log messages of the algorithm container
        """
        logs = self.container.logs().decode('utf8')

        # report if the container has a different status than 0
        self.status_code = self.container.attrs["State"]["ExitCode"]
        if self.status_code:
            self.log.error(f"Received non-zero exitcode: {self.status_code}")
            self.log.error(f"  Container id: {self.container.id}")
            self.log.warn("Will not remove container")
            self.log.info(logs)
        return logs

    def get_results(self) -> bytes:
        """
        Read results output file of the algorithm container

        Returns
        -------
        bytes:
            Results of the algorithm container
        """
        with open(self.output_file, "rb") as fp:
            results = fp.read()
        return results

    def pull(self):
        """ Pull the latest docker image. """
        try:
            self.log.info(f"Retrieving latest image: '{self.image}'")
            pull_if_newer(self.docker, self.image, self.log)

        except Exception as e:
            self.log.debug('Failed to pull image')
            self.log.error(e)

    def run(self, docker_input: bytes, tmp_vol_name: str, token: str,
            algorithm_env: Dict) -> int:
        """
        Runs the docker-image in detached mode.

        It will will attach all mounts (input, output and datafile) to the
        docker image. And will supply some environment variables.

        Parameters
        ----------
        docker_input: bytes
            Input that can be read by docker container
        tmp_vol_name: str
            Name of temporary docker volume assigned to the algorithm
        token: str
            Bearer token that the container can use
        algorithm_env: Dict
            Dictionary with additional environment variables to set

        Returns
        -------
        int or None:
            Port number assigned for VPN communication. None if VPN is inactive
        """
        # generate task folders
        self._make_task_folders()

        # prepare volumes
        self.volumes = self._prepare_volumes(
            docker_input, tmp_vol_name, token
        )
        self.log.debug(f"volumes: {self.volumes}")

        # setup environment variables
        self.environment_variables = \
            self._setup_environment_vars(algorithm_env=algorithm_env)

        # run the algorithm as docker container
        vpn_port = self._run_algorithm()
        return vpn_port

    def cleanup(self) -> None:
        """
        Cleanup the containers generated for this task. Only clean up the
        algorithm container if it exited successfully
        """
        # TODO cleanup temporary docker volume?
        self._remove_container(self.helper_container, kill=True)
        if not self.status_code:
            self._remove_container(self.container)

    def _run_algorithm(self) -> int:
        """
        Run the algorithm container

        Start up a helper container to complete VPN setup, pull the latest
        image and then run the algorithm

        Returns
        -------
        int or None:
            Port number assigned for VPN communication. None if VPN is inactive
        """
        vpn_port = None
        if self.__vpn_manager.has_vpn:
            # if VPN is active, network exceptions must be configured
            # First, start a container that runs indefinitely. The algorithm
            # container will run in the same network and network exceptions
            # will therefore also affect the algorithm.
            self.helper_container = self.docker.containers.run(
                command='sleep infinity',
                image='alpine',
                labels=self.helper_labels,
                network=self.__isolated_network_mgr.network_name,
                detach=True
            )
            # setup forwarding of traffic via VPN client to and from the
            # algorithm container:
            vpn_port = self.__vpn_manager.forward_vpn_traffic(
                algo_container=self.helper_container)

        # Try to pull the latest image
        self.pull()

        # attempt to run the image
        try:
            self.log.info(f"Run docker image={self.image}")
            self.container = self.docker.containers.run(
                self.image,
                detach=True,
                environment=self.environment_variables,
                network='container:' + self.helper_container.id,
                volumes=self.volumes,
                labels=self.labels
            )
        except Exception as e:
            self.log.error('Could not run docker image!?')
            self.log.error(e)
            return None

        return vpn_port

    def _make_task_folders(self) -> None:
        """ Generate task folders """
        # FIXME: We should have a separate mount/volume for this. At the
        #   moment this is a potential leak as containers might access input,
        #   output and token from other containers.
        #
        #   This was not possible yet as mounting volumes from containers
        #   is terrible when working from windows (as you have to convert
        #   from windows to unix several times...).

        # If we're running in docker __tasks_dir will point to a location on
        # the data volume.
        # Alternatively, if we're not running in docker it should point to the
        # folder on the host that can act like a data volume. In both cases,
        # we can just copy the required files to it
        self.task_folder_name = f"task-{self.result_id:09d}"
        self.task_folder_path = \
            os.path.join(self.__tasks_dir, self.task_folder_name)
        os.makedirs(self.task_folder_path, exist_ok=True)
        self.output_file = os.path.join(self.task_folder_path, "output")

    def _prepare_volumes(self, docker_input: bytes, tmp_vol_name: str,
                         token: str) -> Dict:
        """
        Generate docker volumes required to run the algorithm

        Parameters
        ----------
        docker_input: bytes
            Input that can be read by docker container
        tmp_vol_name: str
            Name of temporary docker volume assigned to the algorithm
        token: str
            Bearer token that the container can use

        Returns
        -------
        Dict:
            Volumes to support running the algorithm
        """
        if isinstance(docker_input, str):
            docker_input = docker_input.encode('utf8')

        # Create I/O files & token for the algorithm container
        self.log.debug("prepare IO files in docker volume")
        io_files = [
            ('input', docker_input),
            ('output', b''),
            ('token', token.encode("ascii")),
        ]

        for (filename, data) in io_files:
            filepath = os.path.join(self.task_folder_path, filename)

            with open(filepath, 'wb') as fp:
                fp.write(data)

        volumes = {
            tmp_vol_name: {"bind": self.tmp_folder, "mode": "rw"},
        }

        if running_in_docker():
            volumes[self.data_volume_name] = \
                {"bind": self.data_folder, "mode": "rw"}
        else:
            volumes[self.__tasks_dir] = \
                {"bind": self.data_folder, "mode": "rw"}
        return volumes

    def _setup_environment_vars(self, algorithm_env: Dict = {}) -> Dict:
        """"
        Set environment variables required to run the algorithm

        Parameters
        ----------
        algorithm_env: Dict
            Dictionary with additional environment variables to set

        Returns
        -------
        Dict:
            Environment variables required to run algorithm
        """
        try:
            proxy_host = os.environ['PROXY_SERVER_HOST']

        except Exception:
            print('-' * 80)
            print(os.environ)
            print('-' * 80)
            proxy_host = 'host.docker.internal'

        # define enviroment variables for the docker-container, the
        # host, port and api_path are from the local proxy server to
        # facilitate indirect communication with the central server
        # FIXME: we should only prepend data_folder if database_uri is a
        #   filename
        environment_variables = {
            "INPUT_FILE": f"{self.data_folder}/{self.task_folder_name}/input",
            "OUTPUT_FILE":
                f"{self.data_folder}/{self.task_folder_name}/output",
            "TOKEN_FILE": f"{self.data_folder}/{self.task_folder_name}/token",
            "TEMPORARY_FOLDER": self.tmp_folder,
            "HOST": f"http://{proxy_host}",
            "PORT": os.environ.get("PROXY_SERVER_PORT", 8080),
            "API_PATH": "",
        }
        if self.database_is_file:
            environment_variables["DATABASE_URI"] = \
                f"{self.data_folder}/{self.__database_uri}"
        else:
            environment_variables["DATABASE_URI"] = self.__database_uri
        self.log.debug(f"environment: {environment_variables}")

        # Load additional environment variables
        if algorithm_env:
            environment_variables = \
                {**environment_variables, **algorithm_env}
            self.log.info('Custom environment variables are loaded!')
            self.log.debug(f"custom environment: {algorithm_env}")
        return environment_variables

    def _remove_container(self, container: Container, kill=False) -> None:
        """
        Removes a docker container

        Parameters
        ----------
        container: Container
            The container that should be removed
        kill: bool
            Whether or not container should be killed before it is removed
        """
        try:
            if kill:
                container.kill()
            container.remove()
        except Exception as e:
            self.log.error(f"Failed to remove container {container.name}")
            self.log.debug(e)
