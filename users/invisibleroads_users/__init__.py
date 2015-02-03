from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.settings import asbool


def includeme(config):
    set_security_policy(config)


def set_security_policy(config, prefix='authtkt.'):
    settings = config.registry.settings
    authentication_policy = AuthTktAuthenticationPolicy(
        secret=settings.get(
            prefix + 'secret', make_random_string(RANDOM_LENGTH)),
        callback=get_groups,
        cookie_name=settings.get(prefix + 'key', AUTHTKT_KEY),
        secure=asbool(settings.get(prefix + 'secure', False)),
        http_only=True,
        hashalg='sha512')
    authorization_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)
    config.set_root_factory(RootFactory)
