---
name: lyric-video-forge
description: "End-to-end lyric video generator from audio + lyrics to YouTube-ready MP4. Uses kie.ai API for background image generation, Deepgram Nova-3 for word-level timestamp extraction, forced alignment for perfect lyric sync, and FFmpeg for video assembly with Ken Burns zoom, karaoke highlight effects, and seamless infinite loop mode. Trigger when the user says 'make a lyric video', 'lyrics video', 'generate a music video', 'lyric video from this song', 'assemble a video for this track', 'video for my Suno track', 'YouTube video for my song', or any variation of wanting to create a video from audio + lyrics. Also trigger for 'karaoke video', 'visualize this song', 'put lyrics on a background', or 'infinite loop video'. Even casual mentions like 'I need a video for this track' or 'can you make a simple lyrics video' should trigger this skill."
---

# LYRIC VIDEO FORGE

> Audio + Lyrics in → YouTube-ready MP4 out. Every step human-approved.

## Overview

Fully automated lyric video pipeline that runs from terminal. Takes a song (MP3/WAV), lyrics text, and optional style prompt — produces a polished lyric video with word-level synchronized text over a generated or provided background image.

## Prerequisites

Before first run, verify these are available:

```bash
# FFmpeg (video assembly)
ffmpeg -version
# Install if missing:
#   Windows: winget install Gyan.FFmpeg   (or: choco install ffmpeg)
#   macOS:   brew install ffmpeg
#   Linux:   sudo apt install ffmpeg

# Python 3.10+
python3 --version   # Windows: py --version

# Required Python packages
pip install deepgram-sdk requests Pillow numpy
# (add --break-system-packages only on Linux distros with PEP 668 enforcement)
```

**API Keys needed (environment variables):**
- `DEEPGRAM_API_KEY` — for word-level transcription (Nova-3)
- `KIE_API_KEY` — for image generation via kie.ai (GPT-Image-2)

If keys aren't set, prompt the user before proceeding.

---

## The Pipeline — 7 Steps, 5 Approval Gates

Every step produces output. Every gate pauses for human review. Nothing proceeds without a thumbs up.

```
┌─────────────────────────────────────────────────────┐
│  INPUT: audio.mp3 + lyrics.txt + (optional) image   │
└────────────────┬────────────────────────────────────┘
                 │
    ┌────────────▼────────────┐
    │  STEP 1: Parse Lyrics   │
    │  Extract sections,      │
    │  lines, structure tags  │
    └────────────┬────────────┘
                 │
         ═══ GATE 1 ═══  "Here's how I parsed your lyrics. Correct?"
                 │
    ┌────────────▼────────────┐
    │  STEP 2: Generate or    │
    │  Load Background Image  │
    │  (kie.ai GPT-Image-2)   │
    └────────────┬────────────┘
                 │
         ═══ GATE 2 ═══  "Here's the background. Approve or re-generate?"
                 │
    ┌────────────▼────────────┐
    │  STEP 3: Transcribe     │
    │  Audio (Deepgram Nova-3)│
    │  Word-level timestamps  │
    └────────────┬────────────┘
                 │
    ┌────────────▼────────────┐
    │  STEP 4: Forced         │
    │  Alignment — match      │
    │  lyrics to timestamps   │
    └────────────┬────────────┘
                 │
         ═══ GATE 3 ═══  "Here's the alignment. Preview sync timing?"
                 │
    ┌────────────▼────────────┐
    │  STEP 5: Style Config   │
    │  Font, colors, effects, │
    │  karaoke vs line-by-line│
    └────────────┬────────────┘
                 │
         ═══ GATE 4 ═══  "Here's the style config. Adjust anything?"
                 │
    ┌────────────▼────────────────────┐
    │  STEP 6: FFmpeg Video Assembly  │
    │  - Ken Burns zoom on background │
    │  - Text overlays synced         │
    │  - Karaoke highlight effect     │
    │  - Infinite loop splice         │
    └────────────┬────────────────────┘
                 │
         ═══ GATE 5 ═══  "Video assembled. Preview first 30s?"
                 │
    ┌────────────▼────────────┐
    │  STEP 7: Final Export   │
    │  1080p MP4, YouTube     │
    │  metadata, loop version │
    └────────────┘
```

