import transaction
from importlib import import_module
from invisibleroads.scripts import InvisibleRoadsScript
from pyramid.paster import get_app, setup_logging

from .models import Base


class RecordsInitializationScript(InvisibleRoadsScript):

    priority = 20

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
        for setting in ['invisibleroads.initialize_records']:
            function_definition = settings.get(setting)
            if not function_definition:
                continue
            module_name, function_name = function_definition.rsplit('.', 1)
            module = import_module(module_name)
            function = getattr(module, function_name)
            function()
        transaction.commit()
