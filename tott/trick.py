from collections import Counter
from itertools import chain
import numpy as np

from container import ContainerSet

class Trick(object):
    def __init__(self, **kwargs):
        self.setActive(kwargs['active'] if 'active' in kwargs else True)
        self.depth = kwargs['depth'] if 'depth' in kwargs else 3

    def getCloud(self, query, depth=3):
        if depth < 1:
            return []
        cloud = Cloud(Layer({query}))
        for i in range(depth - 1):
            wordSets = []
            for wordSet in cloud[i]:
                for word in wordSet:
                    if word in self:
                        wordSets.append(set(self[word]))
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

class Layer(ContainerSet):
    def __init__(self, *wordSets):
        self.container = list(wordSets)

    def getCounter(self):
        return Counter(chain(*self))

    def getSet(self):
        return set.union(*self.container)