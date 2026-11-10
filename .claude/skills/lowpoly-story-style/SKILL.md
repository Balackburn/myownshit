---
name: lowpoly-story-style
description: Make a vertical low-poly 3D story short in one pass, in the measured style of the "man lost his dog in a tornado" reference (the tornado replica): deadpan narration with no pauses, a cut every 1-2 s, low moving cameras, bright sky and pastel sets, snappy characters with lip flaps and blinks, pop-in signs, the replica's captions and title-card spring, a music bed and effects on the actions, mixed to -16 LUFS. Use it to remake an existing short (script from a video) or to produce a new story in this style, in French or English, with the absurd-shorts engine and HyperFrames.
---

# Low-poly story shorts in the tornado style (one pass)

Everything here was measured on the reference over 50+ replica passes (`hyperframes/01-tornado-reverse/REVERSE.md`,
`.claude/skills/tesseract-replica/references/lessons.md`) and proven on a full remake (`hyperframes/02-vos-papiers`).
Follow the numbers; don't re-derive them.

Read, in this order:
1. `references/style-bible.md`: what the style is, in numbers (pacing, cameras, palette, grade, characters, captions, cards, sound).
2. `references/shot-library.md`: the shot types with engine snippets (copy, then adapt the coordinates).
3. `references/production.md`: the one-pass pipeline, command by command, with the QA gates.
4. `references/pitfalls.md`: what went wrong on the first stills of a new story and how to avoid it.
5. `references/sand3d-models.md`: when the engine lacks an object, search the sand3d datasets (about 100 000 objects as programs,
- `references/shader-look.md`: new stories use `Story(name, look='natural')`: light bounced from the scene (a probe per shot), soft shadows, auto exposure, ambient occlusion, bloom, haze; `look='shaders'` is the harder Minecraft-with-shaders variant. Per-shot `look={...}` controls; point the sun at the faces.
- `references/tesseract-render.md`: rendering a whole story with Tesseract's path tracer (shots baked from the engine, one Scene3D layer per shot): settings, costs (~1.5 h for 22 s at 720p/15 fps here) and what is lost.
- `references/cartoon-rig.md`: the cartoon rig and the animated face (opt-in, `st.write(..., rig='toon')`): squash and stretch, limbs that bend and stretch, takes, eyes that lead the head, blinks over several frames, the channels a story can key, the clips, the tests. Use it for every new story; the two sections at the end of this file list the gags already used (never reuse one as is) and the mistakes already made.
- `references/faces-and-fx.md`: every character wears the hero's face with variations (glasses, moustache, beard, lipstick, skin tone), 56 expressions, automatic micro-animation, face FX (wet hair and drops, tears, sweat, blush, shiver) and FLUX-generated textures. Give every beat a playing expression and use FX whenever the situation calls for it (rain = wet).
   CC BY 4.0), build a GLB and use it with the `glbModel` prop.

Rules that always apply:
- The ElevenLabs key lives only in the environment (`ELEVENLABS_API_KEY`), never in a file, a commit or this skill. Use the narrator
  voice configured in the project (`absurd-shorts/scripts-fr/actu_common.py`, `VOICE`): one voice for narration and quotes, quotes
  with the expressive settings. Never imitate a real person's voice.
- Satire: aim at the absurd institution or at the prejudice, never make an ethnicity the butt of the joke.
- Use music only from sources the person owns or a licence allows (here: the separated bed of their own reference film). Never
  download copyrighted music.
- Commit sources, the timeline, the final mix and the 3D layer the composition needs; never `out/`, `renders/` or the TTS cache.
- A missing object: search sand3d first (`references/sand3d-models.md`), model by hand only when nothing fits. Run dataset programs only
  through `sand3d_models.py build` (it refuses anything but sand3d calls), and keep their CC BY 4.0 credits with the story.

Scripts (in `scripts/`, run with `python3`):
- `place_narration.py LINES.json TTS_DIR OUT.json [--atempo 1.08]`: back-to-back placement and word timings.
- `build_hf.py TIMELINE.json PROJECT_DIR --cards "A04:AGRESSION,..."`: the captions composition and title cards.
- `mix.py`: voice + music bed loop + effect cues to a -16 LUFS mix (edit the cue list per story).
- `motion.py REF.mp4 OURS.mp4 OUTDIR`: residual (non-camera) motion per shot, to find shots that freeze.
- `sand3d_models.py find|search|get|build|credits`: find a ready-made 3D object in the sand3d datasets, build it to a GLB (in a
  checked, isolated process) and credit it; see `references/sand3d-models.md`.

## Catalogue de gags et techniques

