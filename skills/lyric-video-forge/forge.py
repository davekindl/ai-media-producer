#!/usr/bin/env python3
"""
LYRIC VIDEO FORGE — Main Pipeline Orchestrator

End-to-end lyric video generation with human approval gates.
Run: python3 forge.py --audio song.mp3 --lyrics lyrics.txt [options]
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import math
import tempfile
from pathlib import Path

# Add scripts dir to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from kie_client import generate_image, generate_keyframes
from deepgram_client import transcribe_audio, save_timestamps
from align import parse_lyrics_file, align_lyrics_to_timestamps, crossmatch_with_structure
from ass_generator import generate_ass, generate_srt
from strip import strip_lyrics_file
from world_build import build_constitution, reduce_keyframes, save_constitution
from loop_planner import plan_loops, save_loop_plan


# ─── Default Style Config ────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "display_mode": "karaoke",
    "font": {
        "family": "Montserrat-Bold",
        "size_normal": 64,
        "size_shouted": 80,
        "size_backing": 48,
        "color_inactive": "#CCCCCC",
        "color_active": "#FFFFFF",
        "color_highlight": "#FFD700",
        "shadow": True,
        "shadow_color": "#000000",
        "shadow_offset": 3
    },
    "background": {
        "ken_burns": True,
        "zoom_start": 1.0,
        "zoom_end": 1.08,
        "zoom_style": "slow_zoom_in",
        "pan_direction": "none"
    },
    "effects": {
        "line_fade_in_ms": 300,
        "line_fade_out_ms": 500,
        "highlight_style": "word_by_word_fill",
        "section_transition": "fade_black_500ms",
        "backing_vocal_opacity": 0.6
    },
    "loop": {
        "enabled": True,
        "copies": 3,
        "crossfade_ms": 2000,
        "background_shift_per_copy": True
    },
    "output": {
        "resolution": "1920x1080",
        "fps": 30,
        "codec": "libx264",
        "audio_codec": "aac",
        "bitrate": "8M",
        "crf": 18
    }
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def gate(gate_num: int, message: str, auto: bool = False) -> bool:
    """Approval gate. Returns True to proceed, False to retry/abort."""
    print(f"\n{'='*60}")
    print(f"  GATE {gate_num}: {message}")
    print(f"{'='*60}")
    
    if auto:
        print("  [AUTO MODE] Proceeding automatically.")
        return True
    
    while True:
        choice = input("\n  [A]pprove / [R]etry / [S]kip / [Q]uit → ").strip().upper()
        if choice in ("A", "APPROVE", "Y", "YES", ""):
            return True
        elif choice in ("R", "RETRY"):
            return False
        elif choice in ("S", "SKIP"):
            print("  Skipping this step.")
            return True
        elif choice in ("Q", "QUIT"):
            print("  Aborting pipeline.")
            sys.exit(0)
        else:
            print("  Invalid choice. Enter A, R, S, or Q.")


def run_ffmpeg(cmd: list, description: str = ""):
    """Run an FFmpeg command with error handling."""
    if description:
        print(f"\n  FFmpeg: {description}")
    
    full_cmd = ["ffmpeg", "-y"] + cmd
    print(f"  Command: {' '.join(full_cmd[:6])}...")
    
    result = subprocess.run(
        full_cmd,
        capture_output=True,
        text=True,
        timeout=600  # 10 min timeout
    )
    
    if result.returncode != 0:
        print(f"  ERROR: FFmpeg failed!")
        print(f"  stderr: {result.stderr[-500:]}")
        raise RuntimeError(f"FFmpeg failed: {result.stderr[-200:]}")
    
    return result


def get_audio_duration(audio_path: str) -> float:
    """Get audio duration in seconds via ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def check_font(font_name: str) -> str:
    """Check if a font is available (Linux/macOS via fc-list).

    fontconfig (fc-list) is not present on Windows by default, so we cannot
    reliably enumerate fonts there — trust the requested font and let ffmpeg
    resolve it. Only when fc-list IS available and reports nothing do we fall
    back to a guaranteed-available font.
    """
    if not shutil.which("fc-list"):
        # No fontconfig (typical on Windows). Trust the caller's font.
        return font_name

    result = subprocess.run(
        ["fc-list", f":family={font_name}"],
        capture_output=True, text=True
    )
    if result.stdout.strip():
        return font_name

    print(f"  WARNING: Font '{font_name}' not found. Falling back to DejaVu Sans Bold.")
    return "DejaVu Sans Bold"


