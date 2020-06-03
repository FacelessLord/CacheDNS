import os
import struct
from typing import Tuple, List

from cache import Cache
from pickle import dump, load

from dns.resource_record import ResourceRecord, from_bytes


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
            with open(self.filename, 'rb') as f:
                data = b''
                temp = f.read(1024)
                while temp:
                    data += temp
                    temp = f.read(1024)

                self.cache.cache = deserialize_cache(data)
        else:
            print('Cache file not found.')

    def save_cache(self):
        with open(self.filename, 'wb') as f:
            f.write(serialize_cache(self.cache.cache))


def serialize_cache(cache: dict):
    result = b''
    for k in cache:
        data = serialize_entry((k, cache[k]))
        result += struct.pack('!h', len(data)) + data
    return result


def serialize_entry(entry: Tuple[Tuple[str, bytes, bytes],
                                 List[Tuple[ResourceRecord, float]]]):
    "name_len2|name:name_len|qtype2|qclass2|list_le2n|[record_len2|record:record_len|time2]*"
    key = entry[0]
    key_bytes = struct.pack('!h', len(key[0])) + key[0].encode() \
                + struct.pack('!2h', key[1], key[2])
    value = entry[1]
    print(value)
    records_list = value
    records = b''
    for t in records_list:
        record_bytes = t[0].to_bytes()
        time_bytes = struct.pack('!f', t[1])
        value_bytes = struct.pack('!h',
                                  len(record_bytes)) + record_bytes + time_bytes
        records += value_bytes
    records = struct.pack('!h', len(records_list)) + records

    data = key_bytes + records
    return data


def deserialize_cache(cache_bytes: bytes):
    entries = {}
    while len(cache_bytes) > 0:
        entry_len = struct.unpack('!h', cache_bytes[:2])[0]
        cache_bytes = cache_bytes[2:]
        key, value = deserialize_entry(cache_bytes[:entry_len])
        entries[key] = value
        cache_bytes = cache_bytes[entry_len:]
    return entries


def deserialize_entry(entry_bytes: bytes):
    "name_len2|name:name_len|qtype2|qclass2|list_len2|[record_len2|record:record_len|time2]*"
    name_length = struct.unpack('!h', entry_bytes[:2])[0]
    other = entry_bytes[2:]
    name = other[:name_length].decode()
    other = other[name_length:]

    qtype, qclass = struct.unpack('!2h', other[:4])
    other = other[4:]

    key = (name, qtype, qclass)

    records_count = struct.unpack('!h', other[:2])[0]
    other = other[2:]
    records_list = []
    for i in range(records_count):
        record_length = struct.unpack('!h', other[:2])[0]
        other = other[2:]
        record_bytes = other[:record_length]
        other = other[record_length:]
        time = struct.unpack('!f', other[:4])[0]
        other = other[2:]
        record, left = from_bytes(record_bytes, record_bytes)
        records_list.append((record, time))
    return key, records_list
