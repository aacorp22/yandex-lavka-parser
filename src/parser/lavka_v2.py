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

ADDRESS = "Россия, Одинцово, Можайское шоссе, 122"#"Россия, Москва, Мосфильмовская улица, 42с1"
URL = 'https://lavka.yandex.ru/213/category/snacks'

def click_button(driver: webdriver, class_name: str) -> None:
    """Finds a button by its classname and clicks it"""
    # button = driver.find_element(By.CLASS_NAME, class_name)
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
    button.click()
    time.sleep(2)

def make_input(driver: webdriver, class_name: str, value: str) -> None:
    """Puts the value in the input field"""
    input_field = driver.find_element(By.CLASS_NAME, class_name)
    for letter in value:
        input_field.send_keys(letter)
        time.sleep(0.1)
    time.sleep(2)

def approve_choices(driver: webdriver, class_name: str) -> None:
    """Approves input data by first dropdown option"""
    time.sleep(2)
    option = driver.find_element(By.CLASS_NAME, class_name)
    option.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    option.send_keys(Keys.RETURN)
    time.sleep(2)

options = webdriver.ChromeOptions()
# options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

# Open the website
driver.get(URL)
print("Page loaded successfully")
time.sleep(5)
try:
    # Your location button
    click_button(driver, 'bzscopr.c14xrn6c.cow0qbn.a71den4.m16coeem.m1wd6zeg')
    # Clear text in input field button
    click_button(driver, "c12fmzph")
    # Make input in input field
    make_input(driver, "i164506l", ADDRESS)
    # Press enter to approve the input
    approve_choices(driver, "i164506l")
    # Click OK button
    click_button(driver, "bzscopr.f19ph74x.c14xrn6c.cow0qbn.a71den4.m16coeem.m1wd6zeg.w3gf8dt")
except Exception as error:
    print(error)


session = requests.Session()
# Set correct user agent
selenium_user_agent = driver.execute_script("return navigator.userAgent;")
session.headers.update({"user-agent": selenium_user_agent})

for cookie in driver.get_cookies():
    session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

res = session.get(URL)
content = res.text
soup=BeautifulSoup(content, "html.parser")
# with open("snacksv3.html", "w", encoding="utf-8") as file:
#     file.write(soup.prettify())

driver.quit()

# from selenium import webdriver
# import requests

# driver = webdriver.Chrome()
# driver.get("https://www.linkedin.com/uas/login?")

# s = requests.Session()
# # Set correct user agent
# selenium_user_agent = driver.execute_script("return navigator.userAgent;")
# s.headers.update({"user-agent": selenium_user_agent})

# for cookie in driver.get_cookies():
#     s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

# response = s.get("https://linkedin/example_page.com")