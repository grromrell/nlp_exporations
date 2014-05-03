class LovinsStemmer(object):
    def __init__(self):
        self.word = word

    def stem(self):
        yield self.word

    def stemming(self):
        suffix_list = [end for end in SUFFIXES if self.word.endswith(end)]
        if suffix_list:
            suffix = max(suffix_list, key=len)
            if suffix in SUFFIXES[:203]:
                self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[203:232]:
                if len(self.word.replace(suffix, '')) >= 3:
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[232:238]:
                if len(self.word.replace(suffix, '')) >= 4:
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[238:239]:
                if len(self.word.replace(suffix, '')) >= 5:
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[239:253]:
                if self.word.replace(suffix, '')[-1] != 'e':
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[253:261]:
                if len(self.word.replace(suffix, '')) >= 3:
                    if self.word.replace(suffix, '')[-1] != 'e':
                        self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[261:263]:
                if len(self.word.replace(suffix, '')) >= 3:
                    if self.word.replace(suffix, '')[-1] == 'f':
                        self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[263:264]:
                if self.word.replace(suffix, '')[-1] in ['t', 'll']:
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[264:267]:
                if self.word.replace(suffix, '')[-1] not in ['o', 'e']:
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[267:268]:
                if self.word.replace(suffix, '')[-1] not in ['a', 'e']:
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[268:269]:
                if len(self.word.replace(suffix, '')) >= 3:


SUFFIXES = ['arizability', 'antialness', 'arisations', 'arizations',
            'entialness', 'antaneous', 'antiality', 'arisation', 'arization',
            'ativeness', 'entations', 'entiality', 'entialize', 
            'entiation', 'ionalness', 'istically', 'itousness', 'izability',
            'izational', 'ableness', 'arizable', 'entation', 'entially',
            'eousness', 'ibleness', 'icalness', 'ionalism', 'ionality',
            'ionalize', 'iousness', 'izations', 'lessness', 'ability',
            'aically', 'alities', 'aristic', 'arizing', 'ateness', 'atingly',
            'atively', 'ativism', 'encible', 'entally', 'entials', 'entiate',
            'entness', 'fulness', 'ibility', 'icalism', 'icalist', 'icality',
            'icalize', 'icianry', 'ination', 'ingness', 'ionally', 'isation',
            'ishness', 'istical', 'iteness', 'iveness', 'ivistic', 'ivities',
            'ization', 'izement', 'ivistic', 'oidally', 'ousness', 'aceous',
            'alness', 'ancial', 'ancies', 'ariser', 'arized', 'arizer',
            'atable', 'atives', 'efully', 'encies', 'encing', 'ential',
            'enting', 'entist', 'eously', 'ialist', 'iality', 'ialize', 
            'ically', 'icance', 'icians', 'icist', 'ifully', 'ionals', 
            'ionate', 'ioning', 'ionist', 'iously', 'istics', 'lessly', 
            'nessess', 'oidism', 'acies', 'acity', 'aical', 'alist', 'ality',
            'alize', 'arial', 'aries', 'arily', 'arize', 'aroid', 'ately', 
            'ative', 'ators', 'atory', 'ehood', 'eless', 'elity', 'ement', 
            'enced', 'ences', 'ental', 'ently', 'fully', 'ially', 'icant', 
            'ician', 'icide', 'icism', 'icist', 'icity', 'iedly', 'ihood', 
            'inate', 'iness', 'ional', 'ioned', 'ished', 'istic', 'ities', 
            'itous','ively', 'ivity', 'oidal', 'oides', 'otide', 'ously', 
            'able', 'ably', 'aric', 'ates', 'ator', 'eful', 'eity', 'ence', 
            'ency', 'eous', 'hood', 'ials', 'ians', 'ible', 'ibly', 'ical', 
            'iers', 'iful', 'ious', 'ists', 'less', 'lily', 'ness', 'ogen', 
            'ward', 'wise', 'yish', 'acy', 'aic', 'ata', 'ate', 'ese', 'ful', 
            'ial', 'ian', 'ics', 'ied', 'ier', 'ily', 'ist', 'ity', 'ium', 
            'ive', 'oid', 'ous', 'ae', 'ia', 'ic', 'is', "s'", "'s", 'a', 'e', 
            'i', 'o', 'alistically', 'ationally', 'alistic', 'ational', 
            'acious', 'ancing', 'ations', 'aging', 'anced', 'ances', 'arity', 
            'ation', 'ingly', 'ages', 'ally', 'ance', 'ancy', 'ants', 'aric', 
            'atic', 'ions', 'isms', 'ying', 'age', 'ant', 'ism', 'as', 'ly', 
            'y', 'allically', 'enting', 'antic', 'ented', 'ent', 'ish', 
            'ionate', 'eableness', 'elihood', 'ariness', 'izable', 'ature', 
            'eness', 'ening', 'edly', 'enly', 'ened', 'ene', 'ery', 'ed', 
            'es', 'ization', 'izers', 'izing', 'ized', 'izer', 'ary', 'ize', 
            'en', 'ication', 'action', 'itic', 'idine', 'ating', 'ated', 
            'inism', 'arly', 'ides', 'ide', 'ines', 'ine', 'ings', 'ing', 
            'ars', 'ies', 'ion', 'one', 'yl', 'on', 'or', 'um', 'us', 's', 
            'ar', 'early', 'ealy', 'eal', 'ear', 'eature', 'ite', 'allic', 
            'als', 'al', 'inity']
