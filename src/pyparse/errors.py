
class LoadError(Exception):
	"""Exception raised when loading parsers.

	Attributes:
		file_name -- name of the file in which the exception occured
		message -- explanation of the error
	"""

	def __init__(self, file_name, message):
		self.file_name = file_name
		self.message = message

	def __str__(self):
		return 'error while parsing \'%s\': %s' % (self.file_name, self.message)
