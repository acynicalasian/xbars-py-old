#--------------------------------------------------------------------#
#                                                                    #
# wordtype.py                                                        #
#                                                                    #
# Define parts of speech possible for a word.                        #
#                                                                    #
#--------------------------------------------------------------------#

# >>> Word datatypes (parts of speech for single words)

class Word:
    _s = None
    
    def __init__(self, s):
        self._s = s

    def getWord(self):
        return self._s

    def getType(self):
        return self.__class__.__name__

class FeatureWord(Word):
    _f = None

    def __init__(self, s, f = None):
        self._s = s
        self._f = f
    
    def getFeatures(self):
        return self._f

    def setFeatures(self, f):
        raise NotImplementedError()

    class InvalidFeature(Exception):
        pass

class A(Word):
    pass

class Adv(Word):
    pass

class C(FeatureWord):
    def setFeatures(self, f):
        try:
            if f in ["[+Q]", "[+Q][+wh]", "[+wh]", "[+TOP]", None]:
                self._f = f
        except:
            raise self.InvalidFeature("Invalid feature string for "
                                      "complementizer: " + f)
        
class D(FeatureWord):
    def setFeatures(self, f):
        try:
            if f in ["[+wh]", None]:
                self._f = f
        except:
            raise self.InvalidFeature("Invalid feature string for"
                                      "determiner: " + f)

class N(Word):
    pass

class Neg(Word):
    pass

class P(Word):
    pass

class T(FeatureWord):
    def setFeatures(self, f):
        try:
            if f in ["[-tense]", "[+pres]", "[-pres", "[+future]", None]:
                self._f = f
        except:
            raise self.InvalidFeature("Invalid feature string for "
                                      "tense word: " + f)

class V(Word):
    pass

# Special wordtypes for cases of null words and traces
class Null(Word):
    def __init__(self):
        self._s = '\u2205'

class Trace(Word):
    def __init__(self):
        self._s = 't'
        
# >>> Phrase datatypes (phrase structure rules)
class Phrase(Word):
    _c1 = None
    _c2 = None
    _c3 = None
    
    def __init__(self, c1, c2 = None, c3 = None):
        pass

class AP(Phrase):
    def __init__(self, c1, c2 = None, c3 = None):
