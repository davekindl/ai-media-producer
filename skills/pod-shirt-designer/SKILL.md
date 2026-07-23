---
name: pod-shirt-designer
disable-model-invocation: true
description: "Generate print-ready POD (Print on Demand) t-shirt designs via kie.ai GPT-Image-2 using a curated catalog of prompt templates across 8 trending niches, 10 untapped prospects, and 15+ design styles. Includes full pipeline: prompt construction, kie.ai generation (native transparent background), upscale to 4500x5400px at 300 DPI, and POD platform export. Generation spends ~$0.12-0.25 of kie.ai credits per design, so this skill is invoked explicitly (not auto-triggered). Trigger when the user says: 'design a shirt', 'POD design', 'print on demand', 't-shirt design', 'merch design', 'shirt prompt', 'make a shirt graphic', 'gym shirt', 'anime shirt', 'tech shirt', 'funny shirt design', 'create merch', 'design for Redbubble', 'Merch by Amazon design', 'shirt niche', 'POD niche research', 'trending shirt ideas', 'what sells on shirts'. Also triggers for specific niches: anime streetwear, gym pump cover, fitness motivation, AI disruption, tech culture, vintage retro, fictional brand, profession humor, Magyar Peter, untapped merch."
---

# POD SHIRT DESIGNER -- Print-Ready AI Shirt Design Engine

> "Research-backed prompts. Print-proven pipeline. From niche idea to uploaded listing in 10 minutes."

## Shared Infrastructure
- **API client:** `pod_pipeline.py` (included in this skill folder)
- **Sibling skill:** gpt-image-2-techniques (for non-POD image generation)

Built on 50+ sources across POD platforms, Reddit communities, YouTube tutorials, and market research. Every prompt template is designed for GPT-Image-2 via kie.ai with the transparent-background pipeline baked in.

## Architecture

```
pod-shirt-designer/
+-- SKILL.md                              (this file -- operating instructions)
+-- pod_pipeline.py                       (kie.ai generate + bg removal + export)
+-- techniques/
|   +-- _index.md                         (one-liner per technique -- discovery scan target)
|   +-- library/
|       +-- 01-prompt-architecture.md     (5 prompt construction patterns)
|       +-- 02-design-styles.md           (10 style categories with templates)
|       +-- 03-trending-niches.md         (top 5 niches + anime/gym/AI deep dives)
|       +-- 04-untapped-niches.md         (10 novel prospects not yet on shirts)
|       +-- 05-technical-pipeline.md      (resolution, color, format, workflow)
+-- research-dossier.md                   (all sources, organized by type)
+-- test-prompts.md                       (validation prompts for Phase 1 testing)
+-- evolver-config.md                     (hardening loop config)
+-- CHANGELOG.md                          (version tracking)
```

## Discovery Workflow

**Every request runs through these 4 steps.**

### Step 1 -- Parse the request

Identify:
1. **Design type:** quote/typography, illustration, character, badge/emblem, pattern, mashup
2. **Niche:** anime, gym/fitness, AI/tech, vintage/retro, profession, pet, fictional brand, untapped prospect, or custom
3. **Audience:** who wears this shirt? (age range, gender lean, tribe identity)
4. **Tone:** aggressive, humorous, minimal, premium, streetwear, wholesome, ironic
5. **Color constraint:** dark shirt (light design) or light shirt (dark design) or both
6. **Text:** any specific text/quote to include
7. **Language:** EN, HU, bilingual, other

### Step 2 -- Scan index, propose top 3

1. Read `techniques/_index.md`
2. Match techniques against request dimensions
3. Propose 3 best-matching prompt templates with rationale
4. For each: preview the prompt structure and what variables are needed

### Step 3 -- Present and confirm

```
Based on "[request]", here are 3 approaches:

1. **[ID] [name]** -- [rationale, what variables needed]
   _Best for:_ [when this wins]
   _Trade-off:_ [what you give up]

2. **[ID] [name]** -- [rationale]
   _Best for:_
   _Trade-off:_

3. **[ID] [name]** -- [rationale, often the wildcard]
   _Best for:_
   _Trade-off:_

Pick one, or describe what's missing.
```

### Step 4 -- Generate

1. Read the full technique from `techniques/library/*.md`
2. Assemble the final prompt (substitute variables, apply style modifiers)
3. Run the pipeline: generate -> remove background -> quality check -> export
4. Present result with cost breakdown

## The Pipeline (Step 4 Detail)

