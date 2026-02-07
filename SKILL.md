---
name: pihole-ctl
description: Manage and monitor local Pi-hole instance. Query FTL database for statistics (blocked ads, top clients) and control service via CLI. Use when user asks "how many ads blocked", "pihole status", or "update gravity".
---

# Pi-hole Controller

## Usage
- **Role**: Network Guardian.
- **Trigger**: "Check Pi-hole", "Adblock status", "Who is querying top domains?".
- **Output**: JSON stats or CLI command results.

## Capabilities
1.  **Statistics**: Query FTL database for accurate logs (Last 24h, Top Domains).
2.  **Management**: Enable/Disable blocking (`pihole enable/disable`).
3.  **Blocklists**: Update Gravity (`pihole -g`).
4.  **Audit**: Identify chatty clients or top blocked domains.

## Scripts
- `scripts/query_db.py`: Python wrapper for `sqlite3` to fetch stats safely.
  - Usage: `python3 scripts/query_db.py --summary --hours 24`
  - Usage: `python3 scripts/query_db.py --top 10`

## Reference Materials
- [Database Schema](references/db-schema.md)
