from name_server import NameServer
from cache_controller import CacheController
from config import read_config

if __name__ == "__name__":
    config = read_config()
    controller = CacheController(True, config)  # True for load cache
    server = NameServer(config)
