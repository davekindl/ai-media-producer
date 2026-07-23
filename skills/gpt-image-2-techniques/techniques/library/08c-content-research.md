# Content & Research Outputs

11 techniques. Each entry includes prompt template, source, gotchas, stack notes, and (when relevant) cross-references.

Use the skill's discovery step to pick the right one for a given request.

---

## A8C-T1 — Editorial-Opinion Hero (B&W Conceptual)

**Score:** ★★★★☆ (4/5)  
**Source:** NYT op-ed conventions + Imagine.art  
**Use case:** Single high-contrast conceptual illustration for op-ed/essay. NYT op-ed page + Working Theorys hero art aesthetic. Two symbolic objects in tension, stark lighting. Reads as editorial considered, not AI-stock.

**Prompt template:**

```
A black and white editorial illustration for an opinion piece about artificial intelligence. A human hand and a robotic hand reaching toward each other across a divide, dramatic contrast lighting, high-contrast ink illustration style, stark and conceptual, newspaper editorial aesthetic. No text, no logo, generous negative space, 16:9.
```

**Gotchas:** Drop 'editorial' + 'newspaper aesthetic' tags and model regresses toward glossy stock photography.

**Stack with:** LinkedIn pulse posts, Substack essay heroes, your flagship project section openers.

---

## A8C-T10 — Multilingual Editorial (HU + EN bilingual hero)

**Score:** ★★★★☆ (4/5)  
**Source:** Segmind + VentureBeat 2.0 launch  
**Use case:** In-image text rendering for your local-language brand alongside your primary-language brand without separate typesetting. Hungarian Latin-extended (ő, ű, á, é, í, ó, ú) reliable.

**Prompt template:**

```
A bilingual editorial hero image for a Hungarian-English AI consultancy. Cream background (#F8F5EE), 16:9. Left half: English headline in quotes: 'THINKS IN SYSTEMS. SHIPS IN WEEKS.' Right half: Hungarian headline in quotes: 'RENDSZERBEN GONDOLKODIK. HETEK ALATT SZÁLLÍT.' Typography: black condensed serif, both headlines same size, divided by a thin vertical line. Below both, small-caps brand marks: 'NOVOLITH' on left, 'MI-ÉRTED' on right. Minimal editorial illustration element centered — a Möbius strip glyph. Generous negative space, literary aesthetic, use case: LinkedIn banner / website hero.
```

**Gotchas:** Non-quoted Hungarian gets misspelled diacritics (á → a, ő → o). Always quote verbatim.

**Stack with:** your consulting website, bilingual LinkedIn, pitch-deck covers for HU SMB outreach, your long-form publication HU edition.

---

## A8C-T2 — The 8-Element Framework (Scene→Constraints)

**Score:** ★★★★★ (5/5) · `foundational`  
**Source:** Felo.ai 8-element + OpenAI cookbook  
**Use case:** Canonical structure for any GPT-Image-2 prompt. Cuts iteration cycles roughly in half. Single highest-leverage prompting pattern.

**Prompt template:**

```
[Core Subject]: one line, what the image IS
[Details]: materials, textures, colors
[Action & Position]: where in frame, what it's doing
[Setting]: environment, time, weather
[Lighting]: source, direction, temperature
[Camera]: lens, DOF, angle (50mm, f/1.8, 45° overhead)
[Style & Medium]: photo / editorial ink / flat vector / watercolor
[Constraints]: no text OR exact text in quotes, aspect ratio, what to exclude
[Use case]: "for a Nature journal cover" / "for LinkedIn pulse header"
```

**Gotchas:** Writing one flowing paragraph kills the reasoning step. Always section.

**Stack with:** FOUNDATIONAL — base layer for every other technique. Without this, every other produces 40% of potential.

---

## A8C-T3 — Annotated Diagrams with In-Image Labels

**Score:** ★★★★☆ (4/5)  
**Source:** sci-draw.com 8 rules + OpenAI cookbook  
**Use case:** Cross-section / flowchart / system diagram with leader lines, labels, arrows rendered INSIDE the image. Replaces Figma/Lucidchart for draft-quality explainers.

