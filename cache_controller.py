import os

from cache import Cache
from json import decoder, encoder


class CacheController:
    def __init__(self, load_from_cache: bool, config: dict):
        self.config = config
        self.cache = Cache()
        self.filename = self.config['cache_file'] + ".json"
        if load_from_cache:
            print('Reading Cache from file')
            self.load_cache()

    def load_cache(self):
        if os.path.exists(self.filename):
            cache_decoder = decoder.JSONDecoder()
            with open(self.filename, 'rt') as f:
                self.cache.cache = cache_decoder.decode(
                    '\n'.join(f.readlines()))
        else:
            print('Cache file not found.')

    def save_cache(self):
        cache_encoder = encoder.JSONEncoder()
        json = cache_encoder.encode(self.cache.cache)
        with open(self.filename, 'wt') as f:
            f.write(json)
            f.flush()
