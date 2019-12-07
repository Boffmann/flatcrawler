from typing import List
from .wg_gesucht_crawler import WGGesuchtCrawler
from .wg_result import WGResult


wg_gesucht_msg_base_url = "https://www.wg-gesucht.de/nachricht-senden.html?message_ad_id="

# def write_wg_gesucht_messageadvert_id: str, renter_name: str, city: str, language: str):
#     msg_url = wg_gesucht_msg_base_url + advert_nr

def parse_wg_results_from_advert_urls(advert_urls: List[str], crawler: WGGesuchtCrawler):
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
