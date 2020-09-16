from base64 import b64decode
from miscreant.aes.siv import SIV

from .constants import S


def encrypt(text):
    return S['crypt'].seal(text.encode('utf-8'))


def decrypt(text):
    return S['crypt'].open(text).decode('utf-8')


def get_crypt():
    key = b64decode(S['secret'])
    return SIV(key)
