# 04 · Intake — generated media arrive

> **Goal** — know exactly what is usable, what must be redone and what is still missing.
> **In** — new files in `inbox/` or `~/Downloads` · **Out** — files renamed to IDs in `inbox/`, a status table.

Adem drops batches in `inbox/img`, `inbox/img2`, `~/Downloads/*.mp4`, a `Generated Audio ….wav`, a pasted list
of Flow links. Your job: audit, map to IDs, report what's usable / wrong / missing. Copy, never move or delete
the originals without asking.

## 1 · Look at everything (contact sheets)
```
bash ~/.claude/skills/promo-flow/scripts/contact_sheet.sh <out.jpg> inbox/img/CHR*.png inbox/img/PST*.png
bash ~/.claude/skills/promo-flow/scripts/video_strip.sh  <out.jpg> ~/Downloads/*.mp4     # 6 frames per clip
```
Then Read the jpg. Check per group against the QC list in the prompts file (logo head shape, faces, flat bg,
accent colour, size). Sizes: `ffprobe` (no PIL/numpy needed).

## 2 · Map + rename
- Images: already named by ID → keep. Old sets that match a new ID 1:1 (e.g. IMG-10…18 → OBJ-01…09) → say so.
- Flow clips: names are descriptive ("Man_examining_stethoscope_…mp4"). Map by frames, not by name — the name can
  lie (one VID-08 clip showed a gas detector → flagged `VID-08_rakan-WRONG-….mp4`). Identical sizes = duplicate.
- VO: `inbox/vo/stories/STnn.wav`, `inbox/vo/youtube/YT_nn.wav`. Save the VO master doc into `00-bible/`.

## 3 · Report (table, French)
| Type | In inbox | Status |  → ✅ complete / ⚠️ to redo (why, which prompt) / ❌ missing (exact file names + where to save).
End with: what's already enough to build the next story.
