"""
Login Monitor
--------------
Reads a log of login attempts and flags any IP address with
3 or more FAILED attempts as suspicious.

Expected output when you run this file as-is:

    ALERT: 41.13.9.201 has 3 failed attempts
    ALERT: 105.22.61.4 has 4 failed attempts

    Summary: 2 suspicious IP(s) detected.

But something's off. Find and fix the bugs so the output above
is actually what you get. There is more than one bug.
"""

from typing import Dict, List


RAW_LOG = [
    "41.13.9.201,admin,False,09:01",
    "41.13.9.201,admin,False,09:02",
    "41.13.9.201,root,False,09:03",
    "105.22.61.4,admin,False,10:15",
    "105.22.61.4,admin,True,10:16",
    "105.22.61.4,admin,False,10:17",
    "105.22.61.4,admin,False,10:18",
    "105.22.61.4,admin,False,10:19",
    "8.8.8.8,user1,True,11:00",
    "8.8.8.8,user1,False,11:01",
]


def parse_attempts(log_lines: List[str]) -> List[Dict]:
    attempts = []
    for line in log_lines:
        ip, username, success, timestamp = line.split(",")
        attempts.append({
            "ip": ip,
            "username": username,
            "success": success,
            "timestamp": timestamp,
        })
    return attempts


def count_failures(attempts: List[Dict], ip: str) -> int:
    count = 0
    for attempt in attempts:
        if attempt["ip"] == ip and attempt["success"] == False:
            count += 1
    return count


def build_alert(ip, count: int, tags={}) -> Dict:
    tags["ip"] = ip
    tags["failed_count"] = count
    return tags


def flag_suspicious(attempts: List[Dict], threshold: int = 3) -> List[Dict]:
    seen_ips = []
    alerts = []
    for attempt in attempts:
        ip = attempt["ip"]
        if ip in seen_ips:
            continue
        seen_ips.append(ip)

        fail_count = count_failures(attempts, ip)
        if fail_count > threshold:
            alert = build_alert(ip, fail_count)
            alerts.append(alert)
    return alerts


def main():
    try:
        attempts = parse_attempts(RAW_LOG)
        alerts = flag_suspicious(attempts)

        for alert in alerts:
            print(f"ALERT: {alert['ip']} has {alert['failed_count']} failed attempts")

        print(f"\nSummary: {len(alerts)} suspicious IP(s) detected.")
    except Exception:
        pass


if __name__ == "__main__":
    main()
