import nltk
import re
import urllib
import sys
import logging
import requests
import tldextract
from nltk.tag.stanford import StanfordNERTagger

import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'lib'))
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'apps'))

from apps.frontend.utils.beautiful_soup import get_js_soup, remove_script, tag_visible




class ScrapeFacultyWebPage:
    def __init__(self, faculty_dict):
        self.faculty_dict = faculty_dict
        self.dept_url = self.faculty_dict.get('dept_url')
        self.base_url = self.faculty_dict.get('base_url')
        self.faculty_link = self.faculty_dict.get('faculty_link')
        self.faculty_link_soup = self.faculty_dict.get('faculty_link_soup')
        self.faculty_urls = []

    def get_faculty_urls(self):
        all_a_tags = []
        # TODO - add more here
    #     div_class = ['content', 'container']
    #     for div in self.faculty_link_soup.findAl(
    #             lambda tag: tag.name == "div" and ('content' in tag.class or 'container' in tag.class)):
    #
    #
    #     for cls in div_class:
    #         find_all_divs =
    #         for div in find_all_divs:
    #             a_tags = find_all_divs.findChildren("a", recursive=False)
    #             all_a_tags.append(tag for tag in a_tags)
    #
    #     for tag in all_a_tags:
    #         faculty_js_soup = get_js_soup(tag.)
    #
    # def validate_url(self):


# st = StanfordNERTagger('lib/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz', 'lib/stanford-ner-2020-11-17/stanford-ner.jar')
# text = 'Caltech Electrical Engineering | Yaser S. Abu-Mostafa'
#
# for sent in nltk.sent_tokenize(text):
#     tokens = nltk.tokenize.word_tokenize(sent)
#     tags = st.tag(tokens)
#     for tag in tags:
#         if tag[1]=='PERSON': print (tag)


