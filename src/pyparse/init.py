#!/usr/bin/env python2

from pprint import pprint

from comb import Comb
import comb

tpb = Comb('../../parsers/new_example.yaml')

tpb.load('entry', tpb.source.data, None)

print tpb.parsers[1:]

for parser in tpb.parsers[1:]:
	print parser.extract(first=False)

print zip(tpb.parsers[1].extract(first=False), tpb.parsers[2].extract(first=False))
