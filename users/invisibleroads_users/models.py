import random
from invisibleroads_macros.security import make_random_string
from invisibleroads_records.libraries.cache import FromCache
from invisibleroads_records.models import Base, db
from sqlalchemy import Column, Integer, String, Unicode
from sqlalchemy.ext.hybrid import hybrid_property
from string import letters


ROLE_GUEST, ROLE_MEMBER, ROLE_LEADER = xrange(3)
TICKET_LENGTH = 16


make_ticket = lambda: random.choice(
    letters) + make_random_string(TICKET_LENGTH - 1)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(Unicode)
    ticket = Column(String, default=make_ticket)
    role = Column(Integer, default=ROLE_GUEST)

    @property
    def name(self):
        return self.email.split('@')[0].replace('.', ' ')

    @hybrid_property
    def is_member(self):
        return self.role >= ROLE_MEMBER

    @hybrid_property
    def is_leader(self):
        return self.role >= ROLE_LEADER

    @classmethod
    def get_from_cache(Class, id):
        if id is None:
            return
        return Class._make_query(id).get(id)

    @classmethod
    def clear_from_cache(Class, id):
        Class._make_query(id).invalidate()

    @classmethod
    def _make_query(Class, id):
        return db.query(Class).options(FromCache(
            cache_key='%s.id=%s' % (Class.__name__, id)))
