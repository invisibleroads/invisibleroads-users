from invisibleroads_records.models import (
    CachedRecordMixin, CreationMixin, ModificationMixin)
from sqlalchemy import Column
from sqlalchemy.types import Unicode

from .events import UserAdded
from .settings import S


class UserMixin(ModificationMixin, CreationMixin, CachedRecordMixin):

    __tablename__ = 'user'
    email = Column(Unicode, unique=True)
    name = Column(Unicode)
    image_url = Column(Unicode)

    @property
    def principals(self):
        return []


def make_user(request):
    database = request.database
    User = globals()['User']
    user = User.make_unique_record(database, S['user.id.length'])
    database.add(user)
    database.flush()
    request.registry.notify(UserAdded(user, request))
    return user
