import uuid

from . import logger
from ..config import config

import tempfile
import subprocess
import time
# from appdirs import user_data_dir
# from pathlib import Path
import os
import psycopg2
import docker
from sqlalchemy import create_engine

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 importlib_resources.
    import importlib_resources as pkg_resources


from . import resources

with pkg_resources.path(resources, 'docker-compose_view_factor.yml') as r_path:
    view_factor_compose_template_filename = str(r_path)

with pkg_resources.path(resources, 'docker-compose_shading.yml') as r_path:
    shading_compose_template_filename = str(r_path)

with pkg_resources.path(resources, 'docker-compose_db.yml') as r_path:
    db_compose_template_filename = str(r_path)


class DatabaseService(object):

    name = 'PSR_Database_Service'

    def __init__(self, *args, **kwargs):

        self._shared_dir = None
        self._engine = None
        # self._workdir = kwargs.get('workdir', None)

        self.port = kwargs.get('port', 9006)
        self.user = kwargs.get('user', 'admin')
        self.password = kwargs.get('password', 'admin')
        self.db_name = kwargs.get('db_name', 'shading')

        self.log_dir = kwargs.get('log_dir', 'logs')
        self.logging_mode = kwargs.get('logging_mode', 'DEBUG')

        self._db_compose_file_name = None

        self.running = False

        self.keep_running = kwargs.get('keep_running', False)

        self._volume = None
        self.docker_client = docker.from_env()
        self.persist_volume = kwargs.get('persist_volume', False)

    @property
    def engine(self):
        if self._engine is None:
            engine = create_engine(
                f'postgresql://{self.user}:{self.password}@localhost:{self.port}/{self.db_name}',
                pool_pre_ping=True)
            engine.dispose()
            self._engine = engine
        return self._engine

    @property
    def volume(self):
        if self._volume is None:
            volume = next((x for x in self.docker_client.volumes.list() if x.name == f'PSR_{self.user}'), None)
            if volume is None:
                logger.info(f'Creating database volume...')
                self._volume = self.docker_client.volumes.create(name=f'PSR_{self.user}', driver='local')
                logger.info(f'Created database volume {self._volume.name}')
            else:
                self._volume = volume
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value

    # @property
    # def workdir(self):
    #
    #     if self._workdir is None:
    #         # check if directory exist, otherwise create
    #         # data_path = user_data_dir('PySimultanRadiation', 'TU_Wien')
    #         data_path = db_path
    #         workdir = Path(data_path, 'db', str(self.user))
    #         workdir.mkdir(parents=True, exist_ok=True)
    #         self._workdir = str(workdir)
    #     return self._workdir

    @property
    def shared_dir(self):
        if self._shared_dir is None:
            self._shared_dir = tempfile.TemporaryDirectory(prefix=f'{self.name}_')
            time.sleep(1)
        return self._shared_dir

    @shared_dir.setter
    def shared_dir(self, value):
        self._shared_dir = value

    @property
    def db_compose_file_name(self):
        if self._db_compose_file_name is None:
            self._db_compose_file_name = os.path.join(self.shared_dir.name, 'db_docker_compose.yml')
        return self._db_compose_file_name

    @db_compose_file_name.setter
    def db_compose_file_name(self, value):
        self._db_compose_file_name = value

    def write_db_compose_file(self, filename):

        with open(db_compose_template_filename, 'r') as f:
            compose_template = f.read()

        compose_template = compose_template.replace('<DB_BIND_VOLUME>', self.volume.name)
        compose_template = compose_template.replace('<DB_PORT>', str(self.port))
        compose_template = compose_template.replace('<UserDBName>', str(self.user))
        compose_template = compose_template.replace('<UserDBPassword>', str(self.password))
        compose_template = compose_template.replace('<DBName>', self.db_name)

        with open(filename, 'wt') as f_out:
            f_out.write(compose_template)

    def shut_down_db_service(self):

        folder_name = os.path.basename(os.path.normpath(self.shared_dir.name))
        logger.info(f'Shutting down db compose {folder_name} on port {self.port}...')

        cmd = config.docker_path + ' compose ' + f" -f {self.db_compose_file_name} -p {folder_name} down --remove-orphans"
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if result.returncode:
            logger.error(f"Command Result: {result.stderr}")
        else:
            logger.debug(f"Command Result: {result.stderr}")
            logger.info(f"Database service successfully shut down")

            self.shared_dir.cleanup()
            self.shared_dir = None
            self.db_compose_file_name = None
            self.running = False

        if not self.persist_volume:
            if self.volume is not None:
                logger.info(f'Removing volume {self.volume.name}')
                self.volume.remove()
                self.volume = None

    def start_database_service(self):
        logger.info(f"Starting database container on port: {self.port}...")
        self.write_db_compose_file(self.db_compose_file_name)

        annot_mark = '\"'
        cmd = config.docker_path + ' compose ' + "-f " + f"{annot_mark}{self.db_compose_file_name}{annot_mark}" + " up" + " -d"
        result = subprocess.run(cmd,
                                capture_output=True,
                                text=True,
                                shell=True)
        if result.returncode:
            logger.error(f"Command Result: {result.stderr}\nfor \n\n{cmd}")
            self.shut_down_db_service()
        else:
            logger.debug(f"Command Result: {result.stderr}")
            logger.info(f"Database service successfully started")
            self.running = True

        conn_ok = self.test_connection()
        start_time = time.time()
        while (not conn_ok) and ((time.time() - start_time) < 10):
            conn_ok = self.test_connection()
        if not conn_ok and ((time.time() - start_time) > 10):
            raise Exception(f'Could not connect to database')

    def __enter__(self):
        if not self.running:
            self.start_database_service()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.running and not self.keep_running:
            self.shut_down_db_service()

    def __del__(self):
        if self.running:
            self.shut_down_db_service()

    def test_connection(self):

        try:
            conn = self.get_connection({'connect_timeout': 1})
            # conn = psycopg2.connect(dbname=self.db_name,
            #                         user=self.user,
            #                         host='localhost',
            #                         port=self.port,
            #                         password=self.password,
            #                         connect_timeout=1)
            conn.close()
            return True
        except:
            return False

    def get_connection(self, kwargs):
        conn = psycopg2.connect(dbname=self.db_name,
                                user=self.user,
                                host='localhost',
                                port=self.port,
                                password=self.password, **kwargs)
        return conn


