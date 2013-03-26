
def decode_unicode(string):
	if string is not None:
		return string.encode('ascii', 'ignore')
	return ''
