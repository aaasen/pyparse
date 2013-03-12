
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

	def __init__(self, source):
		self.session = requests.Session()
		self.source = source

	'''returns a list of torrent objects containing only torrent urls'''
	def search(self, term, sort=None, category=None, page=0):
		if sort is None:
			sort = self.source.search["sort_codes"]["default"]

		if category is None:
			category = self.source.search["categories"]["default"]

		url = parse.translate_schema(self.source.search["schema"],
			{ "search_term" : term,
			"page_number" : page,
			"sort_code" : sort,
			"category" : category })

		# response = self.session.get(url)

		# with open('cache/search', 'r') as f:
		# 	f.write(_decode_unicode(response.text))

		# if response.status_code == requests.codes.ok:		
		
		with open('cache/search', 'r') as f:
			text = f.read()

		tree = etree.HTML(text)

		expression = GenericTranslator().css_to_xpath('a.detLink')

		links = tree.xpath(expression)
		links = map(lambda x: parse.get_tuple(x.items(), 'href'), links)
		links = map(lambda x: Torrent(x), links)

		return links
		
		# else:
			# return None

	def get_torrent(self, torrent):
		url = parse.translate_schema(self.source.torrent["schema"],
			{ "url" : torrent.url })

		# response = self.session.get(url)

		# with open('cache/torrent', 'w') as f:
		# 	f.write(_decode_unicode(response.text))

		# if response.status_code == requests.codes.ok:

		with open('cache/torrent', 'r') as f:
			text = f.read()

		tree = etree.HTML(text)

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
		# else:
		# 	return None

def _decode_unicode(string):
	if string is not None:
		return string.encode('ascii', 'ignore')
	return ''
