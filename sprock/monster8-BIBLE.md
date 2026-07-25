# MONSTER8 — BUILD BIBLE (restart)

Single source of truth for rebuilding the Monster8 blockout from scratch.
Written session 7. Supersedes nothing — the Drive canon is still canon; this
consolidates the parts that govern **geometry** into one reachable place.

**Restart rule: the mesh is disposable, the doctrine is not.** Geometry is an
afternoon. The ledger below cost six sessions. Throw away the blockout, keep
every line of this.

---

## 1. Sources this is built from

**Reachable and read:**
- Drive: ★ START HERE v2 — SPROCK Master Handoff (Jul 8) — full text
- Drive: Decisions Locked Jul 6; Session Update Jul 2; Sample Kit v1;
  Blender Core Work Brief Jul 8; Soak Test Log
- Repo: `findings/products/the-gem/hardscape-workflow.md`,
  `findings/topics/cad-and-modeling/cad-pipeline.md`
- Session 6 close: the two laws (§5)
- Two reference images supplied by Isaiah (§3)

**Named in the canon but NOT reachable from any remote session:**
- `blender-limestone-playbook.md` — verified R1–R8 recipes, the v3
  boolean/remesh/displace law, sculpt techniques, A1-mini presets
- `blender-training-brief.md`
- `sprock-knowledge/33-monster8-blockout-state.md`, `34-boot-lean.md`
- the `erosion_rock` module, the BLENDER TRAPS list
- `monster8_blockout.blend` itself

All of the above live in a local outputs folder that has now blocked a remote
session twice (Jul 8 brief, and session 7). **Bank them or this repeats.**

---

## 2. The product, in one paragraph

Grey water-worn **limestone** aquarium hardscape. Sprock is a CORNER-FORMAT
cave — back + left faces flat against tank glass — in through-pigmented epoxy
putty over an optional printed PETG core. Freshwater, goldfish-first. One dead
fish traced to the brand kills the business, so everything is gated by
cure → soak → pH-vs-control before livestock. Everything.

---

## 3. Reference frame: a WAVE-CUT LIMESTONE COAST

Isaiah supplied two images. They do not carry equal authority.

**Image A — Valdoviño, Spain (real coastal rock): the bible.** Stacks left
standing where hard rock resisted, rounded boulders where it did not, water
with somewhere to go. Every feature has a cause. This is the doctrine as a
photograph.

**Image B — a competitor product listing ("Rocks and Caves"): NOT the bible.**
Use only for *structure* — multi-level massing, several openings, ledges,
silhouette variety. Never for *surface*. The drybrushed uniform grey resin is
precisely what Sprock differentiates against (Session Update Jul 2: the
PetSmart shelf validates the category; its weaknesses are our differentiators).

**The conflict, and its resolution.** Valdoviño is Galicia — schist and
granite, steeply dipping, joint-controlled, **no bedding planes and no
fossils**. The entire finish program (Jura Grey, ammonite cross-sections,
stylolites deflecting around fossils, veins cut along bedding) assumes
*flat-bedded limestone*. Adopting Valdoviño literally destroys the fossil
program.

→ **Resolution: a wave-cut LIMESTONE coast** — Étretat, the Algarve. Real
places where the sea eats limestone. Gets Valdoviño's drama (stacks, arches,
undercuts, talus) **and** keeps bedding planes, fossils, stylolites, veins.
Nothing is given up.

**Why this frame is worth adopting: it hands us Law 1 for free.** A sea cave
is the textbook mouth-as-output — surf attacks the weakest bed at the
waterline → undercut → the hard bed above loses support → it collapses → the
mouth is the scar. Nobody bores it. Same mechanism the freshwater story uses:
rain in the crest joint → chamber → drains sideways along the weak bed → tail.

---

## 4. DECISIONS LEDGER — locked, do not reopen without Isaiah

Carried verbatim from ★ START HERE v2.

- **Corner format:** back + left + base FLAT (vertex-clamped, **never
  boolean-on-displaced**). Mouth on RIGHT face. Small exit low on FRONT-left.
  Narrow offset skylight in TOP over the **GALLERY** — never over the chamber;
  the den stays dark so the fish gets a dark+light choice. **One connected
  void, no dead ends.**
