
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

		expression = GenericTranslator().css_to_xpath(self.source.search["parser"]["selector"])

		links = tree.xpath(expression)
		links = map(lambda x: parse.get_attr(x, self.source.search["parser"]["attr"]), links)
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

		expression = GenericTranslator().css_to_xpath(self.source.torrent["description"]["selector"])
		description = tree.xpath(expression)
		torrent.description = parse.get_attr(description[0], self.source.torrent["description"]["attr"])


		expression = GenericTranslator().css_to_xpath('dl.col1,dl.col2')

		col2 = tree.xpath(expression)

		tags = col2[0].iter(tag='dt')
		data = col2[0].iter(tag='dd')

		tags = map(lambda x: x.text, tags)
		data = map(lambda x: x.text, data)

		zipped = zip(tags, data)

		expression = GenericTranslator().css_to_xpath('dl.col1,dl.col2 > dd')
		description = tree.xpath(expression)


		xp = etree.XPath(self.source.torrent["seeders"]["xpath"], namespaces=self.source.torrent["seeders"]["namespaces"])
		torrent.seeders = parse.get_attr(xp(tree)[0], self.source.torrent["seeders"]["attr"])

		xp = etree.XPath(self.source.torrent["leechers"]["xpath"], namespaces=self.source.torrent["leechers"]["namespaces"])
		torrent.leechers = parse.get_attr(xp(tree)[0], self.source.torrent["leechers"]["attr"])

		xp = etree.XPath(self.source.torrent["date"]["xpath"], namespaces=self.source.torrent["date"]["namespaces"])
		date = parse.get_attr(xp(tree)[0], self.source.torrent["date"]["attr"])
		torrent.date = time.strptime(date, self.source.torrent["date"]["format"])

		return torrent
		# else:
		# 	return None

def _decode_unicode(string):
	if string is not None:
		return string.encode('ascii', 'ignore')
	return ''
