#!/usr/bin/env python2

import requests

from fakebrowser import FakeBrowser

print "requesting"

r = requests.get('http://thepiratebay.se/',
	headers = FakeBrowser.headers)

print r.status_code
