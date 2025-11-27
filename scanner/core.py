# scanner/core.py
import socket
import threading
import queue
import time
from typing import List, Dict, Tuple

from .utils import guess_service

class PortScanner:
    """Multithreaded TCP port scanner.

    - hosts: list of host strings
    - ports: list of integer ports
    """
    def __init__(self, hosts: List[str], ports: List[int],
                 timeout: float = 1.0, threads: int = 100):
        self.hosts = hosts
        self.ports = ports
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

    def _scan_one(self, host: str, port: int):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        try:
            err = s.connect_ex((host, port))
            if err == 0:
                status = 'open'
            else:
                status = 'closed'
        except Exception as e:
            status = f'error:{e}'
        finally:
            try:
                s.close()
            except Exception:
                pass

        service = guess_service(port)
        with self.results_lock:
            self.results.append({'host': host, 'port': port, 'status': status, 'service': service})
            self.finished_jobs += 1

    def _worker(self):
        while True:
            try:
                host, port = self.job_q.get_nowait()
            except queue.Empty:
                return
            self._scan_one(host, port)
            self.job_q.task_done()

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
