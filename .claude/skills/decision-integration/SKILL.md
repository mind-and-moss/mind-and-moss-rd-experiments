---
name: decision-integration
description: Use after pulling a voice transcript into the repo (see mobile-voice-pickup). This skill turns verbatim source material into committed repo changes — README updates, decision lineage, open-questions punch list — while preserving the source so the lineage stays auditable.
---

# Decision integration

Voice transcripts are messy. Repo files are tidy. The problem this skill solves: how do you migrate decisions from one to the other without losing the reasoning that produced them?

## The core principle

**Verbatim source is permanent. Distillation is mutable.**

Source transcripts go into `sessions/` and never get edited. Distilled documents (README, open-questions, decisions-pending) get rewritten freely as decisions evolve, *because* the source is preserved separately. This is the same pattern the repo uses for `Source: RESEARCH-XXX Thread N` headers in topic notes.

## Sequence

### 1. Read the transcript fully

Don't skim. The decisions you're integrating may be implicit ("I'm not a fan of springs") rather than explicit ("decision: no springs in tensioner"). You need the full context to capture them as locked.

### 2. Build a working list of decisions

For each, capture:
- **What was decided** (the locked spec)
- **Why** (the reasoning Isaiah or Claude offered)
- **What was rejected** (the alternatives considered and why they lost)
- **What changed** vs. prior state

Rejections matter as much as decisions. Future-Isaiah needs to know "we considered springs and rejected them because..." so the question doesn't reopen six weeks later.

### 3. Reconcile against existing repo state

Check what's already in the repo for the topic. If a previous README says "2x48 or 2x72 belt" and the new transcript locks "2x72," the README is now wrong. Note the supersession explicitly:

> Where this README disagrees with the original handoff, **this README wins** — the Phase 0 review supersedes.

This phrase (or equivalent) belongs in the README itself, not just the commit message. It tells future readers which version is authoritative.

### 4. Detect conflicts in newly locked decisions

Run a math/logic cross-check before committing. See `conflict-detection-on-lock/SKILL.md` — but the short version: when several specs cluster around a single physical system, multiply the values together and see if the result matches.

The Phase 0 review locked: 75 RPM cadence, 8:1 reduction, 750 RPM belt. But 75 × 8 = 600, not 750. **Catch this kind of inconsistency now, while integration is happening, not after FreeCAD geometry locks.** Surface it in the open-questions file and flag it in the commit message.

### 5. Write three artifacts

For a major decision drop, three files get touched:

**README.md** — current locked spec, reads top-to-bottom as the canonical state. No history, no rejected alternatives mentioned in the body. Brief notes ("X was considered and rejected because Y") go inline next to the decision they relate to.

**open-questions.md** — what's still unanswered, split by who needs to answer (Isaiah vs Claude Code research). Tag with priority. Include a "Resolved" section at the bottom listing decisions that are now closed, so they don't reopen.

**sessions/`<date>`-`<topic>`.md** — verbatim transcript, untouched. This file is the receipt.

### 6. Commit message structure

The commit message is the change-log. Future-you will read commit messages to figure out what happened in a session. Make it useful:

```
<short title>: <one-line summary>

<short paragraph explaining the source — which voice session, what date>

<bulleted list of decisions locked, in the form: 'X locked (Y rejected on grounds Z)'>

<bulleted list of files changed and what each represents>
```

Example pattern that worked for the Phase 0 review:

```
Phase 0 review integration: lock 14 decisions from mobile voice session

Integrates the 2026-05-07 mobile voice session ("Bike-powered grinder Phase 0
review") into the bike-grinder branch.

New decisions locked (Phase 0 review supersedes the earlier ranges):
- Belt: 2x72 SiC locked (2x82 rejected on supply chain; 2x48 rejected on platen length)
- Layout: horizontal — belt runs in horizontal plane, glass approached at top edge
- ...

Files:
- README.md: rewritten to reflect locked v2 spec; preserves decision lineage
- open-questions.md: new — punch list for Isaiah and Claude Code research
- sessions/2026-05-07-mobile-phase-0-review.md: full transcript preserved
```

### 7. Push to feature branch

This work belongs on the feature branch (e.g., `tooling/bike-powered-grinder`), not the meta branch. Other branches will pick it up via merge or rebase later.

## What NOT to do

- **Don't paraphrase Isaiah's words in the README.** If a phrasing is distinctive ("how the fuck did they make that"), preserve it.
- **Don't drop rejected alternatives without explanation.** "We considered X but rejected it" is more useful than silently picking Y.
- **Don't auto-resolve a conflict you spotted.** Flag it, don't pick. Isaiah's the source of truth on his own intent.
- **Don't commit before reading the transcript end to end.** You will miss things buried in casual exchanges.
- **Don't edit the source transcript.** Even formatting fixes risk drifting from what was actually said.