class WorkerService(object):

    name = 'PSR_WorkerService'
    compose_template_filename = None

    def __init__(self, *args, **kwargs):

        self.port = kwargs.get('port')
        self.num_workers = kwargs.get('num_workers')

        self.frontend_port = kwargs.get('frontend_port', 8016)
        self.backend_port = kwargs.get('backend_port', 9016)

        self.log_dir = kwargs.get('log_dir', 'logs')
        self.logging_mode = kwargs.get('logging_mode', 'DEBUG')

        self._shared_dir = None
        self._compose_file_name = None

        self.running = False

        self._volume = None
        self.docker_client = docker.from_env()

        # view_factor_worker ftp_server
        self.ftp_port_1 = kwargs.get('ftp_port_1')
        self.ftp_port_2 = kwargs.get('ftp_port_2')
        self.ftp_passive_ports = kwargs.get('ftp_passive_ports')
        self.ftp_user = kwargs.get('ftp_user')
        self.ftp_password = kwargs.get('ftp_password')

    @property
    def volume(self):
        if self._volume is None:
            logger.info(f'Creating client volume...')
            self._volume = self.docker_client.volumes.create(name=f'{self.name}_{str(uuid.uuid4())}', driver='local')
            logger.info(f'Created client volume {self._volume.name}')
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value

    @property
    def shared_dir(self):
        if self._shared_dir is None:
            self._shared_dir = tempfile.TemporaryDirectory(prefix=f'{self.name}_')
            time.sleep(1)
        return self._shared_dir

    @shared_dir.setter
    def shared_dir(self, value):
        self._shared_dir = value

    @property
    def compose_file_name(self):
        if self._compose_file_name is None:
            self._compose_file_name = os.path.join(self.shared_dir.name, 'docker_compose.yml')
        return self._compose_file_name

    @compose_file_name.setter
    def compose_file_name(self, value):
        self._compose_file_name = value

    def write_compose_file(self, filename):

        with open(self.compose_template_filename, 'r') as f:
            compose_template = f.read()

        compose_template = compose_template.replace('<port>', str(self.port))
        compose_template = compose_template.replace('<FRONTEND_PORT>', str(self.frontend_port))
        compose_template = compose_template.replace('<BACKEND_PORT>', str(self.backend_port))

        compose_template = compose_template.replace('<LOG_DIR>', self.log_dir)
        compose_template = compose_template.replace('<SERVER_LOG_MODE>', self.logging_mode)

        compose_template = compose_template.replace('<BIND_VOLUME>', self.volume.name)

        compose_template = compose_template.replace('<WORKER_LOG_MODE>', self.logging_mode)

        compose_template = compose_template.replace('<NUM_WORKERS>', str(self.num_workers))

        # ftp
        compose_template = compose_template.replace('<FTP_Port1>', str(self.ftp_port_1))
        compose_template = compose_template.replace('<FTP_Port2>', str(self.ftp_port_2))
        compose_template = compose_template.replace('<UserName>', str(self.ftp_user))
        compose_template = compose_template.replace('<UserPassword>', str(self.ftp_password))
        compose_template = compose_template.replace('<FTP_PassivePorts>', str(self.ftp_passive_ports))

        with open(filename, 'wt') as f_out:
            f_out.write(compose_template)

    def start_service(self):

        logger.info(f"Starting {self.name} with {self.num_workers} workers on port: {self.frontend_port}...")
        self.write_compose_file(self.compose_file_name)

        cmd = config.docker_path + ' compose ' + '-f ' + self.compose_file_name + ' up -d'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if result.returncode:
            logger.error(f"Command Result: {result.stderr}\nfor \n\n{cmd}")
            self.shut_down_service()
        else:
            logger.debug(f"Command Result: {result.stderr}")
            logger.info(f"{self.name} successfully started")
            self.running = True

    def shut_down_service(self):

        folder_name = os.path.basename(os.path.normpath(self.shared_dir.name))
        logger.info(f'Shutting down {self.name} compose {folder_name} on port {self.frontend_port}...')

        cmd = config.docker_path + ' compose ' + f'-f {self.compose_file_name} -p {folder_name} down --remove-orphans'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if result.returncode:
            logger.error(f"Command Result: {result.stderr}")
        else:
            logger.debug(f"Command Result: {result.stderr}")
            logger.info(f"{self.name} successfully shut down")
            self.running = False

            self.shared_dir.cleanup()
            self.shared_dir = None
            self.compose_file_name = None

        if self.volume is not None:
            logger.info(f'Removing volume {self.volume.name}')
            try:
                self.volume.remove()
                self.volume = None
                logger.info(f'Volume removed')
            except Exception as e:
                logger.error(f'Error removing volume {self.volume.name}:\n{e}')

    def __enter__(self):

        if not self.running:
            self.start_service()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.running:
            self.shut_down_service()

    def __del__(self):
        if self.running:
            self.shut_down_service()


