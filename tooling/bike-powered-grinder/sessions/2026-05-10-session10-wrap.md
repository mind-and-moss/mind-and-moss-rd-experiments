# Session 10 — Wrap (2026-05-10)

End-of-session summary for the bike-powered glass grinder. Branch:
`tooling/bike-powered-grinder`.

## What got built

Session 10 ran in five distinct chunks:

### 1. Bevel pair + cast-block + truss + 1:1 ratio lock (commit `98a7d94`)
- Replaced `RA_Drive_Placeholder` black box with **two visible cone-frustum bevel gears** at apex (X=300, Y=400, Z=450)
- 1:1 bevel ratio chosen — chain stages do all reduction
- Restored stage-2 chain (`stage2_large` 25T → `stage2_pinion` 8T) for the final 3.125× step
- Total drivetrain ratio = 3.231 × 1.00 × 3.125 = **10.096** ✓
- BB ground-support truss landed: cast pyramidal-frustum block (240×400 base, 200×200 top, 200 h, ~32 kg cast concrete), 50mm fat post, BB split-collar clamp, diagonal strut
- Pedal-clearance constraint set the block X-width: foot inner edge at X≈140, block half-width 120 → 20mm clearance

### 2. Phase 1 — Review pass (commit `ef6aa06`)
- 21-item inventory of literal gaps + inconsistencies + missing structural elements
- Risk assessment for the Phase 2 build (chain-link array scale, bolt-hole pattern complexity, bevel-bore subtraction topology)

### 3. Phase 2 — Gaps + gear-support build
**Gaps closed:**
- BB shell modeled (BSA 68mm × 40mm OD × 34mm ID, `parts/bb_shell.FCStd`)
- Bevel gears upgraded to **real involute teeth** via `freecad.gears` workbench (16T, module 3, 45° pitch angle, 20° pressure angle, 8mm face); 12mm axial bore through gear so the shaft passes through
- Crank arms (170 mm) at both ends of the BB shaft, 180° opposed
- Pedals (90×60 platforms) at the crank tips, spindle axes outboard ±X
- Donor-stock shaft App::Links replaced with **parametric** Part::Cylinder spans:
  - Jackshaft OD12, L240, X=70..310
  - BevelOutputShaft OD12, L141, Z=464..605
  - VerticalDriveShaft OD8, L257, Z=560..817
- Chain racetrack-ring solids replaced with **real chain-link arrays**: 63 links on stage-1, 52 on stage-2 (walked along pitch-circle racetracks at 12.7mm pitch)

**Gear support subassembly:**
- `parts/pillow_block.FCStd` — parametric bearing housing with 4× M5 bolt-hole pattern, 35mm bearing seat (6202-2RS), 12mm shaft bore. App::Linked 7× (jackshaft L+R, bevel-out Bot+Top, grinder Bot+Top, idler Top)
- `parts/bevel_mount_bracket.FCStd` — L-bracket, 200mm vertical leg + 80mm horizontal flange, M5 bolt-hole pattern

### 4. Phase 3 — Audit + orientation fixes
Headless audit walked all 156 objects, surfaced 4 critical bugs:

| Bug | Source | Fix |
|---|---|---|
| `add_cyl_x` rotation `-90` → produced local +Z → world **-X** (not +X) | Helper used `App.Rotation(Vector(0,1,0), -90)` | Changed to `+90`. Confirmed via `add_link_axis_x` precedent. Same bug fixed in `add_pillow_block_x`, `BBShell_Link`, `BevelGear_Input` |
| Right pedal basis was left-handed (det = -1) | `z_dir = (0,0,1)` paired with x,y producing `cross = (0,0,-1)` | Changed `z_dir = (0,0,-1)` for right-handed system |
| Crank arms mounted at X=±44 (against shell faces), not X=±70 (axle ends) | Misplaced offset | Set to ±70 |
| Pedal-spindle 30mm offset = visual disconnect | `PEDAL_SPINDLE_REACH = 30` | Set to 0 |

Phase 2+3 squashed into combined commit `5418158` after the original push hit GitHub's 100MB limit (`session10_assembly_render.stl` was 132MB). Added gitignore entry for it; regenerable from `_session10_export_assembly_stl.py`.

