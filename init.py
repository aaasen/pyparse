#!/usr/bin/env python2

import requests

chromium_headers = { 'Host' : 'thepiratebay.se',
	'Connection' : 'keep-alive',
	'Cache-Control' : 'max-age=0',
	'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.152 Safari/537.22',
	'Accept-Encoding' : 'gzip,deflate,sdch',
	'Accept-Language' : 'en-US,en;q=0.8',
	'Accept-Charset' : 'UTF-8,*;q=0.5' }

r = requests.get('http://thepiratebay.se/',
	params = {'action' : 'log', 'js' : 'no'},
	headers = chromium_headers)

print r.status_code
