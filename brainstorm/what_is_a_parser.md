
# Parsers

parsers can:
	- fetch a file and make a tree with it
	- parse their parent document
	- have child parsers
---

parsers: [parent]

parent:
	parsers: [child]

	fetch:
		url: ...
		headers: ...

	method: (css|xpath)
	selector: a.class
	attr: (text|href|class...)

	child:
		method: ...
		selector: ...
		attr: ...

...

## How to parse a parser

	- check for fetch
		- fetch and create a tree
	- execute parser on parent tree if necessary
	- check for children
		- if children make a tree with parser return data
			- execute children on that tree
		- if no children return parser return data
