# Bike-Powered Glass Grinder — Tooling

**Date created:** 2026-05-07 (genesis voice session)
**Last updated:** 2026-05-08 (Q1–Q4 lock-in session, FreeCAD readiness phase)
**Branch:** `tooling/bike-powered-grinder`

This folder is **tooling, not product**. It's the machine that makes the machine. But it's still held to Mind and Moss's "how the fuck did they make that" standard — visible mechanical beauty, deliberate engineering, not a cobbled-together hack.

---

## TL;DR (current locked spec, v3)

A **seated, bike-powered, single-platen glass grinder** with a **22"-long horizontal platen** (sized to a hard 18" max-glass-edge envelope), 2x72 silicon carbide belts (120→1000), **two-chain-stage drivetrain** at 10:1 speed-up from 75 RPM cadence to **750 RPM at the belt** (1180 SFM, upper-glass-spec). 6" crowned drive pulley, 3" crowned idler. Screw-driven tensioner (no springs). **Modular 3-section portable frame** built from hand-cut metal tube + 3D-printed PETG joint nodes with embedded heat-set inserts. Quick-release joints between modules so the whole machine breaks down to fit through a 30" interior door.

Used as the **finishing** stage after Isaiah's existing handheld wet glass grinder pre-finishes the panel edge.

---

## Why this exists

