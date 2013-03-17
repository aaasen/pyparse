
class HTTPError(Exception):
	def __init__(self, value):
		self.value = value
	
	def __init__(self, url, status_code):
		self.value = '%s returned %s' % (str(url), str(status_code))

	def __str__(self):
		return repr(self.value)

class CacheError(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr('no cache entry for %s' % (self.value))	

def decode_unicode(string):
	if string is not None:
		return string.encode('ascii', 'ignore')
	return ''
