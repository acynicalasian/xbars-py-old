# wordtype.py
#
# Define parts of speech possible for a word.

class Word:
    _s = None
    
    def __init__(self, s):
        self._s = s

    def getWord(self):
        return self._s

class FeatureWord(Word):
    _f = None

    def __init__(self, s, f):
        self._s = s
        self._f = f
    
    def getFeatures(self):
        return self._f

    def setFeatures(self, f):
        raise NotImplementedError()

class A(Word):
    pass

class A(Word):
    pass

class C(FeatureWord):
    def setFeatures(self, f):
        try:
            if f in ["[+Q]", "[+Q][+wh]", "[+wh]"]:
                self._f = f
            else:
                
                
    
