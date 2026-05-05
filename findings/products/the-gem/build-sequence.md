# The Gem — Build Sequence (DRAFT)

> **Draft.** This sequence synthesizes existing research in `products/the-gem/` and `topics/` into an ordered build plan. Sequencing calls were made by Claude based on dependencies surfaced in the research — Isaiah should review and revise. No physical prototype has been built yet, so this is a paper plan, not a confirmed sequence.

## Goal
The Gem is a single sculptural object combining four distinct fabrication streams into one finished piece: a mycelium/hempcrete composite **base** that doubles as living substrate, a **glass hardscape frame** built from precision-cut panels joined with invisible silicone seams, **cast hardscape pieces** (3D-print → polymer-clay → silicone-mold → terrarium-safe cast) that form the internal landscape, and a **fused-glass sphere or hemisphere** centerpiece that scatters light. The completed object houses a closed aquarium below and an open terrarium above, with a fully bioactive cleanup crew so the structure can be permanently bonded — no disassembly path needed (per RESEARCH-001 Thread 3 bioactive insight).

## Critical path
1. **Phase 0** — Decisions & material lock-in (gates everything)
2. **Phase 1** — Build the custom glass edge grinder (bottleneck — invisible seams depend on this)
3. **Phase 2** — Hardscape master + mold (parallel to Phase 1 once tooling is queued)
4. **Phase 3** — Fused-glass centerpiece kiln work (parallel to Phases 1–2)
5. **Phase 4** — Mycelium base mold + grow-out
6. **Phase 5** — Glass panel cut, grind, and invisible-seam assembly
7. **Phase 6** — Cast hardscape pieces in terrarium-safe material
8. **Phase 7** — Dry assembly: base + glass frame + hardscape + centerpiece
9. **Phase 8** — Bioactive ecosystem install (last — everything else must be permanent)

---

## Phase 0: Decisions & material lock-in
**Goal:** Resolve the cross-cutting decisions before buying anything that locks the build in.
**Inputs needed before starting:** All current research files; willingness to commit.
**Steps:**
1. Pick a glass COE system (90 vs 96) and stay there — mixing causes guaranteed cracking on cool-down.
2. Pick silicone family for the hardscape master mold: tin-cure (works with Sculpey, sulfur-tolerant) vs platinum-cure (needs sulfur-free clay like Monster Clay).
3. Pick base material: mycelium/hempcrete composite (the differentiator) vs concrete (standard, faster, known).
4. Pick seam adhesive: pure silicone bond, optical UV adhesive (Norland-grade for clarity), or hybrid.
5. Pick final cast material for hardscape pieces: epoxy resin, polyurethane, or pigmented concrete (plaster is out — fails in humidity).
**Outputs:** Material list locked, no contradictions downstream.
**Open questions:** Mycelium composite supplier — none verified in research yet.

## Phase 1: Custom glass edge grinder
**Goal:** Build the wet belt grinder that lets edges hit the bond-line specs in `seam-construction.md` (silicone bond line 0.05–0.15 mm, squareness within 0.25°, 3000-grit final).
**Inputs needed before starting:** Phase 0 decisions; flat reference platen (ground steel/keystock, ~0.001" over 24"); 4"×106" belt format; diamond/SiC belts up to 3000 grit; perpendicular-holding sled jig (3D-printed concept exists).
**Steps:**
1. Build flat-platen-backed belt sander frame (vertical orientation, wet).
2. Build perpendicular sled — this is the make-or-break geometry.
3. Set drive: 800–1500 RPM at the abrasive; crank-and-gearbox is acceptable per research.
4. Calibrate against scrap glass; verify squareness with a machinist square before any real panels go through.
**Outputs:** A grinder that produces invisible-seam-ready edges repeatably.
**Estimated time:** Decision pending — research gives architecture, not a build schedule.
**Open questions / decisions needed:** Pedal-power vs motor input; final sourcing (JLC CNC vs Amazon "Model C" build).

