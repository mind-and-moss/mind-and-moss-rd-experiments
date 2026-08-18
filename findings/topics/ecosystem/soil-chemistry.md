# Soil Chemistry in Bioactive Vivariums

> **Convention note:** This file is **external research synthesis**, not AI-conversation excavation like most other files in `topics/`. Sources are real primary references (university extension publications, peer-reviewed papers, established hobbyist references) cited inline with `Source:` lines pointing to the author + URL. If a claim is unverified or hobbyist-anecdote, it's flagged as such. Companion files: `microorganisms.md`, `decomposers.md`.

The chemistry of a vivarium substrate is the invisible scaffolding that everything else — plants, isopods, springtails, the entire microbial community — depends on. Get the chemistry roughly right and the system tolerates abuse; get it wrong and you'll see plant decline, mold blooms, or invertebrate die-offs that look mysterious until you measure pH or redox state.

## pH and Why It Matters

Soil pH governs both **plant nutrient availability** and **which microbes will dominate** the substrate. Most vascular plants are happiest between pH 6.2 and 6.8, where calcium, magnesium, manganese, copper, zinc, iron, and boron are all reasonably bioavailable. Outside that band, even nutrient-rich soil can starve plants because nutrients become locked into insoluble forms.

Microbial activity follows a similar curve. Penn State Extension notes that "soil microorganism activity is greatest near neutral conditions" and that nitrifying bacteria and nitrogen-fixers "perform poorly when soil pH falls below 6" — directly relevant for a bioactive viv where you depend on those bacteria to convert isopod and springtail waste into plant-usable forms.

- Source: Penn State Extension — *Understanding Soil pH* — https://extension.psu.edu/understanding-soil-ph
- Source: Penn State Extension — *Understanding and Managing Soil Microbes* — https://extension.psu.edu/understanding-and-managing-soil-microbes

## Cation Exchange Capacity (CEC)

CEC is the substrate's ability to hold positively charged nutrient ions (Ca²⁺, Mg²⁺, K⁺, NH₄⁺) on negatively charged sites and release them gradually. Higher CEC = more nutrient buffering. The University of Idaho and Purdue extension publications give working numbers:

- **Sphagnum peat**: ~110–130 meq/100g (very high)
- **Coco coir**: ~39–60 meq/100g (moderate; binds Ca and Mg preferentially, which can starve plants of those nutrients unless the coir is "buffered" with calcium first)
- **Sand / LECA / pumice**: near zero (these contribute drainage and structure, not nutrient holding)

A practical mix for a planted bioactive viv leans on peat or coir for CEC, with bark and leaf litter on top as a slow nutrient feed.

- Source: University of Idaho Extension — *Cation Exchange Capacity (CEC)* — https://www.uidaho.edu/-/media/uidaho-responsive/files/extension/topic/nursery/technical/cec-and-cn-ratio.pdf
- Source: Purdue Extension HO-255-W — *Evaluating Container Substrates and Their Components* — https://www.extension.purdue.edu/extmedia/HO/HO-255-W.pdf

## The Nitrogen Cycle in Substrate

Animal waste hits the substrate as urea or ammonium. Two groups of chemoautotrophic bacteria convert it stepwise:

1. **Ammonia → nitrite** by *Nitrosomonas* / *Nitrosospira*
2. **Nitrite → nitrate** by *Nitrospira* (and historically *Nitrobacter*, though modern molecular studies find *Nitrospira* dominant in freshwater and most soil systems)

Nitrate is non-toxic at the levels a vivarium produces, and plants take it up readily. In **deep, anaerobic substrate zones** (typically below ~3 inches of sediment, or in waterlogged pockets), heterotrophic denitrifiers reduce nitrate back to N₂ gas, which escapes. This is why you don't usually need to "remove nitrate" from a planted bioactive viv — plants and denitrifiers do it for you.

