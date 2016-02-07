__author__ = 'Henry'

from collections import Counter
import json
import numpy as np
import urllib2

from trick import Trick

__all__ = ['GetUrbanDictionaryInfo', 'UrbanDictionary']

class GetUrbanDictionaryInfo(object):
    def __init__(self):
        return

    def get_entry_tags(self):
        """
        returns a list of tags associated with the word or phrases looked up
        useful for looking up associated words
        """
        return self.data['tags']

    def get_entry_definition_all(self):
        """
        ranks definitions based off of the net number of thumbs ups
        returns a list of strings whcih has the definition
        """
        ranking_and_def = []
        for x in self.data['list']:
            definition = x['definition']
            net_thumbs = x['thumbs_up'] - x['thumbs_down']
            ranking_and_def.append([net_thumbs,definition])
        ranking_and_def.sort(key=lambda x: int(x[0]))
        definitions = []
        for x in ranking_and_def:
            definitions.append(x[1])
        return definitions

    def get_json_object(self,query):
        """
        Accepts a query to make a data object
        creates a class object that is a dictionary of results
        """
        response = urllib2.urlopen(query)
        self.data = json.load(response)
        return

    def make_query_simple(self, word):
        """
        Make a query with a single word
        Type must be a string
        Will return an address used to search for the
         gifs that fit the word
        """
        url_frame1 = "http://api.urbandictionary.com/v0/define?term="
        return url_frame1 + word

    def make_query_complex(self, words):
        """
        Same function as make_query_simple but accepts a list
        """
        url_frame1 = "http://api.urbandictionary.com/v0/define?term="
        combo = "+".join(words)
        return url_frame1 + combo

class UrbanDictionary(Trick, GetUrbanDictionaryInfo):
    def __contains__(self, key):
        return True

    def __getitem__(self, key):
        query = self.make_query_complex([key])
        self.get_json_object(query)
        return self.get_entry_tags()

if __name__ == '__main__':
    words = ['happy',
             'smile',
             'lucky']

    def main1():
        test1 = GetUrbanDictionaryInfo()
        query = test1.make_query_complex(['shoelace'])
        test1.get_json_object(query)
        definitions = test1.get_entry_tags()
        for x in definitions:
            print x
            print
        return

    def main2():
        ud = UrbanDictionary()
        counter = ud.getCounter(*words)
        print counter.most_common(10)

    main2()
