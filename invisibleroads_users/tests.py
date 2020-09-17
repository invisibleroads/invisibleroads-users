from pytest import fixture

from . import models as M


@fixture
def users_request(records_request, users_config):
    User = M.User
    users_request = records_request
    users_request.__class__.authenticated_user = property(
        lambda self: User.get(self.database, self.authenticated_userid))
    yield users_request
    users_request.session.redis.flushall()


@fixture
def users_config(config):
    config.include('invisibleroads_users')
    yield config


@fixture
def user(users_request):
    database = users_request.database
    User = M.User
    user = User.make_unique_record(database)
    user.name = 'User'
    user.email = 'user@example.com'
    return user
