from base64 import b64decode
from datetime import datetime
from miscreant.aes.siv import SIV

from . import models as M
from .constants import S
from .events import UserAdded


def encrypt(text):
    return S['crypt'].seal(text.encode('utf-8'))


def decrypt(text):
    return S['crypt'].open(text).decode('utf-8')


def get_crypt():
    key = b64decode(S['secret'])
    return SIV(key)


def get_or_add_user(request, user_definition):
    db = request.db
    is_new_user = False
    User = M.User
    user_email = user_definition['email']
    user = db.query(User).filter_by(email=user_email).first()
    if not user:
        user = User.make_unique_record(db)
        user.email = user_email
        is_new_user = True
    user.name = user_definition['name']
    user.image_url = user_definition.get('imageUrl', S['image_url'])
    user.modification_datetime = datetime.utcnow()
    if is_new_user:
        request.registry.notify(UserAdded(user, request))
    return user


def check_authorization(user_definition):
    pass
