from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///userdb', echo=True)
Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    consumer_key = Column(String)
    consumer_secret = Column(String)
    oauth_token = Column(String)
    oauth_token_secret = Column(String)

    def __init__(self, username, password,consumer_key,consumer_secret):

        self.username = username
        self.password = password
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        # create tables
        Base.metadata.create_all(engine)
