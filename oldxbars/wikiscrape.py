import re
import urllib.request
import urllib.parse
import json
from html.parser import HTMLParser

class missingtitle(Exception):
    pass
class _Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._buffer = ""
        self._checkspans = False
        self._isparsed = False
        self._searchflag = False
        self._featuresearch = False
        self._copyflag = False
        self._quoteflag = False
        self._POS = [ "Adjective", "Adverb", "Conjunction",
                      "Determiner", "Pronoun", "Proper noun", "Noun",
                      "Preposition", "Auxiliary", "Verb" ]
        self.POS = []
    def handle_starttag(self, tag, attrs):
        # Implementation relies on consistent formatting of Wiktionary
        # content to parse the data and organize it
        if self._isparsed:
            return
        elif tag == "h2":
            # h2 tag corresponds to a section dedicated to some lang
            # Language is held in span tags after this
            self._checkspans = True
        elif tag == "hr" and self._searchflag:
            # hr corresponds to the end of a language's section
            # if we were checking English, searchflag should be true
            self._isparsed = True
        elif tag == "span" and self._checkspans:
            if attrs == []:
                return
            # span tag could either show the lang or part of speech
            if attrs[0] == ("class", "mw-headline"):
                if attrs[1][1] == "English":
                    self._searchflag = True
                elif self._searchflag:
                    for a in self._POS:
                        if attrs[1][1] == a:
                            self.POS.append(a)
                        if (attrs[1][1] == "Auxiliary" or
                            attrs[1][1] == "Verb"):                            
                            # We only care about the details of verbs and
                            # auxiliaries because T may be bound
                            self._featuresearch = True
        elif tag == "ol" and self._featuresearch:
            # w/in a language section, ol tags indicate lists,
            # typically definitions; we'll copy these definitions
            # to try to search them for terms related to tense
            self._copyflag = True
        elif tag == "ul":
            print("testing: attr is: ", attrs)
            if attrs == []:
                return
            elif (attrs[0] == ("style", "display: block;") or
                  attrs[0] == ("style", "display: none;") or
                  attrs == ("style", "display: block;") or
                  attrs == ("style", "display: none;")):
                self._quoteflag = True
                print("set it")
        else:
            pass
    def handle_endtag(self, tag):
        if tag == "ol" and self._copyflag:
            self._copyflag = False
            self._buffer += '\n'
        if tag == "ul" and self._quoteflag:
            self._quoteflag = False
    def handle_data(self, data):
        if self._quoteflag:
            print("oh fuck")
            return
        if self._copyflag and not self._quoteflag:
            self._buffer += data
class Scraper:
    def __init__(self):
        self._URL = "https://en.wiktionary.org/w/api.php?"
        self._param = {
            "action" : "parse",
            "page" : None,
            "prop" : "text",
            "format" : "json"
            }
        self.URL = None
        self._data = None
    def search(self, word):
        # Returns (parts_of_speech, features)
        self._param["page"] = word
        self._apiargs = urllib.parse.urlencode(self._param)
        self.URL = self._URL + self._apiargs
        self._data = json.load(urllib.request.urlopen(self.URL))
        if "error" in self._data:
            raise missingtitle(self._data["error"]["info"])
        self._html = self._data["parse"]["text"]["*"]
        # TO-DO: Use _Parser class
        parser = _Parser()
        parser.feed(self._html)
        print(parser.POS)
        #print(parser._buffer)
def test():
    class _testParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            print("Start tag: ", tag)
            if tag == "ul":
                print("found ul")
            for attr in attrs:
                if attr == ("style", "display: none;"):
                    print("found style")
                    self._quoteflag = True
                print("\tattr: ", attr)
        def handle_data(self, data):
            if self._quoteflag:
                print("oh fuck")
            else:
                print("error")
    import io
    from contextlib import redirect_stdout
    p = _Parser()
    p._copyflag = True
    p._quoteflag = False
    p.feed('<ul style="display: none;">stupid</ul>')
    print(p._quoteflag)
    print(p._buffer)
    return
    f = open("testoutput", 'r+')
    s = Scraper()
    with io.StringIO() as buf, redirect_stdout(buf):
       s.search("test")
       output = buf.getvalue()
       f.write(output)
    s.search("test")
