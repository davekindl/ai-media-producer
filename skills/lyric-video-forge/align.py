"""
Forced Alignment Engine

Takes ground-truth lyrics + Deepgram word timestamps and aligns them
using dynamic programming (Needleman-Wunsch variant).

User's lyrics = GRAMMAR TRUTH (correct words, spelling, diacritics).
Deepgram response = TIMING TRUTH (when each word is spoken/sung).

Crossmatch: keep user's text, steal Deepgram's timestamps.
"""

import json
import re
from pathlib import Path
from difflib import SequenceMatcher


def normalize_word(word: str) -> str:
    """Strip punctuation, lowercase, collapse whitespace.
    Preserves Hungarian diacritics for better matching."""
    word = re.sub(r'[^\w\sáéíóöőúüű]', '', word.lower().strip())
    return word


def parse_lyrics_file(lyrics_path: str) -> dict:
    """
    Parse a lyrics file with Suno-style structure tags.
    
    Returns structured representation with sections and lines.
    """
    lines = Path(lyrics_path).read_text(encoding="utf-8").splitlines()
    
    sections = []
    current_section = None
    
    # Tags that are structural (contain lyrics below them)
    structure_tags = {
        "intro", "instrumental intro", "verse", "verse 1", "verse 2", "verse 3",
        "verse 4", "pre-chorus", "chorus", "chant", "bridge", "break",
        "interlude", "build", "build-up", "drop", "guitar solo", "outro",
        "fade out", "end", "spoken word", "whispered", "belted",
        "shouted vocals", "male choir", "call and response", "a cappella",
        "scream", "clean vocals", "lead", "choir", "all together",
    }
    
    # Tags that are descriptors (don't contain lyrics)
    descriptor_pattern = re.compile(r'^\[(Energy|Mood|Gravelly Voice|Male Choir).*\]$', re.IGNORECASE)
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Check for structure tag
        tag_match = re.match(r'^\[(.+)\]$', stripped)
        if tag_match:
            tag_content = tag_match.group(1).strip()
            
            # Skip descriptor tags
            if descriptor_pattern.match(stripped):
                continue
            
            # Check if it's a known structure tag (fuzzy match)
            tag_lower = tag_content.lower()
            is_structure = any(tag_lower.startswith(st) for st in structure_tags)
            
            if is_structure:
                current_section = {
                    "tag": tag_content,
                    "lines": [],
                    "is_instrumental": any(kw in tag_lower for kw in ["instrumental", "guitar solo", "interlude"]),
                }
                sections.append(current_section)
                continue
        
        # It's a lyric line
        if current_section is None:
            current_section = {"tag": "Intro", "lines": [], "is_instrumental": False}
            sections.append(current_section)
        
        if current_section.get("is_instrumental"):
            continue  # Skip text under instrumental sections
        
        # Determine line style
        style = "normal"
        if stripped.startswith("(") and stripped.endswith(")"):
            style = "backing"
            stripped = stripped[1:-1]  # Remove parens for alignment
        elif stripped.isupper() and len(stripped) > 3:
            style = "shouted"
        elif "..." in stripped:
            style = "pause"
        
        # Extract words
        words = [w for w in stripped.split() if w]
        if words:
            current_section["lines"].append({
                "text": stripped,
                "style": style,
                "words": words,
            })
    
    return {"sections": sections}