# ─── Pipeline Steps ──────────────────────────────────────────────────────────

def step1_parse_lyrics(lyrics_path: str, work_dir: Path) -> dict:
    """Step 1: Parse lyrics file into structured JSON."""
    print("\n" + "─"*60)
    print("  STEP 1: Parsing lyrics...")
    print("─"*60)

    parsed = parse_lyrics_file(lyrics_path)

    # Display summary
    total_lines = sum(len(s["lines"]) for s in parsed["sections"])
    total_words = sum(len(w) for s in parsed["sections"] for l in s["lines"] for w in [l["words"]])

    print(f"\n  Sections found: {len(parsed['sections'])}")
    for s in parsed["sections"]:
        line_count = len(s["lines"])
        instrumental = " (INSTRUMENTAL)" if s.get("is_instrumental") else ""
        print(f"    [{s['tag']}] — {line_count} lines{instrumental}")
    print(f"  Total lyric lines: {total_lines}")
    print(f"  Total words: {total_words}")

    # Save parsed output
    parsed_path = work_dir / "parsed_lyrics.json"
    parsed_path.write_text(json.dumps(parsed, indent=2))

    return parsed


def step1a_strip_lyrics(lyrics_path: str, work_dir: Path) -> tuple[str, list]:
    """Step 1a: Strip raw lyrics into clean text + structure map."""
    print("\n" + "─"*60)
    print("  STEP 1a: Stripping lyrics (clean text + structure map)...")
    print("─"*60)

    clean_path, map_path = strip_lyrics_file(lyrics_path, str(work_dir))

    structure_map = json.loads(Path(map_path).read_text())

    # Display structure summary
    print(f"\n  Structure map ({len(structure_map)} sections):")
    for s in structure_map:
        type_label = "INST" if s["type"] == "instrumental" else f"E{s['energy']}"
        lyric_count = len(s["lyrics"])
        print(f"    [{s['section']}] {type_label} — {lyric_count} lines")

    return clean_path, structure_map


