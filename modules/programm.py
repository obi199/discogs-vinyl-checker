#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, json, Flask, flash, redirect, render_template, request, session, abort
import search_API
from discogs_client_oauth import authenticate
import discogs_client
import discogs_settings
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from flask_sqlalchemy import SQLAlchemy
# Session = sessionmaker(bind=engine)
# s = Session()
#userc = tabledef.user()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = discogs_settings.userdb
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = table
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    username = db.Column(String)
    password = db.Column(String)
    consumer_key = db.Column(String)
    consumer_secret = db.Column(String)
    oauth_token = db.Column(String)
    oauth_token_secret = db.Column(String)

def __init__(self, username, password,consumer_key,consumer_secret,oauth_token,oauth_token_secret):
    #self.id = id
    self.username = username
    self.password = password
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.oauth_token = oauth_token
    self.oauth_token_secret = oauth_token_secret
    # create tables
    #db.create_all()

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
        #return render_template('new_user.html')
    else:
        return render_template('search_discogs.html')

@app.route('/login', methods=['POST','GET'])
def do_login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
        result = check_credentials(User,POST_USERNAME,POST_PASSWORD)
        if POST_USERNAME:
            if result:
                global discogsclient
                discogsclient = discogs_client.Client(discogs_settings.user_agent, result.consumer_key, \
                result.consumer_secret, result.oauth_token, result.oauth_token_secret)
                session['logged_in'] = True
                return home()
            else:
                flash('wrong password!')

    # if request.method == 'POST':
    #     if str(request.form['new_user']):
    #         return render_template('new_user.html')
    #


@app.route('/new_user', methods=['POST'])
def new_user():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    add_user(POST_USERNAME, POST_PASSWORD)
    flash('User created!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/', methods=['POST','GET'])
def my_form_post():

    text = request.form['text']
    search_name = text
    format = ''
    type = ''
    if request.form['format'] == '1':
        format = 'vinyl'
    if request.form['type'] == '1':
        type = 'release'

    k = search_API
    search = k.results(search_name, discogsclient, format, type)
    result_Number = search.results().count
    result_Pages = search.results().pages
    result_PerPage = search.results().per_page
    results = search.release_results()
    return render_template('results.html', results = results, result_Number = result_Number, \
result_Pages = result_Pages, result_PerPage = result_PerPage)

@app.route('/<type>/<item_id>', methods=['POST', 'GET'])
def contact(type,item_id):
    # if request.method == 'POST':
    #     item_id = item_id #request.form['foo']
    #
    if type == 'release':
        release = discogsclient.release(item_id)
        k = search_API.full_release_object(release)
        #rObject = k.get_object(item_id, discogsclient).release_object(item_id)
        lowest_price = k.query('lowest_price')
        artists_name =  k.query('artists')[0]['name']
        title =  k.query('title')
        labels =  k.query('labels')[0]['name']
        catno =  k.query('labels')[0]['catno']
        year =  k.query('year')
        country =  k.query('country')
        rating_average = k.query('community')['rating']['average']
        have = k.query('community')['have']
        want = k.query('community')['want']
        tracklist = k.query('tracklist')
        tracks = k.format_tracklist(tracklist)
        videos = k.videos()
        formats = k.query('formats')[0]['descriptions']
        styles = k.query('styles')
        image = k.query('images')[0]['resource_url']
        uri150 = k.query('images')[0]['uri150']
        uri = k.query('uri')

        #all_data = k.data()#json.dumps(k.data)
        return render_template('info.html', item_id = item_id, \
                lowest_price = lowest_price, artists_name = artists_name, title = title, \
                labels = labels, catno = catno, year = year, country = country, \
                rating_average = rating_average, have = have, want = want, \
                tracks = tracks, videos = videos, formats = formats, styles = styles, uri150=uri150, uri=uri)

    elif type == 'master':
        master = discogsclient.master(item_id)
        k = search_API.full_master_object(master)
        artists_name =  k.query('artists')[0]['name']
        title =  k.query('title')
        year =  k.query('year')
        tracklist = k.query('tracklist')
        tracks = k.tracklist_format(tracklist)
        videos = k.videos()
        uri150 = k.query('images')[0]['uri150']
        genres = k.query('genres')
        lowest_price =k.query('lowest_price')
        return render_template('master.html', item_id = item_id, \
                artists_name = artists_name, title = title, \
                tracks = tracks, genres = genres, lowest_price = lowest_price, uri150=uri150)


    elif type == 'artist':
        artist = discogsclient.artist(item_id)
        k = search_API.artist(artist)
        artists_name =  k.query('name')
        name_var = k.query('namevariations')
        profile = k.query('profile')
        uri150 = k.query('images')[0]['uri150']
        url = k.query('resource_url')
        all_data = k.all_data
        #rObject.fetch(url)
        #rObject.fetch(rObject.url)
        return render_template('artist.html',all_data = all_data, url = url, artists_name = artists_name, \
        name_var = name_var, profile = profile, uri150 = uri150)

    else:
        None
        #item_id = k.search_discogs(rObject).id(rObject)

@app.route('/collection', methods=['POST','GET'])
def collection():
    import discogs_settings
    discogsclient = discogs_settings.client
    c = search_API.user(discogsclient)
    user = c.identity()
    print user
    ucollection = c.collection()

    print dir(ucollection)
    print ucollection
    return render_template('collection.html', ucollection = ucollection)



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug = True, host='0.0.0.0')#ssl_context='adhoc'
