
import requests
from lxml import etree

import parser
from parser import Parser
from torrent import Torrent
from source import Source
import cacher
from errors import FetchError

from pprint import pprint

_update_cache = False

class GetTorrent:
	source = None
	session = None

	def __init__(self, source):
		self.session = requests.Session()
		self.source = Source(source)

	'''
	Returns a list of torrent objects containing only torrent urls.
	To fill these torrent objects, use get_torrent(self, torrent)
	or get_torrents(self, torrents) for multiple torrents
	'''
	def search(self, term, sort=None, category=None, page=None):
		sort = parser.fill_none(self.source.search["sort_codes"], sort)
		category = parser.fill_none(self.source.search["categories"], category)
		page = parser.fill_none(self.source.search["page_number"], page)

		url = parser.translate_schema(self.source.search["schema"],
			{ "search_term" : term,
			"page_number" : page,
			"sort_code" : sort,
			"category" : category })

		response = cacher.get(self.session, url, headers=self.source.info['headers'], update_cache=_update_cache)

		if response.status_code == requests.codes.ok:		
			tree = etree.HTML(response.text)

			urls = Parser(tree, self.source.search["url"]).extract(first=False)
			titles = Parser(tree, self.source.search["title"]).extract(first=False)
			magnets = Parser(tree, self.source.search["magnet"]).extract(first=False)
			seeders = Parser(tree, self.source.search["seeders"]).extract(first=False)
			leechers = Parser(tree, self.source.search["leechers"]).extract(first=False)

			torrents = zip(urls, titles, magnets, seeders, leechers)
			torrents = map(lambda x: Torrent(x[0], title=x[1], magnet=x[2], seeders=x[3], leechers=x[4]), torrents)

			return torrents
		else:
			raise FetchError(url, response.status_code)

	'''
	Fetches info like seeders, leechers, magnet, etc. for an individual torrent.
	'''
	def get_torrent(self, torrent):
		url = parser.translate_schema(self.source.torrent["schema"],
			{ "url" : torrent.url })

		response = cacher.get(self.session, url, headers=self.source.info['headers'], update_cache=_update_cache)

		if response.status_code == requests.codes.ok:
			tree = etree.HTML(response.text)

			# torrent.date = Parser(tree, self.source.torrent["date"]).extract()
			torrent.description = Parser(tree, self.source.torrent["description"]).extract()
			torrent.seeders = Parser(tree, self.source.torrent["seeders"]).extract()
			torrent.leechers = Parser(tree, self.source.torrent["leechers"]).extract()
			torrent.magnet = Parser(tree, self.source.torrent["magnet"]).extract()

			return torrent
		else:
			raise FetchError(url, response.status_code)

	'''
	Fetches data for multiple torrents using get_torrent().
	'''
	def get_torrents(self, torrents):
		return map(lambda torrent: self.get_torrent(torrent), torrents)
