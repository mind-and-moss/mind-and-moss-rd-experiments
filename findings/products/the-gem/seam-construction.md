# The Gem — Seam Construction (Invisible Bond Lines)

> **⚠️ Scope note:** "The Gem" is a small component within The Machine, not a standalone product — see `concept.md`. Invisible-seam techniques here apply to the gem-component glass element specifically.

How the glass panels of the gem element actually get joined. The visual goal is "invisible seam — looks bonded by nothing." This file covers seam method ranking, resin/adhesive choices, and the bond-line dimensional specs that drive the whole fabrication approach. The custom edge grinder that physically achieves these specs lives in `topics/fabrication/glass-edge-grinder.md`.

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
Build a custom belt grinder/sander to polish the EDGES of glass panels (up to 2 ft long) for **invisible silicone-seam construction**. Spot-polishing isn't accurate enough — need full-edge consistency.

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
- The bond-line specs Isaiah pasted in came from another bot — worth confirming source if used in production decisions
