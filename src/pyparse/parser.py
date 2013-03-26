
import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

import re
import time

from errors import SchemaError
from errors import ParseMethodError

class Parser:
	parser = None
	tree = None

	def _get_attr(self, el):
		if self.parser["attr"] == 'text':
			return reduce(lambda x, y: x + y, el.itertext())
		else:
			return el.get(self.parser["attr"])

	def _expression(self):
		if self.parser["method"] == "xpath":
			return etree.XPath(self.parser["xpath"], namespaces=self.parser["namespaces"])
		elif self.parser["method"] == "css":
			return GenericTranslator().css_to_xpath(self.parser["selector"])
		else:
			raise ParseMethodError(self.parser["method"])

	def _execute(self, expression):
		if self.parser["method"] == "xpath":
			result = expression(self.tree)
		elif self.parser["method"] == "css":
			result = self.tree.xpath(expression)
		else:
			raise ParseMethodError(self.parser["method"])
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
	keys = re.findall('(\<.*?(\[\[(.+?)\]\]).*?\>)', schema)

	for key in keys:
		try:
			if kv[key[2]] is None:
				schema = schema.replace(key[0], '')
			else:
				el = key[0]
				el = el.replace('<', '').replace('>', '')
				el = el.replace(str(key[1]), str(kv[key[2]]))
				schema = schema.replace(key[0], el)
		except KeyError:
			raise SchemaError(schema, map(lambda x: x[2], keys), kv.keys())

	return schema

def fill_none(kv, field, default='default', eval_default=True):
	if field is None:
		field = kv[default]
		if eval_default and field == 'none':
			field = None
	return field
