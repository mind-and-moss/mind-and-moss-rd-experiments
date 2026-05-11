# Bike Grinder — Session 10 (Visible Bevel Gears + Ground-Anchored BB Support)

> Paste-ready prompt for a fresh Claude Code session. Do not edit; this is the
> handoff. Authored end of Session 9 on 2026-05-10 by Isaiah + Claude after
> reconciling a voice-mode interpretation drift on belt orientation.

---

## Context: where you're picking up

Mind and Moss R&D repo, branch `tooling/bike-powered-grinder`. Session 9 was just committed at `585ccda` ("collapse drivetrain to one chain + RA bevel; App::Link real parts"). The current FreeCAD assembly has:

- Desk-front layout, school-chair seating (no saddle, bars, wheels)
- Drivetrain: chainring (X-axis) → chain → stage1_cog (X-axis) → `RA_Drive_Placeholder` BLACK BOX → vertical drive shaft (Z) → drive pulley (Z) → belt → idler pulley (Z)
- Belt: vertical face (sanding face perpendicular to desk top, faces the rider in -Y direction). Glass lies flat on the desk and is pushed forward (+Y) so its leading edge meets the belt face. **This is correct ergonomically — do NOT change belt orientation.**
- A `Downtube_Brace` cylinder ties the BB area diagonally back to the back-rail centerline
- `stage2_pinion.FCStd` and `stage2_large.FCStd` exist in `parts/` but are NOT currently in the assembly (they were dropped in Session 9 because the bevel gearbox placeholder replaced them)

## Session 10 — three locked decisions

1. **Belt orientation stays as built.** Vertical face, vertical-axis pulleys. Confirmed via Isaiah's voice description: "the glass pane sits on the table, I sit at the desk, slowly push the glass away from myself and into the straight belt" — that's edge-grinding against a vertical belt face. An earlier voice-mode answer suggested "horizontal belt" but that contradicted this description; the description wins.

2. **BB support: drop the diagonal pole, add ground-anchored support.** Remove `Downtube_Brace` from the assembly. Add a new structural element: a vertical post or column that runs from the BB shell straight down to the floor, planted on a **concrete block**. Isaiah hasn't decided whether the block is bought pre-cast or self-cast in his own mold — design the post-to-block interface so either source works (i.e., a mounting plate at the post bottom that bolts/anchors into the block top). The block top sits on the floor; the BB shell sits at its existing parametric height (`crank_y`, `crank_z` in the world frame).

3. **Restore visible mechanical drivetrain — hybrid approach.** Pull the `RA_Drive_Placeholder` black-box block OUT. Replace with a **visible bevel-gear PAIR** — two real meshing conical gears, modeled as parts (initially as cone-frustum placeholders if proper involute teeth are out of scope this session, but explicitly two gears, not a box). Also **bring `stage2_pinion` and `stage2_large` back into the assembly** as App::Linked parts to provide additional reduction ratio. The drivetrain becomes: chainring → chain1 → stage1_cog (jackshaft, X-axis) → bevel input gear (X-axis) ⟂ bevel output gear (Z-axis) → stage2_large (Z-axis) → chain2 → stage2_pinion (Z-axis, on grinder shaft) → drive pulley. Verify total ratio still hits the locked 10:1 target (`Drivetrain.total_ratio` in `Grinder_Params`).

## Open questions to ask Isaiah BEFORE building (one at a time, voice-mode discipline)

The Session-9 work was load-bearing-decision-heavy and Isaiah's bandwidth for back-and-forth is limited. Stage these so each unblocks the next:

- **Q1 (geometry):** Where does the ground-anchored post stick into the BB? Behind the BB (rider side, post comes up from floor and the BB shell mounts on top), in front of the BB (post on the +Y side of the BB), or directly under the BB axle? Recommend "directly under" — shortest load path.
- **Q2 (bevel gears):** Bevel-gear ratio for this stage? Default suggestion: 1:1 (just turn the corner, do all the reduction in chain stages). If he wants reduction in the bevel stage, what ratio?
- **Q3 (concrete block):** Does Isaiah have a target block size in mind (e.g., standard 8×8×16 cinder block)? If not, propose a default and show how it parameterizes.

DO NOT ask all three at once. Ask Q1, build that piece, then Q2, build, then Q3.

## What "done" looks like for Session 10

- `Downtube_Brace` removed from `MANAGED_NAMES` / not built in macro 08
- New `GroundPost_Brace` + `ConcreteBlock_Anchor` (or similarly named) parametric objects in the assembly, anchored under the BB
- New `parts/bevel_gear_input.FCStd` + `parts/bevel_gear_output.FCStd` (or a single shared part used twice with different placements) — modeled as cone frustums or simple bevel placeholders, App::Linked into the assembly at the position currently occupied by `RA_Drive_Placeholder`
- `stage2_pinion` and `stage2_large` restored to assembly via App::Link, with a second chain loop solid built between them (mirror the Session-9 `add_chain_loop` helper)
- Total drivetrain ratio still computes to 10:1 — surface a console message confirming
- Macro 08 idempotent re-run yields no duplicates
- 18" max glass edge constraint still respected at the platen

## Hard constraints + protocols

- **Branch hygiene:** first action — `git checkout tooling/bike-powered-grinder`, `git fetch`, `git log --oneline -3` to confirm `585ccda` is the head. Parallel Claude sessions share this clone.
- **FreeCAD pipeline:** drive everything via `freecadcmd.exe` headlessly. Macros idempotent. VarSet expression syntax: `<<VarSet>>.prop`. Sketcher constraint API as documented in `tooling/bike-powered-grinder/freecad/CONTEXT.md`.
- **Ask before non-obvious geometric assumptions** — Isaiah explicitly wants to be in the loop on real design calls. Don't guess concrete-block dimensions, post diameters, gear cone angles, or anchor patterns.
- **Voice-mode communication:** terse questions with one-line "why I'm asking" framing. One question at a time. Watch for leading questions that produce unreliable yes/no answers — when geometry is at stake, ask Isaiah to describe the *use scenario* (where he sits, what he holds, how it moves) rather than confirming a yes/no on a geometric framing. (See auto-memory `feedback_isaiah_voice_mode.md` — the geometric-questions section was added end of Session 9 from exactly this kind of drift.)
- **Don't auto-commit.** Confirm with Isaiah before each commit.

## First actions

1. `git checkout tooling/bike-powered-grinder`, verify head = `585ccda`, FreeCAD GUI not running.
2. Open `tooling/bike-powered-grinder/freecad/CONTEXT.md` for FreeCAD pipeline reference.
3. Read `macros/08_build_assembly_layout.py` to understand the Session-9 baseline you're modifying.
4. Ask Isaiah Q1 (post attachment to BB).
