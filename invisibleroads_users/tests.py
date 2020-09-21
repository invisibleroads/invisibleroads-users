from pyramid import testing
from pytest import fixture

from . import models as M


@fixture
def users_request(users_config, database, data_folder):
    request = testing.DummyRequest(
        db=database,
        data_folder=data_folder)
    request.json_body = {}
    yield request


@fixture
def users_config(users_settings):
    config = testing.setUp(settings=users_settings)
    config.include('invisibleroads_posts')
    config.include('invisibleroads_records')
    config.include('invisibleroads_users')
    yield config
    testing.tearDown()


@fixture
def users_settings(records_settings):
    users_settings = records_settings
    yield users_settings


@fixture
def user(users_request):
    database = users_request.database
    User = M.User
    user = User.make_unique_record(database)
    user.name = 'User'
    user.email = 'user@example.com'
    return user
