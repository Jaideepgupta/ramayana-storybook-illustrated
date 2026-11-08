# Ramayana Explorer — Product Requirements Document (PRD)

**Product:** Ramayana Explorer  
**Product type:** Tableau Cloud Data App / interactive data-storytelling experience  
**Source tradition:** Valmiki Ramayana  
**Document status:** Detailed implementation baseline — v1.0  
**Prepared:** 8 November 2026  
**Primary audience:** Product owner, Tableau developer, data modeller, QA reviewer

---

## 1. Executive summary

Ramayana Explorer is an interactive, research-aware digital exploration of the Valmiki Ramayana. It combines narrative navigation with analytical exploration so that a user can move from a Kanda to an event, from an event to its participating characters, and from a character to their relationships, locations and appearances elsewhere in the epic.

The product is intended to be implemented as a Tableau Data App on Tableau Cloud. Tableau dashboards provide the visual and analytical layer; the Data App experience provides navigation and a connected, multi-view workflow. The initial release uses a curated, generated starter dataset rather than a live external API.

**Product principle:** this is not a verse repository or a claim to establish historical geography. It is a structured, explorable representation of selected narrative information, with source notes and uncertainty made visible.

## 2. Product vision and objectives

### Vision

Make the epic easier to explore through a visually rich, connected and transparent data experience.

### Objectives

1. Provide an overview of all seven Kandas.
2. Make important characters discoverable through profiles and connected events.
3. Present major events in narrative order.
4. Explore traditional place associations and Rama's journey without presenting uncertain identifications as proven fact.
5. Explain character relationships by type: family, marriage, alliance, service, conflict and other.
6. Provide a focused Yuddha Kanda experience for battles, participants and outcomes.
7. Demonstrate Tableau's strengths in cross-filtering, dashboard actions, parameter-driven navigation and data storytelling.
8. Keep the data model extensible so that additional verses, translations, citations and regional traditions can be added later.

### Success criteria

- A user can reach any major section in no more than two navigation actions from the landing page.
- Selecting a Kanda filters its events and relevant characters consistently.
- Selecting a character reveals their profile, event participation, relationships and associated locations.
- Timeline order is stable and reproducible.
- Every interpretive or geographic claim has a source note or an explicit uncertainty label.
- The initial app works without external API calls or third-party CDN dependencies.

## 3. Users and use cases

| Persona | Need | Example task |
|---|---|---|
| Curious reader | Understand the overall story | Browse the seven Kandas and key events |
| Student | Explore a character or episode | Find every selected event involving Hanuman |
| Educator | Explain story structure visually | Show the exile-to-Lanka narrative sequence |
| Research-oriented reader | Inspect data provenance | Review source notes and confidence labels |
| Tableau portfolio reviewer | Evaluate BI implementation | Test navigation, actions, filters and data modelling |

## 4. Scope

### In scope for release 1

- Landing / overview dashboard
- Kanda explorer
- Character explorer
- Event explorer and narrative timeline
- Journey / location explorer
- Relationship network
- Yuddha Kanda battle explorer
- Shared filters and dashboard actions
- Dataset documentation and provenance fields
- Responsive desktop-first layout with tablet consideration

### Out of scope for release 1

- Full Sanskrit text or complete verse-by-verse translation
- Audio narration or generated voice acting
- Claims of archaeological proof or definitive identification of every place
- Live external APIs, user accounts, comments or social features
- Automated Sanskrit transliteration or machine translation
- Exhaustive comparison of every Ramayana tradition
- A complete scholarly critical edition apparatus

## 5. Information architecture

```text
Ramayana Explorer
├── Home / Overview
│   ├── Seven Kandas
│   ├── Story highlights
│   └── Explore by theme
├── Kanda Explorer
│   ├── Kanda summary
│   ├── Events in narrative order
│   └── Key characters
├── Character Explorer
│   ├── Character profile
│   ├── Event participation
│   ├── Relationships
│   └── Associated locations
├── Event Explorer
│   ├── Event detail
│   ├── Participants
│   ├── Kanda and sequence
│   └── Related events
├── Journey Explorer
│   ├── Location sequence
│   ├── Location detail
│   └── Events at / associated with location
├── Relationship Explorer
│   ├── Character network
│   └── Relationship type
└── Yuddha Kanda
    ├── Battle overview
    ├── Battle detail
    ├── Participants / sides
    └── Outcome and narrative notes
```

## 6. Functional requirements

### FR-01 — Global navigation
The app must expose consistent navigation to Overview, Kandas, Characters, Timeline, Journey, Relationships and Yuddha Kanda. The current section must be visually identifiable.

### FR-02 — Global filters
Where relevant, users must be able to filter by Kanda, character, event category and location. Filters must have clear reset behaviour. Avoid filters that create contradictory or empty states without explanation.