## Phase 2: Hardscape master + silicone mold
**Goal:** Produce a reusable silicone mold of the artistic hardscape form that goes inside The Gem.
**Inputs needed before starting:** Phase 0 silicone decision; 3D printer; polymer clay (or Monster Clay if going platinum-cure); Zinsser Bullseye shellac.
**Steps:**
1. 3D print the armature. Remove supports, light sand 120→220 grit (just kill the worst layer lines).
2. Shellac the print — 2 coats. This blocks plasticizer attack on PLA/ABS and gives clay a grip surface.
3. Sculpt fine detail in polymer clay over the sealed armature. No time pressure — polymer clay doesn't air-cure.
4. Bake per clay spec (110–130 °C, 15–30 min) if using polymer clay; skip if using Monster Clay.
5. Shellac over the cured clay — 2–3 light coats (critical sulfur barrier before silicone).
6. Pour silicone mold (tin-cure if any sulfur risk, platinum if confirmed sulfur-free + no latex/CA-glue contamination).
**Outputs:** A reusable silicone mold. The 3D print never enters the tank.
**Open questions:** Whether to mother-mold with plaster for rigidity (research mentions "silicone + plaster mold").

## Phase 3: Fused-glass centerpiece (parallel kiln workflow)
**Goal:** Produce the sphere/hemisphere "impossible gem."
**Inputs needed before starting:** Glass kiln (top-heated, NOT ceramic side-heated) — Evenheat Studio Pro or Paragon SC-2 for 6–8" pieces; ceramic slump mold (Bullseye/Slumpy's/Creative Paradise, $40–150); sheet glass in the chosen COE system.
**Steps:**
1. Cut blanks from sheet glass. Use 0.3 mm Sharpie offset 5 mm from cut line; wipe before each break.
2. Stack/tack-fuse on flat shelf in kiln per glass-system schedule.
3. Slump over hemisphere mold in second firing.
4. Cold-work edges if needed — same grinder family used for panels (could share Phase 1 tooling at coarse grits).
**Outputs:** One or more centerpieces ready to integrate.
**Open questions:** Whether the centerpiece is structural or floats inside the frame — affects mounting in Phase 7.

## Phase 4: Mycelium base mold + grow-out
**Goal:** Cast the structural-and-substrate base that holds the bottom quarter of the glass.
**Inputs needed before starting:** Phase 0 base decision; mold form (could use the same silicone-mold workflow as Phase 2 at larger scale); mycelium composite kit or hempcrete + spawn.
**Steps:**
1. Build a base-shape mold (rigid form, food-safe interior).
2. Pack inoculated substrate, incubate per product instructions until fully colonized.
3. Heat-kill or air-dry to stop growth and stabilize.
4. Test fit against glass-frame footprint before going further.
**Outputs:** Finished base ready to receive glass.
**Estimated time:** Mycelium grow-out is on the order of days to weeks — start this in parallel with Phase 1/2 work.
**Open questions / decisions needed:** No verified composite supplier in research; sealing strategy for water-contact surfaces is not resolved.

