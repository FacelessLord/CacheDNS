import socket
import time
from typing import List, Tuple

from cache import Cache
from dns.dns_header import DNSHeader
from dns.dns_packet import read_packet, DNSPacket
from dns.resource_record import ResourceRecord


class NameServer:
    def __init__(self, cache: Cache, config: dict):
        self.cache = cache
        self.last_id = 0
        self.request_queue = {}
        self.responses = {}

    def loop(self, config):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((config["ns"]["ip"], config["ns"]["port"]))

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # client_socket.settimeout(2)
        fwd_address = (config["fwd"]["ip"], config["fwd"]["port"])

        print('Server Started')
        while True:
            request_bytes, address = server_socket.recvfrom(
                config['buffersize'])

            print('\tRequest from ' + str(address))
            request_packet = read_packet(request_bytes)

            have_non_cached_quests = False
            for q in request_packet.queries:
                if (q.qname, q.qtype, q.qclass) not in self.cache.cache:
                    have_non_cached_quests = True
                    break

            if have_non_cached_quests:
                print('\tCache miss. Forwarding...')
                client_socket.sendto(request_bytes, fwd_address)
                dns_response_bytes, _ = client_socket.recvfrom(
                    config['buffersize'])
                dns_response = read_packet(dns_response_bytes)

                now = time.time()

                for rr in dns_response.ans_records + \
                          dns_response.auth_records + \
                          dns_response.additional_records:
                    key = (rr.name, rr.rtype, rr.rclass)
                    self.cache.append(key, (rr, now))

                server_socket.sendto(dns_response_bytes, address)
            else:
                print('\tCache hit')
                rrs_with_time: List[Tuple[ResourceRecord, float]] = []
                for q in request_packet.queries:
                    key = (q.qname, q.qtype, q.qclass)
                    rrs_with_time += self.cache[key]

                rrs: List[ResourceRecord] = list(
                    map(lambda p: p[0], rrs_with_time))
                header = DNSHeader(request_packet.header.identifier, True,
                                   ns_count=len(rrs))
                response = DNSPacket(header)
                response.set_data([], rrs)

                server_socket.sendto(response.to_bytes(), address)
