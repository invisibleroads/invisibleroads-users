from invisibleroads_records.libraries.cache import FromCache
from invisibleroads_records.models import Base, DATABASE
from sqlalchemy import Column, Integer, String, Unicode


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(Unicode, unique=True)
    token = Column(String)

    @property
    def name(self):
        return self.email.split('@')[0].replace('.', ' ')

    @property
    def groups(self):
        return []

    @classmethod
    def get_from_cache(Class, id):
        return Class._make_query(id).get(id) if id else None

    @classmethod
    def clear_from_cache(Class, id):
        Class._make_query(id).invalidate()

    @classmethod
    def _make_query(Class, id):
        return DATABASE.query(Class).options(FromCache(
            cache_key='%s.id=%s' % (Class.__name__, id)))
