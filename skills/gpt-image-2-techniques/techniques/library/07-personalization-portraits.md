# Personalization & Generative Portraits

13 techniques. Each entry includes prompt template, source, gotchas, stack notes, and (when relevant) cross-references.

Use the skill's discovery step to pick the right one for a given request.

---

## A7-T1 — Self-Infographic Portrait (Aiker-style anime + life-stats wrap)

**Score:** ★★★★☆ (4/5)  
**Source:** Composite of caricature + Wrapped + maturity-mirror trends  
**Use case:** Anime-style hero portrait centered, legible infographic stat blocks wrapping. Rides 2.0's #1 breakthrough (multilingual pixel-perfect text) + ChatGPT memory. Most viral-shaped personal-brand output.

**Prompt template:**

```
Using everything you know about me from our past conversations and your memory, generate a 9:16 anime-style self-portrait of me as a hero-shot in the center, surrounded by legible, clean infographic panels wrapping around the figure. Include the following stat blocks: name, age, city, profession, daily routine, top 5 interests, current obsessions, 3 defining traits, and 'what I am building right now'. Use clean sans-serif typography, a palette that matches the vibe of my work, subtle grid, small icons next to each stat. Preserve a friendly, slightly stylized anime aesthetic. The stats must be accurate to what you know about me — do not invent facts. Text must be pixel-perfect.

DAVE/CONSULTING VARIANT:
Swap "anime" for "editorial infographic" and feed it the your consulting brand brand palette. Use as LinkedIn banner or speaker-bio card.
```

**Gotchas:** HIGH memory dependency — fails on thin-memory accounts.

**Stack with:** Speaker cards, consulting-intake gifts, LinkedIn hero. ChatGPT Plus memory required.

---

## A7-T10 — Occasion / Greeting Card Personalization

**Score:** ★★★☆☆ (3/5)  
**Source:** Composite — techrushi/toolpic/oimi  
**Use case:** Hand-lettered headline rendering finally works first attempt — previous models needed 3-5 regens for text.

**Prompt template:**

```
Create a 5:7 portrait-oriented birthday greeting card for my friend [Name]. Based on what you know about them from our previous conversations (or from the description I'll give you: [insert]), illustrate them as the hero in their favorite aesthetic [e.g. cottagecore / cyberpunk / minimal Scandi]. Wrap the illustration with a hand-lettered headline 'HAPPY BIRTHDAY [Name]' and three small icons of things they love. Keep the face recognizable from the reference image [upload]. Pixel-perfect text, warm palette.
```

**Gotchas:** MEDIUM memory dependency.

**Stack with:** Gumroad birthday-card-generator skill, your consulting brand client touchpoint automation.

---

## A7-T11 — Future-Self / Alternate-Timeline Visualization

**Score:** ★★★☆☆ (3/5)  
**Source:** Viral 2025-2026 (Medium/TikTok/PlainEnglish)  
**Use case:** Annual-planning ritual, consulting client vision-casting, speaker-talk opener.

**Prompt template:**

```
Simulate an alternate timeline where one decision I made differently changed my entire life. Describe who I become, my career, my relationships, and my biggest accomplishment.
(text generator — append "now draw it as a single cinematic image of that person's Thursday morning")

VARIANT:
Predict what my career will look like if I continue on my current path for the next 10 years. Then create a roadmap for a better version.
(append: "and generate an image of me on that 10-year trajectory's peak day")

VARIANT:
Describe one day in my life in 5 years, including details that I don't even think about now — new habits, the environment I live in, and new friends. Then generate a 16:9 cinematic image of one defining moment from that day.
```

**Gotchas:** HIGH memory dependency for grounded futures.

**Stack with:** Annual review, vision-casting workshops, speaker openers.

---

## A7-T12 — D&D / RPG Character Sheet From Résumé

**Score:** ★★★☆☆ (3/5)  
**Source:** Medium @sheerazullah + ifwego.co  
**Use case:** Résumé → D&D character: race, class, alignment, stats, ability. Then portrait + stats box visual.

**Prompt template:**

```
Imagine you are a Dungeon Master and prize-winning fantasy author. Based on my résumé below / your memory of me [paste or reference], design me as a D&D character: race, class, alignment, 3 stats (STR/INT/CHA 1–20), one unique ability. Then generate a 1:1 portrait-oriented character-sheet image with me at the center in full RPG illustration style, stats box on the right, class/race/alignment header at top, ability description bottom. Preserve facial likeness from the uploaded selfie. Pixel-perfect legible stat text.

ANCHOR WORKFLOW:
Generate a "character anchor" image first, then reference it in all future scene generations ("same face, same outfit, now in a forest") for narrative-consistent RPG portraits.
```

