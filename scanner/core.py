# scanner/core.py
import socket
import threading
import queue
import time
from typing import List, Dict, Tuple

from . import utils

class PortScanner:
    """Multithreaded Network Port Scanner for TCP and UDP.

    - hosts: list of host strings
    - ports: list of integer ports
    - protocol: 'tcp' or 'udp'
    """
    def __init__(self, hosts: List[str], ports: List[int],
                 protocol: str = 'tcp',
                 timeout: float = 1.0, threads: int = 100):
        self.hosts = hosts
        self.ports = ports
        self.protocol = protocol
        self.timeout = timeout
        self.threads_count = threads

        self.job_q = queue.Queue()
        self.results_lock = threading.Lock()
        self.results: List[Dict] = []  # dicts: {host, port, status, service}
        self.total_jobs = 0
        self.finished_jobs = 0

    def _enqueue_jobs(self):
        for host in self.hosts:
            for port in self.ports:
                self.job_q.put((host, port))
                self.total_jobs += 1

    def _scan_tcp(self, host: str, port: int) -> str:
        """Performs a TCP scan on a single port."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.timeout)
            if s.connect_ex((host, port)) == 0:
                return 'open'
            else:
                return 'closed'

    def _scan_udp(self, host: str, port: int) -> str:
        """Performs a UDP scan on a single port."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(self.timeout)
            try:
                # Send a null byte. For many services, this is enough to elicit a response.
                s.sendto(b'', (host, port))
                # If we receive anything, the port is open.
                s.recvfrom(1024)
                return 'open'
            except socket.timeout:
                # If we time out, the port is either open (but not responding) or filtered.
                return 'open|filtered'
            except ConnectionRefusedError:
                # If we get an ICMP "Port Unreachable" message, the port is closed.
                return 'closed'
            except Exception:
                return 'closed'

    def _scan_port(self, host: str, port: int):
        """Selects the correct scan method based on protocol and records the result."""
        try:
            if self.protocol == 'tcp':
                status = self._scan_tcp(host, port)
            else:
                status = self._scan_udp(host, port)
        except Exception as e:
            status = f'error:{e}'

        service = utils.guess_service(port, self.protocol) if status == 'open' else ''
        with self.results_lock:
            result = {'host': host, 'port': port, 'protocol': self.protocol, 'status': status, 'service': service}
            self.results.append(result)
            self.finished_jobs += 1

    def _worker(self):
        while True:
            try:
                host, port = self.job_q.get_nowait()
            except queue.Empty: # No more jobs
                return # Exit thread
            self._scan_port(host, port)

    def run(self, show_progress: bool = True) -> Tuple[float, List[Dict]]:
        start = time.time()
        self._enqueue_jobs()

        threads = []
        for _ in range(min(self.threads_count, max(1, self.total_jobs))):
            t = threading.Thread(target=self._worker, daemon=True)
            t.start()
            threads.append(t)

        try:
            while any(t.is_alive() for t in threads):
                if show_progress:
                    self._print_progress()
                time.sleep(0.5)
            if show_progress:
                self._print_progress(final=True)
        except KeyboardInterrupt:
            print('\n[*] KeyboardInterrupt received: waiting for running threads to exit...')
            # daemon threads will exit with the main program

        elapsed = time.time() - start
        return elapsed, self.results

    def _print_progress(self, final: bool = False):
        with self.results_lock:
            done = self.finished_jobs
            total = self.total_jobs
        pct = (done / total * 100) if total else 100
        end = '\n' if final else '\r'
        print(f'Progress: {done}/{total} ({pct:.1f}%)', end=end, flush=True)
