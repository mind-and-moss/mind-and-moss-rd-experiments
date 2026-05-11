# Bike-Powered Glass Grinder — FreeCAD 1.1 Files

> **For session pickup, load [`CONTEXT.md`](CONTEXT.md) first.** It's the
> dense, self-contained handoff for sessions focused on this FreeCAD
> pipeline — supersedes `SESSION-HANDOFF.md` and `CLAUDE.md` for
> FreeCAD work.

This folder holds the FreeCAD parametric model and supporting macros for the
bike-powered glass grinder. Pattern: one master parameter file holds every
locked design value, every part file external-references it.

## Folder layout

```
freecad/
├── README.md                                          (this file)
├── .gitignore                                         (excludes FCStd backup + report files)
├── Grinder_Params.FCStd                               (master parameter file — current state)
├── Grinder_Assembly.FCStd                             (top-level assembly — coming later)
├── macros/
│   ├── 01_create_grinder_params.py                    (creates the doc + 7 VarSets + empty MasterSketch)
│   ├── 02_scaffold_drivetrain_geometry.py             (adds 10 construction elements with hardcoded values)
│   ├── 03_bind_geometry_to_varsets.py                 (wipes + rebuilds with 21 constraints + 9 expr bindings)
│   ├── 04_constrain_shafts_and_chain_distances.py    (supersedes 03 — adds 4 shaft locks + 2 computed CD props)
│   ├── run_macro_NN_headless.py                       (one wrapper per user-facing macro, drives freecadcmd.exe)
│   └── verify_parametric_binding.py                   (diagnostic — proves expression chain is live)
└── parts/                                             (one .FCStd per printable part — coming later)
```

**Macro lineage:** each macro N supersedes macro N-1 for the same domain (sketch geometry).
Re-running an older macro after a newer one will undo the newer macro's additions. Always run
the highest-numbered macro that exists for the domain you're touching.

## Prerequisites

- **FreeCAD 1.1.1** installed (the installer is at `~/Downloads/FreeCAD_1.1.1-Windows-x86_64-py311-installer.exe`)
- This repo cloned on the machine running FreeCAD

## How to run macros

Two paths: **headless** (Claude Code's default — no GUI needed) or **GUI** (when
you want to see the result while it builds).

### Headless (preferred for routine iteration)

Each user-facing macro has a `run_macro_NN_headless.py` wrapper. The wrapper
opens `Grinder_Params.FCStd`, runs the macro, saves. Invoke with:

```bash
"C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe" path/to/run_macro_NN_headless.py
```

Output goes to stdout. Exit code 0 = success. Macro 01's wrapper creates the
doc fresh (no pre-existing FCStd to open); macros 02+ open and mutate.

### GUI (for visual inspection)

1. Open FreeCAD 1.1.1.
2. Menu: **Macro → Macros...**
3. Set macro location to `<repo>/tooling/bike-powered-grinder/freecad/macros/`
4. Select the macro file, click **Execute**.
5. Save (File → Save) when done.

If a macro errors, check the **Report View** panel (View → Panels → Report View)
for which step failed.

### Verifying the parametric chain is live

`verify_parametric_binding.py` is a diagnostic that mutates a VarSet property,
checks the geometry recomputed, then reverts (does NOT save). Run via:

```bash
"C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe" path/to/verify_parametric_binding.py
```

Exit 0 = bindings are live. Exit 1 = the expression chain is broken; check the
`verify_parametric_binding.report.txt` side-channel report file for details.

## What macro 01 creates

A FreeCAD document containing:

### Six VarSets (parameter groups)

| VarSet | Properties | Purpose |
|---|---|---|
| `Drivetrain` | cadence, target RPM, total ratio, sprocket teeth, chain pitch | the speed-and-power math |
| `Pulleys` | drive/idler diameters, crown depth, face width | the belt-driving wheels |
| `Belt` | width, length, derived center distance | belt geometry |
| `Platen` | length, width, thickness, **max_glass_edge** (hard constraint) | the flat reference surface |
| `Frame` | max printable dimension (Bambu A1 Mini), module target length, door clearance | structural envelope |
| `Fits` | loose / running / press tolerances | print-fit calibration |
| `Bearings` | shaft and bearing dimensions | the rotating bits |

