#!/usr/bin/env python2

import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

from bay_api import BayAPI
from torrent import Torrent
from source import Source

from pprint import pprint

tpb = Source('sources/pirate_bay.json')
tpb_api = BayAPI(tpb)

torrents = tpb_api.search('ubuntu', tpb.config['search']['sort_codes']['seeders'])

torrent = tpb_api.get_torrent(torrents[0])

pprint(vars(torrent))