def align_lyrics_to_timestamps(parsed_lyrics: dict, timestamps: dict, confidence_threshold: float = 0.7) -> dict:
    """
    Forced alignment: match parsed lyrics to Deepgram word timestamps.
    
    Uses SequenceMatcher for fuzzy matching, then transfers timestamps
    from transcription words to lyric words.
    """
    # Flatten lyrics into word list with metadata
    lyric_words = []
    for s_idx, section in enumerate(parsed_lyrics["sections"]):
        for l_idx, line in enumerate(section["lines"]):
            for w_idx, word in enumerate(line["words"]):
                lyric_words.append({
                    "word": word,
                    "normalized": normalize_word(word),
                    "section_idx": s_idx,
                    "line_idx": l_idx,
                    "word_idx": w_idx,
                })
    
    # Flatten transcript words
    ts_words = timestamps["words"]
    ts_normalized = [normalize_word(w["word"]) for w in ts_words]
    
    # Build alignment using SequenceMatcher on normalized word sequences
    lyric_normalized = [w["normalized"] for w in lyric_words]
    
    matcher = SequenceMatcher(None, lyric_normalized, ts_normalized)
    
    # Create alignment map: lyric_word_idx -> timestamp_word_idx
    alignment = {}
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            for offset in range(i2 - i1):
                alignment[i1 + offset] = j1 + offset
        elif op == "replace":
            # Try to match by position within the replacement block
            lyric_len = i2 - i1
            ts_len = j2 - j1
            for offset in range(min(lyric_len, ts_len)):
                # Only align if words are somewhat similar
                sim = SequenceMatcher(None, lyric_normalized[i1 + offset], ts_normalized[j1 + offset]).ratio()
                if sim > 0.5:
                    alignment[i1 + offset] = j1 + offset
    
    # Transfer timestamps and build output
    flagged = []
    aligned_sections = []
    
    for s_idx, section in enumerate(parsed_lyrics["sections"]):
        aligned_lines = []
        section_start = None
        section_end = None
        
        for l_idx, line in enumerate(section["lines"]):
            aligned_words = []
            line_start = None
            line_end = None
            
            for w_idx, word in enumerate(line["words"]):
                # Find this word in our flat list
                flat_idx = None
                for fi, fw in enumerate(lyric_words):
                    if fw["section_idx"] == s_idx and fw["line_idx"] == l_idx and fw["word_idx"] == w_idx:
                        flat_idx = fi
                        break
                
                if flat_idx is not None and flat_idx in alignment:
                    ts_idx = alignment[flat_idx]
                    ts_word = ts_words[ts_idx]
                    
                    word_data = {
                        "word": word,
                        "start": ts_word["start"],
                        "end": ts_word["end"],
                        "confidence": ts_word["confidence"],
                    }
                    
                    if ts_word["confidence"] < confidence_threshold:
                        flagged.append({
                            "word": word,
                            "section": section["tag"],
                            "line": l_idx + 1,
                            "confidence": ts_word["confidence"],
                            "timestamp": ts_word["start"],
                            "reason": "low_confidence",
                        })
                    
                    if line_start is None:
                        line_start = ts_word["start"]
                    line_end = ts_word["end"]
                    
                else:
                    # No alignment found — interpolate later
                    word_data = {
                        "word": word,
                        "start": None,
                        "end": None,
                        "confidence": 0,
                    }
                    flagged.append({
                        "word": word,
                        "section": section["tag"],
                        "line": l_idx + 1,
                        "confidence": 0,
                        "timestamp": None,
                        "reason": "no_alignment",
                    })
                
                aligned_words.append(word_data)
            
            # Interpolate missing timestamps
            _interpolate_gaps(aligned_words)
            
            if line_start is None and aligned_words:
                line_start = aligned_words[0].get("start", 0)
            if line_end is None and aligned_words:
                line_end = aligned_words[-1].get("end", 0)
            
            aligned_lines.append({
                "text": line["text"],
                "style": line["style"],
                "start": line_start or 0,
                "end": line_end or 0,
                "words": aligned_words,
            })
            
            if section_start is None and line_start:
                section_start = line_start
            if line_end:
                section_end = line_end
        
        aligned_sections.append({
            "tag": section["tag"],
            "start": section_start or 0,
            "end": section_end or 0,
            "is_instrumental": section.get("is_instrumental", False),
            "lines": aligned_lines,
        })
    
    # Stats
    total_words = len(lyric_words)
    aligned_count = len(alignment)
    alignment_rate = aligned_count / max(total_words, 1)
    
    return {
        "sections": aligned_sections,
        "flagged": flagged,
        "stats": {
            "total_lyric_words": total_words,
            "aligned_words": aligned_count,
            "alignment_rate": f"{alignment_rate:.1%}",
            "flagged_count": len(flagged),
            "duration": timestamps.get("duration", 0),
        }
    }


