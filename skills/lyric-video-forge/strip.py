"""
Lyric Stripper — Clean raw Suno-tagged lyrics into two outputs:
  A) clean_lyrics.txt — only singable/speakable words
  B) structure_map.json — section/energy/type metadata

Handles Hungarian diacritics, extended vowels, ALL CAPS,
and Suno production tags.
"""

import json
import re
from pathlib import Path


# Energy keywords mapped to levels
ENERGY_MAP = {
    # Explicit energy tags
    "energy: low": 1,
    "energy: medium": 2,
    "energy: high": 4,
    "energy: maximum": 5,
    # Section-type defaults
    "intro": 1,
    "instrumental intro": 1,
    "outro": 1,
    "fade out": 1,
    "end": 1,
    "breakdown": 1,
    "spoken word": 1,
    "whispered": 1,
    "verse": 2,
    "gregorian chant": 2,
    "male choir": 2,
    "choir": 2,
    "clean vocals": 2,
    "a cappella": 2,
    "bridge": 2,
    "pre-chorus": 3,
    "build": 3,
    "build-up": 3,
    "chant": 3,
    "call and response": 3,
    "chorus": 3,
    "belted": 4,
    "shouted vocals": 4,
    "scream": 4,
    "drop": 5,
    "final drop": 5,
}

# Patterns that indicate instrumental (no singable lyrics)
INSTRUMENTAL_KEYWORDS = {
    "instrumental", "guitar solo", "interlude", "instrumental intro",
    "instrumental outro", "instrumental break", "solo",
}

# Tags that are purely structural or descriptive (not lyrics)
TAG_PATTERN = re.compile(r'^\[(.+)\]$')

# Parenthetical production notes (not lyrics)
PAREN_PRODUCTION = re.compile(r'^\(.*\)$')

# Check if a parenthetical is a production note vs backing vocals
# Production notes describe sounds/instruments, not words to sing
PRODUCTION_INDICATORS = [
    "humming", "chanting", "enters", "builds", "fade", "reverb",
    "echo", "saw", "synth", "bass", "drums", "percussion",
    "monks", "choir hums", "instrumental", "silence", "pause",
    "breath", "growl", "scream sfx", "fx", "effect",
]


def is_production_note(text: str) -> bool:
    """Check if parenthetical text is a production note vs backing vocals."""
    inner = text.strip("()")
    lower = inner.lower()
    return any(indicator in lower for indicator in PRODUCTION_INDICATORS)


def detect_energy(tag_lower: str, section_lyrics: list[str]) -> int:
    """Detect energy level from tag name and lyrics content."""
    # Check explicit energy tags first
    for key, level in ENERGY_MAP.items():
        if key in tag_lower:
            energy = level
            break
    else:
        # Default based on section type
        energy = 2

    # ALL CAPS lyrics in section bump energy +1
    caps_count = sum(1 for line in section_lyrics if line.isupper() and len(line) > 3)
    if caps_count > 0 and energy < 5:
        energy = min(energy + 1, 5)

    return energy


def detect_section_type(tag_lower: str, lyrics: list[str]) -> str:
    """Determine if section is vocal or instrumental."""
    if any(kw in tag_lower for kw in INSTRUMENTAL_KEYWORDS):
        return "instrumental"
    if not lyrics:
        return "instrumental"
    return "vocal"


def strip_lyrics(raw_text: str) -> tuple[str, list[dict]]:
    """
    Strip raw Suno-tagged lyrics into clean text and structure map.

    Returns:
        (clean_lyrics_text, structure_map_list)
    """
    lines = raw_text.splitlines()

    structure_map = []
    clean_lines = []
    current_tag = "Intro"
    current_lyrics = []
    line_counter = 0

    def flush_section():
        nonlocal current_tag, current_lyrics, line_counter
        if current_tag is None:
            return

        tag_lower = current_tag.lower()
        section_type = detect_section_type(tag_lower, current_lyrics)
        energy = detect_energy(tag_lower, current_lyrics)

        start_line = line_counter - len(current_lyrics)
        end_line = line_counter - 1 if current_lyrics else start_line

        structure_map.append({
            "section": current_tag,
            "energy": energy,
            "type": section_type,
            "start_line": start_line,
            "end_line": end_line,
            "lyrics": list(current_lyrics),
        })
        current_lyrics = []

    for raw_line in lines:
        stripped = raw_line.strip()

        # Skip empty lines
        if not stripped:
            continue

        # Check for bracketed tag
        tag_match = TAG_PATTERN.match(stripped)
        if tag_match:
            # Flush previous section
            flush_section()
            current_tag = tag_match.group(1).strip()
            current_lyrics = []
            continue

        # Check for parenthetical production notes
        if PAREN_PRODUCTION.match(stripped):
            if is_production_note(stripped):
                continue  # Skip production notes entirely
            else:
                # It's backing vocals — strip parens, keep words
                inner = stripped[1:-1].strip()
                if inner:
                    current_lyrics.append(inner)
                    clean_lines.append(inner)
                    line_counter += 1
                continue

        # Check if line is purely instrumental direction (no actual words)
        # These are lines like "super saw enters" that aren't in brackets/parens
        lower = stripped.lower()
        if any(stripped.lower().startswith(ind) for ind in PRODUCTION_INDICATORS):
            continue

        # It's a lyric line — keep it
        current_lyrics.append(stripped)
        clean_lines.append(stripped)
        line_counter += 1

    # Flush last section
    flush_section()

    # Build clean text: collapse multiple blank lines, add section breaks
    clean_text = "\n".join(clean_lines)
    # Add blank lines between groups of lyrics (where sections break)
    # We'll reconstruct with section-aware spacing
    clean_output = []
    for section in structure_map:
        if section["lyrics"]:
            if clean_output:
                clean_output.append("")  # Blank line between sections
            clean_output.extend(section["lyrics"])

    return "\n".join(clean_output), structure_map


def strip_lyrics_file(input_path: str, output_dir: str) -> tuple[str, str]:
    """
    Strip lyrics from file, write clean_lyrics.txt and structure_map.json.

    Returns (clean_lyrics_path, structure_map_path).
    """
    raw_text = Path(input_path).read_text(encoding="utf-8")
    clean_text, structure_map = strip_lyrics(raw_text)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    clean_path = out / "clean_lyrics.txt"
    clean_path.write_text(clean_text, encoding="utf-8")

    map_path = out / "structure_map.json"
    map_path.write_text(json.dumps(structure_map, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"  Clean lyrics: {clean_path} ({len(clean_text.splitlines())} lines)")
    print(f"  Structure map: {map_path} ({len(structure_map)} sections)")

    return str(clean_path), str(map_path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Strip Suno tags from lyrics")
    parser.add_argument("--input", required=True, help="Path to raw lyrics file")
    parser.add_argument("--output", default="./output", help="Output directory")
    args = parser.parse_args()

    clean_path, map_path = strip_lyrics_file(args.input, args.output)

    # Display structure map summary
    sm = json.loads(Path(map_path).read_text(encoding="utf-8"))
    print(f"\nStructure map ({len(sm)} sections):")
    for s in sm:
        lyric_count = len(s["lyrics"])
        print(f"  [{s['section']}] energy={s['energy']} type={s['type']} lines={lyric_count}")
