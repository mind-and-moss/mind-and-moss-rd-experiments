# Session Handoff — End of Session 7 (2026-05-09)

**For:** Next Claude Code session (or any AI / collaborator picking up this repo)

**Scope:** project-wide state — PRs, mechanical spec lock-ins, open product decisions, repo conventions. **For the FreeCAD pipeline (active build target), load
[`tooling/bike-powered-grinder/freecad/CONTEXT.md`](tooling/bike-powered-grinder/freecad/CONTEXT.md) instead of this file** — it supersedes the FreeCAD-specific sections that used to live here.

**From:** Session 6 locked the bike-grinder Q1–Q4 readiness gates and built the FreeCAD parametric pipeline (macros 01–03, `Grinder_Params.FCStd`). Session 7 verified parametric bindings end-to-end and shipped macro 04 (shaft position locks + computed chain center distances).

---

## TL;DR for the next bot

1. **Bike grinder is the active build.** Tooling, not product — but held to brand standard. Prerequisite for The Machine's gem-component glass panels and all future Mind and Moss products that use precision-cut glass.
2. **Q1–Q4 readiness gates locked** (Q1: math, Q1b: drivetrain architecture, Q2: design envelope, Q3: donor bike spec, Q4: frame architecture). See locked-decisions table below.
3. **FreeCAD pipeline is live and verified.** Macros 01–04 shipped, parametric bindings proven end-to-end. Details: `tooling/bike-powered-grinder/freecad/CONTEXT.md`.
4. **Next CAD move:** macro 05 — assembly-level part split, drive pulley first.
5. **Donor bike still not acquired.** Blocks physical assembly (not CAD).

---

## Locked mechanical spec

