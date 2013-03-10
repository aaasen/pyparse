#!/usr/bin/env python2

import requests
from lxml import etree
from cssselect import GenericTranslator, SelectorError

from bay_api import BayAPI
from torrent import Torrent

from pprint import pprint

tpb = BayAPI()

torrents = tpb.search('ubuntu')

torrent = tpb.get_torrent(torrents[0])

pprint (vars(torrent))
