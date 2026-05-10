# FreeCAD Pickup Context — Bike-Powered Glass Grinder

**Load this file (and ONLY this file) at the start of any session focused on the
FreeCAD parametric model.** It supersedes `SESSION-HANDOFF.md` and `CLAUDE.md`
for FreeCAD work — both files cover broader project state that doesn't apply
when the active task is "build the next macro / part / assembly."

If your task is non-FreeCAD (brand, product decisions, other tooling), stop
and load `SESSION-HANDOFF.md` instead.

---

## What this is

A FreeCAD 1.1 parametric model of the bike-powered glass grinder, driven
entirely by a single source-of-truth file (`Grinder_Params.FCStd`) containing
named VarSets that downstream geometry references via expressions. Built and
mutated by idempotent Python macros, run headless via `freecadcmd.exe`.

State as of this writing: 7 VarSets / 41 properties; MasterSketch fully
constrained (10 geometry, 25 constraints, 13 expression bindings); all
parametric bindings verified live end-to-end.

---

## Working pipeline (locked patterns — copy these)

**FreeCAD binary:**
```
"C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe"
```
The `freecadcmd.exe` (NOT `FreeCAD.exe`) is the headless console build. Use it
for all routine macro runs — Isaiah only opens the GUI for visual inspection.

**Macro pattern (every macro):**
- User-facing macro: `NN_<verb>_<thing>.py` — runnable from GUI's macro panel,
  documents what + why, no save call (GUI handles save).
- Headless wrapper: `run_macro_NN_headless.py` — opens `Grinder_Params.FCStd`,
  `exec()`s the user-facing macro, calls `App.ActiveDocument.save()`. Macro 01
  is special-cased (creates the doc fresh).
- **Idempotency rule:** every macro that mutates the sketch starts with
  ```python
  while sketch.ConstraintCount > 0: sketch.delConstraint(0)
  while sketch.GeometryCount > 0: sketch.delGeometry(0)
  ```
  Re-running gives the same state. No accumulating duplicates.
- **Lineage rule:** macro N supersedes macro N-1 for the same domain. After
  macro 04, re-running macro 03 alone *undoes* macro 04's additions. Always
  run the highest-numbered macro for the domain you touch.

