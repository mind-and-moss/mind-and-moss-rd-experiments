# Decisions Pending — Mind and Moss

Open calls awaiting Isaiah's judgment. Each one is consolidated here so a fresh outside reader (another AI bot, a collaborator, future-Isaiah) can engage with the substance without reading the whole repo.

Each decision includes: **the question**, **the options**, **the trade-offs**, **Claude's recommendation if any**, and **what committing requires**.

Updated: 2026-05-05.

---

## Material / spec decisions

### 1. The Machine's gem-component seam type
**Question:** What actually bonds the glass panels of The Machine's gem-component? This drives the grinder design, the bond-line specs, and the overall fabrication pipeline.

**Options:**
- **(a) UV optical adhesive** — Norland NOA series, thin film (50–250 µm), bonded under UV light.
- **(b) Cosmetic silicone film** — thin smear of clear silicone (~0.1–0.5 mm), decorative seam-hiding.
- **(c) Structural silicone glazing** — ASTM-compliant Dow DOWSIL 983/995 etc., 6 mm minimum bond line, load-bearing.

**Trade-offs:**
- (a) is the strongest visual match for "glass bonded by nothing." Requires UV lamp, specific NOA grade matched to glass refractive index, and structural support from elsewhere (clamping, frame geometry). Cost: $15–30/bottle.
- (b) familiar, repairable, aquarium-safe materials, but **not load-bearing** — frame structure must come from elsewhere. The seam *will* be slightly visible.
- (c) load-bearing standalone, but bond line is 6 mm minimum — visible from any angle, **wrong target if "invisible seam" is the goal.**

**Why this matters:** the spec table inherited from R004 Thread 15 conflated (a) and (b) — described silicone-bond-line dimensions (50–150 µm) that only apply to UV optical adhesive, not silicone. PR #3 added a verification table with the corrections.

**Claude's rec:** **(a) UV optical adhesive.** It's the only path that achieves the actual visual goal. Specifically NOA 65 (RI 1.524) for soda-lime glass or NOA 148 (RI 1.48) for borosilicate. Plan structural support via mechanical clamping of the panels into the mycelium base + glass frame geometry, not via the seam itself.

**What committing requires:**
- Pick (a), (b), or (c)
- If (a): pick glass type first (drives NOA 65 vs NOA 148)
- Lock the spec table accordingly

---

### 2. Glass type for the gem-component
**Question:** Soda-lime or borosilicate?

**Options:**
- **Soda-lime** — common art glass, COE ~85–96 depending on grade. RI ~1.52. Cheaper, easier to source.
- **Borosilicate** — RI ~1.47. More thermal-shock resistant. Used in lab glassware. More expensive.

**Trade-offs:**
- Soda-lime fusing-grade is the dominant hobbyist art glass (Bullseye COE 90, System 96). Best community support, color range, slump molds available.
- Borosilicate has higher clarity and lower RI, but no hobbyist fusing community to speak of. Specialty.

**Claude's rec:** **Soda-lime, fusing-grade.** Pair with NOA 65 if going UV-adhesive seams. Aligns with the rest of the glass-fabrication research.

**What committing requires:** Pick a COE system (next decision).

---

### 3. COE system: 90 vs 96
**Question:** Which fusing-glass system?

**Options:**
- **COE 90** — Bullseye Glass Co. The most popular fusing-glass system. Largest color range, deepest hobbyist resources, well-documented firing schedules.
- **COE 96** — System 96 / Spectrum / Uroboros / Wissmach. Compatible across this family. Alternative ecosystem.

**Trade-offs:** Both work. Pick one and **never mix** — guaranteed cracking on cool-down. Bullseye has more institutional-quality references; System 96 has more sheet-glass options for stained-glass crossover work.

**Claude's rec:** **COE 90 (Bullseye).** Most resources, biggest community, best technical documentation. Already the de facto reference in the repo.

**What committing requires:** Just pick one and commit publicly to your suppliers.

---

### 4. Hardscape master mold: tin-cure vs platinum-cure silicone
**Question:** Which silicone family for The Machine's hardscape master mold?

**Options:**
- **Tin-cure (Smooth-On Oomoo, etc.)** — tolerates sulfur clays (Sculpey) without inhibition. Cheaper. Shorter library life (silicone degrades over years).
- **Platinum-cure (Smooth-On Mold Star, etc.)** — longer library life, better detail, but **inhibits on contact with sulfur clay, latex, certain spray paints, polyester resin, uncured SLA, CA glue residue**. Requires shellac barrier layer.

