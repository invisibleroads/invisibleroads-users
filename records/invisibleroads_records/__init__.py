from sqlalchemy import engine_from_config

from .models import Base, db


def includeme(config):
    settings = config.registry.settings
    engine = engine_from_config(settings, 'sqlalchemy.')
    db.configure(bind=engine)
    Base.metadata.bind = engine
    config.include('pyramid_tm')
