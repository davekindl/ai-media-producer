---
name: line-tapper
description: "Generate an interactive HTML tool for manually timestamping lyrics or script lines against an audio file. Opens in the browser — user plays audio, clicks each line when they hear it, exports precise timestamps. Trigger when the user says 'time these lyrics', 'tap the lines', 'timestamp this audio', 'sync lyrics to audio', 'line tapper', 'manual sync', 'mark the lines', or any variation of needing to manually align text to audio timing."
allowed-tools: Read, Write, Bash
---

# LINE TAPPER

> Audio + Lyrics in → User clicks lines as they hear them → Precise per-line timestamps out.

## When To Use

- User has lyrics/script text and an audio file and needs precise per-line timestamps
- Deepgram or other automated transcription missed too many words
- User wants manual control over subtitle/lyric timing
- Any text-to-audio alignment task where automated tools aren't accurate enough

## Inputs Required

1. **Audio file path** — absolute path to MP3/WAV/OGG on the user's machine
2. **Lyrics or script** — either a file path or pasted text with section tags like `[Verse 1]`, `[Chorus]`, etc.

## How It Works

1. Parse the lyrics into sections and lines, detecting:
   - `[Section Tag]` headers
   - CAPS lines → style: "shouted" (displayed bold white)
   - `(parenthetical lines)` → style: "backing" (displayed italic, dimmed)
   - Everything else → style: "normal"

2. Generate an HTML file from the template (`${CLAUDE_SKILL_DIR}/tapper_template.html`) by injecting:
   - The parsed lyrics as a JSON `data` array
   - The audio file path as `AUDIO_PATH`

3. Open the HTML in the user's default browser

4. User interacts:
   - **Space** — play/pause
   - **Click any line** — stamps the current playback time on that line
   - **Left/Right arrows** — seek ±2 seconds
   - **Shift+Left/Right** — fine seek ±0.5 seconds
   - **R** — restart from beginning
   - **0.5x / 0.75x speed** — slow down for dense sections
   - Re-click a line to re-stamp it
   - **Export** button — copies all timestamps to clipboard

5. User pastes the exported timestamps back into Claude

## Output Format

The export produces text in this format, ready to paste:

```
[Chorus 1]
16.92s | ONE more rep when the body says no
19.88s | GRIP the iron and don't let go
MISSING | Some line the user didn't tap

[Verse 1]
38.55s | Four AM the alarm don't ask twice
...
```

## What Claude Does With The Output

After receiving the pasted timestamps, use them to build an `aligned_lyrics.json` with precise per-line start/end times. Each line's end time = next line's start - 0.1s (or next section start - 0.5s for last line in section, or song end for final line).

## Generation Steps

```
Step 1: Parse lyrics text into sections/lines JSON
Step 2: Read ${CLAUDE_SKILL_DIR}/tapper_template.html
Step 3: Replace LYRICS_DATA_PLACEHOLDER with the JSON
Step 4: Replace AUDIO_PATH_PLACEHOLDER with the file:/// URI
Step 5: Write the HTML to the output directory
Step 6: Open in default browser (start "" "path" on Windows, open on Mac)
Step 7: Wait for user to paste back timestamps
```

## File Reference

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — skill definition |
| `tapper_template.html` | The interactive HTML template |
