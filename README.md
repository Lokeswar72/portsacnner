  ____           _    ____                                  
 |  _ \ ___  ___| |_ / ___|  ___ __ _ _ __  _ __   ___ _ __ 
 | |_) / _ \/ __| __| |  _  / __/ _` | '_ \| '_ \ / _ \ '__|
 |  __/  __/\__ \ |_| |_| || (_| (_| | | | | | | |  __/ |   
 |_|   \___||___/\__|\____| \___\__,_|_| |_|_| |_|\___|_|   

!Python Version
!License

A simple, fast, and multithreaded port scanner written in Python. This tool allows you to scan hosts for open ports by actively "knocking" on them to check their status. It works for both TCP and UDP protocols and generates reports in CSV and HTML formats.

**Disclaimer:** This tool is intended for educational purposes and for use on systems and networks you own or are explicitly authorized to test. Unauthorized scanning of networks is illegal.

## Table of Contents

- Features
- Scan Output
- Setup
- Usage

## Features

🚀 **Multithreaded Scanning:** Utilizes multiple threads to scan ports concurrently for high speed.
🎯 **Flexible Target Selection:** Scan a single host, a comma-separated list of hosts, or a simple last-octet IP range (e.g., `192.168.1.10-20`).
ポート **Flexible Port Selection:** Scan a predefined list of common ports, a single port, a comma-separated list, or a range (e.g., `80,443,8000-8100`).
📜 **Dual Report Generation:** Automatically creates both a `.csv` file and a styled `.html` report for easy analysis.
📂 **Organized Output:** All reports are saved into a dedicated `reports/` directory.
🔄 **Protocol Selection:** Choose between TCP, UDP, or `both`.
⚙️ **Customizable:** Adjust the thread count and socket timeout for your specific needs.

## Scan Output

The scanner provides real-time progress in the terminal and generates two report files.

### Terminal Output

```
[*] Starting TCP scan: hosts=1 ports=138 threads=100 timeout=1.0s
Progress: 138/138 (100.0%)
[*] TCP scan finished in 0.85s.
[*] Starting UDP scan: hosts=1 ports=138 threads=100 timeout=1.0s
Progress: 138/138 (100.0%)
[*] UDP scan finished in 2.15s.

[*] All scans finished in 3.00s. 276 total results recorded.
[*] Reports written: reports\scan_report_127_0_0_1_20251127_052011.csv, reports\scan_report_127_0_0_1_20251127_052011.html
[*] Done.
```

### HTML Report

A clean, modern, and responsive HTML report is generated for easy viewing in any browser. The enhanced design makes it simple to analyze scan results at a glance.

*(Tip: A screenshot of your new HTML report would look great here!)*

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

The main script is `cli.py`. You must provide a target host and a port selection.

### Examples

**1. Scan a single host for the most common TCP ports:**
```bash
python cli.py --host 127.0.0.1 --common
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