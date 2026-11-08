# Ramayana Storybook (v4): design
- Datasources (6 embedded CSVs, found by caption): Events (has Key Moment + Narrative), Kandas
  (Devanagari names), Characters, Locations (Map Latitude/Longitude), Event Participation, Journey.
- Layout: a 46/54 grid at 100vh. The right column = centred text block + a fixed nav bar
  (Cover, the path, and the 7 short Devanagari Kanda names, plus sub-dots for the moments in the
  current Kanda). Arrow keys turn pages.
- Left panel: an image from images.js (moment -> Kanda fallback); otherwise a typographic plate
  (Kanda name in Devanagari plus a caption) on a per-Kanda tint.
- Map: geo.js holds the subcontinent + Sri Lanka coastline (Natural Earth 1:110m, countries
  unioned, so there are no political borders), drawn as a framed plate with a sea fill. Stops are
  projected with the same equirectangular function. "Trace the journey" animates the 12 stops
  every 900 ms. The return leg is a dashed gold line.
- Test: test/storybook_test.js fails if any page needs scrolling at 1440x900 or 1280x800.