- **Two openings**, exit smaller than mouth, everything fish-passable or
  clearly impossible — **no wedges** (a fish pushes forward and jams; it will
  not reverse).
- V1 low / simple / single-piece. Tall hero = pinned segments (A1 mini bed
  180 mm; pins proven perfect).
- **Hollowing:** slicer infill (3 walls, 10–15% gyroid) + Bambu
  modifier-volume blobs. Modeled voids ONLY for function (ballast). Do not
  hollow rocks in Blender.
- **Ballast:** Option C — washed inert gravel (vinegar fizz test every batch)
  + pond-rated foam, inside the sealed shell. No raw concrete inside.
- **Fossils:** hand-finishing tier. Calcite-white cross-sections (burnish to
  satin), molds with dark wash, rare rust halo. Along bedding planes. Flush,
  never proud. Reference stone: **Jura Grey**.
- **Veins:** chronology-true — CUT the firm rock along fracture logic, pack
  cream white, shave flush at leather stage.

---

## 5. THE LAWS

**Law 1 — THE CAVE MOUTH IS AN OUTPUT, NOT AN INPUT.**
Layers + hardness + collapse. Never a bored cylinder. If the stack cannot
produce the mouth by undercut and collapse, fix the *stack*, not the boolean.

**Law 2 — NEVER TUNE A CRACK GENERATOR TO LOOK LIKE ROCK.**
The machine cuts 1–2 real cracks plus a story-driven placement map. Isaiah's
hands do everything that has to read.

**Doctrine #1, which is Law 2 generalised — MACHINES = ANATOMY, ISAIAH = ART.**
Procedural builds do massing, voids, walls, validation, exports. All organic
beauty is Isaiah's hands. **Never art-direct a bot past two iterations —
reframe the job as engineering.**

**Doctrine #2 — cores are invisible.** The printed core is buried under putty.
Its virtues are anatomy, walls, and grip (bedding ledges, scored grooves,
undercut pockets, on visible faces only). Never spend on core beauty.

**Doctrine #4 — ask before acting.** Sessions propose, Isaiah approves, then
execute. Checkpoint rhythm: he works → messages → session LOOKS at a
screenshot → then responds.

---

## 6. GATES — every build passes all three sets

