import urllib.request
import urllib.parse
import json
import copy
import re
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
        self.entry = "" # hold dictionary entry
        self.html = None # hold HTML data of body of page        
        self.POS = [] # hold parts of speech of word
        # Should stay None unless self.POS contains "Verb"
        self.verbInflections = None

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
        # something), and empty <li> tags (for later in extracting
        # definitions)
        for classid in ["nyms-toggle", "HQToggle", "mw-editsection",
                        "reference", "NavFrame", "mw-empty-elt"]:
            for tag in soup.find_all(class_=classid):
                tag.decompose()

        # Remove <dl> tags (example usages) and <ul> tags (show up
        # when clicking the [quotations] button)
        for tagid in ["dl", "ul"]:
            for tag in soup.find_all(tagid):
                tag.decompose()

        # Section headers for etymology and part of speech all occur
        # in tags with class "mw-headline"
        treeptr = treeptr.find_next(class_="mw-headline")
        etym_regex = re.compile("Etymology")
        entry = ""
        # First condition exits if treeptr is None, second exits if we
        # enter a section for a different language, which always
        # occurs in "h2" tags
        while treeptr and treeptr.parent.name != "h2":
            # treeptr jumped to a <span> tag with class "mw-headline"
            # that delineates a section for etymology
            if etym_regex.match(treeptr.string):
                entry += treeptr.string + "\n\n"
                # <p> tags contain the etymology deets
                treeptr = treeptr.find_next("p")
                entry += treeptr.get_text() + '\n'
            # treeptr jumped to a tag that delineates part of speech
            elif treeptr.string in self._POS:
                entry += treeptr.string + '\n'
                # Handle verbs seperately, comb definitions for
                # mentions of being auxiliaries
                verbFlag = False
                if treeptr.string == "Verb":
                    verbFlag = True
                    aux_regex = re.compile("auxiliary")
                    modal_regex = re.compile("modal")
                    # Verbs only inflect for past or present in
                    # English as far as I'm aware
                    past_regex = re.compile("simple past")
                    perf_regex = re.compile("past participle")
                    # Assume verbs are present tense by default, and
                    # use "simple present" as the regex to search
                    # against because "present" will fail for any
                    # dictionary entries for the verb "present";
                    # "simple present" better catches verb inflection
                    # for 3P-present, and I'm not aware of any
                    # irregular forms for this
                    pres_regex = re.compile("simple present")
                # Extract the gloss
                treeptr = treeptr.find_next("p")
                entry += treeptr.get_text() + '\n'
                # Extract the section containing definitions
                olptr = treeptr.find_next("ol").extract()
                olptr = olptr.li
                liCount = 1
                nestedCount = 1
                innerptr = None
                # TO-DO: support searching verb definitions to extract
                # tense/modality data
                while olptr:
                    # if nested definitions
                    if olptr.ol:
                        innerptr = olptr.ol.extract()
                    entry += str(liCount) + '. ' + olptr.get_text()
                    if innerptr:
                        innerptr = innerptr.li
                        while innerptr:
                            entry += ('\t' + str(nestedCount) + '. '
                                      + innerptr.get_text())
                            nestedCount += 1
                            innerptr = innerptr.find_next("li")
                        entry += '\n'
                        nestedCount = 1
                        innerptr = None
                    liCount += 1
                    olptr = olptr.find_next("li")
                entry += '\n'
            # tag with class "mw-headline" that doesn't correspond
            # with etymology or definitions
            else:
                pass
            treeptr = treeptr.find_next(class_="mw-headline")
        self.entry = entry
def test():
    test = DictSearch("would")
    import io
    from contextlib import redirect_stdout
    f = open("test", 'r+')
    with io.StringIO() as buf, redirect_stdout(buf):
        print(test.entry)
        output = buf.getvalue()
        f.write(output)
