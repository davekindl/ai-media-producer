# Client Products & B2B Deliverables

10 techniques. Each entry includes prompt template, source, gotchas, stack notes, and (when relevant) cross-references.

Use the skill's discovery step to pick the right one for a given request.

---

## A8B-T1 — Dashboard Mockup ('As-If-Shipped')

**Score:** ★★★★★ (5/5)  
**Source:** OpenAI cookbook 'describe as if exists'  
**Use case:** Photoreal dashboard with legible sidebar nav, real KPI numbers, axis-labelled charts, correctly spelled UI copy. Ideal when a B2B SaaS product is mid-build and you need client-facing mockups for proposals without leaking roadmap state.

**Prompt template:**

```
A photorealistic rendering of a 27-inch monitor on a clean walnut desk displaying a dark-mode managed-services dashboard titled '[PRODUCT NAME] — Incident Triage'. Left sidebar shows legible navigation items: 'Overview', 'Incidents', 'SLAs', 'Runbooks', 'Clients', 'Reports'. Main panel shows a large stacked-area chart labeled 'Incidents this quarter' with values 412, 388, 341, 302, 280, 261, 234 along the x-axis. Four stat cards on top read exactly: 'Open Tickets 47', 'Avg Resolution 4.2h', 'SLA Met 98.6%', 'AI Auto-Resolved 63%'. Below the chart, a data table with 5 rows, columns 'Ticket ID', 'Client', 'Severity', 'Age', 'AI Action'. Dark navy background (#0b0f1a), teal accent #4fd1c5, purple accent #a78bfa, Inter font, subtle reflections on screen. Datadog-style information density.
```

**Gotchas:** 'Describe as if shipped' not concept-art. aspect_ratio='16:9', resolution='2K' (4K experimental), quality='high'. Replace `[PRODUCT NAME]` with your actual product name and adjust KPIs to match your real metrics story.

**Stack with:** business-mvp landing hero, marketing-plan persona-pain visual, client pitch decks.

---

## A8B-T10 — Target-List / Account Map Visualization

**Score:** ★★★★☆ (4/5)  
**Source:** Marketing-plan target-list + thinking-mode  
**Use case:** 'Target account map' graphics — grid/hierarchical layout of 12-20 company logos/placeholders with tiered labels (Tier 1/2). Currently a text table; visualizing dramatically increases perceived strategic depth.

**Prompt template:**

```
Editorial 'Target Account Map' graphic, 16:9, clean cream (#faf7f2) background. Top center title, Inter Bold 56pt deep navy: 'Q[N] [YEAR] Target Accounts — [MARKET SEGMENT]'. Three horizontal tiers labeled exactly at left: 'Tier 1 — Warm ([N])', 'Tier 2 — Qualified ([N])', 'Tier 3 — Prospect ([N])'. Each tier is a horizontal row of rectangular 'company cards'. Each card is a neutral grey-blue rectangle with a placeholder name, e.g. 'Company 01', 'Company 02' rendered exactly, in Inter Medium 14pt deep navy. Tier 1 cards slightly larger and with a soft teal glow. Tier 2 amber accent. Tier 3 neutral grey. Subtle vertical connector lines between tiers showing the funnel narrowing. Bottom-right footer: 'Source: [Your Firm] outreach pipeline, [Month Year]'. Consulting-grade, clean, no clutter.
```

**Gotchas:** Generate real company names INTO the prompt before calling the API — actual target accounts appear, not placeholders. Replace `[MARKET SEGMENT]`, `[Your Firm]`, and date accordingly.

**Stack with:** marketing-plan target list page, sales planning decks, quarterly outreach materials.

---

## A8B-T2 — Multi-Reference Brand-Consistent Visuals via img2img

**Score:** ★★★★★ (5/5)  
**Source:** OpenAI cookbook + kie.ai img2img + marketing-plan  
**Use case:** gpt-image-2-image-to-image takes up to 16 ref URLs. Combine palette + logo + typography + mood board → generate hero without drifting across long PDF. Solves the 'cover is purple-navy but chart is teal-blue' consistency problem.

**Prompt template:**

```
API body:
{
  "model": "gpt-image-2-image-to-image",
  "input": {
    "prompt": "Magazine-cover hero for a marketing plan titled 'Go-to-Market [YEAR] — [COMPANY NAME]'. Apply the palette from Image 1 (deep navy + teal + warm amber) and the typographic personality of Image 2 (editorial sans, tight tracking). Use the abstract geometric motif from Image 3 (layered translucent hexagons) as the background pattern. Center the title in two lines, 96pt, white, uppercase. Subtitle below in 32pt teal: 'Prepared for [client] — Q[N] [YEAR]'. Bottom-left: small watermark block for logo placement, leave empty (will be composited later). Premium-fintech feel, printable at A4.",
    "input_urls": [
      "[URL to your palette reference image]",
      "[URL to your typography reference image]",
      "[URL to your motif reference image]"
    ],
    "aspect_ratio": "3:4",
    "resolution": "2K"
  }
}
```

