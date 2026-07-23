# Reverse-Engineering & Style Transfer

14 techniques. Each entry includes prompt template, source, gotchas, stack notes, and (when relevant) cross-references.

Use the skill's discovery step to pick the right one for a given request.

---

## A6-T1 — Photo → Full Brand Guideline (THE @weplash hamburger pattern)

**Score:** ★★★★★ (5/5)  
**Source:** [Atlabs AI Ultimate Guide April 2026](https://www.atlabs.ai/blog/the-ultimate-gpt-image-2-prompting-guide-how-to-use-openai%E2%80%99s-best-image-model-2026)  
**Use case:** 1 reference photo in → complete brand-book sheet (logo, hex palette, typography, social post, packaging) out. THE prompt family behind 'photo → brand book in 40 seconds' viral demos.

**Prompt template:**

```
Using the attached photo as inspiration, generate a complete brand
guideline sheet for [BUSINESS TYPE]. Include: logo (primary + mono),
color palette with hex codes, typography pairing, a sample social
post, and a packaging mockup.

HAMBURGER VARIANT (customizable):
Using the attached hamburger photo as inspiration, generate a
complete brand guideline sheet for an artisan burger restaurant.
Include: logo (primary + monochrome), color palette with hex codes
derived from the photo, typography pairing (display + body), a
sample Instagram post, and a packaging mockup (wrapper + takeaway
box). Layout as a single landscape brand-guideline one-pager,
4K, crisp typography, editorial design-studio aesthetic.
```

**Gotchas:** @weplash exact verbatim not retrievable. High confidence the viral demo IS this template applied to a burger photo. Logo reproduction unreliable for proprietary marks.

**Stack with:** Multilingual text means hex codes + type specimens + logo wordmarks all readable inside sheet.

---

## A6-T10 — Accent Graphic Extraction (Transparent PNG)

**Score:** ★★★★☆ (4/5)  
**Source:** DesignHacker brand identity guide  
**Use case:** Background-removal + shape-preservation in one prompt → reusable brand asset. Equivalent to Remove.bg + style-transfer simultaneously.

**Prompt template:**

```
Extract this visual element and recreate it as a high-resolution
transparent PNG. Keep the shape and texture the same but remove
the background.
```

**Gotchas:** Logo extraction outputs raster, not vector.

**Stack with:** Asset library generation from one source.

---

## A6-T11 — Verbal Style-Transfer for Design Systems (Stripe-ify / Apple-ify / Linear-ify)

**Score:** ★★★★☆ (4/5)  
**Source:** [Anil-matcha Awesome-GPT-Image-2-API-Prompts](https://github.com/Anil-matcha/Awesome-GPT-Image-2-API-Prompts)  
**Use case:** No reference image — describe target brand verbally with concrete signature traits ('Stripe-purple-gradient + weight-300 elegance + generous whitespace + crisp sans-serif'). Avoids trademark-dodge refusals.

**Prompt template:**

```
Generate a complete UI design system for me in [style], including
web pages, mobile screens, cards, controls, buttons, and other
components.

GLASSY VARIANT:
Generate a glassy, translucent UI design system with frosted glass
effects, soft shadows, and modern aesthetics. Include web, mobile,
card, and button components.

DAVE'S NOVOLITH VARIANT:
Generate a complete UI design system in the your brand style:
dark-mode Linear-inspired base with ultra-minimal chrome, Stripe-
style purple gradients for accent CTAs, generous Vercel-style
whitespace, crisp sans-serif at weight 300/500/700. Include web
pages, mobile screens, cards, controls, buttons, and other
components.
```

**Gotchas:** Naming brands ('make it Ferrari-like') risks trademark-dodge refusals. Describe verbal style signatures instead.

**Stack with:** Use when you need 'feels like Stripe' without infringement risk.

---

## A6-T12 — Multi-Image Compositing (OpenAI canonical)

**Score:** ★★★★★ (5/5)  
**Source:** OpenAI Developer Cookbook §5.9  
**Use case:** Canonical OpenAI-endorsed phrasing. 'Place X from image N into Y from image M' with 'do not change anything else' as compositing terminator.

**Prompt template:**

```
Place the dog from the second image into the setting of image 1,
right next to the woman, use the same style of lighting, composition
and background. Do not change anything else.
```

**Gotchas:** 'Do not change anything else' is the load-bearing terminator.

**Stack with:** Base template for any reverse-engineering with two-image merge.

---

## A6-T2 — Multi-Reference Character Merge (3-16 refs)

**Score:** ★★★★★ (5/5) · `foundational`  
**Source:** Atlabs AI Ultimate Guide  
**Use case:** The pattern Midjourney can't do. Image 1 = face, Image 2 = outfit, Image 3 = pose, environment via text. Explicit role-assignment prevents cross-blending.

**Prompt template:**

```
Using the attached reference images, generate a new scene with the
exact same character (Image 1), wearing the outfit from Image 2,
posed as in Image 3, in [NEW ENVIRONMENT]. Preserve face, hair,
fabric texture, and brand logo placement exactly. Cinematic
lighting, 4K photoreal.
```

**Gotchas:** Explicit role-assignment is the win — 'face from Image 1 + outfit from Image 2'. Maps to GPT-Image-2's input-routing.

**Stack with:** FOUNDATIONAL for character consistency across brand campaigns + storyboards.

---

## A6-T3 — OpenAI Cookbook Style Transfer (canonical)

**Score:** ★★★★★ (5/5)  
**Source:** [OpenAI Developer Cookbook §5.1](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)  
**Use case:** OpenAI's officially-sanctioned style-transfer pattern. 'Use the same style' phrasing activates GPT-Image-2's style-encoder path.

**Prompt template:**

```
Use the same style from the input image and generate a man riding
a motorcycle on a white background.
```

**Gotchas:** Swap subject + background — pattern is universal.

**Stack with:** Foundational style-transfer.

---

## A6-T4 — Concrete-Visual-Language Style Transfer (fal.ai pro pattern)

**Score:** ★★★★★ (5/5)  
**Source:** [fal.ai prompting guide](https://fal.ai/learn/tools/prompting-gpt-image-2)  
**Use case:** 'Same style' is too abstract — GPT-Image-2 rewards concrete components. Name palette, edge treatment, silhouette language, era energy explicitly.

**Prompt template:**

```
Use the same visual language as the input image: chunky pixel forms,
limited arcade palette, bright glow accents, clean silhouette edges,
playful 1980s poster energy. Generate a new scene of a motorcycle
chase through a neon desert at night. White background. No watermark.

META-TEMPLATE for any style DNA extraction:
Use the same visual language as the input image: [PALETTE descriptor],
[EDGE/LINE treatment], [TEXTURE/RENDERING], [LIGHTING mood], [ERA/
CULTURAL energy]. Generate [NEW SUBJECT + SCENE]. [BACKGROUND
constraint]. [NEGATIVE: no watermark, no text, etc.].
```

**Gotchas:** Describe what you SEE, not what it EVOKES.

**Stack with:** Pro upgrade over a6-t3.

---

## A6-T5 — Wardrobe / Virtual Try-On Transfer

**Score:** ★★★★★ (5/5)  
**Source:** OpenAI Cookbook §5.2 + fal.ai multi-ref  
**Use case:** Identity is locked via negative-list. GPT-Image-2 preserves what you enumerate; drifts on what you leave unstated.

**Prompt template:**

```
Edit the image to dress the woman using the provided clothing images.
Do not change her face, facial features, skin tone, body shape, pose,
or identity in any way.

EXTENDED MULTI-REF VARIANT:
Image 1: base scene to preserve.
Image 2: jacket reference.
Image 3: boots reference.
Instruction: Dress the person from Image 1 using the jacket from
Image 2 and the boots from Image 3. Preserve face, body shape,
pose, background, lighting, and framing from Image 1. No extra
accessories.
```

**Gotchas:** Without explicit identity-lock list, model drifts on face/body/pose.

**Stack with:** E-commerce product-on-model, virtual try-on, fashion.

---

## A6-T6 — Product-on-Surface / Product-on-Model Placement

**Score:** ★★★★☆ (4/5)  
**Source:** [WaveSpeedAI Edit blog](https://wavespeed.ai/blog/posts/introducing-openai-gpt-image-2-edit-on-wavespeedai/)  
**Use case:** Short declarative product-on-surface or product-on-model commands. Lighting descriptor at end is the secret sauce for commercial-grade output.

**Prompt template:**

```
PRODUCT-ON-SURFACE (1 ref):
Place this sneaker on a marble countertop next to a coffee cup,
soft morning light.

PRODUCT-ON-MODEL (2 refs):
Show this dress on the woman in reference image 2, full-length
standing pose.
```

**Gotchas:** Lighting + setting specificity = commercial-grade. Generic = stock-photo.

**Stack with:** E-commerce, marketing collateral, product photography substitute.

---

## A6-T7 — Brand-Consistent Marketing Variants (Change/Preserve binary)

**Score:** ★★★★★ (5/5)  
**Source:** WaveSpeedAI Edit  
**Use case:** Explicit Change/Preserve binary prevents 'everything drifts' failure. Production-grade pattern for brand-consistent marketing variants.

**Prompt template:**

```
Change: [exactly what should change]
Preserve: [face, identity, pose, lighting, framing, background, geometry, text, layout]
Constraints: [any additional rules]

CONCRETE EXAMPLES:
"Change the model's outfit to winter clothing and add snow falling."
"Change the sky to sunset colors while keeping the building exactly the same."
```

**Gotchas:** State preservation list explicitly each iteration.

**Stack with:** Foundational for marketing variant runs.

---

## A6-T8 — Font Extraction from Reference Photo

**Score:** ★★★★☆ (4/5)  
**Source:** [DesignHacker brand identity guide](https://www.designhacker.com/blog/create-brand-identity-chatgpt)  
**Use case:** GPT-Image-2's OCR + visual-similarity identifies typefaces in photographs and returns closest Google Fonts equivalent as rendered specimens.

**Prompt template:**

```
Analyze this image and show me sample text using the closest
matching Google Fonts for both headers and body text. Use clean
formatting on light and dark backgrounds.
```

**Gotchas:** Returns closest match — not exact identification. Cross-check before committing.

**Stack with:** Pairs with a6-t1 brand-book extraction.

---

## A6-T9 — Background Recreation from Brand Mood

**Score:** ★★★★☆ (4/5)  
**Source:** DesignHacker brand identity guide  
**Use case:** After brand extraction (a6-t1), produce infinite on-brand backgrounds. 'Avoid text or logos' negative prevents brand-copy hallucination.

**Prompt template:**

```
Based on this image, generate a high-resolution 16:9 background
that matches the brand's tone and style. Use abstract texture or
atmospheric visual elements. Avoid text or logos.
```

**Gotchas:** Without 'avoid text or logos', model hallucinates brand copy onto background.

**Stack with:** Pair with a6-t1 for branded background series.

---

## A6-TA — Character Consistency Anchor (anchor-and-continue)

**Score:** ★★★★☆ (4/5)  
**Source:** OpenAI Cookbook §6.4  
**Use case:** Generate once, then use the generation as reference for all subsequent scenes. Restate preservation constraints on EVERY continuation — drift happens when constraints aren't repeated.

**Prompt template:**

```
STEP 1 ANCHOR PROMPT:
Create a children's book illustration introducing a main character.
A young, storybook-style hero inspired by a little forest outlaw,
wearing a simple green hooded tunic, soft brown boots, and a small
belt pouch.

STEP 2 CONTINUATION PROMPT (using anchor as reference):
Continue the children's book story using the same character...
Same green hooded tunic, same facial features, proportions, and
color palette. Do not redesign the character.
```

**Gotchas:** Restate constraints every continuation — drift accumulates without repetition.

**Stack with:** Brand-mascot campaigns + book illustrations + music-brand mascot consistency.

---

## A6-TB — Product Extraction for Mockups (cleanup step)

**Score:** ★★★★☆ (4/5)  
**Source:** OpenAI Cookbook §5.4  
**Use case:** Strip product from lifestyle shot, place cleanly on white. Then feed stripped version back as Image 1 for mockup variants.

**Prompt template:**

```
Extract the product from the input image and place it on a plain
white opaque background. Preserve product geometry and label
legibility exactly.
```

**Gotchas:** Preparation step for downstream mockup work.

**Stack with:** Pair with a6-t6 for mockup-ready outputs.

---