```
1. GENERATE via kie.ai (with native transparency)
   Model: gpt-image-2-text-to-image
   Aspect: 3:4 (closest to 12x16 print area)
   Resolution: 4K
   Background: transparent  <-- HARDCODED, never omit
   Prompt: [assembled from technique template]
   Add to ALL prompts: "isolated design element, no background,
                        clean edges, bold outlines, print-ready t-shirt graphic"

   API body MUST include:
   {
     "model": "gpt-image-2-text-to-image",
     "input": {
       "prompt": "...",
       "aspect_ratio": "3:4",
       "resolution": "4K",
       "background": "transparent"
     }
   }

   Output: true RGBA PNG with alpha channel. No post-processing needed.
   Output: save to ./out/ directory

2. QUALITY CHECK (before export)
   - Text: correct spelling, no extra/missing letters
   - Edges: clean, no white halo or fringing
   - Symmetry: logos/emblems balanced
   - Detail: no micro-text noise or AI artifacts
   - 3-Foot Rule: readable from arm's length at print size

4. UPSCALE if below 4500x5400px
   Target: 4500 x 5400 px at 300 DPI (universal POD standard)
   Color profile: sRGB IEC61966-2.1
   Format: PNG-24 with alpha transparency

5. EXPORT + MOCKUP
   Save to ./out/[design-name].png
   Cost: ~$0.12-0.25 per print-ready design (generation only -- native transparency, no bg removal)
```

## Bulk Runs (Batch Submit, Then Poll)

When generating more than ~3 designs in one run, do NOT submit-then-block on each
design serially. kie.ai generation is async (createTask returns a `taskId`; results
come from polling `recordInfo`). For a batch:

1. **Submit all tasks first** (`pipe.generate(prompt, ...)` per design) and collect every `taskId`.
2. **Then poll** each `taskId` to completion (`pipe.poll(task_id)`) and download.

This overlaps generation wall-time across the batch (each design takes ~80-120s) instead
of paying it back-to-back. Budget the spend up front: ~$0.12-0.25 x N designs (this skill
is `disable-model-invocation: true` precisely because each run spends real kie.ai credits).

## Critical Technical Rules

| Rule | Why |
|------|-----|
| Always pass `"background": "transparent"` in API input | Native RGBA alpha -- no post-processing needed |
| Never prompt "on white background" | White fill becomes part of the design and can't be cleanly removed |
| Use 3:4 aspect ratio for standard shirt designs | Closest to 12x16" print area |
| 1:1 aspect ratio CANNOT go to 4K on kie.ai | Use 2K for square, or switch to 3:4 |
| Design in sRGB, export as PNG-24 | POD platforms expect sRGB, convert to CMYK internally |
| Neon colors will be duller in print | Oversaturate by ~10-15% or stick to earth tones |
| Text must be 1"+ tall at print size | The 3-foot rule -- if you can't read it from 3 feet, it won't sell |
| Never use copyrighted character/artist names in prompts | DMCA takedowns kill seller accounts |
| Always reverse-image-search output before listing | AI can accidentally reproduce existing designs |

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Prompt "photorealistic", "8K render", "cinematic" | Looks great on screen, fails on fabric | Use "illustration", "flat color", "screen print style" |
| Use thin line art (<2pt at print size) | Disappears on textured fabric | Bold outlines, 3pt+ at print size |
| Cram 7+ elements into one design | Becomes visual noise at arm's length | 3-5 elements max, one clear focal point |
| Use smooth gradients | Band/step on DTG printers | Flat colors, halftone dots, or hard color transitions |
| Prompt "on white background" then try to remove it | White fill bakes into internal design areas, rembg can't separate | Use `"background": "transparent"` API parameter for native alpha |
| Name specific anime characters | Instant DMCA takedown risk | Create original characters in anime STYLE |
| Skip the 100% zoom artifact check | Text errors, edge halos, symmetry breaks | Run the full checklist before export |

## When NOT to Use

- Want a **photo-quality image** (not for print) -- use gpt-image-2-techniques directly
- Want a **logo** (vector/SVG needed) -- this produces raster only
- Want to **edit an existing design** -- use gpt-image-2 img2img mode
- Want **video content** -- use Seedance/Veo workflow
- Need **brand-locked assets** for a specific brand -- use gpt-image-2-techniques with brand kits

## Hungarian Content

For HU-market shirts (Magyar Peter quotes, Hungarian humor, etc.):
1. Review Hungarian language rules before generating (diacritics, compound words, punctuation)
2. GPT-Image-2 renders Hungarian diacritics (ő, ö, ű, ü, á, é) at 95%+ accuracy
3. Keep text SHORT (1-5 words) for reliable rendering
4. Verify every character at 100% zoom -- diacritics are the failure point

## Cost Model

| Operation | Cost |
|-----------|------|
| GPT-Image-2 generation (4K, kie.ai, transparent) | ~$0.12-0.20 |
| Background removal | $0 (native transparency) |
| Upscale (if needed) | ~$0.01-0.05 |
| **Total per print-ready design** | **~$0.12-0.25** |
| POD platform listing | Free (Printify/Printful/Amazon) |
| Shirt production (on sale) | $5-15 per unit |
| Typical selling price | $22-40 |
| **Profit margin target** | **40%+** |

## Reference Files

| File | Read When |
|------|-----------|
| `techniques/_index.md` | Every request -- discovery scan |
| `techniques/library/01-prompt-architecture.md` | Building any prompt |
| `techniques/library/02-design-styles.md` | Choosing a visual style |
| `techniques/library/03-trending-niches.md` | Designing for proven markets |
| `techniques/library/04-untapped-niches.md` | Exploring novel opportunities |
| `techniques/library/05-technical-pipeline.md` | Resolution, export, platform specs |
