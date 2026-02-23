import csv
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "leaderboard" / "leaderboard.csv"
# CHANGED: Now matches the uppercase filename
MD_PATH = ROOT / "leaderboard" / "LEADERBOARD.md"

def read_rows():
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Standardize keys to lowercase for internal sorting logic
        rows = []
        for r in reader:
            # Handle both 'Team' and 'team' / 'MAE' and 'score'
            row = {k.lower(): v for k, v in r.items()}
            if (row.get("team") or "").strip():
                rows.append(row)
    return rows

def main():
    rows = read_rows()
    
    # Sort by MAE (Ascending - lower is better for MAE)
    def score_key(r):
        try:
            # Check for 'mae' first, then 'score'
            val = r.get("mae") or r.get("score")
            return float(val)
        except:
            return float("inf") # Use infinity so errors go to the bottom

    # Sort: Lower MAE first
    rows.sort(key=score_key)

    lines = []
    lines.append("# 🏆 Leaderboard\n")
    lines.append("This leaderboard is **auto-updated** when a submission PR is merged.\n\n")

    lines.append("| Rank | Team | MAE Score |\n")
    lines.append("|:---:|---|---:|\n")
    
    for i, r in enumerate(rows, start=1):
        team = (r.get("team") or "Unknown").strip()
        mae = (r.get("mae") or r.get("score") or "N/A").strip()
        lines.append(f"| {i} | {team} | {mae} |\n")

    MD_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"Successfully rendered to {MD_PATH.name}")

if __name__ == "__main__":
    main()