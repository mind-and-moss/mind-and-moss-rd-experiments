# The Machine — Gem Component

The "gem" is a small featured detail within The Machine — a fused-glass sphere or hemisphere with an invisible-seam glass setting that scatters light. Not a standalone product; a sub-feature of The Machine that delivers part of the visual "wow" moment. This file consolidates everything specific to the gem-component: concept, fusing for the sphere, and invisible-seam construction for the glass setting.

Cross-cutting glass-work techniques (cutting, marking, soldering, grinding) live in `topics/fabrication/glass-fabrication.md`. The custom edge grinder that hits invisible-seam tolerances lives in `topics/fabrication/glass-edge-grinder.md`. Imitation-example references for similar glass artists live in `references/products/the-machine.md` under the gem-component section.

---

Source: RESEARCH-002 Thread 5 — "Clay substrates for terrariums" (Part C)

### Glass Fusing for Sphere/Hemisphere — Direct Gem Research
Isaiah explored making a fused glass sphere or hemisphere (the light-scattering gem component).

Kiln requirements:
- Small (6-8" spheres): Evenheat Studio Pro STP or Paragon SC-2 — ~$700-1200
- Medium (10-12"): Skutt GM1014 or Evenheat GTS — ~$2000-3000
- Look for "glass kiln" (heats from top), not "ceramic kiln" (heats from sides). Used kilns on Facebook Marketplace often half price.

COE compatibility — critical:
- Bullseye (COE 90) — most popular for art glass, huge color range
- System 96 / Spectrum / Uroboros (COE 96) — also common
- Pick one system and stay there. Mixing COEs = guaranteed cracking during cooling.
- Traditional stained glass cathedral sheets are COE 82-85 — NOT fusing-compatible. Different product entirely.

Slump molds for hemisphere shape:
- Buy: Bullseye, Slumpy's, Creative Paradise sell ceramic hemisphere molds 6"-12", ~$40-150. Best starting point.
- DIY: 50/50 plaster + silica blend, cast around a ball. Advanced, can fail if not dried fully.

---

Source: RESEARCH-002 Thread 6 — "3D CAD software for hobbyists" (Part A)

### Seam/Joinery Methods — Ranked by Achievable + Visual Impact
1. UV optical adhesive seams — most likely to make viewers ask "how is this built?" Invisible seams, glass appears bonded by nothing.
2. Hybrid: solder inside / optical adhesive outside — structural integrity + visually invisible from outside.
3. Embedded side-glow fiber — accessible, dramatic, photographs beautifully.

---

Source: RESEARCH-002 Thread 6 — "3D CAD software for hobbyists" (Part E)

### Resin Types for Seams
- UV resin (Solarez, Padico, Counter Culture DIY UV): cures in seconds, controlled flow, $15-30/bottle. Good for precise seam application.
- Polyester resin: strong odor, traditional, used in fiberglass work.
- Doming / glazing resin: self-leveling, glass-clear, thin topcoat. "Probably what's being used for the look you're describing."
- Process: build piece → clean seams (alcohol wipe, dust removal) → tape glass faces adjacent to each seam to prevent drips → mix + apply resin → cure.

---

Source: RESEARCH-004 Thread 15 — "Untitled" (chat #18 — Glass edge grinder, 100-turn deep dive)

### Project Goal
Build a custom belt grinder/sander to polish the EDGES of glass panels (up to 2 ft long) for **invisible-seam construction**. Spot-polishing isn't accurate enough — need full-edge consistency.

### The Engineering Specs (Isaiah's bond-line targets)
These are the dimensional tolerances for invisible seam to actually be invisible:

| Spec | Target | Notes |
|---|---|---|
| Silicone bond line thickness | 0.05–0.15mm (50–150µm) | Sweet spot |
| Max acceptable bond line | 0.25mm | Above this = optically visible (refractive index change) |
| Min practical bond line | 0.025mm | Below this = bonding voids |
| Edge flatness | 0.05–0.10mm along edge length | |
| Squareness (90° to face) | within 0.25° (~0.05mm across 6mm thick) | **Hardest spec to hit** |
| Edge polish | ~3000–8000 grit final | NO cerium oxide buff needed |
| Panel-to-panel dimensional | within ±0.5mm | |
| Cut squareness (corner-corner) | within 0.5° (~1mm across 6" panel) | |

> **⚠️ This spec table was verified 2026-05-05 against primary sources and found to have multiple errors.** See `topics/fabrication/glass-edge-grinder.md` for the corrected table with citations to Norland NOA datasheets, DOWSIL structural-glazing guides, and ASTM standards. The biggest issue: the silicone bond-line row conflates UV optical adhesive thicknesses (50–250 µm per Norland) with structural silicone glazing (6 mm minimum per Dow/ASTM) — two different products with different target ranges. Decide which seam type before locking the spec.

### Why Squareness is Harder than Flatness
- Flatness 0.002–0.004" over 24" = good shop tooling territory (achievable with steel platen + linear guide)
- Squareness 0.25° = where most invisible-seam attempts fail
- If sled tilts even slightly during pass = wedge-shaped edge — NO silicone film can hide it
- Geometry holding the glass perpendicular = the make-or-break

### Key Insight
Bond-line tolerance pushes the design harder than the polish does. The grinder doesn't need exotic abrasives or extreme RPM — it needs a rigid, perpendicular-holding jig and even pressure across the whole pass.

### Relation to Previous Research
- Builds on RESEARCH-002 Thread 6 ("Seam options ranked: 1) UV optical adhesive (invisible)")
- Adds the **fabrication side** of how to actually achieve the edge precision the invisible seam requires
- The bond-line specs originated from another bot — verified 2026-05-05 against primary sources, see `topics/fabrication/glass-edge-grinder.md`
