# 02-vos-papiers: "Vos papiers" in the tornado style

The earlier 45 s French short "Vos papiers" (voice only, pauses between lines, muted palette) rebuilt with everything measured on
the tornado replica (`.claude/skills/lowpoly-story-style`):

- script transcribed from the earlier video with local whisper (`hyperframes transcribe -m small -l fr`), 27 lines, unchanged words;
- narration in the series' narrator voice (ElevenLabs, word timings), quotes read expressively, time-stretched ×1.08 and placed back
  to back (gaps 0.06-0.16 s): 45.6 s with no dead air (`tools/timeline.json`);
- 30 shots cut one frame before their opening word (1.0-2.4 s each), built by `absurd-shorts/scripts-fr/vospapiers_tornado.py` with
  the new props in `absurd-shorts/engine/props_vp.js` (cloud character, rain, Earth, map, border barrier, prison, signs) and sets
  `parisStreet`, `spaceDark`, `brightCell`;
- the replica's captions (Nunito 900, keywords in #D88168) and its THEFT-card spring for AGRESSION, VOS PAPIERS and GARDE À VUE
  (`tools/build_hf.py`);
- sound: the tornado film's music bed (its own background, separated from the voice) looped under the narration, synthesized effects
  on the visible actions, mixed to -16 LUFS.

Render: `npx --yes hyperframes@0.9.13 render -o renders/vos-papiers.mp4 --fps 30` (the 3D layer comes from
`node render/render3.mjs scripts-fr/vospapiers_render.json --timed --w 1080 --h 1920 --workers 4 --out out/vospapiers_3d.mp4`).
