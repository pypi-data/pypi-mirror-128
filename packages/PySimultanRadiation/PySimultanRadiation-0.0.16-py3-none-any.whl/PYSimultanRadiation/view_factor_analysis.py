import os
import sys
import meshio
import traceback
from .client.client import Client, next_free_port

from . import logger

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 importlib_resources.
    import importlib_resources as pkg_resources

from . import resources

with pkg_resources.path(resources, 'shading_analysis_template.yml') as r_path:
    template_filename = str(r_path)


class ShadingAnalysis(object):

    def __init__(self, *args, **kwargs):

        self._geo_model = None
        self._scene = None
        self._mesh = None

        self.user_name = kwargs.get('user_name', 'admin')
        self.password = kwargs.get('password', 'admin')

        self.project_filename = kwargs.get('project_filename')
        self.template_filename = kwargs.get('template_filename', template_filename)

        self.template_parser = kwargs.get('template_parser', None)
        self.data_model = kwargs.get('data_model', None)
        self.typed_data = kwargs.get('typed_data', None)

        self.setup_component = kwargs.get('setup_component', None)

        self._shading_service = None
        self._db_service = None

        self._db_interface = None

        self.app = kwargs.get('app', None)

    @property
    def mesh(self):
        if self._mesh is None:
            if bool(self.setup_component.run_configuration.PersistDB) and not (
            bool(self.setup_component.run_configuration.RunMeshing)):
                mesh = None
                try:
                    mesh = self.read_mesh_from_db()
                except Exception as e:
                    logger.error(
                        f'Error reading mesh from database:\n{e}\n{traceback.format_exc()}\n{sys.exc_info()[2]}')
                if isinstance(mesh, meshio.Mesh):
                    logger.info(f'Found mesh')
                    self._mesh = mesh
                else:
                    self._mesh = self.generate_mesh()
                    with self.db_service:
                        self.write_mesh_to_db(self._mesh)
            else:
                self._mesh = self.generate_mesh()
                if bool(self.setup_component.run_configuration.PersistDB):
                    with self.db_service:
                        self.write_mesh_to_db(self._mesh)

        return self._mesh

    def read_mesh_from_db(self):

        logger.info(f'Loading mesh from database...')

        with self.db_service:
            return self.db_interface.load_object('view_factor_mesh')

    @property
    def db_service(self):
        if self._db_service is None:
            serv_work_workdir = os.path.join(self.setup_component.run_configuration.ExportDirectory, 'serv_work_workdir')
            port = next_free_port(port=9006, max_port=65535)
            logger.debug(f'database port is {port}')

            self._db_service = DatabaseService(port=port,
                                               user=self.user_name,
                                               password=self.password,
                                               db_name=self.db_name,
                                               log_dir=os.path.join(serv_work_workdir, 'logs'),
                                               logging_mode=self.setup_component.run_configuration.LogLevel,
                                               persist_volume=self.setup_component.run_configuration.PersistDB)
        return self._db_service

    @db_service.setter
    def db_service(self, value):
        self._db_service = value
