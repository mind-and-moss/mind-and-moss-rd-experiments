# MONSTER8 — THE STORY

One history. Every feature in the geometry must be produced by a clause below,
and every clause must produce something visible. Anything in the mesh that no
clause explains is decoration and gets removed; anything a clause demands and
the mesh lacks is missing.

---

## EPISODE 1 — Deposition (the beds)

A shallow, warm, clear-water carbonate shelf. Six depositional units settle,
oldest at the bottom.

| Bed | What was happening | Consequence in the rock |
|---|---|---|
| `A1_platform` | quiet shelf, clean carbonate sand, well washed | thick, well-cemented **grainstone (h5)** — the strongest bed in the piece |
| `A2_marl` | **a river switched course.** Mud and clay poured onto the shelf | thin, clay-rich **marl (h1)** — the weakest bed, and the reason everything else happens |
| `A3_cap` | the river moved away again, clean water returned | thick, massive, well-cemented **(h5)** |
| `A4_bench` | shelf deepens slightly, mixed mud and carbonate | ordinary **biomicrite (h3)** |
| `A5_parting` | a brief muddy pulse, much smaller than Episode 1's | thin **marly parting (h2)** |
| `A6_perch` | shallowing again, moderately clean | **(h4)**, the last bed laid down |

**The whole design rests on one accident: the river.** `A2` is the bed that
should never have been there, and it is the bed that becomes the cave.

## EPISODE 2 — Burial and cementation

Deep burial. Carbonate beds cement hard; the clay-rich ones cannot — clay
blocks the pore throats where cement would grow. **Hardness contrast is set
here**, and it is permanent. The retreat table (h5→0, h4→5, h3→11, h2→19,
h1→38 mm) is the fossilised record of this episode.

Pressure-solution seams — **stylolites** — form along bedding, concentrating
insoluble clay into dark wisps. These deflect around anything rigid, which is
why they wander around fossils.

## EPISODE 3 — Uplift and jointing

Tectonic uplift brings the rock up into fresh water. Regional stress opens
**two near-vertical joint sets**:

- **J1, strike 68°, spacing 86 mm** — the dominant set, opened first, so it is
  more continuous and more widely weathered
- **J2, strike 152°, spacing 118 mm** — the conjugate set, later and less
  persistent

Joint spacing scales with bed thickness, so the thin beds are more finely
fractured than the massive ones.

**This episode is the single biggest control on the piece's shape.** Every
plan outline steps at a joint. Nothing curves smoothly, because nothing in
jointed rock does.

## EPISODE 4 — The water gets in (the cave)

Rain enters along the joints. Water moves fastest where **two joints cross**,
because that is where the rock is most broken and permeability is highest.
It sinks until it reaches the bed it can attack: **`A2`, the marl**.

Then it spreads sideways along that bed and dissolves it out.

**Therefore: the cave sits at a J1×J2 intersection, in `A2`, and nowhere
else.** It is not placed. It is where the water was always going to go.

- **mouth** — where the dissolved bed daylights on the front face
- **den** — the widening at the intersection itself
- **gallery and tail** — drainage running out along the weak bed
- the second, smaller opening — the same bed daylighting on another face,
  because a bed does not rot in one spot only

## EPISODE 5 — Collapse (the embayment and the talus)

`A2` retreats until `A3` above it is unsupported. `A3` is massive and strong,
so it does not sag — **it holds, then fails along the joints already there.**

**Therefore: the embayment sits directly over the cave, and its edges follow
the two joints that cross there.** The blocks that fell are joint-bounded,
which is why the talus is rectangular rather than rounded.

**Therefore: the talus lies at the foot beneath the embayment**, small because
it broke on landing, half-buried because the substrate has been accumulating
ever since.

## EPISODE 6 — Long exposure (wear and the basins)

Ages of weather.

- Exposed faces are **worn smooth and rounded**; sheltered recesses keep their
  detail. This is the wear-geometry gate, and it is a consequence, not a style.
- Ledge tops hold standing water, which dissolves shallow **solution basins**.
  These form preferentially at joint intersections, where water sinks in.
- The crest has been exposed longest and is attacked from above and both
  sides, so the skyline is broken rather than flat.
- **Grikes** — joints widened by dissolution into open slots — run down through
  the stack along the joint planes.

## EPISODE 7 — The fragment (why it is a corner)

