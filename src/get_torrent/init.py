#!/usr/bin/env python2

from getter import Getter
from torrent import Torrent
from source import Source

from pprint import pprint

tpb = Getter(Source('../../sources/pirate_bay.json'))
torrents = tpb.search('ubuntu', sort='seeders')
first = tpb.get_torrent(torrents[0])

pprint(vars(first))
