# -*- coding: utf-8 -*-

import os
import requests


class Builder(object):

    _BASE_URL = "https://www.googleapis.com/youtube/v3/"
    _API_KEY = "AIzaSyAB6526c3Kdl0lM9Vu6bdFAnBbqJ6p5fWA"

    _headers = {"Accept": "application/json", "Accept-Encoding": "*"}

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
        return response.text


if __name__ == "__main__":
    search = Builder("search")

    response = search.list(
        part="snippet",
        maxResults=50,
        publishedAfter="2010-01-01T00:00:00Z",
        type="channel",
        fields="nextPageToken,pageInfo/totalResults,items(id/channelId)"
    )
    print(response)
    

