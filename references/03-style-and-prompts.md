# 03 · Style + generation prompts (`prompts/`)

> **Goal** — a look that belongs to the brand, and prompts that produce clean, composable layers.
> **In** — BRAND-LOCK draft, brand material · **Out** — `prompts/CODEX-IMAGES.md`, `FLOW-VIDEOS.md`, `MUSIC.md`, finished BRAND-LOCK.

## Derive the style from the brand (never from the last project)
1. Look at the brand's campaign material first (posters, ads, landing hero). Name the look in 3 words
   (e.g. "editorial halftone collage", "calm paper + devices").
2. Extract tokens: paper/background, primary, strong (text-safe), ink, accent for AI moments, alert.
3. Decide the **character treatment** with Adem (ask once, show 2–3 options):
   - **Headless brand-symbol head** (Adem's favourite so far): real outfit in B&W halftone, invisible body,
     the logo symbol as a glossy 3D head; hats float above it. Brand on every frame, no face issues, no likeness risk.
   - Faces (AI people) — only if the client wants humans; add a CLIENT-QUESTION.
   - Objects only — for very abstract products.
4. Write it into BRAND-LOCK before any prompt.

## Generate LAYERS (one subject per image, exact ID file names)
| Prefix | What | Format | Notes |
|---|---|---|---|
| CHR- | characters (style block + attach the logo symbol as reference) | 1024×1536, team 1536×1024 | flat bg, no border, 8 % margin |
| PST- | hero poster per character (optional; video can compose it) | 1080×1080 / 1920×1080 / 1280×720 thumb | leave 40 % empty for headline |
| TL- | profession tools, B&W halftone + ONE part in brand colour, white cut border | 1024×1024 | |
| SK- | pencil sketches in the brand's dark tone on flat paper, no text | 1024 (wide ones 2048×512/1024) | draw-on / wipe reveal |
| OBJ- | glossy studio objects for chapter openers | 1024×1536 | |
| PP- | paper texture + torn strips/tape/ticket on **#FF00FF** for keying | | |
| DEV- | devices with **pure #00FF00** screens (laptop, phone, hand+phone per sleeve) | | prep_devices measures the quad |

Every style block ends with: flat background colour, no text, no logo (except the head), no watermark.
Write a **QC checklist** under each group (shape of the logo head exact, no skin, flat bg, one accent colour) —
Adem regenerates only what fails. When a set is redone, add a versioned file (`IMAGES-V3-CAST.md`), don't rewrite history.

## Flow clips (FLOW-VIDEOS.md)
Ingredient = a poster/character/object image. One motion sentence + a shared suffix that locks the style
("keep the halftone outfit, keep the logo head's exact shape, never a face, cream bg, subtle motion, no text").
Flow returns ~6 s 720×1280 (or 1280×720) with descriptive names → intake renames them by looking at frames.

## Music (MUSIC.md)
One bed for stories (~25 s loopable), one long bed for YouTube in sections matching chapters; SFX list
(stamp, paper tear, pop, whoosh, chime, sparkle only for AI). Keep beds under the VO (−18 dB under).

## VO
Adem pastes each code block into the TTS tool (one file per block). Ask for 48 kHz if possible (24 kHz mono is OK;
prep upsamples + loudnorm).
