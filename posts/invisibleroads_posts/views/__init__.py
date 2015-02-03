from os.path import exists, join
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse


def add_routes(config):
    settings = config.registry.settings

    config.add_route('index', '')
    config.add_view(
        'invisibleroads_posts.views.list_posts',
        renderer='invisibleroads_posts:templates/posts.mako',
        route_name='index', http_cache=3600)

    config.add_route('post', '%s/{name}' % settings['posts.url'])
    config.add_view(
        'invisibleroads_posts.views.show_post',
        route_name='post', http_cache=3600)


def list_posts(request):
    settings = request.registry.settings
    path = join(settings['data.folder'], 'list_posts.html')
    if not exists(path):
        return dict()
    return FileResponse(path, request)


def show_post(request):
    settings = request.registry.settings
    path = join(settings['posts.folder'], request.matchdict['name'] + '.html')
    if not exists(path):
        raise HTTPNotFound
    return FileResponse(path, request)
