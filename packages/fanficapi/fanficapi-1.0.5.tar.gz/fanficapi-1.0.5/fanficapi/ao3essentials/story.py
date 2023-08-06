import requests, bs4

from .errors import validate_link, validate_status
"""
1) Fetch html from ao3 (includes error handling)
2) Seperate the part of html which contains story metadata
3) Generate a dictionary which contains metadata
4) The usable function that performs everything serially and returns the dictionarry
"""
# (1) Fetch source html
def fetch_html(link):
    validate_link(link)
    req = requests.get(link)
    validate_status(req)
    return req.text
# (2) Seperate the part of html that contains metadata
def format_part(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    html = soup.find('dl', 'work meta group', role='complementary')
    return html
# (3) Generate dictionary containing metadata
def getDict(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    title = soup.find('h2', 'title heading').getText().replace("\n","").strip()
    author = soup.find('a', rel='author').getText()

    html = format_part(html)
    soup = html
    characters = []
    tags = []
    meta = {}

    rating  = soup.findAll('a', 'tag')[0].getText()
    archiveWarnings = soup.findAll('a', 'tag')[1].getText()
    category = soup.findAll('a', 'tag')[2].getText()
    fandom = soup.findAll('a', 'tag')[3].getText()
    relationship = soup.findAll('a', 'tag')[4].getText()
    character_tags = soup.find('dd', 'character tags')
    for character in character_tags.findAll('a', 'tag'):
        characters.append(character.getText())
    freeform_tags = soup.find('dd', 'freeform tags')
    for tag in freeform_tags.findAll('a', 'tag'):
        tags.append(tag.getText())
    published_date = soup.find('dd', 'published').getText()
    word_count = soup.find('dd', 'words').getText()
    chapter_str = soup.find('dd', 'chapters').getText()
    chapter_count = chapter_str[chapter_str.index('/')+1:]
    if '?' in chapter_count: chapter_count = chapter_str[:chapter_str.index('/')]
    comments = soup.find('dd', 'comments').getText()
    kudos = soup.find('dd', 'kudos').getText()
    hits = soup.find('dd', 'hits').getText()

    meta = {
        'title':title,
        'author':author,
        'rating':rating,
        'archiveWarnings':archiveWarnings,
        'category':category,
        'fandom':fandom,
        'relationship':relationship,
        'characters':characters,
        'tags':tags,
        'published_date':published_date,
        'word_count':word_count,
        'chapter_count':chapter_count,
        'comments':comments,
        'kudos':kudos,
        'hits':hits
    }    
    return meta
# (4) The usable function that performs everything serially and returns the dictionarry
def getMeta(link):
    # parameters
    # ----------
    # link: str (takes ao3 story URL to generate meta dict)
    return getDict(fetch_html(link))