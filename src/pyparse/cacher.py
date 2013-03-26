
import requests

import util

_cache_directory = '../../cache/'

class _FakeResponse:
	def __init__(self, text, status_code):
		self.text = text
		self.status_code = status_code

def _get_cache_name(url):
	url = url.replace('http://', '')
	url = url.replace('/', '.')
	return _cache_directory + url

def _get_local(url):
	with open(_get_cache_name(url), 'r') as f:
		return _FakeResponse(f.read(), 200)

def _get_remote(session, url, headers={}):
	response = session.get(url, headers=headers)
	_update_cache(url, response.text)

	return response

def _update_cache(url, text):
	with open(_get_cache_name(url), 'w') as f:
		f.write(util.decode_unicode(text))

def get(session, url, headers={}, update_cache=False):
	if update_cache:
		return _get_remote(session, url, headers)
	try:
		return _get_local(url)
	except IOError:
		return _get_remote(session, url, headers)
