import urllib.request
import urllib.parse
import json
import copy
from html.parser import HTMLParser
from bs4 import BeautifulSoup

class DictSearch:
    """Given a search term, fetch JSON output from the MediaWiki API
    to determine whether a page exists for the search term. If so,
    copy the HTML data of the page for that term, and parse it to
    extract parts of speech, definitions, etc."""
    
    def __init__(self, word):
        # "Public" data members
        self.word = word
        self.entry = {
            "Adjective" : None,
            "Adverb" : None,
            "Article" : None,
            "Conjunction" : None,
            "Determiner" : None,
            "Pronoun" : None,
            "Proper noun" : None,
            "Noun" : None,
            "Preposition" : None,
            "Verb" : None
            }
        self.html = None # hold HTML data of body of page        
        self.POS = None # hold parts of speech of word

        # "Private" data members
        self._POS = [ "Adjective", "Adverb", "Article", "Conjunction",
                      "Determiner", "Pronoun", "Proper noun", "Noun",
                      "Preposition", "Auxiliary", "Verb" ]
        self._soup = None # keep the BeautifulSoup object "hidden"

        if not isinstance(word, str):
            raise TypeError("Search term must be of type str")
        self._copypage(word) # instantiate self.html

        # Only runs if page exists
        self._soup = BeautifulSoup(self.html, "html.parser")
        self._parsepage()
        
    def _copypage(self, word):
        URL = "https://en.wiktionary.org/w/api.php?"
        param = {
            "action" : "parse",
            "page" : word,
            "prop" : "text",
            "format" : "json"
            }
        URL += urllib.parse.urlencode(param)
        raw = json.load(urllib.request.urlopen(URL))
        # If page does not exist
        if "error" in raw:
            raise LookupError("The page you specified ('" + word +
                              "') doesn't exist")
        self.html = raw["parse"]["text"]["*"]

    def _parsepage(self):
        soup = self._soup
        treeptr = soup.find(id="English")
        if not treeptr:
            raise LookupError("English entry does not exist for '" +
                              word + "'")
        
        # Strip the HTML of the [quotations] and [synonyms] toggle
        # boxes, [edit] buttons, reference links, NavFrames (tables or
        # something)
        
        for classid in ["nyms-toggle", "HQToggle", "mw-editsection",
                        "reference", "NavFrame"]:
            for tag in soup.find_all(class_=classid):
                tag.decompose()

        # Remove <dl> tags (example usages) and <ul> tags (show up
        # when clicking the [quotations] button)
        for tagid in ["dl", "ul"]:
            for tag in soup.find_all(tagid):
                tag.decompose()

        # Parts of speech occur in tags with class "mw-headline"
        treeptr = treeptr.find_next(class_="mw-headline")
        while treeptr and treeptr.parent.name != "h2":
            if treeptr.string in self._POS:
                currentPOS = treeptr.string
                # <p> tags contain the gloss, which has useful
                # information; extract this
                glossptr = treeptr.find_next("p").extract()
                gloss = ""
                while glossptr:
                    if isinstance(glossptr, str):
                        gloss += glossptr
                    glossptr = glossptr.next
                # <ol> tags contain the definitions
                olptr = treeptr.find_next("ol").extract()
                entry = ""
                # liCount = 1
                # olptr = olptr.next
                # while olptr:
                #     if isinstance(olptr, str):
                #         entry += olptr
                #     else:
                #         if olptr.name == "li":
                #             entry += str(liCount)
                #             liCount += 1
                #         elif olptr.name == "ol":
                #             # Handle nested definitions
                #             olptr_cp = copy.copy(olptr)
                #             olptr = olptr.parent.next_sibling
                #             nestedCount = 1
                #             while olptr_cp:
                #                 if isinstance(olptr_cp, str):
                #                     entry += olptr_cp
                #                 else:
                #                     if olptr.name == "li":
                #                         entry += '\t' + str(nestedCount)
                #             nestedCount = 1
                entry = olptr.get_text()
                # After processing the <ol> tag, add the definitions
                # to self.entry
                self.entry[currentPOS] = entry
                treeptr = treeptr.find_next(class_="mw-headline")
            else:
                treeptr = treeptr.find_next(class_="mw-headline")
                
def test():
    test = DictSearch("sex")
    import io
    from contextlib import redirect_stdout
    f = open("testoutput", 'r+')
    with io.StringIO() as buf, redirect_stdout(buf):
        print(test.entry)
        output = buf.getvalue()
        f.write(output)
        
