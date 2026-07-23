# Music Brand / Album-Art Ecosystem

10 techniques for building a consistent visual identity for a music brand — album covers, lyric-video backgrounds, and social cards. Each entry includes prompt template, source, gotchas, stack notes, and (when relevant) cross-references.

Use the skill's discovery step to pick the right one for a given request. The walkthrough uses a fictional dark-industrial training-music brand as the running example; swap in your own brand kit, character anchor, and titles.

---

## A8A-T1 — Anchor-Character Mascot Lock via 16-Ref Image-to-Image

**Score:** ★★★★★ (5/5)  
**Source:** GPT-Image-2 Edit + character-DNA cadence  
**Use case:** Generate 4-image character sheet ONCE (front/3-4/back/forearm-detail), pass those 4 URLs on every subsequent cover + lyric-video call. Solves #1 AI-music-artist problem: mascot drift across releases.

**Prompt template:**

```
ANCHOR ESTABLISHMENT:
Create a professional character reference sheet for the brand mascot, a mythic training figure. Grid layout, 2x2: (1) full-body front view, hooded dark figure, chains wrapped around forearm, barefoot on wet concrete, furnace-red back-light silhouette. (2) three-quarter side profile, same lighting. (3) back view, hood down, scarred back. (4) macro detail of the chained forearm, dust and sweat visible. Photorealistic. Consistent shadow density and colour temperature across all four panels. Dark teal ambient, red rim light from behind. No text, no logos. 2K resolution, 1:1.

LOCK PROMPT (every subsequent cover):
Using the four reference images of the mascot (Images 1–4: character sheet) and Image 5 (mood reference: doom-cinematic stormy field), place the mascot in the environment from Image 5. Preserve face structure, hood shape, chain placement on forearm, and skin tone from the character sheet exactly. Change only the environment and lighting angle. 16:9, photorealistic, no text.
```

**Gotchas:** Without mascot lock, each release looks like a different artist. With it, the mascot becomes a recognisable brand even when BPM/genre flex.

**Stack with:** FOUNDATIONAL brand pattern. Patch into lyric-video-forge env var ARTIST_SHEET_URLS.

---

## A8A-T10 — Reasoning-Mode Role Briefing (Anti-Slop Bias)

**Score:** ★★★★☆ (4/5)  
**Source:** 8-element brief + GPT-Image-2 reasoning  
**Use case:** GPT-Image-2 'thinks through composition before generating'. Role briefing — telling the model WHO + WHAT purpose — biases EVERY downstream decision. Single biggest grammar shift from 4o-image to 2.0.

**Prompt template:**

```
ROLE-BRIEFING PREAMBLE (first 80 tokens):
You are producing a 2K album cover for an independent training-music artist. Brand positioning: mythic-cinematic, dark-industrial, anti-corporate-fitness, against the 'golden-hour-smiling-runner' aesthetic. Target audience: serious lifters who reject mainstream gym branding. This cover will appear on Spotify, Apple Music, YouTube thumbnails, and merch. It must feel like a still from a cinematic thriller, not a stock-photo motivational poster. [INSERT FULL SCENE/SUBJECT/LIGHT/CONSTRAINTS BLOCKS HERE]
```

**Gotchas:** Because 2.0 reasons about the whole brief, role context biases composition/colour/typography/implicit choices.

**Stack with:** Inject as first 80 tokens of every brand call. Layer with a8a-t4 + a8a-t8.

---

## A8A-T11 — Sequential-Edit Pass for Hero Moment Stills

**Score:** ★★★☆☆ (3/5)  
**Source:** Image-edit change/preserve + 'caps earned' rule  
**Use case:** For a 5-6 min build track — visual peak marking the 'scream moment' (~5:00 mark when lowercase→ALL CAPS). Image-edit on the main cover with explicit 'change only' — a second asset from one base.

**Prompt template:**

```
Reference image: main album cover of the track 'RISE UP'. Change only: (1) figure's face orientation — now looking directly up into the light source, jaw forward, mouth open as if mid-scream, tendons visible on neck. (2) Colour temperature of the god-rays — push the red saturation by 30%, the furnace-red rim light now covers 60% of the figure instead of 30%. (3) Dust intensity — double the volumetric particle density. Preserve: subject identity, body proportions, hood shape, chain position, floor reflection geometry, camera angle, framing, typography bar (but not the title text contents — remove title for this still). EXACT pose geometry otherwise, no drift. No text.
```

**Gotchas:** Same track, two assets from one base: quiet/intro cover (lowercase 0:00-5:00) + scream still (peak 5:00+). Matches the 'hold caps until the end' philosophy.

