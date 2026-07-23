# AI-START-HERE — davekindl / ai-media-producer

> **Human?** This file is for your AI assistant. Point Claude Code, Codex, or any capable agent at this repo and say *"read AI-START-HERE.md and integrate these skills."* It installs them and interviews you to customize the ones that need it.

---

## FOR THE AI AGENT READING THIS

You've been pointed at the free AI skills from **The AI Media Producer** (7 skills). Install the ones the user wants, and **customize the ones that need per-user context by interviewing the user** — don't guess their niche, projects, or config, and never invent credentials.

### Step 1 — Install

- **Claude Code:** copy each chosen `skills/<name>/` into `~/.claude/skills/<name>/` (global) or `<project>/.claude/skills/<name>/`. Live next session.
- **Codex / other:** load `skills/<name>/SKILL.md` as instructions when the task arises.

Ask the user which skills they want; confirm each install.

### Step 2 — Customize (interview — the important part)

Most skills are **runtime-interactive**: they ask for what they need when you run them. A few need to know something about **this user** first. For each such skill the user installed, offer two paths and let them choose:

> **A) Scan & infer** — "Point me at your repo(s); I'll read them to propose the config, then confirm each value."
> 
> **B) Answer a few questions** — "I'll ask you N short questions."

**Always confirm before writing config.** Store it in the skill's own config or the user's project — never back into the public `SKILL.md`.

#### Skills that need a secret (a key, not an interview)

Set as env vars before first run — never hardcode or commit:

- `gpt-image-2-techniques` → KIE_AI_API_KEY (kie.ai)
- `lyric-video-forge` → the transcription/image provider keys per its SKILL.md

If a key isn't set, tell the user which env var to set — don't proceed blind.

### Step 3 — Integrate & report

Note how they compose with what the user already has; give a one-screen summary (installed / customized / ready / best first command).

---

## A note on placeholders

These skills are shipped **de-personalized**. Any `[Your Name]`, `[Your Brand]`, `acme-consulting`, `<projects-root>`, or example niche is a **placeholder** to replace with the user's real values via the interview above — never a real credential.

---

davekindl · NOTREPLACED