def _interpolate_gaps(words: list):
    """Fill in missing timestamps by interpolating from neighbors."""
    # Forward pass: inherit start from previous word's end
    for i in range(1, len(words)):
        if words[i]["start"] is None and words[i-1]["end"] is not None:
            gap = 0.05  # 50ms gap between words
            words[i]["start"] = words[i-1]["end"] + gap
    
    # Backward pass: inherit end from next word's start
    for i in range(len(words) - 2, -1, -1):
        if words[i]["end"] is None and words[i+1]["start"] is not None:
            words[i]["end"] = words[i+1]["start"] - 0.05
    
    # Estimate duration for still-missing words
    avg_duration = 0.3  # Default word duration
    known_durations = [w["end"] - w["start"] for w in words if w["start"] is not None and w["end"] is not None]
    if known_durations:
        avg_duration = sum(known_durations) / len(known_durations)
    
    for w in words:
        if w["start"] is not None and w["end"] is None:
            w["end"] = w["start"] + avg_duration
        elif w["end"] is not None and w["start"] is None:
            w["start"] = w["end"] - avg_duration
        # If both still None, leave for manual fix


def crossmatch_with_structure(
    clean_lyrics_path: str,
    timestamps: dict,
    structure_map: list[dict],
    confidence_threshold: float = 0.7,
) -> dict:
    """
    Enhanced crossmatch: user's clean lyrics = grammar truth,
    Deepgram = timing truth, structure_map = section/energy metadata.

    For each line in clean_lyrics, find the corresponding Deepgram
    timestamp window. Per-word: keep user's spelling, steal Deepgram's timing.
    Instrumental sections in structure_map are skipped.

    Returns aligned_lyrics.json format with section references and energy levels.
    """
    clean_text = Path(clean_lyrics_path).read_text(encoding="utf-8")
    clean_lines = [l for l in clean_text.splitlines() if l.strip()]

    ts_words = timestamps["words"]
    ts_normalized = [normalize_word(w["word"]) for w in ts_words]

    # Build section-to-lyrics mapping from structure_map
    section_lyrics = []
    for section in structure_map:
        if section["type"] == "instrumental":
            continue
        for lyric_line in section["lyrics"]:
            section_lyrics.append({
                "text": lyric_line,
                "section": section["section"],
                "energy": section["energy"],
            })

    # Flatten user lyrics into word list with section metadata
    lyric_words = []
    for sl_idx, sl in enumerate(section_lyrics):
        words = sl["text"].split()
        for w_idx, word in enumerate(words):
            lyric_words.append({
                "word": word,
                "normalized": normalize_word(word),
                "section": sl["section"],
                "energy": sl["energy"],
                "line_idx": sl_idx,
                "word_idx": w_idx,
            })

    lyric_normalized = [w["normalized"] for w in lyric_words]

    # Sequence match: user words vs Deepgram words
    matcher = SequenceMatcher(None, lyric_normalized, ts_normalized)

    alignment = {}
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            for offset in range(i2 - i1):
                alignment[i1 + offset] = j1 + offset
        elif op == "replace":
            lyric_len = i2 - i1
            ts_len = j2 - j1
            for offset in range(min(lyric_len, ts_len)):
                sim = SequenceMatcher(
                    None,
                    lyric_normalized[i1 + offset],
                    ts_normalized[j1 + offset]
                ).ratio()
                if sim > 0.5:
                    alignment[i1 + offset] = j1 + offset

    # Build output with section awareness
    flagged = []
    result_words = []
    result_sections = []

    # Track section timing
    current_section = None
    section_start = None
    section_end = None

    for i, lw in enumerate(lyric_words):
        # Section boundary tracking
        if lw["section"] != current_section:
            if current_section is not None:
                result_sections.append({
                    "name": current_section,
                    "start": section_start or 0,
                    "end": section_end or 0,
                    "energy": prev_energy,
                    "type": "vocal",
                })
            current_section = lw["section"]
            prev_energy = lw["energy"]
            section_start = None
            section_end = None

        if i in alignment:
            ts_idx = alignment[i]
            ts_word = ts_words[ts_idx]

            word_data = {
                "text": lw["word"],  # User's spelling (grammar truth)
                "start": ts_word["start"],  # Deepgram's timing (timing truth)
                "end": ts_word["end"],
                "section": lw["section"],
                "energy": lw["energy"],
                "confidence": ts_word["confidence"],
            }

            if ts_word["confidence"] < confidence_threshold:
                flagged.append({
                    "word": lw["word"],
                    "section": lw["section"],
                    "line": lw["line_idx"] + 1,
                    "confidence": ts_word["confidence"],
                    "reason": "low_confidence",
                })

            if section_start is None:
                section_start = ts_word["start"]
            section_end = ts_word["end"]
        else:
            word_data = {
                "text": lw["word"],
                "start": None,
                "end": None,
                "section": lw["section"],
                "energy": lw["energy"],
                "confidence": 0,
            }
            flagged.append({
                "word": lw["word"],
                "section": lw["section"],
                "line": lw["line_idx"] + 1,
                "confidence": 0,
                "reason": "no_alignment",
            })

        result_words.append(word_data)

    # Flush last section
    if current_section is not None:
        result_sections.append({
            "name": current_section,
            "start": section_start or 0,
            "end": section_end or 0,
            "energy": prev_energy,
            "type": "vocal",
        })

    # Add instrumental sections from structure_map
    for section in structure_map:
        if section["type"] == "instrumental":
            result_sections.append({
                "name": section["section"],
                "start": 0,  # Will be estimated from surrounding vocals
                "end": 0,
                "energy": section["energy"],
                "type": "instrumental",
            })

    # Interpolate missing timestamps
    _interpolate_word_gaps(result_words)

    # Sort sections by start time
    result_sections.sort(key=lambda s: s["start"])

    total_words = len(lyric_words)
    aligned_count = len(alignment)

    return {
        "words": result_words,
        "sections": result_sections,
        "flagged": flagged,
        "stats": {
            "total_lyric_words": total_words,
            "aligned_words": aligned_count,
            "alignment_rate": f"{aligned_count / max(total_words, 1):.1%}",
            "flagged_count": len(flagged),
            "duration": timestamps.get("duration", 0),
        }
    }


