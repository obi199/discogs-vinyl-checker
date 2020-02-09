# -*- coding: utf-8 -*-
import json
import discogs_client

class results:

    def __init__(self, stringInput, discogsclient, format, type):
        self._discogsclient = discogsclient
        self._stringInput = stringInput
        self._results = self._discogsclient.search(self._stringInput, format=format, type=type)
    def results(self):
        results = self._results
        return results
    def release_results(self):
        items_per_page = int(self._results.per_page)
        results_per_page = []
        for i in self._results.page(0):
            k = release_data(i)
            result = str(i)
            result = result.split("'")
            newDic = {'type': k.query('type'),\
            'name': result[1], \
            'hyperlink': "https://www.discogs.com"  + i.data['uri'], \
            'year' : k.query('year'), \
            'label': k.query('label'), \
            'catno': k.query('catno'),\
            'country': k.query('country'),\
            'community': k.query('community'),\
            'id': k.query('id'),\
            'format': k.query('format')}
            results_per_page.append(newDic)
        return results_per_page

class release_data:

    def __init__(self, release):
        self._release = release

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
        #print self._release.data['resource_url']
    def data(self):
        data = self._release.data
        json.dumps(data)
        return data
    def format_tracklist(self, tracklist):
        tracks = []
        for track in tracklist  :
            #x = ""
            x = track['position'] + ": " + track['title'] + " " + track['duration']
            tracks.append(x)
        return tracks
    def videos(self):
        vids = []
        dict={}
        if 'videos' in self._release.data:
            for video in self._release.data['videos']:
                vid_id = self.vid_id(video['uri'])
                dict[video['description']] = vid_id
            vids.append(dict)
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
        for track in tracklist  :
            #x = ""
            x = track['position'] + " " + track['title'] + " " + track['duration']
            tracks.append(x)
        return tracks
    def videos(self):
        vids = []
        dict={}
        if 'videos' in self._master.data:
            for video in self._master.data['videos']:
                vid_id = self.vid_id(video['uri'])
                dict[video['description']] = vid_id
            vids.append(dict)
        return vids
    def vid_id(self, uri):
        string, vid_id = uri.split('v=')
        return vid_id

class artist:

    def __init__(self, artist):
        self._artist = artist
        self._artist.fetch(self._artist.url)
        print self._artist.data
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
    def collection_item_by_release(self):
        #to do
        #/users/{username}/collection/releases/{release_id}
        pass
    def collection_value(self):
        return self.client._get("{0}/collection/value".format(self.userObj.data['resource_url']))
