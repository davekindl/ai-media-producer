# Multi-Tool Stacking Workflows

7 techniques. Each entry includes prompt template, source, gotchas, stack notes, and (when relevant) cross-references.

Use the skill's discovery step to pick the right one for a given request.

---

## A5-T10 — ChatGPT Multi-Turn Iterative Refinement (Self-Stacking)

**Score:** ★★★★★ (5/5)  
**Source:** OpenAI default + fal.ai prompting guide  
**Use case:** ChatGPT Images 2.0 preserves context across turns — each refinement is a STACKED operation, not a restart. O-series reasoning plans composition before generating + verifies text.

**Prompt template:**

```
Turn 1:
"Create a startup hero banner for '[Your Brand]' — an AI consultancy. Dark premium aesthetic, navy + teal palette, abstract geometric logo left, headline 'Ship AI That Actually Works' right, 16:9, 4K."

Turn 2 (refine without losing state):
"Change: replace headline with 'AI That Earns Its Keep'. Preserve: all composition, logo, color palette, lighting. Add: subtle grid texture in background."

Turn 3:
"Change: add small CTA button bottom-right reading 'Start Your Pilot'. Preserve: everything else exactly."
```

**Gotchas:** Use pure multi-turn for single deliverable with iterative tweaks. Break out to multi-tool only for motion, audio, non-image artifacts.

**Stack with:** $0.10-$0.30 per session (3-5 turns). 5-10 min.

---

## A5-T11 — Kie.ai Unified Stack (Claude Code orchestrating GPT-Image-2 + Kling + Seedance + Suno)

