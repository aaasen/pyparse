
import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

import re
import time

from log import logger

'''takes an array of tuples and returns the value of the tuple with the specified key'''
def get_tuple(tuples, key):
	try:
		return [v[1] for i, v in enumerate(tuples) if v[0] == key][0]
	except IndexError, e:
		pass

def get_tuple_fuzzy(tuples, key):
	try:
		return [v[1] for i, v in enumerate(tuples) if (key.lower() in v[0].lower())][0]
	except IndexError, e:
		pass

def translate_schema(schema, kv):
	keys = [el.group(1) for el in re.finditer('\[\[(.+?)\]\]', schema)]

	for key in keys:
		try:
			schema = schema.replace('[[' + key + ']]', str(kv[key]))
		except KeyError, e:
			logger.error("Error while parsing schema: not enough values\n\tgot: " + str(kv.keys()) + "\n\texpected: " + str(keys))

	return schema

def get_attr(el, attr):
	if attr == 'text':
		return el.text
	else:
		return el.get(attr)

def _expression(parser):
	if parser["method"] == "xpath":
		return etree.XPath(parser["xpath"], namespaces=parser["namespaces"])
	elif parser["method"] == "css":
		return GenericTranslator().css_to_xpath(parser["selector"])
	else:
		raise ValueError(parser["method"] + 'is not a recognized parsing method')

def _execute(tree, expression, parser):
	if parser["method"] == "xpath":
		result = expression(tree)
	elif parser["method"] == "css":
		result = tree.xpath(expression)
	else:
		raise ValueError(parser["method"] + 'is not a recognized parsing method')
	return result if all else result[0]

def _post_one(result, parser):
	result = get_attr(result, parser["attr"])

	try:
		result = time.strptime(result, parser["date-format"])
	except KeyError:
		pass

	return result

def _post(results, parser, first=True):
	if not first:
		return map(lambda x: _post_one(x, parser), results)
	else:
		return _post_one(results[0], parser)

def parse(tree, parser, first=True):
	return _post(_execute(tree, _expression(parser), parser), parser, first=first)
