import sys
import json
import urllib.request

def check_ip_virustotal(ip):
    # Note: requires free API key from virustotal.com
    print(f"\nChecking {ip}...")

    # Check using AbuseIPDB (free, no key needed for basic check)
    try:
        url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}"
        # For actual use, you need an API key
        print(f"  Check manually: https://www.virustotal.com/gui/ip-address/{ip}")
        print(f"  Check manually: https://www.abuseipdb.com/check/{ip}")
        print(f"  Check manually: https://www.shodan.io/host/{ip}")
    except Exception as e:
        print(f"  Error: {e}")

def check_ips_from_file(filepath):
    with open(filepath) as f:
        for line in f:
            ip = line.strip()
            if ip and not ip.startswith('#'):
                check_ip_virustotal(ip)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ip_checker.py <ip_or_file>")
        sys.exit(1)

    arg = sys.argv[1]
    if '.' in arg and not arg.endswith('.txt'):
        check_ip_virustotal(arg)
    else:
        check_ips_from_file(arg)
