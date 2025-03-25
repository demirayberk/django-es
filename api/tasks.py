from celery import shared_task
from typing import Text
import ipaddress
import random

from celery import shared_task
from es.schemas import HostNameMapping
from es.hostname_ip import HostIpSearch


def generate_random_ip_from_cidr(cidr: Text) -> Text:
    """Generate a random IP address from a CIDR block"""
    network = ipaddress.ip_network(cidr)
    network_address = int(network.network_address)
    broadcast_address = int(network.broadcast_address)
    return str(ipaddress.ip_address(random.randint(network_address + 1, broadcast_address - 1)))


@shared_task
def mock_task():
    print("Mock task executed!")
    return "Task completed"


@shared_task
def populate_mock_data():
    cidr_blocks = [
        "192.168.0.0/16",
        "10.0.0.0/8",
        "172.16.0.0/12",
        "100.64.0.0/10",
    ]
    hostname_prefixes = [
        "web", "db", "app", "auth", "cache",
        "lb", "fileserver", "backup", "mon", "gw", "octoxlabs"
    ]
    base_host = random.choice(hostname_prefixes)
    random_suffix = random.randint(1, 1000)
    hostname = f"{base_host}-{random_suffix}"
    cidr = random.choice(cidr_blocks)
    ip = generate_random_ip_from_cidr(cidr)
    document = {
        "Hostname": hostname,
        "Ip": [ip]
    }
    hs = HostNameMapping(**document)
    HostIpSearch().insert(item=hs)

    print(f"Added document: {document}");
