from pathlib import Path
from python_json_config import ConfigBuilder
from typing import Dict
import requests as req

from .wg_result import WGResult
from .telegram_sender import SenderTelegram
from .telegram_receiver import ReceiverTelegram
from .wg_gesucht_crawler import WGGesuchtCrawler

class FlatCrawler(object):

    def __init__(self):
        """Parse the content of the config file"""
        config_path = Path(".").parent.resolve() / "config.json"
        builder = ConfigBuilder()
        config = builder.parse_config(str(config_path))

        self.wg_gesucht_filter_urls = config.wggesucht.urls
        self.telegram_sender = SenderTelegram(config.telegram.bot_token, config.telegram.receiver_ids)
        self.telegram_receiver = ReceiverTelegram(config.telegram.bot_token, config.telegram.receiver_ids)
        self.wg_gesucht_crawler = WGGesuchtCrawler()
        # Stores all found WGResults. Everytime the query runs its results are added to this list.
        # The dictionary only stores unique values to prevent that inserts are sent more than once to the user
        # self.advert_hash_list = Dict[str, WGResult]
        self.advert_hash_list: Dict[str, WGResult] = {}

    def get_new_wg_gesucht_adverts(self):
        for filter_url in self.wg_gesucht_filter_urls:
            wg_overview_html_response = req.get(filter_url)
            if wg_overview_html_response.status_code == 200:
                new_advert_urls = self.wg_gesucht_crawler.get_new_adverts(wg_overview_html_response.content)
                return WGResult.parse_from_advert_urls(new_advert_urls, self.wg_gesucht_crawler)
        return []

    def run(self):
        """Query, parse and present wggesucht results"""
        wg_results = self.get_new_wg_gesucht_adverts()
        for result in wg_results:
            # To prevent that single adverts are sent twice
            if not result.hash in self.advert_hash_list.keys():
                self.advert_hash_list[result.hash] = result
                print(result.as_string())
