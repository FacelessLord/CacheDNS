import struct
from dns import dns_helper
from dns.dns_header import DNSHeader


def test_qname_marshaling_easy():
    qstring = 'aa.bb.cc.'
    expected = struct.pack('!10s',
                           bytes([2]) + b'aa'
                           + bytes([2]) + b'bb'
                           + bytes([2]) + b'cc'
                           + bytes([0]))

    bstring = dns_helper.create_byte_qname(qstring)
    assert bstring == expected


def test_qname_marshaling_average():
    qstring = 'conversion.codes.are.only.available.for.the.native.size'
    expected = struct.pack('!' + str(len(qstring) + 1 + 1) + 's', # one for last point and another for terminator
                           bytes([10]) + b'conversion'
                           + bytes([5]) + b'codes'
                           + bytes([3]) + b'are'
                           + bytes([4]) + b'only'
                           + bytes([9]) + b'available'
                           + bytes([3]) + b'for'
                           + bytes([3]) + b'the'
                           + bytes([6]) + b'native'
                           + bytes([4]) + b'size'
                           + bytes([0]))

    bstring = dns_helper.create_byte_qname(qstring)
    assert bstring == expected
