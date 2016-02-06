
__author__ = 'Henry'

"""
This contains a class that will allow the user to take
advantage of the API of the Memegenerator
"""

import urllib2
import json

class GetMemeInfo:
    def __init__(self):
        return

    def make_query_simple(self, word):
        """
        Make a query with a single word
        Type must be a string
        Will return an address used to search for the
         gifs that fit the word
        """
        url_frame1 = 'http://version1.api.memegenerator.net/Generators_Search?q='
        url_frame2 = '&pageIndex=0&pageSize=12'
        return url_frame1 + word + url_frame2

    def make_query_complex(self, words):
        """
        Same function as make_query_simple but accepts a list
        """
        url_frame1 = 'http://version1.api.memegenerator.net/Generators_Search?q='
        url_frame2 = '&pageIndex=0&pageSize=12'
        combo = "+".join(words)
        return url_frame1 + combo + url_frame2

    def get_json_object(self,query):
        """
        Accepts a query to make a data object
        returns a dictionary of results
        """
        response = urllib2.urlopen(query)
        data = json.load(response)
        self.search_results = data['result']
        return

    def get_image_url_all(self):
        """
        returns a list of image urls ranking in the order of their
        ranking on the meme generator
        """
        urls_and_rankings = []
        for x in self.search_results:
            rank = x['ranking']
            url = x['imageUrl']
            urls_and_rankings.append([rank,url])
        urls_and_rankings.sort(key=lambda x: int(x[0]))
        urls = []
        for x in urls_and_rankings:
            urls.append(x[1])
        return urls

if __name__ == '__main__':
    def main1():
        test1 = GetMemeInfo()
        query = test1.make_query_simple('happy')
        test1.get_json_object(query)
        rankedurls = test1.get_image_url_all()
        for x in rankedurls:
            print x
            #print
        return

    main1()