- Source: Daims et al. 2015 — *Complete nitrification by Nitrospira bacteria* (PMC) — https://pmc.ncbi.nlm.nih.gov/articles/PMC5152751/
- Source: Hovanec et al. 1998 — *Nitrospira-Like Bacteria Associated with Nitrite Oxidation in Freshwater Aquaria* (PMC) — https://pmc.ncbi.nlm.nih.gov/articles/PMC124703/

## Phosphorus, Potassium, and Micronutrients

Phosphate (PO₄³⁻) chemistry is pH-dependent: locked up below pH 5.5 (binds to iron and aluminum) and above pH 7.5 (binds to calcium). Inside the 6–7 sweet spot it stays plant-available. This is one more reason to keep vivarium pH near neutral.

Potassium and most micronutrients ride on the CEC sites of peat/coir; they're replenished slowly from leaf-litter breakdown and from any reptile/amphibian waste. You generally don't need to dose nutrients in a viv — overfeeding the cleanup crew is your fertilizer schedule.

## Buffering: Keeping pH Stable

Bioactive substrates trend acidic over time as organic acids accumulate from decomposition. Common buffers:

- **Calcium carbonate** (crushed eggshell, cuttlebone, oyster shell, limestone fines): dissolves slowly when pH drops, releases Ca²⁺ and HCO₃⁻ to push pH back up. Doubles as a calcium source for isopods.
- **Sphagnum peat**: paradoxically, peat *itself* acidifies (pH ~3.5–4.5), so peat-heavy mixes need more carbonate buffer than coir-heavy mixes.
- **Organic matter generally** raises CEC, which buffers against rapid swings even if it doesn't change steady-state pH.

For Isaiah's setups (plants + isopods + springtails), I'd target pH 6.3–6.8 with a baseline of crushed cuttlebone or oyster shell mixed into the topsoil layer. The isopods will eat it, the carbonate will dissolve into the substrate, and you avoid the slow acidification problem.

## Substrate Stratification: What Each Layer Does Chemically

A standard bioactive build is three layers, and each has a job:

1. **False bottom (LECA, lava rock, or eggcrate-supported void)** — physically separates the soil from any standing water. Chemically, the LECA pores host aerobic biofilm that helps oxidize anything that leaches down. Source: Terrarium Tribe — *Terrarium False Bottom 101* — https://terrariumtribe.com/terrarium-false-bottom/
2. **Substrate barrier (mesh)** — purely physical; keeps soil out of the drainage layer.
3. **Topsoil mix (ABG, coco-peat-bark blends, etc.)** — where the chemistry happens: CEC, nitrification, root zone, isopod/springtail habitat. Add a thin **leaf-litter cap** on top — this is both food for the cleanup crew and a slow-release nutrient layer.

A subtle point: the **interface between aerobic topsoil and the wetter zone just above the false bottom** is where denitrification can occur. Don't disturb it once it's established.

## Cross-Reference: Concrete Leaching

If hardscape elements include cured concrete, calcium hydroxide leaching will spike pH dramatically (often pH > 11) for weeks to months. See `findings/topics/materials/concrete.md` for cure/seal protocols. Never put fresh concrete into a bioactive viv — the alkali surge will sterilize the microbiome and kill plants.

## Practical Takeaway for a Plant + Isopod + Springtail Vivarium

- Aim pH 6.3–6.8. Test occasionally with a soil probe or 1:1 slurry test.
- Use peat or coco coir as the CEC backbone, mixed roughly 1:1:1 with fine bark and a drainage component (pumice, perlite, or fine LECA).
- Add ~5% by volume crushed cuttlebone or oyster-shell flour as a long-term buffer + calcium source.
- Keep a leaf-litter cap (live oak, magnolia, sea grape — slow-decomposing species).
- Don't disturb the bottom inch of substrate during maintenance; that's where your denitrifiers live.

## Open Questions

- **Unverified**: actual long-term pH drift rate in a sealed vivarium has not, to my knowledge, been measured in published literature — most data comes from agricultural soils. A simple monthly pH log on a working enclosure would be a useful Mind and Moss data point.
- **Unverified**: optimal Ca:Mg ratio for isopod molting in coco-coir-based substrates — hobbyist guidance varies; no peer-reviewed study found.
