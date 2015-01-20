from pyramid.config import Configurator
from pyramid.settings import asbool


def main(global_config, **settings):
    config = Configurator(settings=settings)
    includeme(config)
    return config.make_wsgi_app()


def includeme(config):
    settings = config.registry.settings
    config.in_development = asbool(settings.get(
        'pyramid.reload_templates', False))
    configure_views(config)


def configure_views(config):
    config.include('pyramid_mako')
    config.include('invisibleroads_posts.views')
    config.add_static_view(
        '_', 'invisibleroads_posts:assets', cache_max_age=3600)
    config.scan()