**Prompt template:**

```
RESEARCH DIAGRAM:
A detailed cross-section diagram of a human heart, fully labeled — left ventricle, right ventricle, aorta, pulmonary artery, valves, and chambers. Clean flat illustration style, red and pink color scheme, white background, clear sans-serif label typography with leader lines. Labels in quotes: 'Left Ventricle', 'Right Ventricle', 'Aorta', 'Pulmonary Artery', 'Mitral Valve', 'Tricuspid Valve'. 4:3 aspect ratio, high quality, no extra decorative elements.

DAVE-RELEVANT (10-step methodology):
A flat vector diagram titled 'The 10-Step Innovation Methodology' showing ten labeled steps in a vertical domino chain: 'Absorb', 'Apply Personally', 'Extract Method', 'Package', 'Distribute', 'Iterate', 'Industrialize', 'Tools', 'Systems', 'Monetize'. Each step rendered as a rounded rectangle linked by a curved arrow. Navy background (#0B1220) with teal (#00E0C6) and purple (#8B5CF6) accents. Sans-serif labels. Datadog-style info-density. 16:9, use case: your command center dashboard graphic.
```

**Gotchas:** Vague label lists ('add labels for each part') produce hallucinated misspelled text. Always quote every string verbatim.

**Stack with:** Protocol lesson diagrams, your flagship project chapter explainers, your command center 'My Method' panel, LinkedIn carousel slides.

---

## A8C-T4 — Multi-Reference Chapter Series Lock (img2img)

**Score:** ★★★★★ (5/5)  
**Source:** GPT-Image-2 Edit + 16-ref img2img  
**Use case:** THE single unlock for long-form series. Generate ONE hero style-bible image, then for each chapter call img2img with style-bible + chapter sketch + palette + typography refs. Never re-describe style in words. ~$5-13 for ALL 42 your flagship project assets.

**Prompt template:**

```
STAGE 1 — generate style bible:
A cinematic editorial illustration for a research publication on AI futures. A solitary figure in silhouette stands on a ridge at blue hour, looking across a valley where bioluminescent data-streams flow like rivers. Muted teal-navy palette (#0B1220 base, #00E0C6 highlights), grain texture, painterly brush strokes, low contrast sky, high contrast silhouette. No text. 16:9, high quality. Use case: chapter hero for a 14-chapter AI futures research book, style-bible reference.

STAGE 2 — subsequent chapter call:
Create a chapter hero matching the reference image's style, palette, composition, and lighting exactly. Subject change only: replace the ridge-silhouette with a workshop interior — an older craftsman at a workbench, tools glowing faintly as if touched by a neural field. Keep all else identical. No text.

WORKFLOW:
1. Generate style-bible image with full 8-element prompt (a8c-t2). Save as chapter_style_reference.png.
2. For each chapter call img2img with: input_urls: [style_ref.png, chapter_sketch.png, palette_card.png, typography_card.png] + short prompt: "Create chapter hero for [topic]. Match style/palette/composition/typography/lighting of first reference exactly."
3. Never re-describe the style in words — refs carry it.
```

**Gotchas:** Verbose style description alongside refs causes conflict — model blends written instructions with visual evidence and drifts. Trust refs, keep prompts short.

**Stack with:** FOUNDATIONAL for any series. your flagship project 14 chapters, Protocol course, newsletter editorial seasons.

---

## A8C-T5 — Book Cover / Manifesto Cover (Single Focal Point)

**Score:** ★★★★☆ (4/5)  
**Source:** DAMONZA 2026 trends + Imagine.art  
**Use case:** Single dominant element, not collage. Generous negative space, restrained palette. Renders book cover titles reliably when text quoted + typeface specified.

**Prompt template:**

