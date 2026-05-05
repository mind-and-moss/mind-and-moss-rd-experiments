# LED Wiring (Painted PLA / Illumination Builds)

Wiring, power, and protection notes for small-scale LED illumination builds. Borderline product relevance — captured here because the techniques apply if Mind and Moss adds illumination to The Gem.

---

Source: RESEARCH-004 Thread 14 — "Untitled" (chat #16 in sidebar)

Borderline product relevance — small-scale LED build (2xAA / 6 LEDs / painted PLA) but the techniques apply if Mind and Moss adds illumination to The Gem.

### Power & Protection
- Regulated 12V DC supply (≥2A for ~100 LEDs)
- **Inline fuse on +12V near input** — 1A fast-blow for small builds, 2A for many LEDs (most important "accident proof" element)
- Panel-mount barrel jack so cable can't yank internals
- Switch on +12V line for on/off

### Wiring
- LEDs in **parallel** (500Ω resistor pre-built for 12V types)
- Distribution: WAGO 221 lever nuts (cleanest, reopenable), tiny bus bar/perfboard, or 18 AWG trunk wires + heat-shrink

### Battery Voltage Mismatch (specific build)
- 2xAA = 3V — won't drive 12V LEDs
- Options: 8xAA (=12V), 12V A23 battery (tiny, low capacity), 3x CR2032 (≈9V, dim), boost converter (3V→12V module $2–4), or different LEDs (pre-wired 3V)