### One empty MasterSketch (on the XY plane)

You draw the 2D drivetrain layout into this sketch interactively — pulley
centers, platen position, frame footprint. Reference VarSet values via
expressions like `<<Grinder_Params#Pulleys>>.drive_pulley_dia`.

## Current MasterSketch state (after macro 04)

```
geometry: 10 elements (3 pulley circles + 4 platen lines + 3 sprocket circles)
constraints: 25 (21 from macro 03 + 4 shaft locks from macro 04)
expression bindings: 13 (9 sketch constraint bindings + 2 VarSet computed properties + 2 nested via shaft positions)
```

All locked-down, fully parametric. Edit any of these VarSet properties in the
GUI's properties panel and the geometry reflows on next recompute (F5):

| VarSet.property | Current value | Drives |
|---|---|---|
| `Pulleys.drive_pulley_dia` | 152.4 mm | drive pulley circle radius |
| `Pulleys.idler_pulley_dia` | 76.2 mm | idler circle radius |
| `Belt.belt_path_center_distance` | 734.9 mm | idler X position |
| `Platen.platen_length` | 558.8 mm | platen rectangle length |
| `Platen.platen_width` | 60.0 mm | platen rectangle width |
| `Drivetrain.stage1_chainring_teeth` | 42 | chainring circle radius (chain-pitch formula) |
| `Drivetrain.stage1_cog_teeth` | 13 | cog circle radius |
| `Drivetrain.stage2_large_teeth` | 25 | large sprocket circle radius |
| `Drivetrain.stage2_pinion_teeth` | 8 | pinion circle radius |
| `Drivetrain.intermediate_shaft_x/y` | 0, 500 mm | cog/large center position |
| `Drivetrain.crank_bb_x/y` | 0, 1100 mm | chainring center position |

Two computed properties auto-update:

| VarSet.property | Expression | Current value |
|---|---|---|
| `Drivetrain.stage1_chain_center_distance` | √((crank − intermediate)²) | 600.0 mm |
| `Drivetrain.stage2_chain_center_distance` | √(intermediate²)            | 500.0 mm |

## What's next

- **Macro 05:** assembly-level part split. Start producing individual part
  `.FCStd` files App-Linked to `Grinder_Params.FCStd` for parameters. Drive
  pulley first (simplest 3D extrusion + hub geometry). Generate STL.
- **Test print + load test** of the drive pulley with embedded stainless rod hub.

## Manual fallback (if macro 01 fails)

If the macro errors persistently, you can create the master file manually:

1. **File → New**
2. **Workbench → Default**
3. For each parameter group above, **Object → Variable Set** (or right-click in
   the model tree → **Add VarSet**). Name it (e.g., `Drivetrain`).
4. Right-click the VarSet → **Add property** → pick type and name. Repeat
   for each parameter listed in the macro's `PARAMETER_GROUPS` data.
5. Add a sketch on the XY plane: **Sketch → Sketcher → New Sketch on XY plane**.
6. Save to the path above.

This is tedious but reliable. The macro is just an automation of these steps.

## File-format note

FreeCAD 1.1's `.FCStd` files are NOT backward-compatible with FreeCAD 1.0
because of datum-orientation changes. Don't open this file in 1.0 — pin
everyone on 1.1.x.

## Sources

- Locked spec: [`../README.md`](../README.md)
- Stress analysis: [`../research/sprocket-stress-corrected.md`](../research/sprocket-stress-corrected.md)
- FreeCAD 1.1 readiness: [`../research/freecad-1.1-readiness.md`](../research/freecad-1.1-readiness.md)
