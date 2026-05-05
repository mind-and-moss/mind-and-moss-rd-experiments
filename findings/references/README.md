# References — External / Online Sources

This folder is the parallel sibling to `topics/`, but with a fundamentally different content rule: **external/curated sources only**, not AI-conversation excavation.

## Why this folder is separate

Everything in `topics/`, `products/`, `concepts/`, and `archive/` traces back to AI conversations (Claude.ai, ChatGPT, etc.) — that content is verbatim from threads and tagged with `Source: RESEARCH-XXX Thread N` headers. AI excavation is great for ideation and connecting concepts, but it's not authoritative for technical specs, current pricing, or vendor data.

This folder is the human-curated counterweight: manufacturer datasheets, hobbyist forum threads, YouTube channels, calculator tools, suppliers, books, papers — the actual primary sources.

## Structure

Mirrors `topics/` so a researcher can flip between "what the AI told me" and "what the actual sources say" on the same topic:

```
findings/
  topics/          ← AI-conversation content (verbatim from threads)
  references/     ← external/curated content (this folder)
    materials/
    fabrication/
    ecosystem/
    electronics/
    cad-and-modeling/
```

Subfolders are added only when there's content to put in them. Empty trees aren't worth their footprint.

## File convention

Each file is a curated link list, NOT a content dump. The point is to know *where to look*, not to mirror everything.

Format per entry:

```
- **<Source name>** — what it is, what it's good for. (URL if known)
```

When something in `topics/` is contradicted or confirmed by an external source, add a backlink in the topics file pointing here. Don't paste external content INTO topics files — that mixes provenance.

## When to add an entry

- You found a manufacturer datasheet that nails down a spec the AI was vague on.
- You watched a YouTube build that taught you something the AI couldn't.
- You found a forum thread with real users solving the problem you're researching.
- You bought from a supplier and want the link captured for next time.

## When NOT to add an entry

- A random Google result that you skimmed but didn't validate.
- AI-written content from a different chatbot — that goes in `archive/` as a new RESEARCH file.
- Aspirational links ("I should read this someday") — keep those in personal notes, not the shared knowledge base.

## Tagging unverified entries

If you list a source but haven't fully validated it yet, prefix with `[unvetted]` so future-you knows. Example:

```
- [unvetted] **Some Forum Post** — claims X about silicone bond lines. Need to verify.
```
