
import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

import re

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
