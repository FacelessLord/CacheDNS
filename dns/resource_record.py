import struct
from typing import Tuple, Iterable

from dns.dns_helper import create_byte_qname
from dns.dns_query import read_domain


class ResourceRecord:
    def __init__(self, name: str, rtype: int, rclass: int, ttl: int,
                 rd_length: int, rdata: bytes):
        self.name = name
        self.rtype = rtype
        self.rclass = rclass
        self.ttl = ttl
        self.rd_length = rd_length
        self.rdata = rdata

    def to_bytes(self) -> bytes:
        name, size = create_byte_qname(self.name)
        return struct.pack(
            '!' + str(size) + 's2hIH' + str(self.rd_length) + 's',
            name, self.rtype, self.rclass, self.ttl, self.rd_length, self.rdata)


def from_bytes(record_bytes: bytes) -> Tuple[ResourceRecord, bytes]:
    domain, residual = read_domain(record_bytes)
    # 10 is 2*2+4+2
    rtype, rclass, ttl, rdlength, data = \
        struct.unpack('!2hIH' + str(len(residual) - 10) + 's', residual)
    rdata, next_record = struct.unpack(
        '!' + str(rdlength) + 's' + str(len(data) - rdlength) + 's', data)

    record = ResourceRecord(domain, rtype, rclass, ttl, rdlength, rdata)

    return record, next_record


def parse_records(records: bytes) -> Iterable[ResourceRecord]:
    while len(records) > 0:
        record, records = from_bytes(records)
        yield record
