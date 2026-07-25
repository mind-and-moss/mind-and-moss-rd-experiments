# MONSTER8 — GATE RESULTS (session 7)

Measured, not asserted. Every number below came out of a script in this
folder; nothing here was eyeballed off a render.

## Object

**420 × 250 × 190 mm.** Reference shelf product ≈300 mm long → ~2.5× the volume.

| Bed | Thickness | Hardness | Plan W × D | Note |
|---|---|---|---|---|
| `A1_platform` | 38.0 mm | 5 | 420 × 250 | plinth |
| `A2_marl` | 20.9 mm | **1** | 344 × 174 | **the rotten one — the cave** |
| `A3_cap` | 39.9 mm | 5 | 364 × 194 | **overhangs A2 → the undercut** |
| `A4_bench` | 30.4 mm | 3 | 310 × 140 | |
| `A5_parting` | 17.1 mm | 2 | 258 × 88 | |
| `A6_perch` | 43.7 mm | 4 | 262 × 92 | **overhangs A5** |

Both overhangs are **outputs of hardness**, not drawn in. Retreat by hardness:
h5→0, h4→5, h3→11, h2→19, **h1→38 mm**.

## Boolean validation (`cave_chamber.py`)

| Bed | Faces before → after | Components | Verdict |
|---|---|---|---|
| `A1_platform` | 55 → 300 | 1 | **PASS** |
| `A2_marl` | 51 → 2099 | 1 | **PASS** |
| `A3_cap` | 58 → 2301 | 1 | **PASS** |

**OVERALL: PASS — no bed consumed, no bed split.**

*This check exists because v1 failed it.* The first cutter ate the entire
`A2` bed and left the model as two floating halves. It looked plausible in the
script and only showed up in a render. Now it is asserted.

## Chamber

| Measure | Value |
|---|---|
| ceiling (= `A3` underside, a bedding plane) | z 58.9 mm |
| floor (dished into `A1`) | z 28.0 mm |
| clear headroom | **30.9 mm** |
| den clear floor | 100 × 84 mm |
| turn-room (1.5× rule) | fish to ~56 mm (2.2") |
| mouth | 54 mm wide |
| tail exit | 36 mm wide — smaller than mouth ✓ |

## 3D passability (`validate_cave_passability.py`)

Voxelised at 4 mm, 30 600 cells, flood-filled from the mouth.

- **MOUTH → TAIL: PASS** — flow-through confirmed, not assumed
- **Narrowest constriction: ~1200 mm², ≈39 mm circular equivalent**, in the
  gallery around x = 38–50 mm
- **Passable-or-impossible: PASS** — 39 mm is clearly passable for the ~56 mm
  fish the den is sized for, so it is not a wedge

The constriction profile falls smoothly from 2752 mm² at the mouth to
1200 mm² mid-gallery and opens again to 1600 mm² toward the tail. A monotonic
taper with no sudden pinch is exactly what the no-wedge rule wants.

### Caveat, not yet resolved
8979 free cells vs 7779 reached = **1200 cells unreached**. Some of that is
exterior air outside the grid's connected region rather than sealed pockets
inside the rock, but **it has not been separated**, so "no dead ends" is
**not yet proven**. The validator needs an exterior mask before that claim
can be made.

## Known gaps

1. **Unreached-cell caveat above** — must be resolved before "no dead ends"
   is claimed.
2. **Headroom 30.9 mm is the weakest number in the piece.** A 56 mm fish has
   ~18 mm body depth, so it clears, but there is little margin. Deepening the
   floor dish or thickening `A2` both fix it; both change the terrace read.
3. **Segmentation not yet done at this size.** 420 mm exceeds the A1 mini's
   180 mm bed, so this piece *must* be split. Bedding-plane seams and 0.43 mm
   pegs are specified in `script07_segmentation_and_pegs.py` but have not been
   re-derived for the 420 mm outcrop.
4. **Wall-thickness ray probe (≥1.2 mm) not run** on the outcrop geometry.
5. The piece is armature only. Detail, colour and magic are Isaiah's —
   see `SCULPT-BY-NUMBERS.md`.
