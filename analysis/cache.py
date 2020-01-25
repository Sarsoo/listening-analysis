import os
import logging
import json

logger = logging.getLogger(__name__)


class Cache:
    def __init__(self, cache):
        self.cache = cache

    def set_track(self, name, artist, uri=None, audio_features=None):
        name = str(name).lower()
        artist = str(artist).lower()

        if self.cache['cache'].get(artist) is None:
            self.cache['cache'][artist] = {name: {}}
        if self.cache['cache'][artist].get(name) is None:
            self.cache['cache'][artist][name] = {}

        if uri is not None:
            self.cache['cache'][artist][name]['uri'] = uri
        if audio_features is not None:
            self.cache['cache'][artist][name]['features'] = audio_features

    def get_track(self, name, artist):
        name = str(name)
        artist = str(artist)
        try:
            return self.cache['cache'][artist][name]
        except KeyError:
            return None


def load_cache_from_storage(path: str = '.', name: str = 'cache.json'):

    if os.path.exists(os.path.join(path, name)):
        with open(os.path.join(path, name), 'r') as file:
            return Cache(json.loads(file.read()))
    else:
        logger.error(f'{os.path.join(path, name)} does not exist')
        return {'cache': {}}


def write_cache_to_storage(cache: Cache, path: str = '.', name: str = 'cache.json'):
    with open(os.path.join(path, name), 'w') as file:
        file.write(json.dumps(cache.cache))
