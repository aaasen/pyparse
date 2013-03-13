
import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

import re
import time

from log import logger

class Parser:
	parser = None
	tree = None

	def _get_attr(self, el):
		if self.parser["attr"] == 'text':
			return el.text
		else:
			return el.get(self.parser["attr"])

	def _expression(self):
		if self.parser["method"] == "xpath":
			return etree.XPath(self.parser["xpath"], namespaces=self.parser["namespaces"])
		elif self.parser["method"] == "css":
			return GenericTranslator().css_to_xpath(self.parser["selector"])
		else:
			raise ValueError(self.parser["method"] + 'is not a recognized parsing method')

	def _execute(self, expression):
		if self.parser["method"] == "xpath":
			result = expression(self.tree)
		elif self.parser["method"] == "css":
			result = self.tree.xpath(expression)
		else:
			raise ValueError(self.parser["method"] + 'is not a recognized parsing method')
		return result if all else result[0]

	def _post_one(self, result):
		result = self._get_attr(result)

		try:
			result = time.strptime(result, self.parser["date-format"])
		except KeyError:
			pass

		return result

	def _post(self, results, first=True):
		if not first:
			return map(lambda x: self._post_one(x), results)
		else:
			return self._post_one(results[0])

	def extract(self, first=True):
		return self._post(self._execute(self._expression()), first=first)

	def __init__(self, tree, parser):
		self.tree = tree
		self.parser = parser

def translate_schema(schema, kv):
	keys = [el.group(1) for el in re.finditer('\[\[(.+?)\]\]', schema)]

	for key in keys:
		try:
			schema = schema.replace('[[' + key + ']]', str(kv[key]))
		except KeyError, e:
			logger.error("Error while parsing schema: not enough values\n\tgot: " + str(kv.keys()) + "\n\texpected: " + str(keys))

	return schema
