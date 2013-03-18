
import requests
from lxml import etree

import parser
from parser import Parser
from torrent import Torrent
import getter
import util

from pprint import pprint

UPDATE_CACHE = False

class BayAPI:
	source = None
	session = None

	def __init__(self, source):
		self.session = requests.Session()
		self.source = source

	'''returns a list of torrent objects containing only torrent urls'''
	def search(self, term, sort=None, category=None, page=None):
		sort = parser.fill_none(self.source.search["sort_codes"], sort)
		category = parser.fill_none(self.source.search["categories"], category)
		page = parser.fill_none(self.source.search["page_number"], page)

		url = parser.translate_schema(self.source.search["schema"],
			{ "search_term" : term,
			"page_number" : page,
			"sort_code" : sort,
			"category" : category })

		response = getter.get(self.session, url, headers=self.source.info['headers'], update_cache=UPDATE_CACHE)

		if response.status_code == requests.codes.ok:		
			tree = etree.HTML(response.text)

			links = Parser(tree, self.source.search["parser"]).extract(first=False)
			torrents = map(lambda x: Torrent(x), links)

			return torrents
		else:
			raise util.HTTPError(url, response.status_code)

	def get_torrent(self, torrent):
		url = parser.translate_schema(self.source.torrent["schema"],
			{ "url" : torrent.url })

		response = getter.get(self.session, url, headers=self.source.info['headers'], update_cache=UPDATE_CACHE)

		if response.status_code == requests.codes.ok:
			tree = etree.HTML(response.text)

			# torrent.date = Parser(tree, self.source.torrent["date"]).extract()
			torrent.description = Parser(tree, self.source.torrent["description"]).extract()
			torrent.seeders = Parser(tree, self.source.torrent["seeders"]).extract()
			torrent.leechers = Parser(tree, self.source.torrent["leechers"]).extract()
			torrent.magnet = Parser(tree, self.source.torrent["magnet"]).extract()

			return torrent
		else:
			raise util.HTTPError(url, response.status_code)

	def get_torrents(self, torrents):
		return map(lambda torrent: self.get_torrent(torrent), torrents)
