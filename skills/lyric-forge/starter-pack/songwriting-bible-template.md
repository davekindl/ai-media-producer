# Suno Songwriting Bible — Template

This is your house methodology file. lyric-forge reads it before writing any song.
It ships pre-filled with working defaults so the skill runs out of the box — but it is a
template: overwrite every section with your own findings as your catalog grows. The section
numbering matters: SKILL.md references **section 1.7** (post-generation checklist) and
**section 2** (song catalog) by number. Keep them where they are.

---

## 1. Methodology

### 1.1 Core Principle

One complete Suno-ready script per song. Everything — structure, delivery, dynamics —
is encoded in the lyrics field and the style field. No post-editing dependency: the song
must land at the right length and shape from generation.

### 1.2 Style Field Rules

- Max 998 characters. Target 986-998 for epic tracks, 800-900 for shorter songs.
  Verify with `python scripts/count.py "your style field"` — never eyeball it.
- Order: genre → tempo → key (optional) → vocals → instruments → mood → negatives.
- No square brackets in the style field (brackets belong to the lyrics field).
- Max 2 genre fusions.
- Physical descriptors beat technical ones: "bass you feel in your chest" > "sub-bass at 40Hz".
- Vocal delivery explicit and stacked (4-5 descriptors).
- Always end with negative prompts for unwanted elements.

### 1.3 Structure Tags

Core: `[Intro]`, `[Verse 1]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Outro]`, `[End]`.
Vocal: `[Spoken Word]`, `[Whispered]`, `[Shouted Vocals]`, `[Male Choir]`.
Dynamic: `[Energy: Low]` → `[Energy: Maximum]`.
Compound tags combine both: `[Chorus | Male Choir, Gravelly Lead, Stomping Rhythm]`.

### 1.4 Delivery and Formatting

- ALL CAPS = louder delivery. Surgical use only: 2-3 key words per verse.
- `(parentheses)` = backing vocals / choir response / ad-libs.
- `...` = breathing pause. Extended vowels sustain: `MOOOOORE`.
- Short lines (6-10 syllables) give better rhythmic control.
- Rotating chorus: same anchor lines, different closing verb per chorus for escalation.

### 1.5 Generation Strategy

- Generate 3-5 variations per script. Never accept the first render by default.
- Listen for: vocal delivery matching the tags, chorus lift, section transitions,
  whether the negative prompts held.
- If a section fails consistently, the script is at fault — fix lyrics or style field
  and regenerate. Never plan to splice takes or bolt on external TTS.

### 1.6 Duration Control

- Double-stack end tags: `[Fade Out]` then `[End]` on separate lines, every song.
- Lyric density: 3:00-3:30 → ~40 lines; 4:00-4:30 → ~55 lines. 5:00+ only by design.
- Minimize `[instrumental break]` tags — each adds 30-60 seconds.
- Bridge is the last new content: Bridge → Final Chorus → `[Fade Out]` → `[End]`.

### 1.7 Post-Generation Checklist

- [ ] Length within target — no runaway 7:59 render
- [ ] Vocal delivery matches the structure tags (whisper is whispered, shout is shouted)
- [ ] Chorus is the loudest, most memorable section — clear lift from verse
- [ ] No garbled words; language pronunciation clean (re-check diacritics if not)
- [ ] Negative prompts held (no unwanted instruments/moods leaking in)
- [ ] Dynamic arc audible: the song builds, it is not flat intensity
- [ ] Ending lands — fade or hard stop as scripted, no dead air
- [ ] Catalog updated (section 2) before starting the next song

---

## 2. Song Catalog

Log every finished song here. Step 1's anti-duplication check reads this table:
never repeat a genre + emotional-angle combo that already has a row.

| # | Title (EN / HU) | Genre | Emotional angle | BPM | Blueprint | Status |
|---|-----------------|-------|-----------------|-----|-----------|--------|
| 01 | *(example)* First Light / Első fény | Cinematic hip-hop | Ritual of showing up | 90 | Slow-build orchestral hip-hop | draft |
| 02 |  |  |  |  |  |  |
| 03 |  |  |  |  |  |  |

---

## 3. House Rules

Your standing overrides — things the generator must always or never do, regardless of
concept. Examples to replace with your own:

- Always: one BPM per song; escalate with delivery tags and word weight, not tempo.
- Always: earn the caps — save full-caps delivery for the final peak.
- Never: literary register in Hungarian lyrics; keep it spoken and colloquial.
