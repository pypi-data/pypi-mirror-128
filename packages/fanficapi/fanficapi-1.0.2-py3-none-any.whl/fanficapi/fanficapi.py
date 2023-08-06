from .ao3essentials.story import getMeta as _ao3_story
from .ao3essentials.author import getProfileMeta as _ao3_author_meta
from .ao3essentials.author import getStoryWrittenMeta as _ao3_author_story_meta
from .ffnessentials.story import getMeta as _ffn_story

class AO3:
    def __init__(self, textMode=False):
        self.textMode = textMode
        if self.textMode: print ("Initialized AO3 scraper")

    def getStoryMeta(self, link: str):
        if self.textMode: print (f"Scraping story metadata from {link}...", end="")
        meta =  _ao3_story(link)
        if self.textMode: print ("Done")
        return meta

    def getProfile(self, link: str):
        if self.textMode: print (f"Scraping author metadata from {link}...", end="")
        meta = _ao3_author_meta(link)
        if self.textMode: print ("Done")
        self.profile_meta = meta
        if self.textMode: print (f"Collecting stories written by author in from {link}...", end="")
        meta = _ao3_author_story_meta(link)
        if self.textMode: print ("Done")
        self.stories_meta = meta
        if self.textMode: print ("Note: If author has written more than 20 stories, only the last 20 will be listed, working on the advanced version though with lot more features")
        return self

class FFN:
    def __init__(self, textMode=False, headless=True, executible_path=None, delay=5):
        self.textMode = textMode
        self.headless=headless
        self.executible_path=executible_path
        self.delay=delay
        if self.textMode: print ("Initialized FFN scraper")

    def getStoryMeta(self, link: str):
        if self.textMode: print (f"Scraping story metadata from {link}...", end="")
        meta =  _ffn_story(link, headless=self.headless, executable_path=self.executible_path, delay=self.delay)
        if self.textMode: print ("Done")
        return meta