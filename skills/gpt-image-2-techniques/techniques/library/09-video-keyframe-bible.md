# Image Generation for Video Pipelines (keyframe assets)

1 techniques. Each entry includes prompt template, source, gotchas, stack notes, and (when relevant) cross-references.

Use the skill's discovery step to pick the right one for a given request.

---

## A9-W3 — Character Bible Bootstrap (3-View + Outfit Sheet)

**Score:** ★★★★★ (5/5)  
**Source:** [Scenario character turnarounds + thinking](https://www.scenario.com/blog/generate-character-turnarounds-scenario)  
**Use case:** PRE-PRODUCTION FOUNDATION. Do once at project start. Generate one character reference sheet image + one outfit/prop sheet, host on Cloudinary/S3. URLs pasted into EVERY downstream img2img call.

**Prompt template:**

```
CHARACTER SHEET PROMPT:
Create a professional character reference sheet on a clean light-grey background.
Layout: top row = three-view turnaround (front, 3/4 side, back), full body, neutral pose, arms slightly out. Middle row = six facial expression close-ups (neutral, determined, angry, surprised, exhausted, triumphant). Bottom row = detail callouts (hands/knuckles close-up, shoes close-up, signature jewelry/tattoo close-up) + a 6-swatch color palette row with hex codes.
Character: [40-60 word description: "a 34-year-old Hungarian male powerlifter, 185cm, 95kg, shaved head with week-old stubble, full sleeve blackwork tattoos both arms, wearing a faded black training-brand tank top and grey sweatpants, worn Adidas Adipower lifters"].
Professional concept art style, clean line work, consistent lighting across all views, high resolution. Brief character name label in top-left corner. No background clutter. aspect_ratio: 16:9, resolution: 4K.

OUTFIT/PROP SHEET PROMPT:
Create a wardrobe and equipment reference sheet on a clean white background.
Flat-lay photography style. Items arranged in grid with labels:
Row 1: training-brand tank top (front + back), grey sweatpants, compression shorts.
Row 2: Adidas Adipower weightlifting shoes, knee sleeves, lifting belt (thick leather).
Row 3: wrist wraps, chalk bag, water bottle, gym bag.
Professional product photography, even softbox lighting, hard shadows on surface, 4K, 16:9, no people visible.
```

**Gotchas:** Both URLs pasted into EVERY img2img call downstream. Skipping costs more later in drift-rework.

**Stack with:** FOUNDATIONAL — one-time sunk cost ~$0.30 per project.

---
