import functools
from invisibleroads_macros.log import get_log
from invisibleroads_macros.security import make_random_string
from invisibleroads_posts.views import expect_integer, expect_param
from inspect import getcallargs
from pyramid.httpexceptions import (
    HTTPSeeOther, HTTPTemporaryRedirect, HTTPUnauthorized)
from pyramid.security import remember, forget

from . import models as M
from .providers import get_provider
from .settings import S


D = get_log('data')


def add_routes(config):
    config.add_route('users_enter', '/users/enter/{provider_name}')
    config.add_route(
        'users_enter_callback', '/users/enter/{provider_name}/callback')
    config.add_route('users_leave', '/users/leave')
    config.add_route('user', '/u/{user_id}')

    config.add_view(
        see_provider,
        route_name='users_enter')
    config.add_view(
        remember_user,
        route_name='users_enter_callback')
    config.add_view(
        forget_user,
        route_name='users_leave')
    config.add_view(
        see_user,
        permission='user-see',
        renderer='invisibleroads_users:templates/user.jinja2',
        route_name='user')


def see_provider(request):
    params = request.params
    target_url = params.get('target_url', '/').strip()

    if S['mock']:
        email = params.get('target_email', u'user@example.com')
        provider_name = 'mock'
        return welcome_user(request, {
            'name': email.split('@')[0].title(),
            'email': email,
            'image_url': S['image_url'],
        }, provider_name, target_url)

    provider = get_provider(request, make_random_string(64))
    session = request.session
    session['auth_state'] = provider.auth_state
    session['target_url'] = target_url
    return HTTPSeeOther(provider.auth_url)


def remember_user(request):
    params = request.params
    session = request.session
    auth_state = session.pop('auth_state', '')
    target_url = session.pop('target_url', '/')

    if not params.get('code') or params.get('state') != auth_state:
        raise HTTPSeeOther(target_url)

    provider = get_provider(request, auth_state)
    user_definition = provider.user_definition
    return welcome_user(request, user_definition, provider.name, target_url)


def forget_user(request):
    params = request.params
    target_url = params.get('target_url', '/').strip()
    request.session.invalidate()
    return HTTPTemporaryRedirect(location=target_url, headers=forget(request))


def see_user(request):
    return dict(user=M.User.get_from(request))


def welcome_user(request, user_definition, provider_name, target_url):
    database = request.database
    user_email = user_definition['email']
    user = database.query(M.User).filter_by(email=user_email).first()
    if not user:
        user = M.make_user(request)
    user_id = user.id
    user.email = user_email
    user.name = user_definition['name']
    user.image_url = user_definition['image_url']
    user.update_cache(database)
    D.info(
        'user_id=%s,provider_name=%s,target_url=%s',
        user_id, provider_name, target_url)
    return HTTPSeeOther(target_url, headers=remember(request, user_id))


def authorize_value(f):
    @functools.wraps(f)
    def wrapper(*args, **kw):
        value = f(*args, **kw)
        args = getcallargs(f, *args, **kw)
        request = args['request']
        default = args['default']
        if not request.authenticated_userid and value != default:
            raise HTTPUnauthorized
        return value
    return wrapper


authorize_param = authorize_value(expect_param)
authorize_integer = authorize_value(expect_integer)
