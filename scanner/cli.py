# cli.py
# cli.py
import argparse

from . import COMMON_PORTS, DEFAULT_TIMEOUT, DEFAULT_THREADS
from .utils import parse_hosts, parse_ports
from .core import PortScanner
from .reports import write_csv, write_html

def parse_args():
    p = argparse.ArgumentParser(description='Simple multithreaded Network Port Scanner (ethical use only)')
    p.add_argument('--host', required=True,
                   help='Target host, comma list, or simple last-octet range. E.g. 192.168.1.10 or 192.168.1.10-20')
    p.add_argument('--ports', help='Ports to scan. E.g. 22,80,443,1000-2000')
    p.add_argument('--common', action='store_true', help='Scan a list of common ports (faster)')
    p.add_argument('--timeout', type=float, default=None, help='Socket timeout in seconds (overrides default)')
    p.add_argument('--threads', type=int, default=None, help='Number of scanner threads (overrides default)')
    p.add_argument('--protocol', choices=['tcp', 'udp'], default='tcp', help='Protocol to scan (tcp or udp)')
    p.add_argument('--output-prefix', default=None, help='Prefix for output files (optional)')
    return p.parse_args()

def main():
    args = parse_args()

    hosts = parse_hosts(args.host)

    # Ensure that --common and --ports are not used together
    if args.common and args.ports:
        print('[!] --common and --ports cannot be used at the same time. Aborting.')
        return

    if args.common:
        ports = COMMON_PORTS
    elif args.ports:
        ports = parse_ports(args.ports)
    else:
        print('[*] No ports specified, using common ports. Use --ports to specify a range or list.')
        ports = COMMON_PORTS

    # sanity checks
    if len(hosts) > 256:
        print('[!] Too many hosts specified (limit 256). Aborting.')
        return
    if len(ports) > 65535:
        print('[!] Too many ports. Aborting.')
        return

    # use defaults from package if not provided
    timeout = args.timeout if args.timeout is not None else DEFAULT_TIMEOUT
    threads = args.threads if args.threads is not None else DEFAULT_THREADS

    scanner = PortScanner(hosts=hosts, ports=ports, protocol=args.protocol,
                          timeout=timeout, threads=threads)
    print(f'[*] Starting {args.protocol.upper()} scan: hosts={len(hosts)} ports={len(ports)} threads={threads} timeout={timeout}s')

    elapsed, results = scanner.run()
    print(f'\n[*] Scan finished in {elapsed:.2f}s. {len(results)} results recorded.')

    host_label = args.output_prefix if args.output_prefix else hosts[0].replace('.', '_')
    csv_file = write_csv(results, host_label)
    html_file = write_html(results, host_label)

    print(f'[*] Reports written: {csv_file}, {html_file}')
    print('[*] Done.')

if __name__ == '__main__':
    main()
