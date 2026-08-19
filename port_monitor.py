import subprocess
import json
import os
import sys
from datetime import datetime

BASELINE_FILE = "port_baseline.json"

def get_open_ports(target):
    result = subprocess.run(
        ['nmap', '-sS', '--top-ports', '100', '-oG', '-', target],
        capture_output=True, text=True
    )
    ports = []
    for line in result.stdout.split('\n'):
        if '/open/' in line:
            for part in line.split():
                if '/open/' in part:
                    port = part.split('/')[0]
                    ports.append(int(port))
    return sorted(ports)

def save_baseline(target, ports):
    data = {"target": target, "ports": ports, "timestamp": str(datetime.now())}
    with open(BASELINE_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Baseline saved: {len(ports)} open ports on {target}")

def compare_with_baseline(target, current_ports):
    if not os.path.exists(BASELINE_FILE):
        print("No baseline found. Creating one now...")
        save_baseline(target, current_ports)
        return

    with open(BASELINE_FILE) as f:
        baseline = json.load(f)

    old_ports = set(baseline["ports"])
    new_ports = set(current_ports)

    opened = new_ports - old_ports
    closed = old_ports - new_ports

    if opened:
        print(f"\n⚠️  NEW PORTS OPENED: {sorted(opened)}")
    if closed:
        print(f"\n✓ PORTS CLOSED: {sorted(closed)}")
    if not opened and not closed:
        print("\n✓ No changes detected since baseline")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: sudo python3 port_monitor.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    ports = get_open_ports(target)
    print(f"Current open ports on {target}: {ports}")
    compare_with_baseline(target, ports)
