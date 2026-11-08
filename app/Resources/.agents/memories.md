# Ramayana Storybook (v4): notes
- Key-moment prose, title overrides and map coordinates live in pipeline/story_content.py (editorial;
  needs review). Prose follows Valmiki and avoids later popular additions.
- The user calls Indrajit "Meghnad", so C024 is displayed as "Meghnad (Indrajit)".
- The map shows traditional associations, placed approximately (the caption says so). Dandaka is
  only a centroid of a broad region.
- The user will supply the illustrations (docs/IMAGE_BRIEF.md). Until then, typographic plates.
- Tableau Personal Space does not support folders; a "Ramayan" project must be created on the site.
- 2026-11-08: live queryAsync against packaged CSVs failed on Tableau Cloud (internal-error, all versions). The app now reads a bundled snapshot (src/data.js, built by pipeline/build_snapshot.py). To go live later, publish data/curated/Ramayana_Story_Data.csv as a published data source and switch boot() back to load().
- 2026-11-08 (later): wired to the PUBLISHED source "Ramayana_Story_Data" (project Others/Ramayan), uploaded
  by the user from data/curated/Ramayana_Story_Data.csv (pipeline/build_union.py). One table; rows are
  split by [Record Type]. Numeric fields are measures there, so they are queried as MIN(...) AS <name>.
  If the live query fails, the app falls back to src/data.js and shows a small note under the nav.
- To change the data: edit the pipeline, run build_curated.py + build_union.py + build_snapshot.py, re-upload
  the CSV to the same published source (overwrite), and republish the workbook only if code changed.
- 2026-11-08 (v4.1): added a mini-map inset on Kanda/moment pages (places with coordinates for that Kanda or
  moment; clicking it opens the Path page), a "Who's who" page (editorial FEATURED cast, 4 per world, with
  the Characters.Description), a closing page (॥ इति ॥ with a data-driven "About this storybook" section), and
  resume reading (localStorage key 'ramayana-storybook:page', guarded). Zoom-to-fit (min 0.62) keeps
  every page scroll-free in short Tableau frames. Re-wired with 32 fields (adds Description/Faction/Role).
