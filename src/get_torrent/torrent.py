
class Torrent:
	def __init__(self, url, title=None, description=None, magnet=None, seeders=None, leechers=None):
		self.url = url
		self.title = title
		self.description = description
		self.magnet = magnet
		self.seeders = seeders
		self.leechers = leechers