**Gotchas:** OpenAI rule: reference each input by index — 'Image 1: palette. Image 2: typography. Image 3: motif.' Describe interactions: 'apply Image 2's style to the title.' Replace placeholder URLs with real hosted reference images.

**Stack with:** marketing-plan, business-mvp, grand-slam-offer PDFs, client deliverables.

---

## A8B-T3 — Persona Avatars (4-6 stylistically locked)

**Score:** ★★★★★ (5/5)  
**Source:** Editorial portrait + locked base prompt  
**Use case:** 4-6 stylistically consistent persona avatars for marketing-plan PDF — stock-photo-quality headshots, NOT rubbery 'AI face'. Single highest-ROI unlock for marketing-plan skill.

**Prompt template:**

```
Editorial business portrait of a [AGE]-year-old [NATIONALITY] [GENDER] [JOB TITLE], [HAIR DESCRIPTION], [GLASSES/NO], [OUTFIT]. Neutral office background, slightly blurred open-plan office with warm afternoon light through tall windows. Subject is three-quarter facing camera, natural half-smile, direct gaze. 50mm lens, f/2.0, soft key light from camera left. Shot on Fujifilm GFX, magazine-quality. No text, no logos, no branding visible, no AI-generated uncanny-valley features. Center-framed, headroom above. Color grading: warm neutral, slight teal-and-orange film LUT.
```

**Gotchas:** Run all 6 personas through SAME base prompt with only demographic + wardrobe swapped — lighting, crop, grade, grain match across PDF gallery page. Example placeholder: "52-year-old male IT director, short greying hair, tortoiseshell glasses, navy blazer over light-grey button-down, no tie."

**Stack with:** marketing-plan (biggest single win), business-mvp ICP gallery, grand-slam-offer dream-buyer visualization.

---

## A8B-T4 — Non-English Collateral with Correct Diacritics

**Score:** ★★★★★ (5/5)  
**Source:** GPT-Image-2 multilingual rendering  
**Use case:** Renders non-English headlines and body copy with correct diacritics (e.g., Hungarian ő/ű, German ü/ö, French é/è) at 95%+ accuracy inside the image. Eliminates separate typesetting step for non-English market variants.

**Prompt template:**

```
LinkedIn hero banner, 1584×396, premium-fintech aesthetic, deep navy background with warm amber accent. Left side: large headline in three lines, Inter Bold 72pt, white, rendered exactly as written, no substitutions: '[LINE 1] / [LINE 2] / [LINE 3]'. Below, Inter Regular 24pt, teal: '[COMPANY NAME] — [VALUE PROPOSITION]'. Right side: abstract translucent hexagon pattern in amber. Small CTA button bottom-right: '[CTA TEXT]' in white on teal pill. No logos (will be composited later). Clean editorial spacing, no clutter.
```

**Gotchas:** Always quote non-English text VERBATIM in the prompt. Add 'rendered exactly as written, no substitutions, no extra characters'. Long strings (>15 words) sometimes get truncated — keep headlines short. Replace all bracketed placeholders before calling the API.

**Stack with:** Any non-English market variant: marketing-plan HU/DE/FR, business-mvp localized, landing page hero variants.

---

## A8B-T5 — Editorial Infographics for White Papers / Methodology

**Score:** ★★★★★ (5/5)  
**Source:** Information-design + GPT-Image-2 reasoning  
**Use case:** Vertically-structured process diagrams (numbered stages, icons, captions, bullet notes) — all inside ONE image. Ideal for methodology assets, audit frameworks, and protocol documentation.

**Prompt template:**

```
Editorial infographic poster titled '[METHODOLOGY TITLE] — [N]-Phase Method' in large bold Inter, 64pt, top-center. [N] clearly labeled stages arranged vertically with subtle arrow connectors between them, each on its own card: '1. [Stage 1]', '2. [Stage 2]', '3. [Stage 3]', '4. [Stage 4]', '5. [Stage 5]'. Each stage has a simple line icon (left), a one-sentence caption (center), and two small bullet notes (right). Bottom footer: '[Methodology Name] — [Company] © [Year]'. Clean vector style, strong visual hierarchy, legible at thumbnail size, balanced grid layout, deep navy on cream (#faf7f2) background, teal accent. Printable at A4 portrait.

VARIANT — campaign calendar:
Swap 'vertically stacked stages' for horizontal [N]-week Gantt-style strip with colored bands per channel + milestone markers.
```

**Gotchas:** Detail-rich layouts need 4K (or 2K minimum) for label legibility. Replace all bracketed placeholders before generating.

**Stack with:** methodology documentation, marketing-plan campaign calendar, white papers, chapter dividers.

---

## A8B-T6 — Pitch-Deck Section Dividers / Chapter Openers

**Score:** ★★★★☆ (4/5)  
**Source:** McKinsey/Stripe-deck conventions  
**Use case:** Editorial 'chapter opener' slides — abstract visual + section title + brand motif — between deck sections. Without them deck reads as wall of bullets; with them, McKinsey.

**Prompt template:**

