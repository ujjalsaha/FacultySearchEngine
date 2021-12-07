import string

import nltk
from nltk.tag.stanford import StanfordNERTagger
import sys, os
import re
import random
import json

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'lib'))
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'apps'))
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'data'))

from apps.frontend.utils.beautiful_soup import get_js_soup, remove_script, close_driver
from apps.frontend.crawler.crawler import build_url
from apps.backend.utils.document import Document
from apps.backend.utils.facultydb import FacultyDB

st = StanfordNERTagger('../../../lib/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz',
                       '../../../lib/stanford-ner-2020-11-17/stanford-ner.jar')


def random_str_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def __do_db_call__(faculty_list):
    try:
        faculty_db = FacultyDB()
        faculty_db.add_records(faculty_list)
        print("BIODATA RECORDS:    ", faculty_db.get_biodata_records())
    except Exception as exc:
        raise Exception(" Database error occurred = {}".format(exc))


class ScrapeFacultyWebPage:
    def __init__(self, faculty_dict):
        self.faculty_dict = faculty_dict
        self.dept_url = self.faculty_dict.get('dept_url')
        self.base_url = self.faculty_dict.get('base_url')
        self.faculty_link = self.faculty_dict.get('faculty_link')
        self.faculty_link_soup = self.faculty_dict.get('faculty_link_soup')
        self.faculty_urls = []
        self.all_faculty_text = ''
        self.sanitized_list = []

    def get_faculty_urls(self):
        all_a_tags = list()
        # TODO - add more here
        div_class = ['content', 'container']
        if not self.faculty_link_soup:
            self.faculty_link_soup = remove_script(get_js_soup(self.faculty_link))
        unique_href = set()
        for cls in div_class:
            div_lst = self.__find_div__('class', cls)
            div_lst.extend(self.__find_div__('id', cls))
            all_a_tags.extend(self.__build_a_tags__(div_lst, unique_href))

        for tag in all_a_tags:
            # print('tag  => ', tag)
            tag_text = tag.text.strip()
            if tag_text:
                # print('text inside a tag => ', tag_text)
                self.all_faculty_text += tag_text + ' ~ '
        # print('all text ', self.all_faculty_text)
        self.__check_name__()
        # print('sanitized list ', self.sanitized_list)
        for tag in all_a_tags:
            link = tag["href"]
            tag_text = tag.text.strip()
            tag_text = re.sub("[^a-zA-Z0-9]+", "", tag_text)
            for name in self.sanitized_list:
                if name == tag_text and len(name):
                    faculty_link = build_url(link, self.dept_url)
                    self.faculty_urls.append(faculty_link)
                    break
        headers = ['uni_url', 'dept_url', 'faculty_url', 'bio']
        # fileName = '../../../data/' + random_str_generator() + '_bio.txt'
        # with open(fileName, mode='w+', encoding='utf-8') as temp_file:
        #     for url in self.faculty_urls:
        #         bio_texts = self.get_bio(url)
        #         temp_file.write(bio_texts)
        #         temp_file.write("\n")
        bio_dict = dict()
        for url in self.faculty_urls:
            bio_texts = self.get_bio(url)
            bio_dict[url] = bio_texts
        # process the document
        self.process_document(bio_dict)
        close_driver()

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

    def __check_name__(self):
        print('-' * 20, 'Started NLTK validation for human names ', '-' * 20)
        for token in nltk.sent_tokenize(self.all_faculty_text):
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
        faculty_bio_soup = remove_script(get_js_soup(url))
        div_class = ['content', 'container']
        unique_href = set()
        all_texts = []
        for cls in div_class:
            elements = faculty_bio_soup.find_all(class_=cls)
            if not len(elements):
                elements = faculty_bio_soup.find_all(id=cls)
            for elem in elements:
                all_texts.extend(s.strip() for s in elem.strings if s.strip())

        return " ".join(all_texts)

    def process_document(self, bio_dict):
        faculty_dict_list = []
        file_data = None
        file_line_list = []
        count = 10
        print(file_line_list)
        for url in self.faculty_urls:
            bio = bio_dict.get(url)
            doc = Document(
                doc=bio,
                faculty_url=url,
                department_url=self.dept_url,
                university_url=self.base_url
            )
            faculty_dict['faculty_name'] = doc.extract_name()
            faculty_dict['faculty_department_name'] = doc.extract_department()
            faculty_dict['faculty_university_name'] = doc.extract_university()
            faculty_dict['faculty_phone'] = doc.extract_phone()
            faculty_dict['faculty_email'] = doc.extract_email()
            faculty_dict['faculty_expertise'] = doc.extract_expertise()
            faculty_dict['faculty_homepage_url'] = url
            faculty_dict['faculty_department_url'] = self.dept_url
            faculty_dict['faculty_university_url'] = self.base_url
            faculty_dict['faculty_biodata'] = bio
            faculty_dict['faculty_location'] = doc.extract_location()
            faculty_dict_list.append(faculty_dict)

        print(__file__, ":: faculty_dict_list: ", faculty_dict_list)
        faculty_list_json = json.dumps(faculty_dict_list)
        __do_db_call__(faculty_dict_list)


if __name__ == '__main__':
    faculty_dict = {
        'dept_url': "https://cs.indiana.edu/",
        'faculty_link': "https://cs.indiana.edu/faculty-directory/index.html?&type=2&aca_dept=1&alpha=asc",
        'base_url': "https://www.indiana.edu/",
    }
    scrapper = ScrapeFacultyWebPage(faculty_dict=faculty_dict)
    scrapper.get_faculty_urls()
    print('total faculty page found = ', len(scrapper.faculty_urls))
