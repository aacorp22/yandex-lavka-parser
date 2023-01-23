from src import logger

from src.parser.address_handler import Page
from src.config.config_reader import config

locations = list(config["locations"].values())
urls = list(config["urls"].values())

snacks = Page(urls[0])
snacks.set_address(locations[0])
