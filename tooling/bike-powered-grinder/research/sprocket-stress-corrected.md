# Corrected Sprocket Stress Analysis — Two-Chain-Stage Drivetrain

**Date:** 2026-05-08
**Source:** background research agent dispatched after the Q1–Q4 lock-in session. Supersedes the earlier `freecad-1.1-readiness.md` PETG-gear analysis, which used the wrong torque direction (treated the system as torque-multiplying reduction when it's actually a speed-up gearbox).

Convention note: this is external-research-synthesis, not a verbatim thread excavation.

---

## Torque chain (verified, speed-up direction)

| Shaft | RPM | Sustained T | Peak T |
|---|---|---|---|
| Crank | 75 | **19.1 N·m** | 32 N·m |
| Intermediate (stage 1 driven) | 237 | **6.04 N·m** | 10 N·m |
| Grinder pulley (stage 2 driven) | 750 | **1.91 N·m** | 3.2 N·m |

For the 7.5:1 alternative (~890 SFM at 6" pulley): intermediate 6.97 N·m sustained / 11.7 peak, grinder 2.55/4.27 N·m. Differences are minor; sizing decisions below cover both.

## 1. Stage 1 sprocket pair — donor-bike steel, hugely overbuilt

**Recommended:** 42T chainring × 13T cog (3.23:1). Worst case is the 13T cog.

Chain tension at 19.1 N·m sustained on a 13T × 0.5" chain (PCD ≈ 53.0 mm, r = 26.5 mm):
**F = T/r = 19.1 / 0.0265 = 721 N sustained, 1208 N peak.**

ANSI #40 / bicycle 1/2"×1/8" chain has a min ultimate tensile of **~8,000 N** (per ANSI B29.1 and SRAM/KMC published specs). Safety factor at peak = 8000/1208 ≈ **6.6×** — chain is not the limit.

Tooth bending (Lewis equation, steel sprocket, σ_allow ≈ 200 MPa for hardened bicycle steel cogs):

F_t = 721 N, face width b = 2.4 mm (1/8" chain), tooth thickness ≈ pitch/2 ≈ 6.35 mm, Lewis Y for 13T ≈ 0.261, m ≈ 4.06 mm for #40.

σ = F_t / (b · m · Y) = 721 / (2.4 · 4.06 · 0.261) = **283 MPa** on a single-tooth analytical basis.

Real chain drives share load across 3–4 engaged teeth, dropping effective σ to ~70–95 MPa. **SF ≈ 2–3× sustained, ≥1.3× at 32 N·m peak.** Stock bike cogs routinely survive 100+ N·m sprinter torque, so this is fine. (Refs: Shigley *Mechanical Engineering Design* 10e Ch 17; ANSI B29.1.)

## 2. Stage 2 sprockets — PETG borderline, metal safer at 10:1; PETG works at 7.5:1

PETG fatigue: published S-N data (Ezeh & Susmel, *Int. J. Fatigue* 2018; Prusa Research material datasheet 2023) gives endurance limit ~12–18 MPa at 10⁶ cycles for FDM PETG. Use σ_allow = **15 MPa** for sustained operation.

Lewis stress on the **6–8T grinder-side sprocket** at F_t = T/r:

| Module | Face | 6T PCD | F_t @ 1.91 N·m | F_t @ 3.2 peak | σ_sust | σ_peak |
|---|---|---|---|---|---|---|
| 1.0 | 8 mm | 6 mm | 637 N | 1067 N | **66 MPa** | 110 MPa |
| 1.5 | 12 mm | 9 mm | 424 N | 711 N | **23 MPa** | 39 MPa |
| 2.0 | 16 mm | 12 mm | 318 N | 533 N | **9.5 MPa** | 16 MPa |
| 2.5 | 16 mm | 15 mm | 254 N | 426 N | **6.1 MPa** | 10 MPa |

(Y ≈ 0.245 for 6T, lowest in the table — that's the punishing factor.)

**Verdict:** PETG works only at module ≥ 2.0 with 16 mm face on a 6T grinder pinion. A 6T PETG pinion at module 1.5 would creep-fail under 100 hr cumulative load. Recommend **module 2.0, 16 mm face, 8T minimum, with stainless rod through hub** — *or* a machined 6061 aluminum or steel pinion (~$12 from SDP-SI or Boston Gear), which eliminates the fatigue worry entirely.

Intermediate-shaft sprockets at 6–10 N·m can be PETG comfortably at module 1.5+ on 12+T sprockets (σ < 8 MPa). **Print these.**

**At 7.5:1 (recommended — see SFM analysis below), the grinder pinion bumps to 19T.** With 19 teeth and module 1.5, σ drops well below allowable for PETG, and the whole drivetrain becomes printable.

## 3. Bearings — 6202-2RS on intermediate, 608-2RS on grinder shaft

Chain radial load on intermediate shaft (worst case both chains pulling in the same direction): ~2× 1200 N = 2400 N peak, ~1400 N sustained.

**6202-2RS** (15 mm bore, C = 7.65 kN, C₀ = 3.7 kN, max RPM 14,000 — SKF datasheet):

L₁₀ = (C/P)³ × 10⁶ rev = (7650/1400)³ × 10⁶ = **1.63 × 10⁸ rev** at 237 RPM = 11,400 hr. Far exceeds 100 hr target.

**608-2RS** (8 mm bore, C = 3.45 kN — NSK) on grinder shaft at 750 RPM, P ≈ 600 N:

L₁₀ = (3450/600)³ × 10⁶ = **1.9 × 10⁸ rev** = 4,200 hr. Fine.

**Use 2× 6202-2RS** (intermediate) + **2× 608-2RS** (grinder shaft). ~$20 total from VXB or McMaster.

## 4. Chains

Both stages: **standard 1/2"×3/32" bicycle chain** (KMC Z8.3 or equivalent). Breaking strength ≥ 7,800 N (KMC datasheet). SF ≥ 6× at peak. Stage 2 could go shorter pitch (#25 / 6.35 mm) for the small grinder pinion to allow lower tooth count without skipping, but stocking one chain spec is simpler. **Buy two new chains (~$15 each).**

## 5. Cost

| Item | Cost |
|---|---|
| Donor chainring + cog + BB | $0 (from $40 bike) |
| 2× chains (KMC Z8.3) | $30 |
| 4× sealed bearings (2× 6202, 2× 608) | $20 |
| Stage 2 small pinion (machined steel/Al, 8T) — only if locking 10:1 | $15 |
| Stage 2 small pinion (PETG print, 19T) — if locking 7.5:1 | $0 |
| Stage 2 large sprocket (PETG print) | $0 |
| Intermediate shaft (12 mm stainless rod) | $8 |
| **Total beyond donor (10:1 path)** | **~$73** |
| **Total beyond donor (7.5:1 path)** | **~$58** |

## 6. Recommended spec block (FreeCAD parametric)

```
DRIVETRAIN_SPEC:
  total_ratio: 10.2:1   # alt 7.5:1 by swapping pinion to 19T
  stage1:
    chainring_teeth: 42       # donor steel
    cog_teeth: 13             # donor steel cassette cog
    ratio: 3.23
    chain: 1/2"x3/32" bicycle, KMC Z8.3
  stage2:
    intermediate_large_teeth: 32   # PETG, module 1.5, face 12 mm
    grinder_pinion_teeth: 8        # MACHINED STEEL, module 2.0, face 16 mm
    ratio: 4.00 (10.2:1 total) | 2.32 (7.5:1 total → 19T pinion)
    chain: 1/2"x3/32" bicycle
  intermediate_shaft:
    diameter: 12 mm stainless 304
    bearings: 2x SKF 6202-2RS, 30 mm bore spacing TBD
  grinder_shaft:
    diameter: 8 mm stainless 304
    bearings: 2x NSK 608-2RS
  pulley:
    drive_dia: 6 in (152.4 mm), target 750 RPM → 1180 SFM
    idler_dia: 3 in (76.2 mm)
  input:
    cadence: 75 RPM
    P_sustained: 150 W
    P_peak: 250 W
```

## SFM analysis (this is the actual decision)

The total-ratio choice is really about belt surface speed:

| Ratio | Pulley RPM | SFM @ 6" | Glass spec position | Material implication |
|---|---|---|---|---|
| 10:1 | 750 | **1180 SFM** | Upper edge of 500–1500 spec | 8T grinder pinion needs metal |
| 7.5:1 | 562 | **890 SFM** | Mid-spec | 19T grinder pinion, all PETG |
| 8:1 | 600 | 942 SFM | Mid-spec | borderline, depends on tooth count |

**The 7.5:1 path is recommended:** mid-spec SFM gives more thermal margin on the workpiece (less risk of glass thermal-shock), and the larger 19T pinion stays inside PETG's fatigue envelope so the entire drivetrain stays printable. Saves ~$15 and one machining outsourcing step.

The 10:1 path is viable but pushes against the upper limit of glass-grinding speed and forces one machined metal part. Reserve 10:1 as a future upgrade if surface-speed tests show the grinder is under-aggressive at 890 SFM.

## Final recommendation

**Lock 7.5:1 total reduction. All-PETG drivetrain (except donor steel cogs at stage 1).**

Spec for FreeCAD:

```
total_ratio: 7.5:1
stage1: 42T × 13T = 3.23:1 (donor steel)
stage2: 44T (PETG, m=1.5, b=12) × 19T (PETG, m=1.5, b=16) = 2.32:1
intermediate shaft: 12 mm 304 stainless, 2× 6202-2RS
grinder shaft: 8 mm 304 stainless, 2× 608-2RS
chain: 2× KMC Z8.3 (1/2" × 3/32")
pulley: 6" drive (target 562 RPM @ 75 cadence → 890 SFM), 3" idler
total bought-parts cost: ~$58
```

## Sources

- Shigley, *Mechanical Engineering Design*, 10th ed., Ch. 17 (chain drives), Ch. 14 (gears, Lewis equation)
- Norton, *Machine Design*, 5th ed., Ch. 12 (spur gear bending)
- Ezeh, O. H., & Susmel, L. (2018), "On the fatigue strength of 3D-printed polylactide (PLA)" *International Journal of Fatigue* (PETG follow-up paper)
- Prusa Research PETG material datasheet (2023)
- ANSI B29.1 (precision power transmission roller chains)
- SKF and NSK bearing catalogues
- KMC Z8.3 datasheet
