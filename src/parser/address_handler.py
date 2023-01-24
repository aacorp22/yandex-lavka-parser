import time
import logging
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.config.config_reader import get_config

logger = logging.getLogger("handler")

config = get_config()

class Page():
    def __init__(self, url: str = "NotSpecified") -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.headless = False # TODO: make this configurable
        self.driver = webdriver.Chrome(options=self.options)
        self.url = url

        if "NotSpecified" in self.url:
            raise ValueError("Expected page url")

        conf = config["html_classes"]
        self.location_button = conf["location_button"]
        self.clear_input = conf["clear_input"]
        self.input_field = conf["input_field"]
        self.ok_button = conf["ok_button"]
        logger.info("Page initialized successfully")

    def click_button(self, class_name: str) -> None:
        """Finds a button by its classname and clicks it"""
        # button = driver.find_element(By.CLASS_NAME, class_name)
        button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
        button.click()
        logger.info(f"Button {class_name} clicked")
        time.sleep(2)

    def make_input(self, class_name: str, value: str) -> None:
        """Puts the value in the input field"""
        input_field = self.driver.find_element(By.CLASS_NAME, class_name)
        for letter in value:
            input_field.send_keys(letter)
            time.sleep(0.1)
        logger.info(f"Input '{value}' made in {class_name}")
        time.sleep(2)

    def approve_choices(self, class_name: str) -> None:
        """Approves input data by first dropdown option"""
        time.sleep(2)
        option = self.driver.find_element(By.CLASS_NAME, class_name)
        option.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        option.send_keys(Keys.RETURN)
        logger.info(f"First dropdown option selected in {class_name}")
        time.sleep(2)
    
    def get_html_text(self, html_string: str) -> str:
        """Gets text from html, removes unicode special characters"""
        return html_string.get_text().strip().replace("\xad", "").replace("\xa0", " ")
    
    def save_to_html(self, soup_content: BeautifulSoup, filename: str) -> None:
        """Saves the contents to html file with the given filename"""
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(soup_content.prettify())
                logger.info(f"File {filename} saved to html")
        except Exception as error:
            logger.error(f"Error saving file {filename}")
            raise (f"Could not write to file: {filename}:{error}")

    def set_address(self, address: str) -> None:
        """Handler for calling all functions and setting an address"""
        # Open the website
        try:
            self.driver.get(self.url)
            logger.info("Page loaded successfully")
        except Exception as error:
            logger.error(f"Could not load url {self.url}: {error}")
            raise
        time.sleep(5)
        try:
            # Your location button
            self.click_button(self.location_button)
            # Clear text in input field button
            self.click_button(self.clear_input)
            # Make input in input field
            self.make_input(self.input_field, address)
            # Press enter to approve the input
            self.approve_choices(self.input_field)
            # Click OK button
            self.click_button(self.ok_button)
            self.driver.quit()
        except Exception as error:
            logger.error(f"Could not set address {self.url}: {error}")
