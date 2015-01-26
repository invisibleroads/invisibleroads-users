from importlib import import_module
from os.path import basename, isabs, join
from pyramid.config import Configurator
from pyramid.response import FileResponse
from pyramid.settings import asbool, aslist


def main(global_config, **settings):
    config = Configurator(settings=settings)
    includeme(config)
    return config.make_wsgi_app()


def includeme(config):
    settings = config.registry.settings
    config.in_development = asbool(settings.get(
        'pyramid.reload_templates', False))
    configure_assets(config)
    configure_views(config)


def configure_assets(config):
    settings = config.registry.settings
    config.add_directive('add_root_asset', add_root_asset)
    config.add_static_view(
        '_', 'invisibleroads_posts:assets', cache_max_age=3600)
    root_asset_paths = aslist(settings.get('posts.root_asset_paths', []))
    for root_asset_path in root_asset_paths:
        config.add_root_asset(root_asset_path)


def configure_views(config):
    config.include('pyramid_mako')
    config.include('invisibleroads_posts.views')
    config.scan()


def add_root_asset(config, asset_path):
    settings = config.registry.settings
    absolute_path = resolve_asset_path(asset_path, settings['here'])
    asset_name = basename(absolute_path)
    config.add_route(asset_name, '/' + asset_name)
    config.add_view(
        lambda request: FileResponse(absolute_path, request), asset_name)


def resolve_asset_path(asset_path, base_folder):
    try:
        package_name, relative_path = asset_path.split(':')
    except ValueError:
        absolute_path = asset_path if isabs(asset_path) else join(
            base_folder, asset_path)
    else:
        package_module = import_module(package_name)
        package_folder = package_module.__path__[0]
        absolute_path = join(package_folder, asset_path)
    return absolute_path
