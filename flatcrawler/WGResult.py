from bs4 import BeautifulSoup
from bs4.element import Tag
import re
import requests as req

class WGResult(object):

    def __init__(self, html: Tag):
        """Gets a single advert and creates a data object from it"""
        headline = html.find('h3', {'class': 'headline'}).select("a")
        self.baseurl = 'https://www.wg-gesucht.de/'
        self.url = None
        self.title = None
        self.size_of_room = None
        self.room_cost = None
        self.address = None
        self.availability_from = None
        self.availability_to = None
        if len(headline) > 0:
            self.url = self.baseurl + headline[0]['href']
        if self.url is not None:
            # Crawl side of room
            room_html_response = req.get(self.url)
            if room_html_response.status_code == 200:
                soup = BeautifulSoup(room_html_response.content, 'html.parser')
                self.title = soup.find('h1', {'id': 'sliderTopTitle'}).text.strip()
                main_column = soup.find('div', {'id': 'main_column'})
                self.size_of_room = list(main_column.find_all('div', {'class': "col-xs-6 text-center print_inline"}))[0].select("h2")[0].text.strip()
                self.room_cost = list(main_column.find_all('div', {'class': "col-xs-6 text-center print_inline"}))[1].select("h2")[0].text.strip()
                self.address = list(main_column.find_all('div', {'class': "col-sm-4 mb10"}))[0].select("a")[0].text.strip()
                self.availability_from = list(main_column.find_all('div', {'class': "col-sm-3"}))[0].select("p")[0].select("b")[0].text.strip()
                self.availability_to = list(main_column.find_all('div', {'class': "col-sm-3"}))[0].select("p")[0].select("b")[1].text.strip()

    @classmethod
    def from_html_response(cls, html: str):
        """Creates a list of WGResults from the results in html"""
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        adverts = soup.find_all('div', {'id': re.compile(r'^liste-details-ad-[0-9]*$')})
        print("Number of results: " + str(len(adverts)))
        if len(adverts) != 0:
            for advert in adverts:
                results.append(WGResult(advert))
        return results
