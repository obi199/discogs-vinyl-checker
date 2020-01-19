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


app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        #print search_API.identity(discogsclient)

        return render_template('search_discogs.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        global discogsclient
        discogsclient = discogs_client.Client(discogs_settings.user_agent, result.consumer_key, \
        result.consumer_secret, result.oauth_token, result.oauth_token_secret)
        session['logged_in'] = True
    else:
        flash('wrong password!')
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
        k = search_API.full_master_object(item_id,discogsclient)
        artists_name =  k.artists_name()
        title =  k.title()
        year =  k.year()
        tracklist = k.tracklist()
        tracks = k.tracklist_format(tracklist)
        videos = k.videos()
        uri150 = k.uri150()
        genres = k.genres()
        lowest_price =k.lowest_price()
        return render_template('master.html', item_id = item_id, \
                artists_name = artists_name, title = title, \
                tracks = tracks, genres = genres, lowest_price = lowest_price, uri150=uri150)


    elif type == 'artist':
        k = search_API.full_release_object(item_id,discogsclient)
        artists_name =  k.artists_name()
        name_var = k.name_variations()
        profile = k.profile()
        url = k.data['resource_url']
        #rObject.fetch(url)
        #rObject.fetch(rObject.url)
        return render_template('artist.html',all_data = all_data, url = url, artists_name = artists_name, \
        name_var = name_var, profile = profile)

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
