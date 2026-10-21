#!/bin/bash
# Scaffold a promo repo: new_project.sh <parent-dir> <name>   → <parent>/<name>-promo-video
set -e; K=$(cd "$(dirname "$0")/.." && pwd); P="$1/$2-promo-video"
mkdir -p "$P"/{00-bible,prompts,inbox/{img,vid,vo/stories,vo/youtube,music,devices},kit/assets/{fonts,brand,sfx},ui/{specs,icons},stories,youtube,delivery/{stories,youtube},.claude/skills/$2-promo}
cp "$K"/templates/bible/*.md "$P/00-bible/"
cp "$K"/scripts/{devices.py,prep_devices.py,prep_media.py,extract_icons.py} "$P/kit/"
cp "$K"/assets/gsap.min.js "$P/kit/assets/"; cp "$K"/assets/sfx/*.wav "$P/kit/assets/sfx/"
cat > "$P/.claude/skills/$2-promo/SKILL.md" <<EOT
---
name: $2-promo
description: Project specifics for the $2 promo series. Use with the promo-flow skill.
---
Follow ~/.claude/skills/promo-flow. Project specifics (world, cast, style, pinned CLI, paper colour) live in 00-bible/ — read BRAND-LOCK.md first.
EOT
printf "inbox/\ndelivery/\nstories/*/assets/\nstories/*/snapshots/\nnode_modules/\n" > "$P/.gitignore"
echo "created $P — next: put brand fonts in kit/assets/fonts, logos in kit/assets/brand"
