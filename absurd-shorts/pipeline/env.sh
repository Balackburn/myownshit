#!/bin/bash
# env.sh: sourced by every pipeline script. PIPE = the session's work dir (drafts, logs, TTS, critic folders); never inside the repo.
PIPE=${PIPE:-/tmp/pipe}
PIPELINE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd "$PIPELINE_DIR/.." && pwd)
REPO=$(cd "$ROOT/.." && pwd)
SKILL_SCRIPTS=$REPO/.claude/skills/lowpoly-story-style/scripts
mkdir -p "$PIPE/s7" "$PIPE/critic/configs" "$PIPE/critic/specs"
export PIPE PIPELINE_DIR ROOT REPO SKILL_SCRIPTS
