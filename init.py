#!/usr/bin/env python2

import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

from fakebrowser import FakeBrowser

s = requests.Session()
s.headers.update(FakeBrowser.headers)

print "requesting"

r = requests.get('http://thepiratebay.se/search/test/0/99/0')

print r.status_code

if r.status_code == requests.codes.ok:
	root = etree.HTML(r.text)

	expression = GenericTranslator().css_to_xpath('a.detLink')

	links = root.xpath(expression)

	print map(lambda x: [v[1] for i, v in enumerate(x.items()) if v[0] == 'href'], links)
