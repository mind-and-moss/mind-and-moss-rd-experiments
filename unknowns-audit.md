# Unknowns Audit — NASA-Rigor Pass

> **Purpose:** Surface every unanswered question across the project, not just the 13 already in `decisions-pending.md`. Many gates have been masked by "we'll figure it out later" framing. This is the everything-list.
>
> **Triage column:** **D** = decision (pick from options) — should land in `decisions-pending.md`. **S** = specification (free-form value/number) — should be locked once decided. **R** = research — Claude can investigate further. **U** = needs Isaiah input that no research can substitute for.

Updated: 2026-05-05.

---

## Already in `decisions-pending.md` (13 items)

Briefly: seam type, glass type, COE system, mold silicone, cast material, base material, Machine open/sealed, aquarium method, anchor plant SKU, centerpiece mounting, PR merge order, editorial edits, instrumented prototype start.

The rest of this audit is **what's NOT yet captured.**

---

## A. The Machine — geometric / dimensional unknowns (S)

> **Restructured 2026-05-05:** Sections A (The Gem) and B (The Machine) were merged after the gem restructure (PR #7). The Gem is a small component within The Machine, not a peer product. Gem-component-specific dimensions are listed under "Gem-component sub-section" below.

Some specified in R001 T1 but big gaps remain.

| Question | Triage |
|---|---|
| Total room footprint required | S/U |
| Concrete column / pillar dimensions (height, width, count) | S |
| Tank wall material — given 1 mm acrylic is too thin, what's the spec? | D |
| Tank wall thickness (3 mm cast acrylic? 6 mm glass? other?) | D |
| Total water volume across all tanks | calc |
| Pump capacity (L/h or GPH) | S |
| Cascade head height per stage | S |
| Embedded mechanical features — which are real, which are aesthetic? | D/U |
| Total assembled weight (drives shipping + display surface load) | calc |
| Aquarium-portion water volume | calc |
| Terrarium-portion volume | calc |
| Base material thickness / profile | S |

### Gem-component sub-section

| Question | Triage |
|---|---|
| Glass frame geometry — cube, hex column, curved, faceted? | D/S |
| Glass panel thickness — your inventory has 6 mm; is that the spec? | S |
| Number of glass panels in the frame | S (depends on geometry) |
| Centerpiece diameter (sphere/hemisphere) | S |
| Frame-to-Machine-base interface — flush, recessed, lip? | S |

## C. Livestock specifications (D + U)

The brand promise is "living ecosystems" — but what actually lives in each product hasn't been chosen.

| Question | Triage |
|---|---|
| The Machine aquarium portion — fish species and stocking count | D/U |
| The Machine aquarium portion — invertebrates (shrimp? snails? both?) | D/U |
| The Machine terrarium portion — animals (frogs? isopods? springtails only?) | D/U |
| The Machine terrarium portion — plants (anchor plant decided? others?) | D/U |
| The Machine — confirmed zebrafish per R001 T1, but stocking density? | S |
| The Machine — co-stockers (neon tetras mentioned, locked in?) | D |
| Cylindrical terrarium — current stocking | known? document |
| Livestock sourcing strategy — captive-bred, wild-caught, supplier? | D/U |
| Quarantine protocol for new stock | S/R |

## D. Lighting & power (S + R)

Not specified anywhere in the repo.

| Question | Triage |
|---|---|
| Machine terrarium-portion light — type, color temp, photoperiod | D/S |
| Machine aquarium-portion light — type, color temp, photoperiod | D/S |
| Machine gem-component illumination — internal? external? edge-lit? | D |
| The Machine — lighting per tank or area-wide? | D |
| Total wattage per product (drives plug count, GFCI, customer install) | calc once spec'd |
| Voltage / region — US 120V only, or future international? | D |
| Surge protection / electrical safety story for customer | S/R |
| Smart-home integration (timer? app? none?) | D |

## E. Water specifications (S + R)

Critical for any aquarium portion. None specified.

| Question | Triage |
|---|---|
| Machine aquarium target pH | S |
| Machine aquarium target GH/KH (hardness) | S |
| Machine aquarium target temp | S |
| Machine aquarium turnover rate / filtration plan (Walstad-derived per #8?) | D |
| Water source — tap + dechlorinator? RO/DI? | D |
| Top-off strategy — auto, manual, customer's responsibility? | D |
| Water change schedule — Walstad's "twice yearly" or different? | D |
| Maintenance documentation provided to customer | S |

## F. Climate / environment (S)

| Question | Triage |
|---|---|
| Machine terrarium target humidity | S |
| Machine terrarium target temp | S |
| Heating method — heater, ambient, none? | D |
| Cooling/airflow — passive vent, fan, sealed? | D |
| Room-temperature assumptions for the customer's space | S/U |
| Window/sunlight tolerance — is it OK near a window? | S/R |

## G. Customer / market (U)

These are pure Isaiah calls — no research substitutes.

| Question | Triage |
|---|---|
| Target customer profile (collector? interior designer? hobbyist?) | U |
| Target price point for The Machine (separate from base price?) | U |
| Target price point for The Machine | U |
| Estimated cost of materials per Machine | calc once spec'd |
| Estimated build hours per Machine | U |
| Customer ordering process — direct? gallery? Etsy? Shopify? | U |
| Lead time customer-facing (weeks? months?) | U |
| Customization options offered or fixed designs only? | U |
| First-customer plan — friend? commission? speculative build? | U |

## H. Production strategy (D + U)

Each path has very different tooling implications.

| Question | Triage |
|---|---|
| One-off art piece vs replicable design vs limited series? | D/U |
| If replicable: how many per year is the goal? | U |
| Who builds them — Isaiah only, helpers, contracted fabrication? | U |
| Mold reuse strategy — single-piece master or production molds? | D |
| Standard sizes vs every-piece-bespoke | D/U |
| QC checklist — what makes a Machine "ready to ship"? | S |

## I. Distribution & fulfillment (D + U)

| Question | Triage |
|---|---|
| Local pickup, regional delivery, nationwide ship, international? | U |
| Shipping crate design (heavy + fragile + living + water?) | S/R |
| White-glove install vs customer-installs from a kit? | D |
| Demo / studio space for in-person customer view? | U |
| Photography / video plan for online listings | U |
| Delivery without livestock + customer adds livestock locally? | D |

## J. Brand / business basics (U)

| Question | Triage |
|---|---|
| Domain name owned? | U |
| Website status | U |
| Social presence — Instagram? TikTok? YouTube? | U |
| Logo / typography / brand visual system | U |
| Tagline/positioning — beyond "how the fuck did they make that"? | U |
| Photography portfolio plan | U |

## K. Legal / business structure (U + R)

| Question | Triage |
|---|---|
| Business entity — sole prop, LLC, S-corp? | U |
| Sales tax setup (state-by-state liability) | U/R |
| Liability insurance for live-product claims (mold, leaks, etc.) | U/R |
| Warranty terms — what's covered, for how long? | U |
| Live-stock liability (fish dies in transit) — replacement policy | D |
| Permits / regulations — invertebrate import/export, plants by state | R |

## L. Failure mode coverage (S + R)

For each major thing that could go wrong, what's the response plan?

| Failure | Response plan? |
|---|---|
| Mycelium base dries / dies | Y/N |
| Aquarium half leaks (seam fails) | Y/N |
| Glass cracks (thermal shock, impact) | Y/N |
| Centerpiece breaks loose from mount | Y/N |
| Livestock dies | Y/N |
| Bioactive cleanup crew dies | Y/N |
| Algae bloom in customer's home | Y/N |
| Substrate compaction / chemical drift | Y/N |
| Power loss for >X hours | Y/N |
| Customer mistreats it (overwaters, no light, etc.) | Y/N |

Each is a customer support question with a SOP behind it. None documented.

## M. Time / bandwidth (U)

| Question | Triage |
|---|---|
| Hours per week available for Mind and Moss | U |
| Day job / school constraints | U |
| Target date — first complete prototype Machine | U |
| Target date — first sold Machine | U |
| Target date — first profitable month | U |

## N. Competitive positioning (R + U)

| Question | Triage |
|---|---|
| Direct competitors making art-paludarium pieces — names, prices? | R |
| Indirect competitors (high-end aquarium designers like Aquatic Design Centre) | R |
| What makes Mind and Moss specifically different (positioning statement)? | U |
| Defensibility — is the design copyable? Patent angle? | U |

## O. Documentation gaps (S)

| Question | Triage |
|---|---|
| Customer manual — does one exist? | needs writing |
| Build instructions for Isaiah's own future reference | needs writing |
| Photography / portfolio of completed work | needs creation |
| Video walkthrough of a build | needs creation |
| FAQ for prospective customers | needs writing |

---

## Summary — counts

- **A. Machine geometry (incl. gem-component):** 17 unknowns
- **B. Machine geometry:** 9
- **C. Livestock:** 9
- **D. Lighting/power:** 8
- **E. Water:** 8
- **F. Climate:** 6
- **G. Customer/market:** 9
- **H. Production:** 6
- **I. Distribution:** 6
- **J. Brand:** 6
- **K. Legal:** 6
- **L. Failure modes:** 10
- **M. Bandwidth:** 5
- **N. Competition:** 4
- **O. Documentation:** 5

**Total: ~108 unknowns** (in addition to the 13 already in `decisions-pending.md`).

That's the NASA-grade picture. Most products ship without ever surfacing this many unknowns explicitly — but most products also discover them as failures mid-build, which is what you said you don't want.

---

## Triage by type

- **U (needs Isaiah input, no substitute):** ~55 — customer profile, pricing, time, brand basics, target dates
- **D (decision, options exist):** ~20 — wall material, water source, install method, etc.
- **S (specification, value to lock):** ~25 — temperatures, dimensions, photoperiods, etc.
- **R (research can advance):** ~8 — competitive landscape, regulatory, shipping crate design, RO/DI tradeoffs

## What's solvable RIGHT NOW (this conversation, without your input)

I can take a research-and-draft pass on: shipping crate design for live products, US state-by-state plant/invertebrate regulation summary, competitive landscape (named competitors + price points), failure-mode SOPs (drafts for review), QC checklist template, customer manual outline. These are R-tagged.

## What needs you (no shortcut)

Anything U-tagged. Especially the geometry, customer profile, and price point — these gate everything else and only you can pick.

## My pick for the highest-leverage 5 to crack first

Solve these and 50+ other unknowns auto-resolve as derivatives:

1. **The Machine's overall geometry (and the gem-component within it)** (height, footprint, frame shape). Drives glass count, water volume, weight, lighting, shipping. Pure Isaiah call.
2. **The Machine's target price point**. Drives material budget, build-hours target, who the customer is. Pure Isaiah call.
3. **Production strategy** — one-off art vs replicable. Drives molds, tooling, time, brand voice. Mostly Isaiah call.
4. **First-customer plan**. Real or speculative. Drives the time pressure on everything else. Pure Isaiah call.
5. **Hours per week for Mind and Moss**. Drives every timeline.

Get these five locked and the project shape stops being abstract.
