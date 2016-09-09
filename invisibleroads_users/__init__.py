import logging
from invisibleroads_macros.configuration import resolve_attribute
from invisibleroads_macros.iterable import set_default
from invisibleroads_macros.security import make_random_string
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.events import BeforeRender
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.session import check_csrf_token
from pyramid.settings import asbool
from pyramid_redis_sessions import session_factory_from_settings

from .models import User
from .views import add_routes


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


def includeme(config):
    config.include('invisibleroads_posts')
    config.include('invisibleroads_records')
    configure_settings(config)
    configure_security_policy(config)
    configure_session_factory(config)
    configure_third_party_authentication(config)
    configure_assets(config)
    config.add_subscriber(_define_add_renderer_globals(config), BeforeRender)
    add_routes(config)


def configure_settings(config):
    settings = config.registry.settings
    set_default(settings, 'users.class', User, resolve_attribute)
    set_default(settings, 'users.tokens.length', 16, int)
    settings['website.dependencies'].append(config.package_name)


def configure_assets(config):
    config.add_cached_static_view(
        '_/invisibleroads-users', 'invisibleroads_users:assets')


def configure_security_policy(config, prefix='users.authtkts.'):
    settings = config.registry.settings
    authentication_policy = AuthTktAuthenticationPolicy(
        cookie_name=settings.get(prefix + 'cookie_name', 'a'),
        secure=asbool(settings.get(prefix + 'cookie_secure', False)),
        http_only=asbool(settings.get(prefix + 'cookie_httponly', True)),
        secret=settings.get(prefix + 'secret', make_random_string(128)),
        callback=_define_get_groups(config),
        hashalg='sha512')
    authorization_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)


def configure_session_factory(config, prefix='redis.sessions.'):
    settings = config.registry.settings
    set_default(settings, prefix + 'cookie_name', 's')
    set_default(settings, prefix + 'cookie_secure', False)
    set_default(settings, prefix + 'cookie_httponly', True)
    set_default(settings, prefix + 'secret', make_random_string(128))
    set_default(settings, prefix + 'timeout', 36000)
    set_default(settings, prefix + 'prefix', 'user_session.')
    config.set_session_factory(session_factory_from_settings(settings))


def configure_third_party_authentication(config):
    config.include('velruse.providers.google_oauth2')
    try:
        config.add_google_oauth2_login_from_settings()
    except KeyError as e:
        LOG.warn(e)


def _define_get_groups(config):
    settings = config.registry.settings
    user_class = settings['users.class']

    def get_groups(user_id, request):
        'Define server-side permissions for user'
        user_token = _get_user_token(request)
        if not user_token:
            return  # Cookie is bad
        if request.method in (
            'POST', 'PUT', 'DELETE',
        ) and not check_csrf_token(request, raises=False):
            return  # CSRF token does not match
        cached_user = user_class.get_from_cache(user_id)
        if not cached_user or cached_user.token != user_token:
            return  # User does not exist or user token changed
        return cached_user.groups

    return get_groups


def _define_add_renderer_globals(config):
    settings = config.registry.settings
    user_class = settings['users.class']

    def add_renderer_globals(event):
        'Define client-side permissions for user'
        user_id = event['request'].authenticated_userid
        cached_user = user_class.get_from_cache(user_id)
        event.update(dict(user=cached_user))

    return add_renderer_globals


def _get_user_token(request):
    authentication_policy = request.registry.queryUtility(
        IAuthenticationPolicy)
    user_information = authentication_policy.cookie.identify(request)
    try:
        user_token = user_information['tokens'][0]
    except (TypeError, IndexError):
        user_token = ''
    return user_token
