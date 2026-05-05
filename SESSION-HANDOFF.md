# Session Handoff — 2026-05-05

**For:** Next Claude Code session (or other AI helping Isaiah)
**From:** Session 4 — Reorg merged, references built, ecosystem deep-dives, decisions consolidated
**Read this before doing anything else.**

This file replaces the prior Session 3 handoff. The Session 3 content (R005 excavation, original reorg PR opening) is preserved in the "What Already Happened (Sessions 1–3)" section below.

---

## Where Things Stand Right Now

### 5 PRs open, awaiting Isaiah's review/merge
- **[PR #1](https://github.com/mind-and-moss/mind-and-moss-rd-experiments/pull/1)** — Reorganize findings into topic folders + create `references/` folder. Foundation for everything else.
- **[PR #2](https://github.com/mind-and-moss/mind-and-moss-rd-experiments/pull/2)** — `setup.md` at repo root. Materials, machines, stores, DIY backlog. Tables empty, ready for Isaiah to fill.
- **[PR #3](https://github.com/mind-and-moss/mind-and-moss-rd-experiments/pull/3)** — Auto-improvements: bond-line spec verification (corrected R004 T15's flagged "from another bot" specs against Norland NOA datasheets, DOWSIL guides, ASTM standards), references TODO chase (~80 verified URLs added), `the-gem/build-sequence.md` 9-phase draft, full editorial review surfacing 5 real contradictions. Depends on PR #1.
- **[PR #4](https://github.com/mind-and-moss/mind-and-moss-rd-experiments/pull/4)** — Three new ecosystem deep-dives in `topics/ecosystem/`: `soil-chemistry.md`, `microorganisms.md`, `decomposers.md`. External research synthesis with peer-reviewed citations.
- **[PR #5](https://github.com/mind-and-moss/mind-and-moss-rd-experiments/pull/5)** — Walstad method + Father Fish method files in `topics/ecosystem/`. External research synthesis. Identifies Father Fish as Lou Foxwell Jr. (the "Earl Grey" alias was unverified).

PRs #1, #2, #4, #5 are independent of each other. PR #3 depends on #1. Recommended merge order: 1 → 3 → 2 → 4 → 5 (or any after #1+#3). See `decisions-pending.md` for the full merge-order question.

### Decisions awaiting Isaiah's judgment
**`decisions-pending.md` at repo root** consolidates 13 open calls — engineering specs, scope/product-shape, and process/workflow. Each has options, trade-offs, Claude's recommendation, and what committing requires. **This is the single doc to share with another AI bot for a second opinion** — don't have other bots try to read the whole repo.

The most decision-forcing ones, in priority order:
1. **The Gem's seam type** (UV optical adhesive vs cosmetic silicone vs structural silicone) — gates the grinder design and the entire fabrication pipeline. Claude's rec: UV optical adhesive (NOA 65 for soda-lime, NOA 148 for borosilicate).
2. **The Machine's variant** — open-air, sealed, or both? Claude's rec: open-air for v1.
3. **The Gem's base material** — mycelium, concrete, or hybrid? Claude's rec: hybrid for v1, full mycelium for v2.

### What's actually still in someone's head, not in the repo
- **Materials inventory** — `setup.md` exists but tables are empty. Isaiah said he'd fill it in when home.
- **Physical prototype status** — none yet. Everything is paper plans. The bond-line spec verification is done; the grinder design and first build are still pending.
- **The Machine's wall material** — not yet decided (1mm acrylic is too thin per R005 T16; `structure.md` describes the segmented approach but hasn't picked a thickness/grade).

---

## What Already Happened (Sessions 1–3)

### Excavation pipeline
- **Claude.ai:** complete (R001–R004, Threads 1–15)
- **ChatGPT:** complete (R005, Threads 16–30)
- **Third AI (phone-based):** still pending. Isaiah needs to figure out the data pipeline.

### Repo structure — fully migrated
The 5 RESEARCH-XXX excavation files are now reorganized into topic folders. Original verbatim files preserved under `findings/archive/`. The migration was done in two phases (R001–004 in PR #1's branch, R005 directly on main by the parallel session, then merged into PR #1's branch).

### 5 product candidates surfaced from R005
Each now has a stub or full file in `findings/concepts/`:
1. **DIY canister filter** (R005 T18) — 5-gal bucket + 3D-printed lid, "0 leaks" pitch
2. **Biome cartridge multi-environment chassis** (R005 T17) — 4 sealed biomes in one outer shell
3. **Concrete aquarium-furniture column** (R005 T24) — `concepts/concrete-pillar.md`
4. **Sealed planter box** (R005 T25) — resin-sealed planter
5. **Styrofoam-box vivarium chassis** (R005 T27) — large-format cheap construction

### Strategic insight (still load-bearing)
Mind and Moss **cannot beat Amazon at scale via 3D printing** — Amazon sellers use injection molding at $3-6/unit after $3-20K tooling. Mind and Moss must compete on differentiation, quality, customization, and brand voice — boutique end of the market. (R005 Thread 18.)

---

## Working Setup

### Local clone
- Path: `C:\Users\Isaia\OneDrive\Desktop\Claude c\Sessions\mind-and-moss-rd-experiments`
- Use this instead of the GitHub web editor — 10x faster
- File operations via Read/Write/Edit, git operations via Bash

### Tools installed
- `git` CLI: `C:\Program Files\Git\cmd\git.exe`
- `gh` CLI: installed and authenticated as `bread646464` (carries forward across sessions)

### Author identity (must pass per-commit)
Git config isn't set globally. For commits, use:
```
git -c user.name="bread646464" -c user.email="yourbestbuddy2004@gmail.com" commit -m "..."
```

### Branch coordination (CRITICAL if working in parallel with another session)
This local clone is shared between sessions. Branch switches are visible across sessions. **Protocol:** always start any work block with `git checkout <your-branch>` to be defensive. During Sessions 3 and 4, the bot caught multiple branch flips caused by parallel session checkouts and self-corrected each time.

---

## Files State (current)

### On `main`
- `findings/RESEARCH-001..005-*.md` — moved into `findings/archive/` after migration
- `findings/{products,concepts,topics,business}/` — full topic structure populated with R001–R005 content
- `findings/topics/ecosystem/` includes new external-research files (`soil-chemistry.md`, `microorganisms.md`, `decomposers.md`, `walstad-method.md`, `father-fish-method.md`) once PRs #4 and #5 merge
- `findings/references/` — external/curated sources mirroring `topics/`, `products/`, `concepts/` (once PR #1 merges)
- `findings/products/the-gem/build-sequence.md` — 9-phase draft (once PR #3 merges)
- `findings/EDITORIAL-REVIEW-2026-05-05.md` — advisory review (once PR #3 merges)
- `setup.md` — at repo root (once PR #2 merges)
- `decisions-pending.md` — at repo root (this branch — once merged)
- `SESSION-HANDOFF.md` — this file
- `CLAUDE.md` — project context (Mind and Moss vision, working style)
- `README.md`

### On open PR branches
- See "5 PRs open" section above.

---

## Next Session — Recommended First Moves

### Highest priority
1. **Merge the open PRs** in the order: 1 → 3 → 2 → 4 → 5. After PR #3 merges, the bond-line correction is in main.
2. **Have Isaiah make the seam-type decision** — see `decisions-pending.md` Decision #1. This gates the grinder design.
3. **Apply the editorial review's clarification edits** — `decisions-pending.md` Decision #12, five small edits across existing files. Low risk, high readability gain.

### Medium priority
4. **Have Isaiah fill in `setup.md`** with materials, machines, stores, DIY backlog. Enables the "what can I start today" question.
5. **Phone-AI excavation** — still pending. Ask Isaiah which AI it is and what pipeline he wants (export? screenshots? voice transcription?).
6. **Promote the "two-anchor-plant SKU" decision** from `topics/ecosystem/plants.md` into `business/product-categories.md` if Isaiah confirms.

### Lower priority but worth surfacing
7. **Start an instrumented prototype build** for the pH-drift / NO₃ / DO research opportunity flagged in PRs #4 and #5. **Genuine original-data publishing opportunity** for Mind and Moss — the kind of thing that becomes a brand asset.
8. **Develop one of the five concepts to working prototype** — likely biome cartridge or canister filter.

---

## Key Context About Isaiah (carries forward)

- Name: Isaiah
- GitHub: `bread646464`
- Email: `yourbestbuddy2004@gmail.com`
- Business: Mind and Moss (`github.com/mind-and-moss`)
- Brand: "how the fuck did they make that"
- Skills: Blender (comfortable, since Jan 2025), Python (complete beginner), FreeCAD (future)
- Working dynamic: both chefs — Isaiah brings vision, Claude builds alongside him
- **Considering switching from Blender to Plasticity** for CAD-style precision modeling (R004 Thread 13)
- Tools available: 3D printer (Bambu Lab), xtool laser cutter, glass cutting tools + grinder, stained glass equipment, hardware-store materials, 68oz square deli containers (~30 of them), ~40 wild-caught Armadillidium vulgare isopods (Fresno), starter Giant Canyon isopods (12), Heartleaf Philodendron and various mosses
- **Setup status:** no dedicated workshop space yet — `setup.md` is a "current floating configuration" doc, not a fixed workshop inventory

## Plan Mode + Subagents Are In Play

- Earlier in Session 3, plan mode was used to design the topic-folder reorganization. The plan file lives at `C:\Users\Isaia\.claude\plans\elegant-rolling-horizon.md` (local to this machine, not in repo).
- Throughout Session 4, multiple background research agents were dispatched in parallel for: bond-line verification, references TODO chase, build sequence drafting, soil chemistry / microbes / decomposers research, Walstad / Father Fish research. All returned with cited primary sources.
- Two parallel Claude sessions (excavation + reorg) were active during Session 3. As of Session 4, only the reorg session is active. If both resume, coordinate via the branch-checkout protocol above.

---

## Memory persistence

Outside the repo, Claude maintains user/project/feedback memory at:
`C:\Users\Isaia\.claude\projects\C--Users-Isaia-OneDrive-Desktop-Claude-c-Sessions\memory\`

Includes notes on Isaiah's role, Mind and Moss business context, the both-chefs working dynamic, the R&D repo branch protocol, the R&D repo state (this file is the source of truth for state), and the video-watching division of labor (Isaiah watches, Claude catalogs).