Isaiah cannot precision-finish glass panel edges to optical-clarity standard with current inventory. The gem-component within The Machine requires panel seams that bond cleanly with UV optical adhesive (NOA 65 or NOA 148, per `findings/decisions-pending.md` #1). Any edge irregularity = bond failure, optical distortion, or visible seam defect. The grinder is the gate that opens The Machine's manufacturability — and every other Mind and Moss product that uses precision-cut glass.

## Brand reframe context

Per `CLAUDE.md` and `findings/SESSION-HANDOFF.md`: "The Gem" is no longer a standalone product. It's a glass component within The Machine. The brand's through-line is **biotope fidelity** — environments built so accurately that species express behaviors hobbyist setups don't produce.

---

## Locked design decisions

Decisions are split across three voice/text sessions:
- **Genesis** (2026-05-06) — `sessions/2026-05-06-mobile-genesis-and-freecad.md`
- **Phase 0 review** (2026-05-07) — `sessions/2026-05-07-mobile-phase-0-review.md`
- **Q1–Q4 lock-in** (2026-05-08) — this session, decisions surfaced inline below

Where this README disagrees with earlier handoffs, **this README wins**. The latest session supersedes.

### 1. Belt: 2x72 silicon carbide, 120 → 1000 grit

Sackorange 6-pack 2x72 silicon carbide on Amazon (~$20/pack ≈ $3.30/belt). 120/240/400/600/800/1000 grit progression. **2x82 rejected** (custom-build pricing, 2–3× cost for SiC at glass-grade fine grits). **2x48 rejected** (insufficient platen length for single-pass finishing).

### 2. Platen: 22" usable length, glass-only, single-purpose

**22" platen** (revised from earlier 24" spec to leave room for larger pulleys — see decision #3). Two-pass finishing rejected — glass seam edges for optical adhesive bonding need single-pass consistency.

**18" max glass edge** is the hard design envelope: platen − 4" approach/exit margin so the edge enters and leaves cleanly. **Every Mind and Moss panel design must have its longest edge ≤ 18".** See `findings/design-constraints.md`.

### 3. Pulleys: 6" crowned drive, 3" crowned idler, 3D-printed PETG with stainless hub reinforcement

**Revised from earlier 5"/2" spec.** Going 6"/3" buys:
- More belt-to-pulley contact (better tracking, especially horizontal layout)
- Room for a robust crowned profile
- Bigger bearing seat for stainless reinforcement
- More thermal mass for sustained grinding
- Cost: 2" of platen — accepted

Crown depth ~0.020–0.040" (final value TBD against confirmed Sackorange belt width). Construction: 3D-printed PETG body with embedded stainless rod spokes radiating from a center boss; CNC last resort if printed-and-reinforced fails physical load testing.

### 4. Layout: horizontal — belt runs in a horizontal plane

The grinder lies sideways. Glass panels lay flat in a fixture, edge presented up into the belt at the **top edge of the belt where it crests over the platen** — single-line contact across the belt width.

Implications:
- **Crowned pulleys non-negotiable** (gravity tries to pull belt off the bottom of the pulleys in horizontal layout)
- **Tensioner direction flips:** idler is sprung outward against pure screw force, no gravity assist
- **Coolant routing is gravity-friendly:** drip line above platen, slurry catch tray below
- **Operator stance: seated** (see decision #5)

### 5. Operator: seated rider position

Aero/TT-bike position with hands forward at platen height. Standing pedaling fatigues fast (sprint posture, not endurance). Seated keeps cadence sustainable and matches Isaiah's "conversational pace" target.

### 6. Workpiece fixture: rail-guided sled with full-width straight-edge pusher

Glass panel sits flat in the sled, a straight-edge pusher across the full panel width keeps the edge perfectly parallel to the belt as the whole sled moves forward. Solves: (a) operator doesn't guess where the middle is, (b) belt inconsistencies don't translate to high/low spots on the edge.

### 7. Drivetrain: two chain stages, 10:1 speed-up

**Architecture (Q1b lock — option A from the lock-in session):**

```
pedals → crank → freewheel/one-way clutch
  → STAGE 1: 42T chainring → bike chain → 13T cog on intermediate shaft (3.23:1)
  → STAGE 2: 25T sprocket on intermediate shaft → bike chain → 8T pinion on grinder pulley shaft (3.125:1)
  → 6" crowned drive pulley (target 750 RPM)
  → 2x72 SiC belt → 22" platen → 3" crowned idler
```

**Why two stages:** stock bike gearing maxes out at ~4.8:1 (53T chainring × 11T cog) in a single chain run. Hitting 10:1 in one stage requires either oversized custom chainrings (60T+) or internal-geared hubs (Rohloff $1500+, Sturmey-Archer can't reach 10:1 alone). **Option B (oversized chainring) and option C (internal hub) both rejected.**

**Why 10:1 (and the SFM tradeoff):** target belt RPM = 750. Cadence = 75. So total ratio = 10:1. At 6" pulley × 750 RPM = 1180 SFM, upper edge of 500–1500 SFM glass-grinding spec. Mid-spec 7.5:1 was considered and rejected — Isaiah trusted the client research's 600–750 RPM range as a hard constraint, locked Option A. See `research/sprocket-stress-corrected.md` Section "SFM analysis" for the full tradeoff math.

**Stage materials:**
- Stage 1: stock donor-bike steel chainring (42T) + steel cassette cog (13T)
- Stage 2 large sprocket (25T): 3D-printed PETG, module 1.5, face 12 mm
- Stage 2 small pinion (8T): **machined steel or 6061 aluminum** (~$15 from SDP-SI or Boston Gear), module 2.0, face 16 mm. PETG fails the fatigue check at 8T at this load level.
- Two chains: 1/2" × 3/32" bicycle (KMC Z8.3 or equivalent), ~$15 each

### 8. Speed control: pedal cadence + RPM sensor (closed-loop)

Pedal cadence directly modulates belt speed (no electric motor, no VFD). Cheap Amazon RPM sensor logs actual belt RPM in real time → personal dataset of "this grit, this glass, this pressure, this RPM = best finish." Replaces guesswork with measured data. Target operating range: **600–750 pulley RPM** at the drive pulley (per client research).

### 9. Tensioner: screw-driven, no springs, feel-based tuning

Pure mechanical: idler wheel on a rigid pivot arm, adjustment screw pushes the arm outward as you turn it. **Springs explicitly rejected** — fatigue path Isaiah doesn't want to engineer around, no value for hand-cranked intermittent use.

**Tuning reference:** push belt sideways with thumb at mid-span; should deflect ~¼" under moderate hand pressure, snap back. Document in assembly guide.

### 10. Coolant: water drip line above platen, slurry catch tray below

Silicon carbide runs cooler wet, water flushes glass dust (silicosis risk). Horizontal layout makes routing gravity-friendly: drip → slurry → catch tray. Tray material/recirculation/disposal still open — see `open-questions.md`.

### 11. Hardware: stainless steel bolts, right-sized per joint, replaceable everywhere

M5 stainless as the baseline; larger stainless (e.g., ½") at high-stress anchors only (frame corners, drive pulley axle mount). **No oversizing for its own sake.** 304 stainless inventory baseline. Heat-set inserts (CNC Kitchen brass M3/M5) in PETG for blind threaded holes. See `research/heat-set-inserts.md`.

### 12. Frame: portable 3-module architecture, hybrid metal + 3D-printed nodes

**Three modules, each ~24–36" long, fits through 30" door, liftable by one person:**

1. **Rider module** — saddle, BB, cranks, chainring, freewheel
2. **Drivetrain bridge** — intermediate shaft + stage-1 driven cog + stage-2 driver sprocket
3. **Grinder module** — drive pulley, idler, platen, tensioner, belt path, sled rails, coolant tray

Connection joints: ~4 quick-release points total (wing-nut bolts or quarter-turn cam locks). Chains uncouple at master links for transport.

**Hybrid construction:**
- **Structural members:** mild steel or stainless tube/angle stock, hand-cut to length on Isaiah's table saw
- **Joint nodes:** 3D-printed PETG with embedded heat-set inserts for the bolts
- **Stainless rod reinforcement** at bearing-block locations

Aesthetic: knock-down trade-show booth — looks deliberate, breaks down clean, every part replaceable.

### 13. Donor bike: $40 floor, 7+ speed mountain bike

Facebook Marketplace target. Harvest crankset (cranks + chainring), bottom bracket, cassette/freewheel, possibly rear hub for the freewheel ratchet. Buy fresh from Amazon: chains (×2), sealed bearings (608-2RS or 6202-2RS), small driven pinion for the grinder pulley shaft.

**Pre-purchase checklist:** cassette spins/ratchets correctly, chainring teeth not bent or worn into "shark fin," cranks turn smoothly, no BB-area frame corrosion. Avoid: cruisers (single-speed coaster brake), frozen BBs, kids' bikes.

### 14. Operator workflow context

Isaiah's full glass workflow:
1. Cut glass with score tool + pliers
2. Pre-finish edges with **existing handheld wet grinder** (3/4" water-wheel, already owned)
3. **This bike grinder is the FINISHING stage** — takes a pre-cleaned edge from ~220-grit roughness down to 600–1000 for optical-adhesive bonding

**Implication:** light finishing work, not stock removal. Belt SFM at 1180 is upper-spec, accepted because cuts here are minimal. Optimize for stability, repeatability, surface quality.

---

## Bearings + chains spec (from corrected stress analysis)

- Intermediate shaft: 12 mm 304 stainless rod, 2× SKF 6202-2RS sealed deep-groove ball bearings
- Grinder pulley shaft: 8 mm 304 stainless rod, 2× NSK 608-2RS
- Both chains: KMC Z8.3 (1/2" × 3/32") bicycle, breaking strength ≥7,800 N (SF ≥6× at peak chain tension)
- L₁₀ life on both bearing pairs exceeds 4,200 hours — far past 100 hr cumulative use target

Total bought-parts cost beyond the donor bike: **~$73**.

---

## Status

- [x] Genesis handoff received from voice session (2026-05-06)
- [x] Phase 0 review locked 14 design decisions (2026-05-07)
- [x] Q1–Q4 readiness lock-in (2026-05-08): math conflict resolved, architecture locked, envelope locked, donor spec locked, frame architecture locked, ratio locked at 10:1
- [x] Heat-set inserts research (`research/heat-set-inserts.md`)
- [x] FreeCAD 1.1 readiness research (`research/freecad-1.1-readiness.md`)
- [x] Corrected sprocket stress analysis (`research/sprocket-stress-corrected.md`)
- [ ] FreeCAD 1.1 parametric model: master sketch (drivetrain centers, frame footprint)
- [ ] FreeCAD 1.1 parametric model: each printable part as a linked .FCStd file
- [ ] FreeCAD 1.1 assembly: simulation-validate gear ratios visually before printing
- [ ] Bambu A1 Mini test-coupon for fit calibration (peg+socket pairs at clearances 0.10/0.15/0.20/0.25/0.30 mm)
- [ ] First print + load test — bearing block under pedal torque
- [ ] Donor bike acquired
- [ ] 8T machined-metal pinion sourced (~$15, SDP-SI or Boston Gear)

See `open-questions.md` for the punch list of what's still open.

---

## Cross-references

- Brand context: `CLAUDE.md` (root)
- Current state: `findings/SESSION-HANDOFF.md`
- **Top-level constraints: `findings/design-constraints.md`** ← 18" max glass edge lives here
- Decisions pending: `findings/decisions-pending.md`
- Glass technique research: `findings/topics/fabrication/glass-edge-grinder.md`
- Material inventory: `setup.md`
- Heat-set inserts: `research/heat-set-inserts.md`
- FreeCAD 1.1 readiness: `research/freecad-1.1-readiness.md`
- Corrected sprocket stress: `research/sprocket-stress-corrected.md`
- Open questions: `open-questions.md`
- Voice session transcripts: `sessions/`
