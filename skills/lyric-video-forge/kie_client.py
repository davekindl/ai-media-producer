"""
kie.ai API client for image generation (GPT-Image-2 default, Flux fallback)
and video generation (Kling 3.0, Veo 3 Fast, Sora 2 Pro HD).

Uses the unified jobs API (createTask -> recordInfo poll) for all generation
calls. Async POST -> poll pattern. Requires KIE_API_KEY environment variable.

Image contract (per kie.ai unified jobs API):
  POST https://api.kie.ai/api/v1/jobs/createTask
    {"model": "gpt-image-2-text-to-image",
     "input": {"prompt": "...", "aspect_ratio": "16:9", "resolution": "2K"}}
  GET  https://api.kie.ai/api/v1/jobs/recordInfo?taskId=...
    -> {"data": {"state": "success", "resultJson": "{\\"resultUrls\\":[...]}"}}
"""

import os
import sys
import json
import time
import requests
from pathlib import Path


KIE_BASE_URL = "https://api.kie.ai/api/v1"
# Default image model: OpenAI GPT-Image-2 via kie.ai unified jobs API.
DEFAULT_IMAGE_MODEL = "gpt-image-2-text-to-image"
POLL_INTERVAL = 5  # seconds between polls
MAX_POLL_ATTEMPTS = 60  # 5 minutes max wait


def get_api_key():
    key = os.environ.get("KIE_API_KEY")
    if not key:
        print("ERROR: KIE_API_KEY environment variable not set.")
        print("Set it with: export KIE_API_KEY='your-key-here'")
        sys.exit(1)
    return key


def _headers():
    return {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json"
    }


def _submit_image_task(
    prompt: str,
    model: str = DEFAULT_IMAGE_MODEL,
    aspect_ratio: str = "16:9",
    resolution: str = "2K",
) -> str:
    """Submit an async image task via the unified jobs API. Returns task ID.

    Uses POST /api/v1/jobs/createTask with the GPT-Image-2 input schema.
    """
    payload = {
        "model": model,
        "input": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        },
    }
    response = requests.post(
        f"{KIE_BASE_URL}/jobs/createTask",
        headers=_headers(),
        json=payload,
        timeout=30
    )
    if response.status_code == 402:
        raise RuntimeError("kie.ai error 402: out of credits.")
    if response.status_code == 401:
        raise RuntimeError("kie.ai error 401: invalid/missing KIE_API_KEY.")
    response.raise_for_status()
    result = response.json()
    if result.get("code") not in (200, None):
        raise RuntimeError(f"kie.ai error: {result.get('msg', 'unknown')}")
    return result["data"]["taskId"]


def _extract_result_urls(data: dict) -> list[str]:
    """Pull result image URLs from a recordInfo data block.

    The unified jobs API returns results as a JSON string in `resultJson`
    (e.g. '{"resultUrls": ["https://..."]}'). Fall back to a nested dict
    shape for forward/back compatibility.
    """
    raw = data.get("resultJson")
    if isinstance(raw, str) and raw:
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            raw = {}
    if not isinstance(raw, dict):
        raw = data.get("response", {}) if isinstance(data.get("response"), dict) else {}
    return raw.get("resultUrls", []) or raw.get("result_urls", [])


def _poll_task(task_id: str) -> str | None:
    """Poll a task until complete via GET /api/v1/jobs/recordInfo.

    Returns the first result image URL or None. The unified jobs API reports
    progress in `state`: waiting | queuing | generating | success | fail.
    """
    for attempt in range(MAX_POLL_ATTEMPTS):
        response = requests.get(
            f"{KIE_BASE_URL}/jobs/recordInfo",
            params={"taskId": task_id},
            headers=_headers(),
            timeout=30
        )
        result = response.json()
        data = result.get("data", {}) or {}
        state = str(data.get("state", "")).lower()

        if state == "success":
            urls = _extract_result_urls(data)
            return urls[0] if urls else None
        elif state == "fail":
            print(f"  Task {task_id} failed: {data.get('failMsg', data)}")
            return None

        time.sleep(POLL_INTERVAL)

    print(f"  Task {task_id} timed out after {MAX_POLL_ATTEMPTS * POLL_INTERVAL}s")
    return None


def _download_image(url: str, filepath: Path) -> bool:
    """Download an image URL to a local file."""
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_bytes(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"  ERROR downloading {url}: {e}")
        return False


# ─── Single Image Generation (legacy compat) ────────────────────────────────

