#!/usr/bin/env python2

import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

from bay_api import BayAPI
from torrent import Torrent
import parse

tpb = BayAPI()

r = tpb.search('hello')

root = etree.HTML(r.text)

expression = GenericTranslator().css_to_xpath('a.detLink')

links = root.xpath(expression)

links = map(lambda x: parse.get_tuple(x.items(), 'href'), links)

links = map(lambda x: Torrent(x), links)

for link in links:
	print link.url
