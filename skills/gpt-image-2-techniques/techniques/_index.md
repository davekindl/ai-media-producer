# Technique Index — gpt-image-2-techniques skill

Discovery directory. Used by the skill to scan all techniques during the discovery step.
Each entry: ID · ★score · name · [tag] · one-line summary.
Total: 117 image-only techniques across 11 categories.

**Score legend:** ★★★★★ = multi-source verified · ★★★★ = strong evidence · ★★★ = single-source or synthesized · lower = anecdotal.
**[foundational]** badges = building-block techniques that recur across categories. Pick the framing that fits the use case.
**[synth]** = synthesized from multiple agents' findings. Treat as workflow recipes.

---

## Brand Identity & Design Systems  ·  [`library/01-brand-identity.md`](library/01-brand-identity.md)

- **A1-T1** ★★★★☆ **One-Prompt Brand Guideline From One Image** — Reverse-engineer a complete brand system (logo, palette, typography, applications, voice line) from one inspiration photograph. Single A3-portrait page output.
- **A1-T10** ★★★☆☆ **Rebrand Reveal One-Sheet (Before/After Grid)** — Single-image 'before vs after' rebrand visualization across 6-8 applications. Behance showcase format proving new identity works across the business.
- **A1-T11** ★★★★☆ **SYNTH: Canonical Brand Anchor Workflow** [synth] — Run a1-t1 to generate master brand-anchor page → save as brand_anchor.png → feed as single 'BRAND SYSTEM' reference in every subsequent call. Solves session-to-session drift. Brand reduced to one PNG that persists across the engagement.
- **A1-T12** ★★★★☆ **SYNTH: Deck-Grade Brand Reveal in 3 API Calls** [synth] — Compact reveal deck in exactly 3 calls: anchor (essence) + 4-panel fan-out (in the wild) + before/after grid (what changed). Replaces ~1 day designer work with ~15 min orchestration.
- **A1-T13** ★★★☆☆ **SYNTH: Hungarian-Native Brand Pass (HU)** [synth] — For Hungarian-market B2B client work: GPT-Image-2's 95%+ multilingual text means Hungarian diacritics (é, ö, ő, ü, ű) render cleanly. Bridges 2.0's global advantage with HU business context.
- **A1-T2** ★★★★★ **Thinking-Mode Multi-Format Campaign Fan-Out** — One prompt → 4-10 on-brand assets across distinct aspect ratios via O-series reasoning (IG square + Twitter banner + LinkedIn header + vertical story). Replaces 2-3 hours of designer work per variation set.
- **A1-T3** ★★★★★ **Role-Labeled 16-Reference Brand Lock** **[foundational]** — Up to 16 reference images, each labeled by role (PALETTE ANCHOR, LOGO ANCHOR, TYPOGRAPHY ANCHOR, LIGHTING ANCHOR, PRIOR ASSET). Meta-pattern: invariant declaration + role-labeled references. Solves the drift problem.
- **A1-T4** ★★★★☆ **Packaging Family / SKU Shelf Set** — Coherent product family (3-6 SKUs) with differentiated flavors but unified structural identity. The classic 'shelf impact' shot for merchandising and investor decks.
- **A1-T5** ★★★★☆ **Multi-Page Brand Guidelines Document (8 pages)** — 6-12 page brand guidelines PDF as sequence of individual page renders. Cover, logo rules, color, typography, photography, voice, applications. Client deliverable.
- **A1-T6** ★★★☆☆ **Brand Mood Board (9-Cell Flat-Lay)** — Flat-lay 9-cell mood board photographed top-down — palette chips, type specimen, texture, hero objects, logo disc, polaroid scene. The asset every brief asks for.
- **A1-T7** ★★★☆☆ **Trade-Show / Event Booth Render** — On-brand trade-show booth or event activation for internal approval, sales, agency pitch decks. Replaces weeks of C4D for early-stage decisions.
- **A1-T8** ★★★★☆ **Print-Ready Business Card Stationery Suite** — Complete physical stationery suite (cards front/back + letterhead + envelope + compliments slip) as one flat-lay for client approval, Behance, printer briefs.
- **A1-T9** ★★★☆☆ **Palette + Typography System Generation (Not Extraction)** — Ask the model to PROPOSE a palette + typography system from a brand brief and render the proposal as a usable specimen. For blank-sheet brand projects with no visual anchor.

