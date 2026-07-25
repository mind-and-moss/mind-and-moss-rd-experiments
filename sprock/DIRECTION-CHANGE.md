# DIRECTION CHANGE — the plan is the base geometry, blocks are unbonded

## 1. The oval is gone

Isaiah, on the terraced outcrop: *"that cylinder shape looks like a rock area
rug made up by humans."* Correct, and the cause is structural: concentric
elliptical terraces are a shape rock never makes. Anything built from a
centre-and-radius reads as manufactured no matter how it is textured.

**`structure_base_from_plan.py` has no circle, ellipse or radius in it.** The
footprint is Isaiah's traced perimeter, and everything is built by walking that
line.

## 2. His plan is now the structural base

Seen from above, the geometry *is* the red/blue/green plan:

- **RED** — glass, back and right. Closes the void on two sides.
- **BLUE** — the rock perimeter. Blocks are built outward from it.
- **GREEN** — fish space, between the rock and the glass corner.
- **openings** — where the green passes the blue, exactly Isaiah's rule.

Perimeter run **256 mm**, traced from the sketch, resampled at 3 mm.
Wall thickness **13 mm at the back glass → 28 mm at the front-right toe**,
modulated per bed by hardness (h5 keeps 1.00 of it, **h1 keeps 0.50**), so the
soft beds are recessed on the OUTER face — the face that meets the water.

## 3. The blocks are UNBONDED

**37 separate objects.** Not one mesh, not joined, not welded.

- Blocks are cut at **joint crossings** — a block ends where a fracture crosses
  the perimeter, so the divisions are geological rather than arbitrary
- Slivers under 11 mm are merged away; a block shorter than that is not a block
- **Each block's origin sits at its own centre**, so it rotates and scales about
  itself and can be nudged, tilted or sculpted independently
- Each carries `hardness`, `bed` and `block` as custom properties

| Bed | Hardness | Thickness | Blocks |
|---|---|---|---|
| `A1_platform` | 5 | 38.0 mm | walked from the plan |
| `A2_marl` | **1** | 20.9 mm | fewest wall, most recessed |
| `A3_cap` | 5 | 39.9 mm | |
| `A4_bench` | 3 | 30.4 mm | |
| `A5_parting` | 2 | 17.1 mm | |
| `A6_perch` | 4 | 43.7 mm | |

7 joint-bounded blocks per bed before openings are removed.

**Nothing is ever joined in the build.** The preview mesh is made from
*copies* at render time only, so the sculptable originals are never touched.

## Carried over unchanged

The story (`THE-STORY.md`), the hardness table, the opening rule, the joint
sets, and every validator. Only the massing changed — which is what
`monster8-BIBLE.md` says should be disposable.

---

## 4. "It looks like it's all melted together"

Correct — blocks sharing an edge flush weld into one wall. Fixed, then
**overcorrected into blocks floating in mid-air**, which is worse. Going back
to the Valdoviño photograph settled it:

> **That cliff is a solid mass with fractures running through it. Every block
> is still touching its neighbours.** The separation you see is the *seam*,
> not a gap.

So the separation now lives in the seam and a small set, not in空 space:

| | before | after |
|---|---|---|
| plan offset per block | ±15 mm | **±4.2 mm** — a set, not a gap |
| joint aperture | 3–6 mm | **0.8–1.8 mm** — a fracture is a line |
| block height | 0.80–0.96 of bed | **0.995–1.015** — beds stay in contact |
| tilt | ±0.13 rad | **±0.045 rad** |

An offset larger than the wall is thick slides a block clean off whatever is
under it. The wall is 13–28 mm, so ±15 mm was never going to stand up.

## 5. Staggered joints — what stopped it reading as columns

Every bed was using the *same* joint crossings, so all the block edges lined up
vertically and the wall read as a row of separate towers.

**Joints step between beds.** Each bed now carries its own joint phase, so the
blocks interlock. This is the single change that made it read as one rock
rather than a stack of columns.

Sampling was also tightened from 3 mm to 1.2 mm, because trimming the aperture
dropped a whole sample at each block end — a 1.2 mm aperture was producing a
6 mm gap.

## 6. Maturity systems carried over from the corner-wall lineage

Isaiah: *"I liked most everything about that build before the cylinder was
added, it just was still adolescent."* Those systems are now on the plan
footprint:

- **plucking** — weathering removes whole blocks, weighted by hardness,
  proximity to the mouth, and height
- **broken crest** — pluck probability rises with height
- **bedding dip 9°** — beds climb 41 mm across the run
- **wear bevels** — scaled by how proud and how high a block sits
- **talus** — every plucked block falls outward and lands at the foot

38 unbonded objects, 4 plucked → 4 talus.

## Still short of the reference

Against Valdoviño: block sizes are too uniform (that cliff has huge masses
beside small ones), and the profile is still a thin wall where the photograph
has depth and standing pinnacles. Both are massing, both are machine work,
neither is texture.
