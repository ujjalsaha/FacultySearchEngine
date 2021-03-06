import nltk
from nltk.tag.stanford import StanfordNERTagger
import sys, os
import re
import json
import httplib2
import logging

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'lib'))
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'apps'))
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'data'))

logging.basicConfig(filename='expertsearch.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from apps.frontend.utils.beautiful_soup import BeautifulSoupLocal, html_tag_visible
from apps.frontend.crawler.crawler import build_url
from apps.backend.utils.document import Document
from apps.backend.utils.facultydb import FacultyDB

dirname = os.path.dirname(__file__)
model_file = os.path.join(dirname,
                          '../../../lib/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz')
jar_file = os.path.join(dirname, '../../../lib/stanford-ner-2020-11-17/stanford-ner.jar')

st = StanfordNERTagger(model_file, jar_file, encoding='utf-8')


def validate_url(url):
    h = httplib2.Http()
    resp = h.request(url, 'HEAD')
    return int(resp[0]['status']) < 400


def do_db_call(faculty_list):
    try:
        faculty_db = FacultyDB()
        faculty_db.add_records(faculty_list)
    except Exception as exc:
        print(" Database error occurred = {}".format(exc))


class ScrapeFacultyWebPage:
    def __init__(self, faculty_dict=None):
        self.faculty_dict = faculty_dict
        self.dept_url = self.faculty_dict.get('dept_url')
        self.base_url = self.faculty_dict.get('base_url')
        self.faculty_link = self.faculty_dict.get('faculty_link')
        self.beautiful_soup = BeautifulSoupLocal(url=self.faculty_link)
        self.faculty_link_soup = None
        self.faculty_urls = []
        self.sanitized_list = []
        self.faculty_link_dict = dict()

    def get_faculty_urls(self):
        """
        Get all faculty Urls and inserts them into a database.
        :return:
        """
        if not self.faculty_link_soup:
            self.faculty_link_soup = self.beautiful_soup.get_html()
        if not self.faculty_link_soup:
            return None
        all_faculty_text, all_tag_name_dict = self.__get_all_faculty_text()
        from datetime import datetime
        self.__check_name__(all_faculty_text)
        for name in self.sanitized_list:
            if all_tag_name_dict.get(name):
                link = all_tag_name_dict.get(name)
                faculty_profile_link = build_url(link, self.dept_url)
                start2 = datetime.now()
                validate = validate_url(faculty_profile_link)
                if validate:
                    self.faculty_urls.append(faculty_profile_link)
                    self.faculty_link_dict[faculty_profile_link] = name
                else:
                    faculty_profile_link = build_url(link, self.faculty_link)
                    if validate_url(faculty_profile_link):
                        self.faculty_urls.append(faculty_profile_link)
                        self.faculty_link_dict[faculty_profile_link] = name
        bio_dict = dict()
        n = len(self.faculty_urls)
        for i, url in enumerate(self.faculty_urls):
            print(f"Processing Faculty Url: {i + 1} / {n}")
            try:
                bio_texts = self.get_bio(url)
                bio_dict[url] = bio_texts
            except:
                pass

        # process the document
        self.process_document(bio_dict)

    def __get_all_faculty_text(self):
        all_a_tags = list()
        div_class = ['content', 'container', 'directory']
        unique_href = set()
        all_faculty_text = ''
        all_tag_name_dict = dict()

        for cls in div_class:
            div_lst = self.__find_div__('class', cls)
            div_lst.extend(self.__find_div__('id', cls))
            all_a_tags.extend(self.__build_a_tags__(div_lst, unique_href))

        for tag in all_a_tags:
            # print('tag  => ', tag)
            tag_text = tag.text.strip()
            if tag_text:
                # print('text inside a tag => ', tag_text)
                all_faculty_text += tag_text + ' ~ '
                link = tag["href"]
                tag_text = tag_text.strip()
                tag_text = re.sub("[^a-zA-Z0-9]+", "", tag_text)
                all_tag_name_dict[tag_text] = link
        return all_faculty_text, all_tag_name_dict

    def __build_a_tags__(self, div_tag_lst, unique_href):
        for div in div_tag_lst:
            a_tags = div.find_all("a")
            for tag in a_tags:
                href = tag.get("href")
                if href and 'mailto:' not in href and 'tel:' not in href and tag not in unique_href:
                    unique_href.add(tag)
                    yield tag

    def __find_div__(self, attr_to_search, text):
        return self.faculty_link_soup.find_all("div", recursive=True, attrs={attr_to_search: re.compile(text)})

    def __check_name__(self, all_faculty_text):
        print(f"{'*' * 50}")
        print('Started NLTK validation for human names ')
        tokenize = nltk.sent_tokenize(all_faculty_text)
        n = len(tokenize)
        for i, token in enumerate(tokenize):
            tokens = nltk.tokenize.word_tokenize(token)
            tags = st.tag(tokens)
            full_name = ''
            for tag in tags:
                # print('tag inside validate method ', tag)
                if tag[1] == 'PERSON':
                    full_name += tag[0]
                if tag[0] == '~':
                    full_name = re.sub("[^a-zA-Z0-9]+", "", full_name)
                    if len(full_name):
                        self.sanitized_list.append(full_name)
                    full_name = ''

    def get_bio(self, url):
        faculty_bio_soup = self.beautiful_soup.get_html_from_url(url)
        faculty_page_html = faculty_bio_soup.find_all(text=True)
        visible_texts = filter(html_tag_visible, faculty_page_html)
        return " ".join(visible_texts)

        # faculty_bio_soup = self.beautiful_soup.get_html_from_url(url)
        # div_class = ['content', 'container']
        # all_texts = []
        # for cls in div_class:
        #     elements = faculty_bio_soup.find_all(class_=cls)
        #     if not len(elements):
        #         elements = faculty_bio_soup.find_all(id=cls)
        #     for elem in elements:
        #         all_texts.extend(s.strip() for s in elem.strings if s.strip())
        #
        # return " ".join(all_texts)

    def close_driver(self):
        """
        Close the Selenium Driver
        :return:
        """
        self.beautiful_soup.close_driver()

    def process_document(self, bio_dict):
        faculty_dict_list = []
        n = len(self.faculty_urls)
        for i, url in enumerate(self.faculty_urls):
            print(f"Processing Faculty: {i + 1} / {n}")
            print(f"Base URL (University URL): {self.base_url}")
            print(f"Department URL: {self.dept_url}")
            print(f"Faculty URL: {url}")
            try:
                faculty_dict = dict()
                bio = bio_dict.get(url)
                name = self.faculty_link_dict.get(url)
                faculty_dict['faculty_name'] = " ".join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', name))
                bio = bio if bio else faculty_dict['faculty_name']
                doc = Document(
                    doc=bio,
                    faculty_url=url,
                    department_url=self.dept_url,
                    university_url=self.base_url
                )
                faculty_dict['faculty_department_name'] = doc.extract_department()
                faculty_dict['faculty_university_name'] = doc.extract_university()
                faculty_dict['faculty_phone'] = doc.extract_phone()
                faculty_dict['faculty_email'] = doc.extract_email()
                faculty_dict['faculty_expertise'] = doc.extract_expertise()
                faculty_dict['faculty_homepage_url'] = url
                faculty_dict['faculty_department_url'] = self.dept_url
                faculty_dict['faculty_university_url'] = self.base_url
                faculty_dict['faculty_biodata'] = doc.extract_biodata()
                faculty_dict['faculty_location'] = doc.extract_location()
                faculty_dict_list.append(faculty_dict)
            except Exception as e:
                print(f"(IGNORING) Exception encountered for Faculty URL: {url}", "\n", str(e))
                pass

            print(f"{'*' * 50}")

        print(__file__, ":: faculty_dict_list: ")
        faculty_list_json = json.dumps(faculty_dict_list)
        do_db_call(faculty_dict_list)


if __name__ == '__main__':
    faculty_dict = {'dept_url': 'http://web.cs.dartmouth.edu',
                    'faculty_link': 'https://web.cs.dartmouth.edu/people',
                    'base_url': 'https://www.dartmouth.edu'}
    scrapper = ScrapeFacultyWebPage(faculty_dict=faculty_dict)
    scrapper.get_faculty_urls()
    print('total faculty page found = ', len(scrapper.faculty_urls))
