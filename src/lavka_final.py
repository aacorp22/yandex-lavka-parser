import time
import requests
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Page():
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)

    def click_button(self, class_name: str) -> None:
        """Finds a button by its classname and clicks it"""
        # button = driver.find_element(By.CLASS_NAME, class_name)
        button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
        button.click()
        time.sleep(2)

    def make_input(self, class_name: str, value: str) -> None:
        """Puts the value in the input field"""
        input_field = self.driver.find_element(By.CLASS_NAME, class_name)
        for letter in value:
            input_field.send_keys(letter)
            time.sleep(0.1)
        time.sleep(2)

    def approve_choices(self, class_name: str) -> None:
        """Approves input data by first dropdown option"""
        time.sleep(2)
        option = self.driver.find_element(By.CLASS_NAME, class_name)
        option.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        option.send_keys(Keys.RETURN)
        time.sleep(2)
