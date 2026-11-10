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
| Marcher sur le vide sans le savoir | un seul déplacement `walkRead` qui continue au-dessus du trou, il part à deux pas du bord (0,2 s de trottoir, 0,55 s sur le vide), petits pas rapides (`cadence=2.3`), caméra à 2,7 m qui plonge : les pieds sur le noir du trou pendant 0,7 s | 37 S01 |
| Temps suspendu avant la chute | plan serré, caméra basse : `hangPhone` posé par clé (les yeux quittent l'écran, la tête descend, le téléphone s'écarte), regard caméra `uhoh` tenu 17 images avec la déglutition (la coupe vient 0,25 s plus tôt : c'est l'entrée du plan précédent qui paie la tenue), un clignement posé par clé 5 images avant la chute ; puis la caméra recule et monte | 37 S02 |
| Chute « caramel » : les jambes partent, la tête reste | jambes ×2,7 en 0,12 s sans déplacement (les pieds descendent de 1,6 m, le corps ne bouge pas) ; puis l'acteur descend de 1,22 m pendant que colonne ×1,7 et cou ×9 poussent d'autant vers le haut (la tête reste 3 images) ; puis `toon={}` en 0,05 s : tout claque. `auto: 0` dans ces clés | 37 S02 |
| L'objet qui reste en l'air | `detach` avec `worldRot` (tourné vers la caméra), `wobble`, grossi par une clé `scale` ; il attend 6 images seul, puis `to=[None, y, None]` en 0,1 s (pas la gravité) : téléphone, képi, bloc-notes | 37 S02, S07 |
| Aplati comme un tapis, puis regonflage | chute `fallDrag`, puis `splat` avec `blend=0.02` (allongé sur le dos, mince comme du papier, mains en l'air, d'un mur à l'autre), caméra à 2,9 m qui plonge de 30° ; yeux en spirale, deux clignements, étoiles ; `popAt` : ressort debout | 37 S03 |
| Bosse sur le crâne et téléphone rattrapé | l'accessoire tombe sur le crâne (`face.bump`, tête écrasée 0,05 s), rebondit en arc vers l'oreille ; `phoneEar` démarre avant qu'il arrive : la main est là quand il retombe (`attach`) | 37 S03 |
| Coup de tampon | `stampDesk` : bras étiré au-dessus de la tête tenu 5 images (il tremble), descente en 2 images, tout le corps s'écrase ; les objets du bureau sautent (clés `to` de 0,07 s), la feuille posée à plat bondit vers la caméra (`to` + `rotTo` + `scale`) | 37 S04 |
| Regard à gauche, regard à droite, take | expressions `sideL` puis `side` (0,22 s chacune), puis `take` (`pop: 0.55` : globes à peine sortis, mâchoire étirée), bras en Y qui touchent les deux murs | 37 S05 |
| Les yeux descendent dans le trou et en font le tour | caméra de côté à 2,3 m, 17° en plongée (le trou est un disque sombre, pas un trait) ; le corps reste un poteau, le cou se plie un peu au-delà de l'horizontale (`neck [1.62, 0, 0, 1.6]`), les yeux plongent DANS le trou sur des tiges roses (`pop: 1, popLen: 1.62, eyeScale: 1.6, stalkRed: 1, stalkBow: 0.05`), pupilles tournées vers nous (`eyeYaw: -1.3`), regard à gauche puis à droite (`eyeRoll: ±0.7`, les tiges se balancent), un clignement (`popBlink`), tenu 16 images ; ils reviennent et redressent la tête (petit take de profil) ; il disparaît en 2 images, raide (`auto: 0`, pas d'étirement) ; un seul objet reste : le képi, sur le mur clair | 37 S07 |
| Freinage au bord et moulinets | `dashOff` (traînée), `skidStop`, `teeter` (`spin: 37` : deux tours et demi, yeux sortis `pop: 0.8`, amplitude qui grandit, bascule vers l'objectif) | 37 S08 |
| Atterrissage en accordéon, les voisins tremblent | `fallDrag` puis `accordion` avec `hit: True` et `blend=0.02` : à plat à la première image, trois rebonds de soufflet qui s'éteignent ; `jelly` sur les voisins au même instant | 37 S09 |
| Descente d'ascenseur, digne, la main reste | marche courte (deux enjambées), `royalWave` avec `fore: 1.84` (avant-bras vertical) et `foreAmp: 0.3`, descente linéaire avec `auto: 0` ; la main descend 0,55 m avec lui puis ne bouge plus : l'avant-bras s'allonge de ce que le corps descend (`1 + v (t - t0) / 0.33`, clé linéaire, épaisseur 0,9), la main grossit (`scl.handR ×2,2`) ; seule 13 images devant une vitrine bleue (peau sur fond clair = illisible), un coup de poignet, aspirée en 2 images ; la caméra se resserre sur elle pendant qu'il descend | 37 S10 |
| Serrés comme des sardines, respiration en tuyaux d'orgue | `squeezed` + `sq [0.74, 1.08, 0.9]` ; ils inspirent l'un après l'autre (0,08 s d'écart) : plus fins et plus hauts, joues gonflées (`puffed`), les yeux sur le voisin, les deux du bout poussés contre les murs ; puis relâchent ensemble | 37 S12 |
| Bras élastique jusqu'en haut du puits | élan (écrasement 3 images), `reachHigh` + bras et avant-bras ×3,7 (`outBack`), tenu 6 images la main qui tâtonne, retour en 0,06 s ; le recul fait tanguer la rangée (penchés l'un après l'autre) ; les têtes suivent la lettre (`look='bill'`) | 37 S13 |
| Yeux en euros en cascade | globes sortis avec le signe euro (`face: {pop, euro}`), décalés de 0,05 s par personnage, petit bond, quatre sourires différents | 37 S14 |
| Plongeons variés, un par un | course, bond au-dessus du trou dans la pose (`noseJump`, `cannonball`, `swanDive`), 2 images suspendu, puis chute ; la file avance d'une place à chaque saut (les suivants par `walk`, la file-accessoire par `to` avec un petit `arc`) | 37 S15 |
| Colonne humaine | chacun arrive dans la pose de son plongeon ; celui qui plonge tête la première reste planté (`headStuck`, jambes qui tremblent) ; à chaque arrivée la rangée du dessous est plus plate et ceux qui sont dessus descendent avec elle (fonctions `press` / `ride` de l'histoire) ; trois étages | 37 S16 |
| Fonte en flaque qui garde ses yeux | `meltDown` (`flat: 0.97`) sur 15 images, 4 images après la fin du clignotement du panneau ; quand il est plat on le cache (`visible=False`) et l'accessoire `meltPuddle` a pris sa place : flaque ronde aux couleurs de sa chemise (fleurs), ses deux yeux et sa moustache dessus ; le chapeau (accessoire, celui du rig caché par `hat: [60, 0, 0]`) attend en l'air puis se pose sur la flaque, qui tremble ; les yeux de la flaque suivent le chapeau, le panneau, puis nous regardent comme tout le monde | 37 S18 |
| Cou de cygne et regard en coin | `hoseNeck` (`len: 8.5, curve: -0.5, lean: 0.2`) : il monte avec dépassement, garde un arc (plus un bâton), penché du côté de ce qu'il vient voir ; visage de trois quarts ; il ne tourne PAS la tête vers la flaque (on verrait ses cheveux) : expression `side` et regard vers un point en avant, 0,3 s ; puis regard caméra, clignement lent posé par clé (`face.lid` 0 → 1 → 0 sur 7 images) ; la pile regarde la caméra à son tour, décalée de 0,05 s | 37 S18 |
| Double regard sur un panneau qui change | il lit LIBRE (ravi), se tourne vers le trou et prend son élan (`sq [1.14, 0.8, 1.14]`) ; le panneau passe à COMPLET (clac, deux clignotements) ; 3 images plus tard la tête revient au panneau : chapeau en l'air (`hat: [0.22, 0, 0]`), yeux sortis de profil avec pupilles vers nous (`eyeYaw: 0.8`), mâchoire, corps étiré ; tenu 9 images | 37 S18 |

Gags du rig pas encore servis : langue déroulée, vapeur aux oreilles, `paperThin`, `inflate`, `noodle`, `scramble` avant un départ, `stretchGrab` horizontal, `doubleTakeToon`, expressions `zap`, `strain`, `dotEyes`. Versions de la première passe remplacées (ne pas les reprendre telles quelles non plus) : crêpe verticale `pancake`, take du policier, bras levé tendu du maire, `periscope` en poteau droit.

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
- Un clip à déroulement unique (tampon, temps suspendu, plongeon qui tourne) donné comme clip de départ de l'acteur est déjà fini à la première image :
  le clip de départ commence « il y a un million de secondes ». Le poser par clé : `k(0.0, clip=...)`. Deux gags de la première passe ne jouaient jamais.
- Un impact : `blend=0.02` sur la clé du clip d'arrivée. Avec le fondu par défaut (0,24 s, anticipation, mains en retard) l'écrasement arrive en douceur.
- Étirer les jambes fait descendre les pieds sous l'acteur (le bassin ne bouge pas) ; la colonne et le cou poussent vers le haut. « Les jambes partent,
  la tête reste » : jambes d'abord, sans déplacement ; ensuite un déplacement vers le bas égal à l'allongement de la colonne et du cou.
- Les couches automatiques (étirement à la vitesse, écrasement à la décélération) s'ajoutent à une chute chorégraphiée : la tête monte de plus d'un mètre
  puis retombe. Mettre `auto: 0` dans les clés `toon` du passage (et pour une descente « digne »).
- Deux déplacements enchaînés avec la même démarche repassent par `idle` entre les deux (le bras qui tient le téléphone retombe) : un seul déplacement,
  ou `blend=0.001` sur le second.
- Bande des sous-titres (77 à 83 % de la hauteur) : aucune chute de gag dedans ni dessous. Pour un trou dans le sol : caméra à 2,4 m qui plonge de 16°
  (le bord proche à 75 %) ; pour un sol de puits : caméra à 2,9 m qui plonge de 30°. Tracer la bande sur une image de contrôle.
- Bras levé tendu : jamais (une image arrêtée se lit comme un salut, surtout avec une écharpe officielle). Coude plié, main qui tourne : `royalWave`.
- Chutes : pas de pose en T (`airborne`). `fallDrag` (bras en rubans, chapeau soulevé), ou la pose du plongeon qui précède.
- Une tête basculée à 80° montre le dessus du crâne (ou le képi) à toute caméra de face : filmer de profil. Des yeux sur tiges qui passent sous le bord
  du trou disparaissent pour une caméra basse : les arrêter 0,3 m au-dessus.
- Un accessoire lâché (`detach`) garde l'orientation de la main, souvent de profil pour la caméra : `worldRot`, et une clé `scale` pour qu'il se voie.
- Un panneau ou une feuille qui surgit près de la caméra sort vite du cadre : placer le personnage d'un côté (décaler caméra et cible), le panneau de l'autre.
- Pellicules d'aperçu : une image sur deux. Un geste de 2 images peut tomber entre deux vignettes : pour un doute, rendre les images une à une
  (`shots_at` ou `--stills`) avant de conclure à un bogue.
- (3e passe) **Compter les idées par plan** : cinq idées en 1,17 s ne se lisent pas (S07 : la tête bascule, les yeux descendent, reviennent, regard
  caméra, chute étirée, deux objets qui restent). Une idée tenue 14 à 16 images, une chute en 2 images, un seul objet laissé en l'air.
- (3e passe) **Les tenues se paient sur les entrées** : faire partir le personnage à deux pas de sa marque et couper 0,25 s plus tôt ; trois entrées
  de « Le trou » prenaient 2,9 s pour 1,1 s de tenues sur les quatre regards du gag à répétition.
- (3e passe) Une caméra à hauteur d'homme voit un trou dans le sol comme un trait : 2,3 m et 17° en plongée en font un disque sombre au-dessus duquel
  on peut suspendre quelque chose (des yeux, une main).
- (3e passe) Des globes au bout de leurs tiges, vus de côté, n'ont pas de pupille (elle est au bout, dans l'axe) : `eyeYaw` vers la caméra ; des tiges
  couleur peau sur un trottoir beige disparaissent : `stalkRed`.
