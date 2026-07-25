# THE CRACK LAWS — banked from session 6

Source: Isaiah's `PRE-PRINT PROTOCOL + SCULPT MAP — m8_b2j_core.stl`, itself
drawing on `23-research-01-how-cracks-form` and
`30-explore-fallen-family-monster8`.

**Banked here because this document blocked session 7 three separate times.**
It lived only in the local outputs folder. It is now in the repo.

---

## The piece it describes

**Block 2 = THE STUMP**, the corner mass. **141.3 × 121.7 × 114.4 mm.**
Fits the A1 mini 180 bed **whole — no segmenting, no pins.** Solid volume
1548 cm³, 94.7% of the block kept.

Validated in session 6: manifold 0 · 1 shell · 0 loose verts · walls min
**6.58 mm** (spec 1.2) · back + base planarity **0.000000 mm** · bore radius
24.35 mm held · `global_scale=1000`.

> **"Machine put in TWO jagged cracks and nothing else. Everything else is
> your hand."**
>
> That is Law 2 quantified. Not "a few" — **two.**

## The story

**Block 2 is THE STUMP: the surviving corner remnant that the Fallen Family
broke off from.** Everything cut must serve that one sentence.

**The stump is OLD and the wound is NEW.**

**The fall is this piece's single loud event.** Everything else stays quiet.
If a detail competes with the scar for attention, cut it back.

## The four surface classes

| surface | role | treatment |
|---|---|---|
| **BASE** (down) | glass contact | **DO NOT TOUCH.** Dead flat. |
| **BACK** (tall flat face) | glass contact | **DO NOT TOUCH.** Dead flat. |
| **TOP** | **THE SCAR** — the exhumed hardground the slab tore off along | the wound. Fresh-to-young. Rust-stained. Fine grike lines. |
| **FRONT + the two ends** | the stump's weathered flanks | **OLD-ANCIENT** — fully rounded arrises, grain, no sharp edge survives |
| **TUNNEL INTERIOR** | sheltered den | **edges KEPT SHARP**, pits + grain, darkest. Sheltered rock does not round. |

The front face is the hero. The back-right glass corner is buried — spend
nothing there.

## THE EIGHT LAWS

**1. SPACING = BED THICKNESS.** Well-developed joint spacing is
**0.8–1.2 × the thickness of the bed being cracked.** Closer than 0.8× reads
FAKE — the rock physically cannot over-crack, because each joint casts a
**stress shadow about one bed-thickness wide** where no new joint can form.
Sparser than ~1.5× reads under-strained but is still plausible.
→ Decide bed thickness first, then space cracks off it. A 15 mm bed gets
cracks ~12–18 mm apart. **Never tighter.**

**2. THIN BEDS CRACK DENSE, THICK BEDS CRACK SPARSE.** Automatically, by law.
A platy course near the top gets a fine net; the massive lower body gets a few
big joints only. **This contrast is free realism.**

**3. JOINTS STOP AT WEAK INTERFACES.** A crack dies at a bed seam. Only a
**MASTER joint** runs through many beds — and there should be **ONE OR TWO PER
PIECE, NO MORE.** Every other crack must **die at a bed line.**

**4. T-JUNCTIONS ARE CHRONOLOGY.** A younger crack meeting an older one either
stops dead, **HOOKS to meet it at right angles**, or curves into parallel with
it. **It never crosses it.** Every T says "this one came second," and a viewer
reads that without knowing why.

**5. ADJACENT BEDS JOINT INDEPENDENTLY.** Offset cracks at every bed boundary.
**That stagger is mechanism, not style** — lining them up is what makes it look
like brickwork.

**6. RELIEF TIGHTENS UPWARD.** Unloading cracks run roughly parallel to the top
surface and their spacing gets **FINER toward it.** The crest unclenches first
and finest. → Densest cracking just under the top/scar, calmest at the base.

**7. CRACKS NUCLEATE AT FLAWS** — a pore, a fossil, a concretion. A fresh break
face carries **plumose structure**: a smooth **MIRROR** at the origin, then
**MIST**, then **HACKLE** barbs fanning out like a feather, then concentric
**ARREST LINES** where growth paused. The plume points back at where the break
began. **Put a flaw where you want a crack to start.**

