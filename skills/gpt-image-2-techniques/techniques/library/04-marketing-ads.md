# Marketing & Ad Creative

15 techniques. Each entry includes prompt template, source, gotchas, stack notes, and (when relevant) cross-references.

Use the skill's discovery step to pick the right one for a given request.

---

## A4-T1 — The Quoted-Text Rule (foundational)

**Score:** ★★★★★ (5/5) · `foundational`  
**Source:** [fal.ai + Apiyi + Felo 8-element](https://fal.ai/learn/tools/prompting-gpt-image-2)  
**Use case:** Single biggest driver of usable ad output. Wrap exact copy in English quotes ('YOUR HEADLINE') + state font/placement/'no duplicate text' as constraint. Drops text-render errors from ~30% to <5%.

**Prompt template:**

```
[Scene description]
Headline (EXACT TEXT): "YOUR HEADLINE HERE"
Supporting text: "Exact tagline here"
Typography: [Bold sans serif / Elegant serif], [placement], clean kerning, readable from distance.
Layout: [where subject sits, where text sits, white space]
Constraints:
Render text verbatim.
No extra words.
No duplicate text.
No watermark.
No extra logos.

VERBATIM EXAMPLE (billboard):
Create realistic roadside billboard at sunset using product from input image.
Headline (EXACT TEXT): "Fresh and clean"
Typography: Bold sans serif, high contrast, centered vertically left half, clean kerning, readable from distance.
Layout: Product right, headline left, lots of empty space.
Constraints: Render text verbatim. No extra words. No duplicate text. No watermark. No extra logos.
```

**Gotchas:** Without quotes, model paraphrases. Without 'No duplicate text', renders headline twice. Reserve for display copy — small-point legal/body copy stays fuzzy.

**Stack with:** FOUNDATIONAL — base layer for every marketing technique.

---

## A4-T10 — Dashboard / Product UI Mockup for B2B Proposals

**Score:** ★★★★★ (5/5)  
**Source:** Imagine.art + Felo + fal.ai onboarding  
**Use case:** Believable product screen without real Figma file. For consulting decks, SaaS landing, LinkedIn 'we built this' posts, Gumroad heroes.

**Prompt template:**

```
[Device] screenshot, photoreal mockup.
Device: [iPhone 15 Pro silver / MacBook Pro 14" space grey / iPad Pro 12.9"].
Screen content: [clean mobile / desktop / tablet] [product type] interface.
Dark-mode UI with [teal #06B6D4 / purple #8B5CF6] accent.
Shown on screen:
- Header (EXACT TEXT): "[PRODUCT NAME]"
- Main KPI card (EXACT TEXT): "[metric number]" + "[metric label]"
- Three category cards (EXACT TEXT): "[cat 1]", "[cat 2]", "[cat 3]"
- Bottom nav (EXACT TEXT): "[nav 1]", "[nav 2]", "[nav 3]", "[nav 4]"
Context: Device on [marble / wood / white seamless], soft directional light top-left.
Constraints: iOS-native status bar (signal, wifi, battery, time 9:41), no duplicate text, no watermark, no Apple logo ghosting, no generic stock-iOS look.
```

**Gotchas:** '9:41' iOS time signals you know what you're doing. Skip and reads as AI-gen. Apple logo ghosting known 2.0 failure.

**Stack with:** Combines with a4-t3 (iPhone+iPad+MacBook variants), a4-t7.

---

## A4-T11 — Infographic Poster (saveable LinkedIn asset)

**Score:** ★★★★★ (5/5)  
**Source:** Felo + MindStudio + Imagine.art  
**Use case:** '5-step process,' '3 myths about X,' data-driven insight posts. LinkedIn saves > swipes — saves are the algorithm signal.

**Prompt template:**

```
Vertical infographic, 1080x1350 (LinkedIn portrait).
Headline (EXACT TEXT): "[TITLE — e.g., 'The 5-Step AI Adoption Protocol']"
Sub-headline (EXACT TEXT): "[one-line context]"

Body: Five vertical stages connected by flowing line/path.
For each stage:
- Circular numbered icon (1, 2, 3, 4, 5) in [accent color]
- Stage name (EXACT TEXT): "[name]"
- One-line description (EXACT TEXT): "[description]"

Color: [primary #HEX, secondary #HEX, accent #HEX, white background].
Typography: Bold sans-serif headers, medium-weight body.
Style: Flat design, clean lines, editorial, print-quality.

Footer (EXACT TEXT): "[your name + handle]"

Constraints: Render verbatim. No duplicate text. No watermark. All 5 stages fit. Legible at 30% zoom.
```

**Gotchas:** >6 stages = illegible in feed preview. Hand-drawn beats perfect geometric for saves. Always footer with author name — travels when reposted.

**Stack with:** Core LinkedIn asset. Stack with a4-t7 for series consistency.

---

## A4-T12 — Localized Variant Swap (EN/HU/DE)

**Score:** ★★★★★ (5/5)  
**Source:** [Segmind + OpenAI 99% CJK + Microsoft Foundry](https://blog.segmind.com/ai-image-generation-api-gpt-image-2-review-real-world-use-cases-2026/)  
**Use case:** One master image spawns 3 markets without Figma handoff. 99% CJK + Latin-extended (Hungarian) accuracy.

**Prompt template:**

```
[Master creative brief from any technique above]

LOCALIZATION — generate 3 variants from same master:

Variant EN:
Headline (EXACT TEXT): "[English headline]"
Tagline (EXACT TEXT): "[English tagline]"
CTA (EXACT TEXT): "[English CTA]"

Variant HU:
Headline (EXACT TEXT): "[Hungarian headline — native phrasing, NOT machine translation]"
Tagline (EXACT TEXT): "[Hungarian tagline]"
CTA (EXACT TEXT): "[Hungarian CTA]"

Variant DE:
Headline (EXACT TEXT): "[German headline — formal Sie-form for B2B]"
Tagline (EXACT TEXT): "[German tagline]"
CTA (EXACT TEXT): "[German CTA]"

Keep all other elements identical: same subject, scene, lighting, composition, brand color, typography.

Constraints: Render verbatim per language. No translation drift. No duplicate text. No watermark.
```

**Gotchas:** Do NOT machine-translate inline — provide natively-written copy per language. Hungarian compounds (felhasználóbarát) cause kerning at small sizes — specify 'clean kerning, comfortable letter-spacing' for HU.

**Stack with:** Multiplier on every other technique. Required for a multi-market reach.

---

## A4-T13 — SYNTH: B2B Carousel Pack (10 slides, 1 brief)

**Score:** ★★★★☆ (4/5) · `synth`  
**Source:** Synthesis a4-t1+2+7+11+12  
**Use case:** Stack: editorial photoreal hook → 7 infographic body → 1 mockup case study → 1 quote-card CTA. All a4-t7 brand-locked. Localize via a4-t12. 20 assets per campaign, 15 min prompt assembly.

**Prompt template:**

```
Generate 10 slides in one batch via a4-t3 variant structure:

Slide 1 (hook): a4-t2 editorial photoreal + a4-t1 quoted hook
Slides 2-8 (body): 7 infographic slides using a4-t11 with a4-t7 brand lock
Slide 9 (case study): a4-t8 product mockup showing "what this looks like in practice"
Slide 10 (CTA): a4-t9 quote-card format with one-liner + book-a-call CTA

Localize via a4-t12 for HU + EN versions. Output: 20 assets per campaign.
```

**Stack with:** a weekly LinkedIn workflow.

---

## A4-T14 — SYNTH: Proposal Hero Set (4-asset consulting deliverable)

**Score:** ★★★★☆ (4/5) · `synth`  
**Source:** Synthesis a4-t7+8+10+11  
**Use case:** Brand-consistent 4-asset set for consulting proposals: cover dashboard mockup + section-divider infographic + social-proof quote + product-in-context CTA. McKinsey-grade in 30 min.

**Prompt template:**

```
1. Cover hero: a4-t10 dashboard mockup of your protocol in use
2. Section divider: a4-t11 infographic of 5-step process
3. Social proof slide: a4-t9 quote card with client testimonial
4. CTA slide: a4-t8 product-in-context (protocol playbook on Fast Company magazine cover)

All four share same a4-t7 brand-lock references.
```

**Stack with:** 30-min proposal package.

---

## A4-T15 — SYNTH: Weekly Ship Schedule (cadence stack)

**Score:** ★★★★☆ (4/5) · `synth`  
**Source:** Synthesis applied as cadence  
**Use case:** Mon: quote / Tue: infographic / Wed: editorial photoreal / Thu: UI mockup or product-in-context / Fri: A/B variant / Sat: email header / Sun: rest. 100 min weekly, ~30 assets shipped, zero designer dependency.

**Prompt template:**

```
Monday: a4-t9 quote card (X + LinkedIn) — 10 min
Tuesday: a4-t11 infographic (LinkedIn primary) — 15 min
Wednesday: a4-t2 editorial photoreal (LinkedIn primary) — 15 min
Thursday: a4-t10 UI mockup or a4-t8 product-in-context (LinkedIn + Substack) — 20 min
Friday: a4-t3 A/B variant test for next week's ad push — 30 min
Saturday: a4-t6 email header for Sunday newsletter — 10 min
Sunday: rest

Weekly: ~100 min prompt work, ~30 assets, zero designer.
```

---

## A4-T2 — Editorial Photoreal LinkedIn Carousel (your #1 channel)

**Score:** ★★★★★ (5/5)  
**Source:** [fal.ai + Postiv + PostNitro 2026](https://postiv.ai/blog/linkedin-carousel-examples-2)  
**Use case:** LinkedIn carousels hit 6.6% median engagement vs 2.3% text. The workhorse format. Per-slide template with 'no stock-photo smile' constraint that separates professional from Shutterstock.

**Prompt template:**

```
Scene: [quiet modern setting that carries editorial calm — minimalist studio, Scandinavian office, museum]
Subject: [believable professional — describe age range, clothing, posture — NOT a stock-photo grin]
Important details: Natural expression, realistic skin texture, [specific wardrobe], eye-level [full-body / mid-shot] framing, warm neutral color balance, shallow DOF.

Use case: LinkedIn carousel slide [N of X] — [editorial lifestyle / case study / insight].

Text overlay (EXACT TEXT): "[SLIDE_TEXT — one bold idea, <8 words]"
Typography: Bold condensed sans serif, top-left or lower-third, white or ink-black, clean kerning.

Layout: 1:1 1080x1080, subject [left/right/center], text breathing room opposite.

Constraints: No watermark, no logos, no extra people, no heavy retouching, no duplicate text, no stock-photo smile.
```

**Gotchas:** 'No stock-photo smile' load-bearing — without it, defaults to Shutterstock cheese. 5-7 slide sweet spot; 7-12 push (saves not swipes is KPI). Hook slide 1, single-point 2-(N-1), CTA final.

**Stack with:** Stack with a4-t1 (quoted text), a4-t7 (brand consistency), a4-t12 (HU/EN/DE variants).

---

## A4-T3 — A/B Variant Generator (20-50+ from one brief)

**Score:** ★★★★★ (5/5)  
**Source:** [AdventurePPC + Cometly + XPath Labs 2026](https://www.adventureppc.com/blog/how-to-a-b-test-chatgpt-ad-creative-a-data-driven-framework-for-2026)  
**Use case:** Constraint shift: 'can we produce 10 variants?' → 'which 10 do we test first?' Master brief + axes. Headline archetypes: Pain Interruption / Aspirational / Social Proof / Specificity. Visual tones: Editorial / Graphic / Before-After.

**Prompt template:**

```
MASTER BRIEF:
Brand: [name, 1 sentence identity]
Audience: [ICP, 1 sentence]
Concept: [single creative idea]
Composition: [layout skeleton]

VARY THESE AXES (1 image per combination):
Axis A — Headline archetype:
  A1: Pain Interruption — "Stop losing clients to missed deadlines?"
  A2: Aspirational Outcome — "What 40% more revenue looks like at month 6."
  A3: Social Proof — "Trusted by 40+ IT managers in Hungary."
  A4: Specificity — "From AI-curious to AI-deployed in 14 days."

Axis B — Visual tone:
  B1: Editorial photoreal (office, daylight)
  B2: Graphic typographic (bold type, flat color)
  B3: Before/after split screen

CONSTANT:
Logo placement bottom-left.
Brand color [#HEX].
Font family [name].
1:1 LinkedIn / 9:16 Stories / 16:9 banners.
No watermark, no duplicate text, render verbatim.
```

**Gotchas:** Per AdventurePPC: 5,000-10,000 impressions/variant before declaring winner, 20% MDE, 95% confidence, ONE variable at a time. Messaging is #1 lever, visuals #5.

**Stack with:** Required partner for every campaign.

---

## A4-T4 — YouTube Thumbnail High-CTR Formula

**Score:** ★★★★☆ (4/5)  
**Source:** [Apiyi + MiraFlow + NIGCWorld](https://miraflow.ai/blog/best-ai-prompts-youtube-thumbnails-2026)  
**Use case:** 16:9 with giant text + dramatic subject. Proven viral baseline.

**Prompt template:**

```
Video thumbnail, 16:9, 1920x1080.
Left half: [subject with strong emotional expression — "shocked," "skeptical smirk," "pointing at camera"].
Right half: huge text (EXACT TEXT): "[4 WORDS OR FEWER]" bold, black outline, [primary color] fill.
Accent: red arrow pointing at [focal] / yellow box around [KPI number].
Background: high-contrast, slight radial gradient, no clutter.
Composition: rule-of-thirds — eyes upper-left third, text right third.
Constraints: No duplicate text, no watermark, legible at 150x90 preview, skin tones natural.
```

**Gotchas:** Text >4 words loses CTR. 'Skeptical smirk' beats 'confident smile'. Avoid 3-color + 3-object + 3-effect overload.

**Stack with:** Stack with a4-t1, a4-t7.

---

## A4-T5 — Display Banner Ad Suite (5 IAB sizes)

**Score:** ★★★★☆ (4/5)  
**Source:** MindStudio + Apiyi + Felo  
**Use case:** IAB-spec banner suite (300x250, 728x90, 160x600, 320x50, 970x250). Each size has different compositional logic — specify per-size layout.

**Prompt template:**

```
Display ad for [brand], [SIZE in px]:
- 300x250 Medium Rectangle: vertical stacking, logo top, headline middle, CTA bottom
- 728x90 Leaderboard: left logo | middle headline | right CTA
- 160x600 Skyscraper: tall, logo top, stacked benefit bullets middle, CTA bottom
- 320x50 Mobile Banner: horizontal single-line condensed
- 970x250 Billboard: hero width, full creative

Creative:
[Product/subject] on [clean brand-color background], [primary brand color #HEX].
Headline (EXACT TEXT): "[HEADLINE]"
CTA button (EXACT TEXT): "[CTA — e.g., Book a Call]"
Logo: top-left, subtle.
Typography: clean sans-serif, clean kerning, readable from distance.
Constraints: render verbatim, no duplicate text, no watermark, no extra logos, 20px safe margin.
```

**Gotchas:** 5 sizes have different compositional logic. Safe margin prevents network rejection.

**Stack with:** Combine with a4-t3 (variant matrix), a4-t7 (consistency).

---

## A4-T6 — Email Header / Newsletter Banner

**Score:** ★★★★☆ (4/5)  
**Source:** Felo + MindStudio + 2026 conventions  
**Use case:** 600x200 (or 1200x400 retina) MailChimp/Substack/SendFox/HubSpot newsletter header. Critical text in top 150px (above mobile fold).

**Prompt template:**

```
Email newsletter header, 600x200 (or 1200x400 retina):
Background: [gradient — e.g., deep purple #3B1F6B to indigo #0A1F5C].
Left: company logo placeholder, clean subtle.
Center: headline (EXACT TEXT): "[HEADLINE — <5 words]"
Below: tagline (EXACT TEXT): "[tagline — <10 words]"
Right: subtle data-vis line chart OR product silhouette, low-opacity overlay.
Typography: modern sans-serif, headline 48px, tagline 20px, white.
Constraints: Critical text in top 150px (above mobile fold). Render verbatim. No duplicate text. No watermark. 30px safe margin.
```

**Gotchas:** Email clients crop bottom on mobile. Outlook desktop strips backgrounds — test with solid-color fallback.

**Stack with:** Stack with a4-t7 for consistent look across 12-email sequence.

---

## A4-T7 — Brand Consistency Across Campaign (reference-image lock)

**Score:** ★★★★★ (5/5)  
**Source:** [WaveSpeedAI + MindStudio + Segmind](https://wavespeed.ai/blog/posts/introducing-openai-gpt-image-2-edit-on-wavespeedai/)  
**Use case:** Generate full campaign suite (carousel + display + email + poster) feeling like ONE brand world. Up to 16 ref URLs on kie.ai img2img.

**Prompt template:**

```
Reference images attached: [brand_palette.png, typography_sample.png, hero_product.png]

Generate: [specific asset — e.g., LinkedIn carousel slide 3 of 7]
Brief: [scene, subject, text overlay per a4-t1+t2]

Brand lock instructions:
Use color palette and typography from references.
Match ink-weight and kerning of typography sample.
Preserve product geometry, label text, label colors exactly from hero product reference.

Constraints:
Do not restyle product.
Do not change proportions.
Do not drift from reference palette.
No watermark.
```

**Gotchas:** GPT-Image-2 does NOT maintain brand memory across sessions — attach refs every generation. Logo fidelity imperfect (ZDNET test failed). Composite final logo in post.

**Stack with:** Required for a4-t2/3/5/6/9/10. Mandatory for any campaign >1 asset.

---

## A4-T8 — Product Mockup Billboard / Magazine (aspirational context swap)

**Score:** ★★★★☆ (4/5)  
**Source:** fal.ai + Felo + Anil-matcha + imagine.art  
**Use case:** Show product on prestigious surface (Times Square, Fast Company, airport lounge) for pitch decks, social proof, launch posts.

**Prompt template:**

```
Extract product/asset from input image.
Generate: photoreal [context — roadside billboard at sunset / Times Square at dusk / magazine double-page spread].

Context details: [Specific environment — golden-hour, subtle motion blur on cars, cinematic wide angle].

Placement: Product centered on billboard, billboard upper 2/3 of frame, realistic perspective, billboard metal/LED texture visible at edges.

Copy on billboard (EXACT TEXT):
Headline: "[HEADLINE]"
Tagline: "[TAGLINE]"
Logo: bottom-right.

Constraints: Preserve product geometry, label, colors exactly. Do not restyle product. No duplicate billboard, no duplicate text, no watermark. Photoreal — no illustration look.
```

**Gotchas:** Without 'photoreal — no illustration look', model occasionally renders stylized poster. Realistic perspective load-bearing.

**Stack with:** Stack with a4-t7 (product ref lock), a4-t3 (5 context variants).

---

## A4-T9 — X/Twitter Quote Graphic (scroll-stopping square)

**Score:** ★★★★☆ (4/5)  
**Source:** [Felo + Toolpic viral examples](https://toolpic.me/en/blog/best-gpt-image-2-prompts-viral-examples)  
**Use case:** Pull-quotes, testimonial cards, bold thought-leadership one-liners. Highest-engagement single-image format on X.

**Prompt template:**

```
Square 1080x1080.
Background: [cream #F5F1E8 / sage green #8FA88C / deep navy #0A1628 — pick ONE mood].
Subtle texture: [paper grain / matte / none].
Centered: oversized quotation mark glyph in [accent color], 40% opacity.
Main text (EXACT TEXT): "[QUOTE — 10-20 words max]"
Attribution (EXACT TEXT): "— [NAME, ROLE]"
Typography: serif (Tiempos/Playfair) for quote, sans-serif small for attribution.
Layout: generous margins, quote center 70%, attribution bottom-right.
Constraints: Render verbatim. No duplicate text. No watermark. No logo. Premium editorial feel.
```

**Gotchas:** 'Oversized quotation mark at low opacity' makes it editorial vs Canva-templated. Quote MUST be <20 words.

**Stack with:** Stack with a4-t3 (10 variants from 10-quote article), a4-t7 (consistent background per series).

---
