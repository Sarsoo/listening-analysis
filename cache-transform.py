import os, json, pprint

uri_cache_name = 'cache.json'
if os.path.isfile(uri_cache_name):
    with open(uri_cache_name, 'r') as uri_cache:
        uris = json.loads(uri_cache.read())

        new_cache = {
            'cache': {}
        }

        for uri in uris:

            try:
                new_cache['cache'][uri['artist']]
            except KeyError:
                new_cache['cache'][uri['artist']] = {}

            try:
                new_cache['cache'][uri['artist']][uri['name']]
            except KeyError:
                new_cache['cache'][uri['artist']][uri['name']] = {}

            new_cache['cache'][uri['artist']][uri['name']]['uri'] = uri['uri']

        pprint.pprint(new_cache)

    with open(uri_cache_name, 'w') as uri_cache:
        uri_cache.write(json.dumps(new_cache))



