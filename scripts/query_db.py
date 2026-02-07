#!/usr/bin/env python3
import subprocess
import json
import argparse
import time

# Default DB Path
DB_PATH = "/etc/pihole/pihole-FTL.db"

def run_sqlite(query):
    """Run SQL query via sudo sqlite3"""
    cmd = ["sudo", "sqlite3", DB_PATH, query]
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode().strip()
        return result
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode().strip()}"

def get_summary(hours=24):
    timestamp = int(time.time()) - (hours * 3600)
    
    # Total Queries
    total = run_sqlite(f"SELECT count(*) FROM queries WHERE timestamp >= {timestamp};")
    
    # Blocked Queries (Status 1,4,5,6,7,8,9,10,11,14,15 are various block types)
    blocked = run_sqlite(f"SELECT count(*) FROM queries WHERE timestamp >= {timestamp} AND status IN (1,4,5,6,7,8,9,10,11,14,15);")
    
    # Top Client
    top_client = run_sqlite(f"SELECT client FROM queries WHERE timestamp >= {timestamp} GROUP BY client ORDER BY count(client) DESC LIMIT 1;")
    
    # Percent
    try:
        pct = (int(blocked) / int(total) * 100) if int(total) > 0 else 0
    except:
        pct = 0.0

    return {
        "period_hours": hours,
        "total_queries": int(total) if total.isdigit() else 0,
        "blocked_queries": int(blocked) if blocked.isdigit() else 0,
        "percent_blocked": round(pct, 2),
        "top_client": top_client
    }

def get_top_domains(limit=10, hours=24):
    timestamp = int(time.time()) - (hours * 3600)
    query = f"SELECT domain, count(domain) FROM queries WHERE timestamp >= {timestamp} GROUP BY domain ORDER BY count(domain) DESC LIMIT {limit};"
    raw = run_sqlite(query)
    
    results = []
    if raw and "Error" not in raw:
        for line in raw.split('\n'):
            if '|' in line:
                parts = line.split('|')
                results.append({"domain": parts[0], "count": int(parts[1])})
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query Pi-hole FTL Database")
    parser.add_argument("--summary", action="store_true", help="Get summary stats")
    parser.add_argument("--top", type=int, help="Get top N domains")
    parser.add_argument("--hours", type=int, default=24, help="Time window in hours (default: 24)")
    
    args = parser.parse_args()
    
    output = {}
    
    if args.summary:
        output["summary"] = get_summary(args.hours)
        
    if args.top:
        output["top_domains"] = get_top_domains(args.top, args.hours)
        
    print(json.dumps(output, indent=2))
