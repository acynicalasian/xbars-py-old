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
# > Questions *need* to be marked with a question mark, or parsing
#   will fail.
#---------------------------------------------------------------------

#
# Implementation of Node datatype to allow for tree data structure
# construction. Parts of speech, phrases, and words are all
# represented via the Node datatype.
#
class Node:
    def __init__(self, label, *children):
        if not isinstance(label, str):
            raise TypeError("Nodes need to be initialized with some "
                            "sort of label of type str")
        self._label = label
        self._children = []
        if not children is None:
            self.setChildren(*children)
    def setChildren(self, *children):
        self._children.clear()
        for c in children:
            if isinstance(c, Node):
                self._children.append(c)
            else:
                raise TypeError("Node children must be of type Node")
        
    def __str__(self, level = 0, ws = "|   "):
        if level == 0:
            if len(self._children) > 0:
                output = self._label + '\n'
                for c in self._children:
                    if c == self._children[-1]:
                        ws = "    "
                    output += c.__str__(1, ws)
            else:
                output = self._label + '\n'
        elif level == 1:
            if len(self._children) > 0:
                output = u"|\u2014\u2014\u2014" + self._label + '\n'
                for c in self._children:
                    output += c.__str__(2, ws)
            else:
                output = u"|\u2014\u2014\u2014" + self._label + '\n'
        else:
            if len(self._children) > 0:
                output = (ws + (level - 2)*"    " +
                          u"|\u2014\u2014\u2014" + self._label + '\n')
                          
                for c in self._children:
                    output += c.__str__(level + 1, ws)
            else:
                output = (ws + (level - 2)*"    " +
                          u"|\u2014\u2014\u2014" + self._label + '\n')
        return output
class RuleList:
    def __init__(self):
        self._psr = None
        rules = [
            #
            # TP rules
            #
            ("TP", "DP", "T'"), ("TP", "CP", "T'"), ("T'", "T", "VP"),
            # > Skip T -> V T unless we find T bound to V;
            #
            # CP rules
            #
            ("CP", "C'"), ("C'", "C", "TP"),
            # > Skip T to C unless [+Q]; skip Spec,CP derivations
            # > unless [+Q];
            #
            # VP rules
            #
            ("VP", "t", "V'"), ("VP", "VP", "PP"), ("VP", "V", "VP"),
            ("VP", "AdvP", "VP"), ("VP", "VP", "AdvP"),
            ("VP", "NegP", "VP"), ("VP", "DP", "V'"),
            ("VP", "CP", "V'"), ("V'", "V"), ("V'", "V", "DP"),
            ("V'", "V", "PP"), ("V'", "V", "CP"), ("V'", "V", "TP"),
            ("V'", "V", "DP", "DP"), ("V'", "V", "DP", "PP"),
            # > Skip V' -> T XP rules unless we have bound T;
            #
            # DP rules
            #
            ("DP", "D'"), ("D'", "D", "NP"), ("DP", "DP", "D'"),
            #
            # NP rules
            #
            ("NP", "NP", "PP"), ("NP", "AP", "NP"), ("NP", "N'"),
            ("N'", "N"), ("N'", "N", "CP"), ("N'", "N", "PP"),
            #
            # AP rules
            #
            ("AP", "DP", "A'"), ("AP", "A'"), ("AP", "AdvP", "AP"),
            ("A'", "A"), ("A'", "A", "PP"), ("A'", "A", "CP"),
            ("AP", "t", "A'")
            #
            # PP rules
            #
            ("PP", "P'"), ("PP", "DP", "P'"), ("P'", "P", "DP"),
            ("P'", "P"),
            #
            # AdvP rules
            #
            ("AdvP", "Adv"),
            #
            # NegP rules
            #
            ("VP", "NegP", "VP"), ("NegP", "Neg")
        ]