```
A book cover design for a research publication titled 'THE HORIZON ENGINE'. Subtitle: 'Mapping the AI Futures We Haven't Built Yet'. Author name: '[Author Name]'. Deep navy background (#0B1220), a single centered illustration of a compass rose dissolving into data-particles at its edges, muted teal and purple accents. Title 'THE HORIZON ENGINE' in large condensed serif (Playfair or similar), upper third, white. Subtitle in small caps sans-serif below. Author name lower center, small. Painterly texture, generous negative space, literary-research hybrid aesthetic. 2:3 portrait aspect ratio, 4K.
```

**Gotchas:** Multi-element collage covers read as amateur. Single focal point + restraint = professional.

**Stack with:** your book edition, your manifesto, any of your long-form publications. Generate LAST after 42 chapter assets exist; feed 5 strongest heroes as references.

---

## A8C-T6 — Newsletter / LinkedIn Hero (Project-Folder Workflow)

**Score:** ★★★★☆ (4/5)  
**Source:** [Jenny Ouyang buildtolaunch.substack](https://buildtolaunch.substack.com/p/how-i-create-consistent-hero-images-and-why-i-havent-switched-to-nanobanana)  
**Use case:** Character/scene anchor + project folder = newsletter heroes instantly recognisable as YOURS. 90% first-try satisfaction. 2.0's 16-ref img2img improves consistency rather than breaks.

**Prompt template:**

```
SYSTEM-PROMPT FOR PROJECT FOLDER:
You generate hero images for [Your Name] / [Your Brand] / your consulting brand.
Style bible:
- 3D editorial illustration, desaturated palette, navy + teal + subtle warm accent
- 16:9 aspect ratio, single focal point, generous negative space
- your brand voice: thinks-in-systems, no fluff, direct
- Never include text in the image unless explicitly asked
- Always match character appearance to reference pool
Output: one detailed GPT-Image-2 prompt using the 8-element framework.

PER-POST SLASH:
/hero [topic] → ChatGPT drafts the prompt → pass to GPT-Image-2 with reference pose images.
```

**Gotchas:** Regenerating style description per post = slow drift. Treat reference pool + system prompt as canonical.

**Stack with:** LinkedIn pulse (your #1), Substack newsletter, X/Twitter long-tweets.

---

## A8C-T7 — your command center Datadog-Style Data Widget

**Score:** ★★★★★ (5/5)  
**Source:** OpenAI cookbook UI mockup + a Datadog-style aesthetic  
**Use case:** Tight info-density, navy/charcoal ground, teal/purple accents, in-widget labels, sparkline-like elements. The aesthetic you specify for your command center.

**Prompt template:**

```
A dashboard widget graphic in the style of a Datadog dark-mode panel. Background: deep navy (#0B1220) with charcoal panel backgrounds (#1A2332). A single card showing: header text 'PROJECT HEALTH — AI_HORIZON_ENGINE' in small-caps sans-serif white, below it a sparkline chart with teal (#00E0C6) line on a subtle grid, below that three stat tiles labeled 'UPTIME 99.2%', 'SIGNALS 23', 'DAYS ACTIVE 412', each stat rendered large and purple (#8B5CF6). Typography: Inter or similar geometric sans. Info-dense but readable, subtle inner glow on accents. 16:9, high quality, use case: your command center dashboard screenshot graphic.
```

**Gotchas:** 'Dashboard' alone produces generic corporate BI. Need 'Datadog dark mode' or named reference for info-density.

**Stack with:** your skill/tool icons, project status cards, LinkedIn command-center posts, automated morning briefings.

---

## A8C-T8 — Annotated Screenshot / Explainer Overlay

**Score:** ★★★★☆ (4/5)  
**Source:** [PixelDojo + fal.ai learn](https://pixeldojo.ai/guides/gpt-image-2-prompting-guide)  
**Use case:** Screenshot-like composition with arrows, circles, callouts, labels rendered INTO the image. Eliminates whole Figma/Annotate.app step.

**Prompt template:**

```
A stylized screenshot explainer graphic for an AI upskilling lesson. Center: a flat illustration of a software interface panel with three visible buttons labeled 'Task', 'Workflow', 'System'. Overlay four annotated callouts with leader lines pointing to specific interface elements:

- Top-right callout with red arrow: 'Input brief (natural language)'
- Middle callout with teal arrow: 'Parsed into subtasks'
- Bottom-left callout with purple arrow: 'Agent team dispatched'
- Bottom-right callout with orange arrow: 'Results validated + reported'

Light cream background (#F8F5EE), your editorial style, clean sans-serif labels, subtle drop shadow on the interface panel. 16:9, use case: your course Lesson 4 illustration.
```

**Gotchas:** Describing arrow positions abstractly fails. Be specific: 'red arrow from upper-right callout pointing to Task button.'

**Stack with:** your long-form publication lessons, your flagship project research figures, LinkedIn carousels, Substack deep-dives.

---

## A8C-T9 — LinkedIn Carousel Slide System (5-10 slides @ 1080x1080)

**Score:** ★★★★☆ (4/5)  
**Source:** [carouselli + postiv + contentin](https://carouselli.com/blog/how-to-create-linkedin-carousel)  
**Use case:** Document carousels = ~24% engagement vs ~3% text — 596% multiplier. Sweet spot 5-10 slides. Generate each slide individually with same style ref → reads as designed not templated.

**Prompt template:**

```
SLIDE 1 (hook/cover):
LinkedIn carousel cover slide, 1:1 aspect ratio, 1080x1080. Large bold headline in quotes: 'AI WON'T REPLACE YOU. IT'LL REVEAL YOU.' Typography: black condensed sans-serif, left-aligned, upper half. Below, small-caps subline: 'A 7-STEP UPSKILLING METHOD'. Lower right: small author credit '[YOUR NAME]'. Cream background (#F8F5EE), single editorial illustration element in lower-left — a magnifying glass resting on a book. your brand aesthetic, generous negative space, use case: LinkedIn carousel slide 1 of 8.

SLIDE N (content slide, using slide 1 as ref):
LinkedIn carousel content slide, 1:1 aspect ratio, 1080x1080. Match reference image's style, palette, typography, and margins exactly. Headline in quotes: 'STEP 3: EXTRACT THE METHOD'. Body text in quotes: 'Turn the personal application into a repeatable pattern. If you can't name the steps, you haven't extracted it.' Small '[YOUR NAME] · 3/8' label at bottom. Use case: LinkedIn carousel content slide.
```

**Gotchas:** Not using slide 1 as ref for slides 2-10 → reads as inconsistent. Lock ref before slide 2.

**Stack with:** LinkedIn (your #1), Protocol previews, your book chapter summaries, campaign teasers.

---

## A8C-TBONUS — Magazine-Grade Composite Layout (Headline + Hero + Pullquote)

**Score:** ★★★★☆ (4/5)  
**Source:** OpenAI launch coverage + Coaley Peak  
**Use case:** GENUINELY NEW in 2.0. Full magazine-style spread — masthead, headline, hero, byline, pull quote — all composed by model in one pass. OpenAI calls it 'magazine-grade'.

**Prompt template:**

```
A magazine editorial spread, 16:9 landscape. Left third: large serif headline in quotes: 'THE QUIET DISPLACEMENT'. Below, deck in smaller italic serif: 'How AI is reshaping knowledge work without anyone noticing.' Below that, byline: 'By [Your Name] · [Your Brand]'. Right two-thirds: an editorial illustration of an empty office at dusk, one lamp on a desk still lit, subtle ghost-figure of a silhouetted worker fading into pixels at the window. Muted navy-teal palette. Bottom-right pull-quote card in quotes: 'The systems don't announce themselves. They just become the water.' your brand aesthetic, magazine-grade layout. 4K.
```

**Gotchas:** Cap at 4 text blocks per image (masthead + headline + deck + hero + pullquote + footer is too many).

**Stack with:** your flagship project chapter openers (highest impact), Substack longform covers, pitch-deck section dividers, manifesto pieces.

---
