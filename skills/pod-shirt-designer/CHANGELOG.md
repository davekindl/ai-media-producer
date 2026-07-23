# pod-shirt-designer Changelog

## v1.0.2 -- 2026-05-29 -- Consistency + Publish-Readiness Pass
- Resolved native-transparency contradiction: `techniques/_index.md` (T2/T5) and
  `pod_pipeline.py` (docstring, log line, `estimate_cost`) still implied rembg
  post-processing left over from the v1.0.0 design; all now match the native-alpha
  model already in `SKILL.md`, library file 05, and the v1.0.1 fix
- Removed phantom $0.05 bg-removal add-on from `estimate_cost`; cost band is now
  generation-only (~$0.12-0.25), consistent across SKILL.md and the Cost Model table
- Added `disable-model-invocation: true` to frontmatter -- each run spends ~$0.12-0.25
  of kie.ai credits, so the skill is invoked explicitly, not auto-triggered
- Authored `research-dossier.md` (previously referenced in the Architecture tree but
  missing on disk); consolidates source provenance by type from the build record
- Added "Bulk Runs (Batch Submit, Then Poll)" guidance to SKILL.md -- submit all
  tasks first, then poll, to overlap async generation wall-time across a batch

## v1.0.0 -- 2026-05-16 -- Initial Build (Phase 1 Draft)
- Built via niche-skill-forge methodology
- 45+ prompt templates across 5 categories
- 10 design styles, 6 trending niches (deep dives), 10 untapped prospects
- 8 technical pipeline techniques
- 50+ sources across POD platforms, Reddit, YouTube, market research
- Includes pod_pipeline.py (kie.ai API client + bg removal workflow)
- Status: DRAFT -- awaiting manual validation via test-prompts.md

## v1.0.1 -- 2026-05-16 -- Transparency Fix
- CRITICAL: Discovered kie.ai GPT-Image-2 supports native `"background": "transparent"` parameter
- Removed entire rembg post-processing pipeline (was only stripping outer bg, not internal white)
- Hardcoded `"background": "transparent"` in pod_pipeline.py and all 74 prompt templates
- Updated all prompts: "isolated on solid white background" -> "no background, transparent, isolated design element"
- Archived v1 white-bg test results to archive-v1-white-bg/
- v4 reference designs confirmed as the gold standard

### Research Sources
- POD trending niches: 28+ sources (Printify, Printful, Etsy, Amazon Merch, Grand View Research)
- Design techniques: 21 technique cards (fal.ai, OpenArt, Aiarty, kie.ai docs)
- Untapped niches: 41 searches (Magyar Peter, eldest daughter, vibe coding, dumbphone, etc.)
- Market data: $11-13B POD market (2025), 25.8% CAGR

### Niches Covered
**Trending:** Anime ($3.3B), Fitness ($295B), Pet ($1.5B), Vintage/Retro, Profession/Micro-Community, AI/Tech Culture
**Untapped:** Magyar Peter (HU), Eldest Daughter Syndrome, Vibe Coding, Dumbphone Identity, Micro-Retirement, Hungarian Expressions, Sleepmaxxing, Analog Renaissance, Neo-Homesteader, Solarpunk
