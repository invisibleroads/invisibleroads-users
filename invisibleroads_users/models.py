from invisibleroads_macros.disk import (
    make_enumerated_folder, make_unique_folder, resolve_relative_path)
from invisibleroads_posts.models import FolderMixin
from invisibleroads_records.models import Base, CachedInstanceMixin
from sqlalchemy import Column, String, Unicode


class User(CachedInstanceMixin, Base):

    __tablename__ = 'user'
    email = Column(Unicode, unique=True)
    token = Column(String)

    @property
    def name(self):
        return self.email.split('@')[0].replace('.', ' ')

    @property
    def groups(self):
        return []


class UserFolderMixin(FolderMixin):

    @classmethod
    def spawn_folder(Class, data_folder, random_length=None, owner_id=None):
        user_folder = Class.get_user_folder(data_folder, owner_id)
        return make_unique_folder(
            user_folder, length=random_length,
        ) if random_length else make_enumerated_folder(user_folder)

    @classmethod
    def get_user_folder(Class, data_folder, owner_id):
        parent_folder = Class.get_parent_folder(data_folder)
        return resolve_relative_path(str(owner_id or 0), parent_folder)

    def get_folder(self, data_folder):
        user_folder = self.get_user_folder(data_folder, self.owner_id)
        return resolve_relative_path(str(self.id), user_folder)
