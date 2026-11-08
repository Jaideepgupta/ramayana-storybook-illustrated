"""Bundle docs/ (the web edition) into one self-contained ramayana-storybook.html."""
import base64, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
d = ROOT / "docs"
read = lambda p: (d / p).read_text(encoding="utf-8")
imgs = json.loads(re.search(r"window\.RAMAYANA_IMAGES\s*=\s*(\{.*?\});", read("src/images.js"), re.S).group(1))
inline = {k: "data:image/jpeg;base64," + base64.b64encode((d / v).read_bytes()).decode() for k, v in imgs.items()}
scripts = [read("src/data.js"), read("src/geo.js"), "window.RAMAYANA_IMAGES = " + json.dumps(inline) + ";", read("src/app.js")]
assert not any("</script" in s.lower() for s in scripts)
html = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\" />\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
        "<title>Ramayana Storybook · रामायण</title>\n"
        "<meta name=\"description\" content=\"An illustrated storytelling journey through the seven Kandas of the Valmiki Ramayana.\" />\n"
        f"<style>\n{read('src/styles.css')}\n</style>\n</head>\n<body>\n<div id=\"app\"></div>\n"
        + "".join(f"<script>\n{s}\n</script>\n" for s in scripts) + "</body>\n</html>\n")
out = ROOT / "ramayana-storybook.html"
out.write_text(html, encoding="utf-8")
print(out.name, round(out.stat().st_size / 1e6, 2), "MB")