def generate_image(prompt: str, output_dir: str, width: int = 1920, height: int = 1080, num_images: int = 3) -> list[str]:
    """
    Generate images via kie.ai (async pattern).
    Returns list of saved file paths.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Submit all tasks first (parallel generation)
    print(f"  Submitting {num_images} image generation tasks...")
    task_ids = []
    for i in range(num_images):
        try:
            tid = _submit_image_task(prompt)
            task_ids.append((i, tid))
            print(f"  Task {i+1}/{num_images}: {tid}")
        except Exception as e:
            print(f"  ERROR submitting task {i+1}: {e}")
            if i == 0:
                raise

    # Poll all tasks
    print(f"  Polling {len(task_ids)} tasks...")
    saved_files = []
    for i, tid in task_ids:
        url = _poll_task(tid)
        if url:
            filepath = output_path / f"background_{i+1}.png"
            if _download_image(url, filepath):
                saved_files.append(str(filepath))
                print(f"  Saved: {filepath}")

    return saved_files


# ─── Batch Keyframe Generation (5 tiers x 3 variations = 15 images) ─────────

def generate_keyframes(
    constitution: dict,
    output_dir: str,
    variations: int = 3,
) -> dict[str, list[str]]:
    """
    Generate keyframe images from a visual constitution.

    Fires all tasks in parallel (async), polls for results, downloads.

    Args:
        constitution: Visual constitution with keyframes dict
        output_dir: Where to save images
        variations: Number of variations per tier (default 3)

    Returns:
        Dict mapping tier key -> list of file paths
        e.g. {"A": ["frame_A_v1.png", ...], "B": [...], ...}
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    model = constitution.get("model", DEFAULT_IMAGE_MODEL)
    keyframes = constitution.get("keyframes", {})

    total = len(keyframes) * variations
    print(f"  Generating {total} keyframe images ({len(keyframes)} tiers x {variations} variations)...")
    print(f"  Model: {model}")

    # Submit all tasks
    tasks = []  # (tier_key, variation_idx, task_id)
    for tier_key, kf in sorted(keyframes.items()):
        prompt = kf["prompt"]
        for v in range(variations):
            try:
                tid = _submit_image_task(prompt, model)
                tasks.append((tier_key, v + 1, tid))
                print(f"  Submitted: frame_{tier_key}_v{v+1} ({tid[:12]}...)")
            except Exception as e:
                print(f"  ERROR submitting frame_{tier_key}_v{v+1}: {e}")

    # Poll and download all
    print(f"\n  Waiting for {len(tasks)} images...")
    results = {}
    for tier_key, v_idx, tid in tasks:
        url = _poll_task(tid)
        if url:
            filename = f"frame_{tier_key}_v{v_idx}.png"
            filepath = output_path / filename
            if _download_image(url, filepath):
                results.setdefault(tier_key, []).append(str(filepath))
                print(f"  Downloaded: {filename}")

    # Summary
    print(f"\n  Keyframe generation complete:")
    for tier_key in sorted(results.keys()):
        print(f"    {tier_key}: {len(results[tier_key])} images")

    return results


# ─── Video Generation (NOT IMPLEMENTED) ─────────────────────────────────────
#
# WARNING: image-to-video clip generation is NOT wired up.
#
# The unified jobs API exposes video models (Kling / Veo / Sora) under their
# own model IDs with an image-to-video input schema (start/end frame upload +
# motion prompt). That schema is NOT implemented here. The previous version of
# this function silently routed video requests through the IMAGE endpoint
# (_submit_image_task), which returns a still image, not a video clip — a
# latent bug that produced wrong output.
#
# Until the video input schema is implemented, this raises instead of
# pretending to work. The default pipeline (Ken Burns over a still background)
# is fully functional and is the supported path. See SKILL.md "Capability 4/5".


def generate_video_clip(
    start_image_path: str,
    end_image_path: str | None,
    motion_prompt: str,
    model: str,
    output_path: str,
    duration: int = 5,
) -> str | None:
    """NOT IMPLEMENTED — kie.ai image-to-video clip generation.

    Intentionally raises NotImplementedError rather than silently returning a
    still image (the prior behaviour). Use the Ken Burns assembly path instead.
    """
    raise NotImplementedError(
        "Video clip generation is not implemented. The kie.ai video models "
        "(Kling/Veo/Sora) require an image-to-video input schema that this "
        "client does not yet support. Use the default Ken Burns background "
        "path (omit --video-loops)."
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate images/keyframes via kie.ai")
    parser.add_argument("--prompt", help="Image generation prompt")
    parser.add_argument("--constitution", help="Path to constitution.json for keyframe generation")
    parser.add_argument("--output", default="./output/images", help="Output directory")
    parser.add_argument("--count", type=int, default=3, help="Number of images/variations")
    args = parser.parse_args()

    if args.constitution:
        const = json.loads(Path(args.constitution).read_text())
        results = generate_keyframes(const, args.output, args.count)
        print(f"\nGenerated keyframes: {sum(len(v) for v in results.values())} images")
    elif args.prompt:
        files = generate_image(args.prompt, args.output, num_images=args.count)
        print(f"\nGenerated {len(files)} images:")
        for f in files:
            print(f"  {f}")
    else:
        print("Provide --prompt or --constitution")
