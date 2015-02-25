from sqlalchemy import engine_from_config

from .libraries.cache import configure_cache
from .models import Base, db


def includeme(config):
    configure_cache(config)
    configure_database(config)


def configure_database(config):
    settings = config.registry.settings
    engine = engine_from_config(settings, 'sqlalchemy.')
    db.configure(bind=engine)
    Base.metadata.bind = engine
    config.include('pyramid_tm')
