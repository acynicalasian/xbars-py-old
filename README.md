# xbars-py
Currently scrapes Wiktionary to return dictionary entries, and stores data regarding parts of speech and verb inflections. The goal is to ultimately use this data to produce an automatic syntax tree generator.

Currently, there is one main module:
* dictsearch.py

## Requirements
This project was tested and developed on Python 3.10.2. The following libraries must be installed:
* [Beautiful Soup 4](https://beautiful-soup-4.readthedocs.io/en/latest/) - used by the scraper in `dictsearch.py`

Unfortunately, I can't make any promises regarding which versions of Python 3.x this project targets.

## Modules
### dictsearch.py - a basic Wiktionary scraper
Aims to provide an extremely basic interface to scrape English language dictionary entries from Wiktionary.

The class constructor automatically does the scraping in the background, so the interface consists solely of the constructor and a few instance variables. As such, you'll want to make a new instance of the class when you want to search a new word, instead of modifying the instance variables.

#### Interface
##### `DictSearch(word)`
Searches for `word` on Wiktionary, scrapes the data if an English entry exists, and stores a dictionary entry and part of speech and verb inflection data.
* If a page for `word` does not exist on Wiktionary, a `PageNotFound` exception is raised.
* If a page for `word` exists, but an English entry for it does not exist, a `NoEnglishEntry` exception is raised.
##### `DictSearch.POSList`
* `set` class attribute that holds the parts of speech recognized by the program. Any code implementing this library should ideally aim to conform to the list of parts of speech given in this class attribute.
##### `.word`
* `str` instance variable that holds the `word` used to initialize this instance.
##### `.entry`
* `str` instance variable that holds the dictionary entry on Wiktionary for the word.
##### `.POS`
* `set` instance variable that holds the parts of speech associated with `word` in English.
##### `.verbInflections`
* `set` instance variable that holds any verb inflections associated with `word` in English.