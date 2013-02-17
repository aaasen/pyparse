#!/usr/bin/env python2

import requests

print "hey!"

r = requests.get('http://thepiratebay.se/')
print r.status_code
