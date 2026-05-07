# Bike-Powered Glass Grinder — Tooling

**Date created:** 2026-05-07
**Source:** Voice session with Claude (mobile, Mind and Moss Project) — Session 5 handoff to Claude Code via Chrome MCP.
**Suggested branch (this branch):** `tooling/bike-powered-grinder`

This folder is **tooling, not product**. It's the machine that makes the machine. But it's still held to Mind and Moss's "how the fuck did they make that" standard — visible mechanical beauty, deliberate engineering, not a cobbled-together hack.

---

## TL;DR

Isaiah is designing a **bike-powered glass grinder** as a prerequisite tool before any Mind and Moss product can be manufactured. This tool will be used across most/all future products, not just The Machine's gem-component. Voice session locked the architecture, constraints, and material strategy. Next pass: start FreeCAD 1.1 modeling of the drivetrain and frame, parametric so dimensions can shift as we test.

## Why this exists

Isaiah cannot precision-finish glass panel edges to optical-clarity standard with current inventory. The gem-component within The Machine requires panel seams that bond cleanly with UV optical adhesive (NOA 65 or NOA 148, per `findings/decisions-pending.md` #1). Any edge irregularity = bond failure, optical distortion, or visible seam defect. The grinder is the gate that opens The Machine's manufacturability.

It's also the gate for every other Mind and Moss product that uses precision-cut glass. Solving this once unlocks the whole product roadmap.

## Brand reframe context (Session 4 carryover)

Per `CLAUDE.md` and `findings/SESSION-HANDOFF.md`: "The Gem" is no longer a standalone product. It's a glass component within The Machine. The brand's through-line is **biotope fidelity** — environments built so accurately that species express behaviors hobbyist setups don't produce. This grinder serves that mission by enabling the precision required for the form factors that house biotopes.

Don't reintroduce "The Gem" as a peer product anywhere in the grinder docs.

---

## Locked design decisions (from voice session)

### 1. Working surface: minimum 24-inch usable platen length

**Rationale:** Two-pass finishing is unacceptable. Glass seam edges for optical adhesive bonding need single-pass consistency. Even sub-micron variation between passes shows up as a visible defect or causes seam failure under thermal cycling.

**Implication:** Standard 2x72 belts give ~6–8" platens. Need to go custom-frame with 2x48 minimum, possibly longer. Belt selection drives pulley spacing, which drives frame length.

### 2. Belt spec: 2x48 or 2x72, silicon carbide, 120 → 1000 grit

**Confirmed inventory direction:** Sackorange 6-pack 2x72 silicon carbide on Amazon (~$20/pack = ~$3.30/belt). 120/240/400/600/800/1000 grit progression.

**Open question for Claude Code research:** Does a 2x48 setup let us run that same belt assortment, or do we commit to 2x72 length with a longer frame? Need price-per-belt comparison at the longer custom lengths if we go above 72".

**Higher grits (1500+, 3000+, polishing compounds) deferred to a later session.**

### 3. Drivetrain: bike-powered with one-way clutch (freewheel)

**Behavior:** Pedaling adds speed. Stopping pedaling does NOT stop the belt — it coasts, like a real bicycle drivetrain. Resume pedaling = add more speed on top of current belt RPM.

**Mechanism:** Bicycle-style freewheel hub or industrial overrunning clutch between crank and gear train. The grinder shaft spins free of the crank once the clutch disengages.

**Why this matters:** Lets Isaiah focus entirely on glass positioning during a grinding pass, no fighting pedal resistance. Also lets him stop pedaling, position the next panel, then resume without losing belt momentum.

### 4. Speed control: pedal cadence + RPM sensor for closed-loop validation

- Pedal cadence directly modulates belt speed (no electric motor, no VFD)
- RPM sensor (Amazon, cheap) logs actual belt RPM in real time
- Lets Isaiah build a personal dataset: "this grit, this glass, this pressure, this RPM = best finish"
- Replaces guesswork with measured data

**Target operating range:** 500–2000 RPM at the belt-drive pulley, depending on grit. Coarse grits (120–240) tolerate higher speed. Fine grits (800–1000) want lower speed to avoid heat-induced thermal shock in the glass.

### 5. Gear reduction: 10:1 to 20:1 from crank to belt-drive pulley

**Math:** Standard cycling cadence is 60–100 RPM. Target belt pulley is 500–2000 RPM. So:

- At 80 RPM cadence × 10:1 ratio = 800 RPM at pulley (mid-range, mid-grit)
- At 80 RPM cadence × 20:1 ratio = 1600 RPM at pulley (higher grits)

A multi-speed cassette (like a normal bike's rear cassette) could give Isaiah switchable ratios for different grit stages. This is worth modeling — it's elegant and uses cycling parts we know are durable.

### 6. Material strategy: 3D print first, stainless steel reinforcement, silicone bonding

**Hierarchy of fabrication:**

1. **Primary:** 3D-printed structure on Bambu A1 Mini. Fast iteration. Geometry-driven design (ribs, fillets, infill optimization for stress).
2. **Reinforcement:** Stainless steel plates and inserts at bearing blocks, gear mounts, axle supports — anywhere torque concentrates.
3. **Bonding:** Silicone for plastic-to-metal interfaces. Vibration damping. Tolerates flex without cracking the print.
4. **Last resort:** CNC-machined parts ONLY if 3D-printed-and-reinforced parts fail under measured load testing.

**Why this order:** Cost, iteration speed, learning. Isaiah is a Blender user comfortable with geometry; FreeCAD parametric models export to STL cleanly; failed prints are cheap; CNC is a money sink reserved for proven-necessary geometry.

### 7. Concern hierarchy

**NOT a concern:** Isaiah's leg fatigue. He's run a marathon. Sustained pedaling for hours is fine.

**IS a concern:** Material strain under sustained torque. Specifically:

- Gear tooth shear under continuous load
- Pulley deformation at high RPM
- Bearing block fatigue (the 3D-printed mounts)
- Chain or belt tension creep
- Frame flex at the platen mount (any flex = inconsistent grind = defective glass edge)

Claude Code's modeling needs to flag every high-stress region for stainless reinforcement.

---

## Architecture diagram (text)

> The original handoff artifact had an architecture diagram section that did not transfer cleanly through the Chrome MCP clipboard pipeline. **Reconstructed flow per the locked decisions above:**

```
   pedal crank
       │
       ▼
   freewheel / one-way clutch        ← lets belt coast when pedaling stops
       │
       ▼
   gear reduction stage 1 (e.g., bicycle cassette)
       │
       ▼
   gear reduction stage 2 (chain or belt to grinder pulley)
       │
       ▼
   belt-drive pulley (target 500–2000 RPM)  ← RPM sensor here
       │
       ▼
   2x72 (or 2x48) silicon carbide belt
       │
   ┌───┴───────────────────┐
   │                       │
 idler pulley            drive pulley
   │                       │
   └─── 24" flat platen ───┘    ← stainless-steel-reinforced, ground-flat reference surface
                ▲
                │
        glass panel edge being ground
        (held in jig, perpendicular to platen)
```

**TODO:** Verify against Isaiah's voice-session intent in next conversation; replace with confirmed diagram.

---

## P.S. from Isaiah — additional research request

**For Claude Code:** please gather information about **heat-set inserts** for the bike-powered grinder build:

- Heat-set inserts (brass vs stainless) for use in 3D-printed plastic
- Sizing standards (M3, M5 — match Isaiah's existing hardware inventory)
- Installation method (soldering iron temperature, technique, tools)
- Pull-out and torque resistance compared to press-fit alternatives
- Brands / sources (McMaster, AliExpress, Amazon — price + lead time)
- Best practices for designing the receiving hole geometry in 3D prints
- Failure modes (insert spinning under torque, melting the plastic during install, etc.)

This research feeds directly into the stainless reinforcement strategy (decision #6) and into FreeCAD modeling of every bearing block and fastener point.

**Filing instructions:** add the research write-up to `tooling/bike-powered-grinder/research/heat-set-inserts.md`. This sits alongside other Phase 1 research files in the same folder.

---

## Status: Phase 0 — handoff received, scaffolding in place

- [x] Handoff received from voice session
- [x] Folder scaffold created on branch `tooling/bike-powered-grinder`
- [ ] Heat-set inserts research (in flight via background agent)
- [ ] Verify architecture diagram against Isaiah's intent
- [ ] FreeCAD 1.1 parametric model of drivetrain
- [ ] FreeCAD 1.1 parametric model of frame + platen mount
- [ ] Stainless reinforcement plan (which 3D-printed parts get steel inserts/plates, where, why)
- [ ] Bill of materials (cycling parts: crank, freewheel, cassette, chain; bearings; pulleys; sensors)
- [ ] First print + test — bearing block load test under pedal torque

---

## Cross-references

- Brand context: `CLAUDE.md` (root)
- Current state: `findings/SESSION-HANDOFF.md`
- Decisions: `findings/decisions-pending.md` (especially #1 — gem-component seam type)
- Glass technique: `findings/topics/fabrication/glass-edge-grinder.md` (the AI-excavation research that this physical build implements)
- Material inventory: `setup.md` — esp. M3 + M5 stainless hardware, 304 stainless rod, Bambu A1 Mini, glass cutter + grinder + 6mm aquarium glass stock
