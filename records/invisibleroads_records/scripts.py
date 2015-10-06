import transaction
from importlib import import_module
from invisibleroads.scripts import ConfigurableScript
from pyramid.paster import bootstrap, setup_logging

from .models import Base


class RecordsScript(ConfigurableScript):

    priority = 20
    function_name = 'run'

    def run(self, args):
        setup_logging(args.configuration_path)
        env = bootstrap(args.configuration_path)
        settings = env['registry'].settings
        if 'sqlalchemy.url' not in settings:
            return
        Base.metadata.create_all()
        module_name = settings.get(
            'invisibleroads.' + self.function_name, '').strip()
        if not module_name:
            return
        module = import_module(module_name)
        function = getattr(module, self.function_name)
        function(env['request'])
        transaction.commit()


class InitializeRecordsScript(RecordsScript):

    function_name = 'initialize_records'


class UpdateRecordsScript(RecordsScript):

    function_name = 'update_records'
