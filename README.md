# GetTorrent: an API for *sharing*

GetTorrent is an API for peer to peer file sharing sites like The Pirate Bay.

File sharing sites are awesome, but they're a total pain for developers.
Some have terribly formatted HTML, others protect from robots.
To make it worse (for devs at least), there are *tons* of them.

### GetTorrent takes care of these inconsistencies so you don't have to
```python
tpb = Getter(Source('../../sources/pirate_bay.json'))
torrents = tpb.search('ubuntu', sort='seeders')
first = tpb.get_torrent(torrents[0])
```
### And here's the most seeded Ubuntu torrent on The Pirate Bay:
```python
{'description': '...',
 'seeders': '64',
 'leechers': '8',
 'magnet': 'magnet:...',
 'url': '/torrent/...'}
```

*Magic.*
