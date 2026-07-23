# Technical Pipeline -- POD Shirt Designer

Resolution, color profiles, format specs, background removal, and end-to-end workflow.

---

## T1: Resolution Pipeline (AI Output to Print-Ready)

**Target spec:** 4500 x 5400 pixels at 300 DPI, PNG-24 with alpha transparency, sRGB

**Pipeline:**
1. Generate at max native resolution (GPT-Image-2 supports up to 4K via kie.ai)
2. If below target, upscale using AI upscaler (Let's Enhance, Topaz Gigapixel)
3. Verify at actual print dimensions: Image Size at 300+ DPI
4. Export PNG-24 with alpha

**Platform-specific dimensions:**

| Platform | Required Size | DPI | Format |
|----------|-------------|-----|--------|
| Amazon Merch on Demand | 4500 x 5400px | 300 | PNG |
| Printful | up to 4500 x 5400px | 300 | PNG |
| Printify | up to 4500 x 5400px | 300 | PNG |
| Redbubble | 2400 x 3200px min | 300 | PNG |
| Standard print area | 3600 x 4800px (12"x16") | 300 | PNG |
| Max DTG print area | 4500 x 5400px (15"x18") | 300 | PNG |

**Gotcha:** AI tools typically export at 72 DPI. Upscaling from 1024x1024 to 4500x5400 is an 8x jump -- artifacts will be visible. Generate at 4K resolution from the start to minimize upscaling.

---

## T2: Transparent Background (Native Alpha)

**kie.ai GPT-Image-2 supports native transparency via the `background` parameter.**
Pass `"background": "transparent"` in the API input. Output is true RGBA PNG. No post-processing.

**API body -- always include `background`:**
```json
{
  "model": "gpt-image-2-text-to-image",
  "input": {
    "prompt": "...",
    "aspect_ratio": "3:4",
    "resolution": "4K",
    "background": "transparent"
  }
}
```

**Prompt rules for transparency:**
- Say "no background" or "isolated design element" in the prompt
- NEVER say "on white background" -- white fill bakes into the design permanently
- Designs with intentional white fills (badge interiors, seal backgrounds) keep the white as design, alpha surrounds it

**Verify alpha:**
```python
from PIL import Image
img = Image.open("design.png")
assert img.mode == "RGBA"
```

**Reference:** keep a folder of your own approved reference designs to compare against

**Fallback if native transparency stops working:**
rembg at `D:\tools\rembg\` -- but it only strips OUTER background, not internal white fills

---

## T3: Color Profile and Format

**Rules:**
- Design in **sRGB** (IEC61966-2.1). All major POD platforms expect sRGB.
- Export as **PNG-24** with alpha. JPEG destroys transparency.
- **Never submit CMYK.** Platforms convert internally. Double-conversion causes color shift.
- SVG accepted by some platforms but not universal.

**Problem colors (RGB to print shift):**

| Color | What Happens | Mitigation |
|-------|-------------|------------|
| Bright neon | Significantly duller in print | Oversaturate by 10-15% or avoid |
| Electric blue | May shift purple | Test with print provider |
| Vivid orange | Loses vibrancy | Use burnt orange instead |
| Bright green | Mutes significantly | Use sage/forest green |
| Earth tones | Convert cleanly | Safe default |
| Black | Prints well | Best for text/outlines |
| White | Requires underbase on dark shirts | Some printers handle automatically |

**Safe palette approach:** Design with slightly more saturated colors than target, knowing they'll lose ~10-15% vibrancy in print. Or stick to muted/earth tones that convert cleanly.

---

## T4: Aspect Ratio Selection

| Use Case | Aspect Ratio | kie.ai Resolution | Notes |
|----------|-------------|-------------------|-------|
| Standard front-of-shirt | 3:4 | 4K | Closest to 12x16" print area |
| Chest/pocket design | 1:1 | 2K (not 4K!) | 1:1 cannot go 4K on kie.ai |
| All-over print | 16:9 | 4K | For specialty products |
| Tall/narrow design | 9:16 | 4K | Phone cases, bookmarks |

---

## T5: End-to-End kie.ai Pipeline

**Step-by-step for a single design:**

```python
# 1. Generate (with native transparency)
POST https://api.kie.ai/api/v1/jobs/createTask
Headers: Authorization: Bearer {API_KEY}
Body: {
    "model": "gpt-image-2-text-to-image",
    "input": {
        "prompt": "[ASSEMBLED PROMPT]",
        "aspect_ratio": "3:4",
        "resolution": "4K",
        "background": "transparent"
    }
}
# Returns: {"data": {"taskId": "..."}}

# 2. Poll for result
GET https://api.kie.ai/api/v1/jobs/recordInfo?taskId={taskId}
# Wait until state = "success"  (NOTE: field is "state", not "status")
# Parse resultJson -> resultUrls[]

# 3. Download image (already has alpha channel)
# Save to ./out/{design-name}.png

# 4. Quality check
# - Text accuracy
# - Edge cleanliness
# - Artifact checklist
# - 3-foot rule at print dimensions

# 6. Resize/verify
# - Should be 4500x5400px at 300 DPI
# - sRGB color profile
# - PNG-24 with alpha

# 7. Export
# Save to ./out/{design-name}-print-ready.png
```

**Cost per design:** ~$0.12-0.25 total (no bg removal needed)
**Time per design:** ~1.5-2 minutes (80-120s generation + manual QC)

---

## T6: Artifact Checklist (Pre-Export QC)

Run at 100% zoom before exporting ANY design:

- [ ] **Text:** Correct spelling, no extra/missing letters, consistent font weight
- [ ] **Edges:** Clean, no white halo or fringing around the design
- [ ] **Symmetry:** Logos/emblems balanced (flip horizontally to check)
- [ ] **Micro-text noise:** No tiny illegible text-like artifacts in textures
- [ ] **Gradient banding:** No visible color steps in smooth areas
- [ ] **Over-complexity:** Can you read it from 3 feet away?
- [ ] **Line weight:** Thin lines 2pt+ at print size (won't disappear on fabric)
- [ ] **Color safety:** No neon-dependent colors that will mute on fabric
- [ ] **Alpha channel:** True transparency, not white pixels
- [ ] **Dimensions:** 4500x5400px at 300 DPI minimum

---

## T7: Model Selection for Specific Design Types

| Design Type | Best Model | Why |
|-------------|-----------|-----|
| Typography-heavy | GPT-Image-2 | 95%+ text accuracy, best in class |
| Typography + illustration | GPT-Image-2 | Handles both text and art |
| Pure illustration | Midjourney or Flux | Higher aesthetic ceiling for non-text |
| Vintage/distressed | GPT-Image-2 | Follows texture instructions precisely |
| Minimalist line art | GPT-Image-2 | Follows "continuous line" well |
| Anime/manga | Midjourney Niji or Flux with anime LoRA | More authentic anime aesthetics |
| Fast iteration | nano-banana-pro (kie.ai) | ~$0.12/4K, fast turnaround |

**Default:** GPT-Image-2 via kie.ai for everything that includes text. Midjourney for pure illustration where text accuracy doesn't matter.

---

## T8: Copyright Safety Checklist

Before listing ANY design:

- [ ] No copyrighted character names in prompt (Disney, anime, Marvel, etc.)
- [ ] No specific artist names in prompt for commercial output
- [ ] Reverse image search the output (Google Images, TinEye)
- [ ] USPTO TESS search for any text/phrases used (common words CAN be trademarked in apparel)
- [ ] No trademarked slogans ("Let's Go Brandon", "Girl Boss", "Mama Bear" -- all trademarked)
- [ ] Parody designs reviewed for transformative use (parody is a defense, not a license)
- [ ] AI-generated images have limited copyright protection -- add human modification for stronger claim
