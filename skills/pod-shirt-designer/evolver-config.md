# POD Shirt Designer -- Design Quality Rubric & Improvement Guide

Use this rubric to evaluate generated designs and identify areas for improvement.

## Scoring Rubric (1-10)

| Score | Description |
|-------|-------------|
| 10 | Print-ready, text perfect, style authentic to niche, would sell on Merch by Amazon |
| 8-9 | Strong design, minor prompt tweaks needed (slightly off-center, one color too bright) |
| 6-7 | Good direction, needs refinement (text partially garbled, style generic, bg removal issues) |
| 4-5 | Mediocre -- looks like generic AI art, not niche-specific, wouldn't stand out on a POD platform |
| 1-3 | Broken -- photorealistic fail, completely wrong style, text unreadable, background not removable |

Auto-fail conditions:
- Text is garbled or has extra/missing letters
- Design fails the 3-foot readability rule
- Background cannot be cleanly removed
- Triggers the "photorealism trap" anti-pattern
- Contains accidental copyrighted material

## Evaluation Set

For each evolution run, test these 5 representative prompts:
1. Typography hybrid badge (S1) -- the baseline seller
2. Anime streetwear (N1-B) -- the high-growth niche
3. Fictional brand seal (S7) -- the emerging trend
4. Hungarian text design (U1) -- the diacritics stress test
5. Minimalist line art (S8) -- the simplicity challenge

## Hypotheses to Explore

- Adding "screen print aesthetic" to all prompts improves fabric readability
- Specifying exact color hex codes (not names) produces more consistent palettes
- Adding "no more than 4 design elements" prevents over-complexity
- Specifying "2pt minimum line weight" prevents disappearing-detail issues
- Adding "typography hierarchy: primary text 3x larger than secondary" improves text layouts

## Stopping Conditions for an Improvement Loop

- 5 consecutive non-improvements
- Score >= 9 sustained for 3 runs
- 50 experiments total
