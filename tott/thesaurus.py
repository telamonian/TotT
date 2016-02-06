from collections import Counter, OrderedDict
from itertools import chain
import numpy as np

class Container(object):
    def __contains__(self, key):
        return key in self.container

    def __getitem__(self, *keys):
        if len(keys)<=1:
            return self.container[keys[0]]
        else:
            return [self.container[key] for key in keys]

    def __iter__(self):
        return self.container.__iter__()

    def __setitem__(self, key, value):
        self.container[key] = value

    def append(self, item):
        self.container.append(item)

class ContainerSet(Container):
    def getSet(self):
        pass

    def intersection(self, *others):
        return set.intersection(*([self.getSet()] + [other.getSet() for other in others]))

    def __and__(self, *others):
        return self.intersection(*others)

    def __rand__(self, *others):
        return set.intersection(*([self.getSet()] + [other for other in others]))

class Thesaurus(Container):
    depth = 3

    def __init__(self, fPath):
        with open(str(fPath)) as f:
            self.container = OrderedDict([(wordList[0], set(wordList[1:])) for wordList in [line.strip().split(',') for line in f]])

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

    def keys(self):
        return self.container.keys()

    def items(self):
        return self.container.items()

    def values(self):
        return self.container.values()

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