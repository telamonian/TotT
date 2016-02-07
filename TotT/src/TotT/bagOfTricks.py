from collections import Counter
import numpy as np

from container import ContainerDict
from GetGIFs import Giffy
from GetUrbanDictionary import UrbanDictionary
from thesaurus import Thesaurus
from time import sleep

mobyThesaurusFPath = 'mthesaur.txt'

class TrickInitsMetaclass(type):
    @property
    def inits(cls):
        return [name for name in dir(cls) if name[0]!='_']

class TrickInits(object):
    __metaclass__ = TrickInitsMetaclass
    @classmethod
    def _iterTricks(cls, **kwargs):
        return [getattr(cls, bagInit)(**kwargs) for bagInit in cls.inits]

    @classmethod
    def _getTrickDict(cls, **kwargs):
        return {key: trick for key,trick in cls._iterTricks(**kwargs)}

    @classmethod
    def initMobyThesaurus(cls, **kwargs):
        if 'mobyPath' not in kwargs:
            kwargs['mobyPath'] = mobyThesaurusFPath
        return 'moby_thesaurus', Thesaurus(**kwargs)

    @classmethod
    def initGiffy(cls, **kwargs):
        return 'giffy', Giffy(**kwargs)

    @classmethod
    def initUrbanDictionary(cls, **kwargs):
        return 'urban_dictionary', UrbanDictionary(**kwargs)

class BagOfTricks(ContainerDict):
    def __init__(self, **kwargs):
        self.container = TrickInits._getTrickDict(**kwargs)

    def getCounter(self, *queries, **kwargs):
        '''
        valid kwargs:
        depth: global control for depth of main search. default 3 (returns query + children + grandchildren)
        normalizeTop: number of top results to normalize over. default 20
        popQueries: remove the queries from the final return counter. default True
        resultCount: number of results returned
        '''
        active = kwargs['active'] if 'active' in kwargs else []
        resultCount = kwargs['resultCount'] if 'resultCount' in kwargs else 20
        retCounter = Counter()

        for trick in [trick for name,trick in self.items() if name in active]:
            counter = trick.getCounter(*queries, **kwargs)
            print counter.most_common(20)
            for key,val in counter.most_common(resultCount):
                if key in retCounter:
                    retCounter[key]+=(np.mean([retCounter[key], val]))
                else:
                    retCounter[key] = val

        return retCounter

        # return np.sum([trick.getCounter(*queries, **kwargs) for name,trick in self.items() if name in active])

if __name__=='__main__':
    words = ['happy',
             'smile',
             'lucky']

    # words = ['joke',
    #          'magic',
    #          'ribald']

    # words = ['red',
    #          'bull']

    # words = ['your ',
    #          'mom']

    bot = BagOfTricks(mobyPath=mobyThesaurusFPath)

    counter = bot.getCounter(*words, active=['moby_thesaurus', 'urban_dictionary'], printTop=20)
    print counter.most_common(20)
    # newWords = zip(*counter.most_common(20))[0]
    # for word in newWords:
    #     print bot.getCounter(word, active=['giffy'], printTop=20).most_common(20)
    #     sleep(1e-1)
    # [('felicitous', 97), ('appropriate', 96), ('good', 92), ('fit', 90), ('fitting', 90)]