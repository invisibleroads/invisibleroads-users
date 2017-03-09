import velruse
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from . import models as m
from .events import UserAdded


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
    params = request.params
    request.session['target_url'] = params.get('target_url', '/').strip()
    try:
        return HTTPFound(location=velruse.login_url(request, 'google'))
    except AttributeError:
        return _set_headers(params.get('email', u'user@example.com'), request)


def exit_user(request):
    params = request.params
    request.session.invalidate()
    return HTTPFound(
        location=params.get('target_url', '/').strip(),
        headers=forget(request))


def see_user(request):
    return dict(user=m.User.get_from(request))


def finish_authentication(request):
    context = request.context
    profile = context.profile
    return _set_headers(profile['verifiedEmail'], request)


def cancel_authentication(request):
    return HTTPFound(location=request.session.pop('target_url', '/'))


def _set_headers(email, request):
    database = request.database
    settings = request.registry.settings
    user = database.query(m.User).filter_by(email=email).first()
    if not user:
        user = m.User.make_unique_record(database, settings[
            'user.id.length'])
        user.email = email
        database.add(user)
        database.flush()
        request.registry.notify(UserAdded(user, request))
    return HTTPFound(
        location=request.session.pop('target_url', '/'),
        headers=remember(request, user.id))
