---
name: promo-flow
description: Adem's own promo-video flow (born on two shipped promos) — turn any app repo into a promo series (10 vertical stories + 1 YouTube film ~5 min) built from the app's EXACT live UI, a brand-derived collage world, generated layers (images, Flow clips, VO) and HyperFrames. Use when Adem says "promo", "stories", "video for <app>", "episodes", "YouTube film", drops generated assets ("images done", "video done", a VO wav), or asks to continue/render a story.
---

# promo-flow — Adem's way

One engine, a new world every time. The engine (steps, kit, pitfalls) is reused; the **look, story, cast, language and
dialect always come from the project in front of you** — never from a previous project.

## How Adem works (apply every turn)
- Talk French (short, direct); code, files, prompts and commits in English. Prompts for image/video tools stay in English.
- Before editing > 2 files: short plan, wait for "go". Trade-offs ≤ 3 bullets.
- "Exact" means exact: every UI pixel, label, icon and behaviour comes from the code. If a detail was guessed, it is wrong.
- Unsure business rule / claim / number → `00-bible/CLIENT-QUESTIONS.md` with the default you used. Never invent features.
- Adem generates the media (GPT Image / Codex, Google Flow, a TTS tool) and drops them in batches; you audit,
  rename, prep and build. Never mention tool usage/allowance.
- Show, don't tell: contact sheets and snapshots before claiming something looks right.

## 0 · Where are we? (pick the first row that matches, then read only that reference)
| Project state | Do | Read |
|---|---|---|
| No `00-bible/` yet | Study the app → write the bible | `references/01-study.md`, `references/02-bible.md` |
| Bible exists, no `prompts/` | Derive the style → write generation prompts | `references/03-style-and-prompts.md` |
| Adem dropped images / clips / wav (inbox or ~/Downloads) | Audit with contact sheets → rename to IDs → list what's missing / wrong | `references/04-intake.md` |
| UI not rebuilt yet (or "not the same details") | Rebuild the exact UI from code | `references/05-exact-ui.md` |
| Assets + VO for a story are in | Build the story composition | `references/06-compose.md` |
| Composition exists | check → snapshot → render → review | `references/07-render-review.md` |

## The repo shape (create it once: `scripts/new_project.sh <dir> <name>`)
```
<name>-promo-video/
  00-bible/   BRIEF · BRAND-LOCK · STORY · VO-SCRIPTS (or VO-MASTER) · ASSET-MANIFEST · CLIENT-QUESTIONS
  prompts/    CODEX-IMAGES · FLOW-VIDEOS · MUSIC (+ versioned files like IMAGES-V3-CAST when a set is redone)
  inbox/      img/ vid/ vo/stories vo/youtube music/ devices/      ← Adem drops here, exact IDs
  kit/        devices.py prep_devices.py prep_media.py extract_icons.py + assets/ (fonts, brand, sfx, gsap)
  ui/         specs/*.md · icons/<surface>/*.svg · exact_<screen>.py/.css · preview-*.html
  stories/STnn/  build.py → index.html, assets/ (copied, never symlinked)
  youtube/    YT01 (chapters as sub-compositions)
  delivery/   stories/STnn_<slug>.mp4 · youtube/
  .claude/skills/<name>-promo/SKILL.md   ← only project specifics + a pointer to this skill
```

## Non-negotiables (paid for on the first two projects)
1. **Real UI, live** — HTML/CSS rebuilt from the React/Flutter source + i18n strings + demo data that matters. Screenshots are references only.
2. **Icons are extracted, never generated** (`scripts/extract_icons.py`).
3. **Generated media = layers**, not finished pictures: characters, tools, sketches, paper, green-screen devices, short clips. The video assembles them, so everything can move.
4. **Captions = the exact VO lines.** If VO text changes, captions change.
5. **Every timing is measured** from the real wav (`scripts/vo_timing.sh`), never estimated.
6. **Fix in the generator** (`build.py` / `ui/*.py`), never by hand in `index.html`.
7. **Look before you say done**: snapshot every beat, read the contact sheet, fix overlaps/wraps.
