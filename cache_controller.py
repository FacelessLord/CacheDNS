from cache import Cache


class CacheController:
    def __init__(self, load_from_cache: bool, config: dict):
        self.cache = Cache()
        if load_from_cache:
            self.load_cache()

    def load_cache(self):
        # todo
        pass
