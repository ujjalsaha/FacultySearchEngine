from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import re
import urllib
import sys
import logging
import requests
import tldextract

import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'lib'))
# TODO - Need to update the URL scrapper class.

# options = Options()
# options.headless = True
# driver = webdriver.Chrome('./chromedriver', options=options)
#
# console_format = '%(name)s - %(levelname)s - %(message)s'
# logging.root.setLevel(logging.INFO)
# logging.basicConfig(level=logging.INFO, format=console_format)
#
#
# def get_js_soup(url):
#     driver.get(url)
#     res_html = driver.execute_script('return document.body.innerHTML')
#     soup = BeautifulSoup(res_html, 'html.parser')  # beautiful soup object to be used for parsing html content
#     return soup
#
#
# def remove_script(soup):
#     for script in soup(["script", "style"]):
#         script.decompose()
#     return soup
#
#
# def tag_visible(element):
#     if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
#         return False
#     if isinstance(element, Comment):
#         return False
#     return True


