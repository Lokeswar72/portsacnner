# scanner/reports.py
import datetime
import csv
from typing import List, Dict

def write_csv(results: List[Dict], host_label: str) -> str:
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    fname = f'scan_report_{host_label}_{ts}.csv'
    keys = ['host', 'port', 'status', 'service']
    with open(fname, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in sorted(results, key=lambda r: (r['host'], r['port'])):
            writer.writerow(row)
    return fname


def write_html(results: List[Dict], host_label: str) -> str:
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    fname = f'scan_report_{host_label}_{ts}.html'
    rows = []
    for r in sorted(results, key=lambda r: (r['host'], r['port'])):
        status = r['status']
        cls = 'open' if status == 'open' else 'closed'
        rows.append(f"<tr><td>{r['host']}</td><td>{r['port']}</td><td>{r['service']}</td><td class='{cls}'>{status}</td></tr>")

    html = f'''<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <title>Scan report {host_label}</title>
  <style>
    body{{font-family: Arial, Helvetica, sans-serif}}
    table{{border-collapse: collapse; width: 100%}}
    td, th{{border: 1px solid #ddd; padding: 8px}}
    tr:nth-child(even){{background-color: #f9f9f9}}
    tr:hover{{background-color: #f1f1f1}}
    .open{{color: green; font-weight: bold}}
    .closed{{color: #666}}
  </style>
</head>
<body>
  <h2>Scan report for {host_label}</h2>
  <p>Generated: {datetime.datetime.now().isoformat()}</p>
  <table>
    <thead><tr><th>Host</th><th>Port</th><th>Service</th><th>Status</th></tr></thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</body>
</html>
'''
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    return fname
