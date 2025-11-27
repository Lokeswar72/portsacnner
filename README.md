# Network Port Scanner

A simple, fast, and multithreaded TCP port scanner written in Python. This tool allows you to scan hosts for open ports and generates reports in both CSV and HTML formats.

**Disclaimer:** This tool is intended for educational purposes and for use on systems and networks you own or are explicitly authorized to test. Unauthorized scanning of networks is illegal.

## Features

- **Multithreaded Scanning:** Utilizes multiple threads to scan ports concurrently for high speed.
- **Flexible Target Selection:** Scan a single host, a comma-separated list of hosts, or a simple last-octet IP range (e.g., `192.168.1.10-20`).
- **Flexible Port Selection:** Scan a predefined list of common ports, a single port, a comma-separated list, or a range (e.g., `80,443,8000-8100`).
- **Dual Report Generation:** Automatically creates both a `.csv` file and a styled `.html` report for easy analysis.
- **Organized Output:** All reports are saved into a dedicated `reports/` directory.
- **Protocol Selection:** Choose between TCP, UDP, or both.
- **Customizable:** Adjust the thread count and socket timeout for your specific needs.

## Setup

1.  **Clone or download the repository.**

2.  **Navigate to the project directory:**
    ```bash
    cd "c:\Users\lokes\Desktop\port scanner"
    ```

3.  **Create and activate a Python virtual environment:**
    ```bash
    # Create the virtual environment
    python -m venv .venv

    # Activate on Windows
    .\.venv\Scripts\activate
    ```

## Usage

The main script is `run_scanner.py`. You must provide a target host and a port selection.

### Examples

**Scan a single host for the most common ports:**
```bash
python run_scanner.py --host 127.0.0.1 --common
```

**Scan a single host for a specific range of ports:**
```bash
python run_scanner.py --host example.com --ports 20-1024
```

**Scan a range of hosts for specific ports:**
```bash
python run_scanner.py --host 192.168.1.10-20 --ports 22,80,443
```

**Scan with an increased number of threads and a shorter timeout:**
```bash
python run_scanner.py --host example.com --common --threads 200 --timeout 0.5
```

After a scan is complete, the report files will be saved in the `reports/` directory.