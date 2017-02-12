import velruse
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from .events import UserAdded
from .settings import SETTINGS


def add_routes(config):
    config.add_route('user_enter', '/users/enter')
    config.add_route('user_exit', '/users/exit')
    config.add_route('user', '/u/{user_id}')

    config.add_view(enter_user, route_name='user_enter', require_csrf=False)
    config.add_view(exit_user, route_name='user_exit', require_csrf=False)
    config.add_view(
        see_user,
        permission='see-user',
        renderer='invisibleroads_users:templates/user.jinja2',
        route_name='user')
    config.add_view(
        finish_authentication, context='velruse.AuthenticationComplete')
    config.add_view(
        cancel_authentication, context='velruse.AuthenticationDenied')


def enter_user(request):
    request.session['target_url'] = request.params.get(
        'target_url', '/').strip()
    try:
        return HTTPFound(location=velruse.login_url(request, 'google'))
    except AttributeError:
        return _set_headers(u'user@example.com', request)


def exit_user(request):
    request.session.invalidate()
    return HTTPFound(
        location=request.params.get('target_url', '/').strip(),
        headers=forget(request))


def see_user(request):
    return dict(user=SETTINGS['user_class'].get_from(request))


def finish_authentication(request):
    return _set_headers(request.context.profile['verifiedEmail'], request)


def cancel_authentication(request):
    return HTTPFound(location=request.session.pop('target_url', '/'))


def _set_headers(email, request):
    settings = request.registry.settings
    database = request.database
    user_class = SETTINGS['user_class']
    user = database.query(user_class).filter_by(email=email).first()
    if not user:
        user = user_class.make_unique_record(
            database, settings['user.id.length'])
        user.email = email
        database.add(user)
        database.flush()
        request.registry.notify(UserAdded(user, request))
    return HTTPFound(
        location=request.session.pop('target_url', '/'),
        headers=remember(request, user.id))
