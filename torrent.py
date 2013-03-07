
class Torrent:
	url = None

	name = None
	magnet = None
	info_hash = None
	
	upload_date = None
	upload_user = None

	seeders = None
	leechers = None

	comments = None
	tags = None
	category = None

	size = None
	num_files = None

	def __init__(self, url):
		self.url = url
