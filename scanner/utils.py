# scanner/utils.py
import socket

def parse_hosts(host_arg: str):
    """Accepts single host, comma separated list, or a simple range like 192.168.1.10-12"""
    hosts = []
    for part in host_arg.split(','):
        part = part.strip()
        if '-' in part:
            # support last-octet ranges only e.g. 192.168.1.10-20
            base, rng = part.rsplit('.', 1)
            if '-' in rng:
                start_s, end_s = rng.split('-')
                start, end = int(start_s), int(end_s)
                for i in range(start, end + 1):
                    hosts.append(f'{base}.{i}')
            else:
                hosts.append(part)
        else:
            hosts.append(part)
    return hosts


def parse_ports(ports_arg: str):
    """Accept formats like:
       - single number: 80
       - range: 20-1024
       - comma separated: 22,80,443
       - mixed: 22,80,8000-8100
    """
    ports = set()
    for token in ports_arg.split(','):
        token = token.strip()
        if '-' in token:
            start, end = token.split('-')
            for p in range(int(start), int(end) + 1):
                ports.add(int(p))
        else:
            ports.add(int(token))
    return sorted(ports)


def guess_service(port: int):
    try:
        return socket.getservbyport(port)
    except Exception:
        return ""
