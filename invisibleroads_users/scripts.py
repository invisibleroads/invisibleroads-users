from invisibleroads.scripts import ConfigurableScript
from invisibleroads_macros.configuration import resolve_attribute
from pyramid.paster import get_appsettings


class UsersScript(ConfigurableScript):

    priority = 15

    def run(self, args):
        settings = get_appsettings(args.configuration_path)
        user_class_spec = settings.get('users.user')
        if not user_class_spec:
            return
        resolve_attribute(user_class_spec)
