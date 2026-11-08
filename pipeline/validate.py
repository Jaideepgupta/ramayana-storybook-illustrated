"""
Data tests for the curated layer - the dbt `unique` / `not_null` / `relationships` /
`accepted_values` pattern, in plain Python so it runs anywhere (CI, pre-commit, before packaging).

Exit code 0 = all tests pass, 1 = at least one failure. Run after build_curated.py:

    python3 pipeline/build_curated.py && python3 pipeline/validate.py
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

CURATED = Path(__file__).resolve().parent.parent / "data" / "curated"

failures: list[str] = []


def load(name: str) -> list[dict[str, str]]:
    with open(CURATED / f"{name}.csv", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def check(ok: bool, msg: str) -> None:
    print(("  PASS " if ok else "  FAIL ") + msg)
    if not ok:
        failures.append(msg)


def unique(rows, col, table):
    vals = [r[col] for r in rows]
    dups = sorted({v for v in vals if vals.count(v) > 1})
    check(not dups, f"{table}.{col} unique {dups or ''}")


def not_null(rows, col, table):
    n = sum(1 for r in rows if not r[col].strip())
    check(n == 0, f"{table}.{col} not null ({n} nulls)")


def relationship(rows, col, parent, pcol, table, nullable=False):
    keys = {r[pcol] for r in parent}
    bad = sorted({r[col] for r in rows if (r[col] or not nullable) and r[col] not in keys})
    check(not bad, f"{table}.{col} -> {pcol} {bad or ''}")


def accepted(rows, col, values, table):
    bad = sorted({r[col] for r in rows} - set(values))
    check(not bad, f"{table}.{col} accepted values {bad or ''}")


def main() -> int:
    K, C, E, L = load("Kandas"), load("Characters"), load("Events"), load("Locations")
    R, B, BP = load("Relationships"), load("Battles"), load("Battle_Participants")
    J, X = load("Journey"), load("Event_Character_Bridge")

    print("Primary keys")
    for rows, col, t in [(K, "Kanda ID", "Kandas"), (C, "Character ID", "Characters"),
                         (E, "Event ID", "Events"), (L, "Location ID", "Locations"),
                         (R, "Relationship ID", "Relationships"), (B, "Battle ID", "Battles"),
                         (BP, "Battle Participant ID", "Battle_Participants"),
                         (J, "Journey Stop ID", "Journey"), (X, "Participation ID", "Bridge")]:
        unique(rows, col, t)
        not_null(rows, col, t)

    print("Foreign keys")
    relationship(E, "Kanda ID", K, "Kanda ID", "Events")
    relationship(E, "Location ID", L, "Location ID", "Events")
    relationship(X, "Event ID", E, "Event ID", "Bridge")
    relationship(X, "Character ID", C, "Character ID", "Bridge")
    relationship(R, "From Character ID", C, "Character ID", "Relationships")
    relationship(R, "To Character ID", C, "Character ID", "Relationships")
    relationship(B, "Kanda ID", K, "Kanda ID", "Battles")
    relationship(B, "Location ID", L, "Location ID", "Battles")
    relationship(B, "Event ID", E, "Event ID", "Battles", nullable=True)
    relationship(BP, "Battle ID", B, "Battle ID", "Battle_Participants")
    relationship(BP, "Character ID", C, "Character ID", "Battle_Participants")
    relationship(J, "Location ID", L, "Location ID", "Journey")
    relationship(J, "Kanda ID", K, "Kanda ID", "Journey")
    relationship(C, "First Kanda ID", K, "Kanda ID", "Characters")
    relationship(C, "Last Kanda ID", K, "Kanda ID", "Characters")

    print("Business rules (PRD acceptance criteria)")
    check([r["Kanda Order"] for r in K] == [str(i) for i in range(1, 8)], "seven Kandas in canonical order")
    not_null(K, "Kanda Devanagari", "Kandas"); not_null(K, "Chapter Title", "Kandas"); not_null(K, "Story Intro", "Kandas")  # Story mode
    key = [r for r in E if r["Key Moment"] == "Y"]
    check(len(key) >= 7 and all(r["Narrative"].strip() for r in key), f"key moments have narration ({len(key)})")
    kandas_with_key = {r["Kanda ID"] for r in key}
    check(kandas_with_key == {r["Kanda ID"] for r in K}, "every Kanda has at least one key moment")
    J_ids = {r["Location ID"] for r in J}
    unmapped = sorted(l["Location ID"] for l in L if l["Location ID"] in J_ids and not l["Map Latitude"])
    check(not unmapped, f"every journey stop has map coordinates {unmapped or ''}")
    bad = [l["Location ID"] for l in L if l["Map Latitude"] and not (5 < float(l["Map Latitude"]) < 31 and 67 < float(l["Map Longitude"]) < 93)]
    check(not bad, f"map coordinates inside the map bbox {bad or ''}")
    orders = [int(r["Narrative Order"]) for r in E]
    check(len(set(orders)) == len(orders), "Events.Narrative Order unique (stable timeline)")
    pairs = [(r["Event ID"], r["Character ID"]) for r in X]
    check(len(set(pairs)) == len(pairs), "Bridge (Event, Character) pairs unique - no double counting")
    orphan_events = {r["Event ID"] for r in E} - {r["Event ID"] for r in X}
    check(not orphan_events, f"every event has >=1 participant {sorted(orphan_events) or ''}")
    idle = {r["Character ID"] for r in C} - {r["Character ID"] for r in X} - {r["Character ID"] for r in BP}
    check(not idle, f"every character appears in an event or battle {sorted(idle) or ''}")
    self_links = [r["Relationship ID"] for r in R if r["From Character ID"] == r["To Character ID"]]
    check(not self_links, "no self-relationships")
    accepted(R, "Relationship Group", ["Family", "Marriage", "Alliance", "Service & Devotion",
                                       "Guidance", "Conflict"], "Relationships")
    accepted(E, "Event Category", ["Court & Lineage", "Exile & Journey", "Conflict & War",
                                   "Alliance & Guidance", "Dharma & Consequence"], "Events")
    accepted(L, "Confidence Label", ["Textual", "Traditional association", "Proposed identification",
                                     "Unverified"], "Locations")
    accepted(BP, "Side", ["A", "B"], "Battle_Participants")
    for rows, t in [(K, "Kandas"), (C, "Characters"), (E, "Events"), (L, "Locations"),
                    (R, "Relationships"), (B, "Battles"), (J, "Journey"), (X, "Bridge")]:
        not_null(rows, "Source Note", t)  # FR-12: every record traceable

    print("Tableau compatibility")
    for f in sorted(CURATED.glob("*.csv")):
        text = f.read_text(encoding="utf-8")
        check(text.isascii(), f"{f.name} is pure ASCII (Tableau CSV connector is not UTF-8 safe)")

    print(f"\n{'FAILED' if failures else 'OK'}: {len(failures)} failing test(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
