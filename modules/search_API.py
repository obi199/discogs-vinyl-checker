# -*- coding: utf-8 -*-
import json
import discogs_client
import logging
from modules import db
from sqlalchemy import func

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class results:

    def __init__(self, stringInput, discogsclient, format, type):
        self._discogsclient = discogsclient
        self._stringInput = stringInput
        self._results = self._discogsclient.search(
            self._stringInput, format=format, type=type)
        logger.info(self._stringInput)

    def results(self):
        results = self._results
        return results

    def release_results(self):
        items_per_page = int(self._results.per_page)
        release_results = []
        for i in self._results.page(0):
            k = release_data(i)
            #logger.info(k.data())
            logger.info(str(k.query('user_data')))
            newDic = {'type': k.query('type'),
                      'title': k.query('title'),
                      'group_title': k.query('title').split(" - "),
                      'hyperlink': "https://www.discogs.com" + i.data['uri'],
                      'year': k.query('year'),
                      'label': k.query('label'),
                      'catno': k.query('catno'),
                      'country': k.query('country'),
                      'community': k.query('community'),
                      'id': k.query('id'),
                      'format': k.query('format'),
                      'in_collection': k.query('user_data')['in_collection'],
                      'in_wantlist': k.query('user_data')['in_wantlist'],
                      'in_table2': self.check_with_table2(k.query('title'))}  # check with extra custom table in db
            release_results.append(newDic)
        return release_results

    def check_with_table2(self, title):
        tlist = title.split(" - ")
        try:
            query = db.Table2.query.filter(func.lower(db.Table2.artist) == func.lower(
                tlist[0]), func.lower(db.Table2.album) == func.lower(tlist[1])).first()
            if query:
                return query.track
            else:
                return None
        except:
            return None


class release_data:

    def __init__(self, release):
        self._release = release

    def data(self):
        return self._release.data

    def query(self, qstring):
        if qstring in self._release.data:
            query = self._release.data[qstring]
        else:
            query = ''
        return query
    # todo check if in collection
    # def collection_item(self):
    #     ucollection = discogs_client.models.CollectionItemInstance(self._release.id)
    #     return ucollection


class full_release_object(release_data):
    #fetches full data object
    def __init__(self, release):
        self._release = release
        self._release.fetch(self._release.url)

    def data(self):
        data = self._release.data
        json.dumps(data)
        return data

    def videos(self):
        vids = []
        if 'videos' in self._release.data:
            dict = {}
            for video in self._release.data['videos']:
                vids.append(self.vid_id(video['uri']))
        return vids

    def vid_id(self, uri):
        string, vid_id = uri.split('v=')
        return vid_id


class full_master_object:

    def __init__(self, master):
        self._master = master
        self._master.fetch(self._master.url)
    #    print self._master.data['resource_url']

    def query(self, qstring):
        if qstring in self._master.data:
            query = self._master.data[qstring]
        else:
            query = ''
        return query

    def tracklist_format(self, tracklist):
        tracks = []
        for track in tracklist:
            #x = ""
            x = track['position'] + " " + \
                track['title'] + " " + track['duration']
            tracks.append(x)
        return tracks

    def videos(self):
        vids = []
        dict = {}
        if 'videos' in self._master.data:
            dict = {}
            for video in self._master.data['videos']:
                vids.append(self.vid_id(video['uri']))
        return vids

    def vid_id(self, uri):
        string, vid_id = uri.split('v=')
        return vid_id


class artist:

    def __init__(self, artist):
        self._artist = artist
        self._artist.fetch(self._artist.url)
        self.all_data = self._artist.data

    def query(self, qstring):
        if qstring in self._artist.data:
            query = self._artist.data[qstring]
        else:
            query = ''
        return query


class user:

    def __init__(self, discogsclient):
        self._discogsclient = discogsclient
        self.userObj = self._discogsclient.identity()

    def identity(self):
        return self._discogsclient.identity()

    def collection(self):
        return self._discogsclient._get("{0}/collection/folders/1/releases".format(self.userObj.data['resource_url']))
        #return self.user.collection_all()

    def collection_value(self):
        return self.client._get("{0}/collection/value".format(self.userObj.data['resource_url']))
