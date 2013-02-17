#!/usr/bin/env python2

import requests

print "hey!"

r = requests.get('https://github.com/timeline.json')
print r.status_code
