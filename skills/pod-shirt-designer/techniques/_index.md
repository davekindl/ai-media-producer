# Technique Index -- pod-shirt-designer

Discovery directory. Scan this to match user requests to the best prompt template.
Total: 45+ prompt templates across 5 categories.

---

## Prompt Architecture  .  [`library/01-prompt-architecture.md`]

- **P1** The 4-Part Skeleton -- Universal foundation: [Style] + [Subject] + [Composition] + [Output Spec]
- **P2** The 7-Part Formula -- GPT-Image-2 optimized structured prompt with scene/subject/details/artifact/style/constraints/output
- **P3** Style Anchoring -- Reference real-world aesthetics ("Kodak Portra palette", "Art Deco travel poster") to trigger consistent styles
- **P4** Typography-First Template -- #1 selling POD format: bold text + small illustration in badge composition
- **P5** Vector Artist Directive -- Print-safety override: append to any prompt to force fabric-friendly output

## Design Styles  .  [`library/02-design-styles.md`]

- **S1** Typography + Illustration Hybrid -- #1 seller: text + icon in badge format
- **S2** Distressed Vintage / Retro -- Worn ink, halftone dots, earth tones, universally appealing
- **S3** Y2K / 90s Revival -- Chunky fonts, neon gradients, chrome text, nostalgia
- **S4** Anime / Japanese Streetwear -- Manga panels, glitchcore, subtle fandom, bootleg tour posters
- **S5** Gym / Fitness / Pump Cover -- Greek god, pump cover humor, vintage bodybuilding, powerlifting dark
- **S6** AI / Tech Culture -- Architecture-as-art, vibe coding humor, retro tech, fake startups
- **S7** Fictional Brands / Parody Logos -- Outperforming quotes in 2025-2026: fake institutions and satirical seals
- **S8** Minimalist / One-Line / One-Color -- Clean, sophisticated, works on any shirt color
- **S9** Profession / Micro-Community -- Inside jokes for specific tribes, highest conversion per impression
- **S10** Dark / Gothic / Skull -- Evergreen: metal, biker, gym, alternative lifestyle crossover

## Trending Niches (Top 5 + Deep Dives)  .  [`library/03-trending-niches.md`]

- **N1** Anime / Manga Streetwear -- $3.3B market, 5 sub-style prompts (panel rip, glitchcore, subtle, bootleg, vintage)
- **N2** Fitness / Gym Culture -- $295B market, 5 sub-style prompts (greek god, pump cover, vintage BB, powerlifting, CrossFit)
- **N3** Pet Personalization -- $1.5B AI-pet market, breed-specific humor, retro pet portraits
- **N4** Vintage / Retro / Fictional Brands -- Fictional logos outperforming motivational quotes
- **N5** Profession / Micro-Community -- 13,500+ sales/month for top sellers, winning formula: profession x aesthetic x humor
- **N6** AI / Tech Culture -- LOW competition for genuinely clever designs, tech workers pay $30-40

## Untapped Niches (10 Novel Prospects)  .  [`library/04-untapped-niches.md`]

- **U1** Magyar Peter / Tisza Political Merch -- Near zero competition, 2-3M voters, just inaugurated (HU)
- **U2** Eldest Daughter Syndrome -- Millions of TikTok views, zero merch, women 20-40
- **U3** Vibe Coding Identity -- "Senior Vibe Engineer" / "it mostly works", dev community
- **U4** Dumbphone / Digital Minimalism -- "Unreachable by Design", 35% UK cutting screen time
- **U5** Micro-Retirement Lifestyle -- Zero competition, 13% of millennials planning one
- **U6** Hungarian Absurdist Expressions -- Bilingual humor, 2M+ diaspora, evergreen
- **U7** Sleepmaxxing Identity -- $27B sleep tech market, biohacker community
- **U8** Analog Renaissance -- Vinyl $1B+, film +127%, identity merch gap
- **U9** Neo-Homesteader (Urban Gen Z) -- Existing merch targets wrong demographic
- **U10** Solarpunk -- Only optimistic futurist aesthetic, 1 store exists

## Technical Pipeline  .  [`library/05-technical-pipeline.md`]

- **T1** Resolution Pipeline -- AI output (72 DPI) to print-ready (4500x5400 at 300 DPI)
- **T2** Transparent Background (Native Alpha) -- kie.ai GPT-Image-2 supports native transparency via `"background": "transparent"`; output is true RGBA PNG, no removal post-processing
- **T3** Color Profile and Format -- sRGB, PNG-24, never CMYK, problem color chart
- **T4** Aspect Ratio Selection -- 3:4 for shirts, 1:1 for chest (max 2K), 16:9 for all-over
- **T5** End-to-End kie.ai Pipeline -- Generate (native transparent) -> poll -> download -> QC -> resize -> export
- **T6** Artifact Checklist -- 10-point pre-export quality control
- **T7** Model Selection -- Which AI model for which design type
- **T8** Copyright Safety -- Legal checklist before listing any design
