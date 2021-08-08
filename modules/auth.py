

import functools
from flask import jsonify, json, Flask, redirect, render_template, request, session, abort
from flask import Blueprint, flash, g, url_for
#from modules.discogs_client_oauth import authenticate
import discogs_client
#from modules import discogs_settings
import os
from flask_sqlalchemy import SQLAlchemy
from modules import db
from passlib.hash import sha256_crypt
import uuid

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/register', methods=['POST','GET'])
@login_required
def register():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
        consumer_key = str(request.form['consumer_key'])
        consumer_secret = str(request.form['consumer_secret'])
        oauth_token = str(request.form['oauth_token'])
        oauth_token_secret = str(request.form['oauth_token_secret'])

        if not POST_USERNAME:
            error = 'Username is required.'
        elif not POST_PASSWORD:
            error = 'Password is required.'
        # elif username exists:
        error = add_user(db.User,POST_USERNAME, POST_PASSWORD,consumer_key,consumer_secret,oauth_token,oauth_token_secret)
        flash(error)
        #return home()
    return render_template('auth/register.html')

#
@bp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
        user = check_credentials(db.User,POST_USERNAME,POST_PASSWORD)
        if POST_USERNAME and POST_PASSWORD:
            if user:
                session['logged_in'] = True
                session['user_id'] = user.id
                print(session['user_id'])
                return redirect('/')
            else:
                flash('wrong password!')
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.User.query.filter_by(id = user_id).first()
        #print(g.user.username)
        # g.user = get_db().execute(
        #     'SELECT * FROM user WHERE id = ?', (user_id,)
        # ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    session['logged_in'] = False
    return redirect('/auth/login')


def add_user(User,POST_USERNAME, POST_PASSWORD,consumer_key = '',consumer_secret = '', \
    oauth_token = '',oauth_token_secret =''):
    #USER_ID = uuid.uuid4()
    password = sha256_crypt.encrypt(POST_PASSWORD)
    if User.query.filter_by(username = POST_USERNAME).first() is None:
        new_user = User(username = POST_USERNAME, password = password, \
        consumer_key=consumer_key, \
        consumer_secret= consumer_secret, \
        oauth_token = oauth_token, oauth_token_secret=oauth_token_secret)
        db.dbase.session.add(new_user)
        db.dbase.session.flush()
        db.dbase.session.commit()
        error = 'User created'
    else:
        print('error user existing!')
        error = 'Username already exists!'
    return error

def check_encrypted_password(password, hashed):
    return sha256_crypt.verify(password, hashed)

def check_credentials(User, POST_USERNAME='', POST_PASSWORD=''):
    query = User.query.filter_by(username = POST_USERNAME).first()
    if query:
        if check_encrypted_password(POST_PASSWORD, query.password):
            return query

#def update_password(POST_USERNAME, POST_PASSWORD):
    #pass
