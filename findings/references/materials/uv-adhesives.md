# References — UV Adhesives

External sources for UV-cure adhesives and resins. Cross-references `topics/materials/uv-adhesives.md` and `products/the-gem/seam-construction.md`.

## Optical-grade UV adhesives (for invisible seams)

The Gem's "invisible bond line" target needs UV-stable, non-yellowing optical adhesives. Source threads consistently named one company:

- **Norland Products** — optical-grade UV-cure adhesives (NOA series). Used in optical/photonics manufacturing for refractive-index-matched bonding. Their datasheets list refractive index, viscosity, cure time, and long-term yellowing data — exactly the specs the Gem build needs. URL: https://norlandproducts.com/
- **Norland NOA 61 product page + TDS** — Canonical pick for glass-glass bonding. Cured RI 1.56 (note: NOT a true match for soda-lime ~1.52 or borosilicate ~1.47). Viscosity 200–300 cps. URL: https://norlandproducts.com/product/noa-61/
- **Norland NOA 81 product page + TDS** — More thermally robust than NOA 61. URL: https://norlandproducts.com/product/noa-81/
- **Norland NOA 88 product page + TDS** — Higher Shore D (90) for stiffer stacks. URL: https://norlandproducts.com/product/noa-88/
- **Norland Optical Adhesive Selection Guide PDF** — Master comparison chart across NOA grades: viscosity, RI, cure depth, hardness, temperature range. Use this to pick the right NOA for The Gem. URL: https://www.techoptics.com/media/1037/norland-optical-adhesives-selection-guide.pdf
- **Norland — "Notes on Bonding Holograms" PDF** — Norland's own application note on even-cure technique and lamp choice. Directly applicable to optical bonding workflow. URL: https://norlandproducts.com/wp-content/uploads/2025/03/Notes-on-Bonding-Holograms.pdf
- **Edmund Optics — Norland adhesives catalog** — Distributor-curated comparison and product detail. URL: https://www.edmundoptics.com/f/norland-optical-adhesives/11818/
- **Incure — "How Thick is Optical Adhesive? Bond Line Thickness Guide"** — Practitioner reference for actual bond-line targets: 3–50 µm for precision optical bonds (lens assemblies), 50–250 µm for general optical-component assembly / display lamination. Useful counter to vague AI-thread numbers. URL: https://incurelab.com/wp/how-thick-is-optical-adhesive-navigating-bond-line-thickness-for-optimal-performance/
- **Uvitron — "Why UV-cured adhesives yellow over time"** — Industry explainer on photo-oxidation and yellowing in continuously-lit environments. URL: https://www.uvitron.com/blog/why-do-some-uv-cured-adhesives-turn-yellow-over-time/
- **Incure — UV resin yellowing notes** — Vendor's discussion of UV-glue durability factors over time. URL: https://incurelab.com/wp/uv-resin-yellowing

> Quote from `topics/materials/uv-adhesives.md`: "Standard UV adhesives without UV stabilizers: yellow visibly in 30 days of direct sunlight. Optical-grade UV adhesives (Norland): maintain clarity long-term."

## Hobbyist UV resins (lower spec, lower cost)

Used for the seam-application work where optical perfection isn't required (e.g. UV resin over solder seams in stained glass).

- **Solarez** — surfboard repair resins, also sold for hobby/jewelry use. Cures fast under UV lamp or sunlight.
- **Padico** — Japanese hobby UV resin brand. Common in jewelry/craft applications.
- **Counter Culture DIY UV** — referenced in source threads as another hobby-grade option.

## Doming / glazing resins (self-leveling clear topcoats)

Different category from UV adhesive — these are pour-on, self-leveling, glass-clear topcoats. Useful for sealing finished pieces.

- [unvetted] **ArtResin** — common hobbyist self-leveling epoxy resin.
- [unvetted] **EnviroTex Lite** — older, well-established pour-on resin.

## TODO — sources Isaiah may want to seed when ready

- [x] Norland NOA-XX product comparison — partially done above (NOA 61 / 81 / 88 distinguished); a full chart would still be useful
- [ ] Optical-bonding application notes / case studies from Norland's site
- [ ] Forum threads on UV adhesive longevity in continuously-lit terrarium environments
- [ ] Comparison: Norland vs Wacker SilGel vs Dow optical silicones for clarity + bond strength
- [x] Refractive-index-matched UV adhesives — done (see RI-match section below)

## Refractive-index-matched grades (added 2026-05-05)

> **Important finding for The Gem.** Norland NOA 61 (RI 1.56) is *not* a true match for soda-lime (1.52) or borosilicate (1.47) glass — the seam will be faintly visible. Better grades exist:

- **NOA 65 (RI 1.524) — soda-lime match.** Essentially perfect for soda-lime glass. Designed as a low-strain flexible bond for dissimilar-CTE pairings (plastic-to-glass, lens-in-metal-mount). **The strongest soda-lime candidate Norland makes.** URL: https://norlandproducts.com/product/noa-65/ — TDS: https://norlandproducts.com/wp-content/uploads/2025/02/NOA-65-TDS.pdf
- **NOA 148 (RI 1.48) — borosilicate match.** Closest mainstream Norland grade to borosilicate (~1.47). Norland markets it explicitly for "glass-to-glass bonding." ~0.01 RI mismatch is essentially invisible. URL: https://shop.amstechnologies.com/NOA-148-Optical-Adhesive-1oz-bottle/C007106-6
- **NOA 138 (RI 1.38) and NOA 1315 (RI 1.315)** — too low for borosilicate; only useful for fluoropolymer / low-index media bonding. Not for The Gem.
- **NOA 1625 (RI 1.625) and NOA 170 (RI 1.705)** — high-index, intended for dense flint glass, not soda-lime / borosilicate. URL: https://norlandproducts.com/wp-content/uploads/2025/03/NOA-170-TDS.pdf

**Bottom line:** for The Gem, NOA 65 (soda-lime) or NOA 148 (borosilicate) — pick based on glass type. NOA 61 was wrong by 0.04 RI; NOA 65 is wrong by 0.004. Visually a meaningful difference.