Section tenue à jour à chaque cycle (voir `absurd-shorts/JOURNAL.md`). La structure des histoires ne change pas (accroche qui nomme le mec
et l'événement absurde, logique absurde poussée pas à pas par une institution, escalade, retournement, aparté sec) ; seule la mise en
scène évolue. **Au moins 5 gags visuels par histoire, chacun appuyé sur le rig ; ne jamais réutiliser un gag à l'identique** : reprendre
la technique, changer la situation, le rythme ou la chute. Les numéros renvoient à l'histoire où le gag a servi.

| Gag | Technique (moteur) | Servi dans |
| --- | --- | --- |
| Temps suspendu avant la chute | il marche sur le vide (`then=<la même marche>` : la marche continue), s'arrête ; les yeux descendent, puis la tête (`hangAir` : `downAt`, `usAt`), regard caméra (`gulp`), chute | 37 (quatre chutes, quatre façons, ci-dessous) |
| Chute « caramel » : les jambes partent, la tête reste | clés `toon` : jambes et tibias ×2,7 en 0,17 s, puis cou ×9 pendant 0,08 s pendant que le corps descend, puis tout claque | 37 S02 |
| L'objet qui reste en l'air | l'accessoire se détache (`detach`), attend 0,4 s, puis tombe (`fall`) : le téléphone, le képi (prop à part ; le chapeau du rig sort du champ avec `hat: [60, 0, 0]`) | 37 S02, S07 |
| Chute « pierre » après un take | `lookDown` + cou ×2,2, `take` court (0,12 s), chute en 0,13 s | 37 S07 |
| Freinage au bord et moulinets | `dashOff` (traînée), `skidStop`, `teeter` (bras en tuyaux, amplitude qui grandit) | 37 S08 |
| Descente d'ascenseur, digne | chute linéaire lente, sourire `teeth`, `wave`, bras ×1,9 pour que la main reste la dernière | 37 S10 |
| Crêpe puis regonflage | chute glissée puis `pancake` (`popAt`, `stars`), secousse caméra, poussière | 37 S03 |
| Bosse sur le crâne | `face.bump`, tête écrasée `scl.head [1.3, 0.62, 1.3]` pendant 0,05 s, expression `pain` | 37 S03 |
| Regard à gauche, regard à droite, take | expressions `sideL` puis `side` (0,22 s chacune), puis `take` (`pop: 0` : yeux peints géants, mâchoire étirée) | 37 S05 |
| Atterrissage en accordéon, les voisins tremblent | `accordion` (`decay`, `stars`), `jelly` sur les voisins au même instant | 37 S09 |
| Serrés comme des sardines, respiration en tuyaux d'orgue | `squeezed` + `sq [0.74, 1.08, 0.9]` ; ils inspirent l'un après l'autre (0,09 s d'écart) : plus fins et plus hauts `sq [0.6, 1.26, 0.9]`, joues gonflées (`puffed`), puis relâchent ensemble | 37 S12 |
| Bras élastique | `reachUpL` + bras et avant-bras ×3 (0,24 s), retour sec | 37 S13 |
| Yeux en euros en cascade | expression `greed` décalée de 0,05 s par personnage, petit bond (`sq` y 1,2) | 37 S14 |
| Plongeons variés | `noseJump`, `cannonball`, `swanDive` sur un déplacement avec `arc` | 37 S15 |
| Colonne humaine | les arrivants s'empilent en étages, la rangée du dessous s'écrase à chaque arrivée | 37 S16 |
| Cou périscope | `periscope` (`len: 10`), regard vers un personnage puis caméra, `deadpan` | 37 S18 |
| Fonte de dépit | `melt`, la valise tombe (`detach`, `fall`) | 37 S18 |

Gags du rig pas encore servis : yeux sur tiges prolongés (`pop`), langue déroulée, vapeur aux oreilles, étoiles longues, `paperThin`,
`inflate`, `noodle`, `scramble` avant un départ, `stretchGrab` horizontal, `doubleTakeToon`, expressions `zap`, `strain`, `puffed`,
`dotEyes`.

## Erreurs à éviter

- `then` est ignoré sur un déplacement `glide` (chute, glissade) : poser une clé de clip explicite à la fin (`k(t, clip='pancake')`).
- Une graine par défaut donne des lunettes (rouges) à tout le monde : un `seed` distinct ou `glasses: False` par personnage.
- Le cou mesure 0,1 m : ×3 ne se voit pas. La colonne s'étire vers le haut depuis le bassin : pour qu'une tête reste en place pendant
  que le corps tombe, étirer les jambes puis le cou, pas la colonne.
- Un take grandit le corps de 16 % et la tête de 26 % : laisser de l'air au-dessus, ou faire monter la caméra.
- Les yeux sur tiges suivent l'axe de la tête : tête renversée et caméra basse les font sortir au-dessus du crâne. Garder la tête face caméra.
- La bouche `scream` à petite ouverture ressemble à un rire : sous `jaw` 0,45 le moteur met `O`.
- Un tampon posé à plat sur un bureau est illisible à hauteur d'œil : faire surgir le document face caméra (pop-in), ou tamponner un support vertical.
- 9:16 : demi-angle horizontal de 12,8° à 44. Un panneau de 1,5 m demande 5 m de recul ; vérifier que chaque élément clé (panneau,
  retardataire, pancarte) est dans le cadre sur une image de contrôle avant le rendu.
- Les accessoires animés placés dans un décor ne bougent que si le décor relaie leur `userData.update`.
- Personnages serrés : les clips à bras écartés (`accordion`, `take`) traversent les voisins ; préférer `squeezed` et les canaux `toon`.
- Un pop-in à l'échelle (`k(0.0, scale=0.01)` puis `k(t, scale=1)`) rétrécit l'objet pendant 0,4 s au début du plan : donner `scale=0.01` à l'accessoire lui-même et ne poser que la clé d'apparition.
- Un regard vers un mur à 90° montre la tête de profil et cache le visage peint : viser une cible à 40° environ (trois quarts) et laisser les yeux faire le reste.
- Une largeur de rendu impaire bloque l'encodeur (le rendu reste figé sans erreur visible) ; `render3.mjs` arrondit maintenant au pair.
- Un plan où personne ne bouge pendant plus d'une seconde se voit : donner une action au groupe (respiration en cascade, regards qui se suivent).
- Aperçus de mouvement : `--draft` (ombres allégées, 3 fois plus rapide) et `--range a:b` pour ne rendre qu'un plan ; jamais `--draft` pour une livraison.
- `then=<le clip du déplacement>` rejouait le clip depuis le début (corrigé au cycle 1) ; « La canicule » en garde une double chute au
  plan S10 dans la version livrée.

