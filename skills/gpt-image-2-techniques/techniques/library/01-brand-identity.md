# Brand Identity & Design Systems

13 techniques. Each entry includes prompt template, source, gotchas, stack notes, and (when relevant) cross-references.

Use the skill's discovery step to pick the right one for a given request.

---

## A1-T1 — One-Prompt Brand Guideline From One Image

**Score:** ★★★★☆ (4/5)  
**Source:** [@JohnnotJon, X 2026-04-22](https://x.com/JohnnotJon/status/2046990940729188368)  
**Use case:** Reverse-engineer a complete brand system (logo, palette, typography, applications, voice line) from one inspiration photograph. Single A3-portrait page output.

**Prompt template:**

```
Analyze the uploaded reference image and generate a single-page brand guideline document for a fictional {brand_name} in the {industry} category. The page is A3 portrait, 4K, matte paper texture.

Layout (exact positions):
- Top-left: the logo mark extracted/re-drawn as a flat vector, word "{BRAND_NAME}" in ALL CAPS underneath
- Top-right: 5 color swatches as 80pt squares with exact hex codes typeset underneath in monospace 11pt (e.g., "#0A2540", "#E8F4F8")
- Middle-left: typography specimen — heading typeface at 48pt showing "Aa 01" pairing, body typeface at 14pt with "The quick brown fox jumps over the lazy dog"
- Middle-right: 3 application mockups (business card top-down, app icon on iPhone home screen, signage on glass door), each 180pt tall
- Bottom: single-line voice statement in italic 18pt: "{voice_line}"

Derive all colors, shapes, typography from the uploaded image. Preserve palette warmth and geometric vocabulary. Keep all text sharp and verbatim. No decorative flourishes, no duplicate text, no watermark. 4K, 3:4 aspect ratio.
```

**Gotchas:** Logo extracted is pixel art, not vector — never promise as final. If source has visible text, the model samples it into the brand name. 1:1 cannot do 4K — use 3:4.

**Stack with:** Pair with Nano Banana Pro for photo variants. Re-feed this page as a reference slot in subsequent calls (a1-t3).

---

## A1-T10 — Rebrand Reveal One-Sheet (Before/After Grid)

**Score:** ★★★☆☆ (3/5)  
**Source:** chatimg.ai + hasantoxr X patterns  
**Use case:** Single-image 'before vs after' rebrand visualization across 6-8 applications. Behance showcase format proving new identity works across the business.

**Prompt template:**

```
Single-image brand comparison sheet 16:9 4K, split horizontally. Above: "BEFORE" 36pt sans uppercase. Below: "AFTER" same. Both halves on neutral light gray.

BEFORE half (top): 3x1 grid of existing {brand_name} in OLD palette {old_hex_1, old_hex_2} + OLD typeface ({old_type_description}):
- App 1: logo on business card
- App 2: storefront signage
- App 3: app icon on iPhone home screen

AFTER half (bottom): SAME 3 applications in NEW identity:
- App 1: card with new wordmark "{NEW_WORDMARK}" {new_typeface}, palette {new_hex_1, new_hex_2}
- App 2: same storefront re-signed
- App 3: same phone with new app icon

Card / building / phone IDENTICAL in both halves — only branding changes. Preserve angle, lighting, props, composition. Each tile labeled 9pt mono. Right of both: vertical color strip showing palette.
```

**Gotchas:** 'Identical underlying objects' is hardest part — expect 2-3 rerolls. 'Before' often too generic; pin OLD typeface + palette. For real client, run on actual current identity (a1-t3).

**Stack with:** Pair with a1-t2 (4-panel fan-out) for 'in the wild' follow-up. Together = complete reveal deck in 2 calls.

---

## A1-T11 — SYNTH: Canonical Brand Anchor Workflow

**Score:** ★★★★☆ (4/5) · `synth`  
**Source:** Synthesis a1-t1 + a1-t3 + a1-t5  
**Use case:** Run a1-t1 to generate master brand-anchor page → save as brand_anchor.png → feed as single 'BRAND SYSTEM' reference in every subsequent call. Solves session-to-session drift. Brand reduced to one PNG that persists across the engagement.

**Prompt template:**

```
STEP 1 (a1-t1): Upload mood_image.jpg. Generate single-page master anchor with logo, palette+hex, typography specimen, 3 applications, voice line. Save as brand_anchor.png.

STEP 2 (a1-t3): For every downstream asset, use brand_anchor.png as reference Image 1, labeled "BRAND SYSTEM ANCHOR — pull palette, typography feel, wordmark lockup, voice from this only". Describe only the new subject.

STEP 3 (a1-t5): When full guideline doc needed, re-run each of 8 pages with brand_anchor.png as reference, specifying page type and letting everything inherit.
```

**Gotchas:** Solves drift. Brand becomes one PNG that persists.

---

## A1-T12 — SYNTH: Deck-Grade Brand Reveal in 3 API Calls

**Score:** ★★★★☆ (4/5) · `synth`  
**Source:** Synthesis a1-t1 + a1-t2 + a1-t10  
**Use case:** Compact reveal deck in exactly 3 calls: anchor (essence) + 4-panel fan-out (in the wild) + before/after grid (what changed). Replaces ~1 day designer work with ~15 min orchestration.

**Prompt template:**

```
Call 1 — a1-t1: Brand anchor page = "the essence"
Call 2 — a1-t2: 4-panel thinking-mode fan-out, ref = anchor from Call 1 = "in the wild"
Call 3 — a1-t10: Before/after grid, ref = anchor + client's existing identity = "what changed"
```

**Stack with:** For paid rebrand reveal, Behance case study, consultancy website case page, investor-update post-rebrand.

---

## A1-T13 — SYNTH: Hungarian-Native Brand Pass (HU)

**Score:** ★★★☆☆ (3/5) · `synth`  
**Source:** VentureBeat multilingual coverage + synthesis  
**Use case:** For Hungarian-market B2B client work: GPT-Image-2's 95%+ multilingual text means Hungarian diacritics (é, ö, ő, ü, ű) render cleanly. Bridges 2.0's global advantage with HU business context.

**Prompt template:**

```
Step 1: Generate brand_anchor via a1-t1, but write voice_line + wordmark in Hungarian with full diacritics (e.g., "[YOUR BRAND] · AI üzletre szabva").

Step 2: Verify every diacritic at 4K. If ő or ű artifacts (most common), re-roll with explicit "all Hungarian diacritics rendered sharp and correctly placed".

Step 3: For bilingual, use a1-t2 fan-out with "PANEL 1 = Hungarian" and "PANEL 2 = English" as differentiator.
```

**Gotchas:** ő, ű, á most fragile. Always include 'all Hungarian diacritics rendered sharp'.

**Stack with:** Hungarian-market B2B client work, HUN market outreach, bilingual heroes, Protocol HU PDFs.

---

## A1-T2 — Thinking-Mode Multi-Format Campaign Fan-Out

**Score:** ★★★★★ (5/5)  
**Source:** [@OpenAI launch, X 2026-04-21](https://x.com/OpenAI/status/2046670989719924768)  
**Use case:** One prompt → 4-10 on-brand assets across distinct aspect ratios via O-series reasoning (IG square + Twitter banner + LinkedIn header + vertical story). Replaces 2-3 hours of designer work per variation set.

**Prompt template:**

```
[THINKING MODE ENABLED]

You are producing a 4-panel brand campaign for {brand_name}, a {category} brand. Generate four distinct images that share a locked visual system.

BRAND INVARIANTS (restate on every panel mentally):
- Wordmark: "{BRAND_NAME}" in {ALL CAPS / Title Case}, typeface {sans|serif|display}
- Primary palette: {hex_1}, {hex_2}, {hex_3}
- Accent palette: {hex_4}, {hex_5}
- Texture/material: {e.g., "matte recycled paper"}
- Photographic feel: {e.g., "Kodak Portra 400, 50mm, f/2"}
- Voice line (verbatim once): "{tagline}"

PANEL 1 — IG square (1:1, 2K): Hero {product_1} on {surface}, wordmark bottom-left 40pt.
PANEL 2 — Twitter banner (3:1, 2K): Wide lifestyle {scene_1}, wordmark right, tagline "{tagline}" left.
PANEL 3 — LinkedIn header (16:9, 4K): 3 SKUs in row, wordmark top-left, specs strip "{exact_specs_text}".
PANEL 4 — Vertical story (9:16, 4K): Close-up texture, wordmark small top-center, tagline "{tagline}" bottom-center.

All four: same lighting direction, same palette, same typography hierarchy. No extra text, no duplicate watermarks.
```

**Gotchas:** Thinking mode gated to Plus/Pro Responses API. Cap at 4 panels for production; 8 for draft. Reproducibility is weak — save first winning batch.

**Stack with:** Feed first panel as reference for panels 5-8. Combine with Veeso AI for editable text layers.

---

## A1-T3 — Role-Labeled 16-Reference Brand Lock

**Score:** ★★★★★ (5/5) · `foundational`  
**Source:** [OpenAI Cookbook + fal.ai guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)  
**Use case:** Up to 16 reference images, each labeled by role (PALETTE ANCHOR, LOGO ANCHOR, TYPOGRAPHY ANCHOR, LIGHTING ANCHOR, PRIOR ASSET). Meta-pattern: invariant declaration + role-labeled references. Solves the drift problem.

**Prompt template:**

```
Generate a {asset_type} for {brand_name}.

Reference image roles ({N} attached):
- Image 1 = PALETTE ANCHOR (pull primary + accent colors only)
- Image 2 = TYPOGRAPHY ANCHOR (match feel/weight/kerning, render NEW text)
- Image 3 = LOGO ANCHOR (preserve wordmark spelling/proportions/geometry exactly; do NOT restyle)
- Image 4 = LIGHTING/MOOD ANCHOR (match shadow direction, contrast, atmosphere)
- Image 5 = PRIOR ASSET (match exactly for continuity)

New subject: {subject_description}
New text (VERBATIM, double quotes): "{headline}" {size}, "{subhead}" {size}
Aspect: {9:16|16:9|4:3|3:4|1:1}, resolution: {1K|2K|4K}

Change list: only {what_changes}.
Preserve list: everything not on change list.
Constraints: no extra text, no duplicate logos, no watermark, no stray glyphs.
```

**Gotchas:** Unlabeled refs make model guess — naming roles measurably improves obedience. Logo Anchor still drifts ~20%; spell logo letter-by-letter as belt-and-suspenders. 4-6 well-chosen refs > 16 noisy.

**Stack with:** FOUNDATIONAL — combine with every other technique. Pre-generate master brand-guideline (a1-t1), use as Image 5 = BRAND SYSTEM in subsequent prompts.

---

## A1-T4 — Packaging Family / SKU Shelf Set

**Score:** ★★★★☆ (4/5)  
**Source:** [chatimg.ai + fotor.com](https://www.fotor.com/blog/gpt-image-2-prompts/)  
**Use case:** Coherent product family (3-6 SKUs) with differentiated flavors but unified structural identity. The classic 'shelf impact' shot for merchandising and investor decks.

**Prompt template:**

```
Studio product photography of a {brand_name} {category} family — {N} SKUs side-by-side on {surface}, 85mm f/5.6, soft overhead key with camera-right fill, shallow contact shadow.

Identical silhouette across SKUs. Only label panel + accent color change per variant.

SKU 1: label color {hex_1}, "{VARIANT_1}" ALL CAPS 18pt, icon = {icon_1}
SKU 2: label color {hex_2}, "{VARIANT_2}" 18pt, icon = {icon_2}
SKU 3: label color {hex_3}, "{VARIANT_3}" 18pt, icon = {icon_3}
SKU 4: label color {hex_4}, "{VARIANT_4}" 18pt, icon = {icon_4}

Unified label elements (verbatim, same position):
- Wordmark "{BRAND_NAME}" top-center {typeface} 24pt
- Size callout bottom-right "{size_text}" 10pt monospace
- Cert badges bottom-left: {cert_list}

16:9, 4K. White infinity-curve. Readable small text. No extra bottles, no decorative props.
```

**Gotchas:** >6 SKUs blurs labels at 4K. Trademarked silhouettes refused or genericized. Cert badges <30pt fuzzy.

**Stack with:** Feed shelf shot back as LIGHTING ANCHOR for hero shots. Reuse as PALETTE ANCHOR for social rollout.

---

## A1-T5 — Multi-Page Brand Guidelines Document (8 pages)

**Score:** ★★★★☆ (4/5)  
**Source:** a2e.ai + thinking-mode patterns  
**Use case:** 6-12 page brand guidelines PDF as sequence of individual page renders. Cover, logo rules, color, typography, photography, voice, applications. Client deliverable.

**Prompt template:**

```
Generate page {N} of {total} of brand guidelines for {brand_name}. A4 portrait, print-grade, 4K, 3:4.

Page {N} type: {COVER | LOGO RULES | COLOR | TYPOGRAPHY | IMAGERY | APPLICATIONS | VOICE}.

Header strip (identical every page):
- Wordmark "{BRAND_NAME}" top-left 14pt
- Page label "{N} / {total}  —  {PAGE_TITLE}" top-right 10pt mono
- Thin horizontal rule 20px from top, color {hex_line}

Body (page-specific):
[COVER]: centered wordmark 96pt, subtitle "Brand Guidelines v1.0" 24pt, date "{date}" 12pt.
[LOGO RULES]: wordmark 80pt with clear-space dashed safety square at 50% x-height, three DO/DON'T thumbnails verbatim.
[COLOR]: 5 stacked swatches 60% page width, hex/RGB/CMYK in tabular monospace.
[TYPOGRAPHY]: primary typeface 48pt, full uppercase/lowercase/numerals/symbols specimen.
[IMAGERY]: 4-up grid of mood thumbnails, each one-line rule.
[APPLICATIONS]: 6 mockups — card, letterhead, envelope, website, app icon, social.
[VOICE]: three-column "WE ARE / WE ARE NOT / WE SOUND LIKE".

Footer: "{brand_name}.com  —  ©{year}" 9pt.

Typography hierarchy IDENTICAL across all pages.
```

**Gotchas:** Each page MUST be separate call — one-prompt-all-pages collapses layout. Page numbers '3/8' render wrong; tag VERBATIM. CMYK unreliable.

**Stack with:** Page 1 (cover) becomes ongoing BRAND ANCHOR. Combine with a1-t3 for translated versions.

---

## A1-T6 — Brand Mood Board (9-Cell Flat-Lay)

**Score:** ★★★☆☆ (3/5)  
**Source:** aiforwork.co + fotor.com synthesis  
**Use case:** Flat-lay 9-cell mood board photographed top-down — palette chips, type specimen, texture, hero objects, logo disc, polaroid scene. The asset every brief asks for.

**Prompt template:**

```
Flat-lay mood board top-down on {surface}, 4K, 3:4 portrait. 9-cell implied grid.

Cell 1 (TL): 5-swatch palette strip, paint chips, hex codes "{hex_1}"-"{hex_5}" pencil-labeled.
Cell 2 (TC): typography specimen, heading "{HEADING_TYPEFACE}" 48pt + body "The quick brown fox..." 14pt.
Cell 3 (TR): texture swatch of {material}, side-lit for grain.
Cell 4 (ML): hero object — {object_1}.
Cell 5 (C): logo printed on cardstock as round disc, "{BRAND_NAME}" {typeface_family}.
Cell 6 (MR): secondary object — {object_2}.
Cell 7 (BL): polaroid of {mood_scene} with handwritten caption "{caption}".
Cell 8 (BC): tactile element — {fabric_paper} — partially lifted.
Cell 9 (BR): three fine-liner pens in accent colors crossed diagonally.

Soft overcast top-left, low contrast, no harsh shadows. 50mm slight grain. Tagline verbatim cell 7 only.
```

**Gotchas:** >9 cells = chaos. Hex labels need 4K. Avoid generic ('luxury') — use specifics (raw silk, brushed brass).

**Stack with:** Save as PALETTE+TEXTURE+TYPOGRAPHY ANCHOR. Combine with Nano Banana Pro for photo fidelity.

---

## A1-T7 — Trade-Show / Event Booth Render

**Score:** ★★★☆☆ (3/5)  
**Source:** GPT-Image-2 release + fal.ai patterns  
**Use case:** On-brand trade-show booth or event activation for internal approval, sales, agency pitch decks. Replaces weeks of C4D for early-stage decisions.

**Prompt template:**

```
Architectural photo of {size}-sqm booth for {brand_name} at {show_name}, 24mm wide f/8 eye-level slight upward tilt. 16:9 4K.

Booth:
- Back wall: {height}m matte {palette_primary}, wordmark "{BRAND_NAME}" {typeface} at {wordmark_height_cm}cm illuminated by LED channel
- Side walls: same primary, three backlit niches at 1.4m holding {product} behind non-reflective glass
- Floor: {floor_material}
- Ceiling: black truss with six spots aimed at hero wall

Experiential:
- Counter front-right {material} with 32" flush touchscreen showing brand film (frame: "{screen_text}")
- Two barstools in {accent_color}
- Floor stencil "{tagline}" verbatim

Convention-center ambient, motion-blurred visitor silhouettes. Brand palette {hex_1,2,3}. No competitor logos.
```

**Gotchas:** People destabilize — keep as motion-blurred silhouettes. Glass reflections inconsistent. Real venues recognized but may refuse.

**Stack with:** Feed booth render as BRAND ENVIRONMENT anchor for collateral. Combine with Seedance 2.0 first-frame anchor.

---

## A1-T8 — Print-Ready Business Card Stationery Suite

**Score:** ★★★★☆ (4/5)  
**Source:** [felo.ai 50-template + zeenesia](https://felo.ai/blog/gpt-image-2-prompt-guide-50-templates/)  
**Use case:** Complete physical stationery suite (cards front/back + letterhead + envelope + compliments slip) as one flat-lay for client approval, Behance, printer briefs.

**Prompt template:**

```
Top-down flat-lay 4K 4:3. Stationery for {brand_name} on {surface_color_texture}, natural overcast top-left.

Arrangement:
1. Two cards stacked offset — top FRONT: wordmark "{BRAND_NAME}" 18pt {typeface}, tagline "{tagline}" 8pt. Bottom BACK: "{NAME}" 12pt, "{TITLE}" 9pt, "{phone} · {email} · {domain}" 8pt left-aligned.
2. A4 letterhead center-right — wordmark top-left 14pt, body "{dummy_body_copy}", footer "{address_line}" 8pt.
3. #10 envelope bottom-left — wordmark + "{return_address}" verbatim top-left.
4. Compliments slip top-right 3:1 — wordmark left, "With compliments" italic right.
5. Tiny accent — fountain pen / paper clip — anchor.

Paper: {stock, e.g., "heavy uncoated cotton 350gsm, visible fiber"}. Finish: {e.g., "letterpress deboss for wordmark"}. Palette {hex_1}+{hex_2}.
```

**Gotchas:** Special chars (é, ö, ñ) artifact at 2K — use 4K. Phone formats unreliable; spell digits with separators. 'Deboss' is pseudo-real (subtle shadow only).

**Stack with:** Combines with a1-t5 page 7 (APPLICATIONS) as hero image.

---

## A1-T9 — Palette + Typography System Generation (Not Extraction)

**Score:** ★★★☆☆ (3/5)  
**Source:** Nicholas Rhodes + chatsmith.io synthesis  
**Use case:** Ask the model to PROPOSE a palette + typography system from a brand brief and render the proposal as a usable specimen. For blank-sheet brand projects with no visual anchor.

**Prompt template:**

```
Generate single specimen card 4:3 4K for proposed visual identity for {brand_name}, a {category} brand whose positioning is "{positioning_sentence}", audience "{audience_description}".

LEFT — COLOR SYSTEM:
- Vertical stack of 5 swatches (primary + 2 secondary + 2 neutral), each 60% half-width, 80pt tall
- Right of each: hex 11pt mono, role label 9pt italic, one-line rationale 8pt
- Palette feeling: "{descriptors, e.g., 'earthy, warm, confident, restrained'}". Propose colors reflecting positioning. Derive thoughtfully.

RIGHT — TYPOGRAPHY SYSTEM:
- Top: heading typeface 48pt "Aa 01 & ?". Underneath: name 14pt + rationale.
- Middle: body typeface 14pt "The quick brown fox..." Underneath: name + rationale.
- Bottom: pairing — "{brand_name}" 36pt above "{tagline}" 12pt body.

White background, thin dividing rule 50% width, header "VISUAL SYSTEM · PROPOSAL v1 · {brand_name}" 10pt mono.
```

**Gotchas:** Model proposes 'safe' palettes (earth=wellness, navy=fintech). Push back with palette_feeling_descriptors — demand 'acidic and austere' to break clichés. ~30% proposed typeface names invented.

**Stack with:** Feed approved card into a1-t5 as page 3+4. Combine with a1-t1 to upgrade moodboard-derived palette.

---
