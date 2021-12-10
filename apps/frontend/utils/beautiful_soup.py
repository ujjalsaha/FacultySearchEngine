from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests

import sys, os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'lib'))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def html_tag_visible(element):
    """
    removing items from the below tags.
    :param element: html element tag
    :return: elements
    """
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


class BeautifulSoupLocal:
    def __init__(self, url=None, html=None):
        self.url = url
        self.html = html
        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')
        self.s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.s, options=options)

    def get_html(self):
        """
        Get HTML from any url.
        :return: beautiful soup html.
        """
        try:
            beautiful_soup_html = self.__get_js_soup()
            return self.__remove_script(beautiful_soup_html)
        except Exception as exc:
            print(f"Ignoring extracting URL {self.url}. Exception occured = {exc}")
            return None

    def get_html_from_url(self, base_url):
        """
        Get HTML from any url.
        :return: beautiful soup html.
        """
        try:
            self.url = base_url
            beautiful_soup_html = self.__get_js_soup()
            return self.__remove_script(beautiful_soup_html)
        except Exception as exc:
            print(f"Ignoring extracting URL {base_url}. Exception occured = {exc}")
            return None

    def __get_js_soup(self):
        """
        Get JS Soup using Selenium Webdriver with Chromedrivermanager
        :param base_url: any valid url.
        :return: Beautifulsoup from the html.
        """
        self.driver.get(self.url)
        self.html = self.driver.execute_script('return document.body.innerHTML')
        return self.__build_soup()

    def get_all_page(self):
        """
        Using requests library to get html.
        :param base_url: Any valid url
        :return: Beautifulsoup from the html.
        """
        response = requests.get(self.url)
        self.html = response.text
        return self.__build_soup()

    def __build_soup(self):
        """
        Get Beautifulsoup from html parser.
        :param html: html content of a web page.
        :return:
        """
        soup = BeautifulSoup(self.html, 'html.parser')  # beautiful soup object to be used for parsing html content
        return soup

    def __remove_script(self, beautiful_soup_html):
        """
        Remove Script and Style tags from the html.
        :param beautiful_soup_html: the html of a web page
        :return: refined html.
        """
        if beautiful_soup_html:
            for script in beautiful_soup_html(["script", "style"]):
                script.decompose()
            return beautiful_soup_html
        return None

    def close_driver(self):
        """
        Close the selelnium driver.
        """
        self.driver.close()
