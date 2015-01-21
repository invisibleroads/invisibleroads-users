from os.path import exists, join
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse
from pyramid.view import view_config


def includeme(config):
    settings = config.registry.settings
    config.add_route('index', '')
    config.add_route('post', '/%s/{name}' % settings['posts.url'])


@view_config(
    renderer='invisibleroads_posts:templates/index.mako',
    route_name='index', http_cache=3600)
def index(request):
    settings = request.registry.settings
    path = join(settings['data.folder'], 'index.html')
    if not exists(path):
        return dict()
    return FileResponse(path, request)


@view_config(route_name='post', http_cache=3600)
def post(request):
    settings = request.registry.settings
    path = join(settings['posts.folder'], request.matchdict['name'] + '.html')
    if not exists(path):
        raise HTTPNotFound
    return FileResponse(path, request)