### 5. ViewObject-visibility fix
- Discovered that headless `freecadcmd.exe` saves data-side Visibility=True but doesn't write GuiDocument state — objects open hidden in the GUI viewport
- Solution: updated `show_everything.FCMacro` to call `o.ViewObject.Visibility = True` AND `doc.save()`, which bakes the view state into the .FCStd file. After one manual run, future opens auto-show
- Installed `Mod/GrinderAutoShow/InitGui.py` document-observer mod — but didn't fire on this FreeCAD instance; deferred for later debugging

## Final state of the assembly

156 objects. Drivetrain ratio 10.096. All hard constraints (18" max glass edge, 170mm max print) respected. Macro chain (01 → 11) idempotent; rebuild from scratch via:
```
run_macro_10_headless.py   # build parts/bevel_gear.FCStd (real involute teeth)
run_macro_11_headless.py   # build the six Session-10 parts
run_macro_08_headless.py   # build the assembly
```
Then in the GUI: `Macro → show_everything → Execute` once to bake visibility.

## Parts inventory after Session 10

17 part files in `parts/`:
`bb_shell`, `bevel_gear`, `bevel_mount_bracket`, `chain_link`, `chainring`, `crank_arm`, `crank_bb_shaft`, `drive_pulley`, `grinder_shaft`, `idler_pulley`, `idler_shaft`, `intermediate_shaft`, `pedal`, `pillow_block`, `stage1_cog`, `stage2_large`, `stage2_pinion`

## What's still out of scope (deferred)

- Animation / rotation rigging (Blender, separate session)
- Belt tensioner mechanism
- Real rigid platen behind the belt
- Set-screws + keyways
- Real involute teeth on chainring / stage1_cog / stage2_large / stage2_pinion (currently pitch-diameter disks)
- Pulley crown depth verification on drive pulley
- Drivetrain support beam (Y=400 cross-member tying jackshaft pillow blocks)
- Promotion of assembly-level constants to VarSets
- Bracket-arm geometry tying pillow blocks to actual frame members

## Commits this session

| Hash | Title |
|---|---|
| `98a7d94` | Session 10 — real involute bevel pair + cast frustum BB-block + truss |
| `ef6aa06` | Session 10 Phase 1 — review pass: gaps + inconsistencies inventory |
| `5418158` | Session 10 Phases 2+3 — close geometric gaps, add gear-support subassembly, fix orientation bugs |

All pushed to `origin/tooling/bike-powered-grinder`.

## Key learnings (carried to auto-memory)

1. **FreeCAD headless saves data-side Visibility but not GUI ViewObject state.** Headless builds open hidden in the GUI. Fix: run `show_everything.FCMacro` (sets `o.ViewObject.Visibility=True` + `doc.save()`) once after each headless rebuild.
2. **App.Rotation(axis, angle) sign confusion.** `App.Rotation(Vector(0,1,0), +90)` maps local +Z → world +X. The -90° variant goes the OTHER way. When in doubt, copy from a known-working helper (`add_link_axis_x` was the canonical reference).
3. **`make_rotation_from_basis` requires right-handed basis** (det = +1). Always sanity-check with `cross(x_dir, y_dir) == z_dir`. Left-handed basis silently produces wrong rotation in FreeCAD.
4. **`freecad.gears` workbench is headless-importable** via `sys.path` insert + `freecad.__path__.append`. The repo at `github.com/looooo/freecad.gears` cloned into `~/AppData/Roaming/FreeCAD/Mod/` works for parametric involute gear generation.
5. **GitHub's 100MB file limit bites whole-assembly STL exports.** A 156-object assembly with chain-link arrays serializes to 132MB. Always gitignore whole-assembly STL renders.
6. **Audit-by-bbox after every build.** A headless script that prints each object's position + bbox + rotation as JSON caught all four orientation bugs in Phase 3. Cheap, fast, surfaces problems no visual inspection would catch quickly.
7. **Voice-mode autonomy contract.** Isaiah's pattern: "do this all without stopping" + "ask questions FIRST" + "bias toward stopping when truly stuck" = three-phase autonomy. All clarification UP FRONT, then long autonomous run, then stop only on genuine ambiguity.

## Suggested first actions in the next session

1. `git checkout tooling/bike-powered-grinder`, `git fetch`, `git log --oneline -3` to confirm HEAD = `5418158`
2. Open `Grinder_Assembly.FCStd` in FreeCAD GUI to inspect Phase 2+3 work visually
3. Pick from the deferred items above based on what Isaiah wants next
