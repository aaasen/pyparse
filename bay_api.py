
import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

import itertools

import parse
from torrent import Torrent

class BayAPI:
	base_url = 'http://thepiratebay.se'

	sort_codes = { 
		'default' : 0,
		'date' : 3,
		'size' : 5,
		'seeders' : 7,
		'leechers' : 8,
		'uploader' : 11 
	}

	def __get__(self, path=[], params={}):
		path = map(lambda x: str(x), path)

		path_string = '/'.join(path)

		return self.session.get(self.base_url + ('/' if len(path) > 0 else '') + path_string, params=params)

	def __init__(self):
		self.session = requests.Session()

	def search(self, term, sort=sort_codes['seeders'], page=0):
		response = self.__get__(['search', term, page, sort, 0])

		if response.status_code == requests.codes.ok:		
			tree = etree.HTML(response.text)

			expression = GenericTranslator().css_to_xpath('a.detLink')

			links = tree.xpath(expression)
			links = map(lambda x: parse.get_tuple(x.items(), 'href'), links)
			links = map(lambda x: Torrent(x), links)

			return links
		else:
			return None
