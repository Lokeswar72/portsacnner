# ⚡ Python Port Scanner

A **simple, fast, and multithreaded port scanner** written in Python. This tool actively scans hosts for open TCP and UDP ports and generates reports in both CSV and HTML formats.

> ⚠️ **Disclaimer:** This tool is intended for **educational purposes** and for use on systems and networks you **own or are authorized to test**. Unauthorized scanning of external networks is **illegal**.

---

## 📑 Table of Contents
- [Features](#-features)
- [Scan Output](#-scan-output)
- [Setup](#-setup)
- [Usage](#-usage)
- [License](#-license)

---

## 🚀 Features

- **Multithreaded Scanning:** Leverages concurrent threads to perform scans at high speed.  
- **Flexible Target Selection:**  
  Scan a single host, multiple hosts (comma-separated), or a simple IP range (e.g., `192.168.1.10-20`).
- **Flexible Port Selection:**  
  Define ports as a list (`80,443`), a range (`8000-8100`), or use a predefined set of common ports.
- **Dual Report Generation:**  
  Automatically creates both `.csv` and `.html` reports for easy viewing and analysis.
- **Organized Output:**  
  Reports are stored neatly in a dedicated `reports/` directory.
- **Protocol Support:**  
  Supports **TCP**, **UDP**, or scanning **both**.
- **Highly Customizable:**  
  Adjust thread count, socket timeout, and protocol options to match your needs.

---

## 📊 Scan Output

The scanner provides **real-time terminal progress** and generates **two report files** upon completion.

### 🖥 Terminal Output

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

### 🌐 HTML Report

A **modern, responsive HTML report** is generated for browser viewing.  
The clean design allows quick insights into scan results.

> 💡 *Tip: Add a screenshot of your generated HTML report here for visual reference!*

---

## ⚙️ Setup

1. **Clone or download the repository:**
   ```bash
   git clone https://github.com/yourusername/port-scanner.git
   cd port-scanner
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   # Create the virtual environment
   python -m venv .venv

   # Activate on Windows
   .\.venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧭 Usage

The main entry point is `cli.py`. You must specify at least one host and a port selection.

### 🔹 Examples

**1. Scan a single host for the most common TCP ports:**
```bash
python cli.py --host 127.0.0.1 --common
```

**2. Scan a host for a specific range of ports:**
```bash
python run_scanner.py --host example.com --ports 20-1024
```

**3. Scan a range of hosts for specific ports:**
```bash
python run_scanner.py --host 192.168.1.10-20 --ports 22,80,443
```

**4. Increase thread count and reduce timeout for faster scanning:**
```bash
python run_scanner.py --host example.com --common --threads 200 --timeout 0.5
```

After the scan completes, results will be saved in the `reports/` directory.

---

## 🧾 License

This project is open-source and available under the **MIT License**.  
Feel free to use, modify, and distribute responsibly.

---

## 🐍 Python Version

Compatible with **Python 3.8+**
