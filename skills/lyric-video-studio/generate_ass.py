"""
ASS / SRT subtitle generator for LYRIC VIDEO STUDIO.

Why this exists (do NOT replace with a delegate to lyric-video-forge):
    lyric-video-forge's ass_generator.py writes the subtitle file with
    `encoding="utf-8"` (NO byte-order mark) and performs zero dash / Hungarian
    long-vowel normalization. libass on some FFmpeg builds misreads a BOM-less
    UTF-8 .ass as the system ANSI codepage, which mangles Hungarian accented
    characters (á é í ó ö ő ú ü ű) and turns typographic dashes into mojibake.
    This studio renders Hungarian gym lyrics, so correct encoding is mandatory.

What this fixes vs forge:
    1. Writes UTF-8 WITH BOM (utf-8-sig) so libass detects UTF-8 reliably.
    2. Normalizes dashes: ASCII hyphen-minus surrounded by spaces -> en-dash;
       double/triple hyphen -> em-dash. (Hungarian uses the en-dash "gondolatjel"
       for parenthetical and dialogue dashes, not the hyphen.)
    3. Leaves Hungarian long vowels (ő ű and their caps) intact end-to-end and
       guarantees they survive the write because of the BOM + utf-8-sig codec.
    4. Honors the STUDIO ass spec (line-by-line display, green italic backing,
       multi-font section styles), not forge's karaoke-first spec.

Input: aligned_lyrics.json produced by Studio Step 4. Schema:
    {
      "sections": [
        {
          "name": "Chorus 1",
          "is_instrumental": false,
          "lines": [
            {"start": 16.92, "end": 19.78, "text": "...", "style": "shouted|backing|normal"}
          ]
        }
      ]
    }

Usage:
    python generate_ass.py --aligned aligned_lyrics.json \
        --ass-output lyrics.ass --srt-output lyrics.srt \
        [--font-chorus "FontFamily A"] [--font-verse "FontFamily B"] \
        [--audio-duration 213.4]
"""

import argparse
import json
import re
from pathlib import Path


# --- Hungarian-aware dash normalization -------------------------------------

EN_DASH = "–"   # – gondolatjel
EM_DASH = "—"   # —

# 3+ hyphens (e.g. a literal divider) -> em-dash; 2 -> em-dash.
_MULTI_HYPHEN = re.compile(r"-{2,}")
# A hyphen-minus used as a spaced dash (" - ") -> spaced en-dash.
# Hungarian sets the en-dash for parenthetical/range dashes; the bare hyphen is
# reserved for word-internal compounds, which we must NOT touch.
_SPACED_HYPHEN = re.compile(r"(?<=\S) - (?=\S)")


def normalize_dashes(text: str) -> str:
    """Convert ASCII hyphen-minus used as punctuation into proper dashes.

    Word-internal hyphens (compounds like "anti-hero", " READY-set-GO") are left
    untouched because they have no surrounding spaces and are not runs of 2+.
    """
    text = _MULTI_HYPHEN.sub(EM_DASH, text)
    text = _SPACED_HYPHEN.sub(f" {EN_DASH} ", text)
    return text


# --- color helpers (ASS uses &HAABBGGRR, reversed RGB with alpha) -----------

def hex_to_ass(hex_color: str, alpha: int = 0) -> str:
    h = hex_color.lstrip("#")
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    return f"&H{alpha:02X}{b:02X}{g:02X}{r:02X}"


def seconds_to_ass_time(seconds: float) -> str:
    """ASS timestamp: H:MM:SS.cc"""
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs == 100:  # rounding carry
        cs = 0
        s += 1
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def seconds_to_srt_time(seconds: float) -> str:
    """SRT timestamp: HH:MM:SS,mmm"""
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    if ms == 1000:
        ms = 0
        s += 1
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# --- section -> style-family mapping (Studio Step 5 spec) -------------------

def section_family(section_name: str) -> str:
    """Chorus/Outro -> font A family; Verse/Bridge/other -> font B family."""
    n = (section_name or "").strip().lower()
    if n.startswith("chorus") or n.startswith("outro"):
        return "Chorus"
    if n.startswith("bridge"):
        return "Bridge"
    return "Verse"


