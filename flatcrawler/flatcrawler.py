from pathlib import Path
from python_json_config import Config, ConfigBuilder

class FlatCrawler(object):

    def __init__(self):
        """Parse the content of the config file"""
        config_path = Path(".").parent.resolve() / "config.json"
        builder = ConfigBuilder()
        parsed_config = builder.parse_config(str(config_path))
        self.urls = parsed_config.wggesucht.urls
