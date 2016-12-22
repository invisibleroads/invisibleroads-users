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
