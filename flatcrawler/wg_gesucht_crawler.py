from bs4 import BeautifulSoup
from bs4.element import Tag
import requests as req
import re
import sys
import traceback

class WGGesuchtCrawler(object):
    """Class to get all information from a wg-gesucht advert side"""

    def __init__(self):
        """Gets the url of a single advert"""
        self.url = None
        self.soup = None
        self.baseurl = 'https://www.wg-gesucht.de/'


    def ready(self):
        ready = self.url != None and self.soup != None
        if not ready:
            print("Cannot parse website. URL not set")
        return ready

    def get_new_adverts(self, overview_html: str):
        """Parses all new adverts from a given overview html document and returns urls for all found adverts"""
        results = []
        local_soup = BeautifulSoup(overview_html, 'html.parser')
        adverts = local_soup.find_all('div', {'id': re.compile(r'^liste-details-ad-[0-9]*$')})
        print("Number of results: " + str(len(adverts)))
        if len(adverts) != 0:
            for advert in adverts:
                headline = advert.find('h3', {'class': 'headline'}).select("a")
                if len(headline) > 0:
                    try:
                        results.append(self.baseurl + headline[0]['href'])
                    except:
                        print("Error parsing advert url")
        return results


    def set_url(self, advert_url: str):
        self.url = advert_url
        advert_side_response = req.get(self.url)
        if advert_side_response.status_code != 200:
            raise # TODO Exception
        self.soup = BeautifulSoup(advert_side_response.content, 'html.parser')
        self.main_column = self.soup.find('div', {'id': 'main_column'})


    def get_title(self):
        if not self.ready():
            return ""
        try:
            return self.soup.find('h1', {'id': 'sliderTopTitle'}).text.strip()
        except:
            print("Error parsing wg_gesucht advert's title")
            return ""

    def get_room_size(self):
        if not self.ready():
            return ""
        try:
            return list(self.main_column.find_all('div', {'class': "col-xs-6 text-center print_inline"}))[0].select("h2")[0].text.strip()
        except:
            print("Error parsing wg_gesucht advert's room size")
            return ""


    def get_room_cost(self):
        if not self.ready():
            return ""
        try:
            return list(self.main_column.find_all('div', {'class': "col-xs-6 text-center print_inline"}))[1].select("h2")[0].text.strip()
        except:
            print("Error parsing wg_gesucht advert's costs")
            return ""


    def get_address(self):
        if not self.ready():
            return ""
        try:
            return list(self.main_column.find_all('div', {'class': "col-sm-4 mb10"}))[0].select("a")[0].text.strip()
        except:
            print("Error parsing wg_gesucht advert's address")
            return ""


    def get_available_from(self):
        if not self.ready():
            return ""
        try:
            return list(self.main_column.find_all('div', {'class': "col-sm-3"}))[0].select("p")[0].select("b")[0].text.strip()
        except:
            print("Error parsing availabilty from")
            return ""


    def get_available_to(self):
        if not self.ready():
            return ""
        try:
            return list(self.main_column.find_all('div', {'class': "col-sm-3"}))[0].select("p")[0].select("b")[1].text.strip()
        except:
            print("Error parsing availabilty to")
            return ""

    def get_city(self):
        if not self.ready():
            return ""
        try:
            address = self.get_address()
            if address.find("Berlin"):
                return "Berlin"
            elif address.find("Potsdam"):
                return "Potsdam"
            else:
                return ""
        except:
            e = sys.exc_info()[0]
            track = traceback.format_exc()
            print("Error parsing city \n" + str(e) + "\n" + track)
            return ""