def step2_keyframes(
    constitution: dict,
    work_dir: Path,
    variations: int = 3,
    auto: bool = False,
) -> dict[str, str]:
    """Step 2 (keyframe mode): Generate 5 tiers x N variations of keyframe images.

    Returns dict mapping tier -> chosen image path.
    """
    print("\n" + "─"*60)
    print("  STEP 2: Generating keyframe images...")
    print("─"*60)

    images_dir = str(work_dir / "keyframes")
    results = generate_keyframes(constitution, images_dir, variations)

    if not results:
        print("  ERROR: No keyframe images generated.")
        return {}

    if auto:
        # Auto-select first variation per tier
        chosen = {}
        for tier, paths in sorted(results.items()):
            if paths:
                chosen[tier] = paths[0]
                print(f"  Auto-selected: frame_{tier}_v1")
        return chosen

    # Present all images grouped by tier for user selection
    chosen = {}
    for tier in sorted(results.keys()):
        paths = results[tier]
        print(f"\n  Tier {tier} ({len(paths)} variations):")
        for i, p in enumerate(paths):
            print(f"    [{i+1}] {Path(p).name}")

        while True:
            choice = input(f"  Pick best for tier {tier} [1-{len(paths)}] → ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(paths):
                    chosen[tier] = paths[idx]
                    # Copy to canonical name
                    dest = work_dir / "keyframes" / f"frame_{tier}.png"
                    shutil.copy2(paths[idx], dest)
                    break
            except ValueError:
                pass
            print("  Invalid choice.")

    return chosen


def step2_background(image_prompt: str, image_path: str, work_dir: Path, auto: bool = False) -> str:
    """Step 2: Generate or load background image."""
    print("\n" + "─"*60)
    print("  STEP 2: Background image...")
    print("─"*60)
    
    if image_path and Path(image_path).exists():
        print(f"  Using provided image: {image_path}")
        dest = work_dir / "background.png"
        shutil.copy2(image_path, dest)
        return str(dest)
    
    if not image_prompt:
        image_prompt = "dark cinematic background, dramatic lighting, abstract, 4K wallpaper"
        print(f"  No image prompt provided. Using default: {image_prompt}")
    
    print(f"  Generating 3 background images via kie.ai...")
    images_dir = str(work_dir / "images")
    files = generate_image(image_prompt, images_dir, 1920, 1080, 3)
    
    if not files:
        print("  ERROR: No images generated. Please provide an image manually.")
        sys.exit(1)
    
    if auto:
        chosen = files[0]
    else:
        print(f"\n  Generated {len(files)} images:")
        for i, f in enumerate(files):
            print(f"    [{i+1}] {f}")
        
        while True:
            choice = input(f"\n  Pick an image [1-{len(files)}] or [R]egenerate → ").strip()
            if choice.upper() == "R":
                return None  # Signal to retry
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(files):
                    chosen = files[idx]
                    break
            except ValueError:
                pass
            print("  Invalid choice.")
    
    dest = work_dir / "background.png"
    shutil.copy2(chosen, dest)
    print(f"  Selected: {dest}")
    return str(dest)


def step3_transcribe(audio_path: str, language: str, work_dir: Path) -> dict:
    """Step 3: Transcribe audio with Deepgram Nova-3."""
    print("\n" + "─"*60)
    print("  STEP 3: Transcribing audio (Deepgram Nova-3)...")
    print("─"*60)
    
    result = transcribe_audio(audio_path, language)
    
    ts_path = work_dir / "timestamps.json"
    save_timestamps(result, str(ts_path))
    
    return result


def step4_align(parsed_lyrics: dict, timestamps: dict, work_dir: Path) -> dict:
    """Step 4: Forced alignment."""
    print("\n" + "─"*60)
    print("  STEP 4: Forced alignment...")
    print("─"*60)
    
    aligned = align_lyrics_to_timestamps(parsed_lyrics, timestamps)
    
    print(f"\n  Alignment stats:")
    for k, v in aligned["stats"].items():
        print(f"    {k}: {v}")
    
    if aligned["flagged"]:
        print(f"\n  ⚠ Flagged words ({len(aligned['flagged'])}):")
        for f in aligned["flagged"][:15]:
            print(f"    '{f['word']}' [{f['section']}] line {f['line']} — {f['reason']} (conf: {f['confidence']:.2f})")
        if len(aligned["flagged"]) > 15:
            print(f"    ... and {len(aligned['flagged']) - 15} more")
    
    aligned_path = work_dir / "aligned_lyrics.json"
    aligned_path.write_text(json.dumps(aligned, indent=2))
    
    return aligned


def step5_style_config(config: dict, work_dir: Path) -> dict:
    """Step 5: Style configuration."""
    print("\n" + "─"*60)
    print("  STEP 5: Style configuration...")
    print("─"*60)
    
    # Check font availability
    config["font"]["family"] = check_font(config["font"]["family"])
    
    print(f"\n  Display mode: {config['display_mode']}")
    print(f"  Font: {config['font']['family']} @ {config['font']['size_normal']}px")
    print(f"  Highlight color: {config['font']['color_highlight']}")
    print(f"  Ken Burns: {config['background']['zoom_style']}")
    print(f"  Loop: {'3x infinite' if config['loop']['enabled'] else 'single play'}")
    print(f"  Output: {config['output']['resolution']} @ {config['output']['fps']}fps")
    
    config_path = work_dir / "style_config.json"
    config_path.write_text(json.dumps(config, indent=2))
    
    return config


def step6_assemble(aligned: dict, config: dict, audio_path: str, 
                   background_path: str, work_dir: Path, song_name: str) -> list:
    """Step 6: FFmpeg video assembly."""
    print("\n" + "─"*60)
    print("  STEP 6: Assembling video...")
    print("─"*60)
    
    output_cfg = config["output"]
    bg_cfg = config["background"]
    loop_cfg = config["loop"]
    resolution = output_cfg["resolution"]
    fps = output_cfg["fps"]
    crf = output_cfg.get("crf", 18)
    
    duration = get_audio_duration(audio_path)
    total_frames = int(duration * fps)
    
    print(f"  Audio duration: {duration:.1f}s ({total_frames} frames @ {fps}fps)")
    
    # 6a: Generate ASS subtitle file
    print("\n  Generating subtitle file...")
    ass_path = str(work_dir / "lyrics.ass")
    srt_path = str(work_dir / "lyrics.srt")
    generate_ass(aligned, config, ass_path)
    generate_srt(aligned, srt_path)
    
    # 6b: Build Ken Burns zoom filter
    zoom_start = bg_cfg.get("zoom_start", 1.0)
    zoom_end = bg_cfg.get("zoom_end", 1.08)
    zoom_rate = (zoom_end - zoom_start) / max(total_frames, 1)
    
    zoom_style = bg_cfg.get("zoom_style", "slow_zoom_in")
    if zoom_style == "slow_zoom_out":
        zoom_expr = f"if(eq(on,1),{zoom_end},{zoom_end}-{zoom_rate}*on)"
    elif zoom_style == "breathing":
        # Oscillate on ~8 bar cycle (assume 4 beats/bar at given BPM)
        cycle_frames = fps * 16  # ~16 seconds per cycle
        zoom_expr = f"{(zoom_start + zoom_end)/2}+{(zoom_end - zoom_start)/2}*sin(2*PI*on/{cycle_frames})"
    elif zoom_style == "static":
        zoom_expr = "1"
    else:  # slow_zoom_in (default)
        zoom_expr = f"if(eq(on,1),{zoom_start},{zoom_start}+{zoom_rate}*on)"
    
    # 6c: Render single video
    single_output = str(work_dir / f"{song_name}_single.mp4")
    
    # Two-pass: first create zoompan video, then overlay subtitles + audio
    bg_video = str(work_dir / "bg_video.mp4")
    
    run_ffmpeg([
        "-loop", "1", "-i", background_path,
        "-vf", f"scale=3840:2160,zoompan=z='{zoom_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s={resolution}:fps={fps}",
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "fast", "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        bg_video
    ], "Creating background with Ken Burns zoom")
    
    run_ffmpeg([
        "-i", bg_video, "-i", audio_path,
        "-vf", f"ass={ass_path}",
        "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        single_output
    ], "Compositing lyrics + audio")
    
    outputs = [single_output]
    
    # 6d: Infinite loop assembly
    if loop_cfg.get("enabled", False):
        copies = loop_cfg.get("copies", 3)
        crossfade_s = loop_cfg.get("crossfade_ms", 2000) / 1000
        
        print(f"\n  Building {copies}x infinite loop...")
        
        copy_files = []
        for c in range(copies):
            # Shift Ken Burns starting point for each copy
            shift_factor = c * 0.02  # Each copy starts slightly different
            shifted_zoom = f"if(eq(on,1),{zoom_start + shift_factor},{zoom_start + shift_factor}+{zoom_rate}*on)"
            
            copy_bg = str(work_dir / f"bg_copy_{c}.mp4")
            copy_out = str(work_dir / f"copy_{c}.mp4")
            
            run_ffmpeg([
                "-loop", "1", "-i", background_path,
                "-vf", f"scale=3840:2160,zoompan=z='{shifted_zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s={resolution}:fps={fps}",
                "-t", str(duration),
                "-c:v", "libx264", "-preset", "fast", "-crf", str(crf),
                "-pix_fmt", "yuv420p",
                copy_bg
            ], f"Ken Burns copy {c+1}/{copies}")
            
            run_ffmpeg([
                "-i", copy_bg, "-i", audio_path,
                "-vf", f"ass={ass_path}",
                "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
                "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                copy_out
            ], f"Compositing copy {c+1}/{copies}")
            
            copy_files.append(copy_out)
        
        # Concatenate with crossfades
        loop_output = str(work_dir / f"{song_name}_loop.mp4")
        
        if copies == 3:
            offset1 = duration - crossfade_s
            offset2 = (duration * 2) - (crossfade_s * 2)
            
            run_ffmpeg([
                "-i", copy_files[0], "-i", copy_files[1], "-i", copy_files[2],
                "-filter_complex",
                f"[0:v][1:v]xfade=transition=fade:duration={crossfade_s}:offset={offset1}[v01];"
                f"[v01][2:v]xfade=transition=fade:duration={crossfade_s}:offset={offset2}[vout];"
                f"[0:a][1:a]acrossfade=d={crossfade_s}[a01];"
                f"[a01][2:a]acrossfade=d={crossfade_s}[aout]",
                "-map", "[vout]", "-map", "[aout]",
                "-c:v", "libx264", "-crf", str(crf),
                "-c:a", "aac", "-b:a", "192k",
                loop_output
            ], "Assembling infinite loop with crossfades")
        else:
            # Simple concat for non-3 copy counts
            concat_file = work_dir / "concat.txt"
            concat_file.write_text("\n".join(f"file '{f}'" for f in copy_files))
            
            run_ffmpeg([
                "-f", "concat", "-safe", "0", "-i", str(concat_file),
                "-c:v", "libx264", "-crf", str(crf),
                "-c:a", "aac", "-b:a", "192k",
                loop_output
            ], "Concatenating loop copies")
        
        outputs.append(loop_output)
    
    return outputs


def step7_export(outputs: list, aligned: dict, config: dict, 
                 work_dir: Path, output_dir: Path, song_name: str):
    """Step 7: Final export and metadata."""
    print("\n" + "─"*60)
    print("  STEP 7: Final export...")
    print("─"*60)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    exported = []
    
    # Copy video files
    for src in outputs:
        src_path = Path(src)
        if "loop" in src_path.name:
            dest_name = f"{song_name}_lyric_video_loop.mp4"
        else:
            dest_name = f"{song_name}_lyric_video.mp4"
        dest = output_dir / dest_name
        shutil.copy2(src, dest)
        exported.append(str(dest))
        print(f"  Exported: {dest}")
    
    # Copy subtitle files
    for ext in ["ass", "srt"]:
        src = work_dir / f"lyrics.{ext}"
        if src.exists():
            dest = output_dir / f"{song_name}_lyrics.{ext}"
            shutil.copy2(src, dest)
            exported.append(str(dest))
    
    # Copy aligned lyrics
    aligned_src = work_dir / "aligned_lyrics.json"
    if aligned_src.exists():
        dest = output_dir / f"{song_name}_aligned_lyrics.json"
        shutil.copy2(aligned_src, dest)
        exported.append(str(dest))
    
    # Copy style config
    config_src = work_dir / "style_config.json"
    if config_src.exists():
        dest = output_dir / f"{song_name}_style_config.json"
        shutil.copy2(config_src, dest)
        exported.append(str(dest))
    
    # Generate YouTube metadata
    metadata = {
        "title": f"{song_name.replace('_', ' ').title()} (Lyric Video)",
        "description": f"Official lyric video for {song_name.replace('_', ' ').title()}.\n\nGenerated with Lyric Video Forge.",
        "tags": ["lyric video", "lyrics", "music", song_name.replace("_", " ")],
        "chapters": []
    }
    
    # Add chapters from section timestamps
    for section in aligned.get("sections", []):
        if section.get("start", 0) > 0:
            minutes = int(section["start"] // 60)
            seconds = int(section["start"] % 60)
            metadata["chapters"].append({
                "time": f"{minutes}:{seconds:02d}",
                "title": section["tag"]
            })
    
    meta_path = output_dir / f"{song_name}_metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2))
    exported.append(str(meta_path))
    
    print(f"\n  All files exported to: {output_dir}")
    print(f"  Total files: {len(exported)}")
    
    return exported


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Lyric Video Forge — Audio + Lyrics → YouTube-ready MP4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 forge.py --audio song.mp3 --lyrics lyrics.txt
  python3 forge.py --audio song.mp3 --lyrics lyrics.txt --generate-image "dark cathedral"
  python3 forge.py --audio song.mp3 --lyrics lyrics.txt --image bg.png --mode line_by_line
  python3 forge.py --audio song.mp3 --lyrics lyrics.txt --no-loop --auto
        """
    )
    
    parser.add_argument("--audio", required=True, help="Path to audio file (MP3/WAV)")
    parser.add_argument("--lyrics", required=True, help="Path to lyrics text file")
    parser.add_argument("--image", help="Path to background image (skip generation)")
    parser.add_argument("--generate-image", dest="image_prompt", help="Prompt for kie.ai image generation")
    parser.add_argument("--name", help="Song name (derived from audio filename if not set)")
    parser.add_argument("--language", default="en", help="Audio language for Deepgram (default: en)")
    parser.add_argument("--mode", choices=["karaoke", "line_by_line", "hybrid"], default="karaoke")
    parser.add_argument("--no-loop", action="store_true", help="Disable infinite loop mode")
    parser.add_argument("--loop-copies", type=int, default=3, help="Number of loop copies (default: 3)")
    parser.add_argument("--zoom", choices=["slow_zoom_in", "slow_zoom_out", "breathing", "static"],
                        default="slow_zoom_in")
    parser.add_argument("--config", help="Path to custom style config JSON")
    parser.add_argument("--output", default="./output", help="Output directory")
    parser.add_argument("--auto", action="store_true", help="Skip approval gates (batch mode)")
    parser.add_argument("--keyframe-mode", action="store_true", dest="keyframe_mode",
                        help="Use keyframe image generation (5 tiers x 3 variations) instead of single background")
    parser.add_argument("--genre", default="", help="Song genre for visual constitution (keyframe mode)")
    parser.add_argument("--character", default="", help="Character anchor description (keyframe mode)")
    parser.add_argument("--setting", default="", help="Setting anchor description (keyframe mode)")
    parser.add_argument("--art-style", default="", dest="art_style", help="Art style for keyframes")
    parser.add_argument("--colors", default="", help="Color palette for keyframes")
    parser.add_argument("--variations", type=int, default=3, help="Keyframe variations per tier (default: 3)")
    parser.add_argument("--video-loops", action="store_true", dest="video_loops",
                        help="Generate video loop clips (requires keyframe mode)")

    args = parser.parse_args()
    
    # Validate inputs
    if not Path(args.audio).exists():
        print(f"ERROR: Audio file not found: {args.audio}")
        sys.exit(1)
    if not Path(args.lyrics).exists():
        print(f"ERROR: Lyrics file not found: {args.lyrics}")
        sys.exit(1)
    
    # Check FFmpeg
    if not shutil.which("ffmpeg"):
        if platform.system() == "Windows":
            hint = "winget install Gyan.FFmpeg  (or: choco install ffmpeg)"
        elif platform.system() == "Darwin":
            hint = "brew install ffmpeg"
        else:
            hint = "sudo apt install ffmpeg"
        print(f"ERROR: FFmpeg not found. Install with: {hint}")
        sys.exit(1)
    
    # Song name
    song_name = args.name or Path(args.audio).stem.replace(" ", "_")
    
    # Work directory (cross-platform temp; honors $TMPDIR / %TEMP%, not /tmp)
    work_dir = Path(tempfile.gettempdir()) / "lyric-video-forge" / song_name
    work_dir.mkdir(parents=True, exist_ok=True)
    
    output_dir = Path(args.output)
    
    # Load or build config
    if args.config and Path(args.config).exists():
        config = json.loads(Path(args.config).read_text())
    else:
        config = json.loads(json.dumps(DEFAULT_CONFIG))  # Deep copy
    
    # Apply CLI overrides
    config["display_mode"] = args.mode
    config["background"]["zoom_style"] = args.zoom
    config["loop"]["enabled"] = not args.no_loop
    config["loop"]["copies"] = args.loop_copies
    
    # ─── PIPELINE ─────────────────────────────────────────────────────────

    keyframe_mode = args.keyframe_mode
    video_loops = args.video_loops

    print("\n" + "█"*60)
    print("  LYRIC VIDEO FORGE")
    print(f"  Song: {song_name}")
    print(f"  Mode: {config['display_mode']} | Loop: {'Yes' if config['loop']['enabled'] else 'No'}")
    if keyframe_mode:
        print(f"  Keyframes: ON ({args.variations} variations per tier)")
    if video_loops:
        print(f"  Video loops: ON")
    print("█"*60)

    # Step 1: Parse lyrics (legacy structure)
    parsed = step1_parse_lyrics(args.lyrics, work_dir)

    # Step 1a: Strip lyrics → clean text + structure map
    clean_lyrics_path, structure_map = step1a_strip_lyrics(args.lyrics, work_dir)

    if not gate(1, "Lyrics parsed and stripped correctly?", args.auto):
        print("  Edit your lyrics file and re-run.")
        sys.exit(0)

    # Step 2: Background / Keyframe images
    bg_path = None
    chosen_keyframes = {}
    constitution = None

    if keyframe_mode:
        # Build visual constitution
        print("\n" + "─"*60)
        print("  STEP 2a: Building visual constitution...")
        print("─"*60)

        constitution = build_constitution(
            lyrics_text=Path(clean_lyrics_path).read_text(encoding="utf-8"),
            genre=args.genre,
            character_description=args.character,
            setting_description=args.setting,
            art_style=args.art_style,
            color_palette=args.colors,
        )
        constitution = reduce_keyframes(constitution, structure_map)
        save_constitution(constitution, str(work_dir / "constitution.json"))

        # Generate keyframe images (5 tiers x N variations)
        chosen_keyframes = step2_keyframes(
            constitution, work_dir, args.variations, args.auto
        )

        if not gate(2, "Keyframe images approved?", args.auto):
            print("  Adjust constitution and re-run.")
            sys.exit(0)

        # Use tier A as fallback background for Ken Burns mode
        if "A" in chosen_keyframes:
            bg_path = chosen_keyframes["A"]
        elif chosen_keyframes:
            bg_path = list(chosen_keyframes.values())[0]
    else:
        # Legacy: single background image
        while bg_path is None:
            bg_path = step2_background(args.image_prompt, args.image, work_dir, args.auto)
            if bg_path and not gate(2, "Background image approved?", args.auto):
                bg_path = None  # Retry

    # Step 3: Transcribe
    timestamps = step3_transcribe(args.audio, args.language, work_dir)

    # Step 4: Align (crossmatch mode if structure_map available)
    if structure_map:
        print("\n" + "─"*60)
        print("  STEP 4: Crossmatch alignment (user text + Deepgram timing)...")
        print("─"*60)
        aligned = crossmatch_with_structure(
            clean_lyrics_path, timestamps, structure_map
        )
        aligned_path = work_dir / "aligned_lyrics.json"
        aligned_path.write_text(json.dumps(aligned, indent=2, ensure_ascii=False))
        print(f"\n  Alignment stats:")
        for k, v in aligned["stats"].items():
            print(f"    {k}: {v}")
    else:
        aligned = step4_align(parsed, timestamps, work_dir)

    if not gate(3, "Alignment looks good?", args.auto):
        print("  Edit aligned_lyrics.json manually and re-run from step 6.")
        sys.exit(0)

    # Step 5: Style config
    config = step5_style_config(config, work_dir)
    if not gate(4, "Style config approved?", args.auto):
        print(f"  Edit {work_dir}/style_config.json and re-run.")
        sys.exit(0)

    # Step 5a: Video loop plan (if keyframe mode + video loops)
    loop_plan = None
    if keyframe_mode and video_loops and constitution:
        print("\n" + "─"*60)
        print("  STEP 5a: Generating video loop plan...")
        print("─"*60)
        loop_plan = plan_loops(structure_map, aligned, constitution)
        save_loop_plan(loop_plan, str(work_dir / "loop_plan.json"))

    # Step 6: Assemble (Ken Burns fallback if no video loops)
    outputs = step6_assemble(aligned, config, args.audio, bg_path, work_dir, song_name)
    if not gate(5, "Video looks good?", args.auto):
        print("  Adjust config and re-run step 6.")
        sys.exit(0)

    # Step 7: Export
    exported = step7_export(outputs, aligned, config, work_dir, output_dir, song_name)

    # Also export new artifacts
    for extra in ["clean_lyrics.txt", "structure_map.json", "constitution.json", "loop_plan.json"]:
        src = work_dir / extra
        if src.exists():
            dest = output_dir / f"{song_name}_{extra}"
            shutil.copy2(src, dest)

    print("\n" + "█"*60)
    print("  FORGE COMPLETE")
    print(f"  Output: {output_dir}")
    print("█"*60 + "\n")


if __name__ == "__main__":
    main()
