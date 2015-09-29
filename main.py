"""
Parse thesaurus into dict... I hope this is not too massive.
"""

import re
import sys

def ParseThesaurusIntoDict(thesaurus_fn):
    # this is specifically formatted to the open office thesaurus as of now
    # JRJ 2015-09-29

    thes_dict = {}
    entry_string = re.compile('^.*\|[0-9]*$')
    # e.g. for above
    # simple|9
    # this tells us there are 9 different meanings for simple which will follow below
    mf = open(thesaurus_fn,'r')
    while True:
        line = mf.readline()
        if not line: break
        match = entry_string.match(line)
        if match: # we have found the start of an entry, parse for n lines
            n = int(line.split('|')[1].strip())
            word = line.split('|')[0].strip()
            thes_dict[word] = [] # ready list for synonyms
            for i in range(n): # iterate over next n lines
                # may leave a stray newline char
                synonyms = [x.strip() for x in mf.readline().split('|')]
                # ignore first entry as that is part of speech
                for syn in synonyms[1:]:
                    thes_dict[word].append(syn)

    return thes_dict

if __name__ == '__main__':
    thes_dict = ParseThesaurusIntoDict('./MyThes-1.0/th_en_US_new.dat')
    print 'successful: ' + str(thes_dict['successful'])
    print 'code: ' + str(thes_dict['code'])