**Score:** ★★★★★ (5/5)  
**Source:** [Heather Cooper Substack](https://heatherbcooper.substack.com/p/how-i-built-a-claude-ai-workflow)  
**Use case:** kie.ai exposes 66+ models behind one auth header + one submit/poll/download pattern. Claude orchestrates whole pipeline as one bash-like script.

**Prompt template:**

```
Step 1 (Claude /prompt-gen):
"Raw idea: [user input]. Target tools: GPT-Image-2 (hero frame) → Kling 3.0 (5s hero loop) → Suno (15s audio sting). Output three tool-optimized prompts with exact aspect ratios and duration. Use kie.ai body schemas."

Step 2 (Claude /ai-generate executes):
POST https://api.kie.ai/api/v1/jobs/createTask
{ "model": "gpt-image-2-text-to-image", "input": {...} }
# poll, download hero.png
POST https://api.kie.ai/api/v1/jobs/createTask
{ "model": "kling-v3-image-to-video", "input": { "image_url": "hero.png", "prompt": "...", "duration": 5 } }
# poll, download hero.mp4
POST https://api.kie.ai/api/v1/jobs/createTask
{ "model": "suno-v4", "input": { "prompt": "...", "duration": 15 } }
```

**Gotchas:** Use whenever work is multi-tool AND repeatable. Skip for one-off exploration.

**Stack with:** ~$1.50 per full stack run. 3-5 min fully automated once skills written.

---

## A5-T12 — SYNTH: Tiered Model Stack (Grok → GPT-Image-2 → Nano Banana Pro)

**Score:** ★★★☆☆ (3/5) · `synth`  
**Source:** Synthesis from multi-source consensus  
**Use case:** Each image model has a tier. Grok iterates cheaply for ideation. GPT-Image-2 handles structure + text. Nano Banana adds 'warmth'. Never use one for all three jobs.

**Prompt template:**

```
Step 1 (Grok — ideation batch):
"20 variants: magazine-style hero of premium wristwatch on marble, different angles, props, lighting. Quick."

Step 2 (pick winner → GPT-Image-2 finalize):
"Using this composition as reference [Grok winner URL]: recreate with precise brand text 'CHRONOS' on watch face, 4K sharpness, preserve composition and lighting."

Step 3 (Nano Banana Pro warmth pass):
"Add subtle photorealistic warmth, golden-hour side light, realistic skin tone if hand in frame. Preserve all text and geometry."

DECISION MATRIX PER TIER:
- Speed + volume: Grok / nano-banana
- Structure + text: GPT-Image-2
- Photorealism polish: Nano Banana Pro
- Style exoticism: Midjourney v7
```

**Gotchas:** Pattern real, original Al Edge thread not verified (X 402). Labeled synthesized.

**Stack with:** ~$0.27 per final hero. 12-18 min.

---

## A5-T5 — GPT-Image-2 → Magnific → Topaz Gigapixel (Print-Grade Detail)

**Score:** ★★★★☆ (4/5)  
**Source:** [Chase Jarvis Magnific vs Topaz](https://chasejarvis.com/blog/topaz-vs-magnific-best-ai-image-scaler/)  
**Use case:** GPT-Image-2's native 4K is professional for 95% of cases. Stack Magnific + Topaz only for: very large print, skin-pore close-ups, restoration of stylized output.

**Prompt template:**

```
Step 1 (GPT-Image-2):
"Close-up portrait of a grey-bearded craftsman in a dusty workshop, Rembrandt lighting, leather apron with visible stitching, weathered hands holding a brass tool, soft key light from left, deep shadow right, photorealistic, 4K, 3:4."

Step 2 (Magnific, creativity ~2.5):
"High-frequency detail pass. Describe scene: craftsman portrait, Rembrandt lighting, leather apron, brass tool. Add: skin pores, beard texture, leather grain, brass patina, dust particles in light shaft. Preserve identity, lighting, composition."

Step 3 (Topaz Gigapixel, Recovery mode):
No prompt. Auto-detect subject, Recovery v2 model, target 6K × 8K. Final cleanup of Magnific artifacts.
```

**Gotchas:** Magnific adds INTERPRETIVE detail (Creativity > 2); Topaz preserves fidelity. Run Magnific first, Topaz last as safety net.

**Stack with:** ~$2.10. 8-12 min.

---

## A5-T6 — Claude → GPT-Image-2 → Claude Design (Programmatic Brand System)

**Score:** ★★★★★ (5/5)  
**Source:** [Linas Substack 7-stage workflow](https://linas.substack.com/p/chatgpt-images-2-claude-design-guide)  
**Use case:** Claude decomposes brand brief into structured prompts → GPT-Image-2 executes 8-variant batch via API n=8 → Claude Design generates production React. Replaces 2-4 hours Figma in <60 min for ~$1.30.

**Prompt template:**

```
Step 1 (Claude system):
"You are a brand-identity prompt architect for GPT-Image-2. Given this brief: [brand brief], output 8 asset prompts. Each follows: Subject + Style + Composition + Lighting + Text + Aspect + Use. Text in English quotes. Plain language, 3-5 core elements per prompt."

Step 2 (Claude output, batched to GPT-Image-2 with n=8):
Example #3 of 8: "Product hero shot for 'Lumen' skincare serum bottle, minimalist editorial style, centered composition on marble surface with soft shadow, morning window light, clean serif wordmark 'Lumen' on amber glass, 1:1, 4K, use for Instagram post."

Step 3 (Claude Design after choosing winner):
"Using attached brand assets [URLs to GPT-Image-2 outputs], generate complete React + Tailwind landing page with: hero matching asset 1, product grid matching asset 3-6, footer matching asset 8. Preserve exact color palette from images. Include responsive breakpoints."
```

**Gotchas:** Use for any brand identity project >$500 in value.

**Stack with:** ~$1.30 per full brand system. 30-60 min end-to-end.

---

## A5-T7 — GPT-Image-2 → Photoshop 2026 Generative Fill

**Score:** ★★★★☆ (4/5)  
**Source:** [Photoshop 2026 reference-image release](https://fstoppers.com/photoshop/photoshop-2026-introduces-generative-fill-reference-image-900162)  
**Use case:** PS 2026 added reference-image to Generative Fill with 'geometry-aware compositing matching scale, rotation, lighting, color, perspective.' First time AI products drop into real scenes without manual masking.

**Prompt template:**

```
Step 1 (GPT-Image-2):
"Product packshot of matte-black ceramic espresso cup with 'CRAFT' wordmark in gold foil, centered, plain white cyclorama, studio softbox 45° front-left, subtle contact shadow, 4K, 1:1, no props."

Step 2 (Photoshop 2026 Generative Fill):
Select background. Attach GPT-Image-2 output as Reference.
Prompt: "Wooden cafe counter with morning sunlight, coffee beans scattered, steam rising from cup, warm ambient bokeh in background. Match cup lighting and perspective exactly."

Step 3 (Harmonize Tool): one click. PS matches shadow direction, color temp, scale.
```

**Gotchas:** Use when product identity must be pixel-exact OR composites with real photography. GPT-Image-2 alone for pure imagination; PS stack for brand-fidelity critical.

**Stack with:** ~$0.10 marginal. 8-15 min per composite.

---

## A5-T8 — GPT-Image-2 → Midjourney v7 --sref (Style Match Retexture)

**Score:** ★★★★☆ (4/5)  
**Source:** [Geeky Curiosity 6-ways post](https://geekycuriosity.substack.com/p/6-ways-i-use-chatgpt-images-with)  
**Use case:** GPT-Image-2 nails STRUCTURE; MJ v7 nails ARTISTIC STYLE. --sref to inherit MJ style while keeping GPT-Image-2 structure as ref.

**Prompt template:**

```
Step 1 (GPT-Image-2):
"Magazine cover layout, bold sans-serif masthead 'AURA' top center, small tagline 'The Future Issue', hero portrait of figure wearing reflective metallic garment, geometric background, precise typography, 4K, 2:3."

Step 2 (Midjourney v7 with --sref):
"[GPT-Image-2 output URL as ref] magazine cover, metallic garment portrait, AURA masthead, The Future Issue tagline --sref [Midjourney style ref URL — e.g. a Dazed editorial] --ar 2:3 --v 7 --stylize 500"
```

**Gotchas:** When client wants specific publication's feel (Dazed, 032c, i-D, Apartamento) that MJ nails but GPT can't.

**Stack with:** ~$0.10 + MJ sub. 10-20 min.

---
