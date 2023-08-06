import undetected_chromedriver.v2 as uc
from pathlib import Path
import bs4

from .errors import validate_link

"""
1) Initialize chromedriver profile to prevent chrome startup dialogue
2) Sorry, I packed all these indide a single function, will update later to seperate the tasks
"""
# (1)
def stop_chrome_init_dialog(options):
    # Create empty profile
    Path('./chrome_profile').mkdir(parents=False, exist_ok=True)
    Path('./chrome_profile/First Run').touch()
    options.add_argument('--user-data-dir=./chrome_profile/')
# (2)
def getMeta(link, headless, executable_path, delay):
    options = uc.ChromeOptions()
    stop_chrome_init_dialog(options)
    validate_link(link)
    driver = uc.Chrome(options=options, delay = delay, headless=headless, executable_path=executable_path)

    driver.get(link)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')
    metadata = soup.find('div', id='profile_top').getText()
    metalist = metadata.split('\n')
    metadata = metalist[3].split('-')
    alt_key = ['Language', 'Genre', 'Character']
    i=0
    story_name = soup.find('b', 'xcontrast_txt').getText()
    author_name= metalist[1].split(':')[1].strip()
    meta = {}
    meta['story_name']=story_name
    meta['author_name']=author_name

    for data in metadata:
        if ':' in data:
            key = data.split(':')[0].strip()
            value = data.split(':')[1].strip()
        else:
            key = alt_key[i]
            i += 1
            value = data.strip()
        meta[key]=value

    return meta