class ShadingService(WorkerService):

    name = 'PSR_ShadingWorkerService'
    compose_template_filename = shading_compose_template_filename

    def __init__(self, *args, **kwargs):
        WorkerService.__init__(self, *args, **kwargs)


class ViewFactorService(WorkerService):

    name = 'PSR_ViewFactorService'
    compose_template_filename = view_factor_compose_template_filename

    def __init__(self, *args, **kwargs):
        WorkerService.__init__(self, *args, **kwargs)


# class ShadingService(object):
#
#     def __init__(self, *args, **kwargs):
#
#         self.port = kwargs.get('port')
#         # self.workdir = kwargs.get('workdir')
#         self.num_workers = kwargs.get('num_workers')
#
#         self.frontend_port = kwargs.get('frontend_port', 8006)
#         self.backend_port = kwargs.get('backend_port', 9006)
#
#         self.log_dir = kwargs.get('log_dir', 'logs')
#         self.logging_mode = kwargs.get('logging_mode', 'DEBUG')
#
#         self._shared_dir = None
#         self._compose_file_name = None
#
#         self.running = False
#
#         self._volume = None
#         self.docker_client = docker.from_env()
#
#         # shading_worker ftp_server
#         self.ftp_port_1 = kwargs.get('ftp_port_1')
#         self.ftp_port_2 = kwargs.get('ftp_port_2')
#         self.ftp_passive_ports = kwargs.get('ftp_passive_ports')
#         self.ftp_user = kwargs.get('ftp_user')
#         self.ftp_password = kwargs.get('ftp_password')
#
#     @property
#     def volume(self):
#         if self._volume is None:
#             logger.info(f'Creating client volume...')
#             self._volume = self.docker_client.volumes.create(name=str(uuid.uuid4()), driver='local')
#             logger.info(f'Created client volume {self._volume.name}')
#         return self._volume
#
#     @volume.setter
#     def volume(self, value):
#         self._volume = value
#
#     @property
#     def shared_dir(self):
#         if self._shared_dir is None:
#             self._shared_dir = tempfile.TemporaryDirectory()
#             time.sleep(1)
#         return self._shared_dir
#
#     @shared_dir.setter
#     def shared_dir(self, value):
#         self._shared_dir = value
#
#     @property
#     def compose_file_name(self):
#         if self._compose_file_name is None:
#             self._compose_file_name = os.path.join(self.shared_dir.name, 'docker_compose.yml')
#         return self._compose_file_name
#
#     @compose_file_name.setter
#     def compose_file_name(self, value):
#         self._compose_file_name = value
#
#     def write_compose_file(self, filename):
#
#         with open(compose_template_filename, 'r') as f:
#             compose_template = f.read()
#
#         compose_template = compose_template.replace('<port>', str(self.port))
#         compose_template = compose_template.replace('<FRONTEND_PORT>', str(self.frontend_port))
#         compose_template = compose_template.replace('<BACKEND_PORT>', str(self.backend_port))
#
#         compose_template = compose_template.replace('<LOG_DIR>', self.log_dir)
#         compose_template = compose_template.replace('<SERVER_LOG_MODE>', self.logging_mode)
#
#         compose_template = compose_template.replace('<BIND_VOLUME>', self.volume.name)
#
#         compose_template = compose_template.replace('<WORKER_LOG_MODE>', self.logging_mode)
#
#         compose_template = compose_template.replace('<NUM_WORKERS>', str(self.num_workers))
#
#         # ftp
#         compose_template = compose_template.replace('<FTP_Port1>', str(self.ftp_port_1))
#         compose_template = compose_template.replace('<FTP_Port2>', str(self.ftp_port_2))
#         compose_template = compose_template.replace('<UserName>', str(self.ftp_user))
#         compose_template = compose_template.replace('<UserPassword>', str(self.ftp_password))
#         compose_template = compose_template.replace('<FTP_PassivePorts>', str(self.ftp_passive_ports))
#
#         with open(filename, 'wt') as f_out:
#             f_out.write(compose_template)
#
#     def start_service(self):
#
#         logger.info(f"Starting shading service with {self.num_workers} workers on port: {self.frontend_port}...")
#         self.write_compose_file(self.compose_file_name)
#
#         cmd = config.docker_path + ' compose ' + '-f ' + self.compose_file_name + ' up -d'
#         result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
#         if result.returncode:
#             logger.error(f"Command Result: {result.stderr}\nfor \n\n{cmd}")
#             self.shut_down_service()
#         else:
#             logger.debug(f"Command Result: {result.stderr}")
#             logger.info(f"Shading service successfully started")
#             self.running = True
#
#     def shut_down_service(self):
#
#         folder_name = os.path.basename(os.path.normpath(self.shared_dir.name))
#         logger.info(f'Shutting down shading compose {folder_name} on port {self.frontend_port}...')
#
#         cmd = config.docker_path + ' compose ' + f'-f {self.compose_file_name} -p {folder_name} down --remove-orphans'
#         result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
#         if result.returncode:
#             logger.error(f"Command Result: {result.stderr}")
#         else:
#             logger.debug(f"Command Result: {result.stderr}")
#             logger.info(f"Shading service successfully shut down")
#             self.running = False
#
#             self.shared_dir.cleanup()
#             self.shared_dir = None
#             self.compose_file_name = None
#
#         if self.volume is not None:
#             logger.info(f'Removing volume {self.volume.name}')
#             try:
#                 self.volume.remove()
#                 self.volume = None
#                 logger.info(f'Volume removed')
#             except Exception as e:
#                 logger.error(f'Error removing volume {self.volume.name}:\n{e}')
#
#     def __enter__(self):
#
#         if not self.running:
#             self.start_service()
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if self.running:
#             self.shut_down_service()
#
#     def __del__(self):
#         if self.running:
#             self.shut_down_service()