```
Full-bleed 16:9 pitch-deck section divider. Deep navy (#0b0f1a) background with a large, soft, off-center radial gradient in warm amber fading to transparent. Abstract overlay: layered translucent hexagonal lattice in teal at 12% opacity, bottom-right quadrant. Large headline, Inter Black 140pt, white, bottom-left: '[SECTION NUMBER]'. Below, Inter Regular 56pt, warm amber: '[SECTION TITLE]'. Small caption, Inter Regular 20pt, white 60% opacity, bottom-left under the title: '[ONE-LINE CONTEXT]'. No logo (composite later). Generous whitespace. Premium editorial-consulting feel, feels like a McKinsey or Stripe deck.
```

**Gotchas:** Run pattern: one prompt per section, swap numeral + title + caption. Palette + motif + typography stay identical → whole deck coherent. Replace `[SECTION NUMBER]`, `[SECTION TITLE]`, and `[ONE-LINE CONTEXT]` per slide.

**Stack with:** All client pitch decks, grand-slam-offer, business-mvp PDF cover, chapter openers across any multi-section deliverable.

---

## A8B-T7 — E-Commerce / Product Hero Cards

**Score:** ★★★★☆ (4/5)  
**Source:** E-commerce best practices  
**Use case:** E-commerce-style hero shots — 'product on white' with clean contact shadow, legible label copy, correct pricing, no fringing. Directly usable on Gumroad, Amazon A+, LinkedIn product launches, and marketplace listings.

**Prompt template:**

```
Studio e-commerce product hero, 1:1 square, pure white background (#ffffff). Centered: [PRODUCT], perfectly extracted with clean silhouette, no fringing, sharp label text reading exactly '[PRODUCT NAME]' in [FONT STYLE]. Light soft contact shadow at the base, no dramatic shadows. Even neutral daylight. Product occupies center 70% of frame with generous breathing room. Sharp focus throughout. Color-accurate, slight subtle reflection on glossy surfaces. Ready for Amazon A+ / Gumroad cover use.
```

**Gotchas:** Generic template — swap `[PRODUCT]`, `[PRODUCT NAME]`, and `[FONT STYLE]` per item for batch generation. Works well for digital product mockups, physical product shots, and course covers.

**Stack with:** Gumroad launches, Amazon A+ content, LinkedIn product announcements.

---

## A8B-T8 — ROI Before/After Side-by-Side Visuals

**Score:** ★★★★☆ (4/5)  
**Source:** Consulting proposal conventions  
**Use case:** Two-panel before/after with accurate labels. Every consulting proposal benefits from this. Renders both panels with labels correct in one image.

**Prompt template:**

```
Editorial split-panel comparison graphic, 16:9, titled at top in Inter Bold 56pt: 'Before [SOLUTION] vs After [SOLUTION] — [TIMEFRAME] Impact'. Two equal vertical panels separated by a thin vertical divider. LEFT panel labeled 'Before' (grey-toned, slightly desaturated), contains three stat blocks rendered exactly: '[Metric 1 Name] — [Before Value]', '[Metric 2 Name] — [Before Value]', '[Metric 3 Name] — [Before Value]'. RIGHT panel labeled 'After' (full color, teal-amber brand palette), three matching stat blocks rendered exactly: '[Metric 1 Name] — [After Value]', '[Metric 2 Name] — [After Value]', '[Metric 3 Name] — [After Value]'. Small arrow connectors showing % improvement under each pair. Bottom footer: 'Case: [Client Reference] — [Period]. Numbers verified by client.' Clean, consulting-grade, no clutter.
```

**Gotchas:** Numbers must be verifiable — clients will check. Use real client data, not invented figures. Replace all bracketed placeholders with your actual case study metrics.

**Stack with:** consulting proposals, grand-slam-offer value stack, marketing-plan proof page, case-study one-pagers.

---

## A8B-T9 — White-Paper / Report Cover (Print-Ready A4)

**Score:** ★★★★★ (5/5)  
**Source:** Premium-fintech editorial conventions  
**Use case:** Print-ready A4 portrait covers with large title, subtitle, author, version, brand motif — all as one image, typography rendered inside. SINGLE BIGGEST time-save vs Figma manual work.

**Prompt template:**

```
Print-ready A4 portrait report cover, 3:4 aspect. Deep navy (#0b0f1a) background, top 40% is a large abstract motif: layered translucent hexagons in teal + amber, generative-art feel, no literal icons. Bottom 60% is clean typographic hierarchy, left-aligned, 80px margin. Top-left small caption Inter Regular 18pt warm amber: '[Report Category] — Chapter [N]'. Large main title Inter Black 96pt white, up to three lines: '[MAIN TITLE] / [SUBTITLE LINE 1] / [SUBTITLE LINE 2]'. Below, Inter Regular 28pt white 70%: '[Subtitle or series description]'. Bottom-left author block Inter Medium 20pt white: 'By [Author Name] — [Company]' Date line Inter Regular 16pt teal: '[Month Year] • v[N.N]'. Small logo placeholder block bottom-right (empty, will be composited). Premium-fintech feel — Stripe × McKinsey aesthetic.
```

**Gotchas:** Logo placeholder remains empty — composite SVG in Figma after. Replace all bracketed fields before calling the API.

**Stack with:** research reports, white papers, methodology manuals, business plan PDF covers.

---
