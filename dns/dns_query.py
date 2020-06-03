import struct
from typing import Tuple, List
from dns.dns_helper import create_byte_qname


class DNSQuery:
    def __init__(self, qname: str, qtype: int, qclass: int):
        self.qname = qname
        self.qtype = qtype
        self.qclass = qclass

    def to_bytes(self) -> Tuple[bytes, int]:
        name, size = create_byte_qname(self.qname)
        bytes_query = \
            struct.pack("!" + str(size) + 's2h', name, self.qtype, self.qclass)

        return bytes_query, size + 4


def parse_queries(queries_bytes: bytes, query_count: int, body: bytes) -> \
        Tuple[List[DNSQuery], bytes]:
    queries = []
    for i in range(query_count):
        qname, queries_bytes = read_domain(queries_bytes, body)
        qtype: int = struct.unpack('!h', queries_bytes[:2])[0]
        qclass: int = struct.unpack('!h', queries_bytes[2:4])[0]
        queries_bytes = queries_bytes[4:]

        queries.append(DNSQuery(qname, qtype, qclass))
    return queries, queries_bytes


def read_domain(queries_bytes, body: bytes):
    labels = []
    lsize = queries_bytes[0]
    queries_bytes = queries_bytes[1:]
    while lsize > 0:
        if lsize & 0b1100_0000:
            ptr = (lsize ^ 0b1100_0000) << 8 | queries_bytes[0]
            queries_bytes = queries_bytes[1:]
            subqname, _ = read_domain(body[ptr:], body)
            labels.append(subqname)
            break
        labels.append(queries_bytes[:lsize].decode(encoding='cp1251'))
        queries_bytes = queries_bytes[lsize:]
        lsize = queries_bytes[0]
        queries_bytes = queries_bytes[1:]
    qname = '.'.join(labels)
    return qname, queries_bytes
