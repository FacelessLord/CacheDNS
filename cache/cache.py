import datetime
import time
from threading import Lock
from typing import Tuple, List

from dns.resource_record import ResourceRecord


class Cache:
    def __init__(self):
        self.cache = {}  # dict[(qname, qtype,qclass): (rr, time received)]
        self.lock = Lock()

    def __getitem__(self, item) -> Tuple[ResourceRecord, float]:
        with self.lock:
            return self.cache[item]

    def __contains__(self, item):
        with self.lock:
            return item in self.cache

    def append(self, key, item):
        with self.lock:
            if key in self.cache:
                self.cache[key].append(item)
            else:
                self.cache[key] = [item]

    def remove_expired(self):
        now = time.time()
        with self.lock:
            for k in self.cache:
                rrl: List[Tuple[ResourceRecord, time]] = self.cache[k]
                for rr in rrl:
                    if rr[0].ttl < (now - rr[1]):
                        rrl.remove(rr)
