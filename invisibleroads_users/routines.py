from miscreant.aes.siv import SIV

from .constants import S


TRANSLATOR = SIV(S['secret'])


def encrypt(text):
    return TRANSLATOR.seal(text.encode('utf-8'))


def decrypt(text):
    return TRANSLATOR.open(text).decode('utf-8')
