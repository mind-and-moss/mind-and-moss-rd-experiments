# FreeCAD 1.1 — Readiness for the Bike-Powered Glass Grinder

**Date:** 2026-05-07
**Purpose:** Pre-flight research before Isaiah opens FreeCAD 1.1 to start parametric modeling. Captures (A) what changed in 1.1 vs 1.0, (B) the data Isaiah needs to lock before modeling starts, and (C) non-obvious leverage moves that match Mind and Moss's "how the fuck did they make that" standard.

Source: background research agent dispatched 2026-05-07. Sources cited inline. Convention note: this is external-research-synthesis, not a verbatim thread excavation.

---

## Part A — What changed in FreeCAD 1.1 vs 1.0

### Sketcher
The big one: **external geometry is now defining (real) by default** — no more tracing it as construction lines just to use it. New dedicated **Projection** and **Intersection** tools, group-dragging of selected entities, infinite-length sketch axes, and a preference to decouple external-geometry creation from current construction mode.

[Release Notes 1.1](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Release_notes_1.1.md)

### Part Design
- Origin redesigned on the new **core Datums** system (Datum Plane / Line / Point / CSYS). These are first-class and reusable in Assembly joints.
- Hole feature gained Whitworth (BSW/BSF/BSP/NPT) threads
- Modeled-thread performance improved
- New "Toggle Freeze" command

**Compatibility caveat:** `.FCStd` files saved in 1.1 will break when opened in 1.0 because of datum-orientation changes. **Pin everyone on 1.1.** No round-tripping back through 1.0.

### Assembly
FreeCAD 1.0 introduced the official Assembly workbench. 1.1 adds:
- "Insert a new part" tool (faster bottom-up assembly)
- **Create Simulation** tool — joint motion / animation. Huge for sanity-checking the bike drivetrain kinematics before fabrication.
- Joints can now attach to the new core datums

Workflow is still bottom-up: insert links → ground one → joint others → test motion.

