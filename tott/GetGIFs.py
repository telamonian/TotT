
__author__ = 'Henry'

import urllib2
import json

class GetGifInfo:
    def __init__(self):
        return

    def make_query_simple(self, word):
        """
        Make a query with a single word
        Type must be a string
        Will return an address used to search for the
         gifs that fit the word
        """
        url_frame1 = "http://api.giphy.com/v1/gifs/search?q="
        url_frame2 = "&api_key=dc6zaTOxFJmzC"
        return url_frame1 + word + url_frame2

    def make_query_complex(self, words):
        """
        Same function as make_query_simple but accepts a list
        """
        url_frame1 = "http://api.giphy.com/v1/gifs/search?q="
        url_frame2 = "&api_key=dc6zaTOxFJmzC"
        combo = "+".join(words)
        return url_frame1 + combo + url_frame2

    def get_json_object(self,query):
        """
        Accepts a query to make a data object
        """
        response = urllib2.urlopen(query)
        self.data = json.load(response)
        return

    def get_object_words_all(self):
        """
        From the data object made from the get_json_object
         pulls out words associated with the images pulled up
        Will not pull out independent lines and will be useful for
         getting more words
        """
        associated_words = []
        for entry in self.data['data']:
            words = entry['slug'].strip()
            words = words.split('-')
            words.pop()
            associated_words.append(words)
        return associated_words

    def get_embedded_url_all(self):
        """
        Get all of the embedded urls from the data object
        """
        associated_urls = []
        for entry in self.data['data']:
            myurl = entry['embed_url']
            associated_urls.append(myurl)
        return associated_urls

    def get_object_words_single_line(self,linenum):
        """
        From the data object made from the get_json_object
         pulls out words associated with the images pulled up
        Will pull out independent lines and will be useful for
         getting more words, only accepts one line (type int)_
        """
        words = self.data['data'][linenum]['slug'].strip()
        return words.split('-')

    def flatten(self,nested_info):
        """
        Function that accepts a nested list of lists and
         returns a flattened list
        """
        return [ item for sublist in nested_info for item in sublist ]

    def get_image_info_all(self):
        """
        returns the image dictionary from Giphy API
        will have all of the different formats of the images and their urls
        """
        image_dictionaries = []
        for x in self.data['data']:
            image_dictionaries.append(x['images'])
        return image_dictionaries

    def get_gif_url_original_size_all(self):
        """
        This will get all of urls for the gifs returned by the
        query for the original size.
        """
        gif_url_all = []
        for x in self.data['data']:
            gif_url_all.append(x['images']['original']['url'])
        return gif_url_all

if __name__ == '__main__':
    def main1():
        test1 = GetGifInfo()
        query = test1.make_query_simple('snoopy')
        test1.get_json_object(query)
        #print test1.data['data']
        word_cloud = test1.get_gif_url_original_size_all()
        print word_cloud
        return

    main1()
