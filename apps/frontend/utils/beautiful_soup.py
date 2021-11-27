from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests

import sys, os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'lib'))
# TODO - Need to update the URL scrapper class.

options = Options()
options.headless = True
options.add_argument('--no-sandbox')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)

# driver = webdriver.Chrome('../../../lib/chromedriver', options=options)


def get_js_soup(base_url):
    driver.get(base_url)
    res_html = driver.execute_script('return document.body.innerHTML')
    return build_soup(res_html)


def get_all_page(base_url):
    response = requests.get(base_url)
    html_doc = response.text
    return build_soup(html_doc)

def build_soup(html):
    soup = BeautifulSoup(html, 'html.parser')  # beautiful soup object to be used for parsing html content
    return soup


def remove_script(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def close_driver():
    driver.close()
