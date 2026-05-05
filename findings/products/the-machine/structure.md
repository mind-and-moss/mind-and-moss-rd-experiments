# The Machine — Tank Construction & Structure

Structural engineering for the multi-tank racetrack: how the tanks are built, how they hold water pressure, and what fails.

---

Source: RESEARCH-001 Thread 2 — "DIY sensors for terrariums and aquariums" (continued)

### Design Approach
Circular/polygonal tanks built from flat acrylic segments — no heat bending:
- Flat acrylic sheet segments (avoids cloudiness/cracking from heat bending)
- PVC connectors angle them into a circle/polygon
- Sheet → PVC → Sheet → PVC pattern around perimeter
- Acrylic weld paste (weld liquid + acrylic dust shavings) fills micro-gaps

### Structural System (final validated design)
1. Acrylic dowels bonded between sheets (internal, hidden from water side)
2. Metal bolts drilled through acrylic directly into PVC (handle pressure load)
3. 3D-printed brackets as secondary alignment only — NOT primary load-bearing
4. External cable band around outside diameter (tension, prevents bowing)
5. Silicone as backup seal only

### Failure Modes Identified
1. **Thermal expansion mismatch** — acrylic, PVC, and 3D-printed plastic expand at different rates. Fixed by: keeping water temperature constant
2. **Stress cracking at bolt points** — flat sheet bows outward between bolts under pressure. Fixed by: internal support ribs (3D-printed, bonded inside) OR tension cable around outside diameter
3. **3D-printed bracket creep** — PETG/PLA are not rigid under sustained pressure load over years. Fixed by: metal bolts carry the load, brackets are alignment only

### Key Insight
> Water pressure pushes outward against metal bolts. Steel resists load permanently. Plastic creeps. The fix is making metal do the structural work, plastic do the alignment work.
