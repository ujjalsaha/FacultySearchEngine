import requests
import json
import urllib.parse
import os
import logging
from decouple import config

API_KEY = 'AIzaSyCCeZ68tJ1lbKNG6V2WN_M8vp2bxYh2XFc'
BASE_URL = 'https://maps.googleapis.com/maps/api/place/'

console_format = '%(name)s - %(levelname)s - %(message)s'
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, format=console_format)


class GoogleAPI:
    def __init__(self, place_name):
        """
        Init method to assign fields.
        :param fields: The JSON fieldtype
        """
        self.place_name = place_name
        self.place_id = None
        self.details_url = 'details/json?'
        self.logger = logging.getLogger('Crawler')
        self.__call__()

    def get_component(self, field_comp):
        """
        Get valid component from Google API.
        :return: JSON string of the address
        """
        url = self.__get_details_url__(field_comp)
        try:
            response = requests.get(url)
            response_json = json.loads(response.text)
            components = response_json['result'][field_comp]
        except Exception as exc:
            raise Exception("Error occurred while retrieving component : " + repr(exc))
        return components

    def __call__(self):
        url = 'findplacefromtext/json?'
        params = {'input': self.place_name, 'fields': 'place_id', 'key': API_KEY, 'inputtype': 'textquery'}
        req_url = BASE_URL + url + urllib.parse.urlencode(params)
        try:
            resp = self.__make_call__(req_url)
            if len(resp['candidates']) < 1:
                raise Exception("No matching PlaceId found")
            self.place_id = resp['candidates'][0]['place_id']
        except Exception as ex:
            self.logger.exception(ex.__cause__)
            raise Exception("Received error : " + repr(ex))

    def __get_details_url__(self, field):
        """
        Constructs the url for detail URL.
        :param field: The field name to query
        :return: detail url.
        """
        details_params = {'fields': field, 'key': API_KEY, 'place_id': self.place_id}
        url = BASE_URL + self.details_url + urllib.parse.urlencode(details_params)
        return url

    def __make_call__(self, url):
        """
        Do the get call for the given url
        :param url: the request url.
        :return: response in JSON.
        """
        try:
            response = requests.get(url)
            response_json = json.loads(response.text)
        except Exception as exc:
            self.logger.exception(exc.__cause__)
            raise Exception("Error occurred while calling Google API : " + repr(exc))
        return response_json
