# Heat-Set Inserts for the Bike-Powered Grinder

Research synthesis for picking and installing M3 / M5 heat-set inserts in the 3D-printed structural parts of the bike-powered glass grinder. The grinder's load case is mechanically nasty: continuous bicycle-pedal torque flowing through bearing blocks, gear mounts and axle supports, with vibration and water spray from the grinding wheel. Inserts have to hold under sustained torque, survive vibration, and not corrode after a glass-grinding session.

The short answer for "what should I buy and how do I install it":

- For every M3 and M5 location, use **brass heat-set inserts with double knurling and a tapered/flanged top** (CNC Kitchen, Ruthex, or McMaster-Carr 94459A series). Skip stainless inserts unless a specific part is going to be submerged for hours.
- Print the receiving parts in **PETG, not PLA**, with at least 4-6 perimeters and 2x insert-OD wall thickness around the hole.
- Hole diameter: **CNC Kitchen / Ruthex M3 = 4.0 mm hole; M5 = 6.4 mm hole** (per their datasheets). Voron-spec M3x5x4 inserts use a 4.7 mm hole. Always print a hole-size test piece for your specific filament before committing.
- Soldering iron at **printing-temp + 10-20 deg C** (so PETG = ~245-260 deg C). Use a CNC Kitchen / Trianglelab heat-set tip, not a generic chisel tip.

Everything below is the reasoning.

---

## 1. Brass vs. stainless steel

Brass wins for this build for three independent reasons:

1. **Thermal conductivity.** Brass conducts heat about 15x better than austenitic stainless. That is what makes heat-setting work at all - the iron heats the insert, the insert melts the surrounding plastic, and the plastic re-flows around the knurls. Stainless inserts stay cold long enough that you scorch the part before the insert seats.
2. **Cost / availability.** Brass is the volume product. Stainless heat-set inserts in M3/M5 are a niche item, mostly only relevant in salt-spray marine or FDA-food-contact applications.
3. **Corrosion is not actually a problem here.** The grinder sees occasional tap-water spray, not seawater. Brass resists "mild alkaline solutions, non-oxidizing acids, and petroleum products" without issue. The water that comes off a glass-grinding wheel is essentially tap water plus glass slurry - no chlorides at concentration, no acid. Brass will tarnish cosmetically but will not lose pull-out strength.

If a future version of the grinder has a part that is fully submerged or in a constant water bath (e.g. a pump housing), reconsider 316 stainless inserts for that one part only.

Sources:
- https://www.ezlok.com/stainless-steel-vs-brass-threaded-inserts-for-plastic
- https://www.spirol.com/assets/files/Brass_vs_SST_Inserts_White_Paper.pdf
- https://www.machinedesign.com/materials/article/21831579/brass-and-steel-threaded-inserts-a-comparison

## 2. M3 / M5 sizing and hole geometry

The two dominant standards in the hobby/maker world are:

- **CNC Kitchen "Standard"** - M3 x 5.7 mm long, hole 4.0 mm. M5 x 5.8 mm long ("Short"), hole ~6.4 mm.
- **Voron-spec / Ruthex M3x5x4** - 5 mm long, 4.0 mm OD, hole 4.7 mm. Used across the Voron 3D printer ecosystem; specifically tuned for ABS/ASA prints.

For the grinder, the CNC Kitchen Standard sizes are the right baseline because they have the best published pull-out data and the most retailer redundancy (CNC Kitchen direct, Vector3D, Repkord, KB-3D, Prusa).

Geometry rules from CNC Kitchen and FacFox:

- Hole should be **straight, not tapered**, but with a small lead-in chamfer at the top to prevent burr-up.
- Blind hole **depth = insert length + ~1-2 mm** so displaced plastic has somewhere to go. If you skip this you get a plastic plug that prevents the insert from fully seating, and the bolt will bottom out on goo instead of the insert face.
- Wall thickness around the hole: **at least 2x the insert OD**. For an M5 insert (~6.4 mm OD) that is ~13 mm of wall. Less than that and the insert will bulge or split the part during install.
- Use **4-6 solid perimeters** around the hole, not infill. Walls give torque resistance; infill does not.
- **Holes printed in Z (vertical) are more dimensionally accurate than holes printed in X/Y** - on horizontal holes the top sags and the hole comes out elliptical. For a bearing block where the insert axis is horizontal, this matters - print a test cube and measure before committing the final part.

