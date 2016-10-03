import velruse
from invisibleroads_macros.security import make_random_string
from invisibleroads_records.models import get_unique_instance
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import remember, forget
from random import choice
from string import letters


def add_routes(config):
    config.add_route('users', '/users')
    config.add_route('user_enter', '/users/enter')
    config.add_route('user_exit', '/users/exit')
    config.add_route('user', '/u/{user_id}')

    config.add_view(enter_user, route_name='user_enter', require_csrf=False)
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
    database = request.database
    user_id = request.authenticated_userid

    user_class = settings['users.class']
    cached_user = user_class.get_from_cache(user_id, database)
    if cached_user:
        cached_user.token = _make_user_token(settings)
        database.add(cached_user)  # Save changes
        user_class.clear_from_cache(user_id, database)
    request.session.new_csrf_token()
    return HTTPFound(
        location=request.params.get('target_url', '/').strip(),
        headers=forget(request))


def see_user(request):
    settings = request.registry.settings
    database = request.database
    user_id = request.matchdict['id']

    user_class = settings['users.class']
    cached_user = user_class.get_from_cache(user_id, database)
    if not cached_user:
        raise HTTPNotFound({'id': 'bad'})
    return dict(user_id=user_id)


def finish_authentication(request):
    return _set_headers(request, request.context.profile['verifiedEmail'])


def cancel_authentication(request):
    return HTTPFound(location=request.session.pop('target_url', '/'))


def _make_user_token(settings):
    token_length = settings['users.tokens.length']
    return choice(letters) + make_random_string(token_length - 1)


def _set_headers(request, email):
    settings = request.registry.settings
    database = request.database

    user_class = settings['users.class']
    user = database.query(user_class).filter_by(email=email).first()
    if not user:
        user = get_unique_instance(user_class, database)
        user.email = email
        user.token = _make_user_token(settings)
        database.add(user)
        database.flush()
    return HTTPFound(
        location=request.session.pop('target_url', '/'),
        headers=remember(request, user.id, tokens=[user.token]))
