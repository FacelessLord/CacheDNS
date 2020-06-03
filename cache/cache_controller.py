import pickle
import threading
import time

from cache.cache import Cache


class CacheController:
    def __init__(self, load_from_cache: bool, config: dict):
        self.config = config
        self.cache = Cache()
        self.filename = self.config['cache_file'] + ".json"
        if load_from_cache:
            print('Reading Cache from file')
            self.cache.cache = self.load_cache()
            print('Cache loaded')

        print('Loading Cache Daemon')
        self.daemon = threading.Thread(target=cache_daemon, args=[self.cache])
        self.daemon.setDaemon(True)
        self.daemon.setName("Cache Daemon")

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


def cache_daemon(cache: Cache):
    print('Daemon started')
    while True:
        time.sleep(10)
