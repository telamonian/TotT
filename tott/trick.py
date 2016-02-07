from collections import Counter
from itertools import chain
import nltk
from nltk.corpus import stopwords
import numpy as np
import os

thisDirPath = os.path.dirname(os.path.realpath(__file__))
nltk.data.path.append(thisDirPath)

from container import ContainerSet
from helper import timewith

class Trick(object):
    filterSet = set(stopwords.words('english')) | {'gif'}
    normalizeTop = 20

    @classmethod
    def filter(cls, container):
        filterWords = []
        for word in container:
            if word in cls.filterSet:
                filterWords.append(word)
        [container.pop(word) for word in filterWords]

    def __init__(self, **kwargs):
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
        normalizeTop = kwargs['normalizeTop'] if 'normalizeTop' in kwargs else self.normalizeTop
        printTop = kwargs['printTop'] if 'printTop' in kwargs else False
        popQueries = kwargs['popQueries'] if 'popQueries' in kwargs else True

        counter = np.sum([cloud.getCounter() for cloud in self.getClouds(*queries, depth=depth)])

        if popQueries:
            [counter.pop(query) for query in queries]
        self.filter(counter)

        if printTop:
            print counter.most_common(printTop)

        if len(counter) < 1:
            return counter

        counts = np.array(counter.values())
        zscoreCounts = np.array(zip(*counter.most_common(normalizeTop))[1])
        mean = np.mean(zscoreCounts)
        std = np.std(zscoreCounts)
        zscore = (counts - mean)/std
        for i,key in enumerate(counter.iterkeys()):
            counter[key] = zscore[i]

        return counter

    def getSet(self, *queries, **kwargs):
        depth = kwargs['depth'] if 'depth' in kwargs else self.depth

        retSet = set.intersection(*[cloud.getSet() for cloud in self.getClouds(*queries, depth=depth)])
        self.filter(retSet)
        return retSet

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