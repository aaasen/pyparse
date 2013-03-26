
import json
import yaml
from errors import LoadError

class Source:
	_config = None

	def __init__(self, config_file):
		with open(config_file, 'r') as f:
			suffix = config_file.split('.')[-1]

			if suffix == 'json':
				self._config = json.load(f)
			elif suffix in ['yml', 'yaml']:
				self._config = yaml.load(f)
			else:
				raise LoadError(config_file, '\'%s\' is not a supported file type' % suffix)

			self.info = self._config['info']
			self.search = self._config['search']
			self.torrent = self._config['torrent']
