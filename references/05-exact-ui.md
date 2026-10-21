# 05 · Exact UI (the part Adem checks hardest)

> **Goal** — every screen in the video is indistinguishable from the real app.
> **In** — component source, i18n, theme, screenshots · **Out** — `ui/exact_<screen>.py/.css`, `ui/icons/`, preview pages.

"Some details not the same" = rebuild that screen from the code again. Approximations are not acceptable.

## Rebuild a screen
1. Open the page component + every child it renders. Note layout (flex/grid, widths, gaps), tokens, radius,
   shadows, font per language, RTL handling, conditional states (empty, loading, AI generating, coming soon).
2. Labels: copy from the i18n json of the target language (e.g. `ar.json`). Keep strings the app leaves in
   English in English (and log it in CLIENT-QUESTIONS).
3. Icons: `python3 kit/extract_icons.py --out ui/icons/<surface> --tsx-exports … | --tsx-dir … | --svg-dir … |
   --iconify prefix:name,… | --mui <node_modules>:Name,…` (JSX→SVG handles `style={{}}`, template literals, conditionals). Inline the real SVG; never draw a substitute.
4. Demo data from STORY.md (names, numbers, emails exactly as the app formats them, e.g. `{jobId}@jobs.<brand>.com`).
5. One module per screen family: `ui/exact_<screen>.py` returning HTML strings + `ui/exact_<screen>.css`.
   Prefix classes per module (`xc-`, `xj-`, `xi-`, `xa-`) and give stable ids to every element the video will
   tap/animate (`xj-autofill`, `xc-continue`…). Parameters for states: `step=`, `filled=`, `coming_soon=`, `scroll=`.
6. Fixed canvases: laptop 1700×1104 (or the device quad's ratio), phone 374×~954; desktop + mobile variants
   when the surface has both (career page web + mobile).

## Verify (always, with a picture)
```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1700,1104 --screenshot=/tmp/x.png file://$PWD/ui/preview-exact-<screen>.html
```
Compare side by side with Adem's screenshot or the running app. Typical misses: wrong stat cards, select vs
tabs, donut colours, drawer side in RTL, modal width, wrapped pills (fix with nowrap), unstyled modal header.

## Parallelise
For several screens, spawn one agent per screen family with: the component paths, the spec file, the prefix,
the ids needed, and "verify with headless Chrome against <screenshot>". Review their screenshots yourself.

## Putting UI in the video
`kit/devices.py`: `device()` projects UI into a green-screen photo (homography → matrix3d), `cam()` pushes in,
`at_screen()` computes the tap point on the real control, `float_card()` lifts a card out at mobile width
(×1.6–2.6), `quad_video()` for clips inside screens (root level). `pfx()` / `scope_css()` avoid id/class clashes.
