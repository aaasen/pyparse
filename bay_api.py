
import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

import itertools
import time

import parse
from torrent import Torrent
from fakebrowser import FakeBrowser
from source import Source
from log import logger

class BayAPI:
	source = None
	session = None

	def _url_join(self, el):
		el = map(lambda x: str(x), el)
		return '/'.join(el)

	def _prepend_base_url(self, path, url=None):
		if url is None:
			url = self.source.info['url']

		if url[-1] != '/' and path[0] != '/':
			url += '/'
		elif url[-1] == '/' and path[0] == '/':
			url = url[:-1]

		return url + path

	def _get(self, path='', params={}, url=None):
		return self.session.get(self._prepend_base_url(path), params=params)

	def __init__(self, source):
		self.session = requests.Session()
		self.source = source

	def search(self, term, sort, page=0):
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

	def get_torrent(self, torrent):
		response = self._get(torrent.url)

		if response.status_code == requests.codes.ok:
			tree = etree.HTML(response.text)

			torrent.description = torrent.get_description(tree)

			expression = GenericTranslator().css_to_xpath('dl.col1,dl.col2')

			col2 = tree.xpath(expression)

			tags = col2[0].iter(tag='dt')
			data = col2[0].iter(tag='dd')

			tags = map(lambda x: x.text, tags)
			data = map(lambda x: x.text, data)

			zipped = zip(tags, data)

			torrent.seeders = parse.get_tuple_fuzzy(zipped, 'seed')
			torrent.leechers = parse.get_tuple_fuzzy(zipped, 'leech')
			torrent.date = time.strptime(parse.get_tuple_fuzzy(zipped, 'uploaded'), "%Y-%m-%d %H:%M:%S GMT")

			return torrent
		else:
			return None

def _decode_unicode(string):
	if string is not None:
		return string.encode('ascii', 'ignore')
	return ''