The piece is a **broken fragment of a larger outcrop**. Its back and right are
fresh fracture surfaces, flat because they follow joint planes — which is why
they sit flush against tank glass and why the flat faces are not an artificial
imposition on the story.

---

## CONFORMANCE RULES

Derived from the above. These bind the geometry.

1. **The cave centres on a J1×J2 intersection.** Not a chosen coordinate.
2. **The embayment sits over the cave**, bounded by those same two joints.
3. **Talus lies beneath the embayment**, joint-bounded and rectangular.
4. **Grikes lie ON joint planes**, at true multiples of the joint spacing.
5. **Solution basins sit at joint intersections** on ledge tops.
6. **The second cave opening is in `A2` only**, where the bed daylights.
7. **Flat faces follow joint planes** — back and right.
8. **Nothing else may be placed by hand.** If a feature has no clause, it goes.

---

# CONFORMANCE AUDIT (`structure_story_conformant.py`)

Every feature printed with the clause that produced it. **13 features derived,
0 hand-placed.**

| Feature | Derivation | Position | Clause |
|---|---|---|---|
| cave centre | J1 plane k=0 × J2 plane k=1 | (−57.7, −44.1) | Ep4 — water sinks fastest where joints cross |
| cave run | along J1 strike, 68° | −94,−133 → −2,95 | Ep4 — drains sideways along the weak bed |
| second opening | J1 k=−1 × J2 k=0 | (63.1, 25.3) | Ep4 — a bed does not rot in one spot only |
| embayment | directly over the cave | (−43.5, −8.8) | Ep5 — `A3` loses support, fails along existing joints |
| grike J1 k=0 | ON joint plane | (−46.4, −16.0) | Ep6 — joints widened by dissolution |
| grike J2 k=0 | ON joint plane | (23.4, 46.4) | Ep6 |
| grike J1 k=−1 | ON joint plane, offset −86 mm | (30.4, −55.5) | Ep6 |
| grike J2 k=1 | ON joint plane, offset 118 mm | (−40.3, −53.3) | Ep6 |
| basin 1 | J1 k=1 × J2 k=1, ledge z=99 | (−134.1, −3.5) | Ep6 — standing water sinks in at crossings |
| basins 0, 2, 3 | **omitted** | — | Ep6 — no crossing on that ledge, so no basin |
| talus | beneath the derived embayment | (−43, −9) | Ep5 — joint-bounded blocks fell and broke on landing |

**Three basins were omitted, and that is the story working.** A basin forms
where joints cross on a ledge. On three of the four ledges the joints do not
cross inside the ledge, so those ledges have no basin. Nothing was invented to
fill the gap.

**Joint phase.** The joint sets are offset (J1 +37 mm, J2 −52 mm) rather than
passing through the origin. Without a phase the lattice puts an intersection
exactly at the centre of the piece, which dropped the cave dead-centre and
broke the lopsided ART gate. Episode 7 justifies it: the fragment was broken
out of a larger outcrop at an arbitrary place, so the joints have arbitrary
phase relative to it.

**Relaxation, declared.** Three features needed the search window widened
because the lattice offers no intersection where the composition wanted one.
That is reported at run time, not hidden. Basins may **never** be relaxed — a
basin that walks off its ledge is not a basin.

## Bugs found in this pass

1. **Cave landed at (0,0)** — dead centre, worst possible spot. Cause was the
   unphased joint lattice. Fixed by giving the joints a phase.
2. **Features derived outside the fragment** — a second opening at y=−179 on a
   piece ending at −125, a grike at (−319, 128), two basins on the same point.
   Derivation without bounds is not conformance. Now every candidate must
   exist inside the fragment (Ep7).
3. **A 200 mm drum of solid rock in the middle of the piece.** Rewriting the
   placement section deleted the boolean-apply loop and the cleanup along with
   it, and **the patch that tried to restore them matched nothing and failed
   silently.** So no boolean ever ran, every lamina stayed at its raw 170
   faces, and ~25 unused cutters survived into the render as solid geometry.
   Caught by listing objects and their face counts rather than trusting the
   render. Now verified by asserting the code is present before running, and
   by a name sweep so no cutter can leak.

## Validation after conformance

| Gate | Result |
|---|---|
| boolean ops applied | 74 |
| objects | 12 laminae + 46 talus = 58, no cutters |
| non-manifold after remesh | **0 — PASS** |
| components after remesh | 6 = main mass + talus clusters — correct |
