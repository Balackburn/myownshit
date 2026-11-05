# 03-potes-poissons: the drowned man's city under the sea, in the tornado style

The earlier short from the person's TikTok (script transcribed locally with whisper, three words fixed against its captions) rebuilt
in one pass with `.claude/skills/lowpoly-story-style`: 27 lines in the series' narrator voice, time-stretched ×1.10 and placed back to
back (46.7 s, `tools/timeline.json`); 32 shots by `absurd-shorts/scripts-fr/potespoissons_tornado.py` with the ocean props in
`absurd-shorts/engine/props_ocean.js` and the `seaSurface` / `seabed` sets; the replica's captions and card spring (three cards);
the tornado film's music bed with 68 effect cues, mixed to -16 LUFS.

Render: `npx --yes hyperframes@0.9.13 render -o renders/potes-poissons.mp4 --fps 30` (3D layer:
`node render/render3.mjs scripts-fr/potespoissons_render.json --timed --w 1080 --h 1920 --workers 4 --out out/potespoissons_3d.mp4`).
