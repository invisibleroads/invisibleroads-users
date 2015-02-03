import velruse
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound
from pyramid.interfaces import IAuthenticationPolicy

from .models import User, make_ticket, db


def add_routes(config):
    config.add_route('user_login', 'users/login')
    config.add_view(
        'invisibleroads_users.views.login_user',
        route_name='user_login')
    config.add_view(
        'invisibleroads_users.views.finish_login',
        context='velruse.AuthenticationComplete')
    config.add_view(
        'invisibleroads_users.views.cancel_login',
        context='velruse.AuthenticationDenied')

    config.add_route('user_logout', 'users/logout')
    config.add_view(
        'invisibleroads_users.views.logout_user',
        route_name='user_logout')


def login_user(request):
    request.session['target_url'] = request.params.get('target_url', '')
    try:
        return HTTPFound(location=velruse.login_url(request, 'google'))
    except AttributeError:
        return set_headers(request, u'user@example.com')


def logout_user(request):
    user_id = request.authenticated_userid
    try:
        user = User.get(user_id)
    except TypeError:
        pass
    else:
        user.ticket = make_ticket()
    request.session.new_csrf_token()
    return HTTPFound(
        location=request.params.get('target_url', ''),
        headers=forget(request))


def finish_login(request):
    return set_headers(request, request.context.profile['verifiedEmail'])


def cancel_login(request):
    return HTTPFound(location=request.session.pop('target_url', ''))


def set_headers(request, email):
    user = db.query(User).filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.add(user)
        db.flush()
    return HTTPFound(
        location=request.session.pop('target_url', ''),
        headers=remember(request, user.id, tokens=[user.ticket]))


def get_ticket(request):
    registry = request.registry
    authentication_policy = registry.queryUtility(IAuthenticationPolicy)
    try:
        return authentication_policy.cookie.identify(request)['tokens'][0]
    except (TypeError, IndexError):
        return ''