## Editorial / Informational Design  ·  [`library/02-editorial-info.md`](library/02-editorial-info.md)

- **A2-T1** ★★★★★ **@dotey Hand-Drawn Infographic Card (origin of 'Abhishek framework')** — The actual origin of what circulates as the 'Abhishek framework'. Beige paper + red-black calligraphy title + 2-4 sections + hand-drawn icons. Single highest-leverage prompt for this angle.
- **A2-T10** ★★★★☆ **SYNTH: Series-Consistent Educational Poster Set** [synth] — Multi-part explainers. 10-part LinkedIn series. your 10-step methodology as 10-poster set. Two-stage: render canonical parent, then siblings using parent as reference.
- **A2-T2** ★★★★★ **Article → Cartoon Infographic 16:9 (@dotey landscape)** — Feed full article/section/blog post → return one-image summary readable in 10 seconds. Substitutes for $150-500/infographic designer hire.
- **A2-T3** ★★★★☆ **Atlabs 5-Pattern Infographic Library** — 5 layout archetypes — sketchnote, mind map, soft-pastel educational, technical flowchart, checklist — each with verbatim fill-in-the-blank template. Pick layout matching content shape.
- **A2-T4** ★★★★☆ **baoyu-skills Layout × Style Grid (340 combos)** — 20 layouts × 17 styles = 340 combinations. Pick layout (pyramid, fishbone, mind-map, ikea-manual, journey-path...) and style (claymation, chalkboard, aged-academia, technical-schematic, lego-brick...). The grid IS the IP.
- **A2-T5** ★★★★★ **OpenAI Instructional Design Brief (Educational/Scientific)** — Anatomical diagrams, chemistry reactions, biology labels, classroom explainers, flat scientific icon systems — anything with strict factual labels for print/slide use. OpenAI's official-sanctioned pattern.
- **A2-T6** ★★★★☆ **Chalkboard / Aged-Academia Editorial Poster** — Warm professorial feel for educational + 'this is a serious-but-inviting idea' business framing. Hormozi-whiteboard, Noah-Kagan-napkin-math vibe.
- **A2-T7** ★★★★☆ **IKEA-Manual Visual SOP / Recipe Card** — Any numbered sequence — recipes, equipment-assembly, software-onboarding, business-process, safety drills. Replaces tech-writer hire for internal docs.
- **A2-T8** ★★★★☆ **Knowledge-Density Japanese Ponchi-e Slide** — Cram absurd info-density on one slide while staying coherent and warm — Japanese government white-paper slides + friendly Irasutoya clip-art. Great for dense investor memos / research summaries.
- **A2-T9** ★★★☆☆ **SYNTH: Cheat-Sheet Grid (Learn-X-in-Y-Days)** [synth] — Reference posters. Print-to-wall cheat sheets. Carousel where each slide is a topic's cheat sheet. No canonical prompt existed for 'Python in 30 days' format — combines @dotey + Atlabs + OpenAI VERBATIM into reusable template.

## Web & App UI Mockups  ·  [`library/03-web-app-ui.md`](library/03-web-app-ui.md)

