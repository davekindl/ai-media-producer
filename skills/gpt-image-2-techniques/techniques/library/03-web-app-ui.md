# Web & App UI Mockups

13 techniques. Each entry includes prompt template, source, gotchas, stack notes, and (when relevant) cross-references.

Use the skill's discovery step to pick the right one for a given request.

---

## A3-T1 — Viktor Oddy Liquid-Glass SaaS Landing Template

**Score:** ★★★★★ (5/5)  
**Source:** [@viktoroddy, X 2026-04 (designrocket.io)](https://x.com/viktoroddy/status/2036138734966677970)  
**Use case:** Full-page dark-premium SaaS landing mockup (navbar + hero + announcement pill + CTA + dashboard preview). Oddy's pattern: name fictional company, commit to one aesthetic codename ('liquid glass'), list components top-to-bottom with exact text. Community gold-standard.

**Prompt template:**

```
Create a dark, premium SaaS landing page for fictional company "{COMPANY_NAME}" — a {PRODUCT_CATEGORY} platform. Liquid glass aesthetic with ultra-dark backgrounds (#0A0A0A), translucent glassmorphic elements (rgba(255,255,255,0.01) backdrop blur and inset border gradient), {ACCENT_HEX} accent.

TOP: Centered pill-shaped navbar in liquid-glass container. Left: {COMPANY_NAME} logo with {LOGO_ICON} icon. Center nav: "{NAV_1}", "{NAV_2}", "{NAV_3}", "{NAV_4}". Right: "Sign Up" CTA in {ACCENT_HEX}. Above navbar: small translucent badge "{ANNOUNCEMENT_TEXT}".

HERO: Large centered headline "{HEADLINE}" tight-tracked sans 72-96px. Below: muted subheading "{SUBHEADLINE}" 20px. Two CTAs: primary filled "{CTA_PRIMARY}" in {ACCENT_HEX}, secondary ghost "{CTA_SECONDARY}" in glass.

BELOW FOLD: Floating dashboard preview card (glass surface) showing {DASHBOARD_ELEMENTS}. Drop shadow, subtle rim light.

Typography: {FONT_FAMILY}. All text verbatim, no duplicates, no watermarks, no "Lorem ipsum". 16:9, 2K, photoreal screenshot — not a mockup.
```

**Gotchas:** Don't ask for known brand logos (Stripe/Linear); model fails. Invent logo icon name ('crosshair', 'minimal orb'). 1:1 cannot do 4K — use 16:9.

**Stack with:** Pair with a3-t2 typography. Output works as input_urls for a3-t10 matching pricing/feature pages.

---

## A3-T10 — Reference-URL-Seeded UI Generation (16-Image Superpower)

**Score:** ★★★★★ (5/5) · `foundational`  
**Source:** OpenAI gpt-image-2-image-to-image docs  
**Use case:** Up to 16 reference URLs per call. Seed with typography ref + color palette + component style + logo + competitor screenshot. Visual consistency across 10+ screens, OR re-skin existing UI screenshot.

**Prompt template:**

```
[model: gpt-image-2-image-to-image, input_urls: [ref1, ref2, ref3, ...ref16]]

Generate {SCREEN_TYPE} for {PRODUCT}. Refs:
- Image 1 (base layout to preserve): structure + grid — sidebar width, header height, card positions
- Image 2 (typography reference): match typeface, weights, size ramp
- Image 3 (color palette source): pull brand palette — only these colors
- Image 4 (component style): match border-radius, shadow, border treatment
- Image 5 (iconography): match stroke weight + style

Screen content: {SPECIFIC — use a3-t2 7-slot}.

Do not copy any text, logos, or brand marks from refs. Use only for structural and stylistic cues. Fresh content, consistent style.
```

**Gotchas:** Model SOMETIMES copies visible text from refs — explicitly forbid. More refs = longer latency; 3-5 sweet spot, 16 max but slow.

**Stack with:** FOUNDATIONAL meta-technique — makes every other technique scalable. Any a3-t1...t9 output becomes ref for next a3-t10 run.

---

## A3-T11 — SYNTH: Oddy Cascade — iterative landing refinement

**Score:** ★★★★☆ (4/5) · `synth`  
**Source:** Synthesis a3-t1 + a3-t10  
**Use case:** Stack Oddy template + reference-URL seeding into repeatable workflow: generate full landing → ref for matching pricing → about → mobile. 4 internally-consistent pages in <10min. Replaces 2-3 hours Figma.

**Prompt template:**

```
Pass 1 (text-to-image, 16:9, 4K): Full landing page using Oddy template with fictional company name. Save URL.

Pass 2 (image-to-image, Pass 1 as ref): Matching pricing with same navbar, typography, brand colors. "Preserve navbar exactly. Replace hero + dashboard preview with 3-column pricing. Typography and colors identical."

Pass 3 (image-to-image, Pass 1 + Pass 2 as refs): Matching "About" page.

Pass 4 (image-to-image, Pass 1 as ref, 9:16): Mobile version.
```

**Stack with:** Result: four internally-consistent page mockups in <10 min for client pitch deck.

---

## A3-T12 — SYNTH: Competitive Shadow (re-skin via competitor refs)

**Score:** ★★★☆☆ (3/5) · `synth`  
**Source:** Synthesized — community widely-used pattern  
**Use case:** Ethically ambiguous: upload 3-4 competitor screenshots. 'Extract structural pattern without copying brand marks or text, re-skin in {YOUR_BRAND_PALETTE}.' Output sits in same neighborhood but visibly differentiates.

**Prompt template:**

```
Use 3-4 competitor screenshots as input_urls.

"Extract structural pattern without copying any brand marks or text from references, and re-skin in {YOUR_BRAND_PALETTE}. Use {YOUR_TYPEFACE}. Use {YOUR_COMPONENT_STYLE}.

CRITICAL: Do not reproduce logos, brand marks, or verbatim copy from references. Only use for structural and stylistic cues — layout, hierarchy, density."
```

**Gotchas:** Without explicit 'do not reproduce logos/brand marks/verbatim copy', model may copy elements directly. Trademark risk if you skip this constraint.

---

## A3-T13 — SYNTH: 3-Aspect Render (one prompt, 3 ratios)

**Score:** ★★★★☆ (4/5) · `synth`  
**Source:** Synthesized — leverages 2.0 reasoning  
**Use case:** Generate same screen in 3 aspect ratios — 16:9 desktop + 9:16 mobile + 1:1 square — in one batch. 2.0 reasoning handles responsive-layout adjustment (sidebar→hamburger, 3-col pricing→vertical stack).

**Prompt template:**

```
Generate same screen content in 3 aspect ratios. Identical content spec. Vary only aspect_ratio + brief layout adjustment note.

Run 1: aspect_ratio=16:9, "desktop layout — sidebar nav + 3-column main"
Run 2: aspect_ratio=9:16, "mobile responsive — hamburger menu + single-column stacked"
Run 3: aspect_ratio=1:1, "social media crop — focal hero + minimal chrome"

Same content (verbatim text, same data, same brand colors).
```

**Stack with:** Output: complete responsive asset set for App Store / Play Store / landing page in one sitting.

---

## A3-T2 — fal.ai 7-Slot UI Template

**Score:** ★★★★★ (5/5) · `foundational`  
**Source:** [fal.ai official prompting guide](https://fal.ai/learn/tools/prompting-gpt-image-2)  
**Use case:** Official 7-slot structure forces naming every axis the model needs. Eliminates vague output. Junior designers produce comparable results with the slot structure.

**Prompt template:**

```
Screen type: {mobile app / web dashboard / desktop interface}
Hierarchy: {primary actions, secondary elements, info architecture}
Exact copy: {word-for-word, button labels, headings — all in quotes}
State: {active / loading / empty / error}
Typography: {typeface style, size relationships, contrast levels}
Layout: {spacing patterns, alignment, negative space}
Constraints: {no logos, no watermark, no duplicate text, readable at intended size}
```

**Gotchas:** fal.ai warns against vague style tags ('minimalist brutalist editorial luxury photoreal') — produces mush. Replace mood words with measurable property: 'luxurious' → 'deep navy #0B1033 background, warm ivory #F5F1E8 text, 40px margins'.

**Stack with:** FOUNDATIONAL — base for any UI prompt. Combine with a5 lighting/materials. Batch-template in JSON.

---

## A3-T3 — 'Describe as if shipped' Anti-Concept-Art Directive

**Score:** ★★★★★ (5/5) · `foundational`  
**Source:** [imagine.art + fal.ai consensus](https://www.imagine.art/blogs/gpt-image-2-prompt-guide)  
**Use case:** Universal directive preventing Dribbble-default (floating 3D cards, no real content, gradient nothing). Forces output toward real shipped interface aesthetic. Append as terminal instruction.

**Prompt template:**

```
{any UI prompt} — Looks like a shipped product, not a wireframe. Not a mockup, not concept art, not a sketch. A screenshot of a real working interface. Real content, real data values, real copy. Ignore "design trends" aesthetics unless specified. Production-grade polish.
```

**Gotchas:** Doesn't substitute for content — without verbatim text in quotes, model invents copy in made-up language.

**Stack with:** FOUNDATIONAL — modifier on every other technique. Constant footer.

---

## A3-T4 — Device-Frame Mobile Mockup

**Score:** ★★★★☆ (4/5)  
**Source:** imagine.art + chatimg.ai  
**Use case:** Single mobile screen inside realistic device frame for App Store screenshots, pitch decks, website hero previews.

**Prompt template:**

```
Mobile app {SCREEN_TYPE} for {APP_CATEGORY} app called "{APP_NAME}". {UI_LAYOUT — use a3-t2 7-slot}. Shown inside {DEVICE_FRAME — iPhone 15, Pixel 9} frame, {ANGLE} angle, {LIGHT_MODE}. {ACCENT_COLOR} accents, {TYPEFACE}-style typography. 9:16, 2K. No Apple/Google logos on frame. Pristine device, subtle shadow on neutral surface.
```

**Gotchas:** iPhone 15 frame sometimes 'off' corner radii. If frame quality matters, generate interior screen alone, composite into proper frame in Figma.

**Stack with:** Light/dark variants in one image: 'Two iPhone frames side by side, identical screen, left light, right dark.'

---

## A3-T5 — Multi-Page Web Flow in One Wide Image

**Score:** ★★★★☆ (4/5)  
**Source:** Oddy + chatimg.ai derivation  
**Use case:** Wide 21:9: 3 consecutive screens of web flow (home → product → checkout) side-by-side. Replaces 4-frame Figma file for investor decks.

**Prompt template:**

```
Wide 21:9 composition showing 3 consecutive screens of {PRODUCT} web flow, left-to-right on subtle neutral gradient (#F6F6F7 to #EEEEEF). Each screen: rounded-corner browser window (Chrome dots top-left, URL bar "{DOMAIN}/{PATH}"), ~33% frame width, 16:10 internal.

Screen 1 (left): {HOME_PAGE — use a3-t1/t2}. URL: "{DOMAIN}/".
Screen 2 (middle): {PRODUCT_PAGE}. URL: "{DOMAIN}/product/{slug}".
Screen 3 (right): {CHECKOUT_PAGE}. URL: "{DOMAIN}/checkout".

All three share: {BRAND_PALETTE}, {TYPEFACE}, {COMPONENT_STYLE}. Consistent header. Subtle arrows between. 4K. Photoreal screenshots.
```

**Gotchas:** Reasoning handles 3 screens reliably, 4 starts degrading, 5+ inconsistent. URL bars: '/checkout' fine; '/products/tote-bag-italian-leather?color=tan' fails.

**Stack with:** Seed across 3-step series in img2img by passing first output as ref for screens 2-3.

---

## A3-T6 — Design System / Component Library Sheet

**Score:** ★★★★★ (5/5)  
**Source:** [Anil-matcha + EvoLinkAI](https://github.com/Anil-matcha/Awesome-GPT-Image-2-API-Prompts)  
**Use case:** One image showing complete UI library — buttons, inputs, cards, alerts, nav, type ramp — as cohesive design system. Becomes reference URL for downstream prompts.

**Prompt template:**

```
Generate complete UI design system in {STYLE_NAME} style, single cohesive reference sheet. Include:

- Web page preview (top-left, browser-chrome)
- Mobile screen preview (top-right, iPhone frame)
- 6-step typography ramp (H1 to body, with sample text + px sizes labeled)
- Color palette (6 colors with hex)
- Button variants (primary, secondary, ghost, destructive — hover + default)
- Input/field components (text, select, checkbox, toggle, slider)
- Card components (3 variants)
- Icon set (12 line icons: home, search, user, settings, notifications, calendar, camera, message, heart, bookmark, share, download — 4x3 grid, 2px stroke)
- Alert/toast variants (success, warning, error, info)

All share: {BRAND_PALETTE}, {TYPEFACE}, {BORDER_RADIUS}, {SHADOW_SYSTEM}. 16:9, 4K. Design-spec aesthetic. Clear section labels in small caps.
```

**Gotchas:** Don't over-pack — 9-12 components or unreadable at 4K. For full system, generate 2-3 sheets (colors+typography / components / patterns).

**Stack with:** Output sheet becomes reference URL for every UI prompt via input_urls — most powerful consistency technique in 2.0 era.

---

## A3-T7 — Datadog/Linear Dashboard Analytics Screen

**Score:** ★★★★★ (5/5)  
**Source:** felo.ai + chatimg.ai + imagine.art  
**Use case:** Dark-mode info-dense dashboard with KPI cards, charts, tables — Datadog/Linear/Amplitude aesthetic. Most common B2B SaaS hero image after landing pages.

**Prompt template:**

```
Desktop web analytics dashboard for {PRODUCT_CATEGORY} tool. Dark navy theme (#0E1117 background, #1A1F2E elevated surfaces), {ACCENT_PALETTE — 2-3 chart colors}.

Top bar: product logo left, search center, user avatar right.
Left sidebar: 8 nav items with icons ({LIST_NAV_ITEMS}).
Main top: 4 KPI tiles in row: "{KPI_1}: {VALUE_1}" with {TREND_ARROW}, "{KPI_2}", "{KPI_3}", "{KPI_4}". Subtle sparklines.
Main middle: large area chart "{CHART_TITLE}" x-axis dates (last 30 days), y-axis values. Line in {ACCENT_COLOR_1}, filled gradient.
Main right: donut chart "{DONUT_TITLE}" 4 segments + percentages.
Main bottom: data table "{TABLE_TITLE}" columns {COLUMN_LIST}, 6 rows realistic values.

Typography: Inter / SF Pro / IBM Plex Sans, numeric tabular figures. 8px grid, 1px borders. All text verbatim. No Lorem ipsum. 16:9, 4K. Shipped product, not Dribbble concept.
```

**Gotchas:** Chart axis values hardest text — ~85% accuracy vs 95% on larger. Use whole numbers (12k not 12,347), simple dates (Jan 1 not 2026-01-01).

**Stack with:** Pair with a4 data-viz. Output as ref for matching mobile dashboard. Feeds a3-t1 as floating preview inside full landing.

---

## A3-T8 — Pricing Page / Tiered Offer Table

**Score:** ★★★★☆ (4/5)  
**Source:** Anil-matcha + imagine.art (Stripe/Linear/Vercel)  
**Use case:** Most structurally rigid UI pattern — 3 columns, emphasize middle, features list, CTA per tier. High-value for client pitches.

**Prompt template:**

```
Pricing page for "{COMPANY_NAME}", a {PRODUCT_CATEGORY} platform. Three tier cards on {BACKGROUND}. Headline: "{PAGE_HEADLINE}", subhead: "{PAGE_SUBHEAD}".

Card 1 (left) "{TIER_1_NAME}": "{TIER_1_PRICE}/mo" large, "{TIER_1_TAGLINE}" small, 5 bullets ({TIER_1_FEATURES}), CTA "{TIER_1_CTA}" ghost.
Card 2 (center, elevated with {ACCENT} border + "Most Popular" ribbon) "{TIER_2_NAME}": "{TIER_2_PRICE}/mo", "{TIER_2_TAGLINE}", 7 bullets, filled {ACCENT} CTA "{TIER_2_CTA}".
Card 3 (right) "{TIER_3_NAME}": "{TIER_3_PRICE}", "{TIER_3_TAGLINE}", 9 bullets, ghost CTA "{TIER_3_CTA}".

Each bullet prefixed with checkmark icon. Grayed-out ✕ for "not included". Below: "Trusted by {N} teams" + 5 monochrome logo placeholders. Typography: {TYPEFACE}. All text verbatim. 16:9, 2K.
```

**Gotchas:** Pricing numbers + features must be letter-perfect — verify $29/mo wasn't rendered $29/m0. 'Most Popular' ribbon almost always clean.

**Stack with:** Pass design-system sheet (a3-t6) as ref for brand consistency. Feed forward as ref for matching FAQ page.

---

## A3-T9 — DTC E-commerce Product Detail Page

**Score:** ★★★★★ (5/5)  
**Source:** [MindStudio 'Classic Tote' DTC + OpenAI Cookbook](https://www.mindstudio.ai/blog/gpt-image-2-use-cases-2)  
**Use case:** Single product detail page for DTC/e-commerce — hero photo left, copy right, swatches, Add-to-Cart, reviews. Higher polish than B2B.

**Prompt template:**

```
Clean DTC product detail page for "{PRODUCT_NAME}" by "{BRAND_NAME}". Two-column on {BACKGROUND}.

Left column (50%): single hero photo of {PRODUCT_DESCRIPTION} on {STUDIO_BACKGROUND}. Soft {LIGHT_TYPE}. Below: thumbnail strip of 4 angle photos.

Right column (50%): Breadcrumb "{BREADCRUMB_PATH}". Product name "{PRODUCT_NAME}" {TYPEFACE} (48px). Price "{PRICE}". 4.8-star rating + "({REVIEW_COUNT} reviews)". 2-3 sentence description. Variant swatches for {VARIANT_TYPE} ({N_VARIANTS} options). Quantity stepper. Large "Add to Cart" in {BRAND_ACCENT}. "Shipping & Returns" + "Materials" accordions.

Below: "Why customers love it" with 3 review cards — 5 stars, short quote, customer name.

Typography: serif brand name (Canela/Tiempos), sans-serif body (Inter/Söhne). Hex {BRAND_PALETTE}. Premium, airy, lots of whitespace. Photoreal product render, readable text. 16:9, 4K.
```

**Gotchas:** Product render IS the deliverable. Specify material ('tan full-grain Italian leather' not 'brown leather'), lighting type, setting.

**Stack with:** Pair with a6 photoreal for hero if extreme realism. Pass design-system sheet as ref.

---
