# BOOT PROMPT FOR THE NEXT SESSION

> **CORRECTED.** The first version of this file said the next job was "cut the
> two machine cracks." **They are already cut.** `m8_b2j_core.stl` was exported
> 01:31 and independently verified on disk at 141.33 × 121.70 × 114.38 mm,
> 248k triangles, scale correct in mm.
>
> The error: *"Machine put in TWO jagged cracks and nothing else"* is **past
> tense** — a pre-print protocol describing a finished part. It was read as a
> specification of work to do. A completed deliverable was turned into a task.
>
> Second error underneath it: **Laws 3, 4, 7 and 8 are laws for Isaiah's hand,
> not machine jobs.** T-junctions, nucleation flaws, banded veins are sculpting
> rules. Listing them as "the next job" aimed the machine at precisely the work
> doctrine #1 reserves for him.

---

## THERE IS NO GEOMETRY WORK LEFT BEFORE PRINTING

`m8_b2j_core.stl` is **done and certified**: manifold 0 · 1 shell · 0 loose
verts · walls min 6.58 mm (spec 1.2) · base/back planarity 0.000000 mm · bore
radius 24.35 mm held · `global_scale=1000`. **Fits the A1 mini 180 bed whole —
no segmenting, no pins.**

**Do not open a geometry job.** Per Isaiah's own crack-division-of-labour rule,
that is the work that ate six rounds in session 6. Everything on tonight's path
is slicer-side and hands-on.

---

```
You are the Sprock working director. Monster 8, block 2 = THE STUMP.

STATE: m8_b2j_core.stl is FINISHED, VALIDATED and READY TO SLICE.
141.33 x 121.70 x 114.38 mm, 248k tris, mm scale, fits the A1 mini bed whole.
The two machine cracks are ALREADY CUT. Do not re-cut them. Do not open a
geometry job. There is no modelling between here and printing.

TONIGHT IS: slice -> print -> (after cure) hand-sculpt.

READ FIRST:
  sprock/session6/CRACK-LAWS.md   <- the 8 laws + print protocol + surface
                                     classes. Laws 3,4,7,8 are ISAIAH'S HAND,
                                     not machine tasks.
  sprock/SCULPT-BY-NUMBERS.md     <- zones: what each surface IS
  sprock/THE-STORY.md             <- the stump is OLD, the wound is NEW

SLICE SETTINGS (already decided, do not relitigate):
  PETG - 0.2 mm layer - 3 walls - 0% INFILL
  0% -> ~160 cm3, ~10.5 h.   15% -> ~370 cm3, ~25 h and blows the night.
  It is a puttied substrate, not a structural part, and a hollow cave is
  better in-tank anyway.

BEFORE GO:
  - BASE FLAT DOWN ON THE PLATE. Do not let the slicer auto-orient. The base
    is a glass-contact face; printing it against the plate is what makes it
    true.
  - Tunnel HORIZONTAL, parallel to the bed.
  - NO SUPPORTS. The bore roof is a self-supporting 45 deg teardrop; the cap
    at the peak is 1.25 mm and bridges. If the slicer wants support inside the
    tunnel, THE ORIENTATION IS WRONG - stop and fix it.
  - Elephant-foot compensation ON.
  - Brim on the perimeter ONLY, never on the base face, must come off clean.
  - Preview at half height: open teardrop, nothing inside.
  - ~200 g PETG plus margin.

OFF THE PLATE, BEFORE ANYTHING ELSE:
  - Straightedge across the base. Flat, no rock, no lip. If it is not flat the
    corner format fails at the glass - better to know now.
  - Sight the tunnel end to end: clear and fish-passable.
  - The two machine cracks should read ~3.5 mm wide, ~6 mm deep.

THEN THE HANDS TAKE OVER - order of work from session 6:
  1. bed lines first on front + ends (the skeleton everything obeys)
  2. relief net under the top scar - fine, tight
  3. work down: fewer, bigger joints toward the base
  4. run new cracks INTO the two machine cracks and STOP there (T-junctions =
     chronology; a younger crack never crosses an older one)
  5. round every exposed arris on front + ends; LEAVE THE TUNNEL SHARP -
     sheltered rock does not round
  6. rust ONLY on the top scar plus one protected halo

THE ONE LOUD EVENT is the fall. If a detail competes with the scar, cut it back.

BUDGET: weekly meters are near empty. Protect them by NOT opening a geometry
job. Fable is not a reservoir - it is also nearly spent, and tonight's work is
hands-on anyway, so the saving would be rounding error.
```

---

## Session 7's build is NOT the printable part

`sprock/structure_base_from_plan.py` — 32 unbonded blocks on Isaiah's traced
corner plan — is a **separate massing study**, not `m8_b2j_core`. It explores
block variety, joint spacing under Law 1, staggering, and the surface classes.

**Do not confuse it with the part.** If a future session wants to use it, it is
a study to learn from, not a thing to print.

What it did establish, and what is worth keeping:
- joint spacing derived per bed at 0.8–1.2 × that bed's own thickness, hard
  clamped, because below 0.8× reads fake
- staggered joints between beds (Law 5) — the single change that stopped the
  wall reading as columns
- bevel limited to outward faces so the tunnel keeps sharp edges
- blocks flush along a run **weld**; blocks offset more than the wall is thick
  **float**. Separation lives in the seam.

## The one thing to do yourself

Bank the local outputs folder — the `.blend`, `sprock-knowledge/`,
`erosion_rock`, the BLENDER TRAPS list, `blender-limestone-playbook.md`.

**That folder blocked session 7 three times.** The crack laws only arrived
because Isaiah pasted them by hand — and this stale-boot error is a direct
consequence of the same gap: a session that could not see the STL on disk did
not know the part was already built.
