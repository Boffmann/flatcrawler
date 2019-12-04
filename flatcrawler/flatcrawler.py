from pathlib import Path
from python_json_config import Config, ConfigBuilder
import requests as req

from .WGResult import WGResult

class FlatCrawler(object):

    def __init__(self):
        """Parse the content of the config file"""
        config_path = Path(".").parent.resolve() / "config.json"
        builder = ConfigBuilder()
        parsed_config = builder.parse_config(str(config_path))

        self.urls = parsed_config.wggesucht.urls
        self.wg_results = []

    def run(self):
        """Query, parse and present wggesucht results"""
        for url in self.urls:
            wg_html_response = req.get(url)
            if wg_html_response.status_code == 200:
                wg_results = WGResult.from_html_response(wg_html_response.content)
