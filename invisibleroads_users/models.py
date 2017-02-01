from invisibleroads_records.models import Base, CachedRecordMixin
from sqlalchemy import Column, Unicode


class User(CachedRecordMixin, Base):

    __tablename__ = 'user'
    email = Column(Unicode, unique=True)

    @property
    def name(self):
        return self.email.split('@')[0].replace('.', ' ')

    @property
    def principals(self):
        return []
