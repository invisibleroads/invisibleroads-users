from pyramid.httpexceptions import HTTPNotFound
from pytest import raises

from invisibleroads_users.views import see_user


def test_see_user(users_request):
    users_request.matchdict['user_id'] = 'x'
    with raises(HTTPNotFound):
        see_user(users_request)
