
import json

class Source:
	_config = None

	def __init__(self, config_file):
		with open(config_file, 'r') as f:
			self._config = json.load(f)
			self.info = self._config['info']
			self.search = self._config['search']
			self.torrent = self._config['torrent']
