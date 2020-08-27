

import functools
from flask import jsonify, json, Flask, redirect, render_template, request, session, abort
from flask import Blueprint, flash, g, url_for
from discogs_client_oauth import authenticate
import discogs_client
import discogs_settings
import os
from flask_sqlalchemy import SQLAlchemy
import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
        add_user(POST_USERNAME, POST_PASSWORD)
        flash('User created!')
        #return home()
    return render_template('auth/register.html')

#
@bp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
        user = db.check_credentials(db.User,POST_USERNAME,POST_PASSWORD)
        if POST_USERNAME:
            if user:
                # global discogsclient
                # discogsclient = discogs_client.Client(discogs_settings.user_agent, result.consumer_key, \
                # result.consumer_secret, result.oauth_token, result.oauth_token_secret)
                session['logged_in'] = True
                session['user_id'] = user.id
                print session['user_id']
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

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
