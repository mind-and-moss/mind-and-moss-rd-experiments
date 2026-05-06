# Glass Edge Grinder

Bond-line specs, grit progression, and architecture choices for a custom belt-grinder/sander that polishes glass panel edges to invisible-seam tolerance. Plus clamp options for thin-panel assembly. The "build instructions" themselves are not yet written — most content here is the engineering targets and tradeoffs that constrain the design.

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

### Spec verification (2026-05-05)

The table above was originally flagged in the source research as "specs from another bot, worth confirming source if used in production decisions." A verification pass against primary sources (Norland NOA datasheets, DOWSIL structural-glazing guides, ASTM C1036 / C1184 / C1401, Edmund Optics) found multiple issues that should be resolved before committing the build. **The original table should not be used as a production spec doc as-is.**

| Original row | Verified status | Correction |
|---|---|---|
| Silicone bond line 0.05–0.15mm "sweet spot" | **Wrong if read as structural silicone** (Dow DOWSIL 983: 6 mm minimum, 13 mm max glueline; ASTM C1184 / C1401 confirm). Plausible only as a non-structural cosmetic silicone film. Original spec conflates two different things. | Split into two rows: (a) **UV optical adhesive (Norland NOA)** = 50–250 µm general bonding, 3–50 µm precision (per Incure / Norland). (b) **Cosmetic silicone film** ≈ 0.1–0.5 mm, *not load-bearing*. (c) If load-bearing, use ASTM-compliant 6 mm minimum. |
| Max bond line 0.25mm "= optically visible" | **Unsupported by any primary source found.** Fabricated heuristic. | Remove the optical-visibility claim; depends entirely on adhesive's refractive index match to glass. NOA 61/81 cure to ~1.56 RI vs soda-lime ~1.52 / borosilicate ~1.47 — *not* a true index match. |
| Edge flatness 0.05–0.10mm | **Plausible but unsourced.** No ASTM/Edmund/Bullseye standard at this number. Achievable with hand coldworking. Too loose for true optical contact bonding (which targets λ-fractions, ~0.6 µm at 633 nm). | Keep as practitioner target, drop the "spec" framing. Verify against an actual coldworking trial on 6 mm stock. |
| Squareness 0.25° (~0.05mm across 6mm) | **Internally inconsistent** — tighter than the 0.05–0.10 mm flatness target. Can't have tighter squareness than flatness. | Loosen to 0.5° (≈0.05 mm across 6 mm) so it matches flatness. |
| Edge polish 3000–8000 grit, no cerium oxide | **Contrarian and partially wrong.** Industry standard: 80 → 220 → 400 → 600 grit then **cerium oxide** for transparent edges. Skipping cerium leaves a frosted micro-surface that scatters light at the bond. | Pick a lane: (a) accept matte look, stop at 600–1200 grit (much faster); or (b) go 1200 grit then cerium-buff for true optical edge. Avoid the "3000–8000 no cerium" middle path — slow *and* not fully clear. |
| Panel-to-panel ±0.5mm | **Confirmed.** Within ASTM C1036 commercial-grade and achievable with coldwork. | Keep as-is. |
| Cut squareness 0.5° | **Reasonable** but not directly cited in primary docs. | Keep as-is. |

**Sources for the verification:**
- Norland NOA 61 / 81 / 88 product pages and TDS PDFs ([norlandproducts.com](https://norlandproducts.com/))
- [Incure — Bond Line Thickness Guide](https://incurelab.com/wp/how-thick-is-optical-adhesive-navigating-bond-line-thickness-for-optimal-performance/)
- [DOWSIL 983 Guide Specifications](https://www.buildsite.com/pdf/dowcorning/DOWSIL-983-Structural-Glazing-Sealant-Base-and-Curing-Agent-Guide-Specifications-2152197.pdf), [DOWSIL 795 TDS](https://www.dow.com/content/dam/dcc/documents/en-us/productdatasheet/63/63-12/63-1217-dowsil-795-structural-glazing.pdf)
- ASTM C1036 (flat glass), C1184 (structural silicone sealants), C1401 (structural glazing guide)
- [Edmund Optics — Optical Specifications](https://www.edmundoptics.com/knowledge-center/application-notes/optics/understanding-optical-specifications/)
- [Rocketrose — Polished Edge Glass Guide](https://rocketroseart.com/seamed-edge-vs-polished-edge-glass-complete-guide-2025/)

**Bottom line for the build:** The grinder's geometry targets (rigid platen, perpendicular jig, even pressure) are still correct — those don't depend on which specs were wrong. What changes: the polish endpoint (consider cerium-oxide buffing instead of pushing past 3000 grit) and whether the "invisible seam" target needs to be re-defined as either *UV-adhesive optical bonding* (Norland, thin film) or *cosmetic silicone film* (decorative, not structural). Pick one before the spec table goes into production.

---

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

---

Source: RESEARCH-005 Thread 20 — "Clamps for glass assembly" (chat #48 — first ~10 turns only; rest drifts to PC building)

## Corner / joint clamps for thin glass-acrylic assembly

For holding glass and acrylic panels in rectangular assemblies during silicone cure or weld setup:

| Clamp | Price | Notes |
|---|---|---|
| Kreg 90° Corner Clamp | $49.99 | Auto-adjusts, woodworking-grade |
| Bessey 90° Corner Clamp WS-1 | $10.49 | Budget basic 90° joins |
| Pittsburgh Corner Clamp w/ Quick Release | $11.99 | Quick-release for fast setups |
| Micro-Mark Mini 4 Corner Clamps | $14.96 | For tight spaces / small projects |
| Bessey WS-3+2K 90° Angle Clamp | $31.97 | Pro-grade, 1-1/8" throat |
| Milescraft SquareClampKit | $24.99 | Complete kit |

For The Gem's 6" panel work and similar thin-acrylic builds, the Bessey WS-1 ($10.49) is a strong starter — multiple in parallel beats one expensive Kreg for the price.

## Production-line vertical organization (briefly discussed in same chat)
- 30 × 60oz cube containers needed lights + air, going vertical for floor space
- Design wasn't resolved in the chat — open question for production-line shelving
