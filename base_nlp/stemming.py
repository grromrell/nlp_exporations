import numpy as np

class PorterStemmer(object):
    def __init__(self):
        self.vowel_index = None
        self.li_index = None
        self.r_index = None

    def _index_maker(self, word):
        vowel_index = np.zeros(len(word))
        li_index = np.zeros(len(word))
        r1 = []
        r2 = []
        for i in xrange(len(word)):
            if word[i] in ['a', 'e', 'i', 'o', 'u', 'y']:
                vowel_index[i] = 1
            if word[i] in ['c', 'd', 'e', 'g', 'h', 'k', 'm', 'n', 'r', 't']:
                li_index[i] = 1
            if i+1 > len(word):
                continue
            if word[i] in ['b', 'd', 'f', 'g', 'm', 'n', 'p', 'r','t']:
                if word[i] == word[i+1]:
                    vowel_index[i], vowel_index[i+1] = 2
        for j in xrange(len(word)):
            if word[i-1:i+1] == 
                

        
