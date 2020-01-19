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
        print self._release.data['resource_url']
    def data(self):
        data = self._release.data
        json.dumps(data)
        return data
    def artists_name(self):
        if 'artists' in self._release.data:
            artists_name = self._release.data['artists'][0]['name']
            return artists_name
    def labels(self):
        if 'labels' in self._release.data:
            labels = self._release.data['labels'][0]['name']
            return labels
    def catno(self):
        if 'labels' in self._release.data:
            catno = self._release.data['labels'][0]['catno']
            return catno
    def rating_average(self):
        if 'community' in self._release.data:
            rating_average = self._release.data['community']['rating']['average']
            return rating_average
    def tracklist_format(self, tracklist):
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
    def formats(self):
        if 'formats' in self._release.data:
            formats = self._release.data['formats'][0]['descriptions']
        else:
            formats = []
        return formats
    def image(self):
        img = self._release.data['images'][0]['resource_url']
        return img
    def uri150(self):
        uri150 = self._release.data['images'][0]['uri150']
        return uri150
    def name(self):
        if 'name' in self._release.data:
            artists_name = self._release.data['aliases'][0]['name']
            return artists_name

class full_master_object:

    def __init__(self, id, discogsclient):
        self._discogsclient = discogsclient
        self._master = self._discogsclient.master(id)
        self._master.fetch(self._master.url)
        print self._master.data['resource_url']
    def data(self):
        data = self._master.data
        json.dumps(data)
        return data
    def artists_name(self):
        if 'artists' in self._master.data:
            artists_name = self._master.data['artists'][0]['name']
            return artists_name
    def title(self):
        if 'title' in self._master.data:
            title = self._master.data['title']
            return title
    def year(self):
        if 'year' in self._master.data:
            year = self._master.data['year']
            return year
    def tracklist(self):
        if 'tracklist' in self._master.data:
            tracklist = self._master.data['tracklist']
        else:
            tracklist = ['No tracklist']
        return tracklist
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
    def image(self):
        img = self._master.data['images'][0]['resource_url']
        return img
    def uri150(self):
        uri150 = self._master.data['images'][0]['uri150']
        return uri150
    def lowest_price(self):
        lowest_price = ""
        if 'lowest_price' in self._master.data:
            lowest_price = self._master.data['lowest_price']
        return lowest_price
    def main_release_url(self):
        main_release_url = ""
        if 'main_release_url' in self._master.data:
            main_release_url = self._master.data['main_release_url']
        return main_release_url
    def main_release(self):
        main_release = ""
        if 'main_release' in self._master.data:
            main_release = self._master.data['main_release']
        return main_release
    def genres(self):
        genres = []
        if 'genres' in self._master.data:
            genres = self._master.data['genres']
        return genres

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
