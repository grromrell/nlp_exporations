import re

class LovinsStemmer(object):
    def __init__(self):
        self.word = None

    def stem(self, word):
        self.word = word
        self.stem_rules()
        self.recode()
        yield self.word

    def stem_rules(self):
        suffix = ''
        suffix_list = [end for end in SUFFIXES if self.word.endswith(end)]
        if suffix_list:
            suffix = max(suffix_list, key=len)
        if len(self.word.replace(suffix, '')) >= 2 and suffix:
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
                    if self.word.replace(suffix, '')[-1] in ['l', 'i']:
                        if re.search(r'u*e', self.word.replace(suffix, ''))[-3]:
                            self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[269:271]:
                if self.word.replace(suffix, '')[-2] == 'os':
                    self.word = self.word.replace(suffix, '')
                elif self.word.replace(suffix, '')[-1] not in ['u', 'x', 's']:
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[271:273]:
                if self.word.replace(suffix, '')[-1] not in ['a', 'c', 'e', 'm']:
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[273:275]:
                if re.search(r's**', self.word.replace(suffix, '')[-3]):
                    if len(self.word.replace(suffix, '')) >= 4:
                        self.word = self.word.replace(suffix, '')
                elif len(self.word.replace(suffix, '')) >= 3:
                    self.word.replace(suffix, '')
            elif suffix in SUFFIXES[275:276]:
                if self.word.replace(suffix, '')[-1] in ['l', 'i']:
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[276:277]:
                if self.word.replace(suffix, '')[-1] != 'c':
                    self.word = word.replace(suffix, '')
            elif suffix in SUFFIXES[277:278]:
                if len(self.word.replace(suffix, '')) >= 3:
                    if self.word.replace(suffix, '')[-1] not in ['l', 'n']:
                        self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[278:280]:
                if self.word.replace(suffix, '')[-1] in ['n', 'r']:
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[280:281]:
                if self.word.replace(suffix, '')[-2] == 'tt':
                    pass
                elif self.word.replace(suffix, '')[-2] == 'dr':
                    self.word = self.word.replace(suffix, '')
                elif self.word.replace(suffix, '')[-1] == 't':
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[281:282]:
                if self.word.replace(suffix, '')[-1] in ['s', 't']:
                    if self.word.replace(suffix, '')[-2] == 'ot':
                        pass
                    else:
                        self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[282:283]:
                if self.word.replace(suffix, '')[-1] in ['l', 'm', 'n', 'r']:
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[283:284]:
                if self.word.replace(suffix, '')[-1] == 'c':
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[284:285]:
                if self.word.replace(suffix, '')[-1] not in ['s', 'u']:
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[285:286]:
                if self.word.replace(suffix, '')[-1] in ['l', 'i']:
                    self.word = self.word.replace(suffix, '')
                elif re.search(r'u*e', word.replace(suffix, '')[-3]):
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[286:290]:
                if self.word.replace(suffix, '')[-2] == 'in':
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[290:291]:
                if self.word.replace(suffix, '')[-1] != 'f':
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[291:292]:
                if self.word.replace(suffix, '')[-1] in ['d','f', 'l', 't']:
                    self.word = self.word.replace(suffix, '')
                elif self.word.replace(suffix, '')[-2] in ['ph', 'th', 'er', 
                                                           'or', 'es']:
                    self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[292:295]:
                if len(self.word.replace(suffix, '')) >= 3:
                    if self.word.replace(suffix, '')[-3] not in ['met']:
                        if self.word.replace(suffix, '')[-4] not in ['ryst']:
                            self.word = self.word.replace(suffix, '')
            elif suffix in SUFFIXES[295:296]:
                if self.word.replace(suffix, '')[-1] == 'l':
                    self.word = self.word.replace(suffix, '')

    def recode(self):
        if any(self.word.endswith(x) for x in ['bb', 'dd', 'gg', 'll', 'mm', 
                                               'nn', 'nn', 'pp', 'rr', 'ss',
                                               'tt',]):
            self.word = self.word[:-1]
        elif self.word.endswith('ul'):
            if self.word[-3] not in ['a', 'o', 'i']:
                self.word = self.word.replace('ul', 'l')
        elif self.word.endswith('end'):
            if self.word[-4] != 's':
                self.word = self.word.replace('end', 'ens')
        elif self.word.endswith('her'):
            if self.word[-4] not in ['p', 't']:
                self.word = self.word.replace('her', 'hes')
        elif self.word.endswith('ent'):
            if self.word[-4] != 'm':
                self.word = self.word.replace('ent', 's')
        elif self.word.endswith('et'):
            if self.word[-3] != 'n':
                self.word = self.word.replace('et', 'es')
        else:
            suffix = ''
            suffix_list = [end for end in RECODES if self.word.endswith(end)]
            if suffix_list:
                suffix = max(suffix_list, key=len)
            if suffix:
                if suffix == 'iev':
                    self.word = self.word.replace(suffix, 'ief')
                elif suffix == 'uct':
                    self.word = self.word.replace(suffix, 'uc')
                elif suffix == 'umpt':
                    self.word = self.word.replace(suffix, 'um')
                elif suffix == 'rpt':
                    self.word = self.word.replace(suffix, 'rb')
                elif suffix == 'urs':
                    self.word = self.word.replace(suffix, 'ur')
                elif suffix == 'istr':
                    self.word = self.word.replace(suffix, 'ister')
                elif suffix == 'metr':
                    self.word = self.word.replace(suffix, 'meter')
                elif suffix == 'olv':
                    self.word = self.word.replace(suffix, 'olut')
                elif suffix == 'bex':
                    self.word = self.word.replace(suffix, 'bic')
                elif suffix == 'dex':
                    self.word = self.word.replace(suffix, 'dic')
                elif suffix == 'pex':
                    self.word = self.word.replace(suffix, 'pic')
                elif suffix == 'tex':
                    self.word = self.word.replace(suffix, 'tic')
                elif suffix == 'ax':
                    self.word = self.word.replace(suffix, 'ac')
                elif suffix == 'ex':
                    self.word = self.word.replace(suffix, 'ec')
                elif suffix == 'ix':
                    self.word = self.word.replace(suffix, 'ic')
                elif suffix == 'lux':
                    self.word = self.word.replace(suffix, 'luc')
                elif suffix == 'uad':
                    self.word = self.word.replace(suffix, 'uas')
                elif suffix == 'vad':
                    self.word = self.word.replace(suffix, 'vas')
                elif suffix == 'cid':
                    self.word = self.word.replace(suffix, 'cis')
                elif suffix == 'lid':
                    self.word = self.word.replace(suffix, 'lis')
                elif suffix == 'erid':
                    self.word = self.word.replace(suffix, 'eris')
                elif suffix == 'pand':
                    self.word = self.word.replace(suffix, 'pans')
                elif suffix == 'ond':
                    self.word = self.word.replace(suffix, 'ons')
                elif suffix == 'lud':
                    self.word = self.word.replace(suffix, 'lus')
                elif suffix == 'rud':
                    self.word = self.word.replace(suffix, 'rus')
                elif suffix == 'mit':
                    self.word = self.word.replace(suffix, 'mis')
                elif suffix == 'ert':
                    self.word = self.word.replace(suffix, 'ers')
                elif suffix in ['yt', 'ys']:
                    self.word = self.word.replace(suffix, 'ys')

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

RECODES = ['iev', 'uct', 'umpt', 'rpt', 'urs', 'istr', 'metr', 'olv', 'bex', 
           'dex', 'pex', 'tex', 'ax', 'ex', 'ix', 'lux', 'uad', 'vad', 'cid',
           'lid', 'erid', 'pand', 'ond', 'lud', 'rud', 'mit', 'ert', 'yt', 
           'yz']
