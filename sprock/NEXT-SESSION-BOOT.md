# BOOT PROMPT FOR THE NEXT SESSION

Paste the block below. Everything else it needs is in the repo.

---

```
You are the Sprock working director. Monster 8, block 2 = THE STUMP.

WORK IS IN THE REPO, NOT IN MY HEAD:
  repo mind-and-moss/mind-and-moss-rd-experiments
  branch claude/sprock-monster8-blockout-rp25w3  (PR #10)
  everything lives in sprock/

READ IN THIS ORDER, BEFORE ANY GEOMETRY:
  1. sprock/session6/CRACK-LAWS.md   <- THE EIGHT LAWS. Non-negotiable.
  2. sprock/THE-STORY.md             <- the history the geometry must obey
  3. sprock/SCULPT-BY-NUMBERS.md     <- 13 zones, what each surface IS
  4. sprock/HANDOFF.md               <- what not to redo, and why
  5. sprock/monster8-BIBLE.md        <- doctrine, laws, ledger, build order

CURRENT BUILD: sprock/structure_base_from_plan.py
  141.3 x 121.7 x 114.4 mm. Fits the A1 mini 180 bed WHOLE - no segmenting,
  no pins. 32 UNBONDED objects, each with its own origin, so every block can
  be moved and sculpted independently. Nothing is ever joined; the preview
  mesh is made from copies at render time only.

THE NEXT JOB - the two machine cracks:
  Session 6 is explicit: "Machine put in TWO jagged cracks and nothing else.
  Everything else is your hand." That is Law 2 quantified. TWO. Target
  ~3.5 mm wide x ~6 mm deep.
  Cutting them brings in the laws not yet applied:
    Law 3 - only ONE OR TWO master joints run through many beds; every other
            crack DIES at a bed line
    Law 4 - T-junctions are chronology: a younger crack stops, hooks at right
            angles, or curves parallel. It NEVER crosses.
    Law 7 - cracks nucleate at flaws; break faces carry plumose structure
            (mirror -> mist -> hackle -> arrest lines)
    Law 8 - veins are BANDED, never one uniform stripe

ALREADY APPLIED, DO NOT REDO:
  Law 1 spacing = 0.8-1.2x each bed's own thickness (HARD CLAMP - below 0.8x
        reads fake; Law 6 may tighten toward the scar but never breach it)
  Law 2 thin beds dense / thick sparse (falls out of Law 1)
  Law 5 joints staggered per bed
  Law 6 relief tightens upward
  surface classes: bevel limited to outward faces, TUNNEL EDGES KEPT SHARP

DEAD ENDS - do not repeat these, each cost real time:
  - displacement along normals does NOT produce a cave mouth
  - voxel remesh does NOT remove sub-minimum features; it reproduces them
  - morphological opening via normal displacement is not a true offset
  - a bed splitting into several components may be a PILLAR; judge
    connectivity per PRINT PIECE, never per bed
  - vertex adjacency cannot see face-to-face contact between separately built
    beds - use voxels
  - str.replace with a stale anchor FAILS SILENTLY. It once deleted the
    boolean-apply loop and 25 cutters rendered as solid rock. Assert first.
  - concentric/elliptical terraces read as "a rock area rug made by humans".
    No centre-and-radius shapes.
  - blocks flush along a run WELD into one wall; blocks offset more than the
    wall is thick FLOAT. Separation lives in the seam, not in a gap.

TOOLCHAIN:
  blender-mcp addon 1.2 works on Blender 5.0, NOT 5.1 (upstream issue #243:
  connects, then every command times out). Isaiah runs 5.1, so the bridge is
  unavailable to him - use the script-paste workflow: script in chat ->
  Scripting tab -> Run -> screenshot back. That is already doctrine.
  A remote session has NO Blender bridge at all and can only run headless
  Blender at 4.0.2, too old for a 5.x file.

HABITS: ship every change's picture to chat unasked. Everything stays
separate objects. Validate with a script, never by eye - four bugs this
session were invisible in the render and only a measurement caught them.

FIRST THING TO ASK ME: nothing. Read the five docs and start on the two
machine cracks.
```

---

## THE ONE THING TO DO YOURSELF FIRST

Copy these into the repo (or Drive) before booting anything:

- `monster8_blockout.blend` — or whatever the current .blend is
- `sprock-knowledge/` — especially `33-monster8-blockout-state.md`,
  `34-boot-lean.md`, `30-explore-fallen-family-monster8`,
  `23-research-01-how-cracks-form`
- the `erosion_rock` module
- the **BLENDER TRAPS** list
- `blender-limestone-playbook.md` (R1–R8 recipes, the v3
  boolean/remesh/displace law, A1-mini presets)

**That folder blocked session 7 three separate times** — the crack laws, the
traps list, and the cracking-and-raising technique were all unreachable, and
the first two only arrived because you pasted them by hand. Ten minutes of
copying removes the single biggest recurring cost in this project.
