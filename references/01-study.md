# 01 · Study the app (read-only)

> **Goal** — know the product well enough that every frame traces back to a file in the repo.
> **In** — the app repo(s), landing, campaign material · **Out** — `00-bible/BRIEF.md`, `ui/specs/<surface>.md`, first client questions.

## Find the surfaces
List the repo: every front-end is a surface (e.g. a recruiting app: `frontend/bo` back office, `frontend/jobs` career portal,
`frontend/assessment` candidate test app, `landingPage`; a coaching app: coach web app + client mobile app). Also look for
`docs*/`, `FEATURES.md`, `README`, Figma links, campaign posters, landing copy, blog/vlog pages.

## One Explore agent per surface, in parallel
Ask each agent for (paths + short excerpts, not dumps):
- Purpose, user roles, the 5–8 journeys worth filming, their routes/pages and component files.
- AI features (exact trigger, loading state, output shape) and which ones are **coming soon / disabled / flagged**.
- Theme tokens (colors, radius, shadows, spacing), fonts per language, logo files, favicon.
- i18n files for the target language (path + key naming) — labels are copied from here.
- Icon system (local SVG components, Iconify ids, MUI icons) — feeds `extract_icons.py`.
- Demo/seed data, enums (pipeline stages, statuses, scores), anything hard-coded in English.
- Mobile vs desktop layouts (breakpoints) for each filmed page.

## Then write down the gaps
Every mismatch between marketing and code (feature hidden in the sidebar, "coming soon" pill, English-only card,
calendar bug, missing email domain…) goes to `CLIENT-QUESTIONS.md` with the default you'll use. These were real
on the first project (AI question generation coming soon, HITL card in English, «12 ص» noon label, Monday week start).

## Brand sources (for 03-style)
Collect: landing tokens, app themes, logo variants (wordmark + symbol), existing campaign posters/ads (Adem may paste
images). The campaign look beats the app look for the collage world; the app look is only for UI.

## Output
`00-bible/BRIEF.md` (see 02-bible) + `ui/specs/<surface>.md`: layout, tokens, labels (exact strings), icons, states,
per screen we will film.
