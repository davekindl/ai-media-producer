---
name: gpt-image-2-techniques
description: "Generate production-quality branded images via kie.ai's GPT-Image-2 using a curated catalog of 117 techniques. Runs a discovery step that proposes the top 3 best-matching techniques and lets the user pick before generating. Trigger when the user wants to generate an image or brand/visual asset, mock up a screen or dashboard, build a share card, PDF cover, LinkedIn carousel, landing-page hero, infographic, magazine cover, music album cover, localized B2B collateral, or ad creatives, or to run img2img from reference images. Also triggers on: 'gpt-image-2', 'kie.ai image', 'album cover', 'LinkedIn carousel slide', 'editorial infographic', 'image generation', 'brand asset', 'mockup', 'social card', 'sketchnote', 'SOP / IKEA-manual diagram', 'trading card', 'anatomy or exposure-map diagram', and 117+ other specialized techniques. Brand kits: acme-consulting (generic starter template — copy and customize for your own brand)."
---

# gpt-image-2-techniques

> 117-technique catalog wrapped around kie.ai's GPT-Image-2 endpoint, with a discovery step that proposes the top 3 best-matching techniques per request and lets the user pick. Brand-locked. Production-ready.

## Shared Infrastructure
- **API client:** `kie_client.py` (included in this skill folder — reads `KIE_AI_API_KEY` from environment)
- **Brand kits:** `brand_kits/` (local folder — acme-consulting template; copy it for your own)

## Architecture

```
gpt-image-2-techniques/
├── SKILL.md                         (this file — operating instructions)
├── kie_client.py                    (kie.ai API wrapper: submit_text_to_image, submit_image_to_image, poll, generate)
├── techniques/
│   ├── _index.md                    (one-liner directory of all 117 techniques — read at discovery time)
│   └── library/
│       ├── 01-brand-identity.md           (13 techniques, full prompt templates)
│       ├── 02-editorial-info.md           (10)
│       ├── 03-web-app-ui.md               (13)
│       ├── 04-marketing-ads.md            (15)
│       ├── 05-multi-tool-stacking.md      (7)
│       ├── 06-reverse-style-transfer.md   (14)
│       ├── 07-personalization-portraits.md (13)
│       ├── 08a-music-brand.md            (10)
│       ├── 08b-client-b2b.md              (10)
│       ├── 08c-content-research.md        (11)
│       └── 09-video-keyframe-bible.md     (1 — keyframe asset for video pipelines)
└── brand_kits/
    ├── _index.json                  (registered kits)
    └── acme-consulting.json         (generic starter template — copy and customize for your brand)
```

## The discovery workflow

**Every request runs through these 4 steps. Do not skip discovery.**

### Step 1 — Parse the request

Identify these dimensions from the user's natural-language request:

1. **Output type:** `image-only` (always for this skill — img2img is fine, but never video)
2. **Specific deliverable:** share card, landing hero, dashboard, PDF cover, carousel slide, ad, infographic, album cover, magazine, mockup, etc.
3. **Audience:**
   - `B2C consumer` (broad)
   - `B2B enterprise` (HR/L&D directors, formal register for HU)
   - `Personal/portfolio` (your own brand)
4. **Brand fit:** `acme-consulting` / your-own-kit / `none — generic`
5. **Language:** `en` / your-language / `bilingual`
6. **Aspect/format hint:** square, vertical, wide, print-ready, etc.
7. **Mode:** `text-to-image` or `image-to-image` (img2img if user mentions "based on this", "similar to", "use this as a reference", or attaches/references existing assets)
8. **Stylistic register:** premium-restrained / cinematic-mythic / hand-drawn-friendly / editorial-illustration / sepia-academic / etc.
9. **Hidden constraints:** any avoid list, must-include text, etc.

### Step 2 — Scan the index, propose top 3

