from pytest import fixture
from redis import StrictRedis
from webtest import TestApp

from invisibleroads_users import main as get_app, models as m


@fixture
def users_website(users_request):
    settings = users_request.registry.settings
    yield TestApp(get_app({}, **settings))


@fixture
def users_request(records_request, website_config):
    database = records_request.database
    user_id = records_request.authenticated_userid
    users_request = records_request
    users_request.authenticated_user = m.User.get(database, user_id)
    yield users_request
    StrictRedis().flushall()


@fixture
def website_config(config):
    config.include('invisibleroads_users')
    yield config
