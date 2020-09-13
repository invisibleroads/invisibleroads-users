from pytest import fixture
from redis import StrictRedis
from webtest import TestApp

from invisibleroads_users import main as get_app, models as M


@fixture
def users_website(users_request):
    settings = users_request.registry.settings
    yield TestApp(get_app({}, **settings))


@fixture
def users_request(records_request, website_config):
    users_request = records_request
    users_request.__class__.authenticated_user = property(
        lambda self: M.User.get(self.database, self.authenticated_userid))
    yield users_request
    StrictRedis().flushall()


@fixture
def website_config(config):
    config.include('invisibleroads_users')
    yield config


@fixture
def user(website_request):
    user = M.make_user(website_request)
    user.name = 'User'
    user.email = 'user@example.com'
    return user