# class ViewFactorService(object):
#
#     def __init__(self, *args, **kwargs):
#
#         self.port = kwargs.get('port')
#         self.num_workers = kwargs.get('num_workers')
#
#         self.frontend_port = kwargs.get('frontend_port', 8016)
#         self.backend_port = kwargs.get('backend_port', 9016)
#
#         self.log_dir = kwargs.get('log_dir', 'logs')
#         self.logging_mode = kwargs.get('logging_mode', 'DEBUG')
#
#         self._shared_dir = None
#         self._compose_file_name = None
#
#         self.running = False
#
#         self._volume = None
#         self.docker_client = docker.from_env()
#
#         # view_factor_worker ftp_server
#         self.ftp_port_1 = kwargs.get('ftp_port_1')
#         self.ftp_port_2 = kwargs.get('ftp_port_2')
#         self.ftp_passive_ports = kwargs.get('ftp_passive_ports')
#         self.ftp_user = kwargs.get('ftp_user')
#         self.ftp_password = kwargs.get('ftp_password')
#
#     @property
#     def volume(self):
#         if self._volume is None:
#             logger.info(f'Creating client volume...')
#             self._volume = self.docker_client.volumes.create(name=str(uuid.uuid4()), driver='local')
#             logger.info(f'Created client volume {self._volume.name}')
#         return self._volume
#
#     @volume.setter
#     def volume(self, value):
#         self._volume = value
#
#     @property
#     def shared_dir(self):
#         if self._shared_dir is None:
#             self._shared_dir = tempfile.TemporaryDirectory()
#             time.sleep(1)
#         return self._shared_dir
#
#     @shared_dir.setter
#     def shared_dir(self, value):
#         self._shared_dir = value
#
#     @property
#     def compose_file_name(self):
#         if self._compose_file_name is None:
#             self._compose_file_name = os.path.join(self.shared_dir.name, 'docker_compose.yml')
#         return self._compose_file_name
#
#     @compose_file_name.setter
#     def compose_file_name(self, value):
#         self._compose_file_name = value
#
#     def write_compose_file(self, filename):
#
#         with open(view_factor_compose_template_filename, 'r') as f:
#             compose_template = f.read()
#
#         compose_template = compose_template.replace('<port>', str(self.port))
#         compose_template = compose_template.replace('<FRONTEND_PORT>', str(self.frontend_port))
#         compose_template = compose_template.replace('<BACKEND_PORT>', str(self.backend_port))
#
#         compose_template = compose_template.replace('<LOG_DIR>', self.log_dir)
#         compose_template = compose_template.replace('<SERVER_LOG_MODE>', self.logging_mode)
#
#         compose_template = compose_template.replace('<BIND_VOLUME>', self.volume.name)
#
#         compose_template = compose_template.replace('<WORKER_LOG_MODE>', self.logging_mode)
#
#         compose_template = compose_template.replace('<NUM_WORKERS>', str(self.num_workers))
#
#         # ftp
#         compose_template = compose_template.replace('<FTP_Port1>', str(self.ftp_port_1))
#         compose_template = compose_template.replace('<FTP_Port2>', str(self.ftp_port_2))
#         compose_template = compose_template.replace('<UserName>', str(self.ftp_user))
#         compose_template = compose_template.replace('<UserPassword>', str(self.ftp_password))
#         compose_template = compose_template.replace('<FTP_PassivePorts>', str(self.ftp_passive_ports))
#
#         with open(filename, 'wt') as f_out:
#             f_out.write(compose_template)
#
#     def start_service(self):
#
#         logger.info(f"Starting view factor service with {self.num_workers} workers on port: {self.frontend_port}...")
#         self.write_compose_file(self.compose_file_name)
#
#         cmd = config.docker_path + ' compose ' + '-f ' + self.compose_file_name + ' up -d'
#         result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
#         if result.returncode:
#             logger.error(f"Command Result: {result.stderr}\nfor \n\n{cmd}")
#             self.shut_down_service()
#         else:
#             logger.debug(f"Command Result: {result.stderr}")
#             logger.info(f"Shading service successfully started")
#             self.running = True
#
#     def shut_down_service(self):
#
#         folder_name = os.path.basename(os.path.normpath(self.shared_dir.name))
#         logger.info(f'Shutting down view factor compose {folder_name} on port {self.frontend_port}...')
#
#         cmd = config.docker_path + ' compose ' + f'-f {self.compose_file_name} -p {folder_name} down --remove-orphans'
#         result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
#         if result.returncode:
#             logger.error(f"Command Result: {result.stderr}")
#         else:
#             logger.debug(f"Command Result: {result.stderr}")
#             logger.info(f"View factor service successfully shut down")
#             self.running = False
#
#             self.shared_dir.cleanup()
#             self.shared_dir = None
#             self.compose_file_name = None
#
#         if self.volume is not None:
#             logger.info(f'Removing volume {self.volume.name}')
#             try:
#                 self.volume.remove()
#                 self.volume = None
#                 logger.info(f'Volume removed')
#             except Exception as e:
#                 logger.error(f'Error removing volume {self.volume.name}:\n{e}')
#
#     def __enter__(self):
#
#         if not self.running:
#             self.start_service()
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if self.running:
#             self.shut_down_service()
#
#     def __del__(self):
#         if self.running:
#             self.shut_down_service()
