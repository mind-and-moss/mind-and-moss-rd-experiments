# Bike-Powered Glass Grinder — Open Questions

The punch list of what Isaiah needs to decide (or what Claude Code needs to research) before FreeCAD 1.1 modeling can lock geometry.

Questions are grouped by who needs to answer them and tagged with priority for the FreeCAD pass.

---

## For Isaiah to answer (one at a time, voice-friendly)

### Critical — blocks FreeCAD work

1. **Longest single glass edge in any Machine gem-component panel?**
   24" platen gives ~20–21" usable. If any panel exceeds 20" on its longest edge, the platen needs to grow (and frame, and belt — possibly forcing 2x82 custom belts). Drives the whole frame footprint. Need this answer first.

2. **Gear reduction split across the two stages.**
   8:1 total is locked. How to split it?
   - Option A: cassette ratio ~3:1 × chain-to-pulley ratio ~2.7:1
   - Option B: cassette ratio ~4:1 × chain-to-pulley ratio ~2:1
   - Option C: even split, ~2.83:1 × 2.83:1
   Affects sprocket sizes, intermediate gear printability, and chain length.

3. **Freewheel placement.**
   Diagram shows freewheel right after the crank. Is that Isaiah's intent, or is the freewheel inline between the cassette and the final pulley? Different routing = different bearing block geometry.

4. **Frame footprint (length × width × height).**
   Drives whether it fits Isaiah's workspace, how high the platen sits relative to the seated pedaling position, and whether the whole machine is storable. Need approximate target dimensions.

### Important — drives detail design

5. **Coolant routing.**
   - Tray material: stainless pan, or printed manifold draining to bucket?
   - Recirculating pump or one-way drain to bucket?
   - Slurry disposal: how does the spent grit + glass dust go away?

6. **Belt tracking adjustment range.**
   How much side-to-side trim does Isaiah want? ±0.5" is typical for 2x72 grinders but is this enough for a horizontal-layout, glass-finishing-only build?

7. **Axle / shaft diameter for drive pulley and idler.**
   3/8" stainless rod is the standard knife-grinder default and matches Isaiah's inventory baseline. Confirm or override.

8. **Workshop reality check.**
   Per `findings/SESSION-HANDOFF.md` Isaiah doesn't have a dedicated workshop yet. Where will this grinder live during prototyping? Where during real use? Affects splash-tolerance, dust-tolerance, and storage design choices.

### Nice-to-lock-early

9. **Material color / aesthetic palette.**
   PETG comes in many colors. The grinder will be photographed eventually. "Warm 3D-print color + brushed stainless + black silicone" is the working hypothesis but not locked.

10. **Belt change time target.**
    Quick-release belt tensioner is probably essential — but how fast does belt-swap need to be? 30 seconds? 2 minutes? Affects tensioner mechanism complexity.

---

## For Claude Code to research / resolve before geometry locks

### Phase 1 research (web pass before any FreeCAD work)

1. **Sackorange 2x72 SiC belt — confirmed dimensions.**
   - Exact belt width (2.000" nominal — confirm tolerance)
   - Belt thickness
   - Joint type (skived, butt, or scarf — affects how it tracks over crowned pulleys)

2. **Crown depth standards for 2x72 horizontal-layout grinders.**
   Reference: Beaumont KMG, Reeder, Esteem, and other commercial 2x72 builds. What's the actual crown depth they use, and does it vary between drive and idler? 0.020" or 0.040"? Needs source-citation, not guesswork.

3. **PETG gear tooth stress data.**
   Published numbers for tooth shear under continuous torque, ideally with infill % and orientation. Want safe load-per-tooth at module 1, 1.5, 2 for an 8:1 drivetrain × marathon-runner pedal torque.

4. **Bicycle freewheel torque ratings.**
   Standard freewheel hubs vs threaded freewheels. Max torque at the cog before slip or damage. Translate Isaiah's pedal force × 8:1 into the torque the freewheel actually sees.

5. **Stainless rod embedment in PETG — best practices.**
   How to embed stainless rod spokes during print (pause-and-insert via Bambu's M600 / pause logic), or post-print via heated press-fit, or epoxy-bond. Pull-out resistance data.

6. **Platen face material for wet glass grinding.**
   Steel, ceramic-faced, or glass-faced (literal ceramic-glass platen liner, common in knife-making). What survives wet glass-grinding without rusting or scoring? Stainless 304 is the inventory baseline — does it work as a platen face, or need a hardened/ceramic facing on top?

7. **RPM sensor wiring + wet environment compatibility.**
   The cheap Amazon RPM sensors are typically unsealed. With water dripping, do we need a sealed sensor, an off-axis optical sensor, or a remote magnet-and-reed-switch?

8. **Glass dust extraction at low CFM.**
   Even wet, some aerosolization happens during dry edge inspection between grits. What's the minimum dust extraction (or HEPA-filtered respirator spec) for occasional-use safety?

### Phase 2 — design questions (during FreeCAD modeling)

9. **Bearing block geometry — printable cone or pocket?**
   3D-printed bearing blocks need to hold a stainless bearing race rigidly without cracking the print under load. Heat-set inserts vs press-fit pocket vs embedded stainless cup?

10. **Tensioner pivot axis — fixed pin or sliding rail?**
    The screw-driven tensioner moves the idler arm. Does the arm rotate around a fixed pin (simpler), or slide along rails (more linear motion)?

11. **Sled rail material and tolerance.**
    Stainless rod + linear bearings? Printed channels? V-groove on stainless angle? Dimensional tolerance for repeatable glass positioning.

12. **Quick-release belt tensioner mechanism.**
    The screw-driven tensioner is normal-use. For belt swaps, is there a separate cam lever that retracts the idler quickly without losing the screw-set position? Or do we just back off the screw?

---

## Resolved (recorded here so they don't reopen)

- **2x82 belts:** rejected, supply chain weak for SiC at glass-grade fine grits.
- **2x48 belts:** rejected, 24" platen is the requirement and 2x72 supports it cleanly.
- **Dual-zone platen + slack belt for curves:** rejected, single-purpose glass-only.
- **Springs in tensioner:** rejected, screw-driven only.
- **Tension gauge for tuning:** rejected, by-feel with documented reference deflection.
- **Vertical layout:** rejected, horizontal locked.
- **Standing rider:** rejected, seated locked.
- **CNC-first:** rejected, 3D-print + stainless reinforcement first; CNC last resort.
- **Aluminum oxide / zirconia belts:** rejected, silicon carbide only for glass.
- **Electric motor backup:** rejected, pedal-only for v1.
- **Larger-than-needed bolts everywhere:** rejected, right-size per joint.
