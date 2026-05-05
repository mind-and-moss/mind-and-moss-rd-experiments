# Glass Edge Grinder — Custom Build

Custom belt-grinder/sander build for polishing glass panel edges to invisible-seam tolerance. Bond-line specs that drive the design also live in `products/the-gem/seam-construction.md`.

---

Source: RESEARCH-004 Thread 15 — "Untitled" (chat #18 in sidebar) — 100-turn deep dive

This is the most important fabrication conversation in the entire excavation. Real engineering specs and a complete grinder-build approach for The Gem's invisible-seam panel construction.

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

### Grinder Build Approach
- **Format:** vertical wet belt sander, 4"×106" works for 2-ft panels
- **Grit progression:** up to 3000 grit
- **Wheel speed:** 800–1500 RPM at abrasive (finer grits OK at lower RPM)
- **Crank-and-gearbox is viable** — 5–15% RPM variation doesn't blow 0.002" flatness IF geometry is solid
- **Bicycle pedal power** discussed as input source

### Architecture Choices
- **Wheel-and-sled:** small contact patch, panel rides past it
- **Flat-platen-backed belt:** longer contact, better flatness — likely better for this spec
- Need flat reference platen, ~0.001" over working length (achievable with ground steel bar / machinist keystock + straightedge check)
- **Pressure must be even** across whole pass — uneven pressure = tapered edge

### 3D-Printed Jig Concept
Isaiah proposed: glass standing up on silicone, flat piece resting on top to hold perpendicular while sliding across abrasive. Pulley/racetrack system for unidirectional, repeatable motion.

### Sandpaper vs Lapping Film Crossover
**Crossover is at ~5000 grit:**
- **Below 5000 grit:** sandpaper similar quality, cheaper, wins on cost
- **Above 5000 grit:** sandpaper grit variance ($\pm$5–15µm on a single sheet) creates random deeper scratches; lapping film graded to ±10% particle size = more uniform
- Paper backing flexes at 7000+ grit — inconsistent contact
- For Gem's 3000 grit target: **sandpaper is fine, no need for lapping films**

### Sourcing
- JLC CNC website considered (China sourcing for parts)
- "Model C" Amazon-friendly version discussed for price-conscious build

### Key Insight
Bond-line tolerance pushes the design harder than the polish does. The grinder doesn't need exotic abrasives or extreme RPM — it needs a rigid, perpendicular-holding jig and even pressure across the whole pass.

### Relation to Previous Research
- Builds on RESEARCH-002 Thread 6 ("Seam options ranked: 1) UV optical adhesive (invisible)")
- Adds the **fabrication side** of how to actually achieve the edge precision the invisible seam requires
- The bond-line specs Isaiah pasted in came from another bot — worth confirming source if used in production decisions
