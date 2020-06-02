import os
from json import decoder, encoder


def create_default_config() -> dict:
    return {'ns': {'port': 25565, 'ip': '127.0.0.1'},
            'fwd': {'port': 53, 'ip': '8.8.8.8'},
            'buffersize': 2048,
            'cache_file': 'dns_cache'}


def read_config() -> dict:
    if os.path.exists("config.json"):
        cfg_decoder = decoder.JSONDecoder()
        with open("config.json", 'rt') as f:
            return cfg_decoder.decode('\n'.join(f.readlines()))
    else:
        print('Config file not found. Creating new one...')
        cfg = create_default_config()
        cfg_encoder = encoder.JSONEncoder()
        json = cfg_encoder.encode(cfg)
        with open("config.json", 'wt') as f:
            f.write(json)
            f.flush()
        return cfg
