
import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

'''takes an array of tuples and returns the value of the tuple with the specified key'''
def get_tuple(tuples, key):
	return [v[1] for i, v in enumerate(tuples) if v[0] == key][0]
