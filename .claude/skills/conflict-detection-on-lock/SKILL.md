---
name: conflict-detection-on-lock
description: Use when integrating a batch of newly locked decisions into the repo (especially after a voice session). Run an explicit math/logic cross-check on related specs *before* committing — the cost of catching a conflict here is one paragraph; the cost of catching it after CAD geometry locks is days of rework.
---

# Conflict detection on lock

When Isaiah locks a cluster of decisions in a single session, especially under voice mode where he can't easily flip between specs, conflicts slip in. Catching them at integration time is cheap. Catching them after FreeCAD geometry derives from them is expensive.

## The pattern

After a decision-integration pass, before the commit, walk the locked decisions and ask:

1. **Do the numbers actually multiply?**
2. **Do the locked dimensions fit the constraints?**
3. **Do the locked materials handle the locked loads?**
4. **Are any rejected alternatives being implicitly used?**

If any answer is "no" or "I don't know," the integration isn't done — surface it.

## Real example: the 75 × 8 ≠ 750 catch

Phase 0 review of the bike grinder locked three values in one session:
- Pedal cadence: **75 RPM**
- Gear reduction: **8:1**
- Belt RPM target: **750 RPM**

Pure arithmetic: 75 × 8 = 600, not 750. One of these three is wrong. None of us caught it during the conversation — voice mode, multiple subtopics, gradual lock-in over 100+ messages.

Catching it during integration: cost = 1 paragraph in the response, and one open-question added.

Catching it after the master sketch had been built in FreeCAD with 5"/2" pulleys positioned for an 8:1 ratio: cost = re-derived pulley positions, possibly re-printed prototype, hours of work.

## Where conflicts hide

**Math chains.** Any time you have RPM × ratio = output, RPM × diameter / 60 = surface speed, torque × distance = moment arm — verify the arithmetic explicitly. Don't trust that Isaiah did the math right, and don't trust that *you* did when you locked it together over voice.

**Build-volume vs part-size.** Bambu A1 Mini = 180 mm cube. Any part >170 mm in any axis must split. This conflict only surfaces when the bounding box crosses the threshold — flag it before STL export, not after.

**Material vs load.** PETG yield strength is well-known. Gear-tooth shear at module 1.5 with 8:1 reduction × marathon-runner pedal torque = real number. Compute it. If it's anywhere close to PETG's failure stress, surface that in open-questions.

**Tolerance vs fab process.** A spec calling for "sub-thou flatness over 24 inches" on a 3D-printed PETG platen is impossible without post-machining. The decision to print + post-grind needs to be explicit, not implicit.

**Rejected → resurrected.** If you rejected springs in the tensioner but a downstream decision implicitly uses spring tension, you've contradicted a prior lock. Search the repo for the rejected term and check.

## How to surface a conflict

Don't fix it without asking. Isaiah is the source of truth on his own intent. Pattern:

```
Math conflict in the Phase 0 locked spec:
75 RPM cadence × 8:1 reduction = 600 RPM at the belt, not the 750 RPM target also locked.

One of three values is wrong:
(a) Real cadence is closer to 94 RPM
(b) Reduction is 10:1, not 8:1 (and the durability concern was overweighted)
(c) Belt RPM target is 600, not 750

Need this resolved before drivetrain geometry locks in FreeCAD.
```

Three properties matter:
1. **Show the math.** Don't just say "there's a conflict" — show the calculation.
2. **Enumerate the resolutions.** Don't make him guess what the options are.
3. **Tie it to a downstream consequence.** "Need this before X locks" gives him urgency calibration.

## When to skip the cross-check

- The locked decisions don't share physical dependencies. (Locking "use 304 stainless" and "horizontal layout" independently — no math to cross.)
- A single unambiguous spec that doesn't multiply with anything else.
- You're integrating a tiny change (one decision, no clusters).

For anything more than 3 related decisions locked in a single session, run the check.

## What NOT to do

- Don't quietly resolve the conflict yourself by picking one value
- Don't bury the conflict in a long response — it should be the first thing surfaced
- Don't commit the integration with a known unresolved conflict
- Don't make Isaiah do the arithmetic — show it
