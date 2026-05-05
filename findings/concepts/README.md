# Concepts

This folder is for **unvalidated ideas and random inventions** — product candidates that have surfaced from R&D but aren't yet flagship products.

Each concept lives as a single flat `.md` file here. The folder is designed to scale to many ideas, not just the current shortlist. A concept staying in this folder is not a knock against it — it just means it hasn't earned a dedicated `products/<name>/` directory yet.

## Graduation rules

A concept stays as one `.md` file in `concepts/` until it has **at least one** of:

- **(a) Working prototype** — something physical exists and demonstrates the core idea.
- **(b) Confirmed price/market fit** — researched pricing against competitors, confirmed there's a real market gap.
- **(c) Enough research that one file becomes unwieldy** — when a single `.md` would be hundreds of pages or starts mixing too many sub-topics that deserve their own files.

When a concept graduates:

1. Create a new folder `products/<concept-name>/`.
2. The original file becomes `products/<concept-name>/concept.md`.
3. Sub-topics that have grown enough get split out into sibling files (e.g. `structure.md`, `materials.md`).
4. Update `findings/README.md` map to list the new product folder.

## What goes in a concept file

- Top-level pitch: what is this thing, in one or two sentences.
- Why it might matter: differentiation, market gap, technical feasibility hunch.
- What's known so far: cite source Threads from `archive/` using the standard `Source:` header convention.
- Open questions: what still needs to be answered before this could graduate.

Keep concepts cheap to write. The bar for putting an idea in here is "non-trivially worth remembering" — not "fully validated."