## Phase 5: Glass panel cut, grind, and invisible-seam assembly
**Goal:** Assemble the glass frame with bond lines that disappear optically.
**Inputs needed before starting:** Phase 1 grinder operational; sheet glass (same COE as centerpiece if any fused panels are integrated); aquarium-safe 100% silicone (GE Silicone I, Aqueon, or ASI — NOT GE Silicone II); 90° corner clamps (Bessey WS-1 in parallel is the budget call); isopropyl alcohol.
**Steps:**
1. Lay out and score panels on a true flat surface, alcohol-clean each, mark only corners (per glass-cutting research).
2. Grind every edge through the grinder to 3000 grit, holding squareness to 0.25°. This is the slow part.
3. Dry-fit the frame in corner clamps. Measure squareness corner-to-corner (within 0.5°, ~1 mm across 6").
4. Clean seams with alcohol, tape adjacent faces to control drips.
5. Apply silicone bond — target 0.05–0.15 mm bond-line. Below 0.025 mm = voids; above 0.25 mm = optically visible.
6. Cure film 3–5 days, then full cure 7–10 days until vinegar smell is gone.
**Outputs:** A finished invisible-seam glass frame.
**Open questions:** Whether to layer a Norland-grade UV optical adhesive over silicone for the visible-from-outside faces (hybrid path from `seam-construction.md`).

## Phase 6: Cast hardscape pieces
**Goal:** Pull final hardscape pieces from the Phase 2 mold in terrarium-safe material.
**Inputs needed before starting:** Phase 2 mold; chosen cast material from Phase 0.
**Steps:**
1. Mix and pour. For hollow lightweight pieces, rotate the mold during cure so cast material self-levels along the inner wall.
2. Demold, cure fully, leach/wash if using concrete (high pH needs neutralizing before going in a tank).
3. Test in plain water for any leached residue before installing.
**Outputs:** Hardscape pieces ready for placement.

## Phase 7: Dry assembly
**Goal:** Combine base + glass frame + hardscape + centerpiece into the final structure.
**Inputs needed before starting:** All prior phase outputs.
**Steps:**
1. Seat the glass frame onto the mycelium base — bond with aquarium-safe silicone, cure fully.
2. Place hardscape pieces inside; bond permanently per the bioactive-permanence insight.
3. Mount centerpiece (method depends on Phase 3 open question).
4. Final leak-test the aquarium half with plain water. Hold 48 hours minimum.
**Outputs:** Sealed dry sculpture ready for the ecosystem install.

## Phase 8: Bioactive install
**Goal:** Bring the piece alive.
**Inputs needed before starting:** Springtail and isopod cultures (already part of Mind and Moss production line per `bioactive-systems.md`); substrate layers; plants; livestock for aquarium half.
**Steps:**
1. Substrate + drainage layer in terrarium half.
2. Seed springtails first, then isopods after a week.
3. Plant in.
4. Cycle aquarium half, then stock.
**Outputs:** A finished, living Gem.

---

## Decision points (cross-cutting)
- **COE 90 vs COE 96** for all fused glass. Pick once, never mix.
- **Tin-cure vs platinum-cure** silicone for the hardscape master mold (driven by clay choice and contamination risk).
- **Mycelium composite vs concrete** for the base.
- **Pure silicone vs UV optical adhesive vs hybrid** for invisible seams.
- **Final cast material** — epoxy, polyurethane, or pigmented concrete. Plaster is ruled out.
- **Centerpiece mounting** — structural vs suspended.

## Open whitespace / unknowns
- No verified mycelium composite supplier in the research.
- Bond-line specs in `seam-construction.md` originated from another bot — research itself flags these as needing source verification before production decisions.
- No build schedule (hours/days) for the custom edge grinder.
- Sealing strategy for the water-contact face of a mycelium base is unresolved.
- Centerpiece mounting method is undefined.
- Production-line vertical organization for breeding cultures (referenced in `glass-edge-grinder.md`) is an open business-side question, not a build blocker.

## Cost & material rough sketch
Only items the research actually quotes:
- Glass kiln (small, 6–8" pieces): $700–1200 new, ~half that used.
- Glass kiln (medium, 10–12"): $2000–3000.
- Slump mold: $40–150.
- UV resin (Solarez/Padico/CCD): $15–30/bottle.
- Diamond Pacific Tech Master 8" grinder (if bought instead of DIY): $800–1200 used.
- Total grinder station including DIY belt rig: ~$1000–1500 used + DIY parts.
- Bessey WS-1 corner clamp: $10.49 each — buy several in parallel.

Everything else (mycelium composite, casting resin volumes, sheet glass, aquarium silicone) — decision pending and not quoted in source research.