Sources:
- https://www.cnckitchen.com/blog/tipps-amp-tricks-fr-gewindeeinstze-im-3d-druck-3awey
- https://facfox.com/docs/kb/mastering-heat-set-inserts-a-professionals-guide-to-durable-3d-printed-threads
- https://github.com/VoronDesign/Voron-Afterburner/issues/15

## 3. Installation

Tooling:

- **40W or higher temperature-controlled soldering iron** (TS100, Pinecil, Hakko FX-888 all fine).
- **Dedicated heat-set tip** that matches the insert thread (CNC Kitchen, Trianglelab, or Adafruit 4249 sell these). A chisel tip works in a pinch but does not center the insert well, and it is the #1 reason inserts go in crooked.
- A flat reference surface to align the part square to the iron. CNC Kitchen sells a press jig; a bench vise plus a square works fine for a workshop build.

Temperatures (iron set ~10-20 deg C above print temp):

- PLA: ~225 deg C
- PETG: ~245-260 deg C
- ABS: ~265 deg C

Technique:

1. Place the part on a flat surface, drop the insert into the hole - it should sit half-in by gravity.
2. Bring the iron tip down vertically into the insert. **Push only with the iron's weight**, do not force.
3. Push the insert in to about 90% depth using only the iron, then **switch to a flat metal tool** (a cold M3 bolt head, end of a pair of pliers, etc.) to set the final depth flush. This prevents the insert from being pushed too deep and from sinking after you remove the iron.
4. Wait ~30 sec for the plastic to fully solidify before applying any side load. FacFox recommends 2-3 minutes before threading a bolt at full torque.

Total install time per insert: ~10-15 sec of heat application.

Sources:
- https://hackaday.com/2019/02/28/threading-3d-printed-parts-how-to-use-heat-set-inserts/
- https://www.cnckitchen.com/blog/tipps-amp-tricks-fr-gewindeeinstze-im-3d-druck-3awey

## 4. Pull-out and torque numbers

This is the load-bearing data for the grinder design. Numbers are from CNC Kitchen's "Cheap vs Expensive" comparative test with M3 inserts in PLA:

| Configuration | Pull-out force | Torque-out |
|---|---|---|
| Ruthex (premium brass, knurled+flanged) | 181 kg avg (~399 lbf, ~1775 N) | 3-4 Nm before bolt head sheared |
| Generic eBay brass | 157 kg (~346 lbf) | 3-4 Nm |
| Cheap injection-molded brass | 39 kg (~86 lbf) | 3-4 Nm but easy to spin under impact |
| Direct screw into bare PLA (no insert) | 142 kg (~313 lbf) | ~1 Nm before plastic threads stripped |

Two important takeaways for the grinder:

- **Premium inserts are 4x stronger in pull-out than the cheap AliExpress lookalikes**, even though both look identical in photos. The difference is the knurl geometry and the flange chamfer. For bearing blocks that take live torque, this is worth the price - we are talking $0.30 vs $0.10 per insert.
- **Torque-out failure mode is the M3 bolt itself, not the insert.** That means a properly installed brass insert in PLA can take more torque than the steel fastener it is hosting. In PETG the insert is the same story, but the surrounding part is more vibration-tolerant.

Versus alternatives:

- **Press-fit threaded inserts** (no heat) - lower pull-out, easier for soft plastics, not suitable here.
- **Self-tapping screws into bare plastic** - one-time use, ~1 Nm torque ceiling, plastic threads strip on second assembly. Fine for non-load-bearing covers, **not for bearing blocks**.
- **Tap a thread directly in plastic** - same problem as self-tapping; deteriorates with re-assembly.

Sources:
- https://www.cnckitchen.com/blog/threaded-inserts-for-3d-prints-cheap-vs-expensive
- https://www.protolabs.com/resources/blog/tips-for-threading-and-adding-inserts-in-3d-printing/
- https://hackaday.com/2024/04/15/alternate-threaded-inserts-for-3d-prints/

## 5. Brands and sources (M3 + M5)

Ranked by recommendation:

1. **CNC Kitchen Standard / Voron** (cnckitchenus.store, repkord.com, vector3d.shop). M3 x 5.7 mm: ~$15 for 100 pieces. M5 short: ~$15 for 50 pieces. Best published test data, made in Germany, predictable QC.
2. **Ruthex** (ruthex.de or Amazon) - measured equal-or-better than CNC Kitchen in pull-out tests. Same price band.
3. **McMaster-Carr** - reliable but not specifically branded as the "knurled heat-set for 3D printing" geometry. Their heat-set lookup is under "Heat-Set Inserts for Plastic" (e.g. 94459A series for metric brass). Slightly more expensive but next-day shipping in the US.
4. **Prusa** - rebadged CNC Kitchen, no advantage unless ordering with a printer.
5. **AliExpress / generic Amazon "440 piece kit"** - usable for non-structural applications (covers, brackets), 4x weaker in pull-out. Not for bearing blocks or gear mounts on the grinder.