def _interpolate_word_gaps(words: list):
    """Fill in missing timestamps in the flat word list."""
    for i in range(1, len(words)):
        if words[i]["start"] is None and words[i-1]["end"] is not None:
            words[i]["start"] = words[i-1]["end"] + 0.05

    for i in range(len(words) - 2, -1, -1):
        if words[i]["end"] is None and words[i+1]["start"] is not None:
            words[i]["end"] = words[i+1]["start"] - 0.05

    known = [w["end"] - w["start"] for w in words
             if w["start"] is not None and w["end"] is not None]
    avg = sum(known) / len(known) if known else 0.3

    for w in words:
        if w["start"] is not None and w["end"] is None:
            w["end"] = w["start"] + avg
        elif w["end"] is not None and w["start"] is None:
            w["start"] = w["end"] - avg


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Align lyrics to audio timestamps")
    parser.add_argument("--lyrics", required=True, help="Path to lyrics text file (raw or clean)")
    parser.add_argument("--timestamps", required=True, help="Path to Deepgram timestamps JSON")
    parser.add_argument("--structure-map", dest="structure_map", help="Path to structure_map.json (enables crossmatch mode)")
    parser.add_argument("--output", default="./output/aligned_lyrics.json")
    parser.add_argument("--confidence", type=float, default=0.7, help="Confidence threshold for flagging")
    args = parser.parse_args()

    ts = json.loads(Path(args.timestamps).read_text())

    if args.structure_map:
        # New crossmatch mode
        sm = json.loads(Path(args.structure_map).read_text())
        aligned = crossmatch_with_structure(args.lyrics, ts, sm, args.confidence)
    else:
        # Legacy mode
        parsed = parse_lyrics_file(args.lyrics)
        aligned = align_lyrics_to_timestamps(parsed, ts, args.confidence)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(aligned, indent=2, ensure_ascii=False))

    print(f"\nAlignment complete:")
    print(f"  Words: {aligned['stats']['total_lyric_words']}")
    print(f"  Aligned: {aligned['stats']['aligned_words']} ({aligned['stats']['alignment_rate']})")
    print(f"  Flagged: {aligned['stats']['flagged_count']}")
    if aligned["flagged"]:
        print(f"\n  Flagged words:")
        for f in aligned["flagged"][:10]:
            print(f"    '{f['word']}' in {f['section']} line {f['line']} — {f['reason']}")
