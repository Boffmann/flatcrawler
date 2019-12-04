from pathlib import Path
from python_json_config import ConfigBuilder
from typing import Dict
import requests as req
import sys

from .wg_result import WGResult
from .telegram_sender import SenderTelegram

class FlatCrawler(object):

    def __init__(self):
        """Parse the content of the config file"""
        config_path = Path(".").parent.resolve() / "config.json"
        builder = ConfigBuilder()
        config = builder.parse_config(str(config_path))

        self.urls = config.wggesucht.urls
        self.telegram_sender = SenderTelegram(config.telegram.bot_token, config.telegram.receiver_ids)
        # Stores all found WGResults. Everytime the query runs its results are added to this list.
        # The dictionary only stores unique values to prevent that inserts are sent more than once to the user
        # self.advert_hash_list = Dict[str, WGResult]
        self.advert_hash_list: Dict[str, WGResult] = {}

    def run(self):
        """Query, parse and present wggesucht results"""
        for url in self.urls:
            wg_html_response = req.get(url)
            if wg_html_response.status_code == 200:
                try:
                    wg_results = WGResult.from_html_response(wg_html_response.content)
                except:
                    e = sys.exc_info()[0]
                    print("Error creating wg_result " + str(e))
                    continue
                for result in wg_results:
                    # To prevent that single adverts are sent twice
                    if not result.hash in self.advert_hash_list.keys():
                        self.advert_hash_list[result.hash] = result
                        print(result.as_string())
