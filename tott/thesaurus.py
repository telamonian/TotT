from collections import OrderedDict

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
        return self.intersection(*others)

class Thesaurus(Container):
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

    def keys(self):
        return self.container.keys()

    def items(self):
        return self.container.items()

    def values(self):
        return self.container.values()

class Cloud(ContainerSet):
    def __init__(self, *layers):
        self.container = list(layers)

    def getSet(self):
        return set.union(*[container.getSet() for container in self])

class Layer(ContainerSet):
    def __init__(self, *wordSets):
        self.container = list(wordSets)

    def getSet(self):
        return set.union(*self.container)