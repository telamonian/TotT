___all__ = ['Container', 'ContainerDict', 'ContainerSet']

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

class ContainerDict(Container):
    def keys(self):
        return self.container.keys()

    def items(self):
        return self.container.items()

    def values(self):
        return self.container.values()

class ContainerSet(Container):
    def append(self, item):
        self.container.append(item)

    def getSet(self):
        pass

    def intersection(self, *others):
        return set.intersection(*([self.getSet()] + [other.getSet() for other in others]))

    def __and__(self, *others):
        return self.intersection(*others)

    def __rand__(self, *others):
        return set.intersection(*([self.getSet()] + [other for other in others]))