### FR-03 — Overview
Show headline counts for Kandas, characters, selected events, locations, relationships and battles. Show event distribution by Kanda and a short list of featured characters/events. Counts must be calculated from the connected dataset, not hard-coded in dashboard text.

### FR-04 — Kanda explorer
Display all seven Kandas in canonical sequence. Selecting a Kanda filters the event list, timeline and character participation views. Each Kanda page includes a concise paraphrased summary and editorial/source note.

### FR-05 — Character explorer
Show name, role, description, aliases where supplied, family/affiliation context, associated events and relationship links. A character selection must filter linked events and locations. Do not infer personality traits or biography beyond the documented narrative record.

### FR-06 — Event explorer
Show event title, Kanda, narrative sequence, summary, event category, location association and participating characters. Provide navigation to the event's Kanda and character profiles.

### FR-07 — Timeline
Render selected events in stable narrative order using a numeric sequence field. The timeline must not imply absolute historical dates. If multiple ordering interpretations are possible, store the ordering convention in metadata.

### FR-08 — Journey explorer
Show ordered journey milestones and their associated places. Where coordinates exist, use a map. Every modern location association must include a confidence / evidence note. Do not calculate or display precise route distance unless coordinates and route methodology have been reviewed.

### FR-09 — Relationships
Show source and target characters, relationship type and short explanatory note. Allow filtering by relationship type. Avoid treating all connections as equivalent: parent, sibling, spouse, ally, servant/devotee and adversary are different semantic types.

### FR-10 — Yuddha Kanda
Show selected battle episodes, participating characters, sides, outcome and event sequence. Battle summaries must remain concise and clearly labelled as paraphrases.

### FR-11 — Cross-dashboard actions
A selection in one view must update related views where a valid relationship exists. Use Tableau filter actions, highlight actions and navigation actions deliberately; provide a clear way to clear selections.

### FR-12 — Source and editorial notes
Every record must be traceable to a source note or marked as an editorial starter entry requiring verification. Display an app-level note explaining that summaries are paraphrases and the dataset is not a critical edition.

## 7. Non-functional requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-01 | Performance | Main dashboard should render in under 5 seconds on a normal broadband connection, subject to Tableau Cloud performance |
| NFR-02 | Usability | Consistent navigation, clear titles, readable tooltips and visible filter state |
| NFR-03 | Accessibility | High contrast, meaningful labels, keyboard-operable controls where supported |
| NFR-04 | Reliability | No dependency on external APIs for core app operation |
| NFR-05 | Maintainability | Stable IDs, documented joins, reusable calculations and named worksheets |
| NFR-06 | Data integrity | No duplicate primary keys; bridge tables support many-to-many participation |
| NFR-07 | Trust | Source note and uncertainty label for interpretive/geographic data |
| NFR-08 | Responsive design | Desktop-first, with tablet layout checked before release |

## 8. Dataset and data model

The starter workbook contains nine sheets:

| Table | Purpose | Starter row count |
|---|---|---:|
| Kandas | Seven books / sections | 7 |
| Characters | Character master | 40 |
| Events | Selected narrative events | 44 |
| Locations | Story locations / traditional associations | 20 |
| Relationships | Typed character-to-character links | 31 |
| Battles | Selected battle episodes | 8 |
| Journey | Ordered journey milestones | 12 |
| Event_Character_Bridge | Many-to-many event participation | 38 |
| Read_Me | Dataset documentation | 7 |

Counts describe the generated starter dataset and may change as records are reviewed and expanded.

### 8.1 Logical model

```text
Kandas (1) ──────── (*) Events (*) ──────── (*) Characters
                           │                     ▲
                           │                     │
                           ▼                     │
                     Locations (*)          Event_Character_Bridge
                           ▲
                           │
                     Journey (*) 

Characters (source) ─── Relationships ─── Characters (target)

Battles (*) ─── associated Kanda / event / participant references
```

### 8.2 Recommended Tableau relationships

Use logical relationships rather than flattening all tables into one physical join unless a specific view requires it.

- `Kandas.Kanda_ID` → `Events.Kanda_ID` (one-to-many)
- `Events.Event_ID` → `Event_Character_Bridge.Event_ID` (one-to-many)
- `Characters.Character_ID` → `Event_Character_Bridge.Character_ID` (one-to-many)
- `Locations.Location_ID` → `Events.Location_ID` where a single primary location is assigned
- `Characters.Character_ID` → `Relationships.Source_Character_ID` (one-to-many)
- `Characters.Character_ID` → `Relationships.Target_Character_ID` (second role-playing relationship; if the Tableau model cannot express this cleanly, use two aliases / duplicated logical tables)
- `Kandas.Kanda_ID` → `Battles.Kanda_ID` (one-to-many)
- `Locations.Location_ID` → `Journey.Location_ID` (one-to-many)

