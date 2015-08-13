import logging
from invisibleroads_macros.security import make_random_string
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.events import BeforeRender
from pyramid.session import check_csrf_token
from pyramid.settings import asbool
from pyramid_redis_sessions import RedisSessionFactory

from .models import User
from .views import add_routes, get_ticket


AUTHTKT_KEY = 'a'
SESSION_KEY = 's'
SECRET_LENGTH = 128
LOG = logging.getLogger(__name__)


def includeme(config):
    configure_security_policy(config)
    configure_session_factory(config)
    configure_third_party_authentication(config)
    add_routes(config)
    config.add_subscriber(define_add_renderer_globals(config), BeforeRender)
    config.add_static_view(
        '_/invisibleroads-users', 'invisibleroads_users:assets',
        cache_max_age=3600)


def configure_security_policy(config, prefix='authtkt.'):
    settings = config.registry.settings
    authentication_policy = AuthTktAuthenticationPolicy(
        secret=settings.get(
            prefix + 'secret', make_random_string(SECRET_LENGTH)),
        callback=define_get_groups(config),
        cookie_name=settings.get(prefix + 'key', AUTHTKT_KEY),
        secure=asbool(settings.get(prefix + 'secure', False)),
        http_only=True,
        hashalg='sha512')
    authorization_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)
    config.set_root_factory(settings.get('users.root_factory'))


def configure_session_factory(config, prefix='session.'):
    settings = config.registry.settings
    session_factory = RedisSessionFactory(
        secret=settings.get(
            prefix + 'secret', make_random_string(SECRET_LENGTH)),
        timeout=int(settings.get(prefix + 'timeout', 1800)),
        cookie_name=settings.get(prefix + 'key', SESSION_KEY),
        cookie_secure=asbool(settings.get(prefix + 'secure', False)),
        cookie_httponly=True,
        url=settings.get(prefix + 'storage.url', 'redis://localhost:6379'))
    config.set_session_factory(session_factory)


def configure_third_party_authentication(config):
    config.include('velruse.providers.google_oauth2')
    try:
        config.add_google_oauth2_login_from_settings()
    except KeyError:
        LOG.warn('Missing velruse.google.consumer_key')
        LOG.warn('Missing velruse.google.consumer_secret')


def define_get_groups(config):
    settings = config.registry.settings
    user_class = config.maybe_dotted(settings.get('users.user', User))

    def get_groups(user_id, request):
        'Define server-side permissions for user'
        ticket = get_ticket(request)
        if not ticket:
            return  # Cookie is bad
        if request.method in (
            'POST', 'PUT', 'DELETE',
        ) and not check_csrf_token(request, raises=False):
            return  # CSRF token does not match
        cached_user = user_class.get_from_cache(user_id)
        if not cached_user or cached_user.ticket != ticket:
            return  # User does not exist or ticket changed
        return cached_user.groups

    return get_groups


def define_add_renderer_globals(config):
    settings = config.registry.settings
    user_class = config.maybe_dotted(settings.get('users.user', User))

    def add_renderer_globals(event):
        'Define client-side permissions for user'
        user_id = event['request'].authenticated_userid
        cached_user = user_class.get_from_cache(user_id)
        event.update(dict(user=cached_user))

    return add_renderer_globals
