import atexit

from python_json_config import Config
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

def options(config: Config) -> Options:
    options = Options()
    for key, value in config.firefox.options.items():
        setattr(options, key.split(".")[-1], value)
    return options

def capabilities(config: Config) -> DesiredCapabilities:
    capabilities = DesiredCapabilities.FIREFOX

    for key, value in config.firefox.capabilities.items():
        capabilities[key.split(".")[-1]] = value
    return capabilities

def build_driver(config: Config):
    driver = webdriver.Firefox(firefox_binary=config.firefox.bin_path,
                               capabilities=capabilities(config),
                               options=options(config))
    atexit.register(driver.quit)
    return driver
