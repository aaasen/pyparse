# GetTorrent: an API for *sharing*

GetTorrent is an API for peer to peer file sharing sites like The Pirate Bay.

File sharing sites are awesome, but they're a total pain for developers.
Some have terribly formatted HTML, others protect from robots.
To make it worse (for devs at least), there are *tons* of them.

### GetTorrent takes care of these inconsistencies so you don't have to
```python
>>> tpb = GetTorrent('../../sources/pirate_bay.json')
>>> tpb.search('ubuntu', sort='seeders')
{
	'title': 'Ubuntu 12.10',
	'seeders': '64',
	'leechers': '8',
	'magnet': 'magnet:...',
	'url': '/torrent/...'
}
...
```

*Magic.*