---

## Step 1: Parse Lyrics

Read the lyrics file. Detect and extract:
- Structure tags: `[Verse 1]`, `[Chorus]`, `[Bridge]`, etc.
- Section boundaries and line counts
- CAPS lines (shouted/chanted — affects font weight)
- Parenthetical lines (backing vocals / ad-libs — affects opacity/size)
- Pause markers (`...`) and emphasis markers (`. ` between words)

**Output:** A structured JSON representation of the lyrics:

```json
{
  "sections": [
    {
      "tag": "Verse 1",
      "lines": [
        {"text": "Born in the temple where the iron sings", "style": "normal"},
        {"text": "LIFT. THAT. WEIGHT.", "style": "shouted"},
        {"text": "(ONE MORE REP!)", "style": "backing"}
      ]
    }
  ]
}
```

**GATE 1:** Display the parsed structure to the user. Ask: "Does this look right? Any lines miscategorized?" Fix before proceeding.

---

## Step 2: Background Image

Two paths:

### Path A: Generate via kie.ai (GPT-Image-2)
If user provides a style prompt (or you craft one from the song's mood).

kie.ai uses the **unified jobs API**: submit an async task with `createTask`,
then poll `recordInfo` for the result. Default model is `gpt-image-2-text-to-image`.

```python
import requests, time, json

# 1. Submit the task
resp = requests.post(
    "https://api.kie.ai/api/v1/jobs/createTask",
    headers={
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "gpt-image-2-text-to-image",
        "input": {
            "prompt": "<style prompt here>",
            "aspect_ratio": "16:9",   # auto|1:1|9:16|16:9|4:3|3:4
            "resolution": "2K",        # 1K|2K|4K  (1:1 cannot go 4K)
        },
    },
    timeout=30,
)
task_id = resp.json()["data"]["taskId"]

# 2. Poll for completion (state: waiting|queuing|generating|success|fail)
while True:
    info = requests.get(
        "https://api.kie.ai/api/v1/jobs/recordInfo",
        params={"taskId": task_id},
        headers={"Authorization": f"Bearer {KIE_API_KEY}"},
        timeout=30,
    ).json()["data"]
    if info["state"] == "success":
        urls = json.loads(info["resultJson"])["resultUrls"]
        break
    if info["state"] == "fail":
        raise RuntimeError(info.get("failMsg", "kie.ai task failed"))
    time.sleep(5)
```

Status codes: 200 ok, 401 auth, 402 out-of-credits, 422 bad input, 429 rate-limited.
Submit 3 tasks in parallel to get 3 variants, then present all 3 to the user.
(The `kie_client.py` wrapper already implements this submit-and-poll loop.)

### Path B: User provides image
If user supplies an image file, validate dimensions (must be ≥1920x1080 or we'll upscale) and proceed.

**GATE 2:** Show the image(s). User picks one or requests re-generation with a modified prompt.

---

## Step 3: Transcribe Audio (Deepgram)

Send audio to Deepgram Nova-3 with word-level timestamps:

```python
from deepgram import DeepgramClient, PrerecordedOptions

deepgram = DeepgramClient(DEEPGRAM_API_KEY)

with open("audio.mp3", "rb") as audio:
    source = {"buffer": audio.read(), "mimetype": "audio/mp3"}
    options = PrerecordedOptions(
        model="nova-3",
        smart_format=True,
        utterances=True,
        punctuate=True,
        diarize=False,
        language="en"  # adjust per song language
    )
    response = deepgram.listen.rest.v("1").transcribe_file(source, options)
```

Extract word-level timestamps from the response:

```python
words = response.results.channels[0].alternatives[0].words
# Each word: {"word": "born", "start": 1.234, "end": 1.567, "confidence": 0.98}
```

**Output:** `timestamps.json` — every word with start/end time and confidence score.

---

## Step 4: Forced Alignment

This is the precision step. We have:
- Ground truth lyrics (what the user WROTE)
- Deepgram's transcription (what the AI HEARD)

The forced alignment matches them:

1. **Normalize both:** lowercase, strip punctuation, collapse whitespace
2. **Sequence alignment:** Use dynamic programming (Needleman-Wunsch or similar) to align the lyric words to the transcribed words
3. **Transfer timestamps:** Each lyric word inherits the start/end time from its aligned transcription match
4. **Handle mismatches:**
   - Words Deepgram missed → interpolate timing from surrounding words
   - Words Deepgram hallucinated → skip
   - Low confidence matches (< 0.7) → flag for user review
5. **Section timing:** Derive section start/end from first/last word timestamps per section

**Output:** `aligned_lyrics.json` — every lyric line and word with precise timestamps:

```json
{
  "sections": [
    {
      "tag": "Verse 1",
      "start": 12.5,
      "end": 28.3,
      "lines": [
        {
          "text": "Born in the temple where the iron sings",
          "start": 12.5,
          "end": 15.2,
          "words": [
            {"word": "Born", "start": 12.5, "end": 12.8},
            {"word": "in", "start": 12.85, "end": 12.95}
          ]
        }
      ]
    }
  ],
  "flagged": [
    {"word": "divine", "line": 4, "reason": "low_confidence", "confidence": 0.62}
  ]
}
```

**GATE 3:** Show the alignment summary. Highlight any flagged words. If flagged count > 5, warn the user and offer to re-run with a different Deepgram model or manual correction. Offer a 10-second audio preview at any flagged timestamp so user can verify.

---

## Step 5: Style Configuration

Present the user with style options. Defaults are optimized for readability on dark backgrounds:

```json
{
  "display_mode": "karaoke",
  "font": {
    "family": "Montserrat-Bold",
    "size_normal": 64,
    "size_shouted": 80,
    "size_backing": 48,
    "color_inactive": "#CCCCCC",
    "color_active": "#FFFFFF",
    "color_highlight": "#FFD700",
    "shadow": true,
    "shadow_color": "#000000",
    "shadow_offset": 3
  },
  "background": {
    "ken_burns": true,
    "zoom_start": 1.0,
    "zoom_end": 1.08,
    "zoom_duration_seconds": "full_song",
    "pan_direction": "slow_right"
  },
  "effects": {
    "line_fade_in_ms": 300,
    "line_fade_out_ms": 500,
    "highlight_style": "word_by_word_fill",
    "section_transition": "fade_black_500ms",
    "backing_vocal_opacity": 0.6
  },
  "loop": {
    "enabled": true,
    "copies": 3,
    "crossfade_ms": 2000,
    "background_shift_per_copy": true
  },
  "output": {
    "resolution": "1920x1080",
    "fps": 30,
    "codec": "libx264",
    "audio_codec": "aac",
    "bitrate": "8M"
  }
}
```

### Display Modes

| Mode | Description | When to use |
|------|-------------|-------------|
| `karaoke` | Words highlight gold as they're sung, word-by-word | Default — most engaging |
| `line_by_line` | Full line appears at once, fades out after | Simpler, cleaner look |
| `hybrid` | Lines appear, then individual words highlight within | Best of both — use for slower songs |

### Ken Burns Zoom Options

| Style | Description |
|-------|-------------|
| `slow_zoom_in` | 1.0 → 1.08 over full song (default) |
| `slow_zoom_out` | 1.08 → 1.0 |
| `breathing` | Oscillates 1.0 → 1.04 → 1.0 on 8-bar cycle |
| `pan_and_zoom` | Slow pan right/left with slight zoom |
| `static` | No movement |

### Infinite Loop Mode

When `loop.enabled = true`:
- Video is rendered 3 times (A → B → C)
- Each copy uses a slightly different Ken Burns trajectory (shifted start point) OR a different background image (if user provides 3)
- 2-second crossfade between copies
- Last frame of copy C crossfades into first frame of copy A → seamless loop on YouTube
- Total duration = song_length × 3 + crossfade overhead

**GATE 4:** Present the style config. User adjusts or approves.

---

## Step 6: FFmpeg Video Assembly

This is the core build step. Generate an FFmpeg command pipeline:

### 6a: Background with Ken Burns

```bash
ffmpeg -loop 1 -i background.png \
  -vf "zoompan=z='1+0.0003*in':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1920x1080:fps=30" \
  -t {duration} -pix_fmt yuv420p -c:v libx264 \
  background_video.mp4
```

### 6b: Generate ASS Subtitle File

For karaoke-style highlighting, generate an ASS (Advanced SubStation Alpha) subtitle file. ASS supports:
- Word-by-word karaoke timing via `\k` tags
- Font styling, colors, shadows, borders
- Fade in/out effects per line
- Position control

```ass
[Script Info]
Title: Lyric Video
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Style: Default,Montserrat Bold,64,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,10,10,80

[Events]
Dialogue: 0,0:00:12.50,0:00:15.20,Default,,0,0,0,karaoke,{\k30}Born {\k10}in {\k15}the {\k20}temple {\k18}where {\k15}the {\k22}iron {\k25}sings
```

The `\k` values are in centiseconds (duration each word is highlighted).

### 6c: Composite Everything

```bash
ffmpeg -i background_video.mp4 -i audio.mp3 \
  -vf "ass=lyrics.ass" \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k \
  -shortest -y output.mp4
```

### 6d: Infinite Loop Assembly (if enabled)

```bash
# Render 3 copies with shifted Ken Burns
# Create concat file
echo "file 'copy_a.mp4'" > concat.txt
echo "file 'copy_b.mp4'" >> concat.txt
echo "file 'copy_c.mp4'" >> concat.txt

# Concatenate with crossfade
ffmpeg -f concat -safe 0 -i concat.txt \
  -filter_complex \
  "[0:v]xfade=transition=fade:duration=2:offset={offset1}[v1]; \
   [v1]xfade=transition=fade:duration=2:offset={offset2}[vout]" \
  -map "[vout]" -map 0:a \
  -c:v libx264 -crf 18 -c:a aac -y loop_output.mp4
```

**GATE 5:** Render a 30-second preview (from the first chorus if possible — that's the hook). Play for user. If approved, render full video. If not, identify what's wrong and loop back to the relevant step.

---

## Step 7: Final Export

Export the final video(s) to the output directory:

```
output/
├── {song_name}_lyric_video.mp4          # Single play version
├── {song_name}_lyric_video_loop.mp4     # 3x infinite loop version
├── {song_name}_lyrics.srt               # Subtitle file (for YouTube CC upload)
├── {song_name}_lyrics.ass               # Styled subtitle file
├── {song_name}_aligned_lyrics.json      # Timing data (reusable)
├── {song_name}_style_config.json        # Style config (reusable as template)
└── {song_name}_metadata.json            # YouTube metadata suggestions
```

The metadata file includes suggested YouTube title, description, tags, and chapters (derived from section timestamps).

---

## Character Encoding Rules (Windows ffmpeg)

ffmpeg's `subtitles=` filter on Windows defaults to CP1252, not UTF-8. This causes mangled output (e.g. `—` becomes `â€"`, `Hungarian diacritics` become garbage). Apply these rules to EVERY ASS generation:

1. **Read timing JSON explicitly as UTF-8:**
   ```python
   with open(timing_path, encoding='utf-8') as f:
       timing = json.load(f)
   ```
   Never `json.load(open(path))` without encoding on Windows — it defaults to cp1252.

2. **Write ASS file as UTF-8 with BOM:**
   ```python
   Path(ass_path).write_text(content, encoding='utf-8-sig')
   ```
   The BOM (`utf-8-sig`) makes ffmpeg detect UTF-8 correctly.

3. **Replace problematic Unicode dashes with ASCII hyphens:**
   ```python
   text = text.replace('\u2014', '-').replace('\u2013', '-')  # em dash, en dash
   ```
   Even with BOM, em dashes can still break on some ffmpeg builds. Replace them preemptively.

4. **Use raw strings for ASS escape codes:**
   ```python
   FADE_TAG = r"{\fad(200,200)}"  # NOT "{\fad(200,200)}"
   ```
   Python interprets `\f` as form feed. Always use `r"..."` for ASS tags that start with `\f`, `\t`, `\n`, `\r`.

5. **Verify after generation:**
   ```python
   content = Path(ass_path).read_text(encoding='utf-8-sig')
   assert content.count('\u2014') == 0  # no em dashes
   assert content.count('\x0c') == 0     # no form feeds
   assert content.count('\\fad') > 0     # \fad tags present
   ```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Deepgram API fails | Retry 3x with exponential backoff. If still failing, offer manual timestamp entry mode |
| kie.ai API fails | Retry 2x. Fall back to user-provided image |
| FFmpeg crashes on assembly | Log full command + stderr. Most common: wrong pixel format or audio codec mismatch. Auto-fix and retry |
| Alignment confidence < 50% overall | Warn user. Offer to output a timing CSV they can manually correct, then re-import |
| Font not found | On Linux/macOS (fontconfig present), fall back to DejaVu Sans Bold and warn. On Windows, `fc-list` is absent so the requested font is trusted and ffmpeg resolves it |

---

## Reusable Templates

After a successful run, save the style config as a template. On future runs, offer: "Use your previous style config, or start fresh?"

Templates are saved to `~/.lyric-video-forge/templates/`:
```json
{
  "name": "iron_temple_style",
  "created": "2026-03-30",
  "config": { ... }
}
```

---

## New Capabilities (v2)

### Capability 1: Lyric Stripping (Step 1a)

Runs immediately after Step 1. Takes raw Suno-tagged lyrics and produces:

- **clean_lyrics.txt** — Only singable/speakable words. All `[bracketed tags]`, `(parenthetical production notes)`, and instrumental directions removed. Hungarian diacritics, ALL CAPS, extended vowels preserved.
- **structure_map.json** — Section metadata with energy levels (1-5), section type (vocal/instrumental), lyric line references.

Energy detection: `[Energy: Maximum]`/`[Drop]` = 5, `[Energy: High]`/`[Build-Up]` = 3-4, `[Verse]` = 2, `[Intro]`/`[Outro]` = 1. ALL CAPS lyrics bump energy +1.

### Capability 2: Deepgram Crossmatch (Enhanced Step 4)

User's clean_lyrics.txt = **grammar truth** (correct words, spelling, diacritics).
Deepgram response = **timing truth** (when each word is spoken/sung).

For each word: keep user's text, steal Deepgram's timestamp. If Deepgram hears "kelj" but user wrote "Kelj" — output "Kelj" with Deepgram's timing. Instrumental sections from structure_map are skipped. Missing words get interpolated timing.

Output includes section references and energy levels per word.

### Capability 3: Keyframe Image Generation (Replaces Step 2)

Instead of 1 static background, generates 5 keyframe images (A-E) at different energy tiers:

| Tier | Frame | What Changes |
|------|-------|-------------|
| 1 - Stillness | A | Eyes closed, head down, single dim light, cold, heavy fog |
| 2 - Awakening | B | Eyes opening, warm light entering, embers glowing |
| 3 - Building | C | Active pose, multiple fire sources, sparks, tension |
| 4 - Eruption | D | Full exertion, screaming, blinding backlight, chaos |
| 5 - Transcendence | E | Arms spread, consumed by light/fire, near-abstract |

**Visual Constitution** defines three anchors that appear VERBATIM in all 5 prompts:
- **Character Anchor** — one physical description, locked across all tiers
- **Setting Anchor** — one environment, only lighting/atmosphere changes
- **Art Direction Anchor** — aspect ratio, palette, rendering style, negative prompt

**Model Selection:** Default → GPT-Image-2 (`gpt-image-2-text-to-image`). Photorealistic portraits → Flux (renders faces more naturally).

**3 variations per tier = 15 images total.** User picks best per tier (approval gate).

Enable with `--keyframe-mode` flag.

### Capability 4: Video Loop Plan (Step 5a) — PLANNING ONLY

> **Status: the plan is generated, but clips are NOT.** `--video-loops` produces
> a `loop_plan.json` describing the intended clip sequence. Actual image-to-video
> generation (Kling/Veo/Sora) is **not implemented** — `generate_video_clip()` in
> `kie_client.py` raises `NotImplementedError` rather than silently emitting a
> still image (its prior, buggy behaviour). Until the kie.ai image-to-video input
> schema is wired up, the rendered output always uses the Ken Burns path below.

Maps structure_map sections to keyframe transition pairs with the video model
that *would* be used once generation is implemented:

| Transition Type | Intended Video Model | Use Case |
|----------------|----------------------|----------|
| Same (A→A) | Kling 3.0 | Subtle breathing/flicker loops |
| Adjacent (A→B) | Veo 3 Fast | Smooth energy shifts |
| Skip (A→C, C→E) | Sora 2 Pro HD | Dramatic jumps |
| Reverse (D→B) | Veo 3 Fast | Gradual energy drops |
| Reverse sudden (E→A) | Sora 2 Pro HD | Sudden cuts |

Output: `loop_plan.json` with clip sequence, models, motion prompts, durations, and FFmpeg transition types.

Enable with `--video-loops` flag (requires `--keyframe-mode`). Emits the plan only.

### Capability 5: FFmpeg Assembly

**Supported path (default):** Ken Burns zoom over a still background (single
background, or tier-A keyframe in `--keyframe-mode`), with ASS karaoke subtitles
overlaid and audio mixed in. This is the fully functional render path.

**Not yet implemented:** concatenating generated video-loop clips with
transitions. Depends on Capability 4's clip generation, which is stubbed (see
the status note above).

---

## Quick Reference — Full CLI Flow

On Windows, use `py` instead of `python3`. Each step pauses for approval unless
`--auto` is passed (`--auto` skips gates, for overnight batch runs).

```bash
# Single background (default render path: Ken Burns over one image)
python3 forge.py --audio song.mp3 --lyrics lyrics.txt --generate-image "dark cathedral"

# Keyframe mode (5 tiers x 3 variations)
python3 forge.py --audio song.mp3 --lyrics lyrics.txt \
  --keyframe-mode \
  --genre "industrial metal" \
  --character "A hooded monk with scarred arms, shaved head, iron chains wrapped around forearms" \
  --setting "An ancient cathedral forge with anvils, molten metal channels, and hanging chains" \
  --variations 3

# Keyframe mode + video-loop PLAN (writes loop_plan.json only — clip
# generation is not yet implemented; render still uses Ken Burns)
python3 forge.py --audio song.mp3 --lyrics lyrics.txt \
  --keyframe-mode --video-loops \
  --genre "industrial metal" \
  --character "..." --setting "..." \
  --auto  # skip gates for batch runs
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `forge.py` | Main pipeline orchestrator |
| `align.py` | Forced alignment + crossmatch engine |
| `ass_generator.py` | ASS subtitle file generator |
| `kie_client.py` | kie.ai unified jobs API wrapper (GPT-Image-2 images + keyframes; video clip generation stubbed/`NotImplementedError`) |
| `deepgram_client.py` | Deepgram Nova-3 API wrapper |
| `strip.py` | Lyric stripping (clean text + structure map) |
| `world_build.py` | Visual constitution builder (anchors + keyframe prompts) |
| `loop_planner.py` | Video loop plan generator (section → transition mapping) |