**Important:** event participation is many-to-many and must be represented by `Event_Character_Bridge`. Do not join Characters directly to Events without the bridge if that would duplicate event-level measures.

### 8.3 Key fields to maintain

- Every entity table: stable unique ID.
- Events: `Narrative_Order`, `Kanda_ID`, `Event_Category`, `Summary`, `Location_ID` (nullable), `Source_Note`, `Confidence_Label`.
- Characters: `Character_ID`, `Display_Name`, `Role`, `Description`, `Aliases`, `Source_Note`.
- Locations: `Location_ID`, `Location_Name`, `Traditional_Association`, `Modern_Identification`, `Latitude`, `Longitude`, `Confidence_Label`, `Source_Note`.
- Relationships: `Relationship_ID`, `Source_Character_ID`, `Target_Character_ID`, `Relationship_Type`, `Relationship_Note`.
- Journey: `Journey_Order`, `Location_ID`, `Journey_Note`.
- Battles: `Battle_ID`, `Kanda_ID`, `Battle_Order`, `Battle_Name`, `Side_A`, `Side_B`, `Outcome_Summary`, `Source_Note`.

## 9. KPI and analytical definitions

These are descriptive coverage metrics, not claims about the historical scale or frequency of events.

| Metric | Definition |
|---|---|
| Kanda count | `COUNTD([Kanda_ID])` |
| Character count | `COUNTD([Character_ID])` |
| Selected event count | `COUNTD([Event_ID])` |
| Location count | `COUNTD([Location_ID])` |
| Relationship count | `COUNTD([Relationship_ID])` |
| Battle count | `COUNTD([Battle_ID])` |
| Events per Kanda | Distinct events grouped by Kanda |
| Character event involvement | Distinct linked events per character |
| Relationship mix | Count of relationships by relationship type |
| Journey milestone count | Distinct journey sequence records |
| Source coverage % | Records with a populated source note ÷ total records |
| Review coverage % | Records marked reviewed ÷ records requiring review |

Example Tableau calculations:

```tableau
// Event Count
COUNTD([Event_ID])

// Character Participation Count
COUNTD([Event_ID])

// Source Coverage
COUNTD(IF NOT ISNULL([Source_Note]) AND [Source_Note] <> ""
THEN [Event_ID] END)
/
COUNTD([Event_ID])

// Events per Kanda
{ FIXED [Kanda_ID] : COUNTD([Event_ID]) }
```

For the character participation calculation, use the Event_Character_Bridge context and ensure the view is at character grain. Validate all LOD behaviour against the final relationship model and filter order.

## 10. Dashboard specifications

### D-01 — Overview

**Purpose:** orient the user and reveal the structure of the epic.

Recommended layout:
- Header with title, subtitle and navigation
- KPI strip: Kandas, characters, events, locations, battles
- Seven-Kanda selector / sequence
- Events by Kanda bar chart
- Featured characters by linked event count
- Featured narrative events
- Editorial note / source coverage indicator

Interactions:
- Click a Kanda to navigate to its explorer and filter related content.
- Click a character to open their profile.
- Click a featured event to open event detail.

### D-02 — Kanda Explorer

- Seven Kanda navigation cards in canonical order.
- Selected Kanda summary and key themes.
- Events in narrative order.
- Character participation list.
- Related locations.
- Previous / next Kanda navigation.

### D-03 — Character Explorer

- Character selector with search.
- Profile and role.
- Related-character network or compact connection list.
- Events involving selected character.
- Kanda distribution of their appearances.
- Associated locations.
- Relationship-type filter.

### D-04 — Event Timeline

- Narrative timeline sorted by `Narrative_Order`.
- Kanda colour / section label.
- Event detail tooltip.
- Character participation.
- Location association.
- Filters for Kanda, character and event category.

### D-05 — Journey Explorer

- Map with geocoded records only.
- Ordered journey milestone list.
- Selected location details and associated events.
- Confidence label and source note.
- A non-map fallback list for records without coordinates.

### D-06 — Relationships

- Character network or adjacency table.
- Relationship type legend.
- Selected character's incoming and outgoing relationships.
- Detail panel for the selected link.
- Avoid an overcrowded all-character graph; default to one selected character and its immediate connections.

### D-07 — Yuddha Kanda

- Battle count and key participants.
- Battle sequence.
- Side / faction comparison.
- Battle detail and outcome summary.
- Related character profiles and events.

## 11. Visual and interaction design

### Visual direction

- Warm parchment background with restrained texture.
- Deep maroon / oxblood headers.
- Antique gold accents and saffron highlights.
- Forest green for journey / nature context.
- Dark ink for body text.
- Indian miniature-inspired illustration as supporting artwork, not as a substitute for data labels.

