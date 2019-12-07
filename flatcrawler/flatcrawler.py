from selenium import webdriver
from pathlib import Path
from python_json_config import ConfigBuilder
from typing import Dict
import requests as req

from .wg_result import WGResult
from .telegram_sender import SenderTelegram
from .telegram_receiver import ReceiverTelegram
from .wg_gesucht_crawler import WGGesuchtCrawler
from .driver import build_driver
from .wg_gesucht_utils import parse_wg_results_from_advert_urls
import time

class FlatCrawler(object):

    def __init__(self, config: str):
        """Parse the content of the config file"""
        config_path = Path(".").parent.resolve() / config
        builder = ConfigBuilder()
        self.config = builder.parse_config(str(config_path))
        self.driver = build_driver(self.config)

        self.wg_gesucht_filter_urls = self.config.wggesucht.urls
        self.telegram_sender = SenderTelegram(self.config.telegram.bot_token, self.config.telegram.receiver_ids)
        self.telegram_receiver = ReceiverTelegram(self.config.telegram.bot_token, self.config.telegram.receiver_ids)
        self.wg_gesucht_crawler = WGGesuchtCrawler()



    def get_new_wg_gesucht_adverts(self):
        for filter_url in self.wg_gesucht_filter_urls:
            wg_overview_html_response = req.get(filter_url)
            if wg_overview_html_response.status_code == 200:
                new_advert_urls = self.wg_gesucht_crawler.get_new_adverts(wg_overview_html_response.content)
                return parse_wg_results_from_advert_urls(new_advert_urls, self.wg_gesucht_crawler)
        return []

    def screenshot(self):
        return self.driver.get_screenshot_as_file("/home/hendrik/screenshot.png")

    def login(self):
        self.driver.get("https://www.wg-gesucht.de/")
        login_button = self.driver.find_element_by_xpath("//div[@id='headbar_wrapper']/div[2]/a[2]")
        login_button.click()
        time.sleep(1)
        email_input = self.driver.find_element_by_id("login_email_username")
        email_input.clear()
        email_input.send_keys(self.config.wggesucht.email)
        password_input = self.driver.find_element_by_id("login_password")
        password_input.clear()
        password_input.send_keys(self.config.wggesucht.password)
        time.sleep(1)
        self.driver.find_element_by_id("login_submit").click()
        time.sleep(5)

    def run(self):
        """Query, parse and present wggesucht results"""
        wg_results = self.get_new_wg_gesucht_adverts()
        for result in wg_results:
            # To prevent that single adverts are sent twice
            if not result.hash in self.advert_hash_list.keys():
                self.advert_hash_list[result.hash] = result
                print(result.as_string())
