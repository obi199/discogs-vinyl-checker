from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from discogs_settings import userdb, table
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt

# password = sha256_crypt.encrypt("password")
# password2 = sha256_crypt.encrypt("password")
# print(sha256_crypt.verify("password", password))

engine = create_engine(userdb, echo=True,connect_args={'check_same_thread': False})
Base = declarative_base()
Session = sessionmaker(bind=engine)
s = Session()

class User(Base):
    __tablename__ = table
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

def check_credentials(POST_USERNAME, POST_PASSWORD):
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    return query.first()
#add user and check if name exists in db
def add_user(POST_USERNAME, POST_PASSWORD):
    password = sha256_crypt.encrypt(POST_PASSWORD)
    s.insert(User).values(username = POST_USERNAME, password = password)
