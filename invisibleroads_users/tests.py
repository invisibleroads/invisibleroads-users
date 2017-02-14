from pytest import fixture
from redis import StrictRedis
from webtest import TestApp

from invisibleroads_records import main as get_app
from invisibleroads_users import models


@fixture
def users_request(records_request, config, database):
    config.include('invisibleroads_users')
    user_id = records_request.authenticated_userid
    users_request = records_request
    users_request.authenticated_user = models.User.get(database, user_id)
    yield users_request
    StrictRedis().flushall()


@fixture
def website(settings):
    yield TestApp(get_app({}, **settings))
    StrictRedis().flushall()
