#!/usr/bin/env python2

import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

from bay_api import BayAPI

tpb = BayAPI()

r = tpb.search('hello')

root = etree.HTML(r.text)

expression = GenericTranslator().css_to_xpath('a.detLink')

links = root.xpath(expression)

print map(lambda x: [v[1] for i, v in enumerate(x.items()) if v[0] == 'href'][0], links)
