# Session 10 — Phase 1 Review Pass

Comprehensive review of the bike-powered grinder FreeCAD assembly as of commit `98a7d94`, prior to the Phase-2 gaps + gear-support build.

## A. Literal gaps in geometry

These are visible holes/disconnections where geometry should join but doesn't.

| # | Gap | Where | Severity | Fix path |
|---|---|---|---|---|
| 1 | BB shell not modeled | Around `CrankBB_ShaftLink` at (0, 250, 290) — `BB_SplitCollar` clamps empty air | High | New `parts/bb_shell.FCStd`: 68 mm wide × 40 mm OD × 34 mm ID hollow cylinder, axis X, App::Link in macro 08 |
| 2 | Bevel gears have no bore | `BevelGear_Input` and `BevelGear_Output` are solid cones — shaft cannot pass through | High | Update macro 10 to subtract a 12 mm bore from the gear shape before baking |
| 3 | Jackshaft too short for new bevel layout | `Jackshaft_Link` at X=75..225, bevel input gear sits at X=275..300 — 50 mm air gap between them | Med | Replace donor 150 mm `intermediate_shaft` App::Link with a parametric cylinder built in-macro, spanning chain plane through the bevel input back face (X ≈ 75 to 300 = 225 mm) |
| 4 | Grinder shaft too short for new bevel + chain2 + pulley span | `VerticalDriveShaft_Link` at Z=580..730, drive pulley at Z=732..792 — gap above shaft, pulley unsupported | Med | Replace donor with parametric cylinder spanning stage2_pinion through drive pulley (Z ≈ 560 to 800) |
| 5 | Bevel-output shaft only reaches up from gear, not down past it | `BevelOutputShaft_Link` at Z=474..624. Stage2_large at Z=580 fits, but no support for the BACK side of the bevel-output gear (Z=474) | Low | Extend shaft down ~30 mm below gear back face for bearing seat |
| 6 | No crank arms | Chainring is freestanding on BB shaft — no levers for the rider to push | High | New `parts/crank_arm.FCStd`: 170 mm long arm, square-taper bore at BB end, M9 pedal-thread boss at pedal end. App::Link twice (left + right) at X=±70 |
| 7 | No pedals | Nowhere to put feet | High | New `parts/pedal.FCStd`: 90×60 mm platform with center spindle. App::Link twice at end of each crank arm |
| 8 | No bearings anywhere | All shafts float; sprockets/pulleys have no rolling support | High | New `parts/pillow_block.FCStd`: parametric bearing housing with bolt-hole pattern. App::Link 2× per shaft (top & bottom of span) |
| 9 | Bevel-output shaft not tied to frame | Floats at (X=300, Y=400) with no path to desk | High | Combine with #8 — pillow blocks for the bevel-output shaft must be on a bracket arm reaching the desk frame |
| 10 | Jackshaft not tied to frame | Same problem | High | Pillow-block bracket arms reaching desk legs |
| 11 | Chain loops are solid racetrack rings | Visualization placeholders, not real chain | Med | Replace with arrays of `parts/chain_link.FCStd` along the chain path |
| 12 | Drive pulley/grinder shaft alignment | Drive pulley body sits Z=732..792, shaft ends at Z=730 | Cosmetic | Fixed by #4 |

## B. Inconsistencies / stale references

| # | Issue | Where | Severity |
|---|---|---|---|
| 13 | Final-report banner says "Session 9 complete" | macro 08 line ~694 | Cosmetic |
| 14 | Report still references "RA-drive (placeholder housing center)" — that object was removed in Session 10 | macro 08 final report block | Cosmetic |
| 15 | DeskPlate/leg/rail dimensions hardcoded as assembly-level constants | macro 08 (DESK_THICKNESS, DESK_WIDTH_X, LEG_DIA, etc.) | Low — works but isn't VarSet-promoted |
| 16 | Bevel-gear params duplicated between macro 08 and macro 10 (must stay in sync manually) | macros 08 and 10 | Low — could be moved to a VarSet |

## C. Missing structural / functional elements

