import struct

from dns.dns_helper import TYPES, CLASSES
from dns.resource_record import ResourceRecord


def test_qname_marshaling_easy():
    record = ResourceRecord("google.com", TYPES['a'], CLASSES['in'], 10,
                            0, b'')
    expected = bytes([6]) + b'google' \
               + bytes([3]) + b'com' \
               + bytes([0]) \
               + bytes([0, 1]) \
               + bytes([0, 1]) \
               + bytes([0, 0, 0, 10]) \
               + bytes([0, 0])

    bstring = record.to_bytes()
    assert bstring == expected
