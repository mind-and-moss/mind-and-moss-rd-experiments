---
name: parallel-research-dispatch
description: Use before opening a heavy tool (FreeCAD, Blender, the soldering iron) when there's external research that should inform the work. Fork a research agent in the background while you continue integrating other context, then synthesize when the agent returns. Saves 30+ minutes per session vs sequential research.
---

# Parallel research dispatch

When Isaiah is about to start a new tool-heavy phase (FreeCAD modeling, hardware build, etc.), there's almost always external research that should land *before* he opens the tool — what's changed in the latest version, what other people in the space have tried, what the gotchas are. Doing that research sequentially while Isaiah waits is wasteful. Forking a background agent makes the research happen in parallel with other work.

## When to dispatch

Trigger conditions:
- Isaiah says he's about to use a tool you don't have deep knowledge of (FreeCAD 1.1, Bambu A1 Mini-specific tolerances, specific bicycle freewheel models)
- A decision is about to lock that depends on data you don't have (belt crown depth, gear stress in a specific material, CFM for dust extraction)
- Isaiah says "go figure it out yourself" or "use your vast inventory"

Don't dispatch:
- For things you can answer from existing repo content
- For decisions Isaiah said he'd answer himself
- When the user is waiting and there's no other work to do (just do it inline)

## How to brief the agent

The agent has zero context — write the brief like you're handing the question to a senior consultant who walked into the room cold.

**Required in the brief:**
1. Who Isaiah is (Python beginner, Blender-comfortable, both-chefs dynamic)
2. The brand context (Mind and Moss, biotope fidelity, "how the fuck did they make that")
3. Specific constraints (Bambu A1 Mini 180×180×180, PETG, 304 stainless inventory)
4. The exact deliverable shape — word count cap, format, what sections you want
5. What to NOT do (don't write code, don't edit repo files, just return the report)

**Required output spec:**
- Word count cap (~600 words is good for synthesis)
- Concrete and specific ("not 'consider using parameters' but 'create a Spreadsheet with these specific cells: belt_length, drive_pulley_dia...'")
- Cite sources with URLs

The dispatch I made for FreeCAD 1.1 readiness is a working template — see the prompt in `tooling/bike-powered-grinder/sessions/` history if needed.

## What to do while the agent runs

Don't sit and wait. The whole point of `run_in_background: true` is parallelism. Use the time to:
- Commit other work that was in flight
- Update the SESSION-HANDOFF
- Write the open-questions file
- Tidy a docs folder

When the agent completes, you'll get a notification. Pick the work back up then.

## Synthesizing the result

When the agent returns:

1. **Save the raw research as a citable doc** — usually `<feature>/research/<topic>.md`. Include the date, source ("background research agent dispatched on YYYY-MM-DD"), and the convention note that this is external-research-synthesis (not a verbatim thread excavation).

2. **Distill the actionable bits** — what does Isaiah actually need to do/decide based on this research? Pull those into the open-questions file or the README, with citations back to the research doc.

3. **Surface conflicts you spotted** — research often catches inconsistencies in the locked spec that nobody noticed. Flag these in the response to Isaiah. (See `conflict-detection-on-lock/SKILL.md`.)

4. **Don't repeat the research verbatim in your response to Isaiah.** Surface 5-10 high-leverage takeaways. The full doc is in the repo if he wants to dig in.

## Picking the agent type

- **`general-purpose`** — default; good for synthesis tasks where the agent might need to read multiple sources and weigh tradeoffs
- **`Plan`** — when you need an implementation strategy, not just research
- **`Explore`** — narrow read-only search; use when target is "where is X defined / which files reference Y"

For FreeCAD 1.1 readiness, `general-purpose` was right. The agent needed judgment about what mattered.

## What NOT to do

- **Don't dispatch and then sit idle.** Use the parallel time.
- **Don't pre-write the answer in your brief.** That's not research, that's confirmation bias. Let the agent come back with what it actually finds.
- **Don't paste the agent's full output to Isaiah.** Synthesize and link.
- **Don't dispatch multiple redundant agents.** If two agents would investigate overlapping territory, merge into one brief.
- **Don't dispatch for things Isaiah explicitly said he'd answer.** That's about respecting his role, not just efficiency.
