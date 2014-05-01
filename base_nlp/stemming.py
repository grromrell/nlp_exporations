VOWELS = frozenset(['a', 'e', 'i', 'o', 'u', 'y'])
DOUBLES = frozenset(['bb', 'dd', 'ff', 'gg', 'mm', 'nn', 'pp', 'rr', 'tt'])
LI_ENDING = frozenset(['c', 'd', 'e', 'g', 'h', 'k', 'm', 'n', 'r', 't'])

class PorterStemmer(object):
    
    def __init__(self):
        self.word = None 
        self.r1 = 0
        self.r2 = 0

    def stem(self, word):
        if word.startswith("'"):
            word = word[1:]
        if word.startswith("y"):
            word[0] = 'Y'
        if any(x in word for x in ['ay', 'ey', 'iy', 'oy', 'uy']):
            index = word.find('y')
            word[index] = 'Y'
        self.word = word
        self._region_finder()
        self.step0()
        self.step1a()
        self.step1b()
        self.step1c()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        yield self.word

    def _region_finder(self):
        for i in xrange(1, len(self.word)):
            if self.word[i] in VOWELS:
                continue
            if self.word[i-1] in VOWELS:
                self.r1 = i
                break
        for j in xrange(self.r1+1, len(self.word[self.r1:])):
            if self.word[j] in VOWELS:
                continue
            if self.word[j-1] in VOWELS:
                self.r2 = j
                break

    def step0(self):
        step_suffixes = ["'s'", "'s", "'"]
        suffix_list = [end for end in step_suffixes if self.word.endswith(end)]
        if suffix_list:
            suffix = max(suffix_list, key=len)
            self.word = self.word.replace(suffix, '')
        
    def step1a(self):
        step_suffixes = ['sses', 'ied', 'ies', 'us', 'ss', 's']
        suffix_list = [end for end in step_suffixes if self.word.endswith(end)]
        if suffix_list:
            suffix = max(suffix_list, key=len)
            if suffix == 'sses':
                self.word = self.word.replace(suffix, 'ss')
            elif suffix in ['ied', 'ies']:
                self.word = self.word.replace(suffix, 'ies')
            elif suffix in ['us', 'ss']:
                pass
            elif suffix == 's':
                if any(x in self.word[:-2] for x in VOWELS):
                    self.word = self.word.replace(suffix, '')

    def step1b(self):
        step_suffixes = ['eedly', 'eed', 'ingly', 'ing', 'edly', 'ed']
        suffix_list = [end for end in step_suffixes if self.word.endswith(end)]
        if suffix_list:
            suffix = max(suffix_list, key=len)
            if suffix in ['eed', 'eedly'] and suffix in self.word[self.r1:]:
                self.word = self.word.replace(suffix, 'ee')
            if (suffix in ['ingly', 'ing', 'edly', 'ed'] 
            and any(x in self.word[:-len(suffix)] for x in VOWELS)):
                self.word = self.word.replace(suffix, '')
                if any(self.word.endswith(x) for x in ['at', 'bl', 'iz']):
                    self.word = self.word[:-2] + 'e'
                if any(self.word.endswith(x) for x in DOUBLES):
                    self.word = self.word[:-1]
                if self._short_finder():
                    self.word = self.word + 'e'

    def step1c(self):
        step_suffixes = ['y', 'Y']
        suffix_list = [end for end in step_suffixes if self.word.endswith(end)]
        if suffix_list:
            suffix = max(suffix_list, key=len)
            if self.word[-2] not in VOWELS and not self.word.startswith(self.word[-2]):
                self.word = self.word.replace(suffix, 'i')

    def step2(self):
        step_suffixes = ['tional', 'enci', 'anci', 'entli', 'izer', 'ization',
                         'ational', 'ation', 'ator', 'alism', 'aliti', 'alli',
                         'fulness', 'ousli', 'ousness', 'iveness', 'iviti',
                         'biliti', 'bli', 'logi', 'fulli', 'lessli', 'li']
        suffix_list = [end for end in step_suffixes if self.word.endswith(end)
                       and end in self.word[self.r1:]]
        if suffix_list:
            suffix = max(suffix_list, key=len)
            if suffix == 'tional':
                self.word = self.word.replace(suffix, 'tion')
            if suffix == 'enci':
                self.word = self.word.replace(suffix, 'ence')
            if suffix == 'anci':
                self.word = self.word.replace(suffix, 'ance')
            if suffix == 'abli':
                self.word = self.word.replace(suffix, 'able')
            if suffix in ['izer', 'ization']:
                self.word = self.word.replace(suffix, 'ize')
            if suffix in ['ational', 'ation', 'ator']:
                self.word = self.word.replace(suffix, 'ate')
            if suffix in ['alism', 'aliti', 'alli']:
                self.word = self.word.replace(suffix, 'al')
            if suffix == 'fulness':
                self.word = self.word.replace(suffix, 'ful')
            if suffix in ['ousli', 'ousness']:
                self.word = self.word.replace(suffix, 'ous')
            if suffix in ['iveness', 'iviti']:
                self.word = self.word.replace(suffix, 'ive')
            if suffix in ['biliti', 'bli']:
                self.word = self.word.replace(suffix, 'ble')
            if suffix == 'logi':
                self.word = self.word.replace(suffix, 'log')
            if suffix == 'fulli':
                self.word = self.word.replace(suffix, 'ful')
            if suffix == 'lessli':
                self.word = self.word.replace(suffix, 'less')
            if suffix == 'li' and self.word[-3] in LI_ENDING:
                self.word = self.word.replace(suffix, '')

    def step3(self):
        step_suffixes = ['tional', 'ational', 'alize', 'icate', 'iciti', 
                         'ical', 'ful', 'ness', 'ative']
        suffix_list = [end for end in step_suffixes if self.word.endswith(end)
                       and end in self.word[self.r1:]]
        if suffix_list:
            suffix = max(suffix_list, key=len)
            if suffix == 'tional':
                self.word = self.word.replace(suffix, 'tion')
            if suffix == 'ational':
                self.word = self.word.replace(suffix, 'ate')
            if suffix == 'alize':
                self.word = self.word.replace(suffix, 'al')
            if suffix in ['icate', 'iciti', 'ical']:
                self.word = self.word.replace(suffix, 'ic')
            if suffix in ['ful', 'ness']:
                self.word = self.word.replace(suffix, '')
            if suffix == 'ative' and suffix in word[self.r2:]:
                self.word = self.word.replace(suffix, '')

    def step4(self):
        step_suffixes = ['al', 'ance', 'ence', 'er', 'ic', 'able', 'ible',
                         'ant', 'ement', 'ment', 'ent', 'ism', 'ate', 'iti',
                         'ous', 'ive', 'ize', 'ion']
        suffix_list = [end for end in step_suffixes if self.word.endswith(end)
                       and end in self.word[self.r2:]]
        if suffix_list:
            suffix = max(suffix_list, key=len)
            step_suffixes.remove('ion')
            if suffix in step_suffixes:
                self.word = self.word.replace(suffix, '')
            if suffix == 'ion' and self.word[-4] in ['s', 't']:
                self.word = self.word.replace(suffix, '')

    def step5(self):
        if self.word.endswith('e') and 'e' in self.word[self.r1:]:
            if (self.word[-3] not in VOWELS 
            and self.word[-2] in VOWELS 
            and self.word[-1] not in VOWELS or ['w', 'x' 'Y']):
                self.word = self.word.replace('e', '')
        elif self.word.endswith('l') and 'l' in self.word[self.r2:] and self.word[-2] == 'l':
            self.word = self.word.replace('l', '')
        self.word = self.word.lower()

    def _short_finder(self):
        if (self.word[self.r1:] == ''
        and self.word[-3] not in VOWELS 
        and self.word[-2] in VOWELS 
        and self.word[-1] not in VOWELS or ['w', 'x' 'Y']):
            return True
        else:
            return False
