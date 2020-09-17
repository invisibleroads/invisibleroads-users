from .constants import S


def make_user_auth_service(context, request):
    return UserAuthService(request)


# https://pyramid-authsanity.readthedocs.io/en/latest/api/interfaces.html
class UserAuthService(object):

    def __init__(self, request):
        self.request = request
        self.session = session = request.session
        self.redis = session.redis
        self.user_definition = None

    def userid(self):
        if self.user_definition is None:
            raise Exception
        return self.user_definition.get('id')

    def groups(self):
        return self.user_definition.get('roles', [])

    def verify_ticket(self, principal, ticket):
        if not principal:
            return
        redis = self.redis
        redis_key = S['redis.users.prefix'] + principal
        if not redis.sismember(redis_key, ticket):
            return
        self.user_definition = self.session.get('user', {})

    def add_ticket(self, principal, ticket):
        redis = self.redis
        redis_key = S['redis.users.prefix'] + principal
        redis.sadd(redis_key, ticket)
        self.user_definition = self.request.user_definition

    def remove_ticket(self, ticket):
        try:
            principal = self.user_definition['id']
        except TypeError:
            return
        redis = self.redis
        redis_key = S['redis.users.prefix'] + principal
        redis.srem(redis_key, ticket)
