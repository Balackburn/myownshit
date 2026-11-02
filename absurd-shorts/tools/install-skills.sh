#!/usr/bin/env bash
# Installs the third-party video/animation skills used alongside ce-mec-shorts into ~/.claude/skills.
# Read each repo before trusting it: skills are instructions + scripts that run with your agent.
set -euo pipefail
SRC="${SKILLS_SRC:-$HOME/.claude/skills-src}"; DEST="${SKILLS_DEST:-$HOME/.claude/skills}"
mkdir -p "$SRC" "$DEST"
clone() { [ -d "$SRC/$2" ] || git clone -q --depth 1 "https://github.com/$1" "$SRC/$2"; }
clone LottieFiles/motion-design-skill motion-design-skill
clone angrypenguinpng/blender-claymation-skill blender-claymation-skill
clone greensock/gsap-skills gsap-skills
clone remotion-dev/skills remotion-skills
clone heygen-com/hyperframes hyperframes
clone tuzhechen2005/opus-video-skills opus-video-skills
clone Leonxlnx/earshot earshot
clone lemomo-ai/lemo-opuscar lemo-opuscar
clone JohnHeibel/ClaudeAnimationBase ClaudeAnimationBase        # reference app (p5.js), not a skill
clone ahujasid/mcp-for-blender mcp-for-blender                   # MCP server + Blender addon (needs Blender 4.2+ GUI)
clone zhuyansen/awesome-claude-video-skills awesome-claude-video-skills   # curated list, docs only
install_dir() { local d="$1"; local n; n=$(basename "$d"); rm -rf "$DEST/$n"; cp -r "$d" "$DEST/$n"; echo "installed $n"; }
install_dir "$SRC/motion-design-skill/skills/motion-design"
install_dir "$SRC/blender-claymation-skill" && mv "$DEST/blender-claymation-skill" "$DEST/blender-claymation" 2>/dev/null || true
for d in "$SRC"/gsap-skills/skills/*/ "$SRC"/remotion-skills/skills/*/ "$SRC"/hyperframes/skills/*/ \
         "$SRC"/opus-video-skills/skills/*/ "$SRC"/earshot/skills/*/ "$SRC"/lemo-opuscar/plugin/skills/*/; do
  [ -f "$d/SKILL.md" ] && install_dir "${d%/}"
done
rm -rf "$DEST/blender-claymation/.git"
echo "done. MCP for Blender (optional, Blender 4.2+ with a GUI): uvx mcp-for-blender setup"
