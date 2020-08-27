import functools
from flask import jsonify, json, Flask, flash, redirect, render_template, request, session, abort
from flask import Blueprint, flash, g, url_for
import discogs_settings
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from flask_sqlalchemy import SQLAlchemy
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

dbase = SQLAlchemy()

class User(dbase.Model):
    __tablename__ = table
    id = dbase.Column(Integer, primary_key=True, autoincrement=True)
    username = dbase.Column(String)
    password = dbase.Column(String)
    consumer_key = dbase.Column(String)
    consumer_secret = dbase.Column(String)
    oauth_token = dbase.Column(String)
    oauth_token_secret = dbase.Column(String)

def __init__(self, username, password,consumer_key,consumer_secret,oauth_token,oauth_token_secret):
    #self.id = id
    self.username = username
    self.password = password
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.oauth_token = oauth_token
    self.oauth_token_secret = oauth_token_secret

def check_encrypted_password(password, hashed):
    return sha256_crypt.verify(password, hashed)

def check_credentials(User, POST_USERNAME='', POST_PASSWORD=''):
    query = User.query.filter_by(username = POST_USERNAME).first()
    if query:
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