**Stack with:** --generate-peak-still flag in lyric-video-forge. ffmpeg dissolves to the scream still at the final minute.

---

## A8A-T2 — Non-English Text Rendering (Quote Rule + Spelling Guard)

**Score:** ★★★★★ (5/5)  
**Source:** GPT-Image-2 multilingual + accented-language titles  
**Use case:** GPT-Image-2's flagship upgrade. Accented characters (e.g. Hungarian ő/ű/á, German ö/ü/ß) render reliably first-try with the Quote Rule + letter-by-letter spelling guard. Eliminates the 'print title in Figma' workflow (~15 min saved/release).

**Prompt template:**

```
ACCENTED TITLE TEMPLATE:
Album cover, 1:1, 2K. Subject: lone hooded figure mid-deadlift, furnace red back-light, volumetric dust. Bottom third: bold condensed sans-serif title reading exactly "KELJ FEL" (spelled K-E-L-J F-E-L, no accents on these letters — verify). Below that, smaller subtitle reading exactly "RŐL" where the Ő character must include the double-acute accent (spelled R-Ő-L where Ő is capital O with double acute). EXACT TEXT. No extra words. No duplicated text. High contrast, cold white type on black bar.
```

**Gotchas:** STRIP all art-direction adjectives from the text subsection — keep it functional: exact string + placement + typography + accent verification. Mixing mood language causes diacritic drop.

**Stack with:** Use for any title with accented characters rendered directly inside the cover art.

---

## A8A-T3 — Oversized Canvas (21:9 / 4K) for Ken-Burns-Safe Backgrounds

**Score:** ★★★★★ (5/5)  
**Source:** Ken Burns + lyric-video-forge architecture  
**Use case:** Request a wider canvas (21:9) than the target (16:9) with the subject off-axis. The Ken Burns sweep REVEALS godrays + chain detail as it moves — the image becomes a tiny visual story matching the 'weight increases' philosophy.

**Prompt template:**

```
Wide cinematic composition, 21:9 ultra-widescreen, 4K. Mascot figure positioned on the golden-ratio right third, mid-frame vertically. Left two-thirds: vast empty industrial cathedral with volumetric god-rays slicing diagonally from upper-left to lower-right. Camera angle: low, looking slightly up. Deep chiaroscuro — near-black shadows, furnace-red rim light. Composition must remain readable when cropped centre to 16:9 (zoom out 30%) and when cropped full-right to 16:9 (zoom in 30%). No text.
```

**Gotchas:** 1:1 cannot do 4K. Ken Burns backgrounds must be 16:9 or 21:9 at 4K.

**Stack with:** Patch lyric-video-forge to request aspect_ratio: '21:9', resolution: '4K'.

---

## A8A-T4 — Chiaroscuro + Volumetric-Light Grammar Pack (House Style)

**Score:** ★★★★☆ (4/5)  
**Source:** Cinematic recipe + GPT-Image-2 reasoning  
**Use case:** GPT-Image-2 is a reasoning model — one PRECISE lighting sentence outperforms a bag of adjectives. The dark-industrial cinematic aesthetic is locked via 5 grammar-pack components.

**Prompt template:**

```
HOUSE STYLE PREAMBLE:
- Light quality: "volumetric god-rays from upper [left/right], visible dust particles, light beams through industrial fog"
- Contrast: "deep chiaroscuro — near-black shadows, luminous highlights, extreme contrast ratio like Caravaggio"
- Colour palette: "monochrome with single accent — near-black background, cold white mid-tones, single furnace-red rim light only on the subject's silhouette"
- Camera grammar: "low angle, 35mm feel, shallow depth of field, shot as if a still from a cinematic thriller"
- Texture layer: "wet concrete floor reflecting the rim light, skin with real pore detail, chain showing oxidation and grease"

FULL PROMPT:
Single album cover frame, 1:1, 2K. Mascot figure (ref images 1–4) silhouetted mid-squat rack pull, head down, shoulders loaded. Volumetric god-rays cutting diagonally upper-right to lower-left through industrial steam. Deep chiaroscuro — near-black background, single furnace-red rim light on the figure's right shoulder and forearm chain. Wet concrete floor reflecting the rim light into a subtle red glow pool at the figure's feet. Shot as if a still from a cinematic thriller, 35mm feel, low angle. Real skin-pore texture, oxidised chain detail. No text, no watermark.
```

**Gotchas:** Inject as a shared preamble in every brand call (covers, lyric backgrounds, IG squares).

