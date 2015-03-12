import sys
from invisibleroads_macros import disk
from os.path import basename
from pyramid.paster import get_app, setup_logging

from ..models import Base


def main(argv=sys.argv):
    if len(argv) < 2:
        print('%s development.ini' % basename(argv[0]))
        sys.exit(1)
    configuration_path = argv[1]
    setup_logging(configuration_path)
    app = get_app(configuration_path)
    settings = app.registry.settings
    disk.make_folder(settings['data.folder'])
    Base.metadata.create_all()
