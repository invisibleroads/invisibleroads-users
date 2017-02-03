import logging
from invisibleroads_macros.configuration import resolve_attribute
from invisibleroads_macros.iterable import set_default
from invisibleroads_macros.security import make_random_string
from invisibleroads_posts import (
    InvisibleRoadsConfigurator, add_routes_for_fused_assets,
    add_website_dependency)
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.exceptions import BadCSRFOrigin, BadCSRFToken
from pyramid.events import BeforeRender
from pyramid.settings import asbool
from pyramid_redis_sessions import session_factory_from_settings
from redis import ConnectionError

from .models import User
from .views import add_routes


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())
REDIS_CONNECTION_ERROR_MESSAGE = """\
could not access redis

Is the redis server running?

sudo systemctl start redis"""


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
    configure_third_party_authentication(config)
    configure_assets(config)
    config.add_subscriber(_define_add_renderer_globals(config), BeforeRender)
    add_routes(config)


def configure_settings(config):
    settings = config.registry.settings
    set_default(settings, 'users.class', User, resolve_attribute)
    set_default(settings, 'user.id.length', 16, int)
    add_website_dependency(config)


def configure_assets(config):
    config.add_cached_static_view(
        '_/invisibleroads-users', 'invisibleroads_users:assets')


def configure_security_policy(config, prefix='users.authtkts.'):
    settings = config.registry.settings
    authorization_policy = ACLAuthorizationPolicy()
    authentication_policy = AuthTktAuthenticationPolicy(
        cookie_name=settings.get(prefix + 'cookie_name', 'a'),
        secure=asbool(settings.get(prefix + 'cookie_secure', False)),
        http_only=asbool(settings.get(prefix + 'cookie_httponly', True)),
        secret=settings.get(prefix + 'secret', make_random_string(128)),
        callback=_define_get_principals(config),
        hashalg='sha512')
    config.set_authorization_policy(authorization_policy)
    config.set_authentication_policy(authentication_policy)


def configure_http_session_factory(config, prefix='redis.sessions.'):
    settings = config.registry.settings
    set_default(settings, prefix + 'cookie_name', 's')
    set_default(settings, prefix + 'cookie_secure', False)
    set_default(settings, prefix + 'cookie_httponly', True)
    set_default(settings, prefix + 'secret', make_random_string(128))
    set_default(settings, prefix + 'timeout', 43200)
    set_default(settings, prefix + 'prefix', 'user_session.')
    config.set_session_factory(session_factory_from_settings(settings))
    config.set_default_csrf_options(require_csrf=True)
    config.add_view(handle_redis_connection_error, context=ConnectionError)
    config.add_view(handle_csrf_origin_error, context=BadCSRFOrigin)
    config.add_view(handle_csrf_token_error, context=BadCSRFToken)


def configure_third_party_authentication(config):
    config.include('velruse.providers.google_oauth2')
    try:
        config.add_google_oauth2_login_from_settings()
    except KeyError:
        LOG.warn('missing velruse.google.consumer_key')
        LOG.warn('missing velruse.google.consumer_secret')


def handle_redis_connection_error(context, request):
    response = request.response
    response.status_int = 500
    LOG.error(REDIS_CONNECTION_ERROR_MESSAGE)
    return response


def handle_csrf_origin_error(context, request):
    response = request.response
    response.status_int = 400
    response.content_type = 'text/plain'
    response.body = 'bad csrf origin'
    return response


def handle_csrf_token_error(context, request):
    response = request.response
    response.status_int = 400
    response.content_type = 'text/plain'
    response.body = 'bad csrf token'
    return response


def _define_get_principals(config):
    settings = config.registry.settings
    user_class = settings['users.class']

    def get_principals(user_id, request):
        'Define server-side permissions for user'
        database = request.database
        cached_user = user_class.get(database, user_id)
        if not cached_user:
            return  # User does not exist
        return cached_user.principals

    return get_principals


def _define_add_renderer_globals(config):
    settings = config.registry.settings
    user_class = settings['users.class']

    def add_renderer_globals(event):
        'Define client-side permissions for user'
        request = event['request']
        database = request.database
        user_id = request.authenticated_userid
        cached_user = user_class.get(database, user_id)
        event.update(dict(user=cached_user))

    return add_renderer_globals
