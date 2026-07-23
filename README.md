# davekindl / ai-media-producer

**Free AI skills from The AI Media Producer.**

Images, video, music, and merch — prompt to finished file.

Reusable, self-contained skills for AI coding agents. Built for **Claude Code**, usable by any capable agent. Part of the full [davekindl skills library](https://github.com/davekindl/skills).

## Install

```bash
# Claude Code — global, or swap ~/.claude for <project>/.claude
cp -r skills/<name> ~/.claude/skills/<name>
```

Any other agent: load `skills/<name>/SKILL.md` as instructions. Or point your agent at this repo and say *"read AI-START-HERE.md and integrate these"* — it installs them and interviews you to customize the ones that need it.

## The skills (7)

- `gpt-image-2-techniques` — 117-technique catalog for branded image generation *(needs API key)*
- `line-tapper` — precise lyric/subtitle timing
- `lyric-forge` — songwriting / lyric structuring
- `lyric-video-forge` — automated lyric videos (auto-timed)
- `lyric-video-studio` — manual-precision lyric videos (real footage)
- `pod-shirt-designer` — print-on-demand shirt design pipeline
- `video-prompt-builder` — cinematic AI-video prompts (Seedance & co.)

*"Needs setup"* skills interview you (or scan your repos) before first use — see [`AI-START-HERE.md`](AI-START-HERE.md). Skills that call paid APIs read keys from **your** environment — never hardcode or commit them.

## Using these

Take them, run them, adapt them. Attribution appreciated, not required.

— davekindl · NOTREPLACED
