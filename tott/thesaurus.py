from collections import Counter, OrderedDict
from itertools import chain
import numpy as np

from container import ContainerDict, ContainerSet

class Thesaurus(ContainerDict):
    depth = 3

    def __init__(self, fPath, active=True, depth=None):
        with open(str(fPath)) as f:
            self.active = active
            self.container = OrderedDict([(wordList[0], set(wordList[1:])) for wordList in [line.strip().split(',') for line in f]])
            if depth is not None:
                self.depth = depth

    def getCloud(self, query, depth=3):
        if depth < 1:
            return []
        cloud = Cloud(Layer({query}))
        for i in range(depth - 1):
            wordSets = []
            for wordSet in cloud[i]:
                for word in wordSet:
                    if word in self:
                        wordSets.append(self[word])
            cloud.append(Layer(*wordSets))
        return cloud

    def getClouds(self, *queries, **kwargs):
        depth = kwargs['depth'] if 'depth' in kwargs else self.depth

        return [self.getCloud(query=query, depth=depth) for query in queries]

    def getCounter(self, *queries, **kwargs):
        depth = kwargs['depth'] if 'depth' in kwargs else self.depth
        popQueries = kwargs['popQueries'] if 'popQueries' in kwargs else True

        counter = np.sum([cloud.getCounter() for cloud in self.getClouds(*queries, depth=depth)])
        if popQueries:
            [counter.pop(query) for query in queries]
        return counter

    def getSet(self, *queries, **kwargs):
        depth = kwargs['depth'] if 'depth' in kwargs else self.depth

        return set.intersection(*[cloud.getSet() for cloud in self.getClouds(*queries, depth=depth)])

    def setActive(self, active=True):
        self.active = active

class Cloud(ContainerSet):
    def __init__(self, *layers):
        self.container = list(layers)

    def getCounter(self):
        return np.sum([container.getCounter() for container in self])

    def getSet(self):
        return set.union(*[container.getSet() for container in self])

    def count(self, *others):
        c = Counter(chain)

class Layer(ContainerSet):
    def __init__(self, *wordSets):
        self.container = list(wordSets)

    def getCounter(self):
        return Counter(chain(*self))

    def getSet(self):
        return set.union(*self.container)

if __name__=='__main__':
    t = Thesaurus('mthesaur.txt')

    words = ['happy',
             'smile',
             'lucky']

    counter = t.getCounter(*words)
    print counter.most_common(5)
    # [('felicitous', 97), ('appropriate', 96), ('good', 92), ('fit', 90), ('fitting', 90)]