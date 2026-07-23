---
name: lyric-forge
description: "Generate complete Suno-ready song scripts for gym/training music — bilingual (EN/HU), with style fields, structure tags, and production notes. Trigger when the user says 'write a song', 'new track', 'song idea', 'lyrics for', 'write me a gym song', 'suno script', or any variation of wanting to create song lyrics for gym/training music. Also trigger for 'magyar dal', 'dalszöveg', 'edzős szám'."
---

# LYRIC FORGE -- Gym-Music Song Generation Engine

> Concept -> Complete Suno-ready script. Bilingual. Battle-tested.

## Shared Infrastructure
- **Sibling skills:** video-prompt-builder (Seedance prompts), lyric-video-forge (lyric video pipeline)

## Prerequisites

Before writing ANY song, read these files:

| File | Purpose | Location |
|------|---------|----------|
| `songwriting-bible-template.md` | Complete methodology, style field rules, generation strategy, song catalog | `starter-pack/` |
| `sample-quotes-hooks.md` | 10 quotes/hooks organized by theme — raw material for lyrics | `starter-pack/` |
| `sample-song-concepts.md` | 5 starter concepts with genre, angle, and key hook | `starter-pack/` |

> **Note:** Start from the bundled `starter-pack/` — it ships inside this skill and works out of the box. As your catalog grows, point the skill at your own corpus folder instead: copy `songwriting-bible-template.md` there, fill in your song catalog and house rules, and grow your own quote/concept files (plus optional extras like a Hungarian prosody guide or a genre gap analysis). The bundled `scripts/count.py` (style-field gate) is the only script shipped with the skill itself.

## The Pipeline — 6 Steps

### Step 1: Concept Development

If the user provides a concept, skip to Step 2. If not, brainstorm by:

1. Check `starter-pack/sample-song-concepts.md` (or your own concepts file) for unused concepts
2. Check your gap-analysis file, if you keep one, for untapped genres/angles
3. Cross-reference with `starter-pack/sample-quotes-hooks.md` (or your own quote collection) for thematic inspiration
4. Propose 3 concepts with: title (EN + HU), genre, emotional angle, key hook
5. User picks one

**Anti-duplication check:** Review existing songs in the songwriting bible's section 2 (Song Catalog). Never duplicate a genre+angle combo the catalog already has.

### Step 2: Blueprint Selection

Every song starts with a musical blueprint — a reference track analyzed for structure. Options:

1. **User provides blueprint:** "Like Massive Attack's Teardrop but heavier"
2. **Genre implies blueprint:** Doom metal = Black Sabbath structure, Trip-hop = Massive Attack, Folk metal = Wind Rose
3. **No blueprint:** Analyze the concept's emotional arc and select the closest structural match from the existing catalog in the songwriting bible

Map the blueprint to: tempo, time signature, section order, dynamic arc, vocal delivery style.

### Step 3: Style Field Construction

**Rules (from bible):**
- Max 998 characters. Target 986-998. Run the bundled gate to count — never eyeball it:
  ```
  python scripts/count.py "your style field text"
  ```
  (or `python scripts/count.py --file path/to/field.txt`). Exit 0 = PASS (≤998), exit 1 = FAIL (over limit).
- Order: genre → tempo → key (optional) → vocals → instruments → mood → negatives
- No square brackets (those are for lyrics field only)
- Max 2 genre fusions
- Physical descriptors over technical ones: "bass you feel in your chest" > "sub-bass at 40Hz"
- Named artist references work: "Angerfist meets Rammstein"
- Vocal delivery must be explicit and stacked
- Always include negative prompts for unwanted elements
- For Hungarian: add "Hungarian language vocals" or "Hungarian male vocals with conviction"

**Template:**
```
[genre 1], [genre 2 fusion], [BPM] BPM, [key if relevant], [vocal description stacked 4-5 descriptors], [instrument 1], [instrument 2], [instrument 3], [percussion description], [atmosphere/mood 2-3 words], [dynamic arc instruction], no [unwanted 1], no [unwanted 2], no [unwanted 3], no [unwanted 4], [final vibe sentence]
```

### Step 4: Lyrics — English Version

**Structure tags** (on own lines):
- Core: `[Intro]`, `[Verse 1]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Outro]`, `[End]`
- Vocal: `[Spoken Word]`, `[Whispered]`, `[Shouted Vocals]`, `[Male Choir]`, `[Gregorian Chant]`
- Dynamic: `[Energy: Low]`, `[Energy: Medium]`, `[Energy: High]`, `[Energy: Maximum]`
- Compound tags: `[Chorus | Male Choir, Gravelly Lead, Stomping Rhythm]`

**Formatting:**
- ALL CAPS = louder delivery. Use surgically on 2-3 key words per verse, not every word.
- `(backing text)` = choir/response/ad-libs
- `...` = breathing pause
- Extended vowels for sustain: `MOOOOORE`, `IIIIIIRON`
- Short lines (6-10 syllables) = better rhythmic control

