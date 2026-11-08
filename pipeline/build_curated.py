"""
Build the curated Ramayana Explorer dataset from the raw starter CSVs.

    raw (data/raw/*.csv)  ->  build_curated.py  ->  curated (data/curated/*.csv)  ->  validate.py

Why a separate curated layer (think dbt staging -> marts):
  * The raw starter pack is kept untouched, so every fix below is reviewable and re-runnable.
  * Joins in the raw pack use free-text names (Events.Primary_Location, Battles.Location,
    Battles.Side_A/B). The curated layer replaces them with surrogate-key foreign keys.
  * PRD sections 8.3 / FR-09 / FR-12 require IDs, semantic relationship groups and provenance
    fields the raw pack does not have.

Header convention: curated column names use spaced Title Case ("Event ID"). Tableau keeps such
headers verbatim as field captions, which is what the data app queries by.

Provenance convention (PRD FR-12): every row carries a "Source Note".
  * STARTER  = row came from the user's starter pack (still needs edition-level verification).
  * EDITORIAL = row/field was added during curation (2026-11) and must be reviewed.

Usage:  python3 pipeline/build_curated.py
"""
from __future__ import annotations

import csv
import logging
from pathlib import Path

from story_content import MAP_COORDS, NARRATIVE, TITLE_OVERRIDES

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "curated"

STARTER = "Starter dataset - verify against chosen Valmiki Ramayana edition"
EDITORIAL = "Editorial addition (curation 2026-11) - requires review"

log = logging.getLogger("build_curated")