- (3e passe) Une main couleur peau sur un trottoir clair ne se lit pas, même grossie : placer la chute devant une surface sombre ou saturée (une vitrine)
  et vérifier sur une image que l'alignement tient jusqu'à la dernière image (déplacer la caméra de 0,25 m suffit).
- (3e passe) Un accessoire de la valeur de son fond (képi marine sur vitrine sombre) : décaler la caméra pour qu'il soit sur le mur clair.
- (3e passe) Un membre étiré balaie large : 0,1 rad de balancement au bout d'un avant-bras de 3,5 m fait sortir la main du cadre. Mettre le membre à la
  verticale avant de l'étirer (`royalWave fore: 1.84`) et doser le balancement (`foreAmp`).
- (3e passe) Tourner la tête vers un objet situé derrière soi montre les cheveux : expression `side` (regard en coin) et cible de regard en avant.
- (3e passe) Tableau final : le personnage qui porte la chute entre 55 et 80 % de la largeur (les boutons des applications occupent le bord droit), rien
  d'important dans les 10 % du haut ; un carton et un panneau ne se partagent pas la même bande : 9 % d'écart au moins.
- (3e passe) Une fonte doit finir sur une forme dessinée (accessoire `meltPuddle`), pas sur le rig aplati (des rectangles).
- (3e passe) Une clé dont l'instant devient négatif ne joue pas (`T - 0.14` avec T avancé à 0,10 : la clé `visible=True` passe avant le `visible=False`
  de 0,0 et le personnage n'apparaît jamais). Garder les avances à l'intérieur du plan.
- (3e passe) **Ne jamais insérer un commentaire `//` au milieu d'une instruction d'une ligne** par un remplacement de texte : le reste de la ligne est
  mis en commentaire sans erreur (deux fois : placement des globes, tête du clip `sneezeUp`). Commentaire en fin de ligne ou sur sa propre ligne, et
  avant chaque commit : `git diff | grep '^+' | grep -n "//.*, [a-zA-Z]*: \["`.
- (3e passe) Sous-titres : écrire l'espace française avant les deux-points dans le texte (« répondu : ») ; `build_hf.py` recolle le signe au mot.

