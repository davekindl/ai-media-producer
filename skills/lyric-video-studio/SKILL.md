---
name: lyric-video-studio
description: "End-to-end lyric video production studio. Takes audio + video clips + lyrics, produces a tapper for manual timing, renders a perfectly looped video with styled lyrics overlay, and generates a YouTube description. Trigger when the user says 'lyric video', 'make a lyric video', 'lyrics on video', 'music video with lyrics', 'lyric video studio', or any variation of wanting to create a video with synced lyrics from audio + video + text inputs."
disable-model-invocation: true
---

# LYRIC VIDEO STUDIO

> Audio + Video + Lyrics in → Timed lyric video + YouTube description out.

## Overview

Full production pipeline for lyric videos. Takes raw inputs (audio, video clips, lyrics), walks the user through manual line timing, and outputs a polished video with styled text overlay plus a ready-to-paste YouTube description.

## Studio vs. Forge — Manual vs. Auto (read before choosing)

This studio and `lyric-video-forge` solve the same end goal but at opposite ends of the automation spectrum. They are NOT interchangeable, and this studio does NOT delegate timing or subtitle generation to forge.

| | **lyric-video-studio (this skill)** | **lyric-video-forge** |
|---|---|---|
| Timing | **Manual** — user taps each line in the browser tapper (line-tapper) | **Auto** — Deepgram Nova-3 transcription + forced alignment |
| Background | User-provided video clip(s), looped + crossfaded | kie.ai-generated still image with Ken Burns zoom |
| Subtitle display | Line-by-line fade (whole line appears) | Word-by-word karaoke highlight |
| Subtitle generator | **Bundled `generate_ass.py` (this dir)** | `ass_generator.py` (forge's own) |
| Best for | Hand-timed control, real footage, Hungarian gym tracks | Hands-off, image background, fast turnaround |

**Why this studio ships its OWN `generate_ass.py` instead of calling forge's:** forge's `ass_generator.py` writes the `.ass` file as plain UTF-8 with **no BOM** (`encoding="utf-8"`) and performs **no dash / Hungarian long-vowel normalization**. On some FFmpeg/libass builds a BOM-less file is misread as the system ANSI codepage, which corrupts Hungarian accented characters (`á é í ó ö ő ú ü ű`) and typographic dashes. Delegating to forge would reproduce that bug verbatim. The bundled `generate_ass.py` writes **UTF-8 with BOM (`utf-8-sig`)** and normalizes dashes the Hungarian way (spaced hyphen → en-dash, `--` → em-dash), so this studio is encoding-correct by construction.

If you want the fully automated path (auto-timing + generated image background), use `lyric-video-forge` instead — but accept its karaoke style and its encoding limitation.

## Required Inputs

Ask the user for these 4 things before starting:

| Input | Format | Notes |
|-------|--------|-------|
| **Audio** | WAV or MP3 path | The song/track |
| **Video** | One or more MP4 paths | If multiple: numbered filenames (1-name.mp4, 2-name.mp4, etc.) get concatenated into a loop cycle. If single: looped as-is |
| **Lyrics** | Text with `[Section]` tags | Pasted inline or file path. Sections like `[Chorus]`, `[Verse 1]`, `[Bridge]`, `[Outro]` |
| **Font** | Font name or "pick for me" | Show https://www.dafont.com for browsing. Can use multiple fonts (e.g., one for choruses, one for verses). Ask which font goes where |

## Pipeline — 7 Steps

```
INPUT: audio + video(s) + lyrics + font choice
  │
  ├─ Step 1: Parse lyrics
  ├─ Step 2: Analyze & prep video
  ├─ Step 3: Generate tapper HTML → open in browser
  │          ══ USER TAPS LINES ══
  ├─ Step 4: Process tapped timestamps
  ├─ Step 5: Install fonts + generate ASS subtitles
  ├─ Step 6: Render final video
  └─ Step 7: Generate YouTube description
```

---

### Step 1: Parse Lyrics

Parse the lyrics text into structured sections and lines:

- `[Section Tag]` lines → section headers
- Lines starting with CAPS words (ONE, GRIP, CRUSH, etc.) → style: `shouted`
- Lines wrapped in `(parentheses)` → style: `backing`
- All other lines → style: `normal`

Save as `parsed_lyrics.json` in the output directory.

---

### Step 2: Analyze & Prep Video

**If single video file:**
- Get dimensions and duration
- Will be looped with `-stream_loop` or concat to cover audio duration

**If multiple numbered files (1-xxx.mp4, 2-xxx.mp4, ...):**
1. Probe all files for resolution, fps, pixel format
2. Identify the odd ones out (different resolution)
3. Normalize ALL to match: pick the most common resolution, or scale to the largest square dimension
   - Square videos: scale to `NxN` where N = max dimension found
   - Mixed aspect ratios: center-crop non-square to square, then scale to match
   - Normalize fps to match (use the most common fps)
4. Concatenate in numbered order with 0.5s crossfade transitions between each
5. The sequence forms one loop cycle (last clip crossfades naturally back to first on repeat)

**Framing for 1920x1080 output:**
- If source is square: pad with black pillarbox bars (`pad=1920:1080:(1920-w)/2:0:black`)
- If source is 16:9: use as-is
- If source is 9:16: pillarbox with heavy black bars

**Loop to audio duration:**
- Calculate how many cycles needed: `ceil(audio_duration / cycle_duration)`
- Concat that many copies
- Do NOT trim — let `-shortest` handle it during final mux

Save intermediate files:
- `one_cycle.mp4` — single loop cycle
- `video_loop.mp4` — full-length looped + framed background

---

### Step 3: Generate Tapper HTML

Read the tapper template from the sibling `line-tapper` skill: `${CLAUDE_SKILL_DIR}/../line-tapper/tapper_template.html` (i.e. the `line-tapper` skill directory alongside this one). If `${CLAUDE_SKILL_DIR}` is unset, fall back to the installed skills root for `line-tapper/tapper_template.html`.

Inject:
- `LYRICS_DATA_PLACEHOLDER` → the parsed lyrics JSON array
- `AUDIO_PATH_PLACEHOLDER` → `file:///` URI to the audio file

Write to output directory as `tapper.html`. Open in browser:
- Windows: `start "" "path/to/tapper.html"`
- Mac: `open "path/to/tapper.html"`

Tell the user:
> "Tapper is open. Hit Play, click each line when you hear it, then Export and paste the output back here."

**STOP and wait for the user to paste timestamps.**

---

### Step 4: Process Tapped Timestamps

Parse the user's pasted output. Expected format:
```
[Section Name]
16.92s | Line text here
19.88s | Another line
MISSING | Line they didn't tap
```

Build `aligned_lyrics.json`:
- Each line gets `start` from the tapped timestamp
- Each line's `end` = next line's start - 0.1s
- Last line in section: `end` = next section's first line start - 0.5s
- Very last line: `end` = audio duration or start + 14s (whichever is smaller)
- Lines marked MISSING: interpolate from neighbors
- Distribute word timestamps evenly within each line (for potential karaoke mode)

---

### Step 5: Install Fonts + Generate ASS

**Font installation:**
1. If user provided a dafont.com font name, download it:
   ```
   curl -sL "https://dl.dafont.com/dl/?f=FONT_NAME_SLUG" -o font.zip
   ```
2. Extract .ttf/.otf files
3. Copy to `~/AppData/Local/Microsoft/Windows/Fonts/` (Windows) or `~/Library/Fonts/` (Mac)
4. Run `fc-scan` on the file to get the internal font family name — this is what goes in the ASS file

**ASS subtitle generation — use the bundled `generate_ass.py` (do NOT hand-roll, do NOT call forge):**

Run the encoding-correct generator shipped in this skill directory. It writes the `.ass` and `.srt` as **UTF-8 with BOM (`utf-8-sig`)** and applies Hungarian dash normalization — neither of which forge's generator does.

```bash
python "${CLAUDE_SKILL_DIR}/generate_ass.py" \
  --aligned aligned_lyrics.json \
  --ass-output lyrics.ass \
  --srt-output lyrics.srt \
  --font-chorus "FONT_FAMILY_A" \
  --font-verse  "FONT_FAMILY_B"
```

- Pass the internal font family names from `fc-scan` (step 4 above) as `--font-chorus` (font A → Chorus/Outro) and `--font-verse` (font B → Verse/Bridge). For a single font, pass the same name to both.
- Input is the `aligned_lyrics.json` built in Step 4 (sections → lines with `start`, `end`, `text`, `style`).
- Output is `lyrics.ass` (for FFmpeg) **and** `lyrics.srt` (plain SRT for YouTube CC), both UTF-8+BOM.

**What the generator produces (the studio aesthetic it encodes):**
- Multi-font styles per section type: `ChorusShouted/Normal/Backing` (font A), `VerseShouted/Normal/Backing` and `BridgeShouted/Normal/Backing` (font B)
- Primary color white `&H00FFFFFF`; outline black 5px; shadow black 6px
- Backing vocals: green tint `&H4000FF66`, italic, pushed lower (V120)
- Fade: 150ms in, 300ms out per line; alignment bottom-center (2); margins L40 R40 V80
- Display mode: line-by-line (not karaoke) — whole line appears and fades
- Dash handling: spaced ` - ` → en-dash `–`, `--`/`---` → em-dash `—` (Hungarian typography); word-internal hyphens left untouched
- Section→style mapping: "Chorus"/"Outro" → font A; "Verse" → font B; "Bridge" → font B (dimmer via smaller size)

To override fade timing, pass `--fade-in-ms` / `--fade-out-ms`. See the module docstring in `generate_ass.py` for the full input schema and the encoding rationale.

---

### Step 6: Render Final Video

```bash
ffmpeg -y -i video_loop.mp4 -i audio.wav \
  -vf "ass=lyrics.ass:fontsdir='FONTS_DIR'" \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 320k \
  -shortest \
  -movflags +faststart \
  "OUTPUT_NAME.mp4"
```

**Audio quality:** Use `-b:a 320k` for best AAC quality. If input is WAV, this preserves maximum fidelity. If input is already MP3, match or exceed source bitrate.

**Video quality:** CRF 18, preset slow, libx264. `-movflags +faststart` for YouTube streaming optimization.

**Output naming:** Use the song title derived from the audio filename, sanitized.

---

### Step 7: Generate YouTube Description

Detect lyrics language (Hungarian or English) from the lyrics text. Use character detection:
- If lyrics contain `á`, `é`, `í`, `ó`, `ö`, `ő`, `ú`, `ü`, `ű` → Hungarian
- Otherwise → English

**Hungarian template:**
```
{ARTIST} — {TITLE}

{USER_PROVIDED_INTRO_TEXT OR generate 3-4 raw, short lines about the song's theme}

---

🎵 AI-generated music (Suno) | Visual: Kling 3.0 + KIE.AI
🔔 Feliratkozás az új adagokért hetente
📌 {ARTIST} — illegális teljesítményfokozó audio.

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

DALSZÖVEG:

{FULL LYRICS WITH SECTION TAGS}

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

{HASHTAGS: #edzés #motiváció #gym #metal #magyarzene #{artist} #workout #gymmotivation #aimusic}
```

**English template:**
```
{ARTIST} — {TITLE}

{USER_PROVIDED_INTRO_TEXT OR generate 3-4 raw, short lines about the song's theme}

---

🎵 AI-generated music (Suno) | Visual: Kling 3.0 + KIE.AI
🔔 Subscribe for weekly doses
📌 {ARTIST} — illegal performance-enhancing audio.

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

LYRICS:

{FULL LYRICS WITH SECTION TAGS}

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

{HASHTAGS: #workout #motivation #gym #metal #{artist} #discipline #iron #gymmotivation #aimusic}
```

Also output a **Tags** line (comma-separated) for the YouTube tags field.

Ask the user for:
- Artist name
- Song title (derived from audio filename if not provided)
- Intro text (optional — if not provided, generate 3-4 lines matching the song's raw energy)

---

## Output Files

All saved to the working directory or a `lyric-video/` subdirectory:

| File | Purpose |
|------|---------|
| `tapper.html` | Interactive timing tool |
| `parsed_lyrics.json` | Structured lyrics |
| `aligned_lyrics.json` | Lyrics with timestamps |
| `lyrics.ass` | Styled subtitles for FFmpeg |
| `lyrics.srt` | Plain subtitles for YouTube CC |
| `one_cycle.mp4` | Single video loop cycle |
| `video_loop.mp4` | Full-length looped background |
| `{title}_lyric_video.mp4` | Final rendered video |
| `youtube_description.txt` | Ready-to-paste description |

---

## Prerequisites

- **FFmpeg** with libass support (standard builds include it)
- **Python 3.9+** (runs the bundled `generate_ass.py` subtitle generator — standard library only, no pip installs)
- Fonts installed to system or user fonts directory
- `line-tapper` skill installed alongside this one at `${CLAUDE_SKILL_DIR}/../line-tapper/` (for the tapper template)

---

## Error Handling

| Problem | Fix |
|---------|-----|
| Videos have different resolutions | Auto-normalize to most common, center-crop outliers |
| Font not found by FFmpeg | Use `fontsdir` parameter pointing to install directory |
| User pastes incomplete timestamps (MISSING lines) | Interpolate from neighbors, warn user |
| Audio longer than video loop | Add more loop cycles automatically |
| Non-standard section tags in lyrics | Fuzzy-match against known tags (verse, chorus, bridge, intro, outro, etc.) |

---

## Quick Reference

```
User: "make a lyric video"
→ Ask: audio path, video path(s), lyrics, font preference
→ Parse lyrics, prep video loop, open tapper
→ User taps, pastes back
→ Build ASS, render video, generate YT description
→ Output: MP4 + SRT + youtube_description.txt
```
