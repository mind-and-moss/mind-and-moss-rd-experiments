# MONSTER8 — SESSION 7 HANDOFF

Read in this order. Everything is on branch
`claude/sprock-monster8-blockout-rp25w3` (PR #10).

1. **`THE-STORY.md`** — the geological history. Seven episodes plus the
   conformance audit. This governs everything else.
2. **`SCULPT-BY-NUMBERS.md`** — thirteen numbered zones, what each surface *is*
   and what happened to it, plus an order of work.
3. **`GATE-RESULTS.md`** — every gate, measured, with the bugs each one caught.
4. **`monster8-BIBLE.md`** — consolidated doctrine, laws, ledger, build order.

## The build chain

| Script | Does |
|---|---|
| `structure_story_conformant.py` | **the current build.** Beds → joints → laminae → derived features → cleanup → talus |
| `preview_remesh_displace.py` | canon pipeline: remesh, then displacement last, preview only |
| `validate_gates_final.py` | base / wall / sealed pockets / per-layer connectivity |
| `validate_cave_passability.py` | 3D flood fill, mouth → tail, narrowest constriction |
| `derive_segmentation.py` | print pieces, seams on joint planes, peg count |
| `diagnose_thin_walls.py`, `diagnose_nonmanifold.py`, `diagnose_objects.py` | fault-finding |
| `print_prep_morph_open.py` | minimum-feature attempt — **does not fully work**, kept as a record |

Earlier scripts (`script01`–`script10`, `structure_outcrop.py`,
`structure_mature.py`) are superseded but kept: each carries a recorded failure.

## Where it stands

**Passing:** flat base, sealed pockets = 0, per-layer solid connectivity,
manifold = 0 after remesh, mouth → tail flow-through, 13 features derived and
0 hand-placed.

**Not passing:** 7 wall samples of 2163 under 1.2 mm — knife-edges where a
cutter runs tangent to a bed outline. Three separate causes were found and
fixed; this is the residue.

**Open judgement calls, all Isaiah's:**
- **8.3 litres of displacement** — real water volume in a tank.
- **18 pieces, ~99 pegs** at 420 mm. A serious assembly job, driven entirely by
  the size choice.
- **Headroom 30.9 mm** in the chamber — clears the fish it is sized for, with
  little margin.

## What the next session should NOT redo

- Displacement along normals does not produce a cave mouth.
- Voxel remesh does **not** remove sub-minimum features; it reproduces them.
- Morphological opening by normal displacement is not a true offset.
- A bed may legitimately split into several components — that is a pillar.
  Judge connectivity per **print piece**, never per bed.
- Vertex adjacency cannot see face-to-face contact between separately built
  beds. Use voxels.
- `str.replace` with a stale anchor **fails silently**. A rewrite once deleted
  the boolean-apply loop and the restore patch matched nothing, so no boolean
  ran and 25 cutters rendered as solid rock. Verify code is present before
  running it.

## The one thing still unbanked

`monster8_blockout.blend`, `sprock-knowledge/`, `erosion_rock`, the BLENDER
TRAPS list and `blender-limestone-playbook.md` remain in a local outputs folder
unreachable from any remote session. This has now blocked a remote session
twice. **Bank them or it happens a third time.**
