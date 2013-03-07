
import requests
import itertools

class BayAPI:
	base_url = 'http://thepiratebay.se'

	def __get__(self, path='/', params={}):
		if (path[0] != '/'):
			path = '/' + path

		# ['a', 'b'].join('/') -> 'a/b'

		return self.session.get(self.base_url + path, params=params)


	def __init__(self):
		self.session = requests.Session()

	def search(self, term, sort=0, pages=1):
		return self.__get__('/search/' + term + '/0/7/0')