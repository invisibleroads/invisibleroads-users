from invisibleroads_records.models import (
    CreationMixin,
    ModificationMixin,
    RecordMixin)
from sqlalchemy import Column
from sqlalchemy.ext.hybrid import Comparator, hybrid_property
from sqlalchemy.types import LargeBinary, Unicode

from .routines import decrypt, encrypt


class CaseInsensitiveString(str):

    def __lt__(self, other):
        return self.casefold() < other.casefold()

    def __le__(self, other):
        return self.casefold() <= other.casefold()

    def __eq__(self, other):
        return self.casefold() == other.casefold()

    def __ne__(self, other):
        return self.casefold() != other.casefold()

    def __gt__(self, other):
        return self.casefold() > other.casefold()

    def __ge__(self, other):
        return self.casefold() >= other.casefold()


class CaseInsensitiveEncryptComparator(Comparator):

    def operate(self, op, other, **kwargs):
        if hasattr(other, '__iter__'):
            other = [_.casefold() for _ in other]
        else:
            other = other.casefold()
        return op(self.__clause_element__(), encrypt(other), **kwargs)


class EmailMixin(object):
    'Mixin class for a case-insensitive encrypted email address'
    _email = Column(LargeBinary)

    @hybrid_property
    def email(self):
        return CaseInsensitiveString(decrypt(self._email))

    @email.setter
    def email(self, email):
        self._email = encrypt(email.casefold())

    @email.comparator
    def email(Class):
        return CaseInsensitiveEncryptComparator(Class._email)


class UserMixin(EmailMixin, ModificationMixin, CreationMixin, RecordMixin):
    __tablename__ = 'user'
    email = Column(Unicode, unique=True)
    name = Column(Unicode)
    image_url = Column(Unicode)
