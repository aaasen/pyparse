
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

	def _url_join(self, el):
		el = map(lambda x: str(x), el)
		return '/'.join(el)

	def _get(self, path='', params={}, url=base_url):
		return self.session.get(url + ('/' if path and path[0] != '/' else '') + path, params=params)

	def __init__(self):
		self.session = requests.Session()

	def search(self, term, sort=sort_codes['seeders'], page=0):
		response = self._get(self._url_join(['search', term, page, sort, 0]))

		if response.status_code == requests.codes.ok:		
			tree = etree.HTML(response.text)

			expression = GenericTranslator().css_to_xpath('a.detLink')

			links = tree.xpath(expression)
			links = map(lambda x: parse.get_tuple(x.items(), 'href'), links)
			links = map(lambda x: Torrent(x), links)

			return links
		else:
			return None

	def get_torrent(self, path, torrent=None):
		response = self._get(path)

		if response.status_code == requests.codes.ok:
			if (torrent == None):
				torrent = Torrent(path)

			tree = etree.HTML(response.text)

			torrent.description = torrent.get_description(tree)

			return torrent
		else:
			return None
