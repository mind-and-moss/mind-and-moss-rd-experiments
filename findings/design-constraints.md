# Mind and Moss — Top-Level Design Constraints

Hard constraints that apply across all Mind and Moss products. Any product design that violates one of these can't be built with the current tooling and process. Update this file whenever a new tooling or material decision creates a global limit.

---

## Glass panel dimensions

### Max single edge: **18 inches**

**Source:** Bike-powered glass grinder design (2026-05-08 Q1–Q4 lock-in). 22" usable platen length minus ~4" approach/exit margin = 18" max edge that can be ground in a single pass with the optical-adhesive-grade finish required for The Machine's gem-component seams.

**What this means in practice:**
- Every panel design must have its **longest** edge ≤ 18".
- A square panel ≤ 18×18" is fine.
- A rectangular panel can have one short edge (any length up to 18") and one long edge (≤ 18").
- A panel exceeding 18" on any single edge cannot be ground to optical-clarity standard with current tooling.

**Why this is a hard limit:**
Two-pass grinding produces visible artifacts at the join between passes — sub-micron variation that breaks UV optical adhesive bonds and produces visible defects under thermal cycling. The single-pass requirement is non-negotiable for any product where panels are joined by optical adhesive (which currently means The Machine's gem-component, but extends to any future product using the same seaming approach).

**How to escape this constraint:**
- Build a longer-frame grinder (more belt length, larger pulleys, longer platen, larger frame footprint, more material cost). Not planned in the current roadmap.
- Switch to a different seam type (e.g., structural silicone) that tolerates two-pass edge inconsistency. See `findings/decisions-pending.md` #1.

### Max thickness: **TBD**

Currently 6mm aquarium glass is the inventory baseline (per `setup.md`). Thicker glass requires more aggressive grinding and may exceed the bike grinder's effective stock-removal capacity. Confirm with empirical testing before committing to designs requiring >6mm panels.

---

## Print envelope (Bambu A1 Mini)

### Max printable part: **170 × 170 × 170 mm**

**Source:** Bambu A1 Mini build volume is 180×180×180 mm. The 170 mm working envelope leaves margin for first-layer bed adhesion and avoids edge artifacts.

**What this means:**
- Any 3D-printed part in any product must split if it exceeds 170 mm in any dimension.
- Frame members, pulleys, gear bodies, brackets — all subject to this.
- Designs that need to exceed 170 mm must be split into multiple parts that mate via mechanical joints (heat-set inserts + stainless bolts).

**FreeCAD enforcement:** the manufacturability validator macro (per `tooling/bike-powered-grinder/research/freecad-1.1-readiness.md` Part C #3) walks every Body in the assembly, gets its bounding box, and warns on anything exceeding 170 mm. This catches the violation before slicing.

---

## Hardware standardization

### Stainless steel bolts as the baseline fastener

- M5 304 stainless as the general-purpose size
- Larger stainless (e.g., ½") only at high-stress anchor points
- No oversizing for its own sake (internal tooling stays lean; customer-facing products may vary)
- Heat-set inserts (CNC Kitchen brass M3/M5) in PETG for blind threaded holes
- Through-bolts with nylock nuts for thru-joints
- Every joint replaceable; no glued-in fasteners

**Source:** Bike-grinder Phase 0 review (2026-05-07).

---

## Material inventory baseline

Per `setup.md`:
- 304 stainless rod stock (cut to length on Isaiah's table saw)
- Mold-making silicones (multiple types — confirm appropriate one for plastic-to-metal bonding)
- M3 + M5 stainless hardware in stock
- Bambu A1 Mini PETG (primary) — fit calibration values to be locked via test-coupon (per FreeCAD readiness research, Part C #6)

Filament not in baseline (require new inventory and may not be added):
- PETG-CF, nylon, PA-CF (rejected for bike grinder; may be revisited per-product if a structural need genuinely requires it)

---

## Brand non-negotiables

These aren't engineering constraints but they affect every design:

- **Biotope fidelity** is the through-line. Form factors are vessels for biotopes. Any product that doesn't serve a measurably better biotope outcome doesn't pass the smell test.
- **"How the fuck did they make that"** is the wow standard. Visible mechanical beauty matters; every product must have a wow element.
- **The Gem is a component, not a peer product.** It's a glass element within The Machine, not standalone.

See `CLAUDE.md` for full context.
