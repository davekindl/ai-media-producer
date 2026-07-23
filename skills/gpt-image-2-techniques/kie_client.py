"""
kie.ai GPT-Image-2 client.

Provides:
- submit_text_to_image(prompt, aspect_ratio, resolution) -> task_id
- submit_image_to_image(prompt, aspect_ratio, resolution, input_urls) -> task_id
- poll(task_id, max_wait=600) -> data dict
- extract_urls(data) -> list of result URLs
- download(url, path) -> None
- generate(prompt, ar, res, refs=None, output_path=None) -> dict (one-shot)

Reads KIE_AI_API_KEY from the environment only. No key is hardcoded.
Set the env var before use (sourced from your own secrets config (env var or .env)), e.g.:
    setx KIE_AI_API_KEY "<your-key>"   (Windows, persists)
    $env:KIE_AI_API_KEY = "<your-key>" (PowerShell, current session)
"""
import json
import os
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

API_KEY = os.environ.get("KIE_AI_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "KIE_AI_API_KEY is not set. Set it in your environment before "
        "running this client — no key is hardcoded in v2."
    )
SUBMIT_URL = "https://api.kie.ai/api/v1/jobs/createTask"
POLL_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"

CTX = ssl.create_default_context()


def _post(url: str, body: bytes, timeout: int = 30):
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return json.load(r)


def _get(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {API_KEY}"})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return json.load(r)


def submit_text_to_image(prompt: str, aspect_ratio: str = "16:9", resolution: str = "2K") -> str:
    """Submit a text-to-image task. Returns taskId."""
    if aspect_ratio == "1:1" and resolution == "4K":
        raise ValueError("kie.ai constraint: 1:1 aspect ratio cannot be 4K. Use 2K instead.")
    body = json.dumps({
        "model": "gpt-image-2-text-to-image",
        "input": {"prompt": prompt, "aspect_ratio": aspect_ratio, "resolution": resolution},
    }).encode()
    data = _post(SUBMIT_URL, body)
    if data.get("code") != 200:
        raise RuntimeError(f"kie.ai submit failed: {data}")
    return data["data"]["taskId"]


def submit_image_to_image(
    prompt: str,
    input_urls: list[str],
    aspect_ratio: str = "16:9",
    resolution: str = "2K",
) -> str:
    """Submit an image-to-image task. Up to 16 reference URLs."""
    if not input_urls:
        raise ValueError("image-to-image requires at least 1 input URL")
    if len(input_urls) > 16:
        raise ValueError("kie.ai constraint: maximum 16 input URLs")
    if aspect_ratio == "1:1" and resolution == "4K":
        raise ValueError("kie.ai constraint: 1:1 aspect ratio cannot be 4K.")
    body = json.dumps({
        "model": "gpt-image-2-image-to-image",
        "input": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "input_urls": input_urls,
        },
    }).encode()
    data = _post(SUBMIT_URL, body)
    if data.get("code") != 200:
        raise RuntimeError(f"kie.ai submit failed: {data}")
    return data["data"]["taskId"]


def poll(task_id: str, max_wait: int = 600, log_fn=None) -> dict:
    """Poll until task completes. max_wait in seconds. log_fn(msg) optional."""
    start = time.time()
    last_state = None
    while time.time() - start < max_wait:
        try:
            data = _get(f"{POLL_URL}?taskId={task_id}")
        except urllib.error.HTTPError as e:
            if log_fn:
                log_fn(f"poll HTTP {e.code}, retrying in 15s")
            time.sleep(15)
            continue
        d = data.get("data", {}) or {}
        state = d.get("state")
        if log_fn and state != last_state:
            log_fn(f"state={state}")
            last_state = state
        if state in ("success", "completed", "done", "ok"):
            return d
        if state in ("fail", "failed", "error", "timeout"):
            raise RuntimeError(f"kie.ai task failed: {d.get('failMsg') or d.get('failCode')}")
        time.sleep(12)
    raise TimeoutError(f"polling timeout for {task_id}")


def extract_urls(data: dict) -> list[str]:
    """Extract result URLs from a polled response."""
    rj = data.get("resultJson")
    if rj:
        try:
            parsed = json.loads(rj) if isinstance(rj, str) else rj
        except Exception:
            parsed = None
        if isinstance(parsed, dict):
            for k in ("resultUrls", "imageUrls", "urls", "output", "images"):
                v = parsed.get(k)
                if v:
                    return v if isinstance(v, list) else [v]
            single = parsed.get("imageUrl") or parsed.get("url")
            if single:
                return [single]
        if isinstance(parsed, list):
            return parsed
    for k in ("imageUrl", "imageUrls", "resultUrl", "url"):
        v = data.get(k)
        if v:
            return v if isinstance(v, list) else [v]
    return []


def download(url: str, path: Path) -> None:
    """Download an image URL to the given path."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120, context=CTX) as r:
        path.write_bytes(r.read())


def generate(
    prompt: str,
    aspect_ratio: str = "16:9",
    resolution: str = "2K",
    input_urls: Optional[list[str]] = None,
    output_path: Optional[Path] = None,
    max_wait: int = 600,
    log_fn=None,
) -> dict:
    """One-shot: submit + poll + download. Returns dict with task_id, urls, output_path."""
    if input_urls:
        task_id = submit_image_to_image(prompt, input_urls, aspect_ratio, resolution)
    else:
        task_id = submit_text_to_image(prompt, aspect_ratio, resolution)
    if log_fn:
        log_fn(f"submitted task_id={task_id}")
    data = poll(task_id, max_wait=max_wait, log_fn=log_fn)
    urls = extract_urls(data)
    if not urls:
        raise RuntimeError("no result URLs")
    saved_path = None
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        download(urls[0], output_path)
        saved_path = str(output_path)
        if log_fn:
            log_fn(f"saved to {saved_path}")
    return {
        "task_id": task_id,
        "urls": urls,
        "output_path": saved_path,
        "kie_data": data,
    }


if __name__ == "__main__":
    # Smoke test
    import sys

    def log(m):
        print(m, flush=True)

    if len(sys.argv) < 2:
        print("Usage: python kie_client.py 'your prompt here' [output.png]")
        sys.exit(1)

    prompt = sys.argv[1]
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./out.png")
    result = generate(prompt, output_path=out, log_fn=log)
    print(json.dumps({"task_id": result["task_id"], "saved": result["output_path"]}, indent=2))