### Design rules

- Prioritise readable data labels over ornament.
- Use consistent colours for Kandas and relationship types.
- Keep decorative images in banners, chapter cards and profile areas.
- Use a small set of reusable image assets; do not load external images from a CDN.
- Provide text alternatives / captions for meaningful images.
- Avoid implying that an illustrative image is a primary textual source.

## 12. Data quality, source and editorial policy

The generated dataset is a demo foundation, not a scholarly critical edition.

1. Use Valmiki Ramayana as the intended source tradition.
2. Summaries are paraphrases; do not present them as verse translations or direct quotations.
3. Before public release, choose and record a specific edition / translation / reference convention.
4. Add source references at event and character record level.
5. Treat Uttara Kanda and episodes with textual variation carefully; disclose the editorial scope.
6. Distinguish narrative sequence from absolute chronology.
7. Distinguish traditional place association from modern geographic identification.
8. Add confidence labels such as `Textual`, `Traditional association`, `Proposed identification`, and `Unverified`.
9. Avoid invented dates, distances, coordinates, genealogies or causal claims.
10. Have a knowledgeable reviewer validate summaries and relationships before describing the app as scholarly.

## 13. Acceptance criteria

- [ ] All seven Kandas appear in the correct sequence.
- [ ] Overview counts reconcile to the source tables.
- [ ] Every event has a unique ID and valid Kanda reference.
- [ ] Every bridge row has a valid Event_ID and Character_ID.
- [ ] Character filters return only linked events.
- [ ] Relationship view distinguishes relationship types.
- [ ] Timeline order uses the documented narrative sequence field.
- [ ] Location view clearly distinguishes coordinates from traditional associations.
- [ ] Yuddha Kanda shows only records assigned to that scope.
- [ ] Dashboard actions have a visible reset / clear-selection path.
- [ ] Source and uncertainty notes are accessible from relevant views.
- [ ] No critical feature depends on an external API or CDN.
- [ ] Tableau Cloud publishing, permissions and Data App navigation are tested.

## 14. Delivery plan

| Phase | Work | Deliverable |
|---|---|---|
| 1. Foundation | Confirm source convention, audit starter data, IDs and relationships | Reviewed data model and data dictionary |
| 2. Tableau model | Connect workbook, define relationships and validate grain | Published data source / workbook model |
| 3. Core dashboards | Overview, Kanda, Character and Timeline | Core interactive dashboards |
| 4. Advanced views | Journey, Relationships and Yuddha Kanda | Complete dashboard suite |
| 5. Data App | Navigation, cross-dashboard actions, styling and responsive checks | Integrated Data App |
| 6. QA and release | Reconciliation, source review, performance and access tests | Release candidate and handover |

Indicative effort: approximately 4–6 weeks for a solo developer, depending on source verification, Tableau Data App environment readiness and the depth of the relationship/network views.

## 15. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Textual variation across editions | Conflicting event details | Select one source convention and record alternatives |
| Ambiguous modern place identification | Misleading map | Confidence labels; map only reviewed coordinates |
| Many-to-many join duplication | Inflated metrics | Use bridge table and logical relationships |
| Dense character network | Poor usability | Default to selected-character neighbourhood |
| Over-designed interface | Reduced readability | Keep ornament secondary to content |
| Data App platform / origin restrictions | Deployment delay | Keep release self-contained and validate site settings early |
| Generated starter data errors | Incorrect storytelling | Editorial review before public release |

## 16. Release 2 opportunities

- Verse / sarga references and passage-level citations.
- Multiple translations with edition metadata.
- Comparison of Valmiki Ramayana with selected regional retellings.
- More complete character genealogy.
- Thematic explorer: dharma, devotion, exile, kingship, loyalty.
- Search by Sanskrit name, transliteration and aliases.
- Teacher / classroom guided journeys.
- User bookmarks and curated reading paths, subject to platform capability.

## 17. Starter deliverables in this package

- `Ramayana_Explorer_PRD.md` — this requirements document.
- `assets/` — cropped visual concept references for cover, character, journey, timeline, battle, relationship and Kanda views.
- `data/Ramayana_Explorer_Data.xlsx` — generated nine-sheet starter workbook.
- `data/Ramayana_Explorer_Data_Pack.zip` — CSV version of the starter data.
- `README.md` — package guide and limitations.

## 18. Open decisions before production

1. Which specific Valmiki Ramayana edition / translation will be the reference standard?
2. Should Uttara Kanda be included in the default experience or marked as a separately qualified section?
3. Which place associations have sufficient evidence to receive coordinates?
4. Will the app be public-facing or an internal / portfolio demonstration?
5. Which Tableau Cloud project and publishing permissions will be used for the release?

---

**End of PRD.**
