from bs4 import BeautifulSoup
from bs4.element import Tag
import re
import requests as req
from types import LambdaType

def get_element_save(element_function: LambdaType, error_msg: str):
    try:
        return element_function()
    except(TypeError, KeyError) as e:
        print(error_msg + "\n" + str(e))

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
                try:
                    soup = BeautifulSoup(room_html_response.content, 'html.parser')
                except:
                    print("Error parsing the website: " + self.url)
                    return
                self.title = get_element_save(lambda: soup.find('h1', {'id': 'sliderTopTitle'}).text.strip(), "Error parsing adverts title")
                main_column = soup.find('div', {'id': 'main_column'})
                self.size_of_room = get_element_save(lambda: list(main_column.find_all('div', {'class': "col-xs-6 text-center print_inline"}))[0].select("h2")[0].text.strip(), "Error parsing advert's size of room")
                self.room_cost = get_element_save(lambda: list(main_column.find_all('div', {'class': "col-xs-6 text-center print_inline"}))[1].select("h2")[0].text.strip(), "Error parsing advert's cost")
                self.address = get_element_save(lambda: list(main_column.find_all('div', {'class': "col-sm-4 mb10"}))[0].select("a")[0].text.strip(), "Error parsing advert's address")
                self.availability_from = get_element_save(lambda: list(main_column.find_all('div', {'class': "col-sm-3"}))[0].select("p")[0].select("b")[0].text.strip(), "Error parsing advert's availability_from")
                self.availability_to = get_element_save(lambda: list(main_column.find_all('div', {'class': "col-sm-3"}))[0].select("p")[0].select("b")[1].text.strip(), "Error parsing advert's availability_to")


    def as_string(self):
        result = "Title: " + self.title + "\n" \
                  + "Size: " + self.size_of_room + "\n" \
                  + "Cost: " + self.room_cost + "\n" \
                  + "Available from: " + self.availability_from + "\n" \
                  + "Available to: " + self.availability_to + "\n" \
                  + "Address: " + self.address + "\n" \
                  + "URL: " + self.url
        return result


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
