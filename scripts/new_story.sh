#!/bin/bash
# Scaffold a story composition: new_story.sh <repo>/stories/STnn [hyperframes-version]
set -e; K=$(cd "$(dirname "$0")/.." && pwd); P=$1; V=${2:-0.8.132}; R=$(cd "$P/../.." 2>/dev/null && pwd || true)
N=$(basename "$P"); mkdir -p "$P"/assets/{img,vid,audio,sfx,fonts,brand}
[ -d "$R/kit/assets/fonts" ] && cp "$R"/kit/assets/fonts/* "$P/assets/fonts/" 2>/dev/null || true
[ -d "$R/kit/assets/brand" ] && cp "$R"/kit/assets/brand/* "$P/assets/brand/" 2>/dev/null || true
cp "$K"/assets/gsap.min.js "$P/assets/"; cp "$K"/assets/sfx/*.wav "$P/assets/sfx/"
[ -f "$P/build.py" ] || cp "$K/templates/story_build.py" "$P/build.py"
cat > "$P/package.json" <<EOT
{ "name": "$(echo $N | tr A-Z a-z)", "private": true, "type": "module",
  "scripts": { "dev": "npx --yes hyperframes@$V preview", "check": "npx --yes hyperframes@$V check", "render": "npx --yes hyperframes@$V render" } }
EOT
cat > "$P/hyperframes.json" <<'EOT'
{ "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json", "paths": { "blocks": "compositions", "components": "compositions/components", "assets": "assets" }, "media": { "autoProxy": true } }
EOT
echo "{\"id\":\"$N\",\"name\":\"$N\",\"createdAt\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > "$P/meta.json"
echo "story ready: $P (edit build.py, then: python3 build.py && npx --yes hyperframes@$V check)"
