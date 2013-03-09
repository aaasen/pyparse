
from lxml import etree
from cssselect import GenericTranslator, SelectorError

class Torrent:
	url = None

	name = None
	uid = None
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

	def get_description(self, tree):
			expression = GenericTranslator().css_to_xpath('div.nfo')

			description = tree.xpath(expression)
			
			return description[0].getchildren()[0].text
