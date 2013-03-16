
import requests
from lxml import etree

import parser
from parser import Parser
from torrent import Torrent

from pprint import pprint

class BayAPI:
	source = None
	session = None

	def __init__(self, source):
		self.session = requests.Session()
		self.source = source

	'''returns a list of torrent objects containing only torrent urls'''
	def search(self, term, sort=None, category=None, page=None, fp=None):
		if sort is None:
			sort = self.source.search["sort_codes"]["default"]
			if sort == "none":
				sort = None

		if category is None:
			category = self.source.search["categories"]["default"]
			if category == "none":
				category = None

		if page is None:
			page = self.source.search["page_number"]["default"]
			if page == "none":
				page = None

		url = parser.translate_schema(self.source.search["schema"],
			{ "search_term" : term,
			"page_number" : page,
			"sort_code" : sort,
			"category" : category })

		# response = self.session.get(url)

		# with open('cache/search', 'r') as f:
		# 	f.write(_decode_unicode(response.text))

		# if response.status_code == requests.codes.ok:		
		
		with open(fp, 'r') as f:
			text = f.read()

		tree = etree.HTML(text)

		links = Parser(tree, self.source.search["parser"]).extract(first=False)
		links = map(lambda x: Torrent(x), links)

		return links
		
		# else:
			# return None

	def get_torrent(self, torrent, fp=None):
		url = parser.translate_schema(self.source.torrent["schema"],
			{ "url" : torrent.url })

		# response = self.session.get(url)

		# with open('cache/torrent', 'w') as f:
		# 	f.write(_decode_unicode(response.text))

		# if response.status_code == requests.codes.ok:

		with open(fp, 'r') as f:
			text = f.read()

		tree = etree.HTML(text)

		# torrent.date = Parser(tree, self.source.torrent["date"]).extract()
		torrent.description = Parser(tree, self.source.torrent["description"]).extract()
		torrent.seeders = Parser(tree, self.source.torrent["seeders"]).extract()
		torrent.leechers = Parser(tree, self.source.torrent["leechers"]).extract()

		return torrent
		# else:
		# 	return None

def _decode_unicode(string):
	if string is not None:
		return string.encode('ascii', 'ignore')
	return ''
