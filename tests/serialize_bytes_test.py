from cache import Cache
from cache.cache_controller import deserialize_entry, serialize_entry, \
    deserialize_cache, serialize_cache
from dns.resource_record import ResourceRecord


def test_serialize_entry():
    entry = (('asgfasf', bytes([0, 1]), bytes([0, 1])),
             [(ResourceRecord('asf', 1, 5, 7, 0, bytes()), 1251.4)])

    value = deserialize_entry(serialize_entry(entry))

    assert entry[0] == value[0]
    assert entry[1][0][0] == value[1][0][0]
    assert entry[1][0][1] - value[1][0][1] < 1e-5


def test_serialize_cache():
    cache = Cache()

    entry1 = (('asgfasf.', 1, 1),
              [(ResourceRecord('asf', 1, 5, 7, 0, bytes()), 1251.4)])
    entry2 = (('a.sg.fas3.f', 1, 1),
              [(ResourceRecord('asf', 1, 5, 5, 0, bytes()), 1251.4)])
    entry3 = (('asgf.as3f.', 1, 1),
              [(ResourceRecord('asf2', 1, 5, 5, 0, bytes()), 122.4)])
    cache.cache[entry1[0]] = entry1[1]
    cache.cache[entry2[0]] = entry2[1]
    cache.cache[entry3[0]] = entry3[1]

    new_cache = deserialize_cache(serialize_cache(cache.cache))
    assert new_cache[entry1[0]][0][0] == cache.cache[entry1[0]][0][0]
    assert new_cache[entry1[0]][0][1] - cache.cache[entry1[0]][0][1] < 1e-3
    assert new_cache[entry2[0]][0][0] == cache.cache[entry2[0]][0][0]
    assert new_cache[entry2[0]][0][1] - cache.cache[entry2[0]][0][1] < 1e-3
    assert new_cache[entry3[0]][0][0] == cache.cache[entry3[0]][0][0]
    assert new_cache[entry3[0]][0][1] - cache.cache[entry3[0]][0][1] < 1e-3
