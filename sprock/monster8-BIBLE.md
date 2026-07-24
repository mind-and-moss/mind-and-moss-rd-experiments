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