Spec stack as of end-of-Session-7 (locked, won't reopen unless physical testing forces it):

| Locked | Value | Source |
|---|---|---|
| Belt | 2x72 silicon carbide, 120–1000 grit (Sackorange 6-pack) | Phase 0 review |
| Platen | 22" usable, glass-only, single-purpose | revised in Q2 |
| Drive pulley | 6" crowned PETG with stainless rod hub | revised in Q2 |
| Idler pulley | 3" crowned PETG with stainless rod hub | revised in Q2 |
| Layout | horizontal, glass at top of belt | Phase 0 |
| Operator | seated rider position | Phase 0 |
| Workpiece fixture | rail-guided sled with full-width straight-edge pusher | Phase 0 |
| Tensioner | screw-driven, no springs, by-feel tuning | Phase 0 |
| Cadence target | 75 RPM (conversational) | Phase 0 |
| Belt RPM target | 750 RPM | Phase 0, confirmed Q1 |
| Total ratio | **10:1** (1180 SFM, upper-glass-spec) | Q1 — Isaiah picked over 7.5:1 to honor 600–750 RPM range from client research |
| Drivetrain | two chain stages | Q1b (option A) — single-stage and internal-hub both rejected |
| Stage 1 | 42T donor steel chainring × 13T donor steel cog (3.23:1) | corrected stress analysis |
| Stage 2 | 25T PETG large × **machined-metal 8T pinion** (3.125:1) | corrected stress — PETG fails fatigue at 8T at this load |
| Bearings | 2× 6202-2RS (intermediate, 15mm bore) + 2× 608-2RS (grinder shaft, 8mm bore) | corrected stress |
| Chain | 2× KMC Z8.3 (1/2" × 3/32" bicycle), ~$15/each | corrected stress |
| Coolant | drip line above platen, gravity catch tray below | Phase 0 |
| Hardware | stainless bolts right-sized per joint, M5 baseline | Phase 0 |
| Frame | portable 3-module: rider / drivetrain bridge / grinder | Q4 |
| Frame construction | hand-cut metal tube + 3D-printed PETG joint nodes with heat-set inserts | Q4 |
| Door clearance | 30" (modules fit through any interior door) | Q4 |
| Donor bike | 7+ speed MTB, ~$40 from Facebook Marketplace | Q3 |
| Shaft positions (CAD) | intermediate (0, 500), crank/BB (0, 1100) — chain CDs 600/500 mm | Session 7 macro 04 default |
| **HARD CONSTRAINT** | **18" max glass edge on any Mind and Moss panel** | Q2 — `findings/design-constraints.md` |

Total bought-parts cost beyond donor bike: **~$73** (chains + bearings + machined pinion + intermediate shaft stock).

---

## Math errors caught (project-wide pattern)

Three errors caught and corrected across Sessions 6–7 (the `conflict-detection-on-lock` skill captures this pattern):

1. **Phase 0 review's locked specs didn't multiply** (S6). 75 cadence × 8:1 = 600, not the 750 RPM target also locked. Isaiah picked Path B → revisit 10:1.
2. **First sprocket stress agent had directional error** (S6). Treated speed-up gearbox as torque-multiplying reduction. Real: torque flows pedal → belt with magnitude *decreasing* (19.1 N·m at crank, 1.91 N·m at belt pulley). Re-dispatched with corrected torque chain.
3. **Quantity-vs-float unit mismatch in verify script** (S7). PropertyLength returns an `App.Quantity` carrying units; treating it as a float crashes arithmetic. Fix: coerce via `.Value` before subtracting/dividing. Lesson now in `freecad/CONTEXT.md`.

**Use the `conflict-detection-on-lock` skill before committing any newly-locked decision.**

---

## PRs open (9 total)

| PR | Branch | What it carries | Recent changes |
|---|---|---|---|
| #1 | `reorg/topic-folders` | Foundation reorg + references/ | none |
| #2 | `setup/inventory` | `setup.md` voice-dictation inventory | none |
| #3 | `auto/improvements` | Bond-line spec verification, editorial review | none |
| #4 | `research/ecosystem-microbiology` | soil-chemistry, microorganisms, decomposers | none |
| #5 | `research/aquarium-methods` | Walstad + Father Fish methods | none |
| #6 | `meta/decisions-and-handoff` | decisions-pending + this SESSION-HANDOFF | **handoff trimmed + refreshed in S7** |
| #7 | `fix/gem-as-machine-component` | Gem-as-component restructure | none |
| #8 | `tooling/bike-powered-grinder` | Phase 0 spec, FreeCAD pipeline, design-constraints, sessions, macros 01–04, CONTEXT.md | **S7: macro 04, verify_parametric_binding.py, freecad/CONTEXT.md, README updates** |
| #9 | `meta/skills-and-patterns` | 8+ reusable skills | (S6 added `freecad-headless-pipeline`) |

**Recommended merge order:** 7 → 1 → 3 → 2 → 4 → 5 → 6 → 8 → 9. PR #8 is the highest-density branch.

---

## Open items for Isaiah

### Critical (blocks downstream work)

- **Find a donor bike.** Facebook Marketplace, $20–40, 7+ speed MTB. Pre-purchase checklist in `tooling/bike-powered-grinder/open-questions.md`. Blocks physical assembly (not CAD progress).

### Important (drives detail design but not blocking)

Listed in `tooling/bike-powered-grinder/open-questions.md`:
- Coolant routing (tray material, pump vs gravity drain)
- Belt tracking adjustment range
- Module joint mechanism (wing-nut vs cam vs over-center latch)
- Module dimensions / weight target
- 8T machined pinion source (SDP-SI? Boston Gear? Local shop?)
- Workshop reality check (where does it live?)

### Nice-to-lock-early

- Material color / aesthetic palette
- Belt change time target (drives quick-release tensioner complexity)

### Stack of 13 product-level decisions still pending

In `decisions-pending.md` at repo root. Most decision-forcing:
- Decision #1: gem-component seam type (UV optical adhesive vs structural silicone) — gates The Machine's manufacturability
- Decision #5: Machine total water volume + livestock spec — blocks geometry locks
- Decisions #2, #4, #7 — cluster around concrete base material + form factor

These are PRODUCT decisions, not tooling. Bike grinder progress doesn't unblock them. They need their own session.

---

## What's next

**FreeCAD side:** macro 05 — assembly-level part split. First per-part `.FCStd` file App-Linked to `Grinder_Params.FCStd`. Drive pulley first. Generate STL. **All FreeCAD pipeline state, patterns, and gotchas live in `tooling/bike-powered-grinder/freecad/CONTEXT.md`** — load that file for the CAD work.

**Physical side:** acquire donor bike → harvest steel chainring + cassette cog + crank/BB → first physical print of drive pulley → bench load test under pedal torque.

**Product side:** stack of 13 pending decisions in `decisions-pending.md`. Independent of tooling.

---

## Working patterns (project-wide — distilled across sessions)

If you're picking this up cold, the working pattern that's settled in:

1. **Read this handoff first** for project-wide state. **Then load `freecad/CONTEXT.md`** if your work touches the FreeCAD pipeline (it supersedes this file for that domain).
2. **Use the skills.** They're calibrated to this project, not generic. Especially `isaiah-communication-profile`. (Branch: `meta/skills-and-patterns`.)
3. **Sanity-check agent math.** Multiple sessions caught directional / unit / multiplication errors. Cross-check against physical reality before accepting.
4. **Commit often, push often.** Each meaningful change = one commit + push.
5. **One question at a time when Isaiah's voice-mode or scattered.** He'll explicitly say "let's go one by one" — that's the strongest signal.
6. **When Isaiah says "I trust your opinion"**, decide. Don't bounce the question back. Document the reasoning.
7. **PowerShell `Start-Process -Verb RunAs -Wait`** for elevated installs from automation. Bash-invoked silent installs with /S are unreliable on Windows.

---

## Index of files referenced in this handoff

- `tooling/bike-powered-grinder/freecad/CONTEXT.md` — **FreeCAD pipeline pickup doc (load this for CAD work)**
- `tooling/bike-powered-grinder/README.md` — v3 locked grinder spec, 14 design decisions
- `tooling/bike-powered-grinder/open-questions.md` — punch list
- `tooling/bike-powered-grinder/sessions/` — voice transcripts + Session 6 detail log
- `tooling/bike-powered-grinder/research/sprocket-stress-corrected.md` — drivetrain math
- `findings/design-constraints.md` — top-level hard constraints (18" glass edge)
- `decisions-pending.md` — 13 product-level decisions awaiting Isaiah
- `unknowns-audit.md` — 108 open questions in 15 categories (on `audit/full-unknowns-pass`)
- `.claude/skills/` — reusable patterns (on `meta/skills-and-patterns`)
- `CLAUDE.md` — brand context
- `setup.md` — material inventory baseline
