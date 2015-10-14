import velruse
from pyramid.httpexceptions import (
    HTTPFound, HTTPMovedPermanently, HTTPNotFound)
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.security import remember, forget

from .models import User, make_ticket, db


def add_routes(config):
    config.add_route('user_login', 'users/login')
    config.add_route('user_logout', 'users/logout')
    config.add_route('users', 'users')
    config.add_route('user', 'users/{id}')
    config.add_route('wee_user', 'u/{id}')

    config.add_view(login, route_name='user_login')
    config.add_view(finish_login, context='velruse.AuthenticationComplete')
    config.add_view(cancel_login, context='velruse.AuthenticationDenied')
    config.add_view(logout, route_name='user_logout')
    config.add_view(redirect_to_wee_user, route_name='user')
    config.add_view(
        show,
        renderer='invisibleroads_users:templates/user.jinja2',
        route_name='wee_user')


def login(request):
    request.session['target_url'] = request.params.get('target_url', '/')
    try:
        return HTTPFound(location=velruse.login_url(request, 'google'))
    except AttributeError:
        return set_headers(request, u'user@example.com')


def finish_login(request):
    return set_headers(request, request.context.profile['verifiedEmail'])


def cancel_login(request):
    return HTTPFound(location=request.session.pop('target_url', '/'))


def logout(request):
    user_id = request.authenticated_userid
    cached_user = User.get_from_cache(user_id)
    if cached_user:
        cached_user.ticket = make_ticket()
        db.add(cached_user)  # Reattach cached_user to session to save changes
        User.clear_from_cache(user_id)
    request.session.new_csrf_token()
    return HTTPFound(
        location=request.params.get('target_url', '/'),
        headers=forget(request))


def redirect_to_wee_user(request):
    user = check_user(request.matchdict['id'])
    return HTTPMovedPermanently(location=request.route_path(
        'wee_user', id=user.id))


def show(request):
    check_user(request.matchdict['id'])
    return {}


def set_headers(request, email):
    user = db.query(User).filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.add(user)
        db.flush()
    return HTTPFound(
        location=request.session.pop('target_url', '/'),
        headers=remember(request, user.id, tokens=[user.ticket]))


def get_ticket(request):
    registry = request.registry
    authentication_policy = registry.queryUtility(IAuthenticationPolicy)
    try:
        return authentication_policy.cookie.identify(request)['tokens'][0]
    except (TypeError, IndexError):
        return ''


def check_user(user_id):
    cached_user = User.get_from_cache(user_id)
    if not cached_user:
        raise HTTPNotFound({'id': 'bad_user_id'})
    return cached_user
