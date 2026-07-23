# Editorial / Informational Design

10 techniques. Each entry includes prompt template, source, gotchas, stack notes, and (when relevant) cross-references.

Use the skill's discovery step to pick the right one for a given request.

---

## A2-T1 — @dotey Hand-Drawn Infographic Card (origin of 'Abhishek framework')

**Score:** ★★★★★ (5/5)  
**Source:** [@dotey (宝玉), X — ported to GPT-Image-2 April 2026](https://x.com/dotey/status/1996303762428731486)  
**Use case:** The actual origin of what circulates as the 'Abhishek framework'. Beige paper + red-black calligraphy title + 2-4 sections + hand-drawn icons. Single highest-leverage prompt for this angle.

**Prompt template:**

```
Create a hand-drawn style infographic card in a 9:16 vertical format.
The card has a clear theme: {THEME / QUOTE / MAIN POINT}.
Background: beige or off-white with subtle paper texture, simple and friendly hand-drawn aesthetic.
Title typography: at the top, bold large calligraphy brush-strokes in red and black, drawing attention. All body text is in {LANGUAGE} hand-lettered/brush script.
Layout: 2–4 sections, each with short, concise phrases. Script keeps a rhythmic flow.
Leave white space around. Add simple hand-drawn illustrations or icons.

Text VERBATIM, no substitutions:
  Title: "{EXACT TITLE}"
  Section 1: "{EXACT TEXT}"
  Section 2: "{EXACT TEXT}"
  Section 3: "{EXACT TEXT}"
  Section 4: "{EXACT TEXT}"
```

**Gotchas:** GPT-Image-2 invents sub-section text unless every line marked VERBATIM. For Hungarian add 'ensure diacritics render exactly' or model substitutes Chinese-ish glyphs (brush style biases). 1:1 cannot do 4K.

**Stack with:** Pass beige JPEG as input_urls[0] to lock paper tone. Render 5 cards in batch: same background block, only vary {THEME}+section text.

---

## A2-T10 — SYNTH: Series-Consistent Educational Poster Set

**Score:** ★★★★☆ (4/5) · `synth`  
**Source:** Synthesis using sequential consistency + 16-ref  
**Use case:** Multi-part explainers. 10-part LinkedIn series. your 10-step methodology as 10-poster set. Two-stage: render canonical parent, then siblings using parent as reference.

**Prompt template:**

```
STAGE 1 — parent poster:
Create first of {N} educational posters, 9:16, 4K. This parent sets visual language for all {N}. Lock:
- Background: {EXACT, e.g., "warm off-white with linen texture"}
- Title bar: {EXACT STYLE}, top 15%
- Mascot: {EXACT CHARACTER}
- Palette: exactly 3 colors — {C1}, {C2}, {C3}
- Typography: headline {FONT_A}, body {FONT_B}
- Footer: small "Poster 1 of {N}" bottom-right

This poster covers Part 1: "{PART 1 TITLE}".
Title: "{PART 1 TITLE}"
Sections: 1. "{TEXT}" 2. "{TEXT}" 3. "{TEXT}"

STAGE 2 — siblings using parent as reference:
Create poster {K} of {N} in same series. Use attached reference(s) for visual language exactly.

Only changes:
- Footer: "Poster {K} of {N}"
- Content: Part {K}: "{PART K TITLE}"

API call (kie.ai):
POST https://api.kie.ai/api/v1/jobs/createTask
{ "model": "gpt-image-2-image-to-image",
  "input": {
    "prompt": "{STAGE 2 PROMPT}",
    "aspect_ratio": "9:16",
    "resolution": "4K",
    "input_urls": ["{URL_TO_PARENT}", "{URL_TO_POSTER_K-1}"]
  }
}
```

**Gotchas:** >5 refs over-weight older refs; stick to parent + previous sibling. After ~poster 7, regenerate using only parent. Different subject types shifts illustration style — lock 'illustration vocabulary: {EXACT TYPES}' in parent.

**Stack with:** Pair with business-mvp — 10 posters as visual half of deliverable. ~$1.20 at 4K total.

---

## A2-T2 — Article → Cartoon Infographic 16:9 (@dotey landscape)

**Score:** ★★★★★ (5/5)  
**Source:** [@dotey, X 2026](https://x.com/dotey/status/1993567848564686926)  
**Use case:** Feed full article/section/blog post → return one-image summary readable in 10 seconds. Substitutes for $150-500/infographic designer hire.

**Prompt template:**

```
Create a cartoon-style infographic based on the provided content:
- Hand-drawn illustration style, landscape 16:9
- Simplify: emphasize keywords + core concepts, ample whitespace
- Minimalistic cartoon elements, icons, simple portraits
- Color palette {2-3 BRAND COLORS + off-white background}
- Typography: clear hand-lettered headers, friendly sans body
- Layout: bold title block left/top, 3-5 modules L→R or top→bottom, summary/CTA block

Content (verbatim, no paraphrasing):
"""
{PASTE ARTICLE OR KEY POINTS HERE}
"""

No extra decorative text, no lorem-ipsum, no duplicated labels, no watermarks.
```

**Gotchas:** >6 modules abbreviates body even with VERBATIM. Default 'cartoon' is Western-children's-book; for business add 'mature editorial illustration, NOT children's book, NOT Disney'.

**Stack with:** Run text through Claude first to extract 5 key points in imperative voice. resolution=4K for dense layouts.

---

## A2-T3 — Atlabs 5-Pattern Infographic Library

**Score:** ★★★★☆ (4/5)  
**Source:** [Atlabs AI April 24 2026](https://www.atlabs.ai/blog/30-nano-banana-prompts-for-perfect-infographics-ultimate-infographic-lookbook)  
**Use case:** 5 layout archetypes — sketchnote, mind map, soft-pastel educational, technical flowchart, checklist — each with verbatim fill-in-the-blank template. Pick layout matching content shape.

**Prompt template:**

```
SKETCHNOTE:
Design sketchnote infographic for {TOPIC}. Background: crumpled graph paper texture. Style: doodle thick marker, hand-drawn arrows, circled text, stars. Typography: handwriting, mix print + cursive, hierarchy by size. Color: 80% black ink + 2 highlighters ({ACCENT_1}, {ACCENT_2}). Layout: non-grid, flowing, 5-8 concept clusters with connector arrows. Hand-drawn icons. Text verbatim: {EXACT TEXT BLOCKS}

MIND MAP:
Create complex mind-map for {TOPIC}. Layout: central node + 4-6 radial branches, each with 2-4 sub-nodes. Style: colored bubbles + curved organic lines, biological feel. Color-code each main branch. Labels short (2-5 words), legible sans. Text verbatim: {NODE TEXT}

SOFT-PASTEL EDUCATIONAL:
Create soft educational infographic for {TOPIC}. Hand-drawn vector, polished. Colors: pastels (mint, peach, lavender, butter). Rounded friendly shapes. 4-6 modules with clear reading order, dotted-line connectors, ~30% whitespace. Rounded sans body, hand-lettered headers. Text verbatim: {EXACT TEXT}

TECHNICAL FLOWCHART:
Design flow-chart for {TOPIC}. Geometric shapes — diamonds (decisions), rectangles (actions), rounded (start/end), parallelograms (i/o). Blueprint: thin white/cyan on dark navy OR black on graph paper. Right-angle connectors only. 6-12 nodes. Label each connector (Yes/No/If X). Mono or technical sans. Text verbatim: {NODE TEXT IN ORDER}

CHECKLIST:
Vertical checklist for {TOPIC}. Stylized clipboard or torn-paper. 10 items, round/square checkbox left, handwritten text, margin doodles. Hand-lettered title, "completed by ___ date ___" footer. Text verbatim: {10 ITEMS}
```

**Gotchas:** 'Sketchnote' alone gives infantile output; the crumpled-graph-paper + thick-marker + highlighter stack separates editorial from AI-slop. Mind maps default to tree unless told 'radial.' Flowchart needs shape-per-function spelled out.

**Stack with:** Combine with a2-t4 vocabulary. 4K for SOP print.

---

## A2-T4 — baoyu-skills Layout × Style Grid (340 combos)

**Score:** ★★★★☆ (4/5)  
**Source:** [GitHub JimLiu/baoyu-skills](https://github.com/jimliu/baoyu-skills)  
**Use case:** 20 layouts × 17 styles = 340 combinations. Pick layout (pyramid, fishbone, mind-map, ikea-manual, journey-path...) and style (claymation, chalkboard, aged-academia, technical-schematic, lego-brick...). The grid IS the IP.

**Prompt template:**

```
Create infographic for the following content.
Layout: {bridge | circular-flow | comparison-table | do-dont | equation | feature-list | fishbone | funnel | grid-cards | iceberg | journey-path | layers-stack | mind-map | nested-circles | priority-quadrants | pyramid | scale-balance | timeline-horizontal | tree-hierarchy | venn}
Style: {craft-handmade | claymation | kawaii | storybook-watercolor | chalkboard | cyberpunk-neon | bold-graphic | aged-academia | corporate-memphis | technical-schematic | origami | pixel-art | ui-wireframe | subway-map | ikea-manual | knolling | lego-brick}
Aspect: {16:9 | 9:16 | 1:1 | 4:3 | 3:4}, Resolution: {1K | 2K | 4K}.

Content (verbatim, no paraphrasing):
"""
{CONTENT}
"""

No filler text, no watermarks, no lorem-ipsum, all labels from content above.
```

**Gotchas:** Some combos fight: fishbone × kawaii is weird, mind-map × technical-schematic redundant. ikea-manual works best with journey-path/bridge/layers-stack. Claymation + lego-brick fail on body text <24pt — use for headers only.

**Stack with:** Layout vocabulary alone is a cheat-sheet. Combine with a2-t3 style-specific body-text instructions.

---

## A2-T5 — OpenAI Instructional Design Brief (Educational/Scientific)

**Score:** ★★★★★ (5/5)  
**Source:** [OpenAI Cookbook GPT-Image-2 prompting guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)  
**Use case:** Anatomical diagrams, chemistry reactions, biology labels, classroom explainers, flat scientific icon systems — anything with strict factual labels for print/slide use. OpenAI's official-sanctioned pattern.

**Prompt template:**

```
Produce educational diagram as if written by instructional designer:
- Audience: {8th graders | undergraduates | medical professionals}
- Lesson objective: {SINGLE SENTENCE}
- Visual format: flat scientific illustration, consistent icon style, clear arrows, readable labels, generous whitespace
- Aspect: {16:9 | 4:3}, Resolution: 4K

Required labels (verbatim, no extras):
  {LABEL 1} — pointing to {FEATURE 1}
  {LABEL 2} — pointing to {FEATURE 2}
  ...

Scientific constraints: {e.g., "proportions match real human heart," "organelles in correct positions," "reaction arrows reactants → products"}.

Style: no photorealism, no cartoonish mascots, no decorative elements, no colored backgrounds other than pale neutral.
```

**Gotchas:** Without quality=high or 4K, dense labels compress to illegibility. Model adds false labels for unfamiliar subjects — list every label verbatim AND add 'do not add any labels not listed'. Verify with domain expert.

**Stack with:** Pair with reference image of anatomically-correct structure to lock geometry.

---

## A2-T6 — Chalkboard / Aged-Academia Editorial Poster

**Score:** ★★★★☆ (4/5)  
**Source:** [Oimi top-50 April 2026](https://oimi.ai/en/blog/chatgpt-images-2-hot-prompts)  
**Use case:** Warm professorial feel for educational + 'this is a serious-but-inviting idea' business framing. Hormozi-whiteboard, Noah-Kagan-napkin-math vibe.

**Prompt template:**

```
Generate chalkboard-style infographic 16:9 horizontal.
Background: black chalkboard texture with subtle chalk dust + faint chalk-erase marks.
Elements: simplified info using minimalistic cartoon, icons, simple portraits — ALL in colored chalk rendering, no realistic illustrations.
Color: white primary + 3 chalk accents (yellow, peach, pale blue).
Layout: bold title top in chalk lettering, 4-6 sections in visual hierarchy with chalk arrows.
Typography: hand-drawn chalk lettering for titles, cleaner printed-chalk for body.
Text verbatim: {EXACT TITLE AND SECTION TEXT}.
No photo-realistic elements, no digital effects, only chalk.
```

**Gotchas:** Without 'all in colored chalk rendering, no realistic illustrations' it mixes realistic photos with chalk — looks terrible. Chalk lettering <18pt illegible.

**Stack with:** Series: render your framework's steps as 10 chalkboard explainers.

---

## A2-T7 — IKEA-Manual Visual SOP / Recipe Card

**Score:** ★★★★☆ (4/5)  
**Source:** baoyu-skills + PromptBase + @dotey synthesis  
**Use case:** Any numbered sequence — recipes, equipment-assembly, software-onboarding, business-process, safety drills. Replaces tech-writer hire for internal docs.

**Prompt template:**

```
Create IKEA-manual visual SOP for {TASK}, {16:9 or 3:4}, {2K or 4K}.

Visual: clean line-art, 2 colors max (typically black on warm-off-white + ONE accent — blue or red), minimal shading, high-contrast. Simple stick/blob figures, neutral expressions.

Layout: large title block top in {PRIMARY LANGUAGE} "{TASK NAME}" bold sans. Below: grid of numbered steps. Each step:
- Large numeral (1, 2, 3...) in circle/square
- Line-art illustration of action
- ONE arrow indicating motion
- Short caption: verbatim from list below

No decorative backgrounds, no paragraphs, no brand logos, no photorealism, no color except the one accent.

Steps (verbatim text for captions):
Step 1: "{EXACT TEXT}"
Step 2: "{EXACT TEXT}"
...
Step N: "{EXACT TEXT}"

Optional: "DO NOT" panel in red with 2-3 mistakes verbatim.
```

**Gotchas:** Adds shading/gradients unless told '2 colors max, no shading, no gradients, no halftones.' Stick-figure bias strong; for blobby IKEA-people add 'use rounded shape-based figures, NOT stick figures.' Captions >8 words wrap awkwardly.

**Stack with:** Multi-page: render page 1, feed as input_urls[0], ask 'page 2, same visual language' — sequential consistency shines.

---

## A2-T8 — Knowledge-Density Japanese Ponchi-e Slide

**Score:** ★★★★☆ (4/5)  
**Source:** [@yammamon, X April 2026](https://x.com/yammamon/)  
**Use case:** Cram absurd info-density on one slide while staying coherent and warm — Japanese government white-paper slides + friendly Irasutoya clip-art. Great for dense investor memos / research summaries.

**Prompt template:**

```
Create explanatory slide (ponchi-e / ポンチ絵) fusing gentle Irasutoya アニメ aesthetic with overwhelming info density of Kasumigaseki 霞が関 government-ministry slides.

Format: 16:9, 4K, white or pale-pastel.

Style: flat vector illustration, soft rounded characters with simple expressions (Irasutoya-style mascots), paired with dense organized info blocks using boxes, arrows, labels, numbered sections (Kasumigaseki).

Typography: clean sans-serif body, slightly bolder labels, largest type for headline.

Content: {TOPIC AND STRUCTURE}. Use VERBATIM text for all labels and callouts.

Labels verbatim:
- Title: "{EXACT}"
- Section 1: "{EXACT}" → caption "{EXACT}"
- Section 2: "{EXACT}" → caption "{EXACT}"
- ...
- Legend/footer: "{EXACT}"
```

**Gotchas:** Defaults to Latin script unless told 'render all labels in {LANGUAGE}'. <4K compresses text. Don't ask for photorealism — charm is in flat-vector/clip-art blend.

**Stack with:** For HU/EN bilingual: feed Kasumigaseki slide screenshot as input_urls[0] to lock layout language.

---

## A2-T9 — SYNTH: Cheat-Sheet Grid (Learn-X-in-Y-Days)

**Score:** ★★★☆☆ (3/5) · `synth`  
**Source:** Synthesis @dotey + Atlabs + OpenAI VERBATIM  
**Use case:** Reference posters. Print-to-wall cheat sheets. Carousel where each slide is a topic's cheat sheet. No canonical prompt existed for 'Python in 30 days' format — combines @dotey + Atlabs + OpenAI VERBATIM into reusable template.

**Prompt template:**

```
Create cheat-sheet poster for "{TOPIC IN {N} DAYS/STEPS/KEYS/COMMANDS}."

Format: 3:4 OR 9:16 vertical {2K or 4K}.

Layout: top 15% = bold title block "{TOPIC}" + subtitle "Cheat sheet — {N} items." Remaining 85% = grid of {N} cells {grid dims, e.g., 5×6 for 30 items}.

Each cell:
- Large monospaced code/command/shortcut top half
- Short (3-8 word) plain explanation bottom half in friendly sans
- ONE tiny corner icon for category (optional)

Visual: {soft-pastel educational | chalkboard | aged-academia parchment | corporate-memphis | terminal-dark neon}.

Color-coding: group-related cells share background tint. Small legend bottom margin.

Typography: display sans for headline; monospaced (JetBrains Mono / Consolas) for cell commands; rounded sans for body. ALL text VERBATIM from list — do not substitute, do not invent, do not auto-complete.

Grid content (verbatim):
1. "{CMD/KEY/TERM_1}" : "{EXPLANATION_1}"
2. "{CMD/KEY/TERM_2}" : "{EXPLANATION_2}"
...
{N}. "{CMD/KEY/TERM_N}" : "{EXPLANATION_N}"

No filler, no lorem-ipsum, no extra cells, no duplicates, no watermarks, no © marks.
```

**Gotchas:** >40 cells unreadable even at 4K — split. Without 'do not auto-complete', model invents nonexistent commands.

**Stack with:** Build series: fix header, vary {TOPIC}+cells.

---
