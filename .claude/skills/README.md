# Mind and Moss — Claude Code Skills

Reusable patterns extracted from the multi-session arc that built out this repo. Each skill is a tight playbook a future Claude Code session can invoke (via the Skill tool) or read as a reference.

The skills split into three buckets:

## Workflow / pipeline patterns
Things I do across sessions to move work forward.

- **[mobile-voice-pickup](mobile-voice-pickup/SKILL.md)** — pull a Project Claude voice chat from claude.ai into this repo via Chrome MCP
- **[decision-integration](decision-integration/SKILL.md)** — turn a voice transcript into committed repo changes while preserving full lineage
- **[parallel-research-dispatch](parallel-research-dispatch/SKILL.md)** — fork a research agent before opening a heavy tool, so Isaiah arrives at a readiness packet
- **[conflict-detection-on-lock](conflict-detection-on-lock/SKILL.md)** — math/logic cross-check on freshly locked decisions before they ossify in CAD geometry
- **[freecad-headless-pipeline](freecad-headless-pipeline/SKILL.md)** — drive FreeCAD 1.1 macros via `freecadcmd.exe` without GUI; idempotent macro pattern, Sketcher constraint API, VarSet expression syntax (added Session 6)

## Communication discipline (talking to Isaiah)
Things I do *during* a turn to stay connected.

- **[isaiah-communication-profile](isaiah-communication-profile/SKILL.md)** — the meta-skill: how Isaiah communicates and what works
- **[one-question-at-a-time](one-question-at-a-time/SKILL.md)** — voice-mode-friendly questioning: ask exactly one thing, no lists
- **[length-discipline](length-discipline/SKILL.md)** — when to hard-cap response length to prevent tune-out
- **[decision-mode-when-trusted](decision-mode-when-trusted/SKILL.md)** — when Isaiah delegates a call, actually make it; don't bounce it back

## Why these exist

Across the first five sessions, a lot of stalls weren't *technical* — they were communication failures. I dumped walls of text Isaiah skimmed. I asked five questions when one would do. I missed paradigm shifts buried in casual language. I asked permission for things he'd already delegated.

These skills capture the patterns that worked so we don't relearn them every session. They are project-specific (calibrated to Isaiah, not generic), and they are *opinions* — descriptive of what we've found works in practice, not abstract best-practices.

When a new session begins, the relevant skill should be invoked at the moment its trigger condition appears (described in each SKILL's `description` field), not preemptively dumped at session start.