**Trade-offs:** Tin-cure is the safe path with Sculpey (the polymer clay you've selected). Platinum is technically better but requires careful contamination control.

**Claude's rec:** **Tin-cure.** Matches your stated polymer-clay choice without contamination risk. Shellac is still in the workflow for clay-grip-surface reasons.

**What committing requires:** Buy a tin-cure silicone (Smooth-On OOMOO 30 is the standard hobbyist pick).

---

### 5. Final cast material for hardscape pieces
**Question:** What does the final hardscape get cast in?

**Options:**
- **Epoxy resin** (e.g., Smooth-On EpoxAcast) — excellent detail, durable, expensive.
- **Polyurethane resin** (Smooth-On Smooth-Cast) — fast cure, less expensive, slightly less durable in long-term water exposure.
- **Pigmented concrete** — cheap, heavy, matches The Machine aesthetic, requires multi-week alkalinity cure before going in tanks.
- **Plaster** — RULED OUT (fails in humidity per R001 Thread 3).
- **Pour foam + coating** — lightweight option, less rigid.

**Trade-offs:** Epoxy and polyurethane are the standard for aquarium/terrarium hardscape (used by Universal Rocks, Aquadecor commercially). Concrete is dramatic but adds the cure-and-leach step. Foam is lightweight but feels less premium.

**Claude's rec:** **Epoxy** for The Machine's gem-component hardscape pieces — premium feel, long-term water-stable, matches the boutique brand. Save concrete for The Machine's load-bearing parts (different product, different aesthetic).

**What committing requires:** Pick a brand + grade. MAX ACR A/B is in the references as aquarium-safe.

---

### 6. The Machine's base: mycelium composite vs concrete
**Question:** What's the structural base under the glass top?

**Options:**
- **Mycelium-bound hempcrete or cork composite** (Ecovative MycoComposite) — biomaterial, structural + substrate hybrid, organic aesthetic, novel in the terrarium world. Differentiator.
- **Concrete or GFRC (glass-fiber reinforced concrete)** — proven, available, heavier feel, matches industrial aesthetic.
- **Hybrid** — concrete bottom shell (load-bearing pressure vessel), mycelium top layer (substrate-facing).

**Trade-offs:**
- Mycelium = strongest brand differentiator, but no verified active US supplier reliably sized for this. (MycoWorks insolvent Oct 2025; Ecovative is now the only option.) Long grow-out time (weeks). Sealing strategy for water-contact face is unresolved.
- Concrete = predictable, available, but doesn't hit the "biomaterial under crystalline top" key differentiator from R002 Thread 6.
- Hybrid = best of both, more complex build.

**Claude's rec:** **Hybrid for v1**, mycelium for v2. Get a working Machine out the door with a concrete base + mycelium decorative top layer; iterate to full mycelium once you have time + supplier reliability.

**What committing requires:** Decide which version is v1 and order materials.

---

## Scope / product-shape decisions

### 7. The Machine: open-air, sealed, or both
**Question:** Is The Machine an open-air room-scale racetrack, or a sealed-system variant, or both as separate products?

**Context:** Original concept (R001 T1) is open-air zebrafish racetrack. R005 T17 added closed-cycle gas-exchange research that implies a sealed sub-system. The repo has both threads of research, never explicitly chose one.

**Options:**
- **(a) Open-air only** — commit to the original concept. Move sealed research to a different concept (biome cartridge or new product).
- **(b) Sealed-system only** — discard the room-scale racetrack, focus on a sealed version.
- **(c) Both as variants** — explicitly two Machine variants. Doubles work but allows market test.

**Trade-offs:** Open-air is more dramatic visually (room-scale). Sealed is more controlled (research/lab-grade aesthetic). Doing both is more product surface area than Mind and Moss can probably support at v1.

**Claude's rec:** **(a) open-air only** for v1. The room-scale racetrack is the visual hook. Sealed-cycle research lands in `concepts/biome-cartridge.md` or a new `concepts/sealed-machine.md` for later exploration.

**What committing requires:** Update `products/the-machine/concept.md` to commit explicitly. Move sealed-cycle content out.

---

### 8. Aquarium method baseline: Walstad, Father Fish, or hybrid
**Question:** What's the baseline biology approach for the aquarium portions of Mind and Moss products?

**Context:** PR #5 documented both Walstad (academic, soil-substrate, no-filter, low-stocking) and Father Fish (Lou Foxwell — soil + sand cap, high light, "set-and-forget"). They overlap heavily.

**Options:**
- **(a) Pure Walstad** — committed academic baseline. Citable, well-documented, conservative.
- **(b) Father Fish-style** — more dramatic visually (high light), but his leaf-litter recommendation is contested and has crashed tanks.
- **(c) Hybrid Walstad-derived** — soil + cap, no filter, but tune lighting and species to your specific products.

**Trade-offs:** Walstad is the safer reference; Father Fish is the more "mainstream YouTube" reference but has known failure modes. Hybrid lets you cite Walstad for the engineering and your own observations for the tuning.

**Claude's rec:** **(c) hybrid, Walstad-derived.** Cite Walstad as the methodology basis. Tune empirically. Skip Father Fish's leaf-litter prescription specifically.

**What committing requires:** Decide and document the choice in `products/the-machine/concept.md` for The Machine's aquarium portion.

---

### 9. Anchor plant: single SKU or split
**Question:** Does Mind and Moss ship one anchor plant for all kits, or split open-vented vs sealed-environment SKUs?

**Context:** Heartleaf Philodendron is the proposed universal anchor (R005 T19), but the same paragraph notes it can rot in sealed environments without airflow.

**Options:**
- **(a) Single Heartleaf SKU** — only sell open-vented kits, or accept some rot risk.
- **(b) Split into two SKUs** — Heartleaf for open/vented, something humidity-tolerant for sealed.

**Claude's rec:** **(b) split.** The R005 thread itself proposed this. Implementation overhead is low and customer-fit is much better.

**What committing requires:** Pick the sealed-environment plant. Candidates: bromeliads, button fern, certain ferns/mosses. Update `business/product-categories.md` if you have one yet.

---

### 10. The Machine's gem-component: structural or suspended
**Question:** Is the fused-glass sphere/hemisphere centerpiece structural (load-bearing in the frame) or suspended (visually floating, no structural role)?

**Trade-offs:**
- Structural = stable, designed-in, simpler mounting.
- Suspended = dramatic, the "impossible gem" feel — but requires mounting hardware (steel cable, glass-to-frame bonding) that's hard to make invisible.

**Claude's rec:** **Suspended, with hidden mounting via the frame top.** The whole point of "impossible gem" is that it looks unsupported. Hide the mounting in the frame's top edge or use UV-bonded glass standoffs that disappear.

**What committing requires:** Design a mounting method. Open whitespace flagged in the build sequence.

---

## Process / workflow decisions

### 11. PR merge order
**Question:** Five PRs are open. What order should they merge?

**The PRs:**
- **PR #1** — Reorg + references folder (foundation)
- **PR #2** — setup.md (independent, repo root)
- **PR #3** — Auto-improvements: bond-line correction + TODO chase + build sequence + editorial review (depends on PR #1)
- **PR #4** — Soil chemistry + microorganisms + decomposers (independent of #1)
- **PR #5** — Walstad method + Father Fish method (independent of #1)

**Claude's rec:** Merge in this order:
1. **PR #1** first (foundation)
2. **PR #3** next (depends on #1, brings in the bond-line correction)
3. **PR #2** any time (independent)
4. **PR #4** any time (independent)
5. **PR #5** any time (independent)

OR if you want to ship faster: merge all five, accept that #3's references are lightly out of sync until #1's structure is in place.

**What committing requires:** Click "Merge pull request" in the order above.

---

### 12. Apply the editorial review's recommendations?
**Question:** The editorial review (PR #3, `findings/EDITORIAL-REVIEW-2026-05-05.md`) flagged five small clarification edits across existing files. Apply them?

**The edits:**
- Clarify shellac purpose in `hardscape-workflow.md` and `3d-print-prep.md` (sulfur barrier vs plasticizer barrier)
- Clarify "1mm acrylic ≠ wall material" in `the-machine/concept.md` or `structure.md`
- Clarify the "disposable vs permanent armature" language in `3d-print-prep.md`
- Promote the 2-anchor-plant SKU decision (above #9) into `business/product-categories.md`
- Add the seam-type decision (above #1) clarification into `seam-construction.md`

**Trade-offs:** All small. All make the repo more readable. None are urgent.

**Claude's rec:** **Yes, apply all five.** They're the kind of small clarifications that compound — if you don't apply them, future-you re-reads will hit the same confusions repeatedly.

**What committing requires:** Just say go and Claude can apply them in a follow-up PR.

---

### 13. Start an instrumented prototype build?
**Question:** PR #4 and PR #5 each surfaced a "no published data exists" research opportunity:
- PR #4: long-term pH drift in sealed bioactive vivariums
- PR #5: NO₃ / dissolved O₂ / dissolved organic C tracking over months in Walstad/Father Fish-style tanks

Both are "Mind and Moss could publish original data" opportunities. Start an instrumented build now to capture the data?

**Trade-offs:**
- Pro: Original published data is a brand asset (citable in marketing). Aligns with the bioactive-systems story. Hardware is cheap (a $20 pH probe, basic monitoring equipment).
- Con: Adds a multi-month observational discipline before any data is publishable. Requires patience and a stable build site.

**Claude's rec:** **Start one but don't make it the critical path.** Build a small Walstad-method test tank, instrument it with cheap sensors, log monthly. Lets you build the brand asset in the background while doing the actual product work. **Don't wait on this to ship.**

**What committing requires:** Decide if you have the bandwidth. Buy a pH probe. Set a monthly logging cadence.

---

## How to use this doc

If sharing with another AI bot for a second opinion, paste relevant sections (not the whole thing) and ask for engagement on specific questions. The other bot doesn't need every decision — pick the 2–3 you most want a fresh take on.