def style_for(section_name: str, line_style: str) -> str:
    """Map (section, line style) -> concrete ASS style name."""
    fam = section_family(section_name)
    ls = (line_style or "normal").lower()
    if ls == "backing":
        # Backing styles defined per family below.
        return f"{fam}Backing"
    if ls == "shouted":
        return f"{fam}Shouted"
    return f"{fam}Normal"


def build_styles(font_chorus: str, font_verse: str) -> list[str]:
    """Studio aesthetic: white primary, black 5px outline, 6px shadow,
    green italic backing, line-by-line fades. Two font families (A=chorus/outro,
    B=verse/bridge). Sizes per family per Studio Step 5."""
    white = hex_to_ass("#FFFFFF")
    black = hex_to_ass("#000000")
    green = hex_to_ass("#66FF66", alpha=0x40)  # &H4000FF66 equivalent, italic
    # Format columns:
    # Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,
    # BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing,
    # Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV,
    # Encoding
    # Encoding=1 (default/ANSI-by-name) is fine because the file itself is
    # UTF-8+BOM; libass reads glyph names from the font, not this field.
    rows = [
        # Chorus family (font A)
        f"Style: ChorusShouted,{font_chorus},110,{white},{white},{black},{black},-1,0,0,0,100,100,0,0,1,5,6,2,40,40,80,1",
        f"Style: ChorusNormal,{font_chorus},90,{white},{white},{black},{black},-1,0,0,0,100,100,0,0,1,5,6,2,40,40,80,1",
        f"Style: ChorusBacking,{font_chorus},72,{green},{white},{black},{black},-1,1,0,0,100,100,0,0,1,5,6,2,40,40,120,1",
        # Verse family (font B)
        f"Style: VerseShouted,{font_verse},100,{white},{white},{black},{black},-1,0,0,0,100,100,0,0,1,5,6,2,40,40,80,1",
        f"Style: VerseNormal,{font_verse},88,{white},{white},{black},{black},-1,0,0,0,100,100,0,0,1,5,6,2,40,40,80,1",
        f"Style: VerseBacking,{font_verse},72,{green},{white},{black},{black},-1,1,0,0,100,100,0,0,1,5,6,2,40,40,120,1",
        # Bridge family (font B, slightly dimmer via smaller size)
        f"Style: BridgeShouted,{font_verse},96,{white},{white},{black},{black},-1,0,0,0,100,100,0,0,1,5,6,2,40,40,80,1",
        f"Style: BridgeNormal,{font_verse},82,{white},{white},{black},{black},-1,0,0,0,100,100,0,0,1,5,6,2,40,40,80,1",
        f"Style: BridgeBacking,{font_verse},72,{green},{white},{black},{black},-1,1,0,0,100,100,0,0,1,5,6,2,40,40,120,1",
    ]
    return rows


