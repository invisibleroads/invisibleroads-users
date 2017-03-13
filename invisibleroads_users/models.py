from invisibleroads_records.models import CachedRecordMixin, CreationMixin
from sqlalchemy import Column, Unicode


class UserMixin(CreationMixin, CachedRecordMixin):

    __tablename__ = 'user'
    email = Column(Unicode, unique=True)

    @property
    def name(self):
        return self.email.split('@')[0].replace('.', ' ')

    @property
    def principals(self):
        return []
