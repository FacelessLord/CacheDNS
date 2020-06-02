from config import read_config
from dns.client.dns_client import DNSClient

if __name__ == "__main__":
    config = read_config()
    client = DNSClient(config)
    client.run()