**Rotating chorus technique:** Same anchor lines, different closing verb per chorus to create escalation.

**Call-and-response:**
```
[Lead]
Sound OFF if you're still BREATHING
[Choir]
(STILL BREATHING)
```

### Step 5: Lyrics — Hungarian Version

**DO NOT just translate the English.** Rewrite from the same concept with Hungarian's natural strengths:

**Hungarian advantages to exploit:**
- First-syllable stress → natural downbeat hammering
- Monosyllabic power verbs: FOGD, HÚZD, TÉPD, ZÚZD, TOLD, VERD, ÜSD, ÉGD
- Back vowels for dark mood: harc, vas, súly, ront
- Verbal prefix separation for rhythm: `VÁLTOZZ meg!` not `MEGVÁLTOZOL`

**Rhyme quality checklist:**
- [ ] No more than 30% suffix rhymes (ragrím)
- [ ] Use stem rhymes, assonance (asszonánc), internal rhymes (belső rím)
- [ ] Cross word-class boundaries: noun with verb (`remény / kemény`)
- [ ] Chorus lines ≤ 8 syllables

**Register:** Spoken/colloquial, never literary. Use short forms (`muszáj` not `szükségszerűen`).

**Diacritics:**
- BPM ≤ 100: preserve diacritics
- BPM > 130: strip diacritics to prevent Suno mispronunciation
- Lyric video display versions: ALWAYS preserve diacritics

**Curse word scale:** Max Level 3 in verses. Level 4 (`kurva anyád`) only ONCE at absolute peak, if at all.

### Step 6: Production Notes

For each song, include:
1. **Suno generation strategy:** How many variations to try, what to listen for
2. **Common failure modes:** What might go wrong and how to fix it
3. **Post-generation checklist** (from bible section 1.7)

**Pure Suno only.** If Suno can't handle a section, fix the lyrics or style field — never propose splicing or external TTS (ElevenLabs) fallbacks. Everything runs through Suno in ONE complete script.

## Output Format

```markdown
# [SONG TITLE EN] / [SONG TITLE HU]

## Metadata
- **Genre:** ...
- **BPM:** ...
- **Key:** ...
- **Blueprint:** ...
- **Emotional arc:** ...

## Style Field — English Version (XXX chars)
```
[style field text]
```

## Style Field — Hungarian Version (XXX chars)
```
[style field text — may differ from EN in vocal/language descriptors]
```

## English Lyrics
```
[full lyrics with all tags]
```

## Hungarian Lyrics
```
[full lyrics with all tags]
```

## Production Notes
...
```

## Duration Control (Prevent 7:59 Bloat)

Suno 5.5 generates up to 8 minutes and WILL fill the window if you let it. Apply these rules to EVERY song:

1. **Stack end tags.** Always end with BOTH on separate lines:
   ```
   [Fade Out]
   [End]
   ```
   A single `[End]` is unreliable. Double-stack every time.

2. **Lyric density limits.** Target song lengths:
   - 3:00-3:30 → max 3 verses + 2 choruses + 1 bridge (~40 lines of actual lyrics)
   - 4:00-4:30 → max 4 verses + 3 choruses + 1 bridge (~55 lines)
   - 5:00+ → only if the song structurally demands it. Never by accident.

3. **Kill instrumental padding.** Remove or minimize `[instrumental break]` tags. Each one adds 30-60s. If you need a break, use `[instrumental, 4 bars]` not `[instrumental break, heavy bass, distorted synth melody, no vocals]` — the descriptors invite Suno to explore.

4. **Style field density.** Keep style fields at 800-900 chars for shorter songs. 990+ char style fields encourage Suno to "explore" all descriptors, producing longer output. Save the 990 char density for epic tracks where length is desired.

5. **No post-editing dependency.** Do NOT design songs that require crop/trim to work. The song must land at the right length FROM GENERATION. If it doesn't, the lyrics are too long or the end tags are too weak.

6. **Bridge = last new content.** After the bridge, only the final chorus and outro should remain. No new verses, no new ideas. Bridge → Final Chorus → `[Fade Out]` → `[End]`.

---

## Quality Gate

Before delivering, verify:
- [ ] Style field ≤ 998 characters — verified with `python scripts/count.py` (exit 0), not estimated
- [ ] No square brackets in style field
- [ ] Negative prompts included in style field
- [ ] ALL CAPS used surgically (max 2-3 per verse)
- [ ] Rotating chorus applied (if applicable)
- [ ] Hungarian version is REWRITTEN not translated
- [ ] Hungarian rhymes avoid cheap suffix rhyming
- [ ] Chorus lines ≤ 8 syllables in Hungarian
- [ ] Concept doesn't duplicate the existing catalog
- [ ] Emotional arc has clear shape (not flat intensity)
- [ ] At least one whisper-to-shout dynamic shift exists
