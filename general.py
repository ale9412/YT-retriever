# -*- coding: utf-8 -*-

import os
import time
import pickle
import pprint
import requests



class Builder(object):

    _BASE_URL = "https://www.googleapis.com/youtube/v3/"
    # _API_KEY = "AIzaSyAB6526c3Kdl0lM9Vu6bdFAnBbqJ6p5fWA"
    _API_KEY = "AIzaSyCCHjrrkfRyd7tv94XCsO31Uii0rV9YjUQ"

    _headers = {"Accept": "application/json", "Accept-Encoding":"gzip"}

    def __init__(self, resource):
        self.resource_name = resource
        self.params = None

    def __getattr__(self, method):
        """Dynamically create method"""

        def wrapper(**kwargs):
            return self.execute(method, **kwargs)
        return wrapper

    
    def execute(self, method, **kwargs):
        self.params = kwargs
        self.params["key"] = self._API_KEY
        full_url = os.path.join(self._BASE_URL, self.resource_name)
        response = requests.get(full_url, headers=self._headers, params=self.params)
        return response.json()


def discover():
    iters = 0
    max_results = 5

    search = Builder("search")

    nextPageToken = "CLYHEAA"
    ids = set()
    while iters<200:
        print("NextPageToke:",nextPageToken)
        response = search.list(
        part="snippet",
        maxResults=50,
        publishedAfter="2010-02-26T15:00:00Z",
        type="channel",
        pageToken=nextPageToken,
        order="date",
        fields="nextPageToken,pageInfo/totalResults,items(id/channelId)"
    )   
        break
        channels = response["items"]
        
        for channel in channels:
            id = channel["id"]["channelId"]
            
            ids.add(id)

        iters += 1
        try:
            nextPageToken = response["nextPageToken"]
        except KeyError:
            print("No more results")
            break
      
        time.sleep(0.2)

    # with open("ids.pickle", "wb") as ids_file:
    #     values = {}
    #     values["nextPageToken"] = nextPageToken
    #     values["ids"] = ids
    #     pickle.dump(values, ids_file)

    pprint.pprint(response)

    # return response


if __name__ == "__main__":

  discover()
    

