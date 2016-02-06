
__author__ = 'Henry'

"""
This contains a class that will allow the user to take
advantage of the API of the Memegenerator
"""

class get_meme_info:
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
