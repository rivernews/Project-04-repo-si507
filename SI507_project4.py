from browser import Browser
from cache import CacheManager
from database import DatabaseManager

import traceback
from enum import Enum

class TableName(Enum):
    sites = "Sites"
    index_pages = "SitePages"
    states = "States"

class NationalParkWebCrawler:

    homepage_url = 'https://www.nps.gov/index.htm'

    def __init__(self, browser=None, db=None, cache=None):
        self.browser = browser
        self.db = db
        self.cache = cache

        # only once, will store in db later
        self.get_all_state_urls_and_abbreviations()

        self.get_all_sites_in_page()
    
    def navigate_to(self, url):
        self.browser.request_page(page_url=url)
    
    def url_to_state_abbreviation(self, url):
        return url.split('/')[-2]
    
    def get_all_state_urls_and_abbreviations(self):
        self.navigate_to(self.homepage_url)

        # query elements
        css_selector = (
            'ul.dropdown-menu.SearchBar-keywordSearch >' +
            'li >' +
            'a[id^=anch_]')
        anchors_list = self.browser.access_targets(css_selector)

        # extract information and save
        self.index_urls = [f'{anchor.get_attribute("href")}' for anchor in anchors_list]
        self.abbreviations = [ self.url_to_state_abbreviation(url) for url in self.index_urls]

        # store States in db
        for abb in self.abbreviations:
            self.db.create(TableName.states.value, {
                'Name': abb
            }, unique_fields=[
                'Name'
            ])

        # store index page urls in db
        for url in self.index_urls:
            self.db.create(TableName.index_pages.value, {
                'Url': url,
                'IsDone': False
            }, unique_fields=[
                'Url'
            ])
    
    def get_all_sites_in_page(self):

        # get not yet visited url
        page_objects = self.db.filter(TableName.index_pages.value, {
            'IsDone': False
        })

        for page_index_zero, page_object in enumerate(page_objects):
            page_index = page_index_zero + 1
            page_percentage = str( round(page_index / 56, 2) * 100) + '%'

            page_object_id = page_object[0]
            url = page_object[1]

            state_abbreviation = self.url_to_state_abbreviation(url)
            state_object = self.db.filter(TableName.states.name, {'Name': state_abbreviation})[0]
            state_object_id = state_object[0]

            print("\n\n\n\n")
            print("Page for state", state_abbreviation, "page id =", page_object_id)
            print(page_percentage,"="*30)

            self.navigate_to(url)

            # query elements
            base_css_selector = ' '.join([
                '#parkListResultsArea #list_parks',
                'div.table-cell.list_left'
            ])
            site_elements = self.browser.access_targets(base_css_selector)

            for index_zero, site_element in enumerate(site_elements):
                index = index_zero + 1
                type_element = self.browser.access_targets('h2', base_element=site_element, many=False)
                name_element = self.browser.access_targets('h3 > a', base_element=site_element, many=False)
                location_element = self.browser.access_targets('h4', base_element=site_element, many=False)
                description_element = self.browser.access_targets('p', base_element=site_element, many=False)

                # extract information
                type_value = name_value = location_value = description_value = None

                type_value = type_element.get_attribute("innerHTML")
                name_value = name_element.get_attribute("innerHTML")
                location_value = location_element.get_attribute("innerHTML")
                description_value = description_element.get_attribute("innerHTML").strip()

                # process data (optional)
                print(f'{page_percentage} page {page_index} - site {index}')
                print(type_value)
                print(name_value)
                print(location_value)
                print(description_value)
                print(page_percentage,'-'*30)

                # save in db
                self.db.create(TableName.sites.value, {
                    'Name': name_value,
                    'Type': type_value,
                    'Description': description_value,
                    'Location': location_value,
                    'StateID': state_object_id,
                }, unique_fields=[
                    'Name', 'Type', 'Location', 

                    # same site may spread across different states
                    # in such case, that site will show up in all states' page
                    # even it belongs to the same site, we'll treat each state as different sites
                    'StateID', 
                ])

                self.db.update(TableName.index_pages.value, {
                    'IsDone': True,
                }, pk=page_object_id )


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