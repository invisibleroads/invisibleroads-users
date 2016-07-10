import velruse
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.security import remember, forget

from .models import make_ticket, db


def add_routes(config):
    config.add_route('users', '/users')
    config.add_route('user_enter', '/users/enter')
    config.add_route('user_exit', '/users/exit')
    config.add_route('user', '/u/{user_id}')

    config.add_view(show_entrance, route_name='user_enter')
    config.add_view(show_exit, route_name='user_exit')
    config.add_view(
        show_user,
        renderer='invisibleroads_users:templates/user.jinja2',
        route_name='user')
    config.add_view(
        finish_authentication, context='velruse.AuthenticationComplete')
    config.add_view(
        cancel_authentication, context='velruse.AuthenticationDenied')


def show_entrance(request):
    request.session['target_url'] = request.params.get(
        'target_url', '/').strip()
    try:
        return HTTPFound(location=velruse.login_url(request, 'google'))
    except AttributeError:
        return _set_headers(request, u'user@example.com')


def show_exit(request):
    settings = request.registry.settings
    user_class = settings['users.user']
    user_id = request.authenticated_userid
    cached_user = user_class.get_from_cache(user_id)
    if cached_user:
        cached_user.ticket = make_ticket()
        db.add(cached_user)  # Reattach cached_user to session to save changes
        user_class.clear_from_cache(user_id)
    request.session.new_csrf_token()
    return HTTPFound(
        location=request.params.get('target_url', '/').strip(),
        headers=forget(request))


def show_user(request):
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


def get_ticket(request):
    registry = request.registry
    authentication_policy = registry.queryUtility(IAuthenticationPolicy)
    try:
        return authentication_policy.cookie.identify(request)['tokens'][0]
    except (TypeError, IndexError):
        return ''


def _set_headers(request, email):
    settings = request.registry.settings
    user_class = settings['users.user']
    user = db.query(user_class).filter_by(email=email).first()
    if not user:
        user = user_class(email=email)
        db.add(user)
        db.flush()
    return HTTPFound(
        location=request.session.pop('target_url', '/'),
        headers=remember(request, user.id, tokens=[user.ticket]))
