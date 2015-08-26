from invisibleroads.scripts import InvisibleRoadsScript
from invisibleroads_macros.disk import make_folder, remove_folder
from pyramid.paster import get_appsettings


class PostsInitializationScript(InvisibleRoadsScript):

    priority = 10

    def configure(self, argument_subparser):
        argument_subparser.add_argument('configuration_path')
        argument_subparser.add_argument('--restart', action='store_true')

    def run(self, args):
        settings = get_appsettings(args.configuration_path)
        if args.restart and 'data.folder' in settings:
            remove_folder(settings['data.folder'])
        for key, value in settings.iteritems():
            if key.endswith('.folder'):
                make_folder(value)