# Known Issues — gpt-image-2-techniques

The following items were identified during the build but **deliberately NOT fixed yet**.
Resolve in a follow-up before your next major release.

## 1. Missing brand kit: `novolith.json`
- `brand_kits/_index.json` previously registered a `novolith` kit (`_status: "scaffold pending"`).
- `novolith.json` does not exist on disk. That entry has been removed from `_index.json`.
- If you need an English global brand kit, copy `acme-consulting.json`, rename it, and
  add it to `_index.json`.

## 2. Brand kits state reconciliation
- The shipped `brand_kits/` folder is the local canonical source. There is no external
  shared location — each skill ships its own copies.
- If you maintain multiple skills that share the same brand kit, keep a single source
  in your own infrastructure and copy/symlink as needed. The `acme-consulting.json`
  template is a good starting point.

---
_Changes applied in this version:_
- Removed the hardcoded kie.ai API key fallback in `kie_client.py` — the key is
  now read from `KIE_AI_API_KEY` only (raises if unset).
- Trimmed the SKILL frontmatter `description` to <=1024 chars.
- Removed `__pycache__/` from the skill folder.
- Ships a generic `acme-consulting.json` starter template; copy it to make your own brand kit.
- Updated `_index.json` to reflect current on-disk kits.