Sources:
- https://cnckitchenus.store/products/heat-set-insert-m3-x-5-7-100-pieces
- https://cnckitchen.store/products/heat-set-insert-m5-x-5-8-short-version-50-pieces
- https://vector3d.shop/products/heat-set-insert-m5-short
- https://www.adafruit.com/product/4249

## 6. Failure modes and how to avoid them

| Failure | Cause | Prevention |
|---|---|---|
| Insert spins under torque | Hole oversized, walls too thin, or insert pushed in cold-and-melted plastic re-froze without keying into knurls | Hit hole-size target +/- 0.05 mm, 4-6 perimeters, allow 30 sec cooling |
| Insert sinks below surface during install | Pushed too long with iron alone | Stop at 90% with iron, finish with cold tool |
| Insert tilted off-axis | Soldering iron not square to surface | Use a press jig or align against a square |
| Plastic burns / discolors around insert | Iron too hot or held too long | Calibrate iron to print temp +10-20, total time under 15 sec |
| Insert pulls out under axial load | Cheap insert + thin walls + PLA in vibration | Use premium insert, PETG, walls >= 2x OD |
| Bolt strips threads inside insert | Cross-threading on first bolt insertion (plastic burr clogged threads) | Hole 1-2 mm deeper than insert; chase threads with a clean bolt before final assembly |
| Vibration loosening | PLA part fatiguing around the insert | Print part in PETG (better layer adhesion, not brittle); use threadlocker or nylock nuts on the bolt side |

For the bike-powered grinder specifically, **PLA is the wrong choice** for any part that hosts an insert exposed to pedal-torque vibration. PLA is brittle in shock-load and will spider-crack around the insert over hundreds of pedal cycles. PETG is the right call: better impact tolerance, better layer adhesion, only modestly more expensive.

ABS or ASA would be even better for outdoor durability, but they are noticeably harder to print well on the Bambu A1 Mini (open-frame, no enclosure) - PETG is the practical sweet spot.

Sources:
- https://facfox.com/docs/kb/mastering-heat-set-inserts-a-professionals-guide-to-durable-3d-printed-threads
- https://ultimaker.com/learn/petg-vs-pla-vs-abs-3d-printing-strength-comparison/
- https://forum.prusa3d.com/forum/english-forum-general-discussion-announcements-and-releases/physical-strength-pla-vs-petg/

---

## Bottom line for the grinder build

Buy:

- **CNC Kitchen Standard M3 x 5.7 mm brass heat-set inserts**, 100-pack, ~$15 (cnckitchenus.store or Repkord).
- **CNC Kitchen Short M5 x 5.8 mm brass heat-set inserts**, 50-pack, ~$15.
- **CNC Kitchen heat-set soldering iron tips** for M3 and M5 (one of each).

Print bearing blocks, gear mounts and axle supports in **PETG**, with 4-6 perimeters and at least 2x-OD wall thickness around every insert hole. Holes are **4.0 mm** for M3 and **6.4 mm** for M5, with depth = insert length + 1-2 mm.

Install at **iron temp = print temp + 10-20 deg C** (PETG: ~245-260 deg C), 90% in with the iron, finish with a cold flat tool, wait 30 sec before threading a bolt.

This combination should comfortably exceed any torque the bike pedals can put through an M5 fastener. The bolt will fail before the insert does.

## Open questions for Isaiah

1. **Operating environment** - is the grinder used indoors only, or will it ever be left in a humid garage for weeks? (Affects whether stainless inserts on a couple of the most-exposed bolts is worth the brass-galvanic risk.)
2. **Filament choice** - confirmed PETG for the structural parts? If you are leaning ABS for the gear mounts specifically (cheaper, slightly stronger torque), the A1 Mini's lack of enclosure is the limiting factor; consider farming those parts out to a Bambu X1C or printing in ASA on a hotter day.
3. **Stainless reinforcement plates** - the brief mentions stainless steel plates bonded with silicone at the bearing blocks. The heat-set insert plan above lives in the plastic, not in the stainless plate. If the bolt path goes plastic -> insert -> through-hole in stainless, that is fine. If you want the bolt to thread directly into the stainless, you skip the insert entirely on that bolt and tap the stainless. Worth confirming the load path on each bolt before ordering quantities.
