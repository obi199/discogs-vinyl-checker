import functools
from flask import jsonify, json, Flask, flash, redirect, render_template, request, session, abort
from flask import Blueprint, flash, g, url_for, current_app
from flask.cli import with_appcontext
import click
from modules import settings
import os
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
#from modules.discogs_settings import userdb, table
from sqlalchemy.orm import sessionmaker
#from passlib.hash import sha256_crypt
#import uuid

dbase = SQLAlchemy()

class User(dbase.Model):
    __tablename__ = settings.table
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

@click.command('init-db')
@with_appcontext
def init_db():
    # with current_app.open_resource('schema.sql') as f:
    #     dbase.executescript(f.read().decode('utf8'))
    dbase.create_all()
    click.echo('Initialized the database.')

def init_app(app):
    #app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
