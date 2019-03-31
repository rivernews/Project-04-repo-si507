from browser import Browser

class DatabaseManager:

    db_name = 'my-database'
    database_object = None

    def __init__(self, *args, **kwargs):
        if not self.is_database_exist():
             self.establish_database_and_schema()
        else:
            self.database_object = self.read_database_object()
        
        return self.database_object

    
    def is_database_exist(self):
        # TODO
        return True
    
    def read_database_object(self):
        database_object = None

        # TODO

        return database_object
    
    def establish_database_and_schema(self):
        database_object = None
        # TODO

        self.database_object = database_object
        return
    
    def wipe_database(self):
        # TODO
        return
    
    def export_site_to_csv(self):
        # TODO
        return
    
    def is_page_complete(self, url):
        """
            check if the url is completed.
            will try to get that url from table `CompletedPage`.
            if it's there, it means the page is completed, and should return TRUE.
        """
        return False

class FileCacheManager:

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
    
    def get_or_cache(self, key, value_func, value_func_kwargs={}):
        """
            call this function first to get the value
            this function will guarantee you get a value at the end
            it will handle the cache and optimize for you
        """
        cache_object = None

        if self.is_cache_exist():
            cache_object = self.load_cache_content()
        else:
            cache_object = value_func(**value_func_kwargs)
            self.store_cache_content(cache_object)

        return cache_object
    
    def is_cache_exist(self):
        # TODO
        return False
    
    def load_cache_content(self):
        cache_content = None

        # TODO

        return cache_content # should load file ito python variable
    
    def store_cache_content(self, content):
        # TODO

        return

class NationalParkWebCrawler:

    homepage_url = 'https://www.nps.gov/index.htm'

    def __init__(self, browser=None, db=None, cache=None):
        self.browser = browser
        self.db = db
        self.cache = cache

        # only once, will store in db later
        self.get_all_state_urls_and_abbreviations()
    
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

        # extract information
        index_urls = [f'{self.homepage_url}{anchor.get_attribute("href")}' for anchor in anchors_list]
        abbreviations = [ url.split('/')[-2] for url in index_urls]
        print(abbreviations)
    
    def navigate_state_index_page(self):
        return



if __name__ == "__main__":
    browser = Browser()
    db = DatabaseManager()
    cache = FileCacheManager()
    crawler = NationalParkWebCrawler(browser=browser, db=db, cache=cache)
    browser.close()