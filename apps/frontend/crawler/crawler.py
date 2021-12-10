import logging
import os
import sys
import requests
import tldextract

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'lib'))
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'apps'))

from apps.backend.api.googleapi import GoogleAPI
from apps.frontend.utils.beautiful_soup import BeautifulSoupLocal, html_tag_visible

console_format = '%(name)s - %(levelname)s - %(message)s'
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, format=console_format)
dirname = os.path.dirname(__file__)
keywords_file_path = os.path.join(dirname, '../../../lib/keywords.txt')


def build_url(link, url):
    faculty_link = requests.compat.urljoin(url, link)
    # last_index_slash = url.rfind('/')
    # url = url[:last_index_slash] if last_index_slash == len(url) - 1 else url
    # print('url ==> ', url)
    # print('link ==> ', link)
    # if link.startswith('https:') or link.startswith('//') or link.startswith('http:'):
    #     link = link.replace('//', 'https://') if link.startswith('//') else link
    #     link = link.replace('http:', 'https:')
    #     faculty_link = link
    # elif link.startswith('..'):
    #     link = link.replace('../', '/')
    #     faculty_link = url + link
    # elif link.startswith('/'):
    #     faculty_link = url + link
    # else:
    #     faculty_link = url + '/' + link

    return faculty_link


class Crawler:
    """
    This class crawls the faculty pages.
    """

    def __init__(self, base_url=None):
        self.extract = tldextract.extract(base_url)
        self.return_dict = dict()
        self.base_url = base_url
        self.beautiful_soup = BeautifulSoupLocal(url=self.base_url)
        self.key_words = self.get_key_words()
        self.faculty_links = []
        self.logger = logging.getLogger('Crawler')
        self.get_dept_url()

    def get_base_url(self):
        """
        Get the base URL using tldextract library.
        :return:None
        """
        uni_url = "https://www." + self.extract.domain + "." + self.extract.suffix
        self.return_dict['base_url'] = uni_url

    def get_dept_url(self):
        """
           Get the department URL using tldextract library.
           :return:None
       """
        index_of_slash = self.base_url.rfind("://")
        dept_url = self.base_url[
                   0:index_of_slash + 3] + self.extract.subdomain + "." + self.extract.domain + "." + self.extract.suffix
        self.return_dict['dept_url'] = dept_url
        return dept_url

    def get_key_words(self):
        """
        Get key words for the faculty url
        :return: list of keywords from keywords.txt file
        """
        keywords = ['faculty', 'all-faculty']
        try:
            with open(keywords_file_path) as fileName:
                keywords = fileName.readlines()
                keywords = [line.rstrip() for line in keywords]
        finally:
            return keywords

    def scrape_dir_page(self):
        """
        Scraping the Faculty URL page
        :return: Final URL and the JS Soup
        """
        self.logger.info('Scraping directory page')
        base_page_soup = self.beautiful_soup.get_html()
        if not base_page_soup:
            return None
        faculty_pages = set()
        for faculty in base_page_soup.findAll(
                lambda tag: tag.name == "a" and ("Faculty" in tag.text or "People" in tag.text)):
            link = faculty['href']
            if link not in faculty_pages and \
                    any(keyword in link for keyword in self.key_words):
                faculty_pages.add(link)
                faculty_link = build_url(link, self.base_url)
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
                # print('url in faculty_links => ', url)
                faculty_link_soup = self.beautiful_soup.get_html_from_url(url)
                if not faculty_link_soup:
                    continue
                # print(faculty_link_soup)
                faculty_page_html = faculty_link_soup.find_all(text=True)
                # print(faculty_page_html)
                visible_texts = filter(html_tag_visible, faculty_page_html)
                faculty_count = 0
                for text in visible_texts:
                    # print(f"{url} => {faculty_count} => {text}")
                    if 'PROFESSOR' in text.upper() or 'LECTURER' in text.upper():
                        faculty_count += 1

                if faculty_count >= max_count and faculty_count > 0:
                    max_count = faculty_count
                    final_link = url
                    final_link_js_soup = faculty_link_soup
        self.logger.info('Found faculty url as => %s', final_link)
        self.return_dict['faculty_link'] = final_link

    def valid_faculty_page_found(self):
        """
        Given a URL it validates whether the faculty Link exists
        :return:
        """
        try:
            response = requests.get(self.base_url)
            if response.status_code > 200:
                return False
            self.scrape_dir_page()
            if self.return_dict.get("faculty_link"):
                return True
        except Exception as exc:
            print(str(exc))
            pass
        return False

    def close_driver(self):
        """
        Close the Selenium Driver
        :return:
        """
        self.beautiful_soup.close_driver()


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
        base_url = None
        if self.uni_name:
            try:
                googleAPI = GoogleAPI(place_name=self.uni_name)
                base_url = googleAPI.get_component(field_comp='website')
                print('base url => ', base_url)
            except Exception as ex:
                self.log.error(ex)
        return base_url

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

    def close_driver(self):
        self.crawler.close_driver()


if __name__ == '__main__':
    uni = "rice university, computer science"
    print(uni)
    extractURL = ExtractFacultyURL(uni)
    print('Faculty Page found = ', extractURL.has_valid_faculty_link())
    print('faculty_link = ', extractURL.get_faculty_link())
