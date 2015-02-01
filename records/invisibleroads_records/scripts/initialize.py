import sys
from ConfigParser import ConfigParser
from invisibleroads_macros import disk
from os.path import abspath, basename, dirname
from pyramid.paster import setup_logging
from sqlalchemy import engine_from_config

from ..models import Base, db


def main(argv=sys.argv):
    if len(argv) < 2:
        print('%s development.ini' % basename(argv[0]))
        sys.exit(1)
    configuration_path = argv[1]
    configuration_folder = abspath(dirname(configuration_path))
    setup_logging(configuration_path)

    settings = {}
    configuration = ConfigParser({'here': configuration_folder})
    configuration.read(configuration_path)
    for key in ('data.folder', 'sqlalchemy.url'):
        settings[key] = configuration.get('app:main', key)

    disk.make_folder(settings['data.folder'])
    engine = engine_from_config(settings, 'sqlalchemy.')
    db.configure(bind=engine)
    Base.metadata.create_all(engine)
