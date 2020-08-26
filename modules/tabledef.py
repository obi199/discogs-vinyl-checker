from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from discogs_settings import userdb, table
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt
import discogs_settings
import uuid
from flask_sqlalchemy import SQLAlchemy
# password = sha256_crypt.encrypt("password")
# password2 = sha256_crypt.encrypt("password")
# print(sha256_crypt.verify("password", password))

# engine = create_engine(userdb, echo=True,connect_args={'check_same_thread': False})
# Base = declarative_base()
# Session = sessionmaker(bind=engine)
# s = Session()

# class User(Base):
#     __tablename__ = table
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String)
#     password = Column(String)
#     consumer_key = Column(String)
#     consumer_secret = Column(String)
#     oauth_token = Column(String)
#     oauth_token_secret = Column(String)
#
#     def __init__(self, username, password,consumer_key,consumer_secret,oauth_token,oauth_token_secret):
#         #self.id = id
#         self.username = username
#         self.password = password
#         self.consumer_key = consumer_key
#         self.consumer_secret = consumer_secret
#         self.oauth_token = oauth_token
#         self.oauth_token_secret = oauth_token_secret
#         # create tables
#         Base.metadata.create_all(engine)

def check_encrypted_password(password, hashed):
    return sha256_crypt.verify(password, hashed)

def check_credentials(User, POST_USERNAME='', POST_PASSWORD=''):
    query = User.query.filter_by(username = POST_USERNAME).first()
    if check_encrypted_password(POST_PASSWORD, query.password):
        return query
#add user and check if name exists in db
def add_user(POST_USERNAME, POST_PASSWORD,consumer_key = 'KpmpkHQmVfudnTVufUME',consumer_secret = 'tEAvaSrmmXHKjzfHfqCAEWpXOdULpPXo', \
    oauth_token = 'aXqDiWXTljKJtlyriboZOwUxBNyAhQDyOTqIaXJU',oauth_token_secret ='bTcOJUaVaTrNwENYgpnoPAaUzrNsTHdfFOTYTFjz'):
    USER_ID = uuid.uuid4()
    password = sha256_crypt.encrypt(POST_PASSWORD)
    new_user = User(username = POST_USERNAME, password = password, consumer_key=consumer_key,consumer_secret= consumer_secret, \
    oauth_token = oauth_token, oauth_token_secret=oauth_token_secret)
    s.add(new_user)
    s.flush()
    s.commit()

def update_password(POST_USERNAME, POST_PASSWORD):

    our_user = s.query(User).filter_by(username=POST_USERNAME).first()
    password = sha256_crypt.encrypt(POST_PASSWORD)

    our_user.password = password
    s.flush()
    s.commit()

if __name__ == "__main__":
    #update_password('admin','pass')
    #add_user(12, 'sdsd', 'dsdsd')
    user = s.query(User).filter(User.username == 'admin').first()

    print user.password
    # for instance in s.query(User).order_by(User.id):
    #     print(instance.username, instance.password)
