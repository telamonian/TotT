import numpy as np

from container import ContainerDict
from GetGIFs import Giffy
from GetUrbanDictionary import UrbanDictionary
from thesaurus import Thesaurus
from os.path import dirname, join

mobyThesaurusFPath = join(dirname(__file__),'mthesaur.txt')

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
        return 'moby_thesaurus', Thesaurus(mobyThesaurusFPath, **kwargs)

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
        '''
        return np.sum([trick.getCounter(*queries, **kwargs) for trick in self.values() if trick.active])

    def setActive(self, active=True, name=None):
        if name is None:
            [trick.setActive(active=active) for trick in self]
        else:
            self[name].setActive(active=active)

if __name__=='__main__':
    words = ['happy',
             'smile',
             'lucky']

    bot = BagOfTricks()

    counter = bot.getCounter(*words, printTop=20)
    print counter.most_common(20)
    # [('felicitous', 97), ('appropriate', 96), ('good', 92), ('fit', 90), ('fitting', 90)]
