# MONSTER8 — GATE RESULTS

Every number measured by a script in this folder. Nothing eyeballed off a
render. Where a gate does not pass, it says so.

## Object

**420 × 250 × 190 mm**, solid volume **8319 cm³**. Reference shelf product
≈300 mm long → ~2.5× the volume.

> **Flag for review:** 8.3 litres is real displacement in a tank. Printed
> hollow (slicer infill, per the ledger) it is fine structurally, but tank
> volume and water-change maths should be checked before this size is locked.

| Bed | Thickness | Hardness | Plan W × D | Note |
|---|---|---|---|---|
| `A1_platform` | 38.0 | 5 | 420 × 250 | plinth |
| `A2_marl` | 20.9 | **1** | 344 × 174 | **the rotten one — the cave** |
| `A3_cap` | 39.9 | 5 | 364 × 194 | **overhangs A2 → undercut** |
| `A4_bench` | 30.4 | 3 | 310 × 140 | |
| `A5_parting` | 17.1 | 2 | 258 × 88 | |
| `A6_perch` | 43.7 | 4 | 262 × 92 | **overhangs A5** |

Both overhangs are outputs of hardness. Retreat: h5→0, h4→5, h3→11, h2→19,
**h1→38 mm**.

## Chamber

| Measure | Value | Verdict |
|---|---|---|
| ceiling (`A3` underside — a bedding plane) | z 58.9 mm | |
| floor (dished into `A1`) | z 28.0 mm | |
| clear headroom | **30.9 mm** | weakest number in the piece |
| den clear floor | 100 × 84 mm | |
| turn-room (1.5×) | fish to ~56 mm (2.2") | |
| mouth | 54 mm | |
| tail exit | 36 mm | smaller than mouth ✓ |

## Gate results

| Gate | Result | Verdict |
|---|---|---|
| Solid connectivity — `P1_base` | 1 component, 3876 cm³ | **PASS** |
| Solid connectivity — `P2_mid` | 1 component, 3576 cm³ | **PASS** |
| Solid connectivity — `P3_crest` | 1 component, 871 cm³ | **PASS** |
| Solid connectivity — whole object | 1 component, 8319 cm³ | **PASS** |
| Sealed pockets / no dead ends | **0 cells** | **PASS** |
| Mouth → tail flow-through | reachable | **PASS** |
| Narrowest constriction | ~1200 mm² ≈ 39 mm circular equiv. | **PASS** — clearly passable |
| Flat base | z = 0.00, 56 verts on plane | **PASS** |
| Wall ≥ 1.2 mm | 1 of 876 samples at **1.07 mm** | **REVIEW** |

Constriction profile tapers smoothly 2752 → 1200 mm² and reopens to 1600 mm²
at the tail. A monotonic taper with no sudden pinch is what the no-wedge rule
asks for.

## The pillar

`A2_marl` is two components: the main mass and a **64-vert island spanning the
full bed height (38.0 → 58.9 mm)**. Both cave openings are on the front face,
so the rock between them is an island *within that bed*. It is a **pillar** —
captured by `A1` below and `A3` above, and joined into `P1` at print time,
where connectivity tests as one solid. A pillar between two cave mouths is
geologically real and worth keeping.

## Four bugs found by these gates

Recorded because each looked fine and only a measurement caught it.

1. **`A2` charged twice for its inset** — a 34 mm terrace step *plus* its
   38 mm hardness retreat. The den can never exceed the rotten bed's plan
   area, so this starved the chamber of room. A2's retreat **is** its step.
2. **First cutter consumed the whole `A2` bed**, splitting the model into two
   floating halves. Caught by asserting faces-remaining and component count.
3. **Cutter was not a clean solid.** Every lozenge was capped *and* bridged,
   leaving internal faces; EXACT boolean on self-overlapping geometry produced
   **444 cm³ of phantom void inside `A1`**. Only the volumetric pocket test
   found it. Rebuilt as a chain of clean convex solids → 0 sealed cells.
4. **Two validators were themselves wrong.** Vertex adjacency reported stacked
   beds as disconnected, because separately-built beds touch face-to-face
   without sharing vertices. Replaced with voxel solid connectivity.

## Open

1. **Wall thickness 1.07 mm** on `A3_cap` at (77, −78, 59) — the cave ceiling
   edge near the mouth. Below the 1.2 mm gate. Fix by pulling the cutter a
   little clear of `A3`'s rim.
2. **Headroom 30.9 mm** has little margin for a 56 mm fish (~18 mm body
   depth). Deepening the floor dish or thickening `A2` both fix it; both
   change the terrace read.
3. **Segmentation not re-derived at 420 mm.** The piece exceeds the A1 mini's
   180 mm bed so it *must* split. Bedding-plane seams and 0.43 mm pegs are
   specified in `script07_segmentation_and_pegs.py` but for the 190 mm wall,
   not this outcrop.
4. **Manifold check not run** as a formal gate (non-manifold sources were
   removed, but `manifold = 0` has not been asserted).
5. Armature only. Detail, colour and magic are Isaiah's — `SCULPT-BY-NUMBERS.md`.