def generate_ass(aligned: dict, output_path: str,
                 font_chorus: str = "Montserrat Bold",
                 font_verse: str = "Montserrat Bold",
                 fade_in_ms: int = 150, fade_out_ms: int = 300) -> int:
    sections = aligned.get("sections", [])

    lines: list[str] = []
    lines.append("[Script Info]")
    lines.append("Title: Lyric Video")
    lines.append("ScriptType: v4.00+")
    lines.append("PlayResX: 1920")
    lines.append("PlayResY: 1080")
    lines.append("WrapStyle: 0")
    lines.append("ScaledBorderAndShadow: yes")
    lines.append("YCbCr Matrix: TV.709")
    lines.append("")

    lines.append("[V4+ Styles]")
    lines.append(
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, "
        "ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, "
        "MarginL, MarginR, MarginV, Encoding"
    )
    lines.extend(build_styles(font_chorus, font_verse))
    lines.append("")

    lines.append("[Events]")
    lines.append(
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, "
        "Effect, Text"
    )

    dialogue_count = 0
    for section in sections:
        if section.get("is_instrumental", False):
            continue
        sec_name = section.get("name", "")
        for line_data in section.get("lines", []):
            start = line_data.get("start")
            end = line_data.get("end")
            text = line_data.get("text", "")
            if start is None or end is None or not str(text).strip():
                continue
            if start == 0 and end == 0:
                continue

            display_start = max(0.0, float(start) - fade_in_ms / 1000)
            display_end = float(end) + fade_out_ms / 1000

            ass_style = style_for(sec_name, line_data.get("style", "normal"))

            # Normalize dashes, then escape ASS-special characters. In ASS the
            # only in-text escapes needed are the literal brace and backslash;
            # a real newline becomes \N (hard line break).
            clean = normalize_dashes(str(text))
            clean = clean.replace("\\", "\\​")  # neutralize stray backslash
            clean = clean.replace("{", "\\{").replace("}", "\\}")
            clean = clean.replace("\r\n", "\n").replace("\n", "\\N")

            fade_tag = f"{{\\fad({fade_in_ms},{fade_out_ms})}}"
            ass_text = f"{fade_tag}{clean}"

            lines.append(
                f"Dialogue: 0,{seconds_to_ass_time(display_start)},"
                f"{seconds_to_ass_time(display_end)},{ass_style},,0,0,0,,{ass_text}"
            )
            dialogue_count += 1

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    # utf-8-sig writes a BOM so libass reliably detects UTF-8. THIS is the bug
    # forge has (it uses plain "utf-8"). Do not change this codec.
    out.write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    return dialogue_count


def generate_srt(aligned: dict, output_path: str) -> int:
    counter = 1
    srt_lines: list[str] = []
    for section in aligned.get("sections", []):
        if section.get("is_instrumental", False):
            continue
        for line_data in section.get("lines", []):
            start = line_data.get("start")
            end = line_data.get("end")
            text = line_data.get("text", "")
            if start is None or end is None or not str(text).strip():
                continue
            if start == 0 and end == 0:
                continue
            srt_lines.append(str(counter))
            srt_lines.append(
                f"{seconds_to_srt_time(float(start))} --> "
                f"{seconds_to_srt_time(float(end))}"
            )
            # SRT keeps the dash normalization too; YouTube CC renders UTF-8.
            srt_lines.append(normalize_dashes(str(text)))
            srt_lines.append("")
            counter += 1

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    # YouTube's SRT parser expects UTF-8; a BOM is tolerated and helps editors
    # that sniff encoding. Match the ASS file for consistency.
    out.write_text("\n".join(srt_lines) + "\n", encoding="utf-8-sig")
    return counter - 1


def main() -> None:
    p = argparse.ArgumentParser(
        description="Generate encoding-correct ASS + SRT for lyric-video-studio."
    )
    p.add_argument("--aligned", required=True, help="Path to aligned_lyrics.json")
    p.add_argument("--ass-output", default="./lyrics.ass")
    p.add_argument("--srt-output", default="./lyrics.srt")
    p.add_argument("--font-chorus", default="Montserrat Bold",
                   help="Font family for Chorus/Outro sections (font A)")
    p.add_argument("--font-verse", default="Montserrat Bold",
                   help="Font family for Verse/Bridge sections (font B)")
    p.add_argument("--fade-in-ms", type=int, default=150)
    p.add_argument("--fade-out-ms", type=int, default=300)
    args = p.parse_args()

    aligned = json.loads(Path(args.aligned).read_text(encoding="utf-8-sig"))

    n_ass = generate_ass(
        aligned, args.ass_output,
        font_chorus=args.font_chorus, font_verse=args.font_verse,
        fade_in_ms=args.fade_in_ms, fade_out_ms=args.fade_out_ms,
    )
    n_srt = generate_srt(aligned, args.srt_output)
    print(f"ASS written (utf-8-sig BOM): {args.ass_output}  [{n_ass} dialogue lines]")
    print(f"SRT written (utf-8-sig BOM): {args.srt_output}  [{n_srt} cues]")


if __name__ == "__main__":
    main()
