import shutil
import sys
from argparse import ArgumentParser
from invisibleroads_macros import disk
from os.path import basename
from pyramid.paster import get_app, setup_logging

from ..models import Base


def main(argv=sys.argv):
    argument_parser = ArgumentParser()
    argument_parser.add_argument('configuration_path')
    argument_parser.add_argument('--restart', action='store_true')
    args = argument_parser.parse_args()

    setup_logging(args.configuration_path)
    app = get_app(args.configuration_path)
    settings = app.registry.settings

    if args.restart:
        shutil.rmtree(settings['data.folder'])
    for key, value in settings.iteritems():
        if key.endswith('.folder'):
            disk.make_folder(value)
    Base.metadata.create_all()
