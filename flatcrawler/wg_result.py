from typing import List

from .wg_gesucht_crawler import WGGesuchtCrawler


class WGResult(object):

    def __init__(self,
                 url: str,
                 title: str,
                 size: str,
                 cost: str,
                 address: str,
                 available_from: str,
                 available_to: str,
                 city: str,
                 advert_nr: str):
        self.url = url
        self.title = title
        self.size_of_room = size
        self.room_cost = cost
        self.address = address
        self.availability_from = available_from
        self.availability_to = available_to
        self.city = city
        self.id = advert_nr

    def as_string(self):
        result = "Title: " + self.title + "\n" \
                  + "Size: " + self.size_of_room + "\n" \
                  + "Cost: " + self.room_cost + "\n" \
                  + "Available from: " + self.availability_from + "\n" \
                  + "Available to: " + self.availability_to + "\n" \
                  + "Address: " + self.address + "\n" \
                  + "id: " + self.id + "\n" \
                  + "URL: " + self.url
        return result


    @classmethod
    def parse_from_advert_urls(cls, advert_urls: List[str], crawler: WGGesuchtCrawler):
        """Creates a list of WGResults from a list of advert urls using crawler"""
        results = []
        for url in advert_urls:
            crawler.set_url(url)
            results.append(WGResult(url,
                                    crawler.get_title(),
                                    crawler.get_room_size(),
                                    crawler.get_room_cost(),
                                    crawler.get_address(),
                                    crawler.get_available_from(),
                                    crawler.get_available_to(),
                                    crawler.get_city(),
                                    crawler.get_advert_nr()))


        return results
