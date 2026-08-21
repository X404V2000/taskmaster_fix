from typing import Dict, List
from collections import defaultdict

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

def parse_attempts(raw_log: List[str]) -> List[Dict]:
    attempts = []
    for line in raw_log:
        ip, username, success, timestamp = line.split(",")
        attempts.append({
            "ip": ip,
            "username": username,
            "success": success,
            "timestamp": timestamp,
        })
    return attempts

def count_failures(attempts: List[Dict]) -> Dict[str, int]:
    failures = defaultdict(int)
    for attempt in attempts:
        if attempt["success"] == "False":
            failures[attempt["ip"]] += 1
    return dict(failures)

def build_alert(ip: str, count: int, tags: Dict = None) -> Dict:
    if tags is None:
        tags = {}
    tags["ip"] = ip
    tags["failed_count"] = count
    return tags

def flag_suspicious(attempts: List[Dict], threshold: int = 3) -> List[Dict]:
    failure_counts = count_failures(attempts)  # one pass, all IPs
    alerts = []
    for ip, fail_count in failure_counts.items():
        if fail_count >= threshold:
            alerts.append(build_alert(ip, fail_count))
    return alerts

def main():
    try:
        attempts = parse_attempts(RAW_LOG)
        alerts = flag_suspicious(attempts)
        for alert in alerts:
            print(f"ALERT: {alert['ip']} has {alert['failed_count']} failed attempts")
        print(f"\nSummary: {len(alerts)} suspicious IP(s) detected.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
