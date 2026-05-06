# Findings — Mind and Moss R&D

This folder is the topic-organized knowledge base for Mind and Moss research. Originally the research lived in chronological "excavation" files (`RESEARCH-001`, `-002`, etc.) — one per source AI conversation sweep. That format made it hard to look up a single topic (e.g. "everything I know about silicone bond lines") because info was scattered across multiple files.

This reorg flattens that out by **topic**, not by **excavation date**. The original excavation files are preserved intact under `archive/` as the audit trail.

## Map

```
findings/
  README.md                ← you are here
  archive/                 ← raw excavation files, untouched (audit trail)
  products/                ← things actively in development
    the-machine/           ← lead product: room-scale racetrack aquarium / industrial brutalism + ecosystem. Includes gem.md (gem-component) and base-materials.md inside.
    cylindrical-terrarium/ ← existing sealed cylinder build
  concepts/                ← unvalidated ideas + random inventions (flat .md files)
  topics/                  ← cross-cutting research used across products (AI-conversation excavation)
    fabrication/           ← print prep, mold-making, glass grinding, etc.
    ecosystem/             ← bioactive systems, isopods, plants, humidity
    materials/             ← acrylic, glass, silicone, UV adhesives, etc.
    cad-and-modeling/      ← Blender, Plasticity, iPad workflows
    electronics/           ← LED wiring, soldering, etc.
  references/              ← external/curated sources (datasheets, suppliers, forums) — parallel to topics/
  business/                ← brand, pricing, sourcing, product categories
```

`topics/` and `references/` cover the same subject areas with different content rules. `topics/` is verbatim from AI-conversation excavation. `references/` is human-curated external sources — manufacturer datasheets, hobbyist forums, supplier links. See `references/README.md` for the convention.

## How to navigate

- **"What does this product look like?"** → `products/<name>/concept.md`
- **"How is X built / fabricated?"** → start in `products/<name>/`, fall back to `topics/fabrication/` or `topics/materials/`
- **"What do we know about <material>?"** → `topics/materials/<material>.md`
- **"Is there an idea floating around about ___?"** → `concepts/`
- **"Where did this fact originally come from?"** → every section in every file is tagged with a `Source:` line pointing back to the original Thread in `archive/`. Open the matching `archive/RESEARCH-00X-*.md` and search by Thread number.
- **"Is there a manufacturer datasheet / forum / video for this?"** → `references/<topic-area>/`. AI excavation in `topics/` is for ideation; `references/` is for primary sources.

## Citation convention

Every chunk of content in every file carries a header like:

```
Source: RESEARCH-002 Thread 5 — "Clay substrates for terrariums"
```

If a file pulls from multiple Threads, each section gets its own `Source:` header. This means content in this folder can be re-traced to the exact original conversation it came from.

## Rule for new content

- Zero summarization — content is moved verbatim, only relocated and re-headed. Lists stay lists, tables stay tables.
- New excavation passes (RESEARCH-005, -006, ...) land in `archive/` first, then get migrated into the topic structure as a follow-up pass.
- New unvalidated ideas go into `concepts/` as a single `.md` file. See `concepts/README.md` for the rule on when a concept graduates into `products/`.
