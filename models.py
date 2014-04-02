from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declared_attr, declarative_base


Base = declarative_base()


class BaseTable(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class Comment(Base, BaseTable):
    id = Column(String(16), primary_key=True)
    subreddit = Column(String(20))
    author = Column(String(20))
    body = Column(Text)
