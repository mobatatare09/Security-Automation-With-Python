import re
import sys
from collections import Counter

def parse_auth_log(filepath):
    failed_logins = Counter()
    successful_logins = Counter()

    with open(filepath) as f:
        for line in f:
            # Failed password
            match = re.search(r'Failed password for (\S+) from (\S+)', line)
            if match:
                user, ip = match.groups()
                failed_logins[ip] += 1

            # Accepted password
            match = re.search(r'Accepted password for (\S+) from (\S+)', line)
            if match:
                user, ip = match.groups()
                successful_logins[ip] += 1

    print("\n=== FAILED LOGIN ATTEMPTS ===")
    for ip, count in failed_logins.most_common(10):
        flag = " ⚠️  BRUTE FORCE" if count > 5 else ""
        print(f"  {ip}: {count} attempts{flag}")

    print("\n=== SUCCESSFUL LOGINS ===")
    for ip, count in successful_logins.most_common(10):
        print(f"  {ip}: {count} logins")

    # Check for successful login after many failures (compromise indicator)
    print("\n=== COMPROMISE INDICATORS ===")
    for ip in failed_logins:
        if ip in successful_logins and failed_logins[ip] > 5:
            print(f"  ⚠️  {ip}: {failed_logins[ip]} failures then {successful_logins[ip]} successes — POSSIBLE COMPROMISE")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 log_parser.py /var/log/auth.log")
        sys.exit(1)
    parse_auth_log(sys.argv[1])
