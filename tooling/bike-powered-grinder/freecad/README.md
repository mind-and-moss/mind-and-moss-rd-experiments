# Bike-Powered Glass Grinder — FreeCAD 1.1 Files

This folder holds the FreeCAD parametric model and supporting macros for the
bike-powered glass grinder. Pattern: one master parameter file holds every
locked design value, every part file external-references it.

## Folder layout

```
freecad/
├── README.md                         (this file)
├── .gitignore                        (excludes FreeCAD backup files)
├── Grinder_Params.FCStd              (master parameter file — created by macro 01)
├── Grinder_Assembly.FCStd            (top-level assembly — coming later)
├── macros/
│   ├── 01_create_grinder_params.py   (creates Grinder_Params.FCStd from scratch)
│   └── (future macros)
└── parts/                            (one .FCStd per printable part — coming later)
```

## Prerequisites

- **FreeCAD 1.1.1** installed (the installer is at `~/Downloads/FreeCAD_1.1.1-Windows-x86_64-py311-installer.exe`)
- This repo cloned on the machine running FreeCAD

## How to run macro 01 (`01_create_grinder_params.py`)

This macro creates the master parameter file. **Run it once.** After that,
the resulting `.FCStd` file is the source of truth for all design parameters.

1. Open FreeCAD 1.1.1.
2. Menu: **Macro → Macros...**
3. In the dialog:
   - Click the folder icon at the top right to set the macro location, OR
   - Click **Add** to add this folder to the search path:
     `<repo>/tooling/bike-powered-grinder/freecad/macros/`
4. Select **`01_create_grinder_params.py`**.
5. Click **Execute**.
6. The macro will create a new document with 6 VarSets and an empty MasterSketch.
7. **File → Save As...** → save to:
   `<repo>/tooling/bike-powered-grinder/freecad/Grinder_Params.FCStd`

If the macro errors, check the **Report View** panel (View → Panels → Report View)
for which step failed. Most failures recover by running the macro again on a
fresh blank document (File → New).

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

## What to do after running macro 01

Sketcher workbench, double-click MasterSketch, draw:

1. **Drive pulley center** at origin (0, 0). Add a construction circle of
   diameter `Pulleys.drive_pulley_dia` (152.4 mm) for visual reference.
2. **Idler pulley center** at (-`Belt.belt_path_center_distance`, 0).
   Construction circle of diameter `Pulleys.idler_pulley_dia` (76.2 mm).
3. **Platen rectangle** between the two pulleys, length
   `Platen.platen_length` (558.8 mm), centered on the line between pulley
   centers.
4. **Stage 2 sprocket centers** — large sprocket on the intermediate shaft,
   small pinion on the drive pulley shaft. Position them with chain
   center-distance using sprocket pitch diameters.
5. **Stage 1 sprocket centers** — chainring on the crank, cog on the
   intermediate shaft.
6. **Frame outline** — three modules, joints between them.

When you're ready for the next macro (which scaffolds this geometry
programmatically), tell Claude Code.

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
