import urllib.request
import urllib.parse
import json
from html.parser import HTMLParser
from bs4 import BeautifulSoup

class _Scraper:
    """Given a search term, fetch JSON output from the MediaWiki API
    to determine whether the search term corresponds to an existing
    page. If so, pass the text segment of the JSON in the field
    "parse" : "text" : "*" to an HTML parser."""
    def __init__(self, word):
        self._URL = "https://en.wiktionary.org/w/api.php?"
        self._param = {
            "action" : "parse",
            "page" : None,
            "prop" : "text",
            "format" : "json"
            }
        self.URL = None      # Formatted URL using _param values
        self._data = None    # Hold raw JSON output
        self._html = None    # Hold the HTML data returned in a valid
                             # query in the "parse" : "text" : "*"
                             # field
        self.search(word)
    def search(self, word):
        # Craft formatted MediaWiki API query
        self._param["page"] = word
        self._apiargs = urllib.parse.urlencode(self._param)
        self.URL = self._URL + self._apiargs
        self._data = json.load(urllib.request.urlopen(self.URL))
        if "error" in self._data:
            raise LookupError(self._data["error"]["info"])
        self._html = self._data["parse"]["text"]["*"]

        # TO-DO (?): pass this data to a data parser

class Parser:
    """Initialize the parser with the data from a Scraper; parse the
    data for parts of speech, definitions, and other
    grammatical/lexical data. Relies on Wiktionary having relatively
    consistent formatting in its entries, so some words may fall
    through the cracks."""
    def __init__(self, word):
        _s = _Scraper(word)
        self.word = word
        self.html = _s._html
        self._POS = [ "Adjective", "Adverb", "Conjunction",
                      "Determiner", "Pronoun", "Proper noun", "Noun",
                      "Preposition", "Auxiliary", "Verb" ]
        self.POS = []
        self.soup = BeautifulSoup(self.html, "html.parser")

        self.parse()
        
        # WARNING: might be deprecated
        # Flags to be used by the Parser
        self._buffer = ""
        self._checkspans = False
        self._isparsed = False
        self._searchflag = False
        self._featuresearch = False
        self._copyflag = False
        self._quoteflag = False
    def parse(self):
        # Check if an English entry exists for the input
        if not self.soup.find_all(id="English"):
            raise LookupError("""English entry does not exist for the
            word """ + self.word)
        
def test():
    pass
    # s = Scraper()
    # s.search(u"대")
    # p = Parser(s._html)
    # p.parse()
