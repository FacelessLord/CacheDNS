import struct

MASK = [1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16387,
        32767, 65535, 131071]

TYPES = {'a': 1, 'ns': 2, 'md': 3, 'mf': 4, 'cname': 5, 'soa': 6, 'mb': 7,
         'mg': 8, 'mr': 9, 'null': 10, 'wks': 11, 'ptr': 12, 'hinfo': 13,
         'minfo': 14, 'ms': 15, 'txt': 16}
CLASSES = {'in': 1, 'cs': 2, 'ch': 3, 'hs': 4}


def bytes_at(data, pos, size):
    return (data & (MASK[size - 1] << pos)) >> pos & MASK[size - 1]


def create_byte_qname(qname: str):
    labels = qname.split('.')
    if labels[-1] == '':
        labels = labels[:-1]

    lengths = list(map(lambda l: len(l), labels))
    fmt = '!'
    byte_length = 0
    collection = []
    for i in range(len(labels)):
        byte_length += lengths[i] + 1
        collection.append(bytes([lengths[i]]))
        collection.append(labels[i].encode())
        fmt += 'c' + str(lengths[i]) + 's'

    byte_length += 1
    collection.append(bytes([0]))
    fmt += 'c'

    return struct.pack(fmt, *collection), byte_length
