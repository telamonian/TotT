from collections import Counter, OrderedDict
from itertools import chain
import numpy as np

from container import ContainerDict, ContainerSet
from trick import Trick

class Thesaurus(Trick, ContainerDict):
    def __init__(self, fPath, **kwargs):
        Trick.__init__(self, **kwargs)
        with open(str(fPath)) as f:
            self.container = OrderedDict([(wordList[0], set(wordList[1:])) for wordList in [line.strip().split(',') for line in f]])

if __name__=='__main__':
    t = Thesaurus('mthesaur.txt')

    words = ['happy',
             'smile',
             'lucky']

    counter = t.getCounter(*words)
    print counter.most_common(5)
    # [('felicitous', 97), ('appropriate', 96), ('good', 92), ('fit', 90), ('fitting', 90)]