**ENGINEERING**
- manifold = 0
- ray-probe walls ≥ 1.2 mm at print scale (3 perims × 0.4 mm)
- face-count sanity check after every modifier
- flat base for supportless printing
- STL export `global_scale = 1000` (meters → mm)
- first print at reduced scale (3–4") before any full-size run

**ART**
- shadow-first: the mouth is the **darkest thing** in a top-front-lit render
- lopsided — never symmetrical
- pareidolia check: *"would a toddler name it?"*
- wear-geometry: detail lives in recesses, not on exposed faces
- every feature has a water story

**BIO**
- turn-room ≥ 1.5 body lengths of the largest resident (6" goldfish → ~9"
  clear floor)
- passable-or-impossible, never in between
- smooth flared rims
- flow-through draught, mouth-in → tail-out
- dark + light choice
- feathered buried edges, dig-stable

---

## 7. BUILD ORDER — the stack-order law

Violating this is how blockouts die.

1. All geometry and **booleans FIRST**
2. then voxel remesh
3. then **displacement LAST** — and displacement is for render preview only,
   never on the print core

Corollaries:
- **Never boolean-on-displaced.** The flat glass faces are vertex-clamped, not
  cut.
- Reinforcement, if ever modeled, is an interior named union part *before* the
  texture pass.
- Everything stays **separate, named objects**.

**Session 7 negative result, recorded so it isn't repeated:** displacement
along normals will NOT produce a cave mouth. A strawman was built here with
six hardness-graded beds and mouth-zone vertex weighting; it produced weathered
slabs and no opening. Cranking strength until something cave-shaped appears is
Law 2 exactly. The mouth needs genuine **retreat and collapse** — real
geometry, built in the right order — not a displacement parameter.

Two real bugs found while proving that, worth not repeating:
- a `size=1` cube already spans 1 unit; scaling by `thick/2` builds every bed
  at **half** thickness (silent, and it separates the stack)
- eroding a bed's **buried** top/bottom faces shrinks it away from its
  neighbours; only exposed faces may move

---

## 8. STACK_S7 — the layer stack (SPECIFIED)

Replaces the invented `STACK_B2`. This is **anatomy, therefore machine work**
(doctrine #1) — it is not Isaiah's to guess. Given as fractions of total
height so it rescales without redesign.

| # | Bed | Frac of H | Hardness | Lithology / role |
|---|---|---|---|---|
| 1 | `B1_basal_massive` | 0.20 | **5** | well-cemented grainstone — floor + plinth |
| 2 | `B2_marl_weak` | 0.12 | **1** | argillaceous marl — **THE ROTTEN ONE**, becomes the gallery |
| 3 | `B3_massive_cap` | 0.22 | **5** | massive, well-cemented — the overhang that collapses into the mouth |
| 4 | `B4_medium_bedded` | 0.18 | **3** | ordinary biomicrite |
| 5 | `B5_marl_parting` | 0.08 | **2** | thin marly parting — a ledge, not a collapse |
| 6 | `B6_crest_jointed` | 0.20 | **4** | crest bed, takes the vertical joint — rain enters here |

**Why these are the rotten ones.** In a limestone sequence, resistance is
controlled by cementation and clay content, not by the limestone itself.
Marly / argillaceous interbeds are the classic recessive beds — they weather
back fastest and cut the notch. Massive well-cemented beds hold the cliff.
Stylolitic seams concentrate clay and become weakness planes. Jura Grey (the
locked reference stone) is exactly this: well-bedded micritic limestone with
marly partings.

**Retreat by hardness**, as a fraction of block depth D — the difference
between adjacent rows is the entire design:

| Hardness | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|
| Retreat | 0.02 D | 0.05 D | 0.10 D | 0.18 D | **0.45 D** |

**Contrast is what matters, not softness alone:**
- **B2 (1) under B3 (5) — contrast 4, the maximum.** This is the collapse
  engine: deep undercut, unsupported cap, failure along joints. **The mouth.**
- B5 (2) under B6 (4) — contrast 2. A ledge and a shadow line, no collapse.
  Wear-geometry gate: detail lives in this recess.
- B2 (1) sitting on B1 (5) — the weak bed rots out **above a hard floor**,
  which is why the chamber has a flat diggable floor and drains sideways
  rather than down. Matches the locked water story exactly.

**Units:** built in metres at `1 unit = 1 mm / 1000`; export STL with
`global_scale = 1000`. Default instantiation `H_TOTAL = 120 mm`,
`W = 180 mm` (A1 mini bed limit), `D = 140 mm`. Change `H_TOTAL` to rescale.

**Open conflict, flagged not hidden:** turn-room ≥1.5 body lengths for a 6"
goldfish needs ~9" (228 mm) of clear floor, which exceeds the A1 mini's
180 mm bed. V1 at this scale suits smaller residents; the 6" goldfish hero
must be the pinned-segment build. Isaiah's call, already anticipated in the
ledger.

**Script 01 status (`sprock/script01_massing_and_undercut.py`):** verified
headless. Differential retreat produces real undercuts — the deepest shadow
in a top-front-lit render, satisfying the shadow-first ART gate. Still to do:
localise the retreat so it reads as a mouth rather than a continuous slot,
break the rectangular plan (lopsided gate), then collapse the cap.

## 9. TOOLCHAIN — verified session 7

- **blender-mcp addon 1.2 works on Blender 5.0, NOT 5.1.** On 5.1 it connects
  ("Running on port 9876") and then every command times out, including
  `execute_blender_code`. Upstream issue #243, open. Issue #185 notes the
  `bl_info` minimum is untested.
- Isaiah is running **5.1**, so the bridge is unavailable to him today.
- **The fallback is already doctrine** (Decisions Locked Jul 6): *"MCP bridge
  addon mismatch — use script-paste + chat-panel workflow."* Script written in
  chat → pasted into Blender's Scripting tab → Run → screenshot back. Works on
  5.1, needs no bridge, and satisfies doctrine #4's checkpoint rhythm.
- A remote container can run headless Blender (Ubuntu apt, Cycles CPU,
  `use_denoising = False`) but only at **4.0.2** — far too old for a 5.x file.
- **File-version trap:** Blender opens older files reliably, newer ones not.
  Combined with save-on-quit-over-the-same-file, opening a 5.1 file in 5.0 can
  drop data and then overwrite the only good copy. Check the header by opening
  the `.blend` in Notepad — first line reads `BLENDER-v` + three digits. Copy
  before opening, always. Adopt `Ctrl+Alt+S` (Save Incremental).

---

## 10. First moves on the restart

1. Isaiah fills §8.
2. Build the massing as separate named beds, correct thicknesses, flat
   back/left/base by vertex clamp.
3. Cut the void as a **named cutter part** — one connected void, mouth-in →
   gallery → tail-out, skylight over the gallery only.
4. Let the weak bed retreat and the hard cap collapse. Do not bore the mouth.
5. Validate: manifold, walls, face count, flat base.
6. Only then remesh, and only then displace — preview only.
7. Screenshot at every step. Ship the picture unasked, including the ugly ones.

---

## 11. DECISION CHANGE — corner format is now BACK + RIGHT

**Supersedes the ledger.** ★ START HERE v2 locked "back + left + base FLAT".
Isaiah's session-7 sketch places the glass on **back + right**, and he
confirmed: *"back and right is the new call."* The piece is the mirror of the
old ledger entry.

**Consequence that must not be missed:** the ledger also put the mouth on the
RIGHT face. The right face is now *glass*, so the mouth cannot live there.
All openings move into the perimeter wall.

## 12. The piece is a WALL, not a block

Isaiah's plan is not a solid block with a bored void. It is a curved wall that
sits in the tank corner; **the void is closed on two sides by the tank glass
itself.** Measured off his traced line:

- void 124.8 cm² in plan vs rock 45.1 cm² — mostly space, light and cheap
- wall 13 mm thick at the back glass, thickening to 28 mm at the front-right toe
- perimeter run 256 mm

Lopsided by nature, so the ART gate is satisfied by the form rather than bolted on.

## 13. OPENINGS — Isaiah's rule

> *"where the green passes the blue = opening"*

An opening is simply a stretch of perimeter carrying no wall. Positions are
parameterised along the run (0 = back-glass end, 1 = front-right toe), so they
move by changing one number.

| Opening | s | width |
|---|---|---|
| `upper_vent` | 0.17 | 20 mm |
| `MOUTH` | 0.52 | 42 mm |
| `tail_exit` | 0.83 | 24 mm |

Each is a short tunnel through a 13–28 mm wall, not a notch in a cliff face.

## 14. THE WINDOW — frost film goes on the OUTSIDE

Where the void meets the glass is the window: **123 × 140 mm, L-shaped around
the corner.**

**Mount the film on the OUTSIDE of the tank glass (Route B).** From
`findings/products/cylindrical-terrarium/film-installation.md`:

- Route B — outside mount: **indefinite lifespan, trivially replaceable, zero
  humidity exposure**
- Route A / C — inside mount: 3–5 years, the film edge is the long-term weak
  point, and Route C's adhesive chemistry is *"unvetted for sealed bioactive
  environments"*

**Why this is the whole call and not a detail:** the business is gated on
*one dead fish traced to the brand kills it*. An inside-mounted film puts
unvetted adhesive in the water and drags the window through the full
cure → soak → pH-vs-control pipeline. Outside-mounted, the film never touches
the water and **exits the safety pipeline entirely.** An entire risk category
disappears for free.

Cost: the customer applies it to their own tank, so it ships as a pre-cut
patch with an alignment guide. The finding also notes outside mount gives a
different optical look — worth a bench comparison before it is locked.

## 15. OPEN CONFLICT — a 123 × 140 mm window versus "the den stays dark"

The skylight was restricted to the gallery specifically so *"the den stays
dark; fish gets dark+light choice"*. Frost film **diffuses** light, it does not
block it, so a window this size floods the whole void with soft light and
there is no dark pocket left anywhere.

The dark+light choice is a BIO gate. Options, unresolved:
1. Shelter a dark recess behind the 28 mm toe, away from the window
2. Mask part of the film patch opaque rather than frosting all of it
3. Shrink the window so it lights only part of the void

Isaiah's call.

---

## 16. FUNDAMENTAL CHANGE — the wall is an ASSEMBLY OF RECTANGULAR BLOCKS

Isaiah's call, session 7. The wall is no longer one extruded ribbon; it is
many rectangular blocks in varied positions.

**This is not a simplification — it is the mechanism.** Bedded limestone is
cut horizontally by bedding planes and vertically by two joint sets, and it
comes apart into rectangular blocks. A smooth extruded curve reads as a
retaining wall precisely because rock does not do that. It also happens to be
exactly what a peg-and-socket assembly wants.

**Two real relationships are built in rather than styled in:**

1. **Joint spacing scales with bed thickness.** Thick beds break into wide
   blocks, thin into narrow. Observed geology. The stack then reads on its
   own with nothing tuned:

   | Bed | Thickness | Joint spacing | Blocks |
   |---|---|---|---|
   | `B3_massive_cap` | 26.4 mm | 38.4 mm | 6 |
   | `B5_marl_parting` | 9.6 mm | 19.0 mm | 9–13 |

2. **Collapse is recorded in block POSITIONS, not in a texture.** Blocks near
   the unsupported span have slipped out and dropped; blocks in solid wall
   have not. This keeps the erosion story on the right side of Law 2 — it is
   structural, not generated.

**All variation is deterministic** (seeded FNV hash of bed and block index).
The same script always builds the same rock. This matters: a random rock
cannot be iterated on, reviewed, or reproduced for a second casting.

### Session 7 fixes applied after the first block pass (script 05)

The first assembly read as masonry. Three causes, all structural:

1. **Relief** — every block sat at the same depth, so the face was a plane
   with grooves. Offsets now scale with wall thickness (±0.42 t for hard beds,
   ±0.62 t for soft), and soft beds are biased to sit back.
2. **Plucking** — every course position was filled. Weathering removes whole
   blocks. Pluck probability is by hardness (marl 0.34, massive 0.05) plus a
   bonus near the mouth where blocks were unsupported. 8 of 47 plucked.
3. **Size variation** — was ±25%, which is brickwork. Now 0.45–1.80 × spacing
   on a power curve, so a few large blocks anchor the composition.

### Still open

The overall SILHOUETTE is still a rectangle. Real cliffs have a broken crest
and talus at the base. Fixing the envelope — not the blocks — is the next
form problem.

---

## 17. "THIS PIECE HAS SURVIVED HISTORY" — four structural consequences

Isaiah's note, session 7. Not a mood — a set of physical facts, each of which
changes geometry:

1. **Survivors are big.** Small blocks were carried off long ago. Sizes skew
   large and scale with hardness (massive ×1.30, marl ×0.72), so the resistant
   beds keep large masses while the weak beds fragment.
2. **The crest is broken.** The top has been exposed longest and is attacked
   from above and both sides, so pluck probability rises with height and the
   skyline steps down instead of sitting flat.
3. **Exposed edges are worn.** Bevel width scales with how proud and how high
   a block sits; sheltered blocks under the lintel stay crisp. This *is* the
   wear-geometry gate — detail survives in recesses because that is where the
   weather could not reach.
4. **The debris is still there.** Plucked blocks did not vanish, they fell.
   They return as talus at the foot, tumbled, heavily rounded and half-buried
   — which also supplies the feathered, dig-stable buried edge the BIO gate
   wants.

### The overcorrection, recorded

First attempt read "survived" as "mostly destroyed": blocks fell from 47 to
22, `B5_marl_parting` was erased entirely, and the piece became floating
fragments. **A survivor's resistant core stays continuous** — what goes is the
periphery, the soft beds and the crest, not the mass itself.

Fixes: pluck probability capped at 0.30, crest attack softened from
0.42·hf^2.4 to 0.20·hf^3.0, block lengths narrowed to 0.55–2.10 × spacing, a
1.03 overlap factor so courses stay welded, and a hard rule that **no bed may
lose more than a quarter of its blocks**. A vanished bed destroys the stack
story, which is the one thing the whole design rests on.

Result: 34 wall blocks, every bed populated, 8 plucked and 8 landed as talus.

### DOCTRINE #1 STOP

> *"Never art-direct a bot past two iterations — reframe the job as
> engineering."*

Appearance has now been iterated more than twice in one session. Per doctrine,
further look-tuning by a machine is out of bounds — that is exactly the road
to Law 2. The machine's deliverables are done: stack, wall, voids, openings,
proven connectivity, block anatomy, talus placement, wear scaling. **The look
belongs to Isaiah's hands from here.**