1. Read `techniques/_index.md` once (always do this; it's the discovery directory).
2. Match candidates against the request dimensions. Prioritize:
   - **Output deliverable match** (highest weight — share card request → share-card techniques)
   - **Audience match** (B2B request → B2B-flavored techniques)
   - **Score** (★★★★ and ★★★★★ outrank ★★ and ★)
   - **Foundational tags** — when the request is about brand consistency, multi-asset coherence, or "do this for everything," elevate **[foundational]** techniques (a1-t3, a3-t2, a3-t3, a3-t10, a6-t2, a8c-t2)
   - **Synth tags** — when the request is about a multi-step deliverable or workflow, prefer **[synth]** entries (these are recipes, not single prompts)
3. Pick the **3 best matches** spanning at least 2 categories where possible (give the user variety in approach, not 3 takes on the same idea).
4. For each pick, prepare a concise rationale: why it fits, what makes it different from the other two picks, what variables the user will need to provide.

### Step 3 — Present and wait for user selection

Output a structured proposal in this exact format (markdown table or list — pick whichever fits the response register):

```
Based on your request "[paraphrase]", here are 3 techniques that fit:

1. **[ID] [name]** ★★★★ — [rationale: why this fits, what variables needed]
   _Strength:_ [the one thing this does best]
   _Trade-off:_ [what you give up vs the other options]

2. **[ID] [name]** ★★★★★ — [rationale]
   _Strength:_
   _Trade-off:_

3. **[ID] [name]** ★★★ — [rationale, often this is the wildcard or premium reinterpretation]
   _Strength:_
   _Trade-off:_

Which one do you want me to run? Or describe what's missing and I'll re-propose.
```

If the request is unambiguous and one technique is overwhelmingly the right answer (e.g. "I want a Pokémon-style trading card for X" → a7-t5 is the only real match), still show 3 but make it clear option 1 is the canonical pick — don't overwhelm with weak alternatives.

### Step 4 — Execute

Once the user picks (or specifies):

1. **Read the full technique** from the appropriate `library/{category}.md` file.
2. **Load the brand kit** from `brand_kits/{name}.json` (default: `acme-consulting`; copy it as a starter for your own kit).
3. **For Hungarian content:** Apply correct register (Ön for B2B enterprise, te for SME/consumer), native term substitutions (megtérülés not ROI; versenyelőny not "kompetitív előny"), compound-word rules, correct punctuation, and date format (2026. április 18.).
4. **Assemble the final prompt**:
   - Start with the technique's prompt template
   - Substitute all `{placeholders}` with user-provided variables (ask for missing required vars)
   - Inject brand kit fields (palette hex codes, typography, logo description, voice, hard negatives)
   - Append the brand kit's negatives at the end
   - For HU register: explicitly state "use Ön form" or "use te form (consumer register)" — never let the model default
5. **Call kie.ai** via `kie_client.generate()`:
   ```python
   from kie_client import generate
   result = generate(
       prompt=final_prompt,
       aspect_ratio="16:9",     # or whatever the technique specifies
       resolution="2K",          # 1:1 cannot be 4K — use 2K
       input_urls=[...] if mode == "image-to-image" else None,
       output_path="./out/asset.png",
       log_fn=print,
   )
   ```
6. **Confirm save + show the result** to the user. Cost estimate: ~€0.10–0.20.

## Hungarian content guidelines

When generating Hungarian text inside images, apply these rules:

- **Register:** Ön for B2B enterprise (formal), te for SME/consumer (informal)
- **Native terms:** megtérülés (ROI), versenyelőny (competitive advantage), adatvezérelt (data-driven), bevételnövekedés (revenue increase), costs: költségcsökkentés
- **Compound words:** single word, no hyphen, no space: termelékenységnövekedés, hatékonyságnövelés; hyphen before suffix on abbreviation: AI-képzés, MI-korszak
- **Quotes:** „lower-upper" or »guillemet« — never ASCII straight quotes
- **Comma before hogy:** ALWAYS — non-negotiable
- **Date format:** 2026. április 18. (note: month in lowercase)
- **Name order:** family name first (Hungarian convention)
- **Decimal separator:** comma (4,44 not 4.44); thousand separator: space (1 200 000)

## Avoid these known kie.ai failure modes

| Failure | Symptom | Fix |
|---|---|---|
| 1:1 + 4K combo | API rejects with "aspect_ratio cannot be 4K" | Use 1:1 + 2K, or 16:9 + 4K |
| Dense multi-cell flat-lays (5+ items) | 7-min timeout | Cap at 3-4 items |
| Trademarked names ("Pokémon-style", "Dunder Mifflin") | Safety filter rejects | Use generic ("collectible card", "fictional company") |
| Cinematic-violence keywords (chains, "Denis Villeneuve film still") | Safety filter rejects | Soften: "wrist wraps" + "amber light" + drop named-director references |
| Long Hungarian paragraphs (>15 words in image) | Truncation | Split into shorter labels or quote VERBATIM |
| GTA / Vice City / specific game IP | Safety filter rejects + C&D risk if posted | Use the underlying aesthetic (synthwave, neon Miami, 80s Florida) — never name the IP |

## Brand kit reference (quick)

When the user mentions:
- **Your own brand** → copy `brand_kits/acme-consulting.json`, rename it, fill in your palette/typography/voice

If the user doesn't specify a brand and the project context isn't clear, ask before assuming. Alternatively, use `acme-consulting` as a neutral dark-ink palette for any dark-background digital asset.

## Cost + latency

- Cost per image: ~€0.10–0.20 on kie.ai (depends on aspect/resolution)
- Latency: ~80–120s per image, ~7-min hard timeout server-side
- Image-to-image: same cost, slightly slower (~100–140s)

## Iteration

If the first generation isn't right:
- **Compositional issue (layout wrong, missing elements)** → re-prompt with more explicit positioning. Same technique.
- **Brand drift (wrong palette, wrong logo)** → switch to img2img mode and pass the brand-kit reference images as `input_urls` (foundational technique a3-t10 / a1-t3).
- **Style register wrong** → propose a different technique. Don't over-iterate on a wrong base.
- **Failed safety filter** → soften the prompt (see avoid table above), don't bypass.

## When this skill is the wrong choice

- The user wants a **video** → this skill only does single images. Video generation is a separate workflow (Kling/Runway/Veo via kie.ai's other endpoints) — explain and offer to set up the handoff.
- The user wants **vector / SVG editable output** → GPT-Image-2 produces raster only. Suggest exporting to Canva/Figma after generation, or tracing in Illustrator.
- The user wants **a logo from a description** with no constraints → this skill works best for branded assets in established kits. For pure logo design, suggest manual designer brief instead.
- The user wants to **edit a real photo of a person** with face-swap or identity-spoofing intent → refuse politely, point to safer alternatives.
