from invisibleroads_records.models import (
    CreationMixin,
    ModificationMixin,
    RecordMixin)
from sqlalchemy import Column
from sqlalchemy.ext.hybrid import Comparator, hybrid_property
from sqlalchemy.types import LargeBinary

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
        return op(self.__clause_element__(), encrypt(
            other.casefold()), **kwargs)


class EncryptedNameMixin(object):
    'Mixin class for a case-insensitive encrypted name'
    _name = Column(LargeBinary)

    @hybrid_property
    def name(self):
        return CaseInsensitiveString(decrypt(self._name))

    @name.setter
    def name(self, name):
        self._name = encrypt(name.casefold())

    @name.comparator
    def name(Class):
        return CaseInsensitiveEncryptComparator(Class._name)


class EncryptedEmailMixin(object):
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


class EncryptedImageUrlMixin(object):
    'Mixin class for a case-insensitive encrypted image URL'
    _image_url = Column(LargeBinary)

    @hybrid_property
    def image_url(self):
        return CaseInsensitiveString(decrypt(self._image_url))

    @image_url.setter
    def image_url(self, image_url):
        self._image_url = encrypt(image_url.casefold())

    @image_url.comparator
    def image_url(Class):
        return CaseInsensitiveEncryptComparator(Class._image_url)


class UserMixin(
        EncryptedNameMixin,
        EncryptedEmailMixin,
        EncryptedImageUrlMixin,
        ModificationMixin,
        CreationMixin,
        RecordMixin):
    __tablename__ = 'user'
