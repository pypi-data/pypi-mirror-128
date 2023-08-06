from unicodedata import normalize


class EabrCleansing(object):
    def __init__(self, name):
        self.name = name

    def normalize_name(self):
        try:
            rem = normalize('NFKD', self.name) \
                .encode('ASCII', 'ignore') \
                .decode('ASCII')
            return rem
        except:
            pass

    def ajust_name(self):
        prep_br = ['de', 'do', 'da', 'dos', 'das']

        try:
            ajust_name = (' '.join(word if word in prep_br else word.title()
                                   for word in self.name.capitalize().split(' ')))
            return ajust_name
        except:
            pass
