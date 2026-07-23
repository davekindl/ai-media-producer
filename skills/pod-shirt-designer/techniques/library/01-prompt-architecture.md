# Prompt Architecture -- POD Shirt Designer

5 core prompt construction patterns. Use these as foundations, then layer style modifiers from 02-design-styles.md.

---

## P1: The 4-Part Skeleton (Universal Foundation)

**What:** The minimum viable prompt structure that prevents "pretty but unprintable" output.

**Structure:** `[Style] + [Subject] + [Composition] + [Output Spec]`

**Template:**
```
[STYLE: flat vector illustration / vintage badge / screen print / manga-style / minimalist line art]
of [SUBJECT: what the design depicts],
[COMPOSITION: centered / badge layout / arched text / left-chest / full-front],
[OUTPUT: no background, transparent, isolated design element, clean edges, no shadows, bold outlines, t-shirt design, print-ready]
```

**Example:**
```
Flat vector illustration of a grizzly bear wearing a crown, minimalist style,
bold outlines, 3-color palette (black, gold, white), centered composition,
no background, transparent, isolated design element, clean edges, no shadows, t-shirt design
```

**Gotchas:**
- Omitting "no background, transparent, isolated design element" is the #1 beginner mistake
- Omitting "t-shirt design" causes the model to optimize for screen, not fabric
- Always end with the output spec block

**Sources:** The Loyal Brand, Inksie, Media.io

---

## P2: The 7-Part Formula (GPT-Image-2 Optimized)

**What:** Structured format that maximizes GPT-Image-2's instruction-following capability.

**Structure:**
```
1. Scene/Context: [what world this exists in]
2. Subject: [focal point]
3. Specific Details: [colors, textures, elements]
4. Artifact Type: [t-shirt design / badge / emblem / patch / sticker]
5. Style Reference: [in the style of vintage Americana / Japanese woodblock / etc.]
6. Technical Constraints: [3-color palette / thick outlines / no gradients]
7. Output Spec: [on solid white background / high contrast / print-ready / 3:4 aspect]
```

**Example:**
```
A retro-futuristic space exploration badge.
Central element: a rocket ship breaking through a planetary ring.
Colors: navy, gold, and cream only. Halftone dot texture on the background fill.
This is a t-shirt design, badge/emblem format.
In the style of 1960s NASA mission patches.
Thick outlines, no gradients, no photorealism, limited to 3 colors.
Isolated on solid white background, high contrast, clean edges, print-ready.
```

**Gotchas:** Use linebreaks between sections. Describe the artifact, not the fantasy.

**Sources:** fal.ai GPT-Image-2 Guide, Atlabs.ai

---

## P3: Style Anchoring (Reference-Based)

**What:** Triggers world knowledge by naming specific real-world style references instead of vague adjectives.

**Effective anchors:**
| Anchor Phrase | What It Produces |
|---|---|
| "Kodak Portra color palette" | Warm, slightly faded film tones |
| "1970s Manhattan street photography" | Gritty, high-contrast urban |
| "Ed Hardy tattoo flash art" | Bold outlines, saturated, tattoo-parlor aesthetic |
| "Shepard Fairey screen print poster" | High-contrast, limited-palette, political poster |
| "Japanese ukiyo-e woodblock print" | Traditional Japanese art, flat color blocks |
| "90s Nickelodeon cartoon" | Bold, playful, chunky outlines |
| "Art Deco travel poster" | Geometric, elegant, gold/navy/cream |
| "National Park Service poster" | Vintage illustration, serif typography, muted earth tones |
| "Soviet constructivist propaganda" | Bold red/black, geometric, dramatic angles |
| "Vintage boxing poster" | Distressed typography, fight-card layout |

**Template:**
```
T-shirt design in the aesthetic of [ANCHOR PHRASE].
[SUBJECT DESCRIPTION].
[COLOR/TECHNICAL CONSTRAINTS].
Isolated on solid white background, clean edges, print-ready.
```

**Gotchas:** Avoid naming living artists or specific recent IP. Use era/movement/technique references. "In the aesthetic of vintage National Park posters" is safe; "in the style of [specific living artist]" is legally risky.

**Sources:** fal.ai, Morphic

---

## P4: The Typography-First Template (Top-Selling Format)

**What:** The #1 performing POD category. Combines bold text with a small illustration element.

**Template:**
```
Vintage badge t-shirt design with arched text reading "[PRIMARY TEXT]"
[above/below] a [ILLUSTRATION ELEMENT],
[optional: small subtitle text reading "[SECONDARY TEXT]"],
distressed texture, [N]-color palette ([COLOR 1], [COLOR 2], [COLOR 3]),
[FONT STYLE: bold sans-serif / military stencil / retro script / chunky block],
centered composition, no background, transparent, isolated design element,
clean edges, print-ready, high contrast
```

**Example:**
```
Vintage badge t-shirt design with arched text reading "ADVENTURE AWAITS"
above a mountain range silhouette with small pine trees,
distressed texture, 2-color palette (cream and forest green),
bold sans-serif font, centered composition,
no background, transparent, isolated design element, clean edges, print-ready
```

**The 3-Foot Rule:** Text must be 1"+ tall at print size. If you can't read it from 3 feet away, it won't sell. Keep primary text to 1-5 words max.

**Sources:** Printful Best Selling Designs 2026, Vexels Trends

---

## P5: The Vector Artist Directive (Print-Safety Override)

**What:** Append to ANY prompt to force print-friendly output instead of photorealistic renders.

**The directive:**
```
vector graphic style, flat colors, thick outlines, no photorealism,
no shading, no shadows, no complex background, no watermark,
no text artifacts, no frame, no border, screen print aesthetic
```

**When to use:** Always — unless you specifically want photorealistic output (rare for shirts).

**Why:** "Photorealistic" and "intricate detail" bias toward output that looks great on screen and falls apart on cotton. Vector-style output survives 300 DPI scaling, color conversion, and fabric texture.

**Gotchas:** Some models interpret "vector" literally and produce SVG-like artifacts. Add "illustration" or "graphic design" to keep it in raster-with-vector-aesthetics territory.

**Sources:** OpenArt, Aiarty

---

## Universal Prompt Modifiers (Quick Reference)

Append these to any base prompt:

**Print-safety:** `"no background, isolated design element"`, `"bold outlines"`, `"limited color palette"`, `"high contrast"`, `"print-ready"`, `"t-shirt graphic"`

**Style:** `"screen print aesthetic"`, `"vintage badge"`, `"halftone texture"`, `"distressed worn ink"`, `"sticker style with die-cut border"`

**Quality:** `"clean edges"`, `"no artifacts"`, `"sharp silhouette"`, `"professional graphic design"`

**Negatives:** `"no photorealism"`, `"no shadows"`, `"no gradients"`, `"no watermark"`, `"no frame"`, `"no border"`, `"no busy background"`

**Aspect:** `3:4` for standard front-of-shirt, `1:1` for chest/pocket designs
