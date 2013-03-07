#!/usr/bin/env python2

import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

from bay_api import BayAPI
from torrent import Torrent

tpb = BayAPI()

torrents = tpb.search('hello')

r = tpb._get()

print r.status_code
