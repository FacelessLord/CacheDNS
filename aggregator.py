import signal
import sys

from cache_controller import CacheController
from config import read_config
from name_server import NameServer


def cache_saver(cache_controller: CacheController):
    def saver(signal_id, frame):
        print('Server Stopping')
        print('Saving Cache')
        cache_controller.save_cache()
        print('Server Stopped')
        sys.exit()

    return saver


if __name__ == "__main__":
    print('Reading config')
    config = read_config()
    print('Loading Cache controller')
    controller = CacheController(True, config)  # True for load cache

    signal.signal(signal.SIGINT, cache_saver(controller))

    print('Loading Name server')
    server = NameServer(controller.cache, config)
    server.loop(config)
