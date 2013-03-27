#!/usr/bin/env python2

from pprint import pprint

from comb import Comb
import comb

tpb = Comb('../../parsers/new_example.yaml')

# pprint(vars(tpb.source))

pprint(comb.load(tpb.source.data))

# results = tpb['search'].get({ 'term' : 'ubuntu' })

# pprint(map(lambda x: vars(x), results[:1]))
