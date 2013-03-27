
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

def load(data):
	if 'parsers' in data:
		names = data['parsers']

		parsers = map(lambda x: (x, data[x]), names)

		return map(lambda x: (x[0], load(x[1])), parsers)
	else:
		return data