- **A3-T1** ★★★★★ **Viktor Oddy Liquid-Glass SaaS Landing Template** — Full-page dark-premium SaaS landing mockup (navbar + hero + announcement pill + CTA + dashboard preview). Oddy's pattern: name fictional company, commit to one aesthetic codename ('liquid glass'), list components top-to-bottom with exact text. Community gold-standard.
- **A3-T10** ★★★★★ **Reference-URL-Seeded UI Generation (16-Image Superpower)** **[foundational]** — Up to 16 reference URLs per call. Seed with typography ref + color palette + component style + logo + competitor screenshot. Visual consistency across 10+ screens, OR re-skin existing UI screenshot.
- **A3-T11** ★★★★☆ **SYNTH: Oddy Cascade — iterative landing refinement** [synth] — Stack Oddy template + reference-URL seeding into repeatable workflow: generate full landing → ref for matching pricing → about → mobile. 4 internally-consistent pages in <10min. Replaces 2-3 hours Figma.
- **A3-T12** ★★★☆☆ **SYNTH: Competitive Shadow (re-skin via competitor refs)** [synth] — Ethically ambiguous: upload 3-4 competitor screenshots. 'Extract structural pattern without copying brand marks or text, re-skin in {YOUR_BRAND_PALETTE}.' Output sits in same neighborhood but visibly differentiates.
- **A3-T13** ★★★★☆ **SYNTH: 3-Aspect Render (one prompt, 3 ratios)** [synth] — Generate same screen in 3 aspect ratios — 16:9 desktop + 9:16 mobile + 1:1 square — in one batch. 2.0 reasoning handles responsive-layout adjustment (sidebar→hamburger, 3-col pricing→vertical stack).
- **A3-T2** ★★★★★ **fal.ai 7-Slot UI Template** **[foundational]** — Official 7-slot structure forces naming every axis the model needs. Eliminates vague output. Junior designers produce comparable results with the slot structure.
- **A3-T3** ★★★★★ **'Describe as if shipped' Anti-Concept-Art Directive** **[foundational]** — Universal directive preventing Dribbble-default (floating 3D cards, no real content, gradient nothing). Forces output toward real shipped interface aesthetic. Append as terminal instruction.
- **A3-T4** ★★★★☆ **Device-Frame Mobile Mockup** — Single mobile screen inside realistic device frame for App Store screenshots, pitch decks, website hero previews.
- **A3-T5** ★★★★☆ **Multi-Page Web Flow in One Wide Image** — Wide 21:9: 3 consecutive screens of web flow (home → product → checkout) side-by-side. Replaces 4-frame Figma file for investor decks.
- **A3-T6** ★★★★★ **Design System / Component Library Sheet** — One image showing complete UI library — buttons, inputs, cards, alerts, nav, type ramp — as cohesive design system. Becomes reference URL for downstream prompts.
- **A3-T7** ★★★★★ **Datadog/Linear Dashboard Analytics Screen** — Dark-mode info-dense dashboard with KPI cards, charts, tables — Datadog/Linear/Amplitude aesthetic. Most common B2B SaaS hero image after landing pages.
- **A3-T8** ★★★★☆ **Pricing Page / Tiered Offer Table** — Most structurally rigid UI pattern — 3 columns, emphasize middle, features list, CTA per tier. High-value for client pitches.
- **A3-T9** ★★★★★ **DTC E-commerce Product Detail Page** — Single product detail page for DTC/e-commerce — hero photo left, copy right, swatches, Add-to-Cart, reviews. Higher polish than B2B.

## Marketing & Ad Creative  ·  [`library/04-marketing-ads.md`](library/04-marketing-ads.md)

