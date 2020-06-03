import struct
from typing import List, Tuple

from dns.dns_header import DNSHeader, parse_header
from dns.dns_query import DNSQuery, parse_queries
from dns.resource_record import parse_records, ResourceRecord


class DNSPacket:
    def __init__(self, header: DNSHeader):
        self.header: DNSHeader = header
        self.queries: List[DNSQuery] = []
        self.ans_records: List[ResourceRecord] = []
        self.auth_records: List[ResourceRecord] = []
        self.additional_records: List[ResourceRecord] = []

    def add_query(self, query: DNSQuery):
        self.queries.append(query)
        return self

    def set_data(self, queries: List[DNSQuery], records: List[ResourceRecord]):
        self.queries = queries
        self.ans_records = records[:self.header.an_count]
        self.auth_records = records[self.header.an_count:
                                    self.header.an_count + self.header.ns_count]
        self.additional_records = \
            records[self.header.an_count + self.header.ns_count:
                    self.header.an_count + self.header.ns_count
                    + self.header.ar_count]
        return self

    def to_bytes(self) -> bytes:
        fmt = '!12s'
        values = [self.header.to_bytes()]
        for q in self.queries:
            query_bytes, size = q.to_bytes()
            fmt += str(size) + 's'
            values.append(query_bytes)
        for r in self.ans_records + self.auth_records + self.additional_records:
            record_bytes = r.to_bytes()
            fmt += str(len(record_bytes)) + 's'
            values.append(record_bytes)

        return struct.pack(fmt, *values)


def read_packet(packet_bytes: bytes) -> DNSPacket:
    header, queries = struct.unpack(
        '!12s' + str(len(packet_bytes) - 12) + 's',
        packet_bytes)
    header = parse_header(header)
    queries, residual = parse_queries(queries, header.qd_count, packet_bytes)
    records = list(parse_records(residual, packet_bytes))
    return DNSPacket(header).set_data(queries, records)


def create_dns_packet(request_id: int, queries: List[DNSQuery]) -> DNSPacket:
    header = DNSHeader(request_id, False, 0, False, False, True, True,
                       0, 1, 0, 0, 0)

    return DNSPacket(header).set_data(queries, [])
