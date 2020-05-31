import datetime


class Cache:
    def __init__(self):
        self.a_to_ab = {}
        self.b_to_ab = {}
        self.record_creation_time = {}

    def add_pair(self, a, b):
        pair = (a, b)
        time = datetime.datetime.now()
        self.a_to_ab[a] = pair
        self.b_to_ab[b] = pair
        self.record_creation_time[pair] = time

    def remove_records_older_than(self, timeout):
        now = datetime.datetime.now()
        pairs = filter(lambda k: (self.record_creation_time[k] - now) > timeout,
                       self.record_creation_time.keys())
        for pair in pairs:
            del(self.record_creation_time[pair])
            del(self.a_to_ab[pair[0]])
            del(self.b_to_ab[pair[1]])
