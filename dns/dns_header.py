import struct

from dns.dns_helper import bytes_at


class DNSHeader:
    def __init__(self,
                 identifier: int,
                 qr: bool, opcode: int = 0, aa: bool = True, tc: bool = False,
                 rd: bool = True, ra: bool = True,
                 rcode: int = 0, qd_count: int = 0, an_count: int = 0,
                 ns_count: int = 0, ar_count: int = 0):
        self.identifier = identifier
        self.qr = qr
        self.opcode = opcode
        self.aa = aa
        self.tc = tc
        self.rd = rd
        self.ra = ra
        self.rcode = rcode
        self.qd_count = qd_count
        self.an_count = an_count
        self.ns_count = ns_count
        self.ar_count = ar_count

    def to_bytes(self):
        qr_rcode = (self.qr << 15 | (self.opcode & 0b1111) << 11 |
                    self.aa << 10 | self.tc << 9 | self.rd << 8 |
                    self.ra << 7 | (self.rcode & 0b1111))

        return struct.pack('!hH4h', self.identifier, qr_rcode,
                           self.qd_count, self.an_count,
                           self.ns_count, self.ar_count)


def parse_header(header_bytes):
    lines = struct.unpack('!6h', header_bytes)

    return DNSHeader(
        identifier=lines[0],

        qr=bytes_at(lines[1], 15, 1),
        opcode=bytes_at(lines[1], 11, 4),
        aa=bytes_at(lines[1], 10, 1),
        tc=bytes_at(lines[1], 9, 1),
        rd=bytes_at(lines[1], 8, 1),
        ra=bytes_at(lines[1], 7, 1),
        rcode=bytes_at(lines[1], 0, 1),

        qd_count=lines[2],
        an_count=lines[3],
        ns_count=lines[4],
        ar_count=lines[5])
