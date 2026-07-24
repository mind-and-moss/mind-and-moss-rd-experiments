# Monster8 — Layer Stack Spec (INPUT, awaiting Isaiah)

**Status:** BLOCKING — unanswered.
**Owner of the answer:** Isaiah. Nobody else gets to fill this in.
**Consumer:** `erosion_rock.STACK_B2` in the Sprock toolchain, scene
`Documents/sprock/out/monster8_blockout.blend`.

---

## Why this file exists

Session 7 booted into a remote container with no Blender MCP bridge and no
vault on disk. The live-scene work could not run. This file captures the #1
blocking input so the answer survives the session and the local PC session
can start from Isaiah's numbers instead of guesses.

**`erosion_rock.STACK_B2` is currently a Claude invention.** It was made up to
get geometry moving in an earlier session. It has no authority. It must be
replaced wholesale by the values below before any further erosion work —
not adjusted, not "tuned toward" the real stack. Replaced.

---

## The questions

### 1. How many layers?
> _(unanswered)_

### 2. Thickness of each, top to bottom
Fill one row per layer. Units: whichever the scene is in — state which.

| # | Layer name | Thickness | Hardness (1 = rots out, 5 = holds) | Notes |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

### 3. Which are the rotten ones?
The soft bands that undercut and collapse — the ones doing the actual erosion
work. Name them by row number above.
> _(unanswered)_

### 4. Hardness ordering
Not just which are soft, but the *contrast* between neighbors. A soft band
under a hard cap behaves differently than a soft band between two soft bands.
> _(unanswered)_

---

## Laws this stack has to satisfy

Carried verbatim from the session 6 close. Both were learned expensively.

**Law 1 — The cave mouth is an OUTPUT, not an input.**
It emerges from layers + hardness + collapse. It is never a bored cylinder.
If the stack above can't produce the mouth through undercut and collapse, the
stack is wrong — the fix is the stack, not a boolean.

**Law 2 — Never tune a crack generator to look like rock.**
The machine cuts 1–2 real cracks plus a story-driven placement map. Isaiah's
hands do everything that has to read.

---

## What the Drive canon already answers

Pulled from Isaiah's Drive (★ START HERE v2 Jul 8, Decisions Locked Jul 6,
Session Update Jul 2). These are locked decisions, not new proposals.

**"The window" = the skylight.** Decisions Locked Jul 6: *"narrow offset
skylight in TOP over the GALLERY (never over the chamber — den stays dark;
fish gets dark+light choice)."* So "wire the eroded bite through to the
window" means the bite must reach the **gallery** skylight, not the chamber.

**Iron rule 4 restated in his own words:** *"One connected void, no dead
ends"* — mouth-in → gallery → tail-out. Exit smaller than mouth. Every
passage clearly passable or clearly impossible; no wedges (a fish pushes
forward and jams, it won't reverse).

**The layer stack IS the bedding planes.** The canon is built on Jura Grey
limestone: fossils strung *"loosely ALONG BEDDING PLANES,"* stylolites
wandering the grey and deflecting around fossils, veins cut *"along fracture
logic."* The stack isn't a new invention — it's the bedding the rest of the
finish program already sits on.

**The water story names the rotten layer.** Session Update Jul 2: rain enters
down the crest joint → dissolves the chamber (phreatic, rounded ceiling) →
*"drains sideways along the weak bed"* → exits at the tail. **That weak bed is
a rotten layer already locked by the story.** Question 3 above is therefore
read off the water story, not invented.

**Law 2 is doctrine #1.** *"MACHINES = ANATOMY, ISAIAH = ART. All organic
beauty is Isaiah's hands. Never art-direct a bot past two iterations —
reframe the job as engineering."*

---

## Recurring failure worth fixing

The Jul 8 Blender Core Work Brief already recorded both blockers that stopped
session 7, three weeks earlier: the Blender addon not answering at
localhost:9876, and the build report + STL living in *"that session's local
outputs folder, which this session can't reach."*

Same two failures, same order, twice. **The local outputs folder never gets
banked.** Any remote session will hit this again until `monster8_blockout.blend`
and the sprock-knowledge vault land somewhere reachable.

---

## Still open after this file

**Iron rule 4 — passage continuity.** The eroded bite has to wire through to
the window. Not solved. Depends on the stack above, because the bite's depth
and the collapse geometry are what determine whether the passage actually
connects. Cannot be designed before question 3 is answered.

**BLENDER TRAPS list** — lives in the vault handoff, has not been read by this
session. Must be read before the first boolean of session 7.

---

## Working rules that carry

- Everything stays separate objects.
- Ship every change's picture to chat, unasked.
- Long builds go in `blender --background --python`, not the bridge.
