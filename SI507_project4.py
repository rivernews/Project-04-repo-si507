from browser import Browser
from cache import CacheManager
from database import DatabaseManager

import traceback

class NationalParkWebCrawler:

    homepage_url = 'https://www.nps.gov/index.htm'

    def __init__(self, browser=None, db=None, cache=None):
        self.browser = browser
        self.db = db
        self.cache = cache

        # only once, will store in db later
        # self.get_all_state_urls_and_abbreviations()
    
    def navigate_home_page(self):
        home_page = None

        self.browser.request_page(page_url=self.homepage_url)
        
        return home_page

    def get_all_state_urls_and_abbreviations(self):
        self.navigate_home_page()

        # query elements
        css_selector = (
            'ul.dropdown-menu.SearchBar-keywordSearch >' +
            'li >' +
            'a[id^=anch_]')
        anchors_list = self.browser.access_targets(css_selector)

        # extract information and save
        self.index_urls = [f'{anchor.get_attribute("href")}' for anchor in anchors_list]
        self.abbreviations = [ url.split('/')[-2] for url in self.index_urls]
        print(self.index_urls, self.abbreviations)

        # store States in db
        for abb in self.abbreviations:
            self.db.get_or_create('States', {
                'Name': abb
            })

        # store index page urls in db
        for url in self.index_urls:
            self.db.get_or_create('SitePages', {
                'Url': url,
                'IsDone': False
            })
    
    def navigate_state_index_page(self):
        return



if __name__ == "__main__":
    try:
        browser = Browser()
        db = DatabaseManager()
        cache = CacheManager(db=db)
        crawler = NationalParkWebCrawler(browser=browser, db=db, cache=cache)
    except Exception as err:
        traceback.print_tb(err.__traceback__)
        print(err)
    finally:
        browser.close()