| # | Missing element | Effect |
|---|---|---|
| 17 | No belt tensioner | Belt slack adjustment requires moving the idler shaft mount — needs a slot or pivot |
| 18 | No platen behind belt | The belt has no rigid backing for the glass to push against — pulleys alone can't take grinding force |
| 19 | Pulley crown depth | Drive pulley built by macro 05 may not have crown (locked spec 0.75 mm rise). Idler does. Re-verify |
| 20 | No floor for the rider | RiderSeatRef is a sphere at world origin; nothing connects it to the floor block / desk system (chair is implicit) |
| 21 | No fasteners modeled anywhere | Bolts, screws, set-screws — entirely absent. Will add as part of pillow-block bolt-hole patterns |

## D. Hard constraints still respected

- ✅ 18" max glass edge (`Platen.max_glass_edge = 457.2 mm`) — unchanged in this work
- ✅ 170 mm max printable dim — block (240×400×200) exceeds, but it's CAST not printed, so OK
- ✅ Drivetrain ratio = 10.096 ≈ 10:1 target
- ✅ Belt centerline at desk's far edge (Y=610) — unchanged

## E. Build plan for Phase 2

Execution order chosen to honor dependency edges:

1. **Bevel-gear bore** — update macro 10, re-run, save `parts/bevel_gear.FCStd` with 12 mm axial bore
2. **New parts** in `parts/`:
   - `bb_shell.FCStd` — 68 × 40 × 34 hollow cylinder
   - `crank_arm.FCStd` — 170 mm crank lever
   - `pedal.FCStd` — flat-pedal platform
   - `pillow_block.FCStd` — parametric bearing housing, bolt-hole pattern
   - `bevel_mount_bracket.FCStd` — L-bracket tying bevel-output pillow blocks to desk
   - `chain_link.FCStd` — single chain link (figure-8 plates + roller)
3. **Macro 08 rewrite of drivetrain section**:
   - Replace donor-stock shaft App::Links with parametric in-macro cylinders (correct span)
   - Add BB shell App::Link
   - Add 2× crank-arm App::Links at BB shaft ends
   - Add 2× pedal App::Links at crank-arm ends
   - Add pillow-block App::Links — 2 per shaft (BB, jackshaft, bevel-out, grinder, idler) = 10 total
   - Add bracket arms tying pillow blocks to desk-frame uprights
   - Add bevel mount bracket connecting bevel-output pillow blocks to back rail
   - Replace `ChainLoop` and `ChainLoop2` with chain-link arrays along the racetrack path
4. **Run macros**, save, export STL
5. **Final review pass** (Phase 3)

## F. Out of scope for this run

Deferred (mentioned for visibility, not built):

- Animation / driver rotation rigging (deferred to a Blender session)
- Belt tensioner mechanism (separate decision)
- Real platen rigid backing (separate decision)
- Set-screws + keyways on shaft/sprocket interfaces
- Actual involute teeth on chainring/cogs (placeholder disks remain)
- Pulley crown depth verification (sprocket pulleys may already be straight cylinders)
- VarSet promotion of assembly-level constants

## G. Risks / things that might go sideways during the build

1. **Real chain links scale**: stage-1 chain perimeter ≈ ~600 mm = ~47 chain links. Stage-2 chain ≈ ~500 mm = ~40 links. Belt loop is just a belt, no replacement needed. ~87 App::Links + recomputes could be slow.
2. **Pillow-block bolt-hole patterns**: bolt holes in pillow block geometry require Sketcher + PartDesign Pocket — slow to build, easy to get wrong on the first try.
3. **Bevel-gear bore**: subtracting a 12 mm bore from the conical body via `shape.cut()` could leave odd topology near the apex. Plan B: cylinder cut, accept slight artifact at apex.
4. **App::Link orientation math**: each new linked part with a complex placement (crank arms, pedals, chain links) is a chance to get rotation wrong. Will sanity-check via assembly bounding boxes.

---

End of Phase 1 review. Phase 2 (gaps + supports build) follows.
