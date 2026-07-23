"""
Deepgram Nova-3 client for word-level timestamp extraction.
Requires DEEPGRAM_API_KEY environment variable.
"""

import os
import sys
import json
import requests
from pathlib import Path


DEEPGRAM_API_URL = "https://api.deepgram.com/v1/listen"


def get_api_key():
    key = os.environ.get("DEEPGRAM_API_KEY")
    if not key:
        print("ERROR: DEEPGRAM_API_KEY environment variable not set.")
        print("Set it with: export DEEPGRAM_API_KEY='your-key-here'")
        sys.exit(1)
    return key


def transcribe_audio(audio_path: str, language: str = "en") -> dict:
    """
    Transcribe audio file with word-level timestamps using Deepgram Nova-3.
    
    Returns dict with:
    - words: list of {word, start, end, confidence}
    - transcript: full text
    - duration: audio duration in seconds
    """
    api_key = get_api_key()
    audio_file = Path(audio_path)

    if not audio_file.exists():
        print(f"ERROR: Audio file not found: {audio_path}")
        sys.exit(1)

    # Determine MIME type
    suffix = audio_file.suffix.lower()
    mime_map = {
        ".mp3": "audio/mp3",
        ".wav": "audio/wav",
        ".flac": "audio/flac",
        ".ogg": "audio/ogg",
        ".m4a": "audio/mp4",
        ".mp4": "audio/mp4",
    }
    mime_type = mime_map.get(suffix, "audio/mp3")

    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": mime_type,
    }

    params = {
        "model": "nova-3",
        "smart_format": "true",
        "punctuate": "true",
        "utterances": "true",
        "language": language,
    }

    print(f"  Sending {audio_file.name} to Deepgram Nova-3...")
    print(f"  Language: {language}")

    with open(audio_path, "rb") as f:
        audio_data = f.read()

    try:
        response = requests.post(
            DEEPGRAM_API_URL,
            headers=headers,
            params=params,
            data=audio_data,
            timeout=300  # 5 min timeout for long tracks
        )
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        print(f"  ERROR: Deepgram API request failed: {e}")
        raise

    # Extract word-level data
    channel = result.get("results", {}).get("channels", [{}])[0]
    alternative = channel.get("alternatives", [{}])[0]

    words = []
    for w in alternative.get("words", []):
        words.append({
            "word": w.get("word", ""),
            "start": w.get("start", 0),
            "end": w.get("end", 0),
            "confidence": w.get("confidence", 0),
        })

    transcript = alternative.get("transcript", "")

    # Get duration from metadata if available
    duration = result.get("metadata", {}).get("duration", 0)
    if not duration and words:
        duration = words[-1]["end"]

    print(f"  Transcribed {len(words)} words over {duration:.1f}s")
    print(f"  Average confidence: {sum(w['confidence'] for w in words) / max(len(words), 1):.2%}")

    return {
        "words": words,
        "transcript": transcript,
        "duration": duration,
        "language": language,
        "raw_response": result,
    }


def save_timestamps(transcription: dict, output_path: str):
    """Save word timestamps to JSON (without raw API response to keep it clean)."""
    clean = {
        "words": transcription["words"],
        "transcript": transcription["transcript"],
        "duration": transcription["duration"],
        "language": transcription["language"],
        "word_count": len(transcription["words"]),
    }
    Path(output_path).write_text(json.dumps(clean, indent=2))
    print(f"  Saved timestamps to {output_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transcribe audio with Deepgram Nova-3")
    parser.add_argument("--audio", required=True, help="Path to audio file")
    parser.add_argument("--language", default="en", help="Language code (default: en)")
    parser.add_argument("--output", default="./output/timestamps.json", help="Output JSON path")
    args = parser.parse_args()

    result = transcribe_audio(args.audio, args.language)
    save_timestamps(result, args.output)
