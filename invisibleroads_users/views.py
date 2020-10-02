import functools
from inspect import getcallargs
from invisibleroads_macros_security import make_random_string
from invisibleroads_posts.views import expect_integer, expect_value
from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPInternalServerError,
    HTTPSeeOther,
    HTTPUnauthorized)
from pyramid.security import forget, remember, NO_PERMISSION_REQUIRED
from pyramid.view import view_config

from .constants import L, S, USER_DEFINITION
from .providers import get_auth_provider, get_enter_url_by_name
from .routines import get_or_add_user


@view_config(
    route_name='authorizations.json',
    renderer='json',
    request_method='GET',
    permission=NO_PERMISSION_REQUIRED)
def see_authorizations_json(request):
    session = request.session
    d = {
        'urls': {
            'enter': get_enter_url_by_name(request),
            'leave': request.route_url('authorizations_leave'),
        },
    }
    if 'user' in session:
        user_definition = session['user']
        d['user'] = {_: user_definition.get(_) for _ in S['public_attributes']}
    return d


@view_config(
    route_name='authorizations_enter',
    permission=NO_PERMISSION_REQUIRED)
def see_provider(request):
    target_url = get_target_url(request)

    if S['mock']:
        params = request.params
        user_email = params.get('email', USER_DEFINITION['email'])
        user_definition = dict(USER_DEFINITION, **{
            'name': user_email.split('@')[0].title(),
            'email': user_email,
            'imageUrl': S['image_url'],
        })
        return welcome_user(request, user_definition, target_url)

    form_url = get_form_url(request, target_url)
    return HTTPSeeOther(form_url)


@view_config(
    route_name='authorizations_enter_callback',
    permission=NO_PERMISSION_REQUIRED)
def remember_user(request):
    params = request.params
    session = request.session
    auth_state = session.pop('auth_state', '')
    target_url = session.pop('target_url', '/')

    if not params.get('code') or params.get('state') != auth_state:
        raise HTTPSeeOther(target_url)

    auth_provider = get_auth_provider(request, auth_state)
    user_definition = auth_provider.get_user_definition()
    return welcome_user(request, user_definition, target_url)


@view_config(
    route_name='authorizations_leave',
    permission=NO_PERMISSION_REQUIRED)
def forget_user(request):
    target_url = get_target_url(request)
    session = request.session
    session.invalidate()
    headers = forget(request)
    return HTTPSeeOther(target_url, headers=headers)


def get_form_url(request, target_url):
    auth_state = make_random_string(S['auth_state_length'])
    auth_provider = get_auth_provider(request, auth_state)
    session = request.session
    session['auth_state'] = auth_state
    session['target_url'] = target_url
    return auth_provider.form_url


def get_target_url(request):
    params = request.params
    return params.get('targetUrl', S['target_url']).strip()


def welcome_user(request, user_definition, target_url):
    user_email = user_definition['email']

    if S['storage'] == 'database':
        user = get_or_add_user(request, user_definition)
        user_id = user.id
        tm = request.tm
        tm.commit()
        tm.begin()
    else:
        user_id = user_definition.get('id', user_email)
    user_definition['id'] = user_id

    S['check_authorization'](user_definition)

    # Pass user_definition to UserAuthService
    request.user_definition = user_definition
    headers = remember(request, user_id)

    # Store user_definition in session
    session = request.session
    session['user'] = user_definition
    return HTTPSeeOther(target_url, headers=headers)


def handle_redis_connection_error(request):
    L.error('redis: is not accessible')
    raise HTTPInternalServerError({})


def handle_csrf_origin_error(request):
    raise HTTPBadRequest({'csrf': 'has bad origin'})


def handle_csrf_token_error(request):
    raise HTTPBadRequest({'csrf': 'has bad token'})


def authorize_param(f):
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


authorize_value = authorize_param(expect_value)
authorize_integer = authorize_param(expect_integer)
