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
| Freinage au bord et moulinets | `dashOff` court (0,26 s), puis `skidStop` avec `thenBlend=0.03` (coupe franche : le fondu par défaut moyenne « penché en avant » et « penché en arrière » et donne un homme droit) pendant qu'un `glide` le fait encore glisser 1 m ; écrasement 2 images, bascule sur la pointe des pieds ; `teeter` (`spin: 23` : moins de 60° par image, sinon les bras clignotent au lieu de tourner ; `grow: 2.6`, yeux sortis `pop: 0.8`), inclinaison du tronc qui grandit par clé, bras allongés ×1,3 | 37 S08 |
| Atterrissage en accordéon, les voisins tremblent | `fallDrag` puis `accordion` avec `hit: True` et `blend=0.02` : à plat à la première image, trois rebonds de soufflet qui s'éteignent ; `jelly` sur les voisins au même instant | 37 S09 |
| Descente d'ascenseur, digne, la main reste | marche courte (deux enjambées), `royalWave` avec `fore: 1.84` (avant-bras vertical) et `foreAmp: 0.3`, descente linéaire avec `auto: 0` ; la main descend 0,55 m avec lui puis ne bouge plus : l'avant-bras s'allonge de ce que le corps descend (`1 + v (t - t0) / 0.33`, clé linéaire, épaisseur 0,9), la main grossit (`scl.handR ×2,2`) ; seule 13 images devant une vitrine bleue (peau sur fond clair = illisible), un coup de poignet, aspirée en 2 images ; la caméra se resserre sur elle pendant qu'il descend | 37 S10 |
| Serrés comme des sardines, respiration en tuyaux d'orgue | `squeezed` + `sq [0.74, 1.08, 0.9]` ; ils inspirent l'un après l'autre (0,08 s d'écart) : plus fins et plus hauts, joues gonflées (`puffed`), les yeux sur le voisin, les deux du bout poussés contre les murs ; puis relâchent ensemble | 37 S12 |
| Bras élastique jusqu'en haut du puits | creux de 3 images (écrasement), `reachHigh` + bras et avant-bras ×3,7 (`outBack`) avec une épaisseur de 1,5 (un bras fin de 13 px ne se lit pas à 5 m), tenu 9 images, retour en 0,06 s ; le recul fait tanguer la rangée ; les trois voisins gardent le cou tendu (`neck [-0.5, 0, 0, 1.3]`, à 2 images d'écart) vers un point fixe en haut du puits, puis regardent la lettre dans sa main | 37 S13 |
| Yeux en euros en cascade | globes sortis avec le signe euro (`face: {pop, euro}`), décalés de 0,05 s par personnage, petit bond, quatre sourires différents | 37 S14 |
| Plongeons variés, un par un | course, bond au-dessus du trou dans la pose (`noseJump`, `cannonball`, `swanDive`), 2 images suspendu, puis chute ; la file avance d'une place à chaque saut (les suivants par `walk`, la file-accessoire par `to` avec un petit `arc`) | 37 S15 |
| Colonne humaine | chacun arrive dans la pose de son plongeon ; celui qui plonge tête la première reste planté (`headStuck`, jambes qui tremblent) ; à chaque arrivée la rangée du dessous est plus plate et ceux qui sont dessus descendent avec elle (fonctions `press` / `ride` de l'histoire) ; trois étages | 37 S16 |
| Fonte en flaque qui garde ses yeux | `meltDown` avec `sink: 1` et `flat: 0.97` sur 15 images, 4 images après la fin du clignotement du panneau : droit comme une bougie (la tête rentre dans les épaules, les bras coulent, le tronc raccourcit et s'élargit, il descend dans ses chaussures), jamais plié en avant (un pli à la taille se lit comme un salut) ; quand il est plat on le cache (`visible=False`) et l'accessoire `meltPuddle` a pris sa place, décalé de 0,25 m pour être dégagé des gravats : flaque ronde aux couleurs de sa chemise, ses deux yeux et sa moustache dessus ; le chapeau (accessoire, celui du rig caché par `hat: [60, 0, 0]`) reste en l'air pendant toute la fonte puis se pose sur la flaque, qui tremble ; les yeux de la flaque suivent le chapeau, le panneau, puis nous regardent comme tout le monde | 37 S18 |
| Cou de cygne et regard en coin | `hoseNeck` (`len: 8.5, curve: -0.5, lean: 0.2`) : il monte avec dépassement, garde un arc (plus un bâton), penché du côté de ce qu'il vient voir ; visage de trois quarts ; il ne tourne PAS la tête vers la flaque (on verrait ses cheveux) : expression `side` et regard vers un point en avant, 0,3 s ; puis regard caméra, clignement lent posé par clé (`face.lid` 0 → 1 → 0 sur 7 images) ; la pile regarde la caméra à son tour, décalée de 0,05 s | 37 S18 |
| Double regard sur un panneau qui change | il lit LIBRE (ravi), se tourne vers le trou et prend son élan (`sq [1.14, 0.8, 1.14]`) ; le panneau passe à COMPLET (clac, deux clignotements) ; 3 images plus tard la tête revient au panneau : chapeau en l'air (`hat: [0.22, 0, 0]`), yeux sortis de profil avec pupilles vers nous (`eyeYaw: 0.8`), mâchoire, corps étiré ; tenu 9 images | 37 S18 |

| Trois inspirations qui le gonflent (gag à répétition : rue, crépuscule, printemps) | `sneezeUp` avec `ik: 1` : l'index est tenu sous le nez par la main guidée quoi que fassent la tête et le torse ; chaque inspiration plus grande (torse en trapèze, il décolle), la cravate et les cheveux aspirés vers le nez à chaque fois (canal `wind` du clip). À la troisième la caméra recule (`glide`) pour montrer les pieds décollés et l'ombre dessous. Les 3 dernières images sont la détente, face à nous (`sneeze` avec `fold: 0.6, chin: 1.3` : le visage reste vers la caméra, bouche grande ouverte), puis on coupe derrière lui. Reprises : `back: 0.6` (tête moins renversée) et caméra de face un peu haute, 4 inspirations et `sq` par paliers pour le ballon final | 38 S01, S16, S19 |
| Soufflés, épinglés comme des affiches | les passants : `blownBack` sur un `glide` rapide, puis `poster` avec `blend=0.02` contre le panneau, cheveux en mèches dressées (`hairUp`), étoiles ; tout le texte du panneau dans une bande au-dessus des têtes (`adPanel textH: 0.25`, panneau de 3,6 m) ; deux se décollent et glissent (`slideAt`) | 38 S02, S03 |
| La présentatrice en toupie | `spinTop` (`turns` : montée, palier, arrêt), l'anémomètre tenu en l'air, papiers qui volent, lunettes de travers ensuite | 38 S04 |
| Le doigt qui pousse le curseur | main guidée (`reach`, bout du doigt 7 cm sous le curseur) avec les mêmes instants, durées et courbes que l'accessoire (`toonEase='out'` des deux côtés) ; deux petits coups d'abord, un creux puis la pointe des pieds pour la dernière bande | 38 S06 |
| La liste qu'on déroule par sa corde | `nameList` avec `unroll: [t, 0.27]` (store à enrouleur : le texte s'étire depuis le tube, rebond en bas) ; il fait un pas, lève la main ouverte vers la boule (regard d'abord), la ferme, tire en 8 images (`reach` sur la hauteur de la boule, `inOut` comme l'accessoire), écrasé en bas ; puis deux tapes sur la liste et regard caméra | 38 S07 |
| Le bras télescopique | (troisième passe : la carte en haut du mur, elle au coin opposé du cadre : le bras monte la diagonale sur trois à quatre fois sa longueur, chaque tape fait basculer la carte (`tapAt` liste, `tapAmp`), une ondulation redescend le bras) un bras ordinaire d'abord (2 images, trop court), puis `reach` jusqu'au bout de la carte avec `outBack` (il dépasse, revient), main ×1,5 ; elle garde le visage et le sourire vers la caméra ; la carte tremble à la tape (`tapAt`) ; le doigt se pose à côté du nom, pas dessus | 38 S10 |
| Gyrophare et foule couchée comme du blé | accessoire `beacon` posé sur le crâne (`offset [0, 0.565, 0]` dans le repère de la tête : au-dessus des cheveux, les yeux restent libres), deux faisceaux qui tournent ; les passants se plient l'un après l'autre (`leanAway`, 0,9 m avant son passage) ; travelling arrière partiel pour garder son visage à 15 % de la largeur | 38 S11 |
| Triple double regard | (troisième passe : premier reniflement dès la 2e image ; le premier regard est un vrai mouvement : les trois ensemble, cou tendu, tenu 6 images, retour 4 images, puis le second) caméra de trois quarts : lui à gauche, trois têtes en rang derrière son épaule (une seule profondeur de 1,2 m, 0,6 m d'écart latéral) ; au premier reniflement un coup d'œil, puis ils regardent ailleurs 4 images, au second la tête revient d'un coup, yeux sortis (`pop: 0.5`), décalés de 0,05 s | 38 S12 |
| Jambes en moulinet et perruque qui reste | `scramble` commencé 4 images avant la coupe (clé avant 0 dans le plan suivant), `dashOff` chacun dans sa direction ; la perruque reste 8 images où était la tête puis tombe ; des sacs de sable surgissent en U derrière lui ; ses yeux suivent chaque départ, il cligne vers nous, renifle encore | 38 S13 |
| Le tampon géant, la tête dans les épaules | le tampon suit sa propre trajectoire (clés `to` / `rotTo`, `rotOrder='YXZ'`) et la main de l'assureur est guidée sur son pommeau (`reach` aux mêmes clés) : contact exact ; levée tenue, frappe en 2 images, la tête rentre (`headHammer`), le tampon rebondit vers l'assureur, la tête ressort avec la marque (8 images dans le vide), la caméra s'approche ; puis un plan à part, de trois quarts : il penche 5 images (`plankFall hang`), tombe raide en 8, rebond, les jambes se relèvent 10 images (`feet`) | 38 S14 |
| La poignée de main qui le traverse | `shakeHands2` : les mains tiennent un même point (`grip`) qui pompe de plus en plus fort ; lui est secoué avec 2 images de retard à chaque articulation, il décolle sur les derniers coups, puis sonne (trois oscillations) ; l'autre secoue à deux mains et lève un gros pouce ; les deux hommes à 55° de la caméra | 38 S15 |
| La poivrière au bout d'une canne | tenue PAR-DESSUS son épaule par l'ingénieur caché derrière lui (derrière le canon) : la poivrière étiquetée pend au-dessus du nez, contre le ciel, le poivre tombe ; à chaque inspiration elle descend, l'ingénieur se penche en arrière puis se baisse, une main sur le casque | 38 S16 |
| Le recul dans le matelas | vu de trois quarts de côté : il part en arrière assis le premier (`blownBack`), le matelas rayé se creuse en banane (`mattressWall` en tranches, `hitAt`), revient et le renvoie ; l'ingénieur à l'abri derrière, son casque saute. Puis l'autre bout du champ : trois éoliennes qui démarrent l'une après l'autre (`rpmKeys`), une ville derrière chacune s'allume (`townLights sites`) | 38 S17 |
| Le grain de pollen | très gros plan ; le grain descend en deux arcs et se pose sur les narines (position mesurée sur une image) ; les deux pupilles le suivent et convergent (`cross`), paupières à demi | 38 S18 |
| L'inspiration à cliquet (gag à répétition, trois rythmes) | `sneezeUp` avec `times` (débuts de plus en plus rapprochés), `last`, `tremble` : chaque inspiration garde ce qu'elle a gagné (torse, hauteur, cheveux, cravate), le sommet de la dernière est tenu en tremblant. Trois occurrences, trois rythmes : trois qui se resserrent puis l'éternuement ; une longue (la poivrière descend) puis une courte ; cinq qui se resserrent et le film finit sur le sommet tenu 6 images. Toute la prairie se penche vers lui un peu plus à chaque fois (`flowerMeadow toward / pull`) | 38 S01, S16, S19 |
| La liste qui remonte comme un store | `nameList roll` : la boule est hors de portée, il s'accroupit, saute, redescend avec la liste sur son poids ; elle remonte d'un coup : le bras part d'abord (1 image, pieds au sol), le corps suit trop haut, il pend au bout du bras (main guidée sur la boule), pieds à 0,5 m du sol, jambes qui balancent, regard caméra ; son poids la redescend, il atterrit écrasé | 38 S07 |
| Les yeux seuls suivent le danger | canal `face.gx / face.gy` (− = vers sa droite / vers le haut) : la tête reste face caméra, les pupilles montent après le tampon ; expression aux yeux grands ouverts (`surprised`), puis il déglutit (`gulp`) et se tasse | 38 S14 |
| La chute de planche cadrée bas, la tête tamponnée qui se relève | caméra à 0,5 m du sol, trois quarts côté pieds ; il tient la hauteur du cadre, la caméra descend avec lui (`glide` de 0,32 s) ; jambes en V sur 39 % de la hauteur ; puis le cou se plie (`bend neck [1.0, …, 1.3]`) : le visage tamponné revient vers nous entre ses pieds, sous le certificat | 38 S14 |
| La poignée de main « photo officielle » | celui qui serre regarde la caméra en souriant, pas la main ; après le lâcher, l'autre sonne comme une règle (pieds plantés, la tête en dernier, étoiles dès le lâcher) ; le pouce : point guidé dans le ciel libre entre les deux têtes (`thumb`), `thumbTwist` réglé sur images (0 = pouce droit), main ×1,7, pompé deux fois par le clip | 38 S15 |
| Avalé puis recraché par le matelas | une vingtaine d'images : entrée assis (3), le matelas se creuse et le garde (`hold`, 4 images), il le recrache roulé en boule (`cannonball`, un tour sur le vol, `arc`), atterrissage écrasé (`land` + `sq [1.5, 0.58, 1.0]`), il se relève sonné | 38 S17 |
| Les villes qui s'allument d'un coup | `townLights pop` (toutes les fenêtres en une image) sous un halo (`glow`, `glowK`), une ville à côté de chaque mât, à l'instant où son rotor atteint sa vitesse, la dernière 13 images avant la coupe ; flou du rotor en trois fantômes (`ghosts: 3, blurSpread: 4`) | 38 S17 |
| Décollé tête la première comme du papier peint | `poster` avec `peelK: 3` | 38 S03 |
| Le bras « corde à linge » (gag à répétition du film : le bras reste) | main guidée sur la poignée (`reach` vers `handle(deg)`, mêmes nombres que l'accessoire) ; il s'éloigne de CÔTÉ sur la pointe des pieds (`sneak`), le bras se paie comme un élastique ; au bout, ses pieds patinent (`scramble`, 0,35 s) et le bras tendu vibre (`wave` : `RIP(0.08, phase)`), puis il le ramène en 3 images | 39 S09 |
| Pressé derrière la vitre, puis affiche | le battant se rabat sur lui (`swing` à 166°) : `pressGlass` + `sq [1.9, 1.0, 0.09]` (presque deux fois sa largeur, pas plus épais que la vitre), une paume étalée (`scl handR`), vitre éclaircie (`shopDoor glass: 0.14`) ; le battant revient, il reste sur le mur (`poster`, tenu 0,24 s avant de se décoller) | 39 S09 |
| La casquette qui l'enfonce | elle traverse le haut du cadre (4 images visibles, `ease in`), s'écrase (`squash`), lui aussi : `sq [1.45, 0.55, 1.45]` tenu 7 images pendant que seules les pupilles montent (`gy −1`) ; la caméra descend avec lui (`glide` 0,1 s) puis remonte ; ressort avec dépassement `[0.9, 1.14, 0.9]` | 39 S08 |
| Le cou par-dessus la file | `bend neck [0, bz, 0, 15, 0.55]` (quinze fois sa longueur, aminci) + `wave neck` à bout libre : il monte en 0,3 s (`outBack`) quand la caméra arrive, puis oscille ; la tête contre le ciel, entre 20 et 35 % de la hauteur | 39 S10 |
| Le temps qui passe sur lui | une barbe (accessoire attaché à la tête) qui grandit d'un cran à chaque passant (`scale` par clés `outBack`), une toile d'araignée entre son bras et la porte, une casquette, un pigeon : chaque couche reste dans les plans suivants | 39 S02 à S17 |
| La tête de match de tennis | `look` alterné entre deux points DEVANT lui (le visage reste vers nous), de plus en plus vite (écarts de 0,26 à 0,08 s) ; son poing gonfle (`scl handR` ×1,7 sur 0,8 s) | 39 S05 |
| Le bras resté à la porte, de nuit | à travers la vitre du battant (`glass: 0.03`, `inner: False`), caméra à 2,3 m : la main sur la poignée en bas, la manche qui monte dans l'image jusqu'à lui, qui s'éloigne voûté et salue sans se retourner ; deux pigeons endormis dessus (`pigeon sleep`, ils suivent le bras qui se paie) ; flaques chaudes (`streetLamp pool`) | 39 S11 |
| L'onde qui vient le chercher dans son lit | `wave` sur le bras qui sort par la fenêtre, phase décroissante (elle arrive vers lui), puis il part en 3 images et finit à plat sur le mur DANS SA POSE DE SOMMEIL (`stiffStand`, yeux fermés, tête penchée, l'oreiller attaché à sa tête à l'instant du départ, une bulle « Zzz » qui revient) | 39 S12 |
| Le garde qu'on tapote | plan à deux depuis les hanches ; trois tapes de l'index (`reach` aller-retour) : à chacune sa tête bascule sur son cou comme un punching-ball (`bend neck [0, 0, a, 1.12]`, retour au-delà de la verticale), ses pupilles sur le doigt, rien d'autre ne bouge ; le téléphone à bout de bras, un `flash` | 39 S13 |
| Appuyer sans regarder | un coup d'œil des pupilles seules vers la boîte (0,25 s), puis le bras part en arrière vers le bouton, un sourcil levé ; pressé, clin d'œil (`lidR: 1`, `mouth: 'smirk'`) ; le visage ne quitte pas la caméra | 39 S15 |
| Le poing qui ne tient plus rien | gros plan presque de face : le poing levé devant la poitrine ; regard sur le poing, sur la porte (pupilles), sur le poing ; écrasement d'élan (2 images), puis le take vers NOUS, les pupilles des yeux sortis baissées sur le poing (`eyeYaw`, `eyePitch`) ; il retombe sur les premières images du plan suivant | 39 S16 |
| Le bras qu'on rabat et qui remonte | il le regarde, pose l'autre main dessus et pousse, de côté, devant la porte claire : l'avant-bras plie comme un plongeoir et tremble ; il lâche : il reste en bas ; soupir, yeux fermés (14 images) ; ses yeux y vont AVANT qu'il bouge ; il remonte en 2 images, dépasse la poignée, onde ; la porte s'ouvre pour personne ; regard tenu | 39 S17 |
| L'interrupteur au bout du bras, puis le noir | la main guidée va chercher l'interrupteur à l'autre bout de la pièce ; au clic : plan `dark` (grade en post), seuls ses yeux restent (`darkEyes`), la caméra glisse vers eux | 40 S01 |
| Des yeux qui marchent dans le noir | deux yeux traversent le cadre, se cognent à une porte vitrée (spirales), glissent ; une ville qui s'éteint par vagues, puis la tour (`cityNight keys`, `towerLag`), des yeux dans les fenêtres | 40 S02, S03 |
| La cravate tirée comme le cordon d'une lampe (gag à répétition, trois variations) | canal `tie [longueur, avant, côté]` : l'électricien la tire (deux paires d'yeux dans le noir) ; il la tire lui-même au balcon, Paris s'éteint derrière lui ; à la bougie : la flamme et les yeux restent | 40 S08, S11, S17 |
| L'étiquette claquée sur le front | accessoire attaché à la tête (`[0, 0.4, 0.094]`), `squash` à l'impact, la tête part en arrière | 40 S09 |
| Ce qui reste dans le noir | deux cambrioleurs éclairés par une allumette ; elle s'éteint : leurs sourires restent ; les amoureux : des yeux en cœur, puis une troisième paire | 40 S12, S13 |
| Entrer fin comme du papier | `paperThin` posé à 0 avec un déplacement `glide=True` : il passe de profil par l'entrebâillement, puis reprend son épaisseur d'un coup | 40 S16 |
| Le soleil a un visage, et s'éteint comme une ampoule | `sunLamp` (disque avec visage, `scareAt`, `offAt`) ; la main qui monte à la cravate, la foule qui tend le bras ; noir : les yeux de tous | 40 S18 à S22 |

Gags du rig pas encore servis : langue déroulée, vapeur aux oreilles, `inflate`, `noodle`, `stretchGrab` horizontal, `doubleTakeToon`, expressions `zap`, `dotEyes` (`paperThin` : servi dans la 40). Versions de la première passe remplacées (ne pas les reprendre telles quelles non plus) : crêpe verticale `pancake`, take du policier, bras levé tendu du maire, `periscope` en poteau droit.

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
- (4e passe) **Deux surfaces presque coplanaires clignotent** en vue longue : la route posée 4 mm au-dessus du sol général passait au beige une image sur sept
  dans l'axe de la rue (pas dans les plans rapprochés). Ne jamais empiler deux grandes surfaces à quelques millimètres : descendre celle du dessous de 10 cm
  ou la découper. Contrôle : `python3 absurd-shorts/tools/flash_check.py FILM.mp4 scripts-fr/story_x.json` (plans à caméra fixe), et regarder le bord gauche
  des bandes d'aperçu, pas seulement les personnages.
- (4e passe) Un membre étiré et courbé ressortait par la pièce suivante (le cou ×8,5 à travers le visage) : la partie du maillage qui dépasse
  l'articulation suivante est maintenant rigide. Après tout étirement supérieur à ×3 avec une courbure, regarder l'extrémité en grand.
- (4e passe) Une coupe qui garde le même cadre (S17/S18) n'en est pas une pour l'œil : tout changement de pose saute. Poser avant 0 les clés de regard
  (`k(-1.0, look=...)`) et de clip (`k(-0.28, clip='skidStop')`) pour que la première image continue la dernière du plan précédent ; les clés de
  visibilité, elles, ne se posent jamais avant 0.
- (4e passe) Un regard vers un accessoire qui se fait attacher en cours de plan (`look='bill'`, puis `attach`) saute une image : viser un point fixe.
- (4e passe) Le dernier regard caméra d'un groupe : 15 à 18 images, clignement terminé au moins 4 images avant la fin ; un film qui finit les yeux fermés
  finit sur une faute. Compter les images de la dernière tenue sur la bande avant le rendu.
- (4e passe) Un visage qui descend dans un trou traverse la bande des sous-titres si le bord du trou est plus bas que 76 % : garder le bord entre 66 et
  76 % (caméra à 1,05 m, cible à 0,6 m) : le visage disparaît derrière le bord proche juste au-dessus du texte.
- (4e passe) Texte d'accessoire : l'ajuster à son cadre par mesure (`measureText`), jamais à taille fixe (« AUCUN TROL ») ; deux états d'un même panneau
  (LIBRE / COMPLET) à la même hauteur de lettres, le dernier affiché le plus contrasté ; 5 % de marge avec les bords de l'image, y compris en fin de travelling.
- (4e passe) Un accessoire laissé en l'air doit montrer sa face lisible : incliné vers la caméra (dessus éclairé), pas en rotation (une plaque noire une image sur deux).
- (4e passe) Visages à peau foncée : à petite taille les traits noirs se perdent. Ne pas éclaircir la peau : donner `faceRim: True` au personnage (contour clair autour des sourcils, des yeux et de la bouche ; cycle 2).
- (cycle 2, 1re relecture : 6,8 / 6,8) **Un accessoire posé sur la tête ne doit jamais toucher la ligne des yeux** : le décalage d'un accessoire attaché se
  compte dans le repère de l'articulation (la tête fait 0,5 de haut, cheveux jusqu'à 0,565), pas en mètres du monde : `offset [0, 0.3, 0]` posait le
  gyrophare sur le front et cachait le regard du héros pendant trois plans. Contrôler un gros plan de face après toute attache sur la tête.
- (cycle 2) Le visage est peint sur la face avant de la tête : **un profil est une planche vide**. Tourner chaque personnage d'au moins 30° vers la caméra
  (une poignée de main : les deux à 55° de l'axe, le point serré vers nous ; un coup de tampon : celui qui frappe derrière l'épaule de l'autre, de trois
  quarts). Un seul plan de profil est permis : une chute raide, parce que c'est la silhouette qui joue.
- (cycle 2) Trois réactions ensemble : une caméra de face les cache derrière la tête du premier plan. Caméra de trois quarts, les têtes en rang d'un seul
  côté (du côté opposé au bras levé du héros), vérifiées avec `proj.py` : 16 % d'écart entre centres, chaque visage au moins 11 % de la largeur.
- (cycle 2) Texte d'accessoire et personnages : tout ce qu'on épingle, pose ou tend devant un panneau le couvre. Mettre le texte dans une bande que
  rien n'atteint (en haut du panneau, au-dessus des têtes) et faire passer les bras sous les bandeaux (`stormMap bandTop`). Une aiguille de la couleur
  du chiffre qu'elle désigne l'efface : chiffres hors de sa course, celui qu'on lit plus gros et d'une autre couleur.
- (cycle 2) Un texte ou un objet coupé par le bord du cadre se lit comme une faute : entièrement dedans (5 % de marge) ou entièrement dehors, dans CHAQUE
  cadre du plan (un rapprochement en cours de plan recoupe ce que le plan large contenait). Un objet lointain dont un seul bord dépasse des toits (la tour
  dans la brume) se lit comme une rayure : l'ôter du décor pour ces plans (`eiffel: False`).
- (cycle 2) Sous la lumière chaude d'un intérieur, un mur crème prend la teinte des peaux (31°, 42 % de saturation contre 30° pour un visage) : mesurer
  sur une image (`colorsys.rgb_to_hsv` d'un carré de mur et d'une joue) et refroidir la couleur de base jusqu'à 25 % de saturation ou moins (`mairie`
  accepte `wall`, `band`, `trim`, `floor`). **Un même décor servi pour deux institutions se lit comme le même lieu** : une enseigne (`signBoard`) et une
  couleur propres à chacune (assurance : mur vert-gris), jamais le bandeau tricolore.
- (cycle 2) **La détente d'une anticipation doit se voir sur le personnage** : trois inspirations suivies d'une coupe derrière lui ne paient rien. Garder
  3 images de la détente dans le plan de l'anticipation (la tête fouette vers nous), puis couper ; dans le plan suivant le clip continue (clé avant 0).
- (cycle 2) Une tenue sans action se voit à l'aperçu comme une image arrêtée (0 % de pixels qui changent) : chaque tenue reçoit un geste qui raconte
  (deux tapes du doigt, un hochement, une canne qui s'approche, un pouce pompé deux fois, un dernier reniflement). La respiration automatique ne suffit pas à 124 px.
- (cycle 2) Une chute raide qui s'éloigne de la caméra rétrécit et s'enfonce : la filmer en travers du cadre, dans un plan à part de trois quarts
  (4 à 6 images penché, 8 pour tomber, un rebond, les jambes en l'air 8 images ou plus), et faire sortir le second personnage avant.
- (cycle 2) **Un accessoire tenu qui doit toucher juste** (tampon sur un crâne, canne, curseur) : ne pas régler les angles du bras. Donner à
  l'accessoire sa propre trajectoire (clés `to`, `rotTo`, `rotOrder='YXZ'` s'il bascule dans le plan où il regarde) et guider la main sur sa poignée
  (canal `reach`, mêmes instants, mêmes durées, mêmes courbes). Pour un point du corps : `touch` (`['face', travers, hauteur, mètres devant]`).
- (cycle 2) Deux mains qui se serrent : un seul point du monde tenu par les deux (`shakeHands2 grip`), devant eux et vers la caméra ; sinon les deux bras
  se croisent sur toute leur longueur.
- (cycle 2) Un objet qu'on tend devant un visage le cache à toute caméra : le suspendre au-dessus, contre le ciel, et faire tomber quelque chose de
  lisible vers le visage (du poivre) ; celui qui le tend se tient derrière le héros, pas entre lui et nous.
- (cycle 2) Un corps plat dans un objet qui se creuse passe derrière ses bords (le héros en « affiche » semblait debout sur le matelas) : le faire entrer
  assis le premier (`blownBack`), les hanches au fond du creux, et régler sa hauteur sur le milieu de l'objet (`y` négatif si le clip le soulève).
- (cycle 2) Cheveux dressés : un bloc qui se lève se lit comme un fez ; cinq mèches en éventail (`cloth.js`). Matelas : dix tranches sans contour (dix
  contours font une pile de boîtes), rayures et boutons sur les deux faces, les bouts amincis.
- (cycle 2) **Commentaire au milieu d'une ligne, troisième fois** (les tranches du matelas n'étaient plus ajoutées : accessoire invisible, aucune erreur).
  Second contrôle avant chaque commit : `git diff | grep '^+' | grep -nE "//.*;\s*[a-zA-Z_.]+\(.*\);\s*$"` ; et quand un accessoire disparaît après
  une retouche, relire d'abord la ligne retouchée.
- (cycle 2) Une pièce du rig appliquée deux fois dans la même image double la rotation de ses articulations filles (la tête penchait deux fois, la main
  guidée arrivait trop haut) : `apply` ne plie la colonne et le cou qu'une fois quand une main est guidée. Toute mesure d'une cible se fait après.
- (cycle 2) Clip à déroulement unique donné comme clip de départ avec une clé avant 0 : le moteur avertit ; mettre `stand` en clip de départ.
- (cycle 3) Un bureau au premier plan cache tout ce qui est sous 0,67 m cinq mètres derrière lui : un personnage soulevé du sol semble debout. Placer
  l'action à côté du meuble, le sol dans le cadre, les pieds décollés juste au-dessus de la bande des sous-titres (77 %).
- (cycle 3) Regarder un objet placé derrière soi tourne la tête sur son côté sans visage : viser un point à 45° de l'axe caméra au plus, ou ne bouger
  que les pupilles (`face.gx / gy`). Vérifier le signe sur un gros plan avant de mettre en scène (`gy` positif = vers le bas).
- (cycle 3) Couleur d'un mur sous la lumière chaude d'une pièce : un bleu pâle (#BFD2E4) sortait encore gris chaud (teinte 30°, 12 %) ; #9DBBE0 donne
  un gris-bleu (215°, 10 %). Mesurer sur une image rendue, pas sur le code couleur.
- (cycle 3) Écrasement vu de côté : `sq` en z (le sens où il regarde) l'allonge à l'écran et le sort du cadre ; élargir en x. Atterrir avant le bord.
- (cycle 3) Tête hors cadre sur un étirement ou un sommet : calculer (soulèvement + taille × étirement) contre le haut du cadre à sa profondeur, garder
  5 % ; les mèches dressées ajoutent 0,3 m à chaque inspiration. Regarder l'image de la pose extrême, pas seulement la pose tenue.
- (cycle 3) Changement de caméra dans un même plan : une enseigne coupée en deux par le nouveau cadre, un personnage qui sort dont il reste un liseré
  au bord : clé `visible=False` à l'instant du changement, ou les cadrer entiers.
- (cycle 3) Un accessoire qui arrive avec `ease='in'` n'est dans le cadre que les 3 dernières images : pour qu'il se lise (10 images au moins), une
  dérive lente et linéaire depuis juste hors champ, encore en chemin à la coupe.
- (cycle 3) « Deux fois plus grand » pour des objets alignés est borné par l'écart angulaire entre voisins : calculer cet écart d'abord (les villes
  entre les mâts : 24 % de la largeur au plus).
- (cycle 3) Fouetté de caméra sur un geste en 2 images : la caméra part une image avant le corps, sinon la tête sort du cadre à la première image.
- (cycle 3) Orientation d'une main guidée (pouce levé) : balayer la torsion sur quatre images (−2,4 ; 0 ; 1,2 ; 2,4) au lieu de la deviner.
- (cycle 3) Correction après lecture des bandes : ne re-rendre que la plage du plan dans le brouillon (`--range a:b`) et la recoller
  (`tools/splice_range.sh`) : les preuves montrées aux relecteurs contiennent la correction.
- (cycle 3) Un étirement dans l'axe de la caméra ne se voit pas (le bras élastique partait derrière le corps du personnage qui venait vers nous ; le bras
  télescopique tendu vers le fond ne faisait que 1,6 fois sa longueur à l'écran) : étirer EN TRAVERS du cadre (corde à linge), le personnage à un bord,
  la cible à l'autre ; viser 2,5 fois la longueur du bras au repos mesurée sur l'image. Tenir d'abord le geste ordinaire 8 images, trop court.
- (cycle 3) « Les yeux seuls » demandent une expression aux yeux ouverts (`surprised`, puis `shocked`) : `gulp` les ferme, et le personnage a l'air de ne
  rien voir. Deux paliers des pupilles avec l'objet qui monte, la tête qui s'enfonce dès le début.
- (cycle 3) Un accessoire levé d'une main cache le visage de celui qui le lève : le tenir à deux mains (les deux `reach` sur le pommeau), le visage
  entre les bras.
- (cycle 3) Oscillation après un choc : 22 rad/s avec un amortissement de 4,3 (trois balancements, 100, 55, 25 %) se lit ; 44 rad/s est un flou, et
  disparaît dans des bandes à une image sur deux. Une carte tapée : pendule depuis son bord haut (`pivotTop`, 13 rad/s), elle reste de travers.
- (cycle 3) Une crêpe à l'atterrissage a les bras en croix : 1,6 m de large de trois quarts. Atterrir avec 30 % de marge de chaque côté.
- (cycle 3) Enseigne au-dessus d'une porte : à peine plus large que la porte ; sinon tout plan serré la coupe. Pour un gros plan sous une enseigne,
  caméra plus haute que le sujet et plongeante : l'enseigne passe au-dessus du cadre.
- (cycle 3) Costume noir uni : silhouette découpée sans modelé à côté des costumes peints (revers, coutures) ; prendre un anthracite avec revers.
- (cycle 3) Regarder ce qu'il y a DERRIÈRE le point où se joue le gag (un arbre du décor exactement derrière la poignée de main : ils semblaient tenir
  un objet vert). Changer le tirage du décor (`seed`) pour ce plan.
- (cycle 3) Trois fois le même modèle ne font pas trois villes : un monument par ville (beffroi, dôme, château d'eau) et de l'horizon sombre entre elles.
- (cycle 3) **Commentaire au milieu d'une ligne, quatrième et cinquième fois**, cette fois en remplaçant du texte par script : le texte de remplacement
  finissait par un commentaire alors que la ligne continuait. Règle : dans un remplacement, jamais de commentaire en fin de chaîne sauf si la chaîne
  remplacée finissait la ligne ; mettre le commentaire sur sa propre ligne au-dessus. `node --check` et l'exécution du script Python l'ont attrapé.
- (cycle 3) Lancer le rendu final pendant la dernière relecture ne sert à rien si elle touche plus d'un tiers des plans : attendre les deux rapports.
- (cycle 4, 1re relecture de « La porte » : 6,6 / 6,6) **Un take doit regarder sa cause.** Le sursaut partait à l'opposé de la main vide : caméra à moins
  de 30° de l'axe du personnage (au-delà, `look` vers la caméra est borné et le visage reste de trois quarts arrière), tête vers nous, pupilles des yeux
  sortis tournées vers la cause (`eyeYaw`, `eyePitch` > 0 = vers le bas), la cause remontée près du visage (le poing devant la poitrine : à hauteur de
  poignée, 1,1 m, une main tombe dans la bande des sous-titres en plan moyen). Yeux au moins aussi gros que dans le premier take du film.
- (cycle 4) **Une chute muette demande du temps d'image après la voix** : geste, tenue du soulagement (10 à 14 images), les yeux qui y vont d'abord, le
  retour en 2 images avec dépassement, dernière tenue de plus d'une demi-seconde. Compter 2 s après la dernière phrase (`place_narration.py --tail 2.0`),
  pas 1,3 s : les deux relecteurs ont noté la chute « sans temps suspendu » à 1,3 s.
- (cycle 4) Une pose aplatie ou tassée se tient 7 images au moins, et la caméra la suit (`glide` vers le bas en 0,1 s, retour avec lui) : tassé à 55 %,
  son visage tombait dans la bande des sous-titres. Deux aplatissements du même film ne prennent jamais la même pose (affiche sur le mur, puis endormi
  sur le mur avec son oreiller) ; les yeux en spirale une seule fois par film.
- (cycle 4) Un membre étiré vu dans son axe ne se lit pas non plus de nuit : le bras partait droit devant la caméra, caché derrière deux pigeons. Monter
  la caméra (2,3 m) pour que la ligne MONTE dans l'image (main à 73 %, épaule à 37 %) ; `proj.py` sur la main, l'épaule, la tête avant de rendre.
- (cycle 4) La poignée d'une porte ouverte à 80° est sur la face tournée vers le personnage : toute caméra placée de l'autre côté voit la main derrière
  le montant. Filmer à travers la vitre (`glass: 0.03`) depuis le côté du mur, et ôter la barre intérieure (`inner: False`).
- (cycle 4) Nuit : un cône de lumière translucide dessiné dans la passe des objets `inDark` voile le personnage (il n'est pas dans cette passe). Pas de
  cône (`glow: False`) : des flaques plates au sol (`streetLamp pool`), le personnage en silhouette entre deux flaques, grade un peu plus clair (0,62).
  Une fenêtre éclairée vue en enfilade se lit comme une planche jaune : l'ôter.
- (cycle 4) Un oiseau endormi garde sa silhouette : tête sur les épaules, penchée, yeux fermés ; la tête rentrée dans le corps en fait une boîte grise.
- (cycle 4) `at(objet, x, y, z)` REMET LA ROTATION À ZÉRO : passer la rotation en arguments (`at(d, x, y, z, -PI / 2)`), sinon un disque posé au sol
  reste debout (deux dômes pâles devant le personnage).
- (cycle 4) `look='personnage'` tourne la tête vers lui : de face caméra elle passe de profil (le maire sans visage pendant qu'il pointe). Garder la tête
  de trois quarts (`look=None`, `face=` vers la caméra) et envoyer les pupilles (`face.gx`).
- (cycle 4) Un personnage qui doit arriver dans le plan : dans le cadre dès la coupe (calculer le bord du cadre à sa profondeur), sinon 0,4 s d'image
  arrêtée. Même règle pour un départ : l'action commence à l'image 2, pas après deux regards.
- (cycle 4) Enseigne dont un plan serré ne montre qu'un coin : la ranger pour ce cadre (`shopDoor signHide [[t0, t1]]`, ou `visible=False` à la coupe
  pour une plaque), plutôt que de la laisser coupée. Vérifier avec `proj.py` le coin de l'enseigne dans CHAQUE cadre serré.
- (cycle 4) Veste, casque et peau de la même famille de couleur (orange, jaune, peau) : le personnage se fond. Changer la tenue par les options du
  personnage (`suit`, `cuff`, `pants`, `lapel`, `hatColor`) : bleu de travail et casque blanc.
- (cycle 4) Ceux qui traversent un plan en courant : soit en travers du premier plan, entre la caméra et le sujet (trois traînées), soit entiers dans le
  cadre ; un passant dont le cadre ne garde qu'une tranche se lit comme un défaut.
- (cycle 4) Yeux dans le noir : le rig facial est sur la face avant de la tête : tourner le visage vers la caméra, sinon rien ne reste. `visible` d'un
  objet three.js doit être un booléen (`!!(…)`) : `undefined` se dessine. L'échelle et la visibilité propres à un accessoire se posent sur un groupe
  intérieur (le moteur pilote la racine). Pour que les accessoires `inDark` gardent le même aspect dans un plan éclairé du même lieu : `dark=[[0, 0, 0.001]]`.
- (cycle 4) Une couleur sombre non éclairée (`MeshBasicMaterial`) ressort plus saturée après le mappeur de tons (son pied retire le canal minimum) :
  régler les couleurs d'un ciel de nuit sur une image rendue.
- (cycle 4) Un déplacement sans clip (`k(t, to=…)`) passe à une marche et écrase le clip en cours : `glide=True` pour glisser dans la pose tenue.
- (cycle 4) Repères du personnage de la série : base de la tête 1,77 m, sommet 2,27 m, yeux entre 2,05 et 2,14 m, bouche 1,885 m, épaules 1,63 m, main
  pendante 0,95 m ; une casquette : `offset [0, 0.5, 0]` sur la tête.
- (cycle 4) Planches de contrôle : compter les colonnes avant de conclure. Trois fois une « anomalie au bord gauche » était le bord droit de la vignette
  voisine (la main du maire qui entrait, un personnage au bord du cadre).