[blog.freecad.org — 1.1 release](https://blog.freecad.org/2026/03/25/freecad-version-1-1-released/), [Assembly tutorial](https://blog.freecad.org/2024/09/30/tutorial-getting-started-with-the-assembly-workbench/)

### Spreadsheet
Minor surface changes — bold/italic/underline shortcuts, double-click column auto-resize, zoom.

The big philosophical shift: **1.0 introduced VarSets**, and the 1.1 community consensus is consolidating around:
- **VarSets for design parameters** (the things that drive geometry)
- **Spreadsheet for BOM / fab-handoff tables** (the things you hand to manufacturing)

[Spreadsheets & Parametric Design tutorial](https://blog.freecad.org/2025/04/08/tutorialgetting-started-with-spreadsheets-and-parametric-design/)

### Python API
No documented breaking changes in 1.1 release notes. Standard `App.ActiveDocument`, `Sketcher`, `PartDesign` Python interfaces from 1.0 carry forward. **Macros written for 1.0 should run on 1.1.**

### TechDraw
- Area Annotation now correctly handles holes in faces
- New shape-validation toggle in Preferences
- Link handling in DraftViews fixed
- SVG symbol scaling corrected

### File format
.FCStd is forward-only safe (1.1 → 1.1+). Don't round-trip through 1.0.

---

## Part B — Decisions to lock before opening FreeCAD

### Top-level VarSet — `Grinder_Params`

Isaiah needs to provide values for these before the model starts. Fields tagged **[need]** require Isaiah's input; **[derived]** are computed from other fields.

**Drivetrain:**
- `bike_cassette_teeth_min` / `bike_cassette_teeth_max` **[need]** — what cassette is on the donor bike?
- `freewheel_teeth` **[need]** — what tooth count does the freewheel use? (Drives gear-stage-1 ratio.)
- `drive_pulley_dia` = **5"** (locked)
- `idler_pulley_dia` = **2"** (locked)
- `belt_pitch` **[need]** — only relevant if we go GT2/HTD timing belt for an internal stage. For the silicon carbide grinding belt itself, pitch isn't relevant.
- `belt_length` = **72"** (locked, Sackorange 2x72)
- `target_belt_rpm` = **750 RPM** (locked)
- `pedal_rpm_nominal` = **75 RPM** (locked)
- `gear_ratio_total` **[derived]** = `target_belt_rpm / pedal_rpm_nominal` = 10:1 ❌ — wait. This is **8:1 per the Phase 0 review**, which means the math implies 75 × 8 = 600 RPM, not 750. **Decision needed:** is the locked ratio 8:1 or 10:1, or is the locked pedal RPM 93–94 instead of 75? See "Math reconciliation" below.

**Glass workpiece envelope:**
- `max_panel_edge_length` **[need]** — the longest single edge on any Machine gem-component panel. Drives whether 24" platen is enough.
- `max_panel_thickness` **[need]** — Isaiah's stock is 6 mm aquarium glass per inventory. Confirm.

**Bearings (bought parts — pick part numbers now so envelopes can be modeled):**
- `spindle_bearing_OD` / `spindle_bearing_ID` / `spindle_bearing_W` **[need]** — typical knife-grinder default is 6202-2RS (15 ID × 35 OD × 11 W mm) for the drive shaft, smaller (608-2RS) for the idler. Confirm or pick.

**Frame:**
- `frame_height` **[need]** — drives platen height relative to seated rider position
- `frame_width` **[need]**
- `frame_depth` **[need]**
- `tube_OD` / `tube_wall` **[need]** — only if we use steel tube structurally; if pure 3D-print + stainless rod reinforcement, this is N/A
- **`max_print_dim` = 170 mm** — Bambu A1 Mini build volume is 180×180×180 mm; 170 mm leaves margin for first-layer bed adhesion and avoids edge artifacts. Any frame member >170 mm in any axis must split into multiple printable parts. **Use this as a constraint check** in the manufacturability validator macro (Part C #3).

**Print fits (PETG on A1 Mini — verify with a printed coupon first):**
- `fit_clearance_loose` = 0.30 mm
- `fit_clearance_press` = 0.10 mm
- `fit_clearance_running` = 0.20 mm

[Tolerance reference](https://www.raphaelgarcia.me/blog/2024/9/9/tolerances-and-fits-in-3d-printing-how-to-get-it-right-with-your-bambu-lab-x1c)

### Math reconciliation needed

The Phase 0 review locked **8:1 reduction with 75 RPM cadence**, but separately stated **750 RPM target belt speed**. 75 × 8 = 600, not 750.

Likely reconciliations:
- (a) Cadence is 93–94 RPM, not 75 (Isaiah is faster than the conversational baseline)
- (b) Reduction is 10:1, not 8:1 (the original 10:1 was right and 8:1 was a stress-driven downgrade that nobody re-ran the math on)
- (c) Belt RPM target is 600, not 750 (the 750 number was carried over from a 5"-pulley-at-10:1 calc that's now obsolete)

**Need Isaiah to confirm one of these** before drivetrain geometry locks in FreeCAD. Don't model assuming any of the three.

### Independent vs derived parameters

| Independent (Isaiah picks) | Derived (formulas) |
|---|---|
| Pulley diameters (5" drive, 2" idler) | Gear ratio total |
| Target RPM | Belt path length around pulleys |
| Bought-part dimensions | Pulley center distance |
| Frame envelope | Splice locations / part split planes |
| Cassette + freewheel tooth counts | Stage-1 vs stage-2 ratio split |

### File hierarchy

**One folder per project. Multiple files, linked.**

```
freecad/
├── Grinder_Params.FCStd        ← VarSet + master sketch (drivetrain centers, frame footprint)
├── Grinder_Assembly.FCStd      ← App-Links every printable + bought-part shell
├── parts/
│   ├── drive_pulley.FCStd      ← one printable per file
│   ├── idler_pulley.FCStd
│   ├── frame_left.FCStd
│   ├── frame_right.FCStd
│   ├── platen_mount.FCStd
│   ├── sled.FCStd
│   ├── tensioner_arm.FCStd
│   └── ...
└── bought/
    ├── bearing_6202.FCStd      ← simple envelope from datasheet
    ├── freewheel.FCStd
    ├── cassette.FCStd
    └── ...
```

**Why this pattern:** App-Link-based assembly lets you re-print a single sled without dirtying the assembly file's history. Every part file external-references `Grinder_Params.FCStd`'s master sketch — move a pulley center 5 mm, every bracket regenerates.

References:
- [Multi-file pattern (XSim)](https://www.xsim.info/articles/FreeCAD/en-US/HowTo/Assemble-multiple-files-into-a-single-file.html)
- [Share VarSet across files (YouTube)](https://www.youtube.com/watch?v=ZHYmFKmMnUI)

---

## Part C — Non-obvious leverage moves

These are the "how the fuck did they do that" moves — patterns that compound force-multiplier on a parametric workflow.

### 1. Master sketch in `Grinder_Params.FCStd` defines drivetrain geometry in 2D
Pulley centers, frame footprint, platen position — all live as a single master sketch in the params file. Every part `.FCStd` external-references it. Move a pulley center 5 mm in the master sketch → every bracket, mounting hole, and frame member that derives from it regenerates automatically.

**1.1 makes this dramatically cleaner than 1.0** because external geometry is now defining by default — no more "trace it as construction line just to use it" boilerplate.

### 2. Python macro for repetitive features
A ~30-line script iterates `bolt_pattern_radius`, `hole_count`, `hole_dia` from the VarSet and adds Datum Points + Hole features to a body. Use this for:
- Pulley bolt circles (especially if pulleys split for multi-piece printing)
- Frame mounting plates
- Sled rail attachment patterns

Saves hours of click-by-click repetition and ensures every hole comes from the same spec.

### 3. Manufacturability validator macro
Walk every Body in the assembly, get its bounding box, assert `bbox.x/y/z < max_print_dim` (170 mm). Print a red console warning per part that exceeds.

**Catches "won't fit on the A1 Mini" before slicing**, which is the difference between catching a problem in 30 seconds vs after 4 hours of failed print attempts.

### 4. TechDraw auto-page generator
A macro that loops printable parts and emits a TechDraw page per part with front/top/iso views + dimensions pulled from the VarSet. Hit one button → instant fab packet for every part.

When Isaiah eventually has the grinder built and wants to publish the design (or re-use it for a future tooling iteration), this is what makes the difference between "polished documentation" and "I'll redo the drawings someday."

### 5. Assembly Simulation kinematic validation (new in 1.1)
Drive the cassette joint at `pedal_rpm_nominal`, watch the drive-pulley shaft RPM in the joint readouts. Validates the `gear_ratio_total` formula visually before any geometry locks.

This is also the cleanest way to catch interference issues — does the freewheel collide with the frame mount when it rotates? Simulate it before printing.

### 6. Test-coupon `.FCStd` for fit calibration
A separate test file with parametric peg+socket pairs at clearance 0.10 / 0.15 / 0.20 / 0.25 / 0.30 mm. Print once on the A1 Mini, pick the winner (the one that slides without slop), write that number into `Grinder_Params.fit_clearance_running` — every part in the project updates.

**This is the single highest-leverage hour Isaiah can spend before printing real parts.** Get the fits calibrated to his actual printer + filament + temperature, then every downstream part inherits the right tolerance.

---

## Sources

- [FreeCAD 1.1 Release Notes (official)](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Release_notes_1.1.md)
- [FreeCAD 1.1 Released — blog.freecad.org](https://blog.freecad.org/2026/03/25/freecad-version-1-1-released/)
- [Spreadsheets & Parametric Design tutorial](https://blog.freecad.org/2025/04/08/tutorialgetting-started-with-spreadsheets-and-parametric-design/)
- [Assembly workbench tutorial](https://blog.freecad.org/2024/09/30/tutorial-getting-started-with-the-assembly-workbench/)
- [Multi-file assembly pattern (XSim)](https://www.xsim.info/articles/FreeCAD/en-US/HowTo/Assemble-multiple-files-into-a-single-file.html)
- [Share VarSet across files (YouTube)](https://www.youtube.com/watch?v=ZHYmFKmMnUI)
- [Bambu tolerances & fits guide](https://www.raphaelgarcia.me/blog/2024/9/9/tolerances-and-fits-in-3d-printing-how-to-get-it-right-with-your-bambu-lab-x1c)
- [Industry Insider — FreeCAD 1.1 overview](https://industryinsider.eu/3d-designing-and-simulation/freecad-1-1-improvements-following-the-latest-major-update/)
