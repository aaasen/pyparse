
Here goes a sample parser to design pyparse around.

```yaml
available_parsers: [search]

search:
    available_parsers: [seeders, magnet]
    schema: |
        http://tpb.anonhi.de/search/<[[search_term]]>/<[[sort_code]]>/
    
    args:
        sort_code:
            default: 0
            date: 3
            size: 5
            seeders: 7
            leechers: 8
            uploader: 11
    
    seeders:
        method: xpath
        selector: |
            //tr/td[3]
        attr: text
    
    magnet:
        method: css
        selector: |
            td > a[title~=magnet]
        attr: href
    
```
