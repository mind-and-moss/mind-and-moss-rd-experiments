---
name: decision-mode-when-trusted
description: Use when Isaiah explicitly delegates a call ("I trust your opinion more than mine on this," "go figure it out for yourself," "use your vast inventory"). Don't bounce the question back. Make the call, document the reasoning, move on. The wrong move here is asking another question.
---

# Decision mode (when trusted)

When Isaiah delegates, he means it. The wrong response is "Got it — to make the right call, I just need to know..." That's me bouncing the question back to him after he just said "stop bouncing it back."

## Delegation triggers

He's said any of:
- "I trust your opinion more than mine at this specific variable"
- "go figure it out for yourself"
- "you can go search up stuff"
- "use your vast inventory"
- "make the call"
- "I don't know, you decide"

Or implicitly:
- He's in voice mode and just said "Yeah, that sounds good" to a recommendation you offered tentatively
- He's busy/driving and you've already asked one clarifying question this turn

## What to do

### 1. Search if needed

If you don't know the answer and he gave you "go figure it out" — go figure it out. WebSearch, WebFetch, or fork a research agent. Don't ask him for the data; gather it yourself.

### 2. Pick

Make the call. There's almost always a defensible choice. Pick the one with the strongest reasoning and commit.

### 3. Document the reasoning

In one sentence, in the response or in the repo. Why this and not the alternatives? Future-Isaiah (or future-Claude) will read this and know whether to trust the decision or revisit it.

### 4. Tell him cleanly

Pattern that works:

```
Picked X. Reasoning: [one sentence]. Logged in [file].
```

Not:

```
After researching, I think X is the right choice for [paragraph]. 
But Y is also viable for [paragraph]. And Z if [paragraph].
What do you think?
```

## Real example: idler wheel sizing

From the Phase 0 review, after Isaiah delegated:
> "Well, you can go search up stuff. So why don't you... I mean, go figure it out for yourself."
> "Yeah. And I actually trust your opinion more than mine at this at this specific point... at this specific variable."

Right response (what I did): web-search, find that 2" is the consensus for 2x72 grinders, lock 2" idler, note it as decided, move on.

Wrong response (what I almost did): "Got it — to pick the right idler diameter, I just need to know your target belt geometry, frame envelope, and tracking-wheel placement. Could you share those?"

He just told you to stop asking. Stop asking.

## When to escalate back

Even in decision mode, escalate to Isaiah when:

- The call has irreversible consequences (a part you can't unprint, a check you can't unsend)
- You'd be touching one of his explicit non-negotiables (biotope fidelity, "how the fuck did they make that," The Gem framing)
- The cost of being wrong exceeds the cost of one extra round trip (high-budget hardware purchases, branch-merge decisions)
- You hit a genuine tie between two defensible options with materially different downstream consequences

In all four cases, surface ONE question, framed as: "This is one I want your call on because: [reason]. Two options: A or B."

## The asymmetry

Isaiah's bandwidth for decisions is the bottleneck on this whole project. Every question you bounce back costs him a round trip. Every decision you make for him saves a round trip.

If you're wrong, the cost is "we redo this." If you fail to decide, the cost is "we wait for him." The first is recoverable; the second compounds.

Default to deciding. Document. Move.

## What NOT to do

- Don't use phrases like "to give you a thoughtful answer, I'd need..." — that's bouncing, dressed up
- Don't list options without picking one
- Don't ask a "clarifying question" that's actually a different version of the original question
- Don't apologize for deciding
- Don't ask for permission to research — research is delegation territory
- Don't decide silently — log the reasoning so it's auditable
