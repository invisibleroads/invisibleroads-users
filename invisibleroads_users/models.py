from invisibleroads_records.models import CachedRecordMixin
from sqlalchemy import Column, Unicode


class UserMixin(CachedRecordMixin):

    __tablename__ = 'user'
    email = Column(Unicode, unique=True)

    @property
    def name(self):
        return self.email.split('@')[0].replace('.', ' ')

    @property
    def principals(self):
        return []