**Gotchas:** MEDIUM memory dependency.

**Stack with:** Team-offsite activity, workshop ice-breaker, gamer-client gift.

---

## A7-T13 — ChatGPT Wrapped Annual Image Card

**Score:** ★★★★☆ (4/5)  
**Source:** [Official OpenAI Wrapped Dec 2025 + TechRadar/Tom's Guide](https://www.techradar.com/ai-platforms-assistants/chatgpt/chatgpt-users-are-making-a-spotify-wrapped-for-their-year-in-ai-heres-how-to-do-it)  
**Use case:** This output class was the proof-of-concept OpenAI cited for 2.0 launch — stat-card image rendering at >95% text legibility. CRITICAL memory dependency.

**Prompt template:**

```
OFFICIAL VERBATIM:
Make me a ChatGPT Wrapped summary like a Spotify Wrapped showing my usage this year.

DEEP-ANALYSIS VARIANT:
Analyze my queries from this year and create a fun 'ChatGPT Wrapped' summary. Include categories like my top topics, most-used prompt style, funniest question, most chaotic question, most productive session, and any surprising habits you find.

IMAGE-CARD ADD-ON (verbatim reconstruction for GPT-Image-2):
Now render that Wrapped summary as a 9:16 shareable Spotify-Wrapped-style image card: vertical gradient background, my archetype name at top, 4 big stat cards (total messages, chattiest day, image count, em-dash count), my badge set along the bottom as small icons with labels, my 'vibe poem' inset on the right in small italic type. Pixel-perfect text throughout.
```

**Gotchas:** CRITICAL memory dependency — draws from actual ChatGPT usage data.

**Stack with:** Annual review artifact, your command center year-end asset, Gumroad white-label ('Your Year in [Role]').

---

## A7-T2 — ChatGPT Caricature Trend ('Me and My Job')

**Score:** ★★★★★ (5/5)  
**Source:** [Original viral Feb 2026 (CyberLink + Creative Bloq + TheTab)](https://www.cyberlink.com/blog/trending-topics/5207/chatgpt-caricature-trend)  
**Use case:** The original viral that briefly crashed OpenAI servers. 20 verified style-modifier variants (3D, 1920s vintage, surreal-fantasy, street-graffiti).

**Prompt template:**

```
PRIMARY VERBATIM:
Create a caricature of me and my job based on everything you know about me.

FALLBACK (thin memory):
Create a caricature of me and my job. I am a nurse in a hospital and mainly work with children.
Create a caricature of me and my job. I am an air hostess who wears a red uniform and flies to long-haul sunny destinations.

20 STYLE MODIFIERS (CyberLink set, each requires uploaded selfie):
"Exaggerate facial features for energetic excited expression, large sparkling eyes, wide smile, playful cartoonish style, keep identity recognizable, dynamic pose, bright vibrant colors"
"3D render caricature with exaggerated facial features, playful proportions, humorous cartoonish style, cinematic lighting, preserve identity, vibrant colors"
"Vintage 1920s comic-style caricature, exaggerated facial features, bold expressive lines, classic monochrome or sepia tone, humorous expression, preserve identity"
"Surreal fantasy-style caricature, exaggerated personality and profession, imaginative whimsical elements, cartoonish humor, preserve identity, rich vibrant colors, dynamic composition"
```

**Gotchas:** Best with memory enabled. Uploads one head-and-shoulders selfie + optional memory.

**Stack with:** Consulting-client persona cards, team offsite icebreakers, Gumroad seed product.

---

## A7-T3 — 'Draw My Life' / Current-State Visualization

**Score:** ★★★★☆ (4/5)  
**Source:** Tom's Guide + TikTok @adamstewartmarketing  
**Use case:** Memory-only. No selfie required. Often produces accurate environmental cues (desk, city skyline, pets, clothing colors) rather than face-accurate portraits.

**Prompt template:**

```
Based on what you know about me, draw a picture of what you think my current life looks like.

VARIANTS:
Based on everything you know about me, draw me an image of my future self in 5 years time.
What do you know about me that I might not know about myself based on our previous interactions.
(prose generator — append "...now draw it")
```

**Gotchas:** HIGH memory dependency. Output is interpretive — environmental, not photo-accurate.

**Stack with:** Morning-routine illustrations, 'about me' page, annual-planning artifacts.

---

## A7-T4 — Personality-Mirror (Reddit viral)

**Score:** ★★★★☆ (4/5)  
**Source:** [r/ChatGPT viral June 2025 (Fello AI)](https://felloai.com/2025/06/ask-chatgpt-to-visualize-your-personality-this-reddit-trend-turns-ai-into-a-mirror/)  
**Use case:** CRITICAL memory dependency — output entirely derived from chat-history tone analysis. Outputs metaphorical/symbolic.

**Prompt template:**

```
Make an image that reflects my maturity level based on our chats.

VARIANTS:
Create an image of how I treat you.
What you would like to do to me?
(WARNING: third variant trips alignment/bias issues)
```

**Gotchas:** Symbolic not literal. Some variants trip alignment systems.

**Stack with:** Team-building exercise, annual self-audit card, workshop opener.

---

## A7-T5 — Personal Stats Trading Card (Pokémon Holo-Foil)

**Score:** ★★★★☆ (4/5)  
**Source:** PromptBase + Threads @aitrend_1 viral April 2026  
**Use case:** GPT-Image-2 advantage: holo-foil + small legible 1999-style stat text + icon rendering = three things 1.5 reliably broke. 2.0 does all three in one pass.

**Prompt template:**

```
REFERENCE PROMPT:
Generate a Pokémon-style trading card of [insert character here]: vertical close-up held between thumb and finger, classic 1999 gold holo-foil frame; three-quarter portrait lit by a rim light that matches the character's signature colors, against a backdrop of subtle icons tied to their story; auto-assign HP, element icon, one concise red-label ability, and one attack (damage scaled to fit the HP).

SELF-VERSION (memory-aware):
Generate a Pokémon-style 1999 gold-holo-foil trading card of me, based on everything you know about me and the selfie I uploaded. Vertical card, three-quarter portrait lit by rim light matching my brand colors. Auto-assign HP based on my chaos level, an element icon for my dominant vibe, one concise red-label ability name (my strongest skill), and one attack (my go-to move at work). Add stat lines at the bottom: Speed, Charm, Focus, Creativity — on a 1–10 scale, calibrated to what you know about me. The name on the card is my actual name. 9:16 ratio, pixel-perfect text.
```

**Gotchas:** MEDIUM memory dependency — stats from memory or input.

**Stack with:** Welcome-kit gift per client, team offsite swag, Gumroad seed product.

---

## A7-T6 — LinkedIn Professional Headshot Suite (Ruben Hassid 8-prompt set)

**Score:** ★★★★★ (5/5)  
**Source:** [Ruben Hassid LinkedIn post 7371210822884335616](https://www.linkedin.com/posts/ruben-hassid_chatgpt-prompt-for-headshots-activity-7371210822884335616-hUVv)  
**Use case:** 249-comment viral. Selfie-driven (no memory). 8 verbatim prompts covering corporate, cinematic, B&W, candid, formal, gallery, automotive moods. 2.0's identity preservation lock makes this work where 1.5 failed ~30%.

**Prompt template:**

```
SETUP: Upload one clear selfie. Run each in sequence, save best.

1. Generate the corporate headshot of this person

2. Cinematic overhead shot of me standing still a brick city sidewalk, wearing a dark oversized blazer, motion-blurred crowd rushes past around me moody lighting 35mm film look. Shallow depth of field, sharp focus on me. Ration portrait 4:3

3. Generate a top-angle and close-up black and white portrait of my face, focused on the head facing forward. Use a 35mm lens look, 10.7K 4HD quality. Proud expression, water droplets on my face. Deep black shadow background – only the face is visible and appears ultra-sharp. 4:3 ratio, with a 1/5 processing depth effect.

4. Profile shot of me walking through a rushing metro station crowd. Everyone else is motion-blurred with trailing effects, while I remain in sharp focus with a serious expression, wearing a long trench coat. Cool blue tones dominate the scene, evoking a 35mm film aesthetic. Ambient lighting comes from train signs and station fixtures. Ratio: Portrait 4:3

5. Cinematic overhead shot of me standing hands in my pockets a brick city sidewalk, wearing a royal blue formal blazer. Motion blurred crowd rushes past around me. Moody lightning 35mm film look. Shallow depth of field, sharp focus on me. Ration portrait 4:3 no changing face

6. Create a high-end black and white portrait using my selfie. The face must remain exactly as in on my original selfie — no editing, no retouching, no smoothing. I'm wearing the business suits. Preserve every facial detail and texture for a raw, authentic look. The lighting should be dramatic and studio-quality, using strong contrast and shadows to sculpt the features. Use a clean, blurred studio-style background with soft gradients or subtle texture to enhance focus on the subject. Frame the portrait vertically (9:16 format), centered composition, with ultra-realistic skin texture and depth. No digital makeup or alterations. The final result should look timeless, editorial, and emotionally powerful — suitable for a gallery or fashion magazine.

7. Create a moody black-and-white night portrait of me sitting inside a modern black car with the door open. Fair skin, medium-length wavy hair, no glasses. Serious and intense expression. Black puffer jacket and light gray sweatpants. The city skyline with glowing lights is visible in the blurred background. Soft lighting from inside the car highlights face subtly. Cinematic, stylish, introspective.
```

**Gotchas:** NONE memory dependency. Prompt 6's 'preserve every facial detail and texture' lock is materially stronger on 2.0 vs 1.5.

**Stack with:** LinkedIn refresh, your consulting website hero, speaker-deck shot.

---

## A7-T7 — Family / Team / Group Portrait (multi-ref, 4-6 subjects)

**Score:** ★★★★☆ (4/5)  
**Source:** OpenAI Cookbook portrait-consistency  
**Use case:** GPT-Image-2 Edit handles 4-6 subject group shots preserving relative scale, eyeline, lighting. Critical: REPEAT preservation constraints on EVERY iteration.

**Prompt template:**

```
VERBATIM TECHNIQUE (OpenAI Cookbook):
Edit the image to dress the woman using the provided clothing images. Do not change her face, facial features, skin tone, body shape, pose, or identity in any way. Preserve her exact likeness, expression, hairstyle, and proportions.

GROUP PORTRAIT VARIANT (family use):
Using the provided reference images of 4 family members (image 1: dad, image 2: mom, image 3: son, image 4: daughter — do not alter faces), compose a single 4:3 editorial family portrait. All four standing in a light-filled living room, window behind, soft natural light. Preserve each person's exact facial likeness, skin tone, hairstyle, and approximate age. Allow clothing to be coordinated neutral tones (beige, cream, soft navy). Natural, slightly candid poses — no stiff formal line-up. Ultra-realistic, shot-on-Leica-Q3 quality, preserve eye contact direction as appearing in each reference image.
```

**Gotchas:** Reset preservation list each turn. Multi-turn drift accumulates without repetition. Identical-twin disambiguation underspecified.

**Stack with:** Family Christmas card, 'meet the team' consulting block, executive group portraits.

---

## A7-T8 — Anime-Mashup Vertical Selfie

**Score:** ★★★★☆ (4/5)  
**Source:** TikTok viral (50M+ views) + techrushi.com  
**Use case:** GPT-Image-2 advantage: anime-realism blend was 1.5's biggest quality drop zone. 2.0 holds consistent lighting between real-skin and cel-shaded sides.

**Prompt template:**

```
Ultra-realistic 9:16 vertical format fisheye selfie of me with [shinchan, Doraemon, Naruto, Nobita, Satoru Gojo, Sung Jin who, Ash from pokimon].

COUPLE VARIANT:
ultra realistic vertical format fisheyes selfie of me and my girlfriend with [Black Fragon]...anime characters integrated with stylized realism.
```

**Gotchas:** NONE memory dependency. Selfie required.

**Stack with:** Birthday cards, fitness-brand marketing (gym-bro selfie with anime bodybuilders).

---

## A7-T9 — Renaissance Oil-Painting Pet Portrait

**Score:** ★★★★☆ (4/5)  
**Source:** TechRadar Renaissance trend + PromptBase  
**Use case:** Pet → 16th-century European nobility portrait. Verbatim from ImagePromptly.

**Prompt template:**

```
BASE PROMPT:
Transform this portrait into Renaissance-style oil painting with classical composition and rich color palette. Visible brushstroke texture with chiaroscuro lighting technique, museum-quality artwork aesthetic.

PET-SPECIFIC FULL VERSION:
Transform my beloved pet into a noble figure straight out of 16th-century Europe. Majestic Renaissance-style oil painting with rich historical clothing (velvet robes, ruff collar, gold chain of office), regal three-quarter pose, candlelit chiaroscuro lighting, aged-canvas texture, museum-worthy detail. Pet's face must remain exactly as in the uploaded photo.
```

**Gotchas:** NONE memory; pet photo upload required.

**Stack with:** Pet Christmas cards, your consulting brand 'team pets' page, Gumroad gift product.

---
