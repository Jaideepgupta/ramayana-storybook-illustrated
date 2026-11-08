"""Harness for apps wired to the single published source "Ramayana Story Data": the mock returns
rows of data/curated/Ramayana_Story_Data.csv (same file uploaded to Tableau). Measures come back
under their alias, like VDS. Pass --fail to make every live query reject (tests the fallback)."""
import csv, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "app")
FAIL = "--fail" in sys.argv
CONTENT = next((APP / "Packages").glob("*/content"))
NUM = {"Kanda Order", "Narrative Order", "Journey Order", "Map Latitude", "Map Longitude"}
rows = [{k: (None if v == "" else float(v) if k in NUM else v) for k, v in r.items()}
        for r in csv.DictReader(open(ROOT / "data/curated/Ramayana_Story_Data.csv", encoding="utf-8"))]
cols = list(rows[0])
mock = """
window.__ROWS__ = %s; window.__COLS__ = %s; window.__FAIL__ = %s;
window.tableau = { extensions: { initializeAsync: () => Promise.resolve(), workbook: {
  getAllDataSourcesAsync: () => Promise.resolve([{ name: 'Ramayana Story Data', id: 'x',
    readMetadataAsync: () => Promise.resolve({ data: __COLS__.map(c => ({ fieldCaption: c })) }),
    queryAsync: (q) => __FAIL__ ? Promise.reject({ errorCode: 'internal-error', message: 'error' })
      : Promise.resolve({ data: __ROWS__.map(r => Object.fromEntries(q.fields.map(f => [f.fieldAlias || f.fieldCaption, r[f.fieldCaption]]))) })
  }]) } } };""" % (json.dumps(rows), json.dumps(cols), "true" if FAIL else "false")
html = (CONTENT / "index.html").read_text().replace(
    '<script src="src/tableau.extensions.1.latest.min.js"></script>', "<script>" + mock + "</script>")
out = CONTENT / "__harness.html"
out.write_text(html)
print(out)
