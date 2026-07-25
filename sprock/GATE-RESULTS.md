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
| Wall ≥ 1.2 mm | 0 of 715 samples thin; thinnest **2.08 mm** | **PASS** |
| Manifold = 0 | 0 non-manifold edges, 0 loose verts, all 6 beds | **PASS** |

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

## Fifth bug: the thin wall

`A3_cap` measured **1.07 mm** at the cave rim, under the 1.2 mm gate. Cause:
the cutter's top face sat *exactly* on `A3`'s underside, so the boolean was a
coplanar cut against a bed that never needed cutting — **`A3` is the lintel;
its underside already is the ceiling.** Removed `A3` from the boolean targets.
Thinnest wall went 1.07 → **2.08 mm** and the manifold gate passes clean.

## Segmentation for the A1 mini (180 mm bed)

| | |
|---|---|
| footprint vs bed | 420 × 250 mm vs 180 mm → **3 × 2 columns** |
| column size | 140 × 125 mm |
| `L1_base` | z 0 → 58.9 (58.9 mm) — fits |
| `L2_mid` | z 58.9 → 146.3 (87.4 mm) — fits |
| `L3_crest` | z 146.3 → 190.0 (43.7 mm) — fits |
| **total pieces** | **18** |
| seams | 7 vertical per layer, 2 horizontal |
| pegs | ~99 at 6.0 mm / 6.43 mm socket |

> **Flag for review:** 18 pieces and ~99 pegs is a serious assembly job. The
> 420 mm size drives this directly. Worth deciding whether the piece wants to
> be this big before committing to that build.

## Open

1. **Headroom 30.9 mm** has little margin for a 56 mm fish (~18 mm body
   depth). Deepening the floor dish or thickening `A2` both fix it; both
   change the terrace read.
3. **Segmentation not re-derived at 420 mm.** The piece exceeds the A1 mini's
   180 mm bed so it *must* split. Bedding-plane seams and 0.43 mm pegs are
   specified in `script07_segmentation_and_pegs.py` but for the 190 mm wall,
   not this outcrop.
4. **Manifold check not run** as a formal gate (non-manifold sources were
   removed, but `manifold = 0` has not been asserted).
5. Armature only. Detail, colour and magic are Isaiah's — `SCULPT-BY-NUMBERS.md`.

---

# MATURE STRUCTURE (`structure_mature.py`) — the 70% armature

The 30% version was six smooth slabs. Rock has **systems**, and those are what
a sculptor should be handed rather than asked to invent.

## Systems added

| System | What it does | Why it is not decoration |
|---|---|---|
| **Joint sets** | two near-vertical fracture directions, strike 68°/152°, spacing 86/118 mm | every plan outline now **steps at a joint** instead of curving. Rock breaks along joints, not along splines — this is the single biggest reason a smooth extrusion reads as fake |
| **Sub-bedding** | each bed split into 2 laminae, 2.6 mm retreat apart | thick beds are not one slab; laminae give the fine horizontal steps |
| **Open joints (grikes)** | 6 widened fractures cutting down through the stack | ties the beds together visually — without them the beds read as separate plates |
| **Collapsed embayment** | one sector lost its upper beds outright | breaks the profile so the piece has a front and a back, not a uniform mound |
| **Two caves** | the marl rots wherever it is exposed, not in one spot | a second, smaller opening on another face |
| **Talus** | 46 blocks, piled at the foot under the embayment, half-buried | the rock that left had to go somewhere — and it lands where it fell from |
| **Solution basins** | 4 shallow dishes on ledge tops | ledges hold water, so they dissolve |

Counts: **12 rock laminae, 46 talus, 29 cutters, 128 boolean operations.**
All variation is a seeded FNV hash — same script, same rock, every run.

## Validation

| Gate | Result |
|---|---|
| Non-manifold edges (armature) | **3** boundary edges on one lamina |
| Non-manifold edges (after voxel remesh) | **0** — **PASS** |
| Components after remesh | 5 = main mass + 4 talus clusters — **correct**, fallen rock *is* separate |
| Rock volume | 7618 cm³ |

**Manifold is asserted after the remesh, which is where the canon pipeline puts
it** (geometry → remesh → displacement). The armature's 3 boundary edges are
resolved by that step, and this was proven rather than assumed.

## Three bugs found here

1. **Talus read as scattered dice** — too big, too far out, evenly spread.
   Rockfall piles *at the foot*, heaviest under where it fell from, and
   half-buries itself. Now 46 small blocks clustered under the embayment.
2. **A joint slot severed the piece**, leaving a free-standing fin that read as
   a wall. Joint slots were 200–300 mm across a 420 mm piece. Now partial —
   about a third of the span, and stopped short of the base.
3. **A picket fence of thin fins under the bench.** Cause was the *same*
   coplanar-boolean bug fixed earlier and reintroduced here: the cave cutter's
   top sat exactly on `A3`'s underside, punching 28 boundary holes, and
   **voxel-remeshing an open surface renders it as a thin wall**. Cutters are
   now tagged with the beds they may cut. 31 → 3 non-manifold edges.

> First diagnosis of that fence was **wrong** — I blamed the outline sampling
> and rewrote it to hold retreat per facet. That change is worth keeping on its
> own merits, but it was not the cause. Recorded so the next session does not
> trust the first explanation.

## Honest position

This is armature, not rock. It now carries jointing, sub-bedding, collapse,
talus and solution features — the structural story — but the terraces still
read as somewhat regular plates, and the surface is bare. Detail, colour and
magic remain Isaiah's, per `SCULPT-BY-NUMBERS.md`.
