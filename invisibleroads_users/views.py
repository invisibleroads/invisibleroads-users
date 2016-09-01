import velruse
from invisibleroads_macros.security import make_random_string
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import remember, forget
from random import choice
from string import letters

from .models import db


def add_routes(config):
    config.add_route('users', '/users')
    config.add_route('user_enter', '/users/enter')
    config.add_route('user_exit', '/users/exit')
    config.add_route('user', '/u/{user_id}')

    config.add_view(enter_user, route_name='user_enter')
    config.add_view(exit_user, route_name='user_exit')
    config.add_view(
        see_user,
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
        return _set_headers(request, u'user@example.com')


def exit_user(request):
    settings = request.registry.settings
    user_class = settings['users.user']
    user_id = request.authenticated_userid
    cached_user = user_class.get_from_cache(user_id)
    if cached_user:
        cached_user.token = _make_user_token(settings)
        db.add(cached_user)  # Reattach cached_user to session to save changes
        user_class.clear_from_cache(user_id)
    request.session.new_csrf_token()
    return HTTPFound(
        location=request.params.get('target_url', '/').strip(),
        headers=forget(request))


def see_user(request):
    settings = request.registry.settings
    user_class = settings['users.user']
    user_id = request.matchdict['id']
    cached_user = user_class.get_from_cache(user_id)
    if not cached_user:
        raise HTTPNotFound({'id': 'bad'})
    return dict(user_id=user_id)


def finish_authentication(request):
    return _set_headers(request, request.context.profile['verifiedEmail'])


def cancel_authentication(request):
    return HTTPFound(location=request.session.pop('target_url', '/'))


def _make_user_token(settings):
    length = settings['users.token_length']
    return choice(letters) + make_random_string(length - 1)


def _set_headers(request, email):
    settings = request.registry.settings
    user_class = settings['users.user']
    user = db.query(user_class).filter_by(email=email).first()
    if not user:
        user = user_class(email=email, token=_make_user_token(settings))
        db.add(user)
        db.flush()
    return HTTPFound(
        location=request.session.pop('target_url', '/'),
        headers=remember(request, user.id, tokens=[user.token]))
