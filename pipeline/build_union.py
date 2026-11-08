"""
Combine the curated tables the storybook needs into ONE CSV, so the data can be published to
Tableau as a single published data source (one upload). Each row carries a "Record Type"
(Kanda, Event, Character, Location, Participation, Journey); unused columns stay blank.

Why: live queries from a data app against CSV files *packaged inside* the workbook failed on
Tableau Cloud with 'internal-error'; published data sources are the supported query target.
"""
import csv
from pathlib import Path

CUR = Path(__file__).resolve().parent.parent / "data" / "curated"
TABLES = [("Kanda", "Kandas"), ("Event", "Events"), ("Character", "Characters"),
          ("Location", "Locations"), ("Participation", "Event_Character_Bridge"), ("Journey", "Journey")]

rows, cols = [], ["Record Type", "Record ID"]
for rtype, name in TABLES:
    with open(CUR / f"{name}.csv", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for c in reader.fieldnames:
            if c not in cols:
                cols.append(c)
        for r in reader:
            key = next(iter(r))                       # first column is the table's primary key
            rows.append({"Record Type": rtype, "Record ID": f"{rtype}:{r[key]}", **r})

out = CUR / "Ramayana_Story_Data.csv"
with open(out, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
text = out.read_text(encoding="utf-8")
assert text.isascii(), "union CSV must be ASCII"
print(f"wrote {out.name}: {len(rows)} rows x {len(cols)} columns")
