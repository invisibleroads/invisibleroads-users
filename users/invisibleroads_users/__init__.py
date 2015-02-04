import logging
from invisibleroads_macros.security import make_random_string
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.events import BeforeRender
from pyramid.security import Allow, Authenticated
from pyramid.session import check_csrf_token
from pyramid.settings import asbool
from pyramid_redis_sessions import RedisSessionFactory

from .models import User
from .views import add_routes, get_ticket


AUTHTKT_KEY = 'a'
SESSION_KEY = 's'
RANDOM_LEN = 128
LOG = logging.getLogger(__name__)


class RootFactory(object):
    'Permission definitions'
    __acl__ = [
        (Allow, Authenticated, 'guest'),
        (Allow, 'member', 'member'),
        (Allow, 'leader', 'leader'),
    ]

    def __init__(self, request):
        pass


def includeme(config):
    configure_security_policy(config)
    configure_session_factory(config)
    configure_third_party_authentication(config)
    add_routes(config)
    config.add_subscriber(add_renderer_globals, BeforeRender)


def configure_security_policy(config, prefix='authtkt.'):
    settings = config.registry.settings
    authentication_policy = AuthTktAuthenticationPolicy(
        secret=settings.get(prefix + 'secret', make_random_string(RANDOM_LEN)),
        callback=get_groups,
        cookie_name=settings.get(prefix + 'key', AUTHTKT_KEY),
        secure=asbool(settings.get(prefix + 'secure', False)),
        http_only=True,
        hashalg='sha512')
    authorization_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)
    config.set_root_factory(RootFactory)


def configure_session_factory(config, prefix='session.'):
    settings = config.registry.settings
    session_factory = RedisSessionFactory(
        secret=settings.get(prefix + 'secret', make_random_string(RANDOM_LEN)),
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


def get_groups(user_id, request):
    'Define server-side permissions for user'
    ticket = get_ticket(request)
    if not ticket:
        return  # Cookie is bad
    if 'POST' == request.method and not check_csrf_token(
            request, raises=False):
        return  # CSRF token does not match
    user = User.get(user_id)
    if not user or user.ticket != ticket:
        return  # User does not exist or ticket changed
    groups = []
    if user.is_member:
        groups.append('member')
    if user.is_leader:
        groups.append('leader')
    return groups


def add_renderer_globals(event):
    'Define client-side permissions for user'
    user_id = event['request'].authenticated_userid
    event.update(dict(
        user=User.get(user_id)))
