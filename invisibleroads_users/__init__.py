from invisibleroads_macros.configuration import (
    parse_list, resolve_attribute, set_default)
from invisibleroads_macros.log import get_log
from invisibleroads_macros.security import make_random_string
from invisibleroads_posts import (
    InvisibleRoadsConfigurator, add_routes_for_fused_assets,
    add_website_dependency)
from invisibleroads_posts.libraries.configuration import fill_secrets
from invisibleroads_records.models import Base
from os import environ
from pyramid.exceptions import BadCSRFOrigin, BadCSRFToken
from pyramid.events import BeforeRender
from pyramid.security import Allow, Everyone
from pyramid.settings import asbool
from pyramid_redis_sessions import session_factory_from_settings
from redis import ConnectionError, StrictRedis

from . import models as M
from .settings import S
from .views import add_routes


L = get_log(__name__)
PREFIX = 'invisibleroads_users.'
REDIS_CONNECTION_ERROR_MESSAGE = """\
could not access redis

Is the redis server running?

sudo systemctl start redis"""


class RootFactory(object):

    __acl__ = [
        (Allow, Everyone, 'see user'),
    ]

    def __init__(self, request):
        pass


def main(global_config, **settings):
    config = InvisibleRoadsConfigurator(settings=settings)
    includeme(config)
    add_routes_for_fused_assets(config)
    return config.make_wsgi_app()


def includeme(config):
    config.include('invisibleroads_posts')
    config.include('invisibleroads_records')
    configure_settings(config)
    configure_security_policy(config)
    configure_http_session_factory(config)
    configure_views(config)
    configure_assets(config)
    configure_provider_definitions(config)


def configure_settings(config, prefix=PREFIX):
    settings = config.registry.settings
    UserMixin = S.set(
        settings, prefix, 'user_mixin', M.UserMixin, resolve_attribute)
    if not hasattr(M, 'User'):
        M.User = type('User', (UserMixin, Base), {})
    S.set(settings, '', 'user.id.length', 32, int)
    S.set(settings, prefix, 'mock', True, asbool)
    set_default(settings, prefix + 'auth_button.enter_text', 'Enter')
    set_default(settings, prefix + 'auth_button.leave_text', 'Leave')
    set_default(settings, prefix + 'auth_modal.title', 'Choose a Provider')
    set_default(settings, prefix + 'auth_modal.button_text', 'Cancel')
    S.set(settings, prefix, 'cookie_name', 'u')
    S.set(settings, prefix, 'cookie_secure', False, asbool)
    S.set(settings, prefix, 'cookie_httponly', True, asbool)
    S.set(
        settings, prefix, 'image_url',
        '/_/invisibleroads-users/smiley-20170620-2300.png')
    add_website_dependency(config)


def configure_security_policy(config):
    settings = config.registry.settings
    fill_secrets(settings, 'multiauth.policy.')
    config.include('pyramid_multiauth')
    config.add_request_method(lambda request: M.User.get(
        request.database, request.authenticated_userid
    ), 'authenticated_user', reify=True)


def configure_http_session_factory(config, prefix='redis.sessions.'):
    settings = config.registry.settings
    fill_secrets(settings, prefix)
    set_default(settings, prefix + 'cookie_name', 's')
    set_default(settings, prefix + 'cookie_secure', S['cookie_secure'])
    set_default(settings, prefix + 'cookie_httponly', S['cookie_httponly'])
    set_default(settings, prefix + 'secret', make_random_string(128))
    set_default(settings, prefix + 'timeout', 43200)
    set_default(settings, prefix + 'prefix', 'user_session.')
    config.set_session_factory(session_factory_from_settings(settings))
    config.set_default_csrf_options(require_csrf=True)
    config.add_view(handle_redis_connection_error, context=ConnectionError)
    config.add_view(handle_csrf_origin_error, context=BadCSRFOrigin)
    config.add_view(handle_csrf_token_error, context=BadCSRFToken)
    try:
        StrictRedis().info()
    except ConnectionError:
        L.error(REDIS_CONNECTION_ERROR_MESSAGE)


def configure_views(config):
    config.set_root_factory(RootFactory)
    config.add_subscriber(add_renderer_globals, BeforeRender)
    add_routes(config)


def configure_assets(config):
    config.add_cached_static_view(
        '-/invisibleroads-users', 'invisibleroads_users:assets')


def configure_provider_definitions(config, prefix=PREFIX):
    S['provider_definitions'] = d = {}
    settings = config.registry.settings
    for provider_name in set_default(
            settings, prefix + 'auth_providers', [], parse_list):
        provider_prefix = prefix + 'auth_provider.' + provider_name + '.'
        d[provider_name] = {
            'consumer_key': settings[provider_prefix + 'consumer_key'],
            'consumer_secret': settings[provider_prefix + 'consumer_secret'],
        }
    if not S['cookie_secure']:
        environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def handle_redis_connection_error(context, request):
    response = request.response
    response.status_int = 500
    L.error(REDIS_CONNECTION_ERROR_MESSAGE)
    return response


def handle_csrf_origin_error(context, request):
    response = request.response
    response.status_int = 400
    response.content_type = 'text/plain'
    response.text = 'bad csrf origin'
    return response


def handle_csrf_token_error(context, request):
    response = request.response
    response.status_int = 400
    response.content_type = 'text/plain'
    response.text = 'bad csrf token'
    return response


def get_principals(user_id, request):
    'Define server-side permissions for user'
    database = request.database
    user = M.User.get(database, user_id)
    if not user:
        return  # User does not exist
    return user.principals


def add_renderer_globals(event):
    'Define client-side permissions for user'
    request = event['request']
    event.update(dict(authenticated_user=request.authenticated_user))
