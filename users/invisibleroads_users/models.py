from invisibleroads_macros.security import make_random_string
from invisibleroads_records.libraries.cache import FromCache
from invisibleroads_records.models import Base, db
from random import choice
from sqlalchemy import Column, Integer, String, Unicode
from string import letters


TICKET_LENGTH = 16
make_ticket = lambda: choice(letters) + make_random_string(TICKET_LENGTH - 1)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(Unicode, unique=True)
    ticket = Column(String, default=make_ticket)

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
        return db.query(Class).options(FromCache(
            cache_key='%s.id=%s' % (Class.__name__, id)))
