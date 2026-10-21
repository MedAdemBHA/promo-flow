# 07 · Check → look → render → review

> **Goal** — ship only what was looked at.
> **In** — a composition that passes `check` · **Out** — `delivery/…mp4`, duration + loudness, notes applied.

```
cd stories/STnn
npx --yes hyperframes@<pinned> check                       # must say "Check passed"
npx --yes hyperframes@<pinned> snapshot --at <one time per beat> --no-end --describe false
bash ~/.claude/skills/promo-flow/scripts/contact_sheet.sh /tmp/stnn.jpg snapshots/frame-*.png   # then Read it
```
Look for: wrapped headlines/tags, labels covering captions, objects under the stamp, empty frames at cuts,
caption wraps > 2 lines, wrong word sync. Fix in build.py, re-snapshot only the touched beats.

## Render
1. `df -h /` first — the render needs ~2–3 GB temp. If low, propose (don't do silently) `npm cache clean --force`
   and clearing `~/.cache/hyperframes` (both re-download).
2. `npx --yes hyperframes@<pinned> render -o ../../delivery/stories/STnn_<slug>.mp4` (background for long ones).
3. Loudness: `ffmpeg -i out.mp4 -af ebur128 -f null -` → target ≈ −14 LUFS.
4. Report: path, duration, LUFS, and anything still waiting (music, a regenerated clip, client answers).

## Review loop with Adem
Notes arrive short, in mixed FR/EN, often with screenshots. Ask for notes as `timecode + change` when unclear. Every note →
generator fix → re-snapshot → re-render that file only. Keep a short changelog in the story folder if the
round is big.

## YouTube film
Same engine at 1920×1080: one sub-composition per chapter (YT_00 … YT_14), each with its VO file; chapter
cards from the bible table; the long music bed in sections; render chapters, then the master.
