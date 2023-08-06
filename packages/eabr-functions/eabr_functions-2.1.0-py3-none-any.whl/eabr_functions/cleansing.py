from unicodedata import normalize


class EabrCleansing(object):
    def normalize_name(name):
        try:
            rem = normalize('NFKD', name) \
                .encode('ASCII', 'ignore') \
                .decode('ASCII')
            return rem
        except:
            pass

    def ajust_name(name):
        prep_br = ['de', 'do', 'da', 'dos', 'das']

        try:
            ajust_name = (' '.join(word if word in prep_br else word.title()
                                   for word in name.capitalize().split(' ')))
            return ajust_name
        except:
            pass
