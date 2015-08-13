from importlib import import_module
from os.path import basename, isabs, join
from pyramid.config import Configurator
from pyramid.response import FileResponse
from pyramid.settings import aslist

from .libraries.cache import configure_cache
from .libraries.text import render_title
from .views import add_routes


def main(global_config, **settings):
    config = Configurator(settings=settings)
    includeme(config)
    return config.make_wsgi_app()


def includeme(config):
    configure_assets(config)
    configure_cache(config)
    configure_views(config)


def configure_assets(config):
    settings = config.registry.settings
    config.add_directive('add_root_asset', add_root_asset)
    for asset_path in aslist(settings.get('website.root_asset_paths', [])):
        config.add_root_asset(asset_path)
    config.add_static_view(
        '_/invisibleroads-posts', 'invisibleroads_posts:assets',
        cache_max_age=3600)


def configure_views(config):
    settings = config.registry.settings
    config.include('pyramid_jinja2')
    config.commit()
    template_environment = config.get_jinja2_environment()
    template_environment.globals['website_name'] = settings['website.name']
    template_environment.globals['website_sections'] = aslist(
        settings['website.sections'])
    template_environment.globals['render_title'] = render_title
    add_routes(config)


def add_root_asset(config, asset_path):
    settings = config.registry.settings
    absolute_path = resolve_asset_path(asset_path, settings['website.folder'])
    asset_name = basename(absolute_path)
    config.add_view(
        lambda request: FileResponse(absolute_path, request),
        asset_name, http_cache=3600)


def resolve_asset_path(asset_path, base_folder):
    try:
        package_name, relative_path = asset_path.split(':')
    except ValueError:
        absolute_path = asset_path if isabs(asset_path) else join(
            base_folder, asset_path)
    else:
        package_module = import_module(package_name)
        package_folder = package_module.__path__[0]
        absolute_path = join(package_folder, relative_path)
    return absolute_path
