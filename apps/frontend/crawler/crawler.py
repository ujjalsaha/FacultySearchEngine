import logging
import os
import sys
import requests
import tldextract
from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'lib'))
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'apps'))

from apps.backend.api.googleapi import GoogleAPI

options = Options()
options.headless = True
driver = webdriver.Chrome('lib/chromedriver', options=options)

console_format = '%(name)s - %(levelname)s - %(message)s'
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, format=console_format)


def get_js_soup(url):
    driver.get(url)
    res_html = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html, 'html.parser')  # beautiful soup object to be used for parsing html content
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


class Crawler:
    """
    This class crawls the faculty pages.
    """

    def __init__(self, base_url=None):
        self.base_url = base_url
        self.key_words = self.get_key_words()
        self.faculty_links = []
        self.logger = logging.getLogger('Crawler')
        self.return_dict = {}
        self.return_dict['dept_url'] = base_url

    def get_base_url(self):
        """
        Get the base URL using tldextract library.
        :return:None
        """
        extractURL = tldextract.extract(self.base_url)
        uni_url = "https://www." + extractURL.domain + "." + extractURL.suffix
        self.return_dict['base_url'] = uni_url

    def get_key_words(self):
        """
        Get key words for the faculty url
        :return: list of keywords from keywords.txt file
        """
        try:
            with open("lib/keywords.txt") as fileName:
                keywords = fileName.readlines()
                keywords = [line.rstrip() for line in keywords]
            return keywords
        finally:
            return ['faculty', 'all-faculty']

    def scrape_dir_page(self):
        """
        Scraping the Faculty URL page
        :return: Final URL and the JS Soup
        """
        self.logger.info('Scraping directory page')
        base_page_soup = remove_script(get_js_soup(self.base_url))
        faculty_pages = set()
        for faculty in base_page_soup.findAll(
                lambda tag: tag.name == "a" and ("Faculty" in tag.text or "People" in tag.text)):
            link = faculty['href']
            if link not in faculty_pages and \
                    any(keyword in link for keyword in self.get_key_words()):
                faculty_pages.add(link)
                url = self.base_url
                last_index_slash = url.rfind('/')
                url = url[:last_index_slash] if last_index_slash == len(url) - 1 else url
                faculty_link = None
                if link.startswith('https:') or link.startswith('//') or link.startswith('http:'):
                    link = link.replace('//', 'https://') if link.startswith('//') else link
                    link = link.replace('http:', 'https:')
                    faculty_link = link
                elif link.startswith('/'):
                    faculty_link = url + link
                else:
                    faculty_link = url + '/' + link
                self.faculty_links.append(faculty_link)
        self.get_faculty_dir_page()
        self.get_base_url()

    def get_faculty_dir_page(self):
        """
        Given a list of Faculty Links, returns the valid faculty URL.
        :param faculty_links: A list of URLs
        :return: valid link
        """
        final_link = None
        final_link_js_soup = None
        if len(self.faculty_links) > 0:
            max_count = 0
            for url in self.faculty_links:
                if url.endswith('/faculty'):
                    final_link = url
                    break
                # print('url in max count => ', url)
                faculty_link_soup = remove_script(get_js_soup(url))
                faculty_page_html = faculty_link_soup.find_all(text=True)
                visible_texts = filter(tag_visible, faculty_page_html)
                faculty_count = 0
                for text in visible_texts:
                    if 'PROFESSOR' in text.upper() or 'LECTURER' in text.upper():
                        faculty_count += 1
                if faculty_count >= max_count and faculty_count > 0:
                    max_count = faculty_count
                    final_link = url
                    final_link_js_soup = faculty_link_soup
                # print('max_count => ', max_count)
                # print('current faculty count  => ', faculty_count)
        # elif len(self.faculty_links) > 0:
        #     final_link = self.faculty_links[0]
        #     final_link_js_soup = remove_script(get_js_soup(final_link))
        self.logger.info('Found faculty url as => %s', final_link)
        self.return_dict['faculty_link'] = final_link
        self.return_dict['faculty_link_soup'] = final_link_js_soup

    def valid_faculty_page_found(self):
        """
        Given a URL it validates whether the faculty Link exists
        :return:
        """
        response = requests.get(self.base_url)
        if response.status_code > 200:
            return False
        self.scrape_dir_page()
        if self.return_dict.get("faculty_link"):
            return True
        return False


class ExtractFacultyURL:
    """
    Class to extract the Faculty URL from the crawler class.
    This class should be imported.
    """

    def __init__(self, uni_name=None):
        self.uni_name = uni_name
        self.log = logging.getLogger('Extract_Faculty_URL')
        self.base_url = self.get_base_url()
        self.crawler = None
        if self.base_url:
            self.crawler = Crawler(base_url=self.base_url)

    def get_base_url(self):
        """
        Get base url from Google API university name
        :return: Base URL
        """
        if self.uni_name:
            try:
                googleAPI = GoogleAPI(place_name=self.uni_name)
                return googleAPI.get_component(field_comp='website')
            except Exception as ex:
                self.log.error(ex)
        return None

    def get_faculty_link(self):
        """
        Get the Dictionary from the crawler.
        :return: A dictionary with faculty url, base url, dept url and faculty page soup.
        """
        if self.crawler:
            faculty_link_dict = self.crawler.return_dict
            return faculty_link_dict
        return {}

    def has_valid_faculty_link(self):
        """
        Returns whether a valid faculty page found or not
        :return: Boolean.
        """
        found = False
        if self.crawler:
            found = self.crawler.valid_faculty_page_found()
        return found


if __name__ == '__main__':
    uni = sys.argv[1]
    print(uni)
    extractURL = ExtractFacultyURL(uni)
    print('Faculty Page found = ', extractURL.has_valid_faculty_link())
    print('faculty_link = ', extractURL.get_faculty_link().get('faculty_link'))
