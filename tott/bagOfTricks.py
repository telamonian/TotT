import numpy as np

from container import ContainerDict
from thesaurus import Thesaurus

mobyThesaurusFPath = 'mthesaur.txt'

class BagOfTricks(ContainerDict):
    trickInits = ['initMobyThesaurus']

    def __init__(self, **kwargs):
        self.container = {key: trick for key,trick in [self.__getattribute__(bagInit)(**kwargs) for bagInit in self.trickInits]}

    def initMobyThesaurus(self, **kwargs):
        return 'moby_thesaurus',Thesaurus(mobyThesaurusFPath, **kwargs)

    def getCounter(self, *queries, **kwargs):
        return np.sum([trick.getCounter(*queries, **kwargs) for trick in self.values() if trick.active])

if __name__=='__main__':
    words = ['happy',
             'smile',
             'lucky']

    bot = BagOfTricks()

    counter = bot.getCounter(*words)
    print counter.most_common(5)
    # [('felicitous', 97), ('appropriate', 96), ('good', 92), ('fit', 90), ('fitting', 90)]