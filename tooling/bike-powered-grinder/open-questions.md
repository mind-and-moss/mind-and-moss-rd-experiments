# Bike-Powered Glass Grinder — Open Questions

The punch list of what Isaiah needs to decide (or what Claude Code needs to research) before FreeCAD 1.1 modeling can lock geometry.

Updated 2026-05-08 after the Q1–Q4 readiness lock-in session and the corrected sprocket stress analysis.

---

## For Isaiah to answer (one at a time, voice-friendly)

### Critical — blocks FreeCAD work

1. **None currently blocking the master sketch.** The Q1–Q4 lock-in session resolved the four critical gating questions and the corrected stress analysis confirmed the drivetrain spec. The remaining items below are detail-design questions that surface as the FreeCAD model gets built out.

### Important — drives detail design

2. **Coolant routing.**
   - Tray material: stainless pan, or printed manifold draining to bucket?
   - Recirculating pump or one-way drain to bucket?
   - Slurry disposal: how does the spent grit + glass dust go away?

3. **Belt tracking adjustment range.**
   How much side-to-side trim does Isaiah want? ±0.5" is typical for 2x72 grinders but is this enough for a horizontal-layout, glass-finishing-only build?

4. **Module joint mechanism.**
   Wing-nut bolts vs quarter-turn cam locks vs over-center latches. Tradeoff: wing-nuts cheap and known, cam locks fastest, latches cleanest aesthetic but most engineered. Isaiah's call.

5. **Module dimensions within portability constraints.**
   Each module ~24–36" long, fits through 30" door, liftable by one person. Need a target weight per module (15 lb? 30 lb?) — drives metal-tube wall thickness and how much load each printed node can carry.

6. **Workshop reality check (continued).**
   Per `findings/SESSION-HANDOFF.md` Isaiah doesn't have a dedicated workshop yet. Where will the grinder live during prototyping? Where during real use? Affects splash-tolerance, dust-tolerance, storage design.

7. **Source for the 8T machined pinion.**
   Options: SDP-SI, Boston Gear, McMaster-Carr, or local machine shop. ~$15 is the spec. Steel or 6061 aluminum both fine at 1.91 N·m sustained / 3.2 N·m peak. Bore size needs to match the 8 mm grinder shaft.

### Nice-to-lock-early

8. **Material color / aesthetic palette.**
   PETG comes in many colors. The grinder will be photographed eventually. "Warm 3D-print color + brushed stainless + black silicone" is the working hypothesis but not locked.

9. **Belt change time target.**
   Quick-release belt tensioner is probably essential. How fast does belt-swap need to be? 30 seconds? 2 minutes? Affects tensioner mechanism complexity.

---

## For Claude Code to research / resolve before geometry locks

### Phase 1 research (web pass before any FreeCAD work)