- **A4-T1** ★★★★★ **The Quoted-Text Rule (foundational)** **[foundational]** — Single biggest driver of usable ad output. Wrap exact copy in English quotes ('YOUR HEADLINE') + state font/placement/'no duplicate text' as constraint. Drops text-render errors from ~30% to <5%.
- **A4-T10** ★★★★★ **Dashboard / Product UI Mockup for B2B Proposals** — Believable product screen without real Figma file. For consulting decks, SaaS landing, LinkedIn 'we built this' posts, Gumroad heroes.
- **A4-T11** ★★★★★ **Infographic Poster (saveable LinkedIn asset)** — '5-step process,' '3 myths about X,' data-driven insight posts. LinkedIn saves > swipes — saves are the algorithm signal.
- **A4-T12** ★★★★★ **Localized Variant Swap (EN/HU/DE)** — One master image spawns 3 markets without Figma handoff. 99% CJK + Latin-extended (Hungarian) accuracy.
- **A4-T13** ★★★★☆ **SYNTH: B2B Carousel Pack (10 slides, 1 brief)** [synth] — Stack: editorial photoreal hook → 7 infographic body → 1 mockup case study → 1 quote-card CTA. All a4-t7 brand-locked. Localize via a4-t12. 20 assets per campaign, 15 min prompt assembly.
- **A4-T14** ★★★★☆ **SYNTH: Proposal Hero Set (4-asset consulting deliverable)** [synth] — Brand-consistent 4-asset set for consulting proposals: cover dashboard mockup + section-divider infographic + social-proof quote + product-in-context CTA. McKinsey-grade in 30 min.
- **A4-T15** ★★★★☆ **SYNTH: Weekly Ship Schedule (cadence stack)** [synth] — Mon: quote / Tue: infographic / Wed: editorial photoreal / Thu: UI mockup or product-in-context / Fri: A/B variant / Sat: email header / Sun: rest. 100 min weekly, ~30 assets shipped, zero designer dependency.
- **A4-T2** ★★★★★ **Editorial Photoreal LinkedIn Carousel (your #1 channel)** — LinkedIn carousels hit 6.6% median engagement vs 2.3% text. The workhorse format. Per-slide template with 'no stock-photo smile' constraint that separates professional from Shutterstock.
- **A4-T3** ★★★★★ **A/B Variant Generator (20-50+ from one brief)** — Constraint shift: 'can we produce 10 variants?' → 'which 10 do we test first?' Master brief + axes. Headline archetypes: Pain Interruption / Aspirational / Social Proof / Specificity. Visual tones: Editorial / Graphic / Before-After.
- **A4-T4** ★★★★☆ **YouTube Thumbnail High-CTR Formula** — 16:9 with giant text + dramatic subject. Proven viral baseline.
- **A4-T5** ★★★★☆ **Display Banner Ad Suite (5 IAB sizes)** — IAB-spec banner suite (300x250, 728x90, 160x600, 320x50, 970x250). Each size has different compositional logic — specify per-size layout.
- **A4-T6** ★★★★☆ **Email Header / Newsletter Banner** — 600x200 (or 1200x400 retina) MailChimp/Substack/SendFox/HubSpot newsletter header. Critical text in top 150px (above mobile fold).
- **A4-T7** ★★★★★ **Brand Consistency Across Campaign (reference-image lock)** — Generate full campaign suite (carousel + display + email + poster) feeling like ONE brand world. Up to 16 ref URLs on kie.ai img2img.
- **A4-T8** ★★★★☆ **Product Mockup Billboard / Magazine (aspirational context swap)** — Show product on prestigious surface (Times Square, Fast Company, airport lounge) for pitch decks, social proof, launch posts.
- **A4-T9** ★★★★☆ **X/Twitter Quote Graphic (scroll-stopping square)** — Pull-quotes, testimonial cards, bold thought-leadership one-liners. Highest-engagement single-image format on X.

## Multi-Tool Stacking Workflows  ·  [`library/05-multi-tool-stacking.md`](library/05-multi-tool-stacking.md)

- **A5-T10** ★★★★★ **ChatGPT Multi-Turn Iterative Refinement (Self-Stacking)** — ChatGPT Images 2.0 preserves context across turns — each refinement is a STACKED operation, not a restart. O-series reasoning plans composition before generating + verifies text.
- **A5-T11** ★★★★★ **Kie.ai Unified Stack (Claude Code orchestrating GPT-Image-2 + Kling + Seedance + Suno)** — kie.ai exposes 66+ models behind one auth header + one submit/poll/download pattern. Claude orchestrates whole pipeline as one bash-like script.
- **A5-T12** ★★★☆☆ **SYNTH: Tiered Model Stack (Grok → GPT-Image-2 → Nano Banana Pro)** [synth] — Each image model has a tier. Grok iterates cheaply for ideation. GPT-Image-2 handles structure + text. Nano Banana adds 'warmth'. Never use one for all three jobs.
- **A5-T5** ★★★★☆ **GPT-Image-2 → Magnific → Topaz Gigapixel (Print-Grade Detail)** — GPT-Image-2's native 4K is professional for 95% of cases. Stack Magnific + Topaz only for: very large print, skin-pore close-ups, restoration of stylized output.
- **A5-T6** ★★★★★ **Claude → GPT-Image-2 → Claude Design (Programmatic Brand System)** — Claude decomposes brand brief into structured prompts → GPT-Image-2 executes 8-variant batch via API n=8 → Claude Design generates production React. Replaces 2-4 hours Figma in <60 min for ~$1.30.
- **A5-T7** ★★★★☆ **GPT-Image-2 → Photoshop 2026 Generative Fill** — PS 2026 added reference-image to Generative Fill with 'geometry-aware compositing matching scale, rotation, lighting, color, perspective.' First time AI products drop into real scenes without manual masking.
- **A5-T8** ★★★★☆ **GPT-Image-2 → Midjourney v7 --sref (Style Match Retexture)** — GPT-Image-2 nails STRUCTURE; MJ v7 nails ARTISTIC STYLE. --sref to inherit MJ style while keeping GPT-Image-2 structure as ref.

## Reverse-Engineering & Style Transfer  ·  [`library/06-reverse-style-transfer.md`](library/06-reverse-style-transfer.md)

- **A6-T1** ★★★★★ **Photo → Full Brand Guideline (THE @weplash hamburger pattern)** — 1 reference photo in → complete brand-book sheet (logo, hex palette, typography, social post, packaging) out. THE prompt family behind 'photo → brand book in 40 seconds' viral demos.
- **A6-T10** ★★★★☆ **Accent Graphic Extraction (Transparent PNG)** — Background-removal + shape-preservation in one prompt → reusable brand asset. Equivalent to Remove.bg + style-transfer simultaneously.
- **A6-T11** ★★★★☆ **Verbal Style-Transfer for Design Systems (Stripe-ify / Apple-ify / Linear-ify)** — No reference image — describe target brand verbally with concrete signature traits ('Stripe-purple-gradient + weight-300 elegance + generous whitespace + crisp sans-serif'). Avoids trademark-dodge refusals.
- **A6-T12** ★★★★★ **Multi-Image Compositing (OpenAI canonical)** — Canonical OpenAI-endorsed phrasing. 'Place X from image N into Y from image M' with 'do not change anything else' as compositing terminator.
- **A6-T2** ★★★★★ **Multi-Reference Character Merge (3-16 refs)** **[foundational]** — The pattern Midjourney can't do. Image 1 = face, Image 2 = outfit, Image 3 = pose, environment via text. Explicit role-assignment prevents cross-blending.
- **A6-T3** ★★★★★ **OpenAI Cookbook Style Transfer (canonical)** — OpenAI's officially-sanctioned style-transfer pattern. 'Use the same style' phrasing activates GPT-Image-2's style-encoder path.
- **A6-T4** ★★★★★ **Concrete-Visual-Language Style Transfer (fal.ai pro pattern)** — 'Same style' is too abstract — GPT-Image-2 rewards concrete components. Name palette, edge treatment, silhouette language, era energy explicitly.
- **A6-T5** ★★★★★ **Wardrobe / Virtual Try-On Transfer** — Identity is locked via negative-list. GPT-Image-2 preserves what you enumerate; drifts on what you leave unstated.
- **A6-T6** ★★★★☆ **Product-on-Surface / Product-on-Model Placement** — Short declarative product-on-surface or product-on-model commands. Lighting descriptor at end is the secret sauce for commercial-grade output.
- **A6-T7** ★★★★★ **Brand-Consistent Marketing Variants (Change/Preserve binary)** — Explicit Change/Preserve binary prevents 'everything drifts' failure. Production-grade pattern for brand-consistent marketing variants.
- **A6-T8** ★★★★☆ **Font Extraction from Reference Photo** — GPT-Image-2's OCR + visual-similarity identifies typefaces in photographs and returns closest Google Fonts equivalent as rendered specimens.
- **A6-T9** ★★★★☆ **Background Recreation from Brand Mood** — After brand extraction (a6-t1), produce infinite on-brand backgrounds. 'Avoid text or logos' negative prevents brand-copy hallucination.
- **A6-TA** ★★★★☆ **Character Consistency Anchor (anchor-and-continue)** — Generate once, then use the generation as reference for all subsequent scenes. Restate preservation constraints on EVERY continuation — drift happens when constraints aren't repeated.
- **A6-TB** ★★★★☆ **Product Extraction for Mockups (cleanup step)** — Strip product from lifestyle shot, place cleanly on white. Then feed stripped version back as Image 1 for mockup variants.

## Personalization & Generative Portraits  ·  [`library/07-personalization-portraits.md`](library/07-personalization-portraits.md)

- **A7-T1** ★★★★☆ **Self-Infographic Portrait (Aiker-style anime + life-stats wrap)** — Anime-style hero portrait centered, legible infographic stat blocks wrapping. Rides 2.0's #1 breakthrough (multilingual pixel-perfect text) + ChatGPT memory. Most viral-shaped personal-brand output.
- **A7-T10** ★★★☆☆ **Occasion / Greeting Card Personalization** — Hand-lettered headline rendering finally works first attempt — previous models needed 3-5 regens for text.
- **A7-T11** ★★★☆☆ **Future-Self / Alternate-Timeline Visualization** — Annual-planning ritual, consulting client vision-casting, speaker-talk opener.
- **A7-T12** ★★★☆☆ **D&D / RPG Character Sheet From Résumé** — Résumé → D&D character: race, class, alignment, stats, ability. Then portrait + stats box visual.
- **A7-T13** ★★★★☆ **ChatGPT Wrapped Annual Image Card** — This output class was the proof-of-concept OpenAI cited for 2.0 launch — stat-card image rendering at >95% text legibility. CRITICAL memory dependency.
- **A7-T2** ★★★★★ **ChatGPT Caricature Trend ('Me and My Job')** — The original viral that briefly crashed OpenAI servers. 20 verified style-modifier variants (3D, 1920s vintage, surreal-fantasy, street-graffiti).
- **A7-T3** ★★★★☆ **'Draw My Life' / Current-State Visualization** — Memory-only. No selfie required. Often produces accurate environmental cues (desk, city skyline, pets, clothing colors) rather than face-accurate portraits.
- **A7-T4** ★★★★☆ **Personality-Mirror (Reddit viral)** — CRITICAL memory dependency — output entirely derived from chat-history tone analysis. Outputs metaphorical/symbolic.
- **A7-T5** ★★★★☆ **Personal Stats Trading Card (Pokémon Holo-Foil)** — GPT-Image-2 advantage: holo-foil + small legible 1999-style stat text + icon rendering = three things 1.5 reliably broke. 2.0 does all three in one pass.
- **A7-T6** ★★★★★ **LinkedIn Professional Headshot Suite (Ruben Hassid 8-prompt set)** — 249-comment viral. Selfie-driven (no memory). 8 verbatim prompts covering corporate, cinematic, B&W, candid, formal, gallery, automotive moods. 2.0's identity preservation lock makes this work where 1.5 failed ~30%.
- **A7-T7** ★★★★☆ **Family / Team / Group Portrait (multi-ref, 4-6 subjects)** — GPT-Image-2 Edit handles 4-6 subject group shots preserving relative scale, eyeline, lighting. Critical: REPEAT preservation constraints on EVERY iteration.
- **A7-T8** ★★★★☆ **Anime-Mashup Vertical Selfie** — GPT-Image-2 advantage: anime-realism blend was 1.5's biggest quality drop zone. 2.0 holds consistent lighting between real-skin and cel-shaded sides.
- **A7-T9** ★★★★☆ **Renaissance Oil-Painting Pet Portrait** — Pet → 16th-century European nobility portrait. Verbatim from ImagePromptly.

## Music Brand / Album-Art Ecosystem  ·  [`library/08a-music-brand.md`](library/08a-music-brand.md)

- **A8A-T1** ★★★★★ **Anchor-Character Mascot Lock via 16-Ref Image-to-Image** — Generate 4-image character sheet ONCE (front/3-4/back/forearm-detail), pass those 4 URLs on every subsequent cover + lyric-video call. Solves #1 AI-music-artist problem: mascot drift across releases.
- **A8A-T10** ★★★★☆ **Reasoning-Mode Role Briefing (Anti-Slop Bias)** — GPT-Image-2 'thinks through composition before generating'. Role briefing — telling the model WHO + WHAT purpose — biases EVERY downstream decision. Single biggest grammar shift from 4o-image to 2.0.
- **A8A-T11** ★★★☆☆ **Sequential-Edit Pass for Hero Moment Stills** — For a 5-6 min build track — visual peak marking the 'scream moment' (~5:00 mark when lowercase→ALL CAPS). Image-edit on main cover with explicit 'change only' — second asset from one base.
- **A8A-T2** ★★★★★ **Non-English Text Rendering (Quote Rule + Spelling Guard)** — GPT-Image-2's flagship upgrade. Accented characters (e.g. Hungarian ő/ű/á, German ö/ü/ß) reliable first-try with Quote Rule + letter-by-letter spelling guard. Eliminates 'print title in Figma' workflow (~15 min saved/release).
- **A8A-T3** ★★★★★ **Oversized Canvas (21:9 / 4K) for Ken-Burns-Safe Backgrounds** — Request wider canvas (21:9) than target (16:9) with subject off-axis. Ken Burns sweep REVEALS godrays + chain detail as it moves — image becomes a tiny visual story matching the 'weight increases' philosophy.
- **A8A-T4** ★★★★☆ **Chiaroscuro + Volumetric-Light Grammar Pack (House Style)** — GPT-Image-2 is a reasoning model — one PRECISE lighting sentence outperforms a bag of adjectives. The dark-industrial cinematic-thriller aesthetic locked via 5 grammar pack components.
- **A8A-T5** ★★★★☆ **Bilingual Cover-Edition Series (Preserve-Layout Edit)** — For EN/non-EN release pairs. Generate English first, then image-edit with explicit change/preserve to swap title only.
- **A8A-T6** ★★★★☆ **Infographic-Poster Mode for IG Carousels (Lyric Quote-Cards)** — 2.0 topped LM Arena at 1512 because of multi-font dense text. For music artist = high-conversion IG format previously Canva-only.
- **A8A-T8** ★★★★☆ **Negative-Constraint Stack to Kill AI Slop Tells** — #1 reason AI covers look 'AI' isn't subject — it's giveaways. The last two negatives are CRITICAL — the gym/motivation default is the OPPOSITE of the dark-industrial aesthetic.
- **A8A-T9** ★★★☆☆ **Audiogram / Reel Background Loop-Prep Mode** — For 30-sec lyric snippet promos. Visual must be seamlessly loopable OR slow-motion enough cut is invisible. Purpose-built 'slow-motion-friendly' background.

## Client Products & B2B Deliverables  ·  [`library/08b-client-b2b.md`](library/08b-client-b2b.md)

- **A8B-T1** ★★★★★ **SaaS Dashboard Mockup ('As-If-Shipped')** — Photoreal dashboard with legible sidebar nav, real KPI numbers, axis-labelled charts, correctly spelled UI copy. A mid-build product needs client-facing mockups NOW for proposals without leaking roadmap state.
- **A8B-T10** ★★★★☆ **Target-List / Account Map Visualization** — 'Target account map' graphics — grid/hierarchical layout of 12-20 company logos/placeholders with tiered labels (Tier 1/2). Currently a text table; visualizing dramatically increases perceived strategic depth.
- **A8B-T2** ★★★★★ **Multi-Reference Brand-Consistent Visuals via img2img** — gpt-image-2-image-to-image takes up to 16 ref URLs. Combine palette + logo + typography + mood board → generate hero without drifting across long PDF. Solves marketing-plan's 'cover is purple-navy but chart is teal-blue' problem.
- **A8B-T3** ★★★★★ **Persona Avatars (4-6 stylistically locked)** — 4-6 stylistically consistent persona avatars for marketing-plan PDF — stock-photo-quality headshots, NOT rubbery 'AI face'. Single highest-ROI unlock for marketing-plan skill.
- **A8B-T4** ★★★★★ **Hungarian Collateral with Correct Diacritics** — Renders Hungarian body + headlines with correct ő, ű, á, é at 95%+ inside the image. Eliminates separate-designer-typesetting step for HU variants.
- **A8B-T5** ★★★★★ **Editorial Infographics for White Papers / Methodology** — Vertically-structured process diagrams (audit → map → identify → augment → measure) with numbered stages, icons, captions, bullet notes — all inside ONE image. The your long-form publication methodology asset.
- **A8B-T6** ★★★★☆ **Pitch-Deck Section Dividers / Chapter Openers** — Editorial 'chapter opener' slides — abstract visual + section title + brand motif — between deck sections. Without them deck reads as wall of bullets; with them, McKinsey.
- **A8B-T7** ★★★★☆ **Gumroad / Family Money Printer Product Cards** — E-commerce-style hero shots — 'product on white' with clean contact shadow, legible label copy, correct pricing, no fringing. Directly usable on Gumroad, Amazon A+, LinkedIn product launches.
- **A8B-T8** ★★★★☆ **ROI Before/After Side-by-Side Visuals** — Two-panel before/after with accurate labels. Every your product proposal needs this. Currently hand-built in PPT; GPT-Image-2 renders both panels with labels correct in one image.
- **A8B-T9** ★★★★★ **White-Paper / Report Cover (Print-Ready A4)** — Print-ready A4 portrait covers with large title, subtitle, author, version, brand motif — all as one image, typography rendered inside. SINGLE BIGGEST time-save vs Figma manual work.

## Content & Research Outputs  ·  [`library/08c-content-research.md`](library/08c-content-research.md)

- **A8C-T1** ★★★★☆ **Editorial-Opinion Hero (B&W Conceptual)** — Single high-contrast conceptual illustration for op-ed/essay. NYT op-ed page + Working Theorys hero art aesthetic. Two symbolic objects in tension, stark lighting. Reads as editorial considered, not AI-stock.
- **A8C-T10** ★★★★☆ **Multilingual Editorial (HU + EN bilingual hero)** — In-image text rendering for your local-language brand alongside your primary-language brand without separate typesetting. Hungarian Latin-extended (ő, ű, á, é, í, ó, ú) reliable.
- **A8C-T2** ★★★★★ **The 8-Element Framework (Scene→Constraints)** **[foundational]** — Canonical structure for any GPT-Image-2 prompt. Cuts iteration cycles roughly in half. Single highest-leverage prompting pattern.
- **A8C-T3** ★★★★☆ **Annotated Diagrams with In-Image Labels** — Cross-section / flowchart / system diagram with leader lines, labels, arrows rendered INSIDE the image. Replaces Figma/Lucidchart for draft-quality explainers.
- **A8C-T4** ★★★★★ **Multi-Reference Chapter Series Lock (img2img)** — THE single unlock for long-form series. Generate ONE hero style-bible image, then for each chapter call img2img with style-bible + chapter sketch + palette + typography refs. Never re-describe style in words. ~$5-13 for ALL 42 your flagship project assets.
- **A8C-T5** ★★★★☆ **Book Cover / Manifesto Cover (Single Focal Point)** — Single dominant element, not collage. Generous negative space, restrained palette. Renders book cover titles reliably when text quoted + typeface specified.
- **A8C-T6** ★★★★☆ **Newsletter / LinkedIn Hero (Project-Folder Workflow)** — Character/scene anchor + project folder = newsletter heroes instantly recognisable as YOURS. 90% first-try satisfaction. 2.0's 16-ref img2img improves consistency rather than breaks.
- **A8C-T7** ★★★★★ **your command center Datadog-Style Data Widget** — Tight info-density, navy/charcoal ground, teal/purple accents, in-widget labels, sparkline-like elements. The aesthetic you specify for your command center.
- **A8C-T8** ★★★★☆ **Annotated Screenshot / Explainer Overlay** — Screenshot-like composition with arrows, circles, callouts, labels rendered INTO the image. Eliminates whole Figma/Annotate.app step.
- **A8C-T9** ★★★★☆ **LinkedIn Carousel Slide System (5-10 slides @ 1080x1080)** — Document carousels = ~24% engagement vs ~3% text — 596% multiplier. Sweet spot 5-10 slides. Generate each slide individually with same style ref → reads as designed not templated.
- **A8C-TBONUS** ★★★★☆ **Magazine-Grade Composite Layout (Headline + Hero + Pullquote)** — GENUINELY NEW in 2.0. Full magazine-style spread — masthead, headline, hero, byline, pull quote — all composed by model in one pass. OpenAI calls it 'magazine-grade'.

## Image Generation for Video Pipelines (keyframe assets)  ·  [`library/09-video-keyframe-bible.md`](library/09-video-keyframe-bible.md)

- **A9-W3** ★★★★★ **Character Bible Bootstrap (3-View + Outfit Sheet)** — PRE-PRODUCTION FOUNDATION. Do once at project start. Generate one character reference sheet image + one outfit/prop sheet, host on Cloudinary/S3. URLs pasted into EVERY downstream img2img call.
