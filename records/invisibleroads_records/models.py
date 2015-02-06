from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from .libraries.cache import make_query_factory


db = scoped_session(sessionmaker(
    extension=ZopeTransactionExtension(),
    query_cls=make_query_factory))
Base = declarative_base()