**VarSet expression syntax (FreeCAD 1.1):**
- Same-doc cross-VarSet ref: `<<VarSetName>>.property_name`
- Trig: `sin(180 deg / N)` — the `deg` literal forces degree interpretation
- Exponentiation: `^` (NOT Python's `**` — FreeCAD expressions use `^`)
- Built-in math: `sqrt`, `sin`, `cos`, `tan`, `pow`, etc.
- Units propagate: `mm * mm = mm²`, `sqrt(mm²) = mm`. PropertyLength accepts mm.

**Sketcher constraint API (FreeCAD 1.1):**
- Origin reference: `GeoId = -1, PosId = 1`
- Circle vertex codes: `PosId = 3` is the center
- Line vertex codes: `PosId = 1` is start, `PosId = 2` is end
- `Sketcher.Constraint("Coincident", a_idx, a_pos, b_idx, b_pos)`
- `Sketcher.Constraint("Diameter", circle_idx, mm_value)`
- `Sketcher.Constraint("DistanceX"/"DistanceY", a_idx, a_pos, b_idx, b_pos, value)`
- `Sketcher.Constraint("Horizontal"/"Vertical", line_idx)`
- `Sketcher.Constraint("Distance", line_idx, length_mm)`
- Bind expression to constraint: `sketch.setExpression(f".Constraints[{idx}]", expr)`
- Bind expression to VarSet property: `varset.setExpression("propertyName", expr)`

**Quantity coercion (gotcha):**
PropertyLength returns an `App.Quantity` (carries units). For arithmetic, use
`.Value` to get the float in mm: `qty.Value if hasattr(qty, "Value") else float(qty)`.

**Stdout buffering (gotcha):**
`print()` output from inside a macro is unreliable under `freecadcmd.exe` —
sometimes flushed, sometimes swallowed. Use `App.Console.PrintMessage(msg)` for
anything you need to see. For test scripts, also write a side-channel report file.

---

## Current macro chain

| # | File | What it does |
|---|---|---|
| 01 | `01_create_grinder_params.py` | Creates the doc + 7 VarSets + empty MasterSketch |
| 02 | `02_scaffold_drivetrain_geometry.py` | Adds 10 construction elements with hardcoded values |
| 03 | `03_bind_geometry_to_varsets.py` | Wipes + rebuilds with 21 constraints + 9 expr bindings |
| 04 | `04_constrain_shafts_and_chain_distances.py` | Supersedes 03. Adds 4 shaft locks + 2 computed CD properties |
| 05 | `05_create_drive_pulley_part.py` | Creates `parts/drive_pulley.FCStd` (PartDesign Body + Sketch + Revolution). v1: cylinder + bore, no crown, hardcoded values from master. |
| 06 | `06_create_drivetrain_placeholders.py` | **Current head for parts.** Creates 7 more part placeholders in one run: idler_pulley, stage2_pinion, stage2_large, stage1_cog, chainring, intermediate_shaft, grinder_shaft. Each is a hollow-cylinder placeholder (no gear teeth) — sized to chain-pitch diameter so chain-engagement clearances are accurate. Shafts are solid (bore=0). |

Diagnostic / utility (not part of the chain):
- `verify_parametric_binding.py` — sanity check after touching any expression code
- `export_stl.py [partname]` — writes ASCII STL alongside any part .FCStd. Bypasses MeshPart.meshFromShape (which hangs) by using `shape.tessellate()` + manual ASCII STL writing. Default partname: `drive_pulley`.

Diagnostic (not part of the chain): `verify_parametric_binding.py` — mutates
`Pulleys.drive_pulley_dia` 152.4→180, checks the drive pulley circle radius
recomputed, reverts. Run as a sanity check after touching any expression code.

## parts/ inventory (after macro 06)

| File | OD (mm) | Bore (mm) | Height (mm) | Purpose |
|---|---|---|---|---|
| drive_pulley.FCStd | 152.4 | 8.20 | 60 | 6" drive pulley, PETG print, sits on grinder shaft |
| idler_pulley.FCStd | 76.2 | 8.20 | 60 | 3" idler pulley, PETG print |
| stage2_pinion.FCStd | 33.18 | 8.20 | 16 | 8T pinion, machined metal, on grinder shaft (placeholder disk) |
| stage2_large.FCStd | 101.33 | 12.20 | 12 | 25T sprocket, PETG print, on intermediate shaft (placeholder) |
| stage1_cog.FCStd | 53.07 | 12.20 | 5 | 13T donor steel cog, on intermediate shaft (placeholder) |
| chainring.FCStd | 169.94 | 16 | 5 | 42T donor steel chainring, on crank/BB (placeholder) |
| intermediate_shaft.FCStd | 12 (solid) | — | 150 | 12mm 304 stainless rod (donor stock) |
| grinder_shaft.FCStd | 8 (solid) | — | 150 | 8mm 304 stainless rod (donor stock) |

All have matching `.stl` files generated via `export_stl.py`. Sprockets/cog/chainring use chain-pitch diameter as OD — geometrically accurate for chain-engagement clearance, but no actual gear teeth (placeholder disks).

## Open issues / gotchas (Session 7)

- **Cross-doc expression bindings (`<<Grinder_Params#Pulleys>>.drive_pulley_dia`) are flaky in part files.** The syntax resolves correctly when set in isolation (diagnostic confirms 152.4) but Revolution.Shape stays null in-session when constraints have such bindings. Macros 05 + 06 hardcode values from master at macro-build time; live cross-doc binding revisited later once the recompute-time resolution is understood. Try App::Link objects as an alternative to `<<>>` syntax.
- **MeshPart.meshFromShape + mesh.write hangs under freecadcmd.** Solved by `export_stl.py` using `shape.tessellate()` + manual ASCII STL writing — bypass works reliably for all 8 parts so far.
- ~~All cylindrical parts have axis along global Y, not Z.~~ **Retracted in Session 8.** Empirical bounding-box inspection of all 8 parts shows the cylinder axis is actually on global Z (height runs Z=0..H, OD spans X and Y equally). The earlier warning was a misdiagnosis — the sketch placement rotation in macros 05/06 (`App.Rotation(Vector(1,0,0), 90)`) does correctly land V_Axis on global Z. Macro 07 (assembly) places links with pure translation, no rotation.
- **No gear teeth on sprockets/cog/chainring.** Placeholders use pitch diameter as OD. Real teeth come later via PartDesign Gear workbench or external tooth-generator macro.
- **No crown on pulleys.** 0.75 mm rise needed per locked spec for belt tracking. v2 macro will add.

---

## Current sketch state (after macro 04)

```
geometry:           10 elements (3 pulley circles + 4 platen lines + 3 sprocket circles)
constraints:        25 (21 from macro 03 baseline + 4 shaft locks)
expression bindings 13 (9 sketch constraint bindings + 2 VarSet computed + 2 nested via positions)
sketch is fully constrained (zero degrees of freedom)
```

---

## VarSet quick reference (current values, all parametric)

| Group | Property | Value | Notes |
|---|---|---|---|
| Drivetrain | cadence_rpm | 75 | conversational pace |
| Drivetrain | target_belt_rpm | 750 | upper-glass-spec |
| Drivetrain | total_ratio | 10.0 | 75 × 10 = 750 ✓ |
| Drivetrain | stage1_chainring_teeth | 42 | donor steel |
| Drivetrain | stage1_cog_teeth | 13 | donor steel |
| Drivetrain | stage2_large_teeth | 25 | PETG print |
| Drivetrain | stage2_pinion_teeth | 8 | machined metal (PETG fails fatigue here) |
| Drivetrain | chain_pitch | 12.7 mm | 1/2" bicycle |
| Drivetrain | intermediate_shaft_x/y | (0, 500) mm | macro 04 default |
| Drivetrain | crank_bb_x/y | (0, 1100) mm | macro 04 default |
| Drivetrain | stage1_chain_center_distance | 600 mm | **computed** from positions |
| Drivetrain | stage2_chain_center_distance | 500 mm | **computed** from positions |
| Pulleys | drive_pulley_dia | 152.4 mm | 6" crowned |
| Pulleys | idler_pulley_dia | 76.2 mm | 3" crowned |
| Pulleys | pulley_crown_depth | 0.75 mm | refine after belt arrives |
| Pulleys | pulley_face_width | 60 mm | wider than 2" belt |
| Belt | belt_width | 50.8 mm | 2" Sackorange SiC |
| Belt | belt_length | 1828.8 mm | 72" |
| Belt | belt_path_center_distance | 734.9 mm | derived from belt geometry |
| Platen | platen_length | 558.8 mm | 22" usable |
| Platen | platen_width | 60 mm | matches pulley face |
| Platen | platen_thickness | 12 mm | TBD, starting point |
| Platen | max_glass_edge | 457.2 mm | **HARD CONSTRAINT — 18"** |
| Frame | max_print_dim | 170 mm | **HARD CONSTRAINT — Bambu A1 Mini** |
| Frame | module_target_length | 762 mm | 30" door clearance |
| Fits | fit_clearance_loose / running / press | 0.30 / 0.20 / 0.10 mm | calibrate via test coupon |
| Bearings | intermediate_shaft_dia | 12 mm | 304 stainless rod |
| Bearings | grinder_shaft_dia | 8 mm | 304 stainless rod |

(Bearings group also has bearing OD/ID/W for both shafts — 6202-2RS and 608-2RS.)

---

## Hard constraints (don't violate without surfacing)

- **18" max glass edge** on any panel design — `Platen.max_glass_edge = 457.2 mm`
- **170 mm max printable dimension** in any axis — `Frame.max_print_dim = 170`
- **Units are mm** throughout, even for inch-spec parts (6" pulley = 152.4 mm)
- **FreeCAD 1.1.x only** — `.FCStd` files are NOT backward-compatible with 1.0

---

## What's next

**Macro 05 — assembly-level part split.** Start producing individual part
`.FCStd` files App-Linked to `Grinder_Params.FCStd` for parameters. Drive
pulley first (simplest 3D extrusion + hub geometry). Generate STL.

After macro 05: first physical print + bench load test on the drive pulley
with embedded stainless rod hub.

---

## What NOT to do

- Don't run macro 03 after macro 04 (undoes the shaft locks). Always run the
  highest-numbered macro for the domain you're touching.
- Don't edit `Grinder_Params.FCStd` in FreeCAD 1.0 (file format incompatible).
- Don't store chain center distance as an independent VarSet property — it's
  derived from shaft positions via expression. Editing it directly creates a
  conflict with the position-based computation.
- Don't `print()` from inside a macro and assume the output appears under
  `freecadcmd.exe` — use `App.Console.PrintMessage`.
- Don't bind expressions before adding the geometry they reference (Sketcher
  errors with "constraint references nonexistent geometry").

---

## Cross-references (only follow if directly relevant)

- Locked grinder spec (mechanical): `tooling/bike-powered-grinder/README.md`
- Stress analysis backing the gear/bearing choices: `research/sprocket-stress-corrected.md`
- FreeCAD 1.1 readiness research (datums, assembly, VarSets): `research/freecad-1.1-readiness.md`
- Top-level project state, PRs, decisions awaiting Isaiah: repo-root
  `findings/SESSION-HANDOFF.md` (on `meta/decisions-and-handoff` branch)
- Brand voice / how-we-work / Isaiah's skill level: repo-root `CLAUDE.md`
