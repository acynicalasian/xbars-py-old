#---------------------------------------------------------------------
# xbars.py 
#
# This program aims to return all valid parse trees for any given
# grammatically correct English word, phrase, or input. These parse
# trees are based off of X-bar theory. Online dictionary APIs are
# used so that the program is more robust, avoiding the need for a
# hard-coded list of valid words with associated parts of speech.
#
# Known issues:
# > This program struggles to parse sentences that feature
#   discontinuity, although wh-movement is planned to be implemented.
# > Expletives and interjections are not supported and will be removed
#   during analysis.
# > Admittedly, many dependent clauses are a struggle for me to
#   implement, other than those of form (CP -> C TP) (and even those
#   might be a struggle if C is null! i.e. I heard <that> John died.)
#---------------------------------------------------------------------

#
# Implementation of Node datatype to allow for tree data structure
# construction. Parts of speech, phrases, and words are all
# represented via the Node datatype.
#
class Node:
    def __init__(self, list_children = None):
        if type(self) == Node:
            # Prevent base class instantiation
            raise NotImplementedError("Base class is intended to be "
                                      "abstract")
        self._children = None
        if type(self) == VP:
            self._maxchildren = 3
        else:
            self._maxchildren = 2
        if not list_children is None:
            self.setChildren(list_children)
    def __str__(self):
        raise NotImplementedError("This method is intended to be pure"
                                  "virtual")
    def setChildren(self, list_children):
        if (isinstance(list_children, list) or
            isinstance(list_children, tuple)):
            lenlist = len(list_children)
            if lenlist <= self._maxchildren:
                for n in range(lenlist):
                    if not isinstance(list_children[n], Node):
                        raise TypeError("Elements of positional "
                                        "argument 'list_children' "
                                        "must be of type 'Node'; "
                                        "check list_children[" + n +
                                        "]")
                if isinstance(list_children, list):
                    self._children = list_children
                else:
                    self._children = list(list_children)
            else:
                raise TypeError("Positional argument 'list_children' "
                                "must contain at most "
                                + self._maxchildren + " elements. "
                                "Current size of 'list_children' is "
                                + lenlist)
        else:
            raise TypeError("Positional argument 'list_children' is "
                            "required to be of type 'list' or "
                            "'tuple'")
class Word(Node):
    def __init__(self, word):
        if isinstance(word, str):
            self._word = word
        else:
            raise TypeError("Positional argument 'word' is required "
                            "to be of type 'str'")
    def __str__(self):
        return self._word
    def setChildren(self, list_children):
        raise NotImplementedError("Words cannot have children")
class NullWord(Word):
    def __init__(self):
        Word.__init__(self, '\u2205')
    def setChildren(self, list_children):
        raise NotImplementedError("Null constituents cannot have "
                                  "children")
class Trace(Word):
    def __init__(self):
        Word.__init__(self, 't')
    def setChildren(self, list_children):
        raise NotImplementedError("Traces cannot have children")
class POS(Node):
    def __init__(self, list_children = None):
        if type(self) == POS:
            # Prevent base class instantiation
            raise NotImplementedError("Base class is intended to be "
                                      "abstract")
        # Allow for (T -> V T)
        if type(self) == T:
            pass
        else:
            self._maxchildren = 1
        self._children = None
        if not list_children is None:
            self.setChildren(list_children)
    def __str__(self):
        return self.__class__.__name__
class FeaturePOS(POS):
    def __init__(self, list_children = None, features = None):
        if type(self) == FeaturePOS:
            # Prevent base class instantiation
            raise NotImplementedError("Base class is intended to be "
                                      "abstract")
        POS.__init__(self, list_children)
        self._features = None
        if type(self) == C:
            self._validfeatures = ("[+Q]", "[+Q][+wh]", "[+wh]",
                                   "[+TOP]", None)
            self._pos_longtext = "complementizer"
        elif type(self) == D:
            self._validfeatures = ("[+wh]", None)
            self._pos_longtext = "determiner"
        elif type(self) == T:
            self._validfeatures = ("[-pres]", "[+pres]")
            self._pos_longtext = "tense word"
        else:
            raise TypeError("Only complementizers, determiners, and "
                            "tense words should have features")
        self.setFeatures(features)
    def __str__(self):
        return self.__class__.__name__
    def setFeatures(self, features):
        if features in self._validfeatures:
            self._features = features
        else:
            raise TypeError("Invalid feature string for " +
                            self._pos_longtext + ": " + features)
class A(POS):
    pass
class Adv(POS):
    pass
class C(FeaturePOS):
    pass
class D(FeaturePOS):
    pass
class N(POS):
    pass
class Neg(POS):
    pass
class P(POS):
    pass
class T(FeaturePOS):
    pass
class V(Word):
    pass
#
# Implementation of phrase structure rules
#
class AP(Node):
    pass
class ABar(Node):
    def __str__(self):
        return "A'"
class AdvP(Node):
    pass
class CP(Node):
    pass
class CBar(Node):
    def __str__(self):
        return "C'"
class DP(Node):
    pass
class DBar(Node):
    def __str__(self):
        return "D'"
class NP(Node):
    pass
class NBar(Node):
    def __str__(self):
        return "N'"
class NegP(Node):
    pass
class PP(Node):
    pass
class PBar(Node):
    def __str__(self):
        return "P'"
class TP(Node):
    pass
class TBar(Node):
    def __str__(self):
        return "T'"
class VP(Node):
    pass
class VBar(Node):
    def __str__(self):
        return "V'"
class PSRLookup:
    # This nested tuple doesn't have much reason to change, hence
    # hardcoded constants for indices based on the left-hand side
    # of a PSR; the data in the table is the right-hand side
    # Each right-hand side is represented by a tuple
    _AP = 0
    _ABar = 1
    _AdvP = 2
    _CP = 3
    _CBar = 4
    _DP = 5
    _DBar = 6
    _NP = 7
    _NBar = 8
    _NegP = 9
    _PP = 10
    _PBar = 11
    _T = 12
    _TP = 13
    _TBar = 14
    _VP = 15
    _VBar = 16
    _Null = 17
    _Trace = 18
    _A = 19
    _C = 20
    _D = 21
    _N = 22
    _Neg = 23
    _P = 24
    _V = 25
    _Word = 26
    _lookup = (
        (
            # CP ->
            (_DP, _CBar), (_CBar), (_PP, _CBar), (_AdvP, _CBar)
        ),
        (
            # C' ->
            (_C, _TP)
        ),
        (
            # DP ->
            (_DP, _DBar), (_DBar)
        ),
        (
            # D' ->
            (_D, _NP)
        ),
        (
            # T ->
            (_T, _VP), (_V, _T), (_T, _V), (_Word)
        ),
        (
            # TP ->
            (_DP, _TBar), (_CP, _TBar), (_TP, 
        ),
        (
            # T' ->
            (_T, _VP)
        ),
        (
            # VP ->
            (_CP, _VBar), (_TP, _VBar), (_V, _VP)
        ),
        (
            # V' ->
            (_V, _DP), (_V, _CP), (_V, _PP), (_V, _TP)
        ),
        
