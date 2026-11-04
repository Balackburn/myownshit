# The viral-video-writing loop, applied to "ce mec" shorts (French)

The `viral-video-writing` skill (installed next to this one) writes scripts that people watch to the end:
a hook that stops the scroll, a story arc, a re-hook every few seconds, no AI-sounding lines, and a checker.
This page says how to use it for our format. Read the skill's own files for the rules (`hook-craft.md`, `story.md`,
`retention.md`, `writing.md`, `checks.md`). Working examples: `absurd-shorts/scripts-fr/parking.py`, `pas.py`, `voisin.py`,
`photo.py` (each docstring maps the beats).

## The loop, step by step

1. **Facts sheet.** Our stories are fiction. Write that down: no real person, brand or company; generic institutions; every
   number is part of the joke, not a claim. Real places only as signposts.
2. **Shape.** Use the 7 story beats compressed onto our 8-beat formula:
   - decision (B1-B2);
   - the villain or doubter inside the first 10 s: a warden, a doctor, a neighbour, a rule;
   - the promise or open loop (he never leaves, he never turns, he never smiles again);
   - the grind, written as re-hooks: numbers and time jumps ("Le lendemain", "Trois ans plus tard");
   - the low point (the wife leaves, he sleeps in the cellar);
   - the turn;
   - the callback payoff: the same people or place, the opposite result.
3. **Five hooks per story.** Keep the formula "Ce mec a [verbe] [objet banal] pour [but banal]." and put a number or a named
   thing in the first two sentences. Pick the one that passes the most checks in `hook-craft.md`, not the one you like best.
4. **Three drafts,** each with a different hook or angle. Typical angles: chronological, before/after ("Ce mec vit sur une
   place de parking depuis douze ans."), and mystery ("Ce mec a reçu quatre mille amendes...").
5. **Score them** with `python3 .claude/skills/ce-mec-shorts/scripts/score_fr.py draft.txt ...`. The skill's own `score.py` is
   English-only: it doesn't recognise French number words, French filler or our dry tag.
   - The French checker keeps the hard fails: em dash, semicolon, "pas seulement... mais", "ce n'est pas X, c'est Y",
     filler, fake suspense, AI words, more than one one-word sentence.
   - It adds the ce-mec rules: starts with "Ce mec"; "ce con" and one "putain" (never two); an institution; a tag of 7 words
     or fewer.
   - It also checks that the end calls back to the start.
   Then run the manual checks in `checks.md`: is the doubter early, is there a low point, does it end on the last word?
6. **Rewrite** until 90+ with zero hard fails, and keep a short log of what changed.
7. **Deliver** the script, 2 alternate hooks, and a post caption: the hook line, then ONE CTA keyword, then 3-5 hashtags.

## What changes compared with the plain formula

- **Length.** 25-33 s and 10-11 lines, instead of 16-24 s. The arc needs the doubter, the low point and the callback. Every
  line is still one beat with its own image.
- **No CTA in the voice.** The deadpan tag stays the last word, then silence. The CTA goes in the post caption ("Commente
  PLACE si..."). The skill's "end on the last word" rule and our silent hold agree.
- **Make it loop.** Design the last shot to flow into the first:
  - the car circling the block again;
  - walking off over the roof, as he arrived;
  - the broom against a ceiling again;
  - the mugshot flash answering the photo-booth flashes.
  Replays count as watch time.
- **Visual pace.** Something moves on frame 0 (driving, marching, jabbing a broom, a flash), and there is a new shot every
  1.5-3 s. A new place is itself a re-hook: Poland, Siberia, the ocean, the Sécu in four lines.
- **Mute test.** The burned-in captions carry the words. Inserts carry the numbers: the pedometer at 9 999, the tax bill,
  the stamps "REFUSÉ" and "RADIÉ", the placard "N° 38". Don't add overlays (house rule).

## What not to take from the skill

- The CTA line in the voiceover.
- The "real proof / real footage" step: this is fiction, so the facts sheet says so instead.
- Long flowing 8-16 word sentences everywhere. Our deadpan needs some short lines; keep only the hard rule (at most one
  one-word sentence).

## `famous-reel-editor`

The other skill in the same pack edits raw talking-head footage (transcribe, cut, cards, karaoke captions). It does not
apply to the 3D engine. Use it only if the user brings a filmed clip, for example a face-cam reaction to one of the shorts.
