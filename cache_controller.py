import pickle

from cache import Cache


class CacheController:
    def __init__(self, load_from_cache: bool, config: dict):
        self.config = config
        self.cache = Cache()
        self.filename = self.config['cache_file'] + ".json"
        if load_from_cache:
            print('Reading Cache from file')
            self.cache.cache = self.load_cache()

    def save_cache(self):
        file = open(self.filename, 'wb')
        pickle.dump(self.cache.cache, file)
        file.close()

    def load_cache(self):
        try:
            file = open(self.filename, 'rb')
            new_cache = pickle.load(file)
            file.close()
            return new_cache
        except:
            return {}
