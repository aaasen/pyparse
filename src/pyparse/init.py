#!/usr/bin/env python2

from pprint import pprint

from comb import Comb
import comb

tpb = Comb('../../parsers/new_example.yaml')

# pprint(vars(tpb.source))

pprint(tpb.load(tpb.source.data, None))

print map(lambda x: x.parser, tpb.parsers)

print tpb.parsers[1].extract(first=False)

# results = tpb['search'].get({ 'term' : 'ubuntu' })

# pprint(map(lambda x: vars(x), results[:1]))
