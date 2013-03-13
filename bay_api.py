
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

		links = parse.parse(tree, self.source.search["parser"], first=False)
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

		torrent.date = parse.parse(tree, self.source.torrent["date"])
		torrent.description = parse.parse(tree, self.source.torrent["description"])
		torrent.seeders = parse.parse(tree, self.source.torrent["seeders"])
		torrent.leechers = parse.parse(tree, self.source.torrent["leechers"])

		return torrent
		# else:
		# 	return None

def _decode_unicode(string):
	if string is not None:
		return string.encode('ascii', 'ignore')
	return ''
