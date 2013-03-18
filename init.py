#!/usr/bin/env python2

from bay_api import BayAPI
from torrent import Torrent
from source import Source

from pprint import pprint

tpb = BayAPI(Source('sources/pirate_bay.json'))
torrents = tpb.search('ubuntu')
first = tpb.get_torrent(torrents[0])

pprint(vars(first))
