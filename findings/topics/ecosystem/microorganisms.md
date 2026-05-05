# Microorganisms in Bioactive Vivaria and Aquaria

> **Convention note:** This file is **external research synthesis**, not AI-conversation excavation like most other files in `topics/`. Sources are real primary references (peer-reviewed papers, university extension publications, established hobbyist references) cited inline with `Source:` lines pointing to the author + URL. If a claim is unverified or hobbyist-anecdote, it's flagged as such. Companion files: `soil-chemistry.md`, `decomposers.md`.

A gram of healthy soil contains several billion bacteria plus archaea, fungi, protozoa, and viruses (Penn State Extension). These are the organisms doing the actual chemistry — the visible cleanup crew is a downstream consumer of what the microbes produce. This file covers what's running underneath.

## The Nitrifying Bacteria — the Workhorses

Nitrification is a two-step aerobic process performed by chemoautotrophic bacteria that oxidize inorganic nitrogen for energy. It's the same process whether you're running a freshwater aquarium, a planted vivarium, or a wastewater plant.

**Step 1: Ammonia → Nitrite (AOB — ammonia-oxidizing bacteria)**
- *Nitrosomonas europaea* is the classical textbook organism. Modern surveys also find *Nitrosospira* and the archaeal **AOA** (ammonia-oxidizing archaea) often dominant in oligotrophic/low-ammonia systems like a mature aquarium.

**Step 2: Nitrite → Nitrate (NOB — nitrite-oxidizing bacteria)**
- For decades the hobby pointed at *Nitrobacter* as the nitrite oxidizer. Hovanec et al. (1998) used 16S rRNA molecular methods to show *Nitrobacter* is essentially absent from freshwater aquaria — *Nitrospira* spp. are the actual nitrite oxidizers in aquaria.
- Daims et al. (2015) further showed that some *Nitrospira* are **comammox** ("complete ammonia oxidizer") organisms that perform both steps in one cell.

This matters for product selection: a "bottle bacteria" containing only *Nitrobacter* (older formulations) cannot establish a freshwater nitrite-oxidizing population, because the resident community simply doesn't include it.

- Source: Hovanec et al. 1998, *Appl. Environ. Microbiol.* — https://pmc.ncbi.nlm.nih.gov/articles/PMC124703/
- Source: Daims et al. 2015, *Nature* — https://pmc.ncbi.nlm.nih.gov/articles/PMC5152751/
- Source: Penn State Extension — *Soil Microbiome: Functions of a Community* — https://extension.psu.edu/understanding-and-managing-soil-microbes

## Denitrifying Bacteria

Denitrification is the **anaerobic** reduction of nitrate stepwise to N₂ gas, performed by facultative heterotrophs (*Pseudomonas*, *Paracoccus*, many others) when oxygen drops below ~10% saturation. They burn organic carbon for energy and use nitrate as the electron acceptor.

In a vivarium, denitrification happens in the bottom inch or two of damp substrate, inside chunks of decaying wood, and in waterlogged moss mats. You don't have to add denitrifiers — they're cosmopolitan and they show up. You just have to leave them undisturbed and supply organic carbon.

- Source: Aquarium Science — *Denitrifying Media* (review with primary citations) — https://aquariumscience.org/index.php/7-5-denitrifying-media/

## Heterotrophic Soil Bacteria

The much larger background population. They consume dead organic matter and excrete CO₂ + simpler inorganic nutrients. The C:N ratio of their substrate determines whether nitrogen ends up *available to plants* (mineralization, C:N below ~20) or **locked into microbial biomass** (immobilization, C:N above ~30). Fresh wood chips in a viv (C:N ~400:1) will tie up nitrogen for months; well-rotted leaf litter (C:N ~20:1) releases it.

Bacteria break down sugars, simple proteins, and easy carbohydrates fastest. Cellulose and especially lignin are slower and dominated by fungi.

- Source: *C:N Ratio* overview, Tamil Nadu Agricultural University — http://eagri.org/eagri50/SSAC121/lec19.pdf
- Source: Mooshammer et al. 2014, *Frontiers in Microbiology* (PMC) — https://pmc.ncbi.nlm.nih.gov/articles/PMC3910245/

## Mycorrhizal Fungi — the Plant-Symbionts

Mycorrhizae are root-fungus partnerships. The fungus extends hyphae far beyond the root zone, scavenging phosphorus, nitrogen (mostly as NH₄⁺), potassium, calcium, copper, and zinc, and trades them to the plant for photosynthetic carbon.

**Two relevant types for a vivarium:**

- **Arbuscular mycorrhizae (AM, formerly VAM)** — symbionts of *most* tropical understory plants, mosses' liverwort relatives, ferns, and the majority of foliage species used in vivaria. Phylum Glomeromycota. They penetrate root cells and form tree-like "arbuscules" where nutrient exchange happens.
- **Ectomycorrhizae (ECM)** — symbionts of many temperate trees (oak, pine, beech). Less directly relevant in vivaria, but ECM-associated fungi are why **leaf litter from oak trees** brings useful microbes when you collect it for a build.

Practical implication: when you transplant a tropical plant from sterile tissue culture into a viv, it has no mycorrhizal partners. Inoculating with a generic AM product (Glomus / Rhizophagus mixes) or just adding a scoop of healthy forest soil tends to accelerate establishment.

- Source: Bonfante & Genre 2010 / annual reviews summary — Annual Review of Plant Biology — https://www.annualreviews.org/content/journals/10.1146/annurev-arplant-061722-090342
- Source: Begum et al. 2023, *PMC* — *Symbiotic synergy: How AMF enhance nutrient uptake* — https://pmc.ncbi.nlm.nih.gov/articles/PMC11953731/

## Saprotrophic Fungi — the Wood Eaters

Saprotrophs are the fungi decomposing dead plant matter. Two textbook categories:

- **White-rot fungi** degrade lignin AND cellulose using lignin peroxidase, manganese peroxidase, and laccase. Wood ends up bleached, fibrous, and crumbly. *Trametes versicolor* (turkey tail), *Pleurotus* (oyster mushrooms), and *Ganoderma* are common examples.
- **Brown-rot fungi** degrade only cellulose and hemicellulose, leaving the lignin behind as a brown, cubically-cracked residue. *Fomitopsis*, *Serpula*, *Postia*. They're the fungi that produce the soft, crumbly red-brown wood that isopods love.

Both groups appear spontaneously on decaying wood added to a vivarium. They are food for many isopod species (especially *Porcellio* spp.) and the substrate for fungus-grazing springtails.

- Source: Floudas et al. 2012 / Riley et al. 2014 *PNAS* — *Extensive sampling of basidiomycete genomes...* — https://www.pnas.org/doi/10.1073/pnas.1400592111
- Source: Goodell et al., USDA Forest Products Lab — *Section 2: Saprotrophic Fungi* — https://www.fpl.fs.usda.gov/documnts/pdf2014/fpl_2014_cullen001.pdf

## "Cycling" — What's Actually Happening

When hobbyists "cycle" a tank, they're seeding and growing the AOB and NOB populations until ammonia and nitrite both read zero with a stable nitrate climb. Biochemically it's:

1. Add an ammonia source (fish food, pure NH₄Cl, or an animal).
2. AOB populations double roughly every 24–36 hours, lagging behind ammonia spikes.
3. Once ammonia → nitrite is established, NOB populations follow on a similar lag.
4. Plant uptake and (in deep substrate) denitrification close the loop on nitrate.

A typical fishless cycle takes 3–6 weeks at 24–28 °C, faster at higher temps and with a seed of established media or substrate from another tank.

## The Bottle Bacteria Question

Do products like Tetra SafeStart, Seachem Stability, API Quick Start, and Fritz Zyme actually work?

- Most independent tests are mixed-to-negative. Aquarium Science (Loiselle, citing controlled tank trials) tested several products and found most performed no better than a no-additive control.
- One notable peer-reviewed study by **Scagnelli, Javier, Mitchell & Acierno (2022)** — *Efficacy of quick-start nitrifying products in controlled fresh-water aquaria* — found Tetra SafeStart Plus did measurably reduce ammonia from 1 ppm → 0.29 ppm over 14 days vs. a control, while several other products did not.
- Mechanistically, Tetra SafeStart contains *Nitrosomonas*, *Nitrosospira*, and *Nitrospira* (the right organisms based on Hovanec et al.); some older products contained *Nitrobacter* — the wrong organism for freshwater.

Practical take: if you want a head start, Tetra SafeStart Plus has the best documented efficacy. None of these products replace cycling; at best they shorten it by a week or two. Free media or substrate from an established system remains the gold standard.

- Source: Aquarium Science — *Bacteria in a Bottle in Depth* — https://aquariumscience.org/index.php/2-8-1-bacteria-in-a-bottle-in-depth/

## Microbe–Isopod–Springtail Interactions

- **Springtails** (Collembola) preferentially graze fungal hyphae and bacteria-coated detritus. They're net mineralizers: their grazing keeps fungal mats from going dormant and accelerates nutrient release back to the soil.
- **Isopods** consume coarser detritus pre-digested by saprotrophic fungi. The fungal pre-treatment is mandatory for many species — fresh leaves are unpalatable until they've been "conditioned" by fungi for weeks.
- **Microbes also live inside isopods**: like termites, isopods rely on gut bacteria to digest cellulose. Antibiotic exposure (e.g., contaminated tap water with chloramine that hasn't been dechlorinated) can sterilize their gut and kill them indirectly.

The whole loop: dead plant matter → fungi colonize → isopods eat the fungal-colonized matter → isopod waste re-enters the substrate → bacteria mineralize it → plants take up the mineralized N and P. Springtails are the rapid cleanup at every stage.

## Open Questions

- **Unverified for vivaria specifically**: the relative dominance of AOA (archaea) vs AOB (bacteria) at vivarium-typical low ammonia loadings. AOA dominate in oligotrophic systems; whether a stocked vivarium qualifies as oligotrophic enough is an open question I couldn't find primary data on.
- **Unverified**: long-term efficacy claims of mycorrhizal-inoculation products under closed-vivarium conditions (most studies are in agricultural fields).
