# Fanficapi
## An unofficial API (more like story and author metadata scraper) for fanfiction.net and archiveofourown.org written in python

Fanficapi is simple and easy to use python package for scraping story and author metadata from fanfiction.net and archiveofourown.org.

## Features

- Get story metadata from FFN and AO3 from a story link
- Get author metadata from FFN and AO3 from author link
- Simple keyword search to get the story link from FFN or AO3

Note: This was just my November project that I made for learning html scraping using python, I know the code is sh*t and just wanted to save it as a private repo, but recently I noticed all my other scrapers stopped working because of FFN's cloudflare protection. This one's working because it's based on undetected-chromedriver. So, if you feel it might be useful to you, here it is!

## Installation

Installation using pip:

`pip install fanficapi` or `pip3 install fanficapi`

Manual installation by cloning the github repository:
```
git clone https://github.com/lonely-code-cube/fanficapi
cd fanficapi
python3 setup.py install
```

Note: The github repository usually has latest updates and features, so it might contain more bugs

## Usage

For getting ao3 story metadata:
```py
import fanficapi

ao3 = fanficapi.AO3()
print (ao3.getStoryMeta("https://archiveofourown.org/works/5105735/chapters/11745368"))
```
The `getStoryMeta()` function returns a dictionary that looks like:
```
{'title': 'When In Doubt',
'author': 'JesWithOneEss',
'rating': 'Teen And Up Audiences',
'archiveWarnings': 'Creator Chose Not To Use Archive Warnings',
'category': 'F/M',
'fandom': 'Harry Potter - J. K. Rowling',
'relationship': 'Hermione Granger/Ron Weasley',
'characters': ['Hermione Granger', 'Ron Weasley'],
'tags': ['romione', 'Ron and Hermione - Freeform','Angst', 'Missing Moments', 'Deathly Hallows','book canon', 'Harry Potter - Freeform', 'book 7', 'rhr'],
'published_date': '2015-10-30',
'word_count': '13921',
'chapter_count': '4',
'comments': '8',
'kudos': '76',
'hits': '4217'}
```

For getting ffn story metadata:
```py
import fanficapi

ffn = fanficapi.FFN(headless=False, delay=5)
print (ffn.getStoryMeta("https://www.fanfiction.net/s/7562379/1/Australia"))
```
It is not recommended to use the headless mode as increases chances of getting detected by cloudflare, nevertheless, depends on when your are using and your luck

The `getStoryMeta()` returns a dictionary that looks like:
```
{'story_name': 'Australia',
'author_name': 'MsBinns',
'Rated': 'Fiction M',
'Language': 'English',
'Genre': 'Romance/Angst',
'Character': 'Ron W., Hermione G.',
'Chapters': '45',
'Words': '340,509',
'Reviews': '2,555',
'Favs': '2,026',
'Follows': '1,456',
'Updated': 'Aug 31, 2014',
'Published': 'Nov 19, 2011',
'Status': 'Complete',
'id': '7562379'}
```

- The `fanficapi.AO3()` takes only one optional argument `AO3(textMode: bool)` which is by default False
- The `fanficapi.FFN()` takes 4 optional argument `FFN(textMode: bool, headless: bool, executable_path: str, delay: int)`
- By default undetected-chromedriver is run in headless mode, set this to False if scraping doesnot work
- If you don't have chrome added to path, download the chromedriver from their wesite or use the one in the repo, set `executable_path = "/path/of/chromedriver"`
- If scraping doesn't work even after disableing headless mode, try increasing the delay (default is 5)
- Text mode just informs what's happening if you don't planning on printing the result but want to know the status

## License

> GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

I am not responsible for any kind of loss caused by the usage of this software. This is just a free software, use it at your own risk.