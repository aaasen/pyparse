#!/usr/bin/env python2

from pprint import pprint

from comb import Comb
import comb

tpb = Comb('../../parsers/new_example.yaml')

# pprint(vars(tpb.source))

pprint(tpb.load(tpb.source.data, None))

print map(lambda x: str(x.parser), tpb.parsers)

# results = tpb['search'].get({ 'term' : 'ubuntu' })

# pprint(map(lambda x: vars(x), results[:1]))
