"""
ASS (Advanced SubStation Alpha) Subtitle Generator

Converts aligned lyrics JSON into a styled ASS subtitle file
with word-by-word karaoke highlighting.
"""

import json
import math
from pathlib import Path


def seconds_to_ass_time(seconds: float) -> str:
    """Convert seconds to ASS timestamp format: H:MM:SS.cc"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds % 1) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def generate_ass(aligned_lyrics: dict, config: dict, output_path: str):
    """
    Generate ASS subtitle file from aligned lyrics.
    
    config should contain font/color/effect settings.
    """
    sections = aligned_lyrics["sections"]
    
    # Extract config values with defaults
    font_cfg = config.get("font", {})
    effects_cfg = config.get("effects", {})
    display_mode = config.get("display_mode", "karaoke")
    
    font_family = font_cfg.get("family", "Montserrat Bold")
    font_size = font_cfg.get("size_normal", 64)
    font_size_shouted = font_cfg.get("size_shouted", 80)
    font_size_backing = font_cfg.get("size_backing", 48)
    
    # ASS colors are in &HAABBGGRR format (reversed from RGB, with alpha)
    color_inactive = font_cfg.get("color_inactive", "#CCCCCC")
    color_active = font_cfg.get("color_active", "#FFFFFF")
    color_highlight = font_cfg.get("color_highlight", "#FFD700")
    
    shadow = font_cfg.get("shadow", True)
    shadow_color = font_cfg.get("shadow_color", "#000000")
    shadow_offset = font_cfg.get("shadow_offset", 3)
    
    fade_in_ms = effects_cfg.get("line_fade_in_ms", 300)
    fade_out_ms = effects_cfg.get("line_fade_out_ms", 500)
    backing_opacity = effects_cfg.get("backing_vocal_opacity", 0.6)
    
    # Convert hex colors to ASS format (&H00BBGGRR)
    def hex_to_ass(hex_color: str, alpha: int = 0) -> str:
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"&H{alpha:02X}{b:02X}{g:02X}{r:02X}"
    
    ass_inactive = hex_to_ass(color_inactive)
    ass_active = hex_to_ass(color_active)
    ass_highlight = hex_to_ass(color_highlight)
    ass_shadow = hex_to_ass(shadow_color)
    ass_backing = hex_to_ass(color_inactive, int(255 * (1 - backing_opacity)))
    
    # Build ASS file
    lines = []
    
    # Script info
    lines.append("[Script Info]")
    lines.append("Title: Lyric Video")
    lines.append("ScriptType: v4.00+")
    lines.append("PlayResX: 1920")
    lines.append("PlayResY: 1080")
    lines.append("WrapStyle: 0")
    lines.append("ScaledBorderAndShadow: yes")
    lines.append("")
    
    # Styles
    lines.append("[V4+ Styles]")
    lines.append("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding")
    
    # Default style (normal lyrics)
    shadow_val = shadow_offset if shadow else 0
    lines.append(
        f"Style: Default,{font_family},{font_size},{ass_inactive},{ass_highlight},{ass_shadow},{ass_shadow},"
        f"-1,0,0,0,100,100,0,0,1,3,{shadow_val},2,40,40,80,1"
    )
    
    # Shouted style (bigger, bolder)
    lines.append(
        f"Style: Shouted,{font_family},{font_size_shouted},{ass_active},{ass_highlight},{ass_shadow},{ass_shadow},"
        f"-1,0,0,0,100,100,2,0,1,4,{shadow_val},2,40,40,80,1"
    )
    
    # Backing vocal style (smaller, semi-transparent)
    lines.append(
        f"Style: Backing,{font_family},{font_size_backing},{ass_backing},{ass_highlight},{ass_shadow},{ass_shadow},"
        f"-1,1,0,0,100,100,0,0,1,2,{shadow_val},2,40,40,120,1"
    )
    
    lines.append("")
    
    # Events
    lines.append("[Events]")
    lines.append("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")
    
    for section in sections:
        if section.get("is_instrumental", False):
            continue
        
        for line_data in section["lines"]:
            start = line_data.get("start", 0)
            end = line_data.get("end", 0)
            words = line_data.get("words", [])
            style_name = line_data.get("style", "normal")
            
            if not words or start == 0 and end == 0:
                continue
            
            # Add padding for fade
            display_start = max(0, start - fade_in_ms / 1000)
            display_end = end + fade_out_ms / 1000
            
            ass_start = seconds_to_ass_time(display_start)
            ass_end = seconds_to_ass_time(display_end)
            
            # Select style
            if style_name == "shouted":
                ass_style = "Shouted"
            elif style_name == "backing":
                ass_style = "Backing"
            else:
                ass_style = "Default"
            
            # Build text with effects
            fade_tag = f"\\fad({fade_in_ms},{fade_out_ms})"
            
            if display_mode == "karaoke":
                # Word-by-word karaoke highlighting
                text_parts = [f"{{{fade_tag}}}"]
                for w in words:
                    # \k duration is in centiseconds
                    w_start = w.get("start") or start
                    w_end = w.get("end") or (w_start + 0.3 if w_start else start + 0.3)
                    duration_cs = max(1, int((w_end - w_start) * 100))
                    
                    # \kf = smooth fill, \k = instant highlight
                    text_parts.append(f"{{\\kf{duration_cs}}}{w['word']} ")
                
                text = "".join(text_parts).rstrip()
                
            elif display_mode == "line_by_line":
                # Full line appears at once
                text = f"{{{fade_tag}}}{line_data['text']}"
                
            elif display_mode == "hybrid":
                # Line appears, then words highlight within
                text_parts = [f"{{{fade_tag}}}"]
                for w in words:
                    w_start = w.get("start", start)
                    w_end = w.get("end", w_start + 0.3)
                    duration_cs = max(1, int((w_end - w_start) * 100))
                    text_parts.append(f"{{\\kf{duration_cs}}}{w['word']} ")
                text = "".join(text_parts).rstrip()
            
            else:
                text = f"{{{fade_tag}}}{line_data['text']}"
            
            lines.append(f"Dialogue: 0,{ass_start},{ass_end},{ass_style},,0,0,0,,{text}")
    
    # Write file
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Generated ASS subtitle file: {output_path}")
    print(f"  Total dialogue lines: {sum(1 for l in lines if l.startswith('Dialogue:'))}")


def generate_srt(aligned_lyrics: dict, output_path: str):
    """Also generate a plain SRT file for YouTube CC upload."""
    counter = 1
    srt_lines = []
    
    for section in aligned_lyrics["sections"]:
        if section.get("is_instrumental", False):
            continue
        for line_data in section["lines"]:
            start = line_data.get("start", 0)
            end = line_data.get("end", 0)
            text = line_data.get("text", "")
            
            if not text or (start == 0 and end == 0):
                continue
            
            srt_start = _seconds_to_srt(start)
            srt_end = _seconds_to_srt(end)
            
            srt_lines.append(str(counter))
            srt_lines.append(f"{srt_start} --> {srt_end}")
            srt_lines.append(text)
            srt_lines.append("")
            counter += 1
    
    Path(output_path).write_text("\n".join(srt_lines), encoding="utf-8")
    print(f"  Generated SRT subtitle file: {output_path}")


def _seconds_to_srt(seconds: float) -> str:
    """Convert seconds to SRT format: HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate ASS/SRT from aligned lyrics")
    parser.add_argument("--aligned", required=True, help="Path to aligned_lyrics.json")
    parser.add_argument("--config", required=True, help="Path to style_config.json")
    parser.add_argument("--ass-output", default="./output/lyrics.ass")
    parser.add_argument("--srt-output", default="./output/lyrics.srt")
    args = parser.parse_args()
    
    aligned = json.loads(Path(args.aligned).read_text())
    config = json.loads(Path(args.config).read_text())
    
    generate_ass(aligned, config, args.ass_output)
    generate_srt(aligned, args.srt_output)