**Stack with:** lyric-video-forge HOUSE_STYLE constant in the prompt assembler.

---

## A8A-T5 — Bilingual Cover-Edition Series (Preserve-Layout Edit)

**Score:** ★★★★☆ (4/5)  
**Source:** OpenAI Cookbook change/preserve + bilingual releases  
**Use case:** For EN/non-EN release pairs. Generate the English cover first, then image-edit with explicit change/preserve to swap the title only.

**Prompt template:**

```
EDIT CALL:
Reference image: English cover of the track 'RISE UP'. Change only the title text: replace 'RISE UP' with 'KELJ FEL' (spelled K-E-L-J F-E-L). Preserve the subject figure, pose, lighting direction, god-ray angles, colour palette, floor reflection, background geometry, typography style, type weight, letter spacing, and bar-position exactly. The new title must occupy the same bounding box and baseline as the original English title. No other changes. No extra text.
```

**Gotchas:** Separate change from preserve, and REPEAT the preserve list each iteration.

**Stack with:** One generation cycle for the English original, one-shot edit for the translated twin.

---

## A8A-T6 — Infographic-Poster Mode for IG Carousels (Lyric Quote-Cards)

**Score:** ★★★★☆ (4/5)  
**Source:** GPT-Image-2 multi-font dense-layout + IG carousel patterns  
**Use case:** 2.0 topped LM Arena at 1512 because of multi-font dense text. For a music artist = a high-conversion IG format previously Canva-only.

**Prompt template:**

```
Instagram carousel slide, 1080x1350 portrait, 4:5. Dark navy-to-black gradient background with subtle film grain. Centered composition: large condensed sans-serif quote reading exactly 'THE WEIGHT DON'T CARE IF YOU CRY OR BLEED' in cold white, hierarchical — 'THE WEIGHT DON'T CARE' slightly larger than 'IF YOU CRY OR BLEED'. Below the quote, small accent text reading exactly the artist + track name in furnace red. Top-right corner: tiny brand mark, white. Generous negative space. No watermarks, no extra text, no duplicate lines.
```

**Gotchas:** Slide 1 = hook + cover. Slides 2-8 = one lyric line per slide. Slides 9-10 = CTA + cover. Matches a call-and-response lyric structure.

**Stack with:** IG carousel completion 72%+ on 8-10 slide sequences.

---

## A8A-T8 — Negative-Constraint Stack to Kill AI Slop Tells

**Score:** ★★★★☆ (4/5)  
**Source:** GPT-Image-2 + anti-slop discipline  
**Use case:** The #1 reason AI covers look 'AI' isn't the subject — it's the giveaways. The last two negatives are CRITICAL — the gym/motivation default is the OPPOSITE of the dark-industrial aesthetic.

**Prompt template:**

```
APPEND TO EVERY BRAND PROMPT:
NO: watermarks, no platform logos, no extra text, no brand marks, no fake signage, no duplicate text, no corporate stock-photo composition, no centered symmetrical framing, no over-smoothed skin, no vaseline lens blur, no generic motivational-poster composition, no 'golden hour fitness Instagram' aesthetic.
```

**Gotchas:** The last two negatives ('motivational-poster' + 'golden hour fitness IG') are the biggest quality lift for gym-music — they exclude GPT-Image-2's default prior.

**Stack with:** lyric-video-forge NEGATIVES constant in the prompt assembler.

---

## A8A-T9 — Audiogram / Reel Background Loop-Prep Mode

**Score:** ★★★☆☆ (3/5)  
**Source:** Reel/Short audiogram + GPT-Image-2  
**Use case:** For 30-sec lyric snippet promos. The visual must be seamlessly loopable OR slow-motion enough that the cut is invisible. A purpose-built 'slow-motion-friendly' background.

**Prompt template:**

```
Vertical 9:16 cinematic background plate for a music video, 4K, 2160x3840. Distant mascot silhouette centred on the horizon line (bottom third), slowly approaching camera. Massive volumetric storm cell behind the figure — layered dust, ember particles, slow-drifting fog. Composition intentionally designed to tolerate a slow vertical pan with zero cuts: top half is storm/sky (zoom-in target), bottom half is figure/ground (zoom-out anchor). Monochrome with single accent — near-black + furnace red rim on figure only. No text, no watermarks. Subject should appear static but the atmosphere should read as continuously moving when Ken-Burns panned.
```

**Gotchas:** Top/bottom designed as zoom targets — the image loops 3x across a Reel without visible repetition.

**Stack with:** 30-second IG Reel snippet promos with lyric overlay.

---
