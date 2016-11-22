from os.path import basename, dirname
from pytest import fixture, raises

from invisibleroads_posts.models import DummyBase
from invisibleroads_users.models import UserFolderMixin


class Y(UserFolderMixin, DummyBase):
    pass


class TestUserFolderMixin(object):

    random_length = 10
    instance_id = 100
    user_id = 1000

    def test_spawn(self, data_folder):
        y = Y.spawn(data_folder, owner_id=self.user_id)
        assert basename(y.folder) == '1'
        assert basename(dirname(y.folder)) == str(self.user_id)

    def test_spawn_enumerated_folder(self, data_folder):
        with raises(IOError):
            Y.spawn_folder(data_folder, owner_id='../1')
        folder = Y.spawn_folder(data_folder, owner_id=self.user_id)
        assert basename(folder) == '1'
        assert basename(dirname(folder)) == str(self.user_id)
        folder = Y.spawn_folder(data_folder)
        assert basename(folder) == '1'
        assert basename(dirname(folder)) == '0'

    def test_spawn_random_folder(self, data_folder):
        with raises(IOError):
            Y.spawn_folder(data_folder, self.random_length, owner_id='../1')
        folder = Y.spawn_folder(data_folder, self.random_length, self.user_id)
        assert len(basename(folder)) == self.random_length
        assert basename(dirname(folder)) == str(self.user_id)
        folder = Y.spawn_folder(data_folder, self.random_length)
        assert len(basename(folder)) == self.random_length
        assert basename(dirname(folder)) == '0'

    def test_get_user_folder(self, data_folder):
        with raises(IOError):
            Y.get_user_folder(data_folder, owner_id='../1')
        user_folder = Y.get_user_folder(data_folder, self.user_id)
        assert basename(user_folder) == str(self.user_id)

    def test_get_folder(self, data_folder):
        with raises(IOError):
            Y(id=self.instance_id, owner_id='../1').get_folder(data_folder)
        folder = Y(id=self.instance_id, owner_id=self.user_id).get_folder(
            data_folder)
        assert basename(folder) == str(self.instance_id)


@fixture
def data_folder(tmpdir):
    return str(tmpdir)
