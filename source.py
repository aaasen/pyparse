
import json

class Source:
	config = None

	def __init__(self, config_file):
		with open(config_file, 'r') as f:
			self.config = json.load(f)
