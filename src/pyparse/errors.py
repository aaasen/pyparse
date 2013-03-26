
class LoadError(Exception):
	"""Raised when loading parsers in unsupported formats.

	Attributes:
		file_name -- name of the file in which the exception occured
		message -- explanation of the error
	"""

	def __init__(self, file_name, message):
		self.file_name = file_name
		self.message = message

	def __str__(self):
		return 'error while parsing \'%s\': %s' % (self.file_name, self.message)

class SchemaError(Exception):
	"""Raised when parsing incorrect schema.

	Attributes:
		schema -- given schema
		expected -- required keys
		actual -- actual keys
	"""

	def __init__(self, schema, expected, actual):
		self.schema = schema
		self.expected = expected
		self.actual = actual

	def __str__(self):
		return 'error while parsing schema \'%s\',\n\texpected: %s\n\tbut only got: %s' % \
			(self.schema, str(self.expected), str(self.actual))

class ParseMethodError(Exception):
	"""Raised when an unsupported parsing method is specified.

	Attributes:
		method -- method specified
	"""

	def __init__(self, method):
		self.method = method

	def __str__(self):
		return '\'%s\' is not a supported parsing method' % self.method

class FetchError(Exception):
	"""Raised when an request returns an invalid status code.

	Attributes:
		url -- url that triggered the error
		status_code -- bad status code
	"""

	def __init__(self, url, status_code):
		self.url = url
		self.status_code = status_code

	def __str__(self):
		return '\'%s\' returned invalid status code %s' %\
			(self.url, self.status_code)
