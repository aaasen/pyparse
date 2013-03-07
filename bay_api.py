
import requests
import itertools

class BayAPI:
	base_url = 'http://thepiratebay.se'

	def __get__(self, path=[], params={}):
		path = map(lambda x: str(x), path)

		path_string = '/'.join(path)

		return self.session.get(self.base_url + ('/' if len(path) > 0 else '') + path_string, params=params)

	def __init__(self):
		self.session = requests.Session()

	def search(self, term, sort=0, pages=1):
		return self.__get__(['search', term, 0, 7, 0])
