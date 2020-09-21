from invisibleroads_macros_configuration import (
    load_attribute,
    load_attributes,
    set_default)
from invisibleroads_macros_security import make_random_string
from invisibleroads_records.models import Base
from os import environ
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.exceptions import BadCSRFOrigin, BadCSRFToken
from pyramid.security import Allow, Authenticated
from pyramid.settings import asbool, aslist
from pyramid_authsanity.interfaces import IAuthService
from pyramid_redis_sessions import session_factory_from_settings
from redis import ConnectionError as RedisConnectionError

from . import models as M
from .constants import (
    DEFAULT_SECRET,
    DEFAULT_SECRET_ERROR_MESSAGE,
    INVISIBLEROADS_USERS_SETTINGS_PREFIX,
    L,
    REDIS_SESSIONS_COOKIE_NAME,
    REDIS_SESSIONS_PREFIX,
    REDIS_SESSIONS_SECRET_LENGTH,
    REDIS_SESSIONS_SETTINGS_PREFIX,
    REDIS_SESSIONS_TIMEOUT_IN_SECONDS,
    S)
from .routines import get_crypt
from .services import make_user_auth_service
from .views import (
    handle_csrf_origin_error,
    handle_csrf_token_error,
    handle_redis_connection_error)


def includeme(config):
    configure_settings(config)
    configure_request_session_factory(config)
    configure_security_policy(config)
    configure_provider_definitions(config)
    configure_views(config)


def configure_settings(config, prefix=INVISIBLEROADS_USERS_SETTINGS_PREFIX):
    settings = config.get_settings()
    UserMixin = S.set(
        settings, prefix, 'user_mixin', M.UserMixin, load_attribute)
    if not hasattr(M, 'User'):
        M.User = type('User', (UserMixin, Base), {})
    S.set(settings, prefix, 'mock', S['mock'], asbool)
    S.set(settings, prefix, 'storage', S['storage'])
    S.set(settings, prefix, 'cookie_secure', S['cookie_secure'], asbool)
    S.set(settings, prefix, 'cookie_httponly', S['cookie_httponly'], asbool)
    S.set(settings, prefix, 'verify_tls', S['verify_tls'], asbool)
    S.set(settings, prefix, 'auth_state_length', S['auth_state_length'], int)
    S.set(settings, prefix, 'public_attributes', S[
        'public_attributes'], aslist)
    S.set(settings, prefix, 'secret', S['secret'])
    if S['secret'] == DEFAULT_SECRET:
        L.warning(DEFAULT_SECRET_ERROR_MESSAGE)
    S.set(settings, prefix, 'default_permission', S[
        'default_permission'], asbool)
    S.set(settings, prefix, 'require_csrf', S['require_csrf'], asbool)


def configure_request_session_factory(
        config, prefix=REDIS_SESSIONS_SETTINGS_PREFIX):
    settings = config.get_settings()
    set_default(settings, prefix + 'secret', make_random_string(
        REDIS_SESSIONS_SECRET_LENGTH))
    set_default(
        settings, prefix + 'timeout', REDIS_SESSIONS_TIMEOUT_IN_SECONDS)
    set_default(settings, prefix + 'cookie_name', REDIS_SESSIONS_COOKIE_NAME)
    set_default(settings, prefix + 'cookie_secure', S['cookie_secure'])
    set_default(settings, prefix + 'cookie_httponly', S['cookie_httponly'])
    set_default(settings, prefix + 'prefix', REDIS_SESSIONS_PREFIX)
    config.set_session_factory(session_factory_from_settings(settings))
    config.add_view(
        handle_redis_connection_error, context=RedisConnectionError)


def configure_security_policy(config):
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.include('pyramid_authsanity')
    config.register_service_factory(make_user_auth_service, iface=IAuthService)
    config.set_default_permission(S['default_permission'])
    config.set_default_csrf_options(require_csrf=S['require_csrf'])
    config.add_view(handle_csrf_origin_error, context=BadCSRFOrigin)
    config.add_view(handle_csrf_token_error, context=BadCSRFToken)
    S['crypt'] = get_crypt()


def configure_provider_definitions(
        config, prefix=INVISIBLEROADS_USERS_SETTINGS_PREFIX):
    settings = config.get_settings()
    S['provider_definitions'] = d = {}
    for provider_name in set_default(
            settings, prefix + 'auth_providers', [], aslist):
        provider_prefix = prefix + 'auth_providers.' + provider_name + '.'
        d[provider_name] = {
            'auth_scopes': aslist(settings[provider_prefix + 'auth_scopes']),
            'consumer_key': settings[provider_prefix + 'consumer_key'],
            'consumer_secret': settings[provider_prefix + 'consumer_secret'],
            'form_url': settings[provider_prefix + 'form_url'],
            'token_url': settings[provider_prefix + 'token_url'],
            'resource_url': settings[provider_prefix + 'resource_url'],
            'compliance_fixes': load_attributes(settings[
                provider_prefix + 'compliance_fixes']),
        }
    if not S['cookie_secure']:
        environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def configure_views(config):

    class DefaultRootFactory(object):

        __acl__ = [
            (Allow, Authenticated, S['default_permission']),
        ]

        def __init__(self, request):
            pass

    config.set_root_factory(DefaultRootFactory)
    config.include('.routes')
    config.scan('.views')
