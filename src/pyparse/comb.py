
import requests
from lxml import etree

import parser
from parser import Parser
from source import Source
import cacher
from errors import FetchError

from pprint import pprint

class Comb:
	def __init__(self, source):
		self.session = requests.Session()
		self.source = Source(source)
		self.parsers = []

	def _get_tree(self, url):
		response = cacher.get(self.session, url)

		if response.status_code == requests.codes.ok:
			return etree.HTML(response.text)
		else:
			raise FetchError(data['fetch']['url'], response.status_code)

	def load(self, parser, tree=None):
		if 'fetch' in parser:
			tree = self._get_tree(parser['fetch']['url'])

		if tree is None:
			# raise an exception
			pass
		else:
			self.parsers.append(Parser(tree, parser))
		if 'parsers' in parser:
			for child in parser['parsers']:
				self.load(parser[child], tree)
