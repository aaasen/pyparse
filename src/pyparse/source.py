
import json
import yaml
from errors import LoadError

class Source:
	def __init__(self, config_file):
		with open(config_file, 'r') as f:
			suffix = config_file.split('.')[-1]

			if suffix == 'json':
				self.data = json.load(f)
			elif suffix in ['yml', 'yaml']:
				self.data = yaml.load(f)
			else:
				raise LoadError(config_file, '\'%s\' is not a supported file type' % suffix)