# --------------------------------------------------------------------------------------------
# IO helpers
# --------------------------------------------------------------------------------------------
def read(name: str) -> list[dict[str, str]]:
    # utf-8-sig strips the BOM the raw files carry (it would otherwise corrupt the first header).
    with open(RAW / f"{name}.csv", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def ascii_safe(value):
    """Tableau's text (CSV) connector reads packaged files in a legacy single-byte codepage, so
    non-ASCII text (Devanagari) makes live queries fail with 'internal-error'. Store such text as
    \\uXXXX escapes; the apps decode it on display."""
    if not isinstance(value, str) or value.isascii():
        return value
    value = value.replace("\u2014", "-").replace("\u2013", "-")   # dashes -> hyphen
    return value if value.isascii() else value.encode("unicode_escape").decode("ascii")


def write(name: str, rows: list[dict], columns: list[str]) -> None:
    rows = [{k: ascii_safe(v) for k, v in r.items()} for r in rows]
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.csv"
    with open(path, "w", encoding="utf-8", newline="") as fh:  # no BOM on output
        w = csv.DictWriter(fh, fieldnames=columns, extrasaction="raise")
        w.writeheader()
        w.writerows(rows)
    log.info("wrote %-28s %4d rows", path.name, len(rows))


# --------------------------------------------------------------------------------------------
# Lookups / mappings (the "business logic" of the curation)
# --------------------------------------------------------------------------------------------
# Kanda enrichment: English gloss, scope note (PRD open decision #2: Uttara is shown, qualified),
# and the Story-mode chapter title + intro. Titles/intros are EDITORIAL paraphrase - review them.
KANDA_EXTRA = {
    "K01": ("Book of Youth", "", "The Beginning",
            "In Ayodhya, King Dasharatha's long wait for heirs ends with the birth of four sons. The sage "
            "Vishvamitra takes young Rama out into the wider world, and the chapter closes with the breaking "
            "of Shiva's bow and Rama's marriage to Sita."),
    "K02": ("Book of Ayodhya", "", "The Great Exile",
            "On the eve of Rama's coronation, Kaikeyi calls in two old boons. Rama accepts fourteen years of "
            "exile to keep his father's word, and Sita and Lakshmana go with him. Ayodhya is left grieving, "
            "and Bharata refuses a throne he believes is not his."),
    "K03": ("Book of the Forest", "", "Into the Forest",
            "Deep in the Dandaka forest, life among the hermitages gives way to danger. An encounter with "
            "Shurpanakha sets off a chain of events, and a golden deer draws Rama away while Ravana carries "
            "Sita off towards Lanka."),
    "K04": ("Book of Kishkindha", "", "The Alliance",
            "Searching for Sita, Rama meets Hanuman and the exiled Vanara prince Sugriva. A pact is sealed, "
            "Vali falls, and search parties go out in every direction until the vulture Sampati points them "
            "south, to Lanka."),
    "K05": ("The Beautiful Book", "", "Hanuman's Mission",
            "Hanuman leaps the ocean alone. In the Ashoka grove he finds Sita, gives her Rama's ring, confronts "
            "Ravana's court and returns with the news everyone has been waiting for."),
    "K06": ("Book of War", "", "The Great War",
            "With Vibhishana at his side, Rama's army bridges the sea. Kumbhakarna and Indrajit fall, Rama "
            "faces Ravana, and the long exile ends with a return to Ayodhya and a coronation."),
    "K07": ("The Final Book",
            "Qualified section: many scholars treat Uttara Kanda as a later layer; "
            "only one summary event is modelled.",
            "The Later Story",
            "The final book follows Rama's reign and the later lives of Sita and their sons, Lava and Kusha. "
            "Because its textual history is debated, it appears here as a short, qualified epilogue."),
}

# Real Kanda names in Devanagari (Valmiki Ramayana). Used as the chapter headings in the story app.
KANDA_DEVANAGARI = {
    "K01": "बालकाण्ड", "K02": "अयोध्याकाण्ड",
    "K03": "अरण्यकाण्ड", "K04": "किष्किन्धाकाण्ड",
    "K05": "सुन्दरकाण्ड", "K06": "युद्धकाण्ड",
    "K07": "उत्तरकाण्ड",
}

# Faction drives colour in the network / character views. Derived from People_or_Lineage,
# with explicit overrides where lineage and narrative allegiance differ.
FACTION_BY_LINEAGE = {
    "Ikshvaku": "Ayodhya & Mithila", "Videha": "Ayodhya & Mithila",
    "Vanara": "Kishkindha", "Riksha": "Kishkindha",
    "Rakshasa": "Lanka",
    "Sage": "Sages & Forest", "Human": "Sages & Forest", "Nishada": "Sages & Forest",
    "Bird": "Sages & Forest",
}

# Narrative side in the central conflict - kept separate from Faction on purpose:
# Vibhishana is Lanka by faction but on Rama's side.
SIDE_OVERRIDES = {"C015": "Neutral / Other", "C031": "Neutral / Other", "C036": "Neutral / Other",
                  "C021": "Ravana's side"}

ALIASES = {
    "C001": "Raghava; Ramachandra; Dasharathi",
    "C002": "Janaki; Vaidehi; Maithili",
    "C003": "Saumitri",
    "C013": "Anjaneya; Maruti; Vayuputra",
    "C020": "Dashanana; Lankeshvara",
    "C024": "Meghanada",
    "C022": "Bibhishana",
}

DISPLAY_NAMES = {"C024": "Meghnad (Indrajit)"}

# New character needed so Battles B001 can reference a Character ID instead of free text.
NEW_CHARACTERS = [
    {"Character ID": "C041", "Character": "Tataka", "Description": "Yakshi-turned-rakshasi slain by Rama while escorting Vishvamitra",
     "People or Lineage": "Rakshasa", "Role": "Antagonist", "Associated Location": "Siddhashrama",
     "First Kanda ID": "K01", "Last Kanda ID": "K01"},
]

# Events.Primary_Location -> Location ID. Two raw names had no match in Locations:
#   "Lanka campaign" (E035, Vibhishana's refuge): he reaches Rama's camp on the mainland shore
#                    before the crossing -> Southern Coast (L013).
EVENT_LOCATION_FIX = {"Lanka campaign": "L013"}
BATTLE_LOCATION_FIX = {"Siddhashrama region": "L003"}

# 31 raw Event_Type labels -> 5 filterable categories (PRD FR-02 "event category").
EVENT_CATEGORY = {
    "Court and lineage": "Court & Lineage", "Birth": "Court & Lineage", "Marriage": "Court & Lineage",
    "Succession": "Court & Lineage", "Regency": "Court & Lineage", "Coronation": "Court & Lineage",
    "Later reign": "Court & Lineage",
    "Exile": "Exile & Journey", "Journey": "Exile & Journey", "Return": "Exile & Journey",
    "Mission": "Exile & Journey", "Search": "Exile & Journey",
    "Battle": "Conflict & War", "Conflict trigger": "Conflict & War", "Confrontation": "Conflict & War",
    "Climax": "Conflict & War", "Trial": "Conflict & War", "Abduction": "Conflict & War",
    "Deception": "Conflict & War", "Mobilisation": "Conflict & War",
    "Alliance": "Alliance & Guidance", "Guidance": "Alliance & Guidance", "Defection": "Alliance & Guidance",
    "Call to adventure": "Alliance & Guidance", "Encounter": "Alliance & Guidance",
    "Discovery": "Alliance & Guidance", "Communication": "Alliance & Guidance",
    "Recognition": "Alliance & Guidance",
    "Turning point": "Dharma & Consequence", "Consequence": "Dharma & Consequence",
    "Dharma": "Dharma & Consequence", "Sacrifice": "Dharma & Consequence",
    "Aftermath": "Dharma & Consequence",
}

# 17 raw relationship labels -> 6 semantic groups (PRD FR-09).
REL_GROUP = {
    "Spouse": "Marriage",
    "Brother": "Family", "Sibling": "Family", "Son": "Family", "Daughter": "Family", "Father": "Family",
    "Ally": "Alliance", "Friend": "Alliance", "Associate": "Alliance", "Rescuer": "Alliance",
    "Devotee and ally": "Service & Devotion", "Devotee": "Service & Devotion",
    "Mentor": "Guidance", "Guide": "Guidance", "Teacher and guide": "Guidance", "Royal sage": "Guidance",
    "Captor": "Conflict", "Brother and rival": "Conflict", "Adversary": "Conflict",
    "Protector": "Alliance",
}

# Key adversarial / marital links missing from the raw pack (a Ramayana network without
# Rama-Ravana is misleading).
NEW_RELATIONSHIPS = [
    ("C020", "C001", "Adversary", "Ravana and Rama are the central adversaries"),
    ("C003", "C024", "Adversary", "Lakshmana defeats Indrajit"),
    ("C001", "C015", "Adversary", "Rama kills Vali in support of Sugriva"),
    ("C017", "C014", "Ally", "Angada serves Sugriva in the search and war"),
    ("C029", "C001", "Devotee", "Shabari awaits and honours Rama"),
    ("C036", "C002", "Protector", "Trijata comforts Sita in the Ashoka grove"),
    ("C007", "C006", "Spouse", "Kaushalya and Dasharatha"),
    ("C008", "C006", "Spouse", "Kaikeyi and Dasharatha"),
    ("C009", "C006", "Spouse", "Sumitra and Dasharatha"),
    ("C011", "C041", "Adversary", "Vishvamitra directs Rama against Tataka"),
]

# Missing participation rows. Raw bridge left 17/44 events with no participants and 18/40
# characters with no events. (event, character, role)
NEW_BRIDGE = [
    ("E001", "C006", "Primary"), ("E001", "C040", "Supporting"), ("E001", "C012", "Supporting"),
    ("E002", "C001", "Primary"), ("E002", "C003", "Primary"), ("E002", "C004", "Primary"),
    ("E002", "C005", "Primary"), ("E002", "C006", "Supporting"), ("E002", "C007", "Supporting"),
    ("E002", "C008", "Supporting"), ("E002", "C009", "Supporting"),
    ("E003", "C011", "Primary"), ("E003", "C006", "Primary"), ("E003", "C012", "Supporting"),
    ("E004", "C001", "Primary"), ("E004", "C003", "Primary"), ("E004", "C011", "Supporting"),
    ("E005", "C030", "Primary"), ("E005", "C001", "Primary"), ("E005", "C011", "Supporting"),
    ("E006", "C010", "Supporting"), ("E006", "C011", "Supporting"),
    ("E007", "C001", "Primary"), ("E007", "C002", "Primary"), ("E007", "C006", "Supporting"),
    ("E008", "C012", "Supporting"),
    ("E009", "C006", "Primary"),
    ("E010", "C006", "Supporting"),
    ("E011", "C001", "Primary"),
    ("E012", "C037", "Primary"), ("E012", "C001", "Primary"), ("E012", "C002", "Supporting"),
    ("E012", "C003", "Supporting"),
    ("E013", "C038", "Primary"), ("E013", "C001", "Primary"),
    ("E014", "C001", "Primary"), ("E014", "C002", "Primary"), ("E014", "C003", "Primary"),
    ("E015", "C007", "Supporting"),
    ("E016", "C001", "Primary"), ("E016", "C012", "Supporting"),
    ("E018", "C001", "Primary"), ("E018", "C002", "Primary"), ("E018", "C003", "Primary"),
    ("E018", "C039", "Supporting"),
    ("E019", "C001", "Primary"), ("E019", "C003", "Primary"),
    ("E020", "C001", "Primary"), ("E020", "C033", "Supporting"),
    ("E021", "C001", "Primary"), ("E021", "C002", "Supporting"),
    ("E023", "C020", "Primary"), ("E023", "C002", "Supporting"),
    ("E024", "C001", "Primary"),
    ("E025", "C001", "Primary"), ("E025", "C003", "Supporting"),
    ("E026", "C001", "Primary"), ("E026", "C014", "Primary"), ("E026", "C013", "Supporting"),
    ("E027", "C001", "Primary"), ("E027", "C031", "Supporting"),
    ("E028", "C014", "Primary"), ("E028", "C013", "Supporting"), ("E028", "C017", "Supporting"),
    ("E028", "C016", "Supporting"),
    ("E029", "C013", "Supporting"), ("E029", "C017", "Supporting"), ("E029", "C016", "Supporting"),
    ("E030", "C016", "Supporting"),
    ("E031", "C036", "Supporting"),
    ("E032", "C013", "Primary"), ("E032", "C002", "Primary"),
    ("E033", "C020", "Primary"),
    ("E034", "C013", "Primary"), ("E034", "C001", "Primary"),
    ("E035", "C001", "Primary"), ("E035", "C020", "Supporting"),
    ("E036", "C001", "Primary"),
    ("E037", "C001", "Primary"), ("E037", "C020", "Primary"), ("E037", "C013", "Supporting"),
    ("E037", "C014", "Supporting"), ("E037", "C017", "Supporting"), ("E037", "C032", "Supporting"),
    ("E038", "C001", "Primary"),
    ("E040", "C021", "Supporting"),
    ("E041", "C002", "Primary"), ("E041", "C001", "Primary"),
    ("E042", "C002", "Primary"), ("E042", "C003", "Supporting"), ("E042", "C013", "Supporting"),
    ("E043", "C002", "Supporting"), ("E043", "C004", "Supporting"), ("E043", "C012", "Supporting"),
    ("E044", "C001", "Primary"), ("E044", "C002", "Primary"),
]

# Battles: free-text sides -> participant bridge with Character IDs; plus a link to the matching
# event where one exists. (battle, related event, [(character, side)])
BATTLE_LINKS = {
    "B001": ("", [("C001", "A"), ("C003", "A"), ("C041", "B")]),
    "B002": ("E020", [("C001", "A"), ("C034", "B"), ("C035", "B")]),
    "B003": ("E027", [("C001", "A"), ("C014", "A"), ("C015", "B")]),
    "B004": ("E033", [("C013", "A"), ("C020", "B")]),
    "B005": ("E037", [("C001", "A"), ("C003", "A"), ("C013", "A"), ("C014", "A"), ("C017", "A"),
                      ("C022", "A"), ("C020", "B"), ("C023", "B"), ("C024", "B")]),
    "B006": ("E038", [("C001", "A"), ("C013", "A"), ("C023", "B")]),
    "B007": ("E039", [("C003", "A"), ("C022", "A"), ("C024", "B")]),
    "B008": ("E040", [("C001", "A"), ("C020", "B")]),
}


def confidence_for(modern_association: str, location: str) -> str:
    """PRD 12.8 labels. Rules are deliberately conservative."""
    text = modern_association.lower()
    if location in {"Ashoka Grove"}:
        return "Textual"
    if "debated" in text or "varies" in text or "proposed" in text:
        return "Proposed identification" if "debated" in text else "Unverified"
    if "traditional" in text:
        return "Traditional association"
    return "Unverified"


# --------------------------------------------------------------------------------------------
# Builders - one per curated table
# --------------------------------------------------------------------------------------------
def build_kandas():
    rows = []
    for r in read("Kandas"):
        gloss, scope, title, intro = KANDA_EXTRA[r["Kanda_ID"]]
        rows.append({"Kanda ID": r["Kanda_ID"], "Kanda": r["Kanda"], "Kanda Order": r["Sequence"],
                     "English Gloss": gloss, "Summary": r["Summary"], "Scope Note": scope,
                     "Kanda Devanagari": KANDA_DEVANAGARI[r["Kanda_ID"]],
                     "Chapter Title": title, "Story Intro": intro,
                     "Source Note": STARTER + "; chapter title/intro are editorial"})
    write("Kandas", rows, list(rows[0]))


def build_locations():
    rows = []
    for r in read("Locations"):
        rows.append({"Location ID": r["Location_ID"], "Location": r["Location"],
                     "Location Type": r["Location_Type"], "Region or People": "" if r["Region_or_People"].strip() == "\u2014" else r["Region_or_People"],
                     "Modern Association": r["Modern_Association"],
                     "Story Significance": r["Story_Significance"],
                     "Confidence Label": confidence_for(r["Modern_Association"], r["Location"]),
                     "Map Latitude": MAP_COORDS.get(r["Location_ID"], ("", ""))[0],
                     "Map Longitude": MAP_COORDS.get(r["Location_ID"], ("", ""))[1],
                     "Source Note": STARTER})
    write("Locations", rows, list(rows[0]))
    return {r["Location"]: r["Location ID"] for r in rows}


def build_characters():
    raw = read("Characters")
    rows = []
    for r in raw:
        rows.append({k.replace("_", " "): v for k, v in r.items()} | {"Source Note": STARTER})
    rows += [c | {"Source Note": EDITORIAL} for c in NEW_CHARACTERS]
    for r in rows:  # names readers use (user request: "Meghnad")
        r["Character"] = DISPLAY_NAMES.get(r["Character ID"], r["Character"])
    for r in rows:
        cid = r["Character ID"]
        r["Aliases"] = ALIASES.get(cid, "")
        r["Faction"] = FACTION_BY_LINEAGE[r["People or Lineage"]]
        if cid in SIDE_OVERRIDES:
            r["Narrative Side"] = SIDE_OVERRIDES[cid]
        elif r["Role"] in {"Antagonist", "Catalyst"}:
            r["Narrative Side"] = "Ravana's side"
        elif r["Role"] == "Rival":
            r["Narrative Side"] = "Neutral / Other"
        else:
            r["Narrative Side"] = "Rama's side"
    cols = ["Character ID", "Character", "Aliases", "Description", "People or Lineage", "Faction",
            "Narrative Side", "Role", "Associated Location", "First Kanda ID", "Last Kanda ID",
            "Source Note"]
    write("Characters", rows, cols)


def build_events(loc_ids: dict[str, str]):
    rows = []
    for r in read("Events"):
        name = r["Primary_Location"]
        loc = loc_ids.get(name) or EVENT_LOCATION_FIX.get(name, "")
        fixed = name in EVENT_LOCATION_FIX
        sensitive = "interpretive" in r["Chronology_Note"] or "debate" in r["Chronology_Note"] \
            or "vary" in r["Chronology_Note"]
        rows.append({"Event ID": r["Event_ID"], "Event": TITLE_OVERRIDES.get(r["Event_ID"], r["Event"]), "Kanda ID": r["Kanda_ID"],
                     "Narrative Order": r["Sequence"], "Location ID": loc,
                     "Event Type": r["Event_Type"], "Event Category": EVENT_CATEGORY[r["Event_Type"]],
                     "Summary": r["Summary"], "Chronology Note": r["Chronology_Note"],
                     "Confidence Label": "Interpretive - see note" if sensitive else "Textual (paraphrase)",
                     "Key Moment": "Y" if r["Event_ID"] in NARRATIVE else "N",
                     "Narrative": NARRATIVE.get(r["Event_ID"], ""),
                     "Source Note": EDITORIAL + " (location remapped)" if fixed else STARTER})
    write("Events", rows, list(rows[0]))


def build_bridge():
    rows = [{"Event ID": r["Event_ID"], "Character ID": r["Character_ID"],
             "Participation Role": r["Participation_Role"], "Source Note": STARTER}
            for r in read("Event_Character_Bridge")]
    seen = {(r["Event ID"], r["Character ID"]) for r in rows}
    for e, c, role in NEW_BRIDGE:
        if (e, c) in seen:
            log.warning("bridge row %s/%s already present - skipped", e, c)
            continue
        seen.add((e, c))
        rows.append({"Event ID": e, "Character ID": c, "Participation Role": role,
                     "Source Note": EDITORIAL})
    rows.sort(key=lambda r: (r["Event ID"], r["Participation Role"] != "Primary", r["Character ID"]))
    # Surrogate key: a single-column unique key keeps VDS from collapsing rows.
    for i, r in enumerate(rows, 1):
        r["Participation ID"] = f"P{i:03d}"
    write("Event_Character_Bridge", rows,
          ["Participation ID", "Event ID", "Character ID", "Participation Role", "Source Note"])


def build_relationships():
    rows = [{"From Character ID": r["From_Character_ID"], "To Character ID": r["To_Character_ID"],
             "Relationship Type": r["Relationship_Type"], "Context": r["Context"], "Source Note": STARTER}
            for r in read("Relationships")]
    rows += [{"From Character ID": a, "To Character ID": b, "Relationship Type": t, "Context": c,
              "Source Note": EDITORIAL} for a, b, t, c in NEW_RELATIONSHIPS]
    for i, r in enumerate(rows, 1):
        r["Relationship ID"] = f"R{i:03d}"
        r["Relationship Group"] = REL_GROUP[r["Relationship Type"]]
    write("Relationships", rows, ["Relationship ID", "From Character ID", "To Character ID",
                                  "Relationship Type", "Relationship Group", "Context", "Source Note"])


def build_battles(loc_ids: dict[str, str]):
    rows, parts = [], []
    for order, r in enumerate(read("Battles"), 1):
        bid = r["Battle_ID"]
        event_id, sides = BATTLE_LINKS[bid]
        loc = loc_ids.get(r["Location"]) or BATTLE_LOCATION_FIX[r["Location"]]
        rows.append({"Battle ID": bid, "Battle": r["Battle"], "Battle Order": order,
                     "Kanda ID": r["Kanda_ID"], "Event ID": event_id, "Location ID": loc,
                     "Side A": r["Side_A"], "Side B": r["Side_B"], "Outcome": r["Outcome"],
                     "Notes": r["Notes"], "Source Note": STARTER})
        for cid, side in sides:
            parts.append({"Battle ID": bid, "Character ID": cid, "Side": side, "Source Note": EDITORIAL})
    for i, p in enumerate(parts, 1):
        p["Battle Participant ID"] = f"BP{i:03d}"
    write("Battles", rows, list(rows[0]))
    write("Battle_Participants", parts, ["Battle Participant ID", "Battle ID", "Character ID", "Side",
                                         "Source Note"])


def build_journey():
    rows = [{"Journey Stop ID": f"J{int(r['Journey_Sequence']):02d}",
             "Journey Order": r["Journey_Sequence"], "Location ID": r["Location_ID"],
             "Story Milestone": r["Story_Milestone"], "Kanda ID": r["Kanda_ID"], "Source Note": STARTER}
            for r in read("Journey")]
    write("Journey", rows, list(rows[0]))


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    build_kandas()
    loc_ids = build_locations()
    build_characters()
    build_events(loc_ids)
    build_bridge()
    build_relationships()
    build_battles(loc_ids)
    build_journey()


if __name__ == "__main__":
    main()
