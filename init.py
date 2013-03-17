#!/usr/bin/env python2

from bay_api import BayAPI
from torrent import Torrent
from source import Source

from pprint import pprint

kat = Source('sources/kick_ass_torrents.json')
kat_api = BayAPI(kat)

torrents = kat_api.search('ubuntu')

torrent = kat_api.get_torrent(torrents[0])

pprint(vars(torrent))


tpb = Source('sources/pirate_bay.json')
tpb_api = BayAPI(tpb)

torrents = tpb_api.search('ubuntu')

torrent = tpb_api.get_torrent(torrents[0])

pprint(vars(torrent))
