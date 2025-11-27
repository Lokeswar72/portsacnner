# scanner/__init__.py
"""network-port-scanner package"""

__all__ = ["core", "utils", "reports"]

DEFAULT_TIMEOUT = 1.0
DEFAULT_THREADS = 100
COMMON_PORTS = [
    20,21,22,23,25,53,80,110,111,135,139,143,161,389,443,445,
    587,631,993,995,1433,1521,1723,2049,3306,3389,5060,5900,8080
]
