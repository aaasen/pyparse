
import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

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