**8. VEINS ARE BANDED.** Crack-seal repeats tens to hundreds of times, so a real
white vein is a **STACK OF THIN BANDS**, not one uniform stripe.

## Order of work

1. Establish **bed lines** first on the front + ends — the skeleton everything obeys
2. Cut the **relief net under the top scar** (fine, tight)
3. Work down: **fewer, bigger** joints toward the base
4. Run new cracks **into the two machine cracks and STOP them there** (T-junctions)
5. **Round every exposed arris** on the front and ends. **Leave the tunnel sharp.**
6. **Rust ONLY on the top scar** plus one protected halo. Palette law — do not spread it.

## Print protocol

- **Base flat down on the plate.** The base is a glass-contact face; printing it
  against the plate is what makes it true. **Do not let the slicer auto-orient.**
- Tunnel runs **HORIZONTALLY**, parallel to the bed
- **NO SUPPORTS.** The bore roof is a **TEARDROP, apex 45°**, self-supporting;
  the near-flat cap at the peak is 1.25 mm wide and bridges. **If the slicer
  wants support inside the tunnel, the orientation is wrong — stop and fix it.**
- PETG · 0.2 mm layer · **3 walls · 0% infill** → ~160 cm³, ~10.5 h.
  15% infill would be ~370 cm³ and ~25 h — do not. This is a puttied substrate,
  not a structural part, and a hollow cave is better in-tank anyway.
- Elephant-foot compensation ON. Brim around the perimeter only, **never on the
  base face.** Preview at half height: open teardrop, no support inside.
- After printing, before packing: **straightedge the base** (flat, no rock, no
  lip — if it isn't flat the corner format fails at the glass), sight the tunnel
  end to end, confirm the two machine cracks read ~3.5 mm wide × ~6 mm deep.

---

# APPLIED IN SESSION 7 — `structure_base_from_plan.py`

| Law | Before | After |
|---|---|---|
| **1. spacing = bed thickness** | one global 34/44 mm regardless of bed | **per bed, 0.8–1.2× its own thickness** |
| **2. thin dense / thick sparse** | not modelled | falls out of Law 1 for free |
| **5. adjacent beds independent** | ✔ already staggered | kept |
| **6. relief tightens upward** | not modelled | spacing finer toward the scar |
| **surface classes** | bevel by exposure | **bevel limited to a vertex group of outward faces — tunnel edges stay SHARP** |
| **scale** | 420 × 250 × 190, 8.3 L, 18 pieces, 99 pegs | **141.3 × 121.7 × 114.4 — fits the bed whole** |

Measured result, every bed inside the legal window:

| Bed | Thickness | Spacing | Ratio |
|---|---|---|---|
| `A1_platform` | 22.9 mm | 22.6 mm | 0.99× |
| `A2_marl` | 12.6 mm | 11.2 mm | 0.89× |
| `A3_cap` | 24.0 mm | 27.2 mm | 1.13× |
| `A4_bench` | 18.3 mm | 16.0 mm | 0.87× |
| `A5_parting` | 10.3 mm | 11.3 mm | 1.09× |
| `A6_perch` | 26.3 mm | 27.6 mm | 1.05× |

**Law 1 needed a hard clamp.** First attempt let Law 6's relief factor multiply
the ratio down, and two beds came out at **0.75× and 0.78×** — inside the
reads-fake zone. Law 1 is a floor, not a preference: below 0.8× the rock
physically cannot over-crack. **Law 6 may tighten spacing toward the scar but
may never breach Law 1's floor.** Clamped to [0.80, 1.20].

## Not yet applied

- **Law 3** — only 1–2 master joints. Blocks are per-bed so cracks already die
  at bed lines, but the master joints are not yet explicit.
- **Law 4** — T-junctions. Needs the two machine cracks placed first, then
  hand cracks hooked into them.
- **Law 7** — flaws as nucleation points, plumose structure on break faces.
- **Law 8** — banded veins.
- **The two machine cracks** (~3.5 mm wide × 6 mm deep) are not cut yet. Per
  session 6 these are the *only* machine cracks; everything else is Isaiah's
  hand.
