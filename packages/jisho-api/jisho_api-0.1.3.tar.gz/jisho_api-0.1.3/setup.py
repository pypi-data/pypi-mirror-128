# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jisho_api', 'jisho_api.kanji', 'jisho_api.sentence', 'jisho_api.word']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click>=8.0.1,<9.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.11.0,<11.0.0']

entry_points = \
{'console_scripts': ['jisho = jisho_api.cli:make_cli']}

setup_kwargs = {
    'name': 'jisho-api',
    'version': '0.1.3',
    'description': 'A jisho.org API and scraper in Python.',
    'long_description': '# jisho-api\n\n[![GitHub tag](https://img.shields.io/github/tag/pedroallenrevez/jisho-api)](https://github.com/pedroallenrevez/jisho-api/releases/?include_prereleases&sort=semver "View GitHub releases")\n\n\n\nA Python API built around scraping [jisho.org](https://jisho.org), an online Japanese dictionary.\n\n```bash\npip install jisho_api\n```\n\n[![asciicast](https://asciinema.org/a/NJuZQnNfe0JDdDELn08NhmYuY.svg)](https://asciinema.org/a/NJuZQnNfe0JDdDELn08NhmYuY)\n\n## Requests\n\nYou can request three types of information:\n- Words\n- Kanji\n- Sentences\n\nThe search terms are directly injected into jisho\'s search engine, which means all of \nthe filters used to curate a search should work as well. For instance, `"水"` would look \nprecisely for a word with just that character.\n\nCheck https://jisho.org/docs on how to use the search filters.\n\n```bash\njisho search word water\njisho search word 水\njisho search word "#jlpt-n4"\n```\n\nThe request replies are [Pydantic](https://pydantic-docs.helpmanual.io/) objects.\nYou can check the structure of a word request in `jisho/word/cfg.py`, and likewise for both kanji and sentences.\n\nYou could also do so programatically, by doing:\n```python\nfrom jisho.word import Word\nr = Word.request(\'water\')\n```\n\n> **Note**: Almost everything that is available in a page is being scraped.\n> **Note**: Kanji requests can come with incomplete information, because it is not available in the page.\n\n## Scrapers\n\nYou can scrape the website for a list of given search terms.\nSupply them with a `.txt` file with the words separated by newlines.\n\n```bash\njisho scrape word words.txt\njisho scrape kanji kanji.txt\njisho scrape sentence search_words.txt\n```\nAll of the resulting searches will be stored in `~/.jisho/data`.\n\nIn case you want to scrape programatically you can:\n```python\nfrom jisho.cli import scrape\nfrom jisho.word import Word\n\nword_requests = scrape(Word, [\'water\', \'fire\'], \'/to/path\')\n```\nThis will return a dictionary, which key values are the search term and request result.\nFailing requests are not included.\n\n## Cache and config\n\nIf you want cache enabled just run \n```bash\njisho config\n```\n\nThis will create a `~/.jisho/` folder with a `config.json` with your settings.\nAll your searches will be cached, and accessed if you search for the exact same term again.\n\n## Notes and considerations\nAccording to this [thread](https://jisho.org/forum/54fefc1f6e73340b1f160000-is-there-any-kind-of-search-api),\nthere is no official API, although there is a kind of [API request](https://jisho.org/api/v1/search/words?keyword=house) made by jisho.org, which is used to scrape words. This does not work for Kanji tho,\nbecause it would search the Kanji as a word, and not have any relevant metadata for the character itself.\n\nPermissions to scrape also granted in the aforementioned thread.\n\nAs stated in their [about page](https://jisho.org/docs) as well, jisho.org uses a collection of well-known [electronic dictionaries](http://www.edrdg.org/):\n> This site uses the JMdict, Kanjidic2, JMnedict and Radkfile dictionary files. -jisho.org\n\n## Credits and Acknowledgements for data\n\nAll credit is given where it\'s due, and the several extracted resources is given at jisho.org\'s [about page](https://jisho.org/docs).',
    'author': 'pedro',
    'author_email': 'pedroallenrevez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pedroallenrevez/jisho-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
