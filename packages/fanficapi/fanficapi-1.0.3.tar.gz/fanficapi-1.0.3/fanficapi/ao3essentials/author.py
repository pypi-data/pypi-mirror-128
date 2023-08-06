import requests
import bs4

from .errors import validate_link, validate_status
# (1) Fetch source html
def fetch_html(link):
    validate_link(link)
    req = requests.get(link)
    validate_status(req)
    return req.text

def getProfileMeta(link):
    link = link + "/profile"
    html = fetch_html(link)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    soup_meta = soup.find('dl', 'meta')
    pseuds = soup_meta.find('dd', 'pseuds').getText()
    join_date = soup_meta.find('dd', False).getText()
    user_id = soup_meta.findAll('dd', False)[2].getText()
    author = soup.find('h2', 'heading').getText().strip()
    alt_name = soup.findAll('h3', 'heading')[1].getText().strip()
    soup = soup.find('div', 'bio module')
    bio = soup.find('p').getText()
    meta = {
        'link' : link,
        'pseuds' : pseuds,
        'join_date' : join_date,
        'user_id' : user_id,
        'author' : author,
        'alt_name' : alt_name,
        'bio' : bio
    }
    return meta

def getStoryWrittenMeta(link):
    html = fetch_html(link + "/works")
    soup = bs4.BeautifulSoup(html, 'html.parser')
    total = soup.find('span', 'current').getText()
    total = total[total.index('(')+1 : total.index(')')] ## Still lot to do, other story meta needed
    soup = soup.find('ol', 'work index group')
    list = soup.findAll('a', False, rel=False, href=True)
    base = "https://archiveofourown.org"
    story_links = []
    for each in list:
        nlink = str(each['href'])
        if ('chapters' not in nlink and 'comments' not in nlink and 'kudos' not in nlink and 'bookmarks' not in nlink):
            story_links.append(base+nlink)
    meta = {
        'link' : link + "/works",
        'total' : total,
        'story_links' : story_links
    }
    return meta