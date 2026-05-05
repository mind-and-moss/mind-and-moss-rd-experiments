# The Machine — Water Flow & Oxygenation

Cascade flow design, pump sizing, and pure-O2 saturator considerations for the racetrack circuit.

---

Source: RESEARCH-001 Thread 1 — "DIY sensors for terrariums and aquariums"

### Water Flow System
- Gravity-fed cascade (water falls tank to tank downward)
- Air gaps between tanks kill pressure spikes
- Baffle plates dial in current strength
- Fish should dart upstream against gentle current — not get pinned
- Single pump recycles water back to top of the stack
- Tube sizing: 0.5-0.75 inch vinyl or silicone for main lines

---

Source: RESEARCH-004 Thread 12 — "Pumping oxygenated water between containers"

### Context
Isaiah asked: can I mix O2 in a 4x4 in water box and then pump it 12 inches to be in an aquarium, and then pump it out for the cycle.

### Validation
**Yes — this is a real technique** called an "oxygen reactor" or "O2 saturator," used in aquaculture and high-density fish setups.

### Design Notes
- 12" head is trivial — any submersible/inline pump handles it
- **Flow rate matters more than lift** — want enough turnover to keep O2 stable
- **Mixing box MUST be sealed** (or have gas cap) for pure O2 to dissolve efficiently
  - If open to air = just aerating — same result as an airstone for far less complexity
- Common designs:
  - Downflow contact column (water cascades through O2 atmosphere)
  - Venturi/diffuser inside pressurized chamber

### CRITICAL FAILURE MODE: Gas Bubble Disease
- Pure O2 can supersaturate water past 100%
- Above ~115% total dissolved gas saturation = bubbles in fish blood/tissues = can kill fish
- Commercial O2 reactors tuned carefully + often include a **degassing step**
- This risk only applies with pure O2 (compressed). Air pumps can't supersaturate.

### When O2 Injection is Worth the Complexity
- Very heavily stocked tanks
- Warm-water fish farming
- Koi in summer
- Hospital/quarantine tanks treating sick fish
- Research setups

### When It's NOT Worth It
- Normal home aquarium — airstone or surface agitation gets ~100% saturation, plenty for almost any fish

### Relevance to The Machine
For zebrafish in 55–75 ft racetrack, surface agitation from cascade flow + airstones likely sufficient. Only consider O2 saturator if stocking density gets very high.

---

Source: RESEARCH-005 Thread 17 — "Aquarium Pressure and Oxygen Issues" (chat #15)

### Closed-cycle gas exchange basics (relevant to The Machine if any portion is sealed)
- 5-gallon bucket as integrated gas + filter chamber discussed (cross-references the canister filter concept)
- DIY condenser for humidity control
- Self-contained biosphere principles
- Net positive O₂ in closed setup raises the CO₂ accumulation question

### Humidity escape via dehumidifier coupling
- 15-gallon aquarium with all airflow routed out one tube → external dehumidifier
- Cab Yick $45 dehumidifier on Amazon as low-cost prototype hardware

### Copepod feeding (cross-reference)
- Source: RESEARCH-005 Thread "Feeding Copepods in 1G Tank" (chat #12)
- Single question — feeding copepod populations in 1-gallon tank
- Live food culture for fish — could be a Machine inhabitant supply
