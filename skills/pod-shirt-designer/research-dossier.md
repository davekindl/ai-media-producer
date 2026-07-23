# Research Dossier -- pod-shirt-designer

Source provenance for the prompt catalog, niche selection, and the print pipeline.
Organized by type. This file backs the catalog claims; it is a reference record, not
operating instructions (see `SKILL.md` for the workflow).

> The skill was built via the niche-skill-forge methodology on 2026-05-16 from 50+
> sources across POD platforms, Reddit communities, YouTube tutorials, and market
> research. The per-type counts below are recorded from that build (see `CHANGELOG.md`
> v1.0.1 "Research Sources"). Where a specific claim in the technique library cites a
> number (market size, sales/month), that number originates from the corresponding
> source category here.

---

## 1. POD Platforms & Trending Niches (28+ sources)

Platform docs, marketplaces, and market-sizing reports used to choose the trending
niches in `techniques/library/03-trending-niches.md` and the platform export specs in
`techniques/library/05-technical-pipeline.md` (T1 dimensions table).

- Printify -- product catalog, print-area dimensions, DTG color behavior
- Printful -- file/resolution requirements (up to 4500x5400px, 300 DPI, PNG)
- Etsy -- POD category trend signals, listing conventions
- Amazon Merch on Demand -- file spec (4500x5400px, 300 DPI, PNG), tier/listing rules
- Redbubble -- minimum upload size (2400x3200px), format
- Grand View Research -- POD market sizing ($11-13B in 2025, 25.8% CAGR)

Niche market-size figures cited in the library (anime $3.3B, fitness $295B, pet $1.5B AI-pet)
trace to this category's market-research sources.

## 2. Design Techniques (21 technique cards)

Prompt-construction and print-safety patterns behind
`techniques/library/01-prompt-architecture.md` and `02-design-styles.md`, plus the
transparency and color rules in `05-technical-pipeline.md`.

- kie.ai docs -- GPT-Image-2 endpoint, `background: "transparent"` native-alpha
  parameter, aspect-ratio/resolution constraints (1:1 capped at 2K), model IDs
  (`gpt-image-2-text-to-image`, `nano-banana-pro`)
- fal.ai -- comparative image-model technique notes
- OpenArt -- prompt-structure patterns (style anchoring, composition specs)
- Aiarty -- upscaling / resolution-recovery guidance for print

> **Transparency note (authoritative):** kie.ai GPT-Image-2 returns true RGBA PNG via
> `"background": "transparent"`. The skill does NOT use rembg/background-removal
> post-processing. Earlier drafts (v1.0.0) assumed no native transparency; that was
> corrected in v1.0.1 (see `CHANGELOG.md`). The technique index, `SKILL.md`, library
> file 05, and `pod_pipeline.py` are all aligned to native transparency.

## 3. Untapped Niches (41 searches)

Discovery searches behind `techniques/library/04-untapped-niches.md` (U1-U10). Each
prospect was selected for a documented competition gap plus an audience signal.

- Magyar Peter / Tisza political merch (HU) -- near-zero competition, voter-base signal
- Eldest Daughter Syndrome -- TikTok view volume vs. zero merch
- Vibe Coding identity -- dev-community phrase trends
- Dumbphone / digital minimalism -- screen-time-reduction trend data
- Micro-retirement, sleepmaxxing, analog renaissance, neo-homesteader, solarpunk,
  Hungarian absurdist expressions -- trend + merch-gap searches

## 4. Market Data (summary)

- POD market: $11-13B (2025), 25.8% CAGR -- Grand View Research
- Per-niche sizing and top-seller sales/month figures: see in-library citations,
  sourced from category 1 above.

---

## Maintenance

- This dossier is a build-time record. When a niche or platform spec changes, update the
  matching `techniques/library/*.md` file first, then reflect the source change here.
- Do not add unverifiable source URLs. Record source *categories* and the counts captured
  at build time unless a specific, checkable citation is available.
- Reference designs (gold standard): collect your own validated print-ready designs locally as a reference set.