1. **Sackorange 2x72 SiC belt — confirmed dimensions.**
   Exact belt width (2.000" nominal — confirm tolerance), belt thickness, joint type (skived/butt/scarf — affects how it tracks over crowned pulleys).

2. **Crown depth standards for 2x72 horizontal-layout grinders.**
   Reference: Beaumont KMG, Reeder, Esteem. Actual crown depth they use, variation between drive and idler. 0.020" or 0.040"? Source-cited, not guesswork.

3. **Bicycle freewheel torque ratings.**
   Standard freewheel hubs vs threaded freewheels. Max torque at the cog before slip or damage. Translate Isaiah's pedal force × 10:1 into the torque the freewheel actually sees.

4. **Stainless rod embedment in PETG — best practices.**
   How to embed stainless rod spokes during print (pause-and-insert via Bambu's M600 / pause logic), or post-print via heated press-fit, or epoxy-bond. Pull-out resistance data.

5. **Platen face material for wet glass grinding.**
   Steel, ceramic-faced, or glass-faced (literal ceramic-glass platen liner, common in knife-making)? What survives wet glass-grinding without rusting or scoring? Stainless 304 inventory baseline — does it work as a platen face, or need a hardened/ceramic facing?

6. **RPM sensor wiring + wet environment compatibility.**
   Cheap Amazon RPM sensors are typically unsealed. With water dripping, do we need a sealed sensor, an off-axis optical sensor, or a remote magnet-and-reed-switch?

7. **Glass dust extraction at low CFM.**
   Wet grinding reduces aerosolization but doesn't eliminate it. What's the minimum dust extraction (or HEPA-filtered respirator spec) for occasional-use safety?

### Phase 2 — design questions (during FreeCAD modeling)

8. **Bearing block geometry — printable cone or pocket?**
   3D-printed bearing blocks need to hold a stainless bearing race rigidly without cracking the print under load. Heat-set inserts vs press-fit pocket vs embedded stainless cup?

9. **Tensioner pivot axis — fixed pin or sliding rail?**
    The screw-driven tensioner moves the idler arm. Does the arm rotate around a fixed pin (simpler) or slide along rails (more linear motion)?

10. **Sled rail material and tolerance.**
    Stainless rod + linear bearings? Printed channels? V-groove on stainless angle? Dimensional tolerance for repeatable glass positioning.

11. **Quick-release belt tensioner mechanism.**
    The screw-driven tensioner is normal-use. For belt swaps, is there a separate cam lever that retracts the idler quickly without losing the screw-set position?

12. **Module joint geometry — repeatable alignment.**
    The whole machine breaks down for portability. When it reassembles, the platen flatness reference must repeat to within… how much? Drives joint tolerance (locating dowels vs slip fits vs precision pin-bushing).

---

## Resolved (recorded so they don't reopen)

### From the Phase 0 review (2026-05-07)

- **2x82 belts:** rejected, supply chain weak for SiC at glass-grade fine grits.
- **2x48 belts:** rejected, 24"/22" platen requirement and 2x72 supports it cleanly.
- **Dual-zone platen + slack belt for curves:** rejected, single-purpose glass-only.
- **Springs in tensioner:** rejected, screw-driven only.
- **Tension gauge for tuning:** rejected, by-feel with documented reference deflection.
- **Vertical layout:** rejected, horizontal locked.
- **Standing rider:** rejected, seated locked.
- **CNC-first:** rejected, 3D-print + stainless reinforcement first; CNC last resort.
- **Aluminum oxide / zirconia belts:** rejected, silicon carbide only for glass.
- **Electric motor backup:** rejected, pedal-only for v1.
- **Larger-than-needed bolts everywhere:** rejected, right-size per joint.

### From the Q1–Q4 lock-in session (2026-05-08)

- **Math conflict (75 × 8 ≠ 750):** resolved. Belt RPM target = 750 wins. Cadence stays 75. Reduction = 10:1 locked.
- **Single-stage chain drivetrain:** rejected. Stock bike parts max at ~4.8:1 in one stage; can't reach 10:1 without oversized custom chainrings or internal hubs. Two stages locked.
- **Internal-geared hub (Rohloff/Sturmey-Archer):** rejected. Rohloff $1500+, Sturmey-Archer 8-speed maxes at ~6.6:1 even with 4:1 chain ratio. Hides engineering inside opaque component, anti-brand-story. Two visible chain stages preferred.
- **Original 5"/2" pulleys + 24" platen:** revised. Bumped to 6"/3" pulleys + 22" platen for better belt tracking, crown room, and bearing seat. Sacrificed 2" of platen.
- **Open-ended platen length sized to longest panel:** flipped. Define envelope first, constrain panel designs to fit. **18" max glass edge** is now a hard project-wide design constraint (`findings/design-constraints.md`).
- **Single-piece welded frame:** rejected. Portable 3-module architecture with hand-cut metal tube + 3D-printed PETG joint nodes locked.
- **All-PETG drivetrain (gears) at 7.5:1:** considered (would have given mid-spec 890 SFM, all parts printable, ~$15 cheaper). **Rejected** — Isaiah locked Option A (10:1, upper-spec 1180 SFM, machined 8T metal pinion at stage 2) to honor the 600–750 RPM range from the client chat as a hard constraint.
- **Earlier "10:1 fails on PETG fatigue" gut call:** reversed. The original analysis used wrong torque direction (treated speed-up as reduction). With corrected torque chain (pedal 19.1 N·m → belt 1.91 N·m), the math closes; only the smallest sprocket (8T grinder pinion) needs to be metal.

### Drivetrain spec (locked)

- **Total ratio:** 10:1 nominal (10.2:1 exact)
- **Stage 1:** 42T donor chainring × 13T donor cog = 3.23:1 (steel, hugely overbuilt)
- **Stage 2:** 32T sprocket (PETG, m=1.5, b=12 mm) × 8T pinion (machined steel/Al, m=2.0, b=16 mm) = 4:1
- **Intermediate shaft:** 12 mm 304 stainless rod, 2× SKF 6202-2RS bearings
- **Grinder pulley shaft:** 8 mm 304 stainless rod, 2× NSK 608-2RS bearings
- **Chains:** 2× KMC Z8.3 (1/2" × 3/32") bicycle, breaking strength ≥7,800 N
- **Pulleys:** 6" drive (target 750 RPM → 1180 SFM at belt), 3" idler, both crowned 0.020–0.040", 3D-printed PETG with embedded stainless rod hub
- **Total bought-parts cost beyond donor bike:** ~$73
