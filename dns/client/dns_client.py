import socket

from dns.dns_header import DNSHeader
from dns.dns_packet import DNSPacket, read_packet
from dns.dns_query import DNSQuery
from name_server import NameServer
from dns.dns_helper import TYPES, CLASSES


class DNSClient:
    """Used for tests"""

    def __init__(self, config: dict):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (config["ns"]["ip"], config["ns"]["port"])

    def run(self):
        response_bytes = self.request(1, "google.com", TYPES['ns'],
                                      CLASSES['in'])
        response = read_packet(response_bytes)

        for rr in response.ans_records:
            print(f'name:{rr.name}')
            print(f'class:{rr.rclass}')
            print(f'data:{rr.rdata}')

    def request(self, identifier, qname, qtype, qclass):
        header = DNSHeader(identifier, True, qd_count=1)
        packet = DNSPacket(header)
        packet.add_query(DNSQuery(qname, qtype, qclass))

        self.socket.sendto(packet.to_bytes(), self.server_address)

        response = self.socket.recv(1024)
        full_response = response
        while response:
            print(response)
            response = self.socket.recv(1024)
            full_response += response

        return full_response
