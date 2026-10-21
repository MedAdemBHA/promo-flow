# promo-flow

**Turn any app repo into a promo video series — built from the app's real UI.**

A personal [Claude Code](https://claude.com/claude-code) skill, distilled from two shipped projects.
One engine, a new world every time: the steps and tools are reused, while the look, story, cast and language always come from the project you are working on.

---

## What it makes

| Deliverable | Format |
|---|---|
| 10 vertical stories, one feature each | 1080×1920 · 20–28 s |
| 1 YouTube film in chapters | 1920×1080 · ~5 min |

Every screen in the videos is the product's **exact UI**, rebuilt live from the source code (labels, icons, states). There are no screenshots.

---

## The flow

```
  study ──▶ bible ──▶ prompts ──▶ intake ──▶ exact UI ──▶ compose ──▶ render
   code      story     images     audit      from code    HyperFrames  check · look · ship
   brand     cast      clips      rename     real icons   VO-timed
   gaps      VO        VO · music  report     verified     collage
```

| Step | What happens | Output |
|---|---|---|
| **1 · Study** | One agent per surface reads the code: journeys, AI features, tokens, i18n, icons, what's not shipped | `ui/specs/`, `BRIEF.md` |
| **2 · Bible** | A world with a deadline and a number, a cast tied to features, dialect VO | `00-bible/` |
| **3 · Prompts** | The style is derived from the brand; media are generated as **layers** (characters, tools, sketches, paper, green-screen devices) | `prompts/` |
| **4 · Intake** | Contact sheets of every batch, mapped to IDs, list of what to redo or what's missing | `inbox/` |
| **5 · Exact UI** | Screens rebuilt from components + i18n + extracted SVG icons, checked in headless Chrome | `ui/exact_*.py` |
| **6 · Compose** | `build.py` generates the composition, timed on the real voice; captions are the exact VO lines | `stories/STnn/` |
| **7 · Render** | check → snapshots → render → loudness → review loop | `delivery/` |

The skill detects where a project stands and resumes at the right step.

---

## Install

```bash
gh repo clone MedAdemBHA/promo-flow ~/.claude/skills/promo-flow
```

Requires `ffmpeg`, `python3`, `node` (for `npx hyperframes`) and Google Chrome.

## Use

Open any app repo in Claude Code and say:

```
promo            video for <app>            /promo-flow
images done      here is the VO for ST02     render ST01
```

---

## Inside

```
promo-flow/
├── SKILL.md                     entry point: rules + "where are we?" router
├── references/
│   ├── 01-study.md              read the app, find the gaps
│   ├── 02-bible.md              brief, brand lock, story, VO, manifest, client questions
│   ├── 03-style-and-prompts.md  brand → style → layered image / clip / music prompts
│   ├── 04-intake.md             audit and map what was generated
│   ├── 05-exact-ui.md           rebuild screens from code, verify
│   ├── 06-compose.md            beat grammar, timing, HyperFrames rules
│   └── 07-render-review.md      check, look, render, review
├── scripts/
├── templates/
│   ├── bible/                   6 starter files
│   └── story_build.py           reference story (ST01)
└── assets/                      GSAP + SFX
```

### Scripts

| Script | Does |
|---|---|
| `new_project.sh <dir> <name>` | scaffold a full `<name>-promo-video` repo |
| `new_story.sh <repo>/stories/STnn` | scaffold a story (pinned CLI, fonts, brand, sfx, build.py) |
| `prep_media.py --story … --img … --vid … --vo …` | lift images to white, key `#FF00FF` paper, clips to 1080×1920 @30, VO to −16 LUFS |
| `prep_devices.py` | key green screens, measure the screen quads → `devices.json` |
| `devices.py` | project live UI into device photos, camera moves, taps on real controls |
| `extract_icons.py --out … --tsx-exports / --tsx-dir / --svg-dir / --iconify / --mui` | app icon components → clean SVG |
| `vo_timing.sh <wav>` | speech ranges per line and per word, no Whisper needed |
| `contact_sheet.sh` · `video_strip.sh` | visual audit of images and clips |

---

## Principles

1. **Real UI, live.** It is rebuilt from the code and verified. A guessed detail counts as a wrong detail.
2. **Icons are extracted, never generated.**
3. **Generate layers, assemble in the video**, so everything can move.
4. **Captions are the exact VO lines.** Timings are measured, never estimated.
5. **The scenario and the look belong to the brand.** Nothing is reused from a previous project.
6. **Unknown business rules become client questions.** Never invent a feature.
7. **Fix in the generator, never in the output.**
8. **Look before saying done.** Every beat gets a snapshot.

---

<sub>Private · built and maintained by Adem</sub>
