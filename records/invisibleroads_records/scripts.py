import transaction
from importlib import import_module
from invisibleroads.scripts import InvisibleRoadsScript
from pyramid.paster import get_app, setup_logging

from .models import Base


class RecordsScript(InvisibleRoadsScript):

    priority = 20
    function_name = 'run'

    def configure(self, argument_subparser):
        if not argument_subparser.has_argument('configuration_path'):
            argument_subparser.add_argument('configuration_path')

    def run(self, args):
        setup_logging(args.configuration_path)
        app = get_app(args.configuration_path)
        settings = app.registry.settings
        if 'sqlalchemy.url' not in settings:
            return
        Base.metadata.create_all()
        module_name = settings.get(
            'invisibleroads.' + self.function_name).strip()
        if not module_name:
            return
        module = import_module(module_name)
        function = getattr(module, self.function_name)
        function()
        transaction.commit()


class InitializeRecordsScript(RecordsScript):

    function_name = 'initialize_records'


class UpdateRecordsScript(RecordsScript):

    function_name = 'update_records'
