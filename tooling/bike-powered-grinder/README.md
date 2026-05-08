# Bike-Powered Glass Grinder — Tooling

**Date created:** 2026-05-07 (genesis voice session, "FreeCAD 1.1 and AI-assisted 3D printing")
**Last updated:** 2026-05-07 (Phase 0 review voice session, "Bike-powered grinder Phase 0 review")
**Branch:** `tooling/bike-powered-grinder`

This folder is **tooling, not product**. It's the machine that makes the machine. But it's still held to Mind and Moss's "how the fuck did they make that" standard — visible mechanical beauty, deliberate engineering, not a cobbled-together hack.

---

## TL;DR (current locked spec)

A **seated, bike-powered, single-platen glass grinder** with a **24"-long horizontal platen**, 2x72 silicon carbide belts (120→1000), **8:1 gear reduction** from 75 RPM cadence to **750 RPM at the belt**, screw-driven tensioner (no springs), 5" crowned drive pulley, 2" crowned idler. 3D-printed PETG structure with embedded stainless rod reinforcement and stainless bolts at every joint for replaceability. Used as the **finishing** stage after Isaiah's existing wet glass grinder pre-finishes the panel edge.

---

## Why this exists

Isaiah cannot precision-finish glass panel edges to optical-clarity standard with current inventory. The gem-component within The Machine requires panel seams that bond cleanly with UV optical adhesive (NOA 65 or NOA 148, per `findings/decisions-pending.md` #1). Any edge irregularity = bond failure, optical distortion, or visible seam defect. The grinder is the gate that opens The Machine's manufacturability — and every other Mind and Moss product that uses precision-cut glass.

## Brand reframe context

Per `CLAUDE.md` and `findings/SESSION-HANDOFF.md`: "The Gem" is no longer a standalone product. It's a glass component within The Machine. The brand's through-line is **biotope fidelity** — environments built so accurately that species express behaviors hobbyist setups don't produce. This grinder serves that mission by enabling the precision required for the form factors that house biotopes.

---

## Locked design decisions

Decisions are split between the **genesis voice session** (2026-05-06) and the **Phase 0 review voice session** (2026-05-07). The Phase 0 review tightened ranges into single values and resolved several open questions. Where this README disagrees with the original handoff, **this README wins** — the Phase 0 review supersedes.

Full transcripts: `sessions/2026-05-06-mobile-genesis-and-freecad.md`, `sessions/2026-05-07-mobile-phase-0-review.md`.

### 1. Belt: 2x72 silicon carbide, 120 → 1000 grit

Sackorange 6-pack 2x72 silicon carbide on Amazon (~$20/pack ≈ $3.30/belt). 120/240/400/600/800/1000 grit progression. **2x82 was investigated and rejected** — silicon carbide at glass-grade fine grits is not standardly stocked at 2x82, custom builds run 2–3× the cost. 2x72 is the sweet spot for supply chain.

Higher grits (1500+, polishing compounds) deferred to a later session.

### 2. Platen: 24" usable length, glass-only, single-purpose

Two-pass finishing is unacceptable. Glass seam edges for optical adhesive bonding need single-pass consistency.

**Dual-zone idea (slack belt or multi-bearing zone for curves) was considered and rejected** — single-purpose tool, glass-only. Dual-zone would have forced compromises on tensioner design, belt tracking, and frame stiffness. Glass needs the platen flat and rigid. Anything else compromises that.

Realistic max glass edge on a 24" platen is ~20–21" (need approach + exit on the platen so the edge enters and leaves cleanly). **Open question:** longest single glass edge in The Machine's gem-component panels — if any panel exceeds ~20", the platen needs to grow.

### 3. Layout: horizontal — belt runs in a horizontal plane

The grinder lies sideways. Glass panels lay flat on a fixture, edge presented up into the belt at the **top edge of the belt where it crests over the platen**. This is the contact line — single-line contact across the belt width, not a full platen face.

Implications:
- **Crowned pulleys non-negotiable.** Horizontal layout means gravity tries to pull the belt off the bottom of the pulleys. Both drive and idler pulleys must be crowned ~0.020–0.040" higher in the middle than the edges so the belt naturally centers.
- **Tensioner direction flips.** Idler is sprung outward against pure spring/screw force — no gravity assist. Spring rate / screw thrust needs to be higher than vertical layouts.
- **Coolant routing is gravity-friendly.** Drip line above platen, slurry catch tray below. (See decision #10.)
- **Operator stance: seated.** See decision #4.

### 4. Operator: seated rider position

Aero/TT-bike position with hands forward at the platen height. Standing pedaling fatigues fast (it's a sprint posture, not endurance). Seated keeps cadence sustainable and matches Isaiah's "conversational pace" target.

The work surface needs to be at the right height for a seated rider's reach. **Open question:** seat-to-platen geometry, frame footprint, frame height.

### 5. Workpiece fixture: rail-guided sled with straight-edge pusher

Glass panel sits flat in the sled, a straight-edge pusher across the full panel width keeps the edge perfectly parallel to the belt as the whole sled moves forward. The platen underneath supports the belt; the glass edge presses up into the belt; the sled controls approach speed and angle.

This solves two problems at once:
- Operator doesn't have to guess where the middle is and push from there
- Belt inconsistencies (slight bumps) don't translate to high/low spots on the edge — the rigid sled keeps pressure even across the full edge length

### 6. Drivetrain power flow

```
pedals
  ↓
crank
  ↓
freewheel / one-way clutch        ← bike-style; lets belt coast when pedaling stops
  ↓
gear reduction stage 1 (bicycle cassette)
  ↓
bike chain (same chain — one chain, two jobs: shifts pedal speed AND drives grinder)
  ↓
final sprocket bolted to drive pulley shaft
  ↓
5" crowned drive pulley (target 750 RPM)   ← RPM sensor here
  ↓
2x72 silicon carbide belt
  ↓
2" crowned idler pulley (returns belt; tensioner pivot point)
  ↓
24" flat platen between idler and drive
  ↓
glass panel edge presented to top of belt at platen crest
  (held in rail-guided sled with straight-edge pusher)
```

**Re-verify with Isaiah** before FreeCAD geometry locks: is the freewheel placed at the crank as shown, or somewhere else in the chain?

### 7. Cadence and gear reduction

- **Target cadence:** 75 RPM (mid-range conversational, talk-while-pedaling threshold)
- **Target belt RPM:** 750 RPM
- **Gear reduction:** **8:1 LOCKED** (from crank to drive pulley)

8:1 was chosen over 10:1 for material durability. 10:1 puts ~25% more torque on every gear tooth, chain link, bearing, and print layer. For 2-min-on / 1-min-off intermittent duty, 8:1 stays comfortably within a PETG-printed gear's fatigue envelope. 10:1 starts approaching it.

**Open question:** how to split the 8:1 across two stages. Cassette ratio (e.g., 3:1) × chain-to-pulley ratio (e.g., 2.7:1)? Different split? Affects sprocket sizes and printability of intermediate gears.

### 8. Pulleys: 5" drive, 2" idler, crowned, 3D-printed PETG with stainless reinforcement

- **Drive pulley:** 5" diameter. With 75 RPM cadence × 8:1 reduction = 750 RPM at the belt — middle of the 600–800 RPM glass-finishing window.
- **Idler:** 2" diameter (consensus standard for 2x72 grinders; doesn't affect belt speed).
- **Both crowned** ~0.020–0.040" (final crown TBD against confirmed Sackorange belt width and material).
- **Construction:** 3D-printed PETG bodies with embedded stainless rod spokes radiating from a center hub. CNC is **last resort** if the printed-and-reinforced design fails physical load testing.

### 9. Tensioner: screw-driven, no springs, feel-based tuning

**Mechanism:** A pure screw-driven tensioner. The idler wheel bolts to a rigid pivot arm; the arm pivots on a pin at one end; the adjustment screw on the other end pushes the arm outward as you turn it. No spring fatigue risk, fewer failure modes, dirt cheap (just a stainless bolt + threaded hole in the arm).

**Why no springs:** Springs auto-maintain tension as belts wear and stretch — useful for high-duty-cycle electric grinders, irrelevant for a hand-cranked tool that gets re-tensioned manually before each session anyway. Springs also add cost, sourcing complexity, and a fatigue path Isaiah doesn't want to engineer around.

**Tuning method:** **By feel, not by gauge.** Reference: push the belt sideways with your thumb at mid-span; it should deflect about ¼" under moderate hand pressure, then snap back. **Document this in the assembly guide** so future-Isaiah (or anyone else building one) has the calibration target.

### 10. Coolant: water drip line above platen, slurry catch tray below

Silicon carbide runs cooler wet, and water flushes glass dust (which is nasty to breathe). Horizontal layout makes this gravity-routable: drip line above the platen → slurry runs across the platen → falls into a catch tray below.

**Open questions:**
- Tray material: stainless steel pan, or printed drain manifold draining to bucket? Stainless wins on corrosion resistance but adds sourcing.
- Recirculating pump or one-way drain to bucket? One-way is simpler; recirculating wastes less water but adds plumbing.
- Slurry handling: how does Isaiah dispose of the spent grit + glass dust slurry? (Glass dust = silicosis risk if it dries and aerosolizes.)

### 11. Hardware: stainless steel bolts, right-sized per joint, replaceable everywhere

**Spec:**
- M5 stainless steel as the baseline for general assembly (matches Isaiah's existing inventory)
- Larger stainless (e.g., ½") at high-stress anchor points only — frame corners, drive pulley axle mount, bearing block pivots — wherever load is genuinely concentrated
- **No oversizing for its own sake.** Right-size per joint. Save overkill engineering for products sold to customers. Internal tooling stays lean.
- Sourced from Amazon (consistent inventory) or Home Depot (for the larger or oddly-sized fasteners)
- **304 stainless** as the inventory baseline (per `setup.md`)

**Joining:** Heat-set inserts in PETG (CNC Kitchen brass M3/M5) for blind threaded holes; through-bolts with nylock nuts for thru-joints. Both compatible with the "every part replaceable, no glued-in fasteners" principle.

See `research/heat-set-inserts.md` for the full insert spec, torque targets, and 3 open questions.

### 12. Operator workflow context (clarifies what this grinder does)

Isaiah's full glass workflow:
1. Cut glass to size with score tool + pliers
2. **Pre-finish edges with the existing handheld wet grinder** (3/4" water-wheel grinder Isaiah already owns) — gets the edge close to clean
3. **This bike-powered grinder is the FINISHING stage** — takes a pre-cleaned edge from ~220-grit roughness down to 600–1000 for optical-adhesive bonding

**Implication:** This is light finishing work, not stock removal. Slow belt speed is correct (700–800 RPM target). Coarse grits (120–240) are mostly there to "walk down" the surface progression cleanly between grits, not to remove material.

This clarification means the grinder doesn't need to be aggressive. Optimize for stability, repeatability, and surface quality — not maximum cut rate.

---

## Status

- [x] Genesis handoff received from voice session (2026-05-06)
- [x] Phase 0 review locked 14 additional decisions (2026-05-07)
- [x] Folder scaffold created
- [x] Heat-set inserts research (`research/heat-set-inserts.md`)
- [x] **Architecture diagram verified against Isaiah's voice-session intent** (Phase 0 review)
- [ ] FreeCAD 1.1 readiness research — what context I need to model parametrically
- [ ] FreeCAD 1.1 parametric model of drivetrain
- [ ] FreeCAD 1.1 parametric model of frame + platen mount + sled
- [ ] Stainless reinforcement plan
- [ ] Bill of materials (cycling parts: crank, freewheel, cassette, chain; bearings; pulleys; sensors; coolant tray)
- [ ] First print + test — bearing block load test under pedal torque
- [ ] Confirm longest gem-component panel edge ≤ 20" (drives whether 24" platen is enough)

See `open-questions.md` for the punch list of what Isaiah needs to answer before FreeCAD 1.1 work starts.

---

## Cross-references

- Brand context: `CLAUDE.md` (root)
- Current state: `findings/SESSION-HANDOFF.md`
- Decisions pending: `findings/decisions-pending.md`
- Glass technique research: `findings/topics/fabrication/glass-edge-grinder.md`
- Material inventory: `setup.md`
- Heat-set inserts: `research/heat-set-inserts.md`
- Open questions for FreeCAD: `open-questions.md`
- Voice session transcripts: `sessions/`
