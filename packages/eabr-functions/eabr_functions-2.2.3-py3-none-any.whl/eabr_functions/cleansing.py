from unicodedata import normalize


class EabrCleansing(object):
    class Normalize:
        def __init__(self, string):
            self.string = string

        def execute(self):
            try:
                rem = normalize('NFKD', self.string) \
                    .encode('ASCII', 'ignore') \
                    .decode('ASCII')
                return rem
            except:
                pass

    class Prepositions:
        def __init__(self, string, prepositions):
            self.string = string
            self.prepositions = prepositions

        def execute(self):
            try:
                ajust_name = (' '.join(word if word in self.prepositions else word.title()
                                       for word in self.string.capitalize().split(' ')))
                return ajust_name
            except:
                pass
