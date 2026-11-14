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
| L'onde qui vient le chercher dans son lit | `wave` sur le bras qui sort par la fenêtre, phase décroissante (elle arrive vers lui), puis il part en 3 images, étiré, et finit plaqué au mur À L'HORIZONTALE, comme il dormait, pendu au bras qui monte dans la fenêtre (clip `wallBunk` : dos au mur, tête vers sa droite, le bras du dessous qui pend), paupières fermées, l'oreiller attaché à sa tête à l'instant du départ, une bulle « Zzz » ; fenêtre au clair de lune, bande pâle sur le mur derrière lui, la caméra va au mur avec lui | 39 S12 |
| Le garde qu'on tapote | plan à deux depuis les hanches ; DEUX tapes de l'index (`reach` aller-retour ; trois ne laissaient pas le temps de balancer) : à chacune sa tête bascule de 35 à 45° sur son cou (`bend neck [0, −a, 0, 1.2]` : flexion de CÔTÉ, à l'opposé du doigt), repasse la verticale (−0,55 a), 0,3 a, −0,12 a, repos : huit images ; le pigeon sur sa casquette bat des ailes pour tenir (`flaps`) ; ses pupilles sur le doigt, rien d'autre ne bouge ; le téléphone à bout de bras, un `flash` | 39 S13 |
| Le doigt du maire qui arrive | sa main guidée traverse toute l'entrée (le bras s'étire autant qu'il faut) et s'arrête à une main du visage ; puis elle touche, deux fois : la tête part de côté sur un cou qui s'étire (0,42 puis 0,62 rad ; 1,2 puis 1,35), repasse la verticale, se pose | 39 S07 |
| Appuyer sans regarder | un coup d'œil des pupilles seules vers la boîte (0,25 s), puis le bras part en arrière vers le bouton, un sourcil levé ; pressé, clin d'œil (`lidR: 1`, `mouth: 'smirk'`) ; le visage ne quitte pas la caméra | 39 S15 |
| Le poing qui ne tient plus rien, puis le take « casquette en l'air, mâchoire dans la paume » | gros plan presque de face, le poing déjà levé à la coupe ; regard sur le poing (5 images), sur la porte (une torsion du cou, 5 images), sur le poing (4) ; écrasement d'élan ; il décolle des talons (`sq [0.86, 1.2, 0.86]`), sa casquette RESTE en l'air (l'accessoire attaché est caché, un second, libre, tient 4 images puis retombe : `squash`), la main s'ouvre et la mâchoire descend dans la paume (`jaw 1, jawLen 0.5`, la barbe ré-attachée sous le menton, 0,14 m en avant) ; la caméra monte avec lui et redescend avec la casquette ; au plan suivant il referme sa mâchoire avec la paume. Version précédente (yeux sur tiges vers le poing) abandonnée : c'était le take de S03 | 39 S16, S17 |
| Le bras qu'on rabat et qui remonte | il le regarde, pose l'autre main dessus et pousse, de côté, devant la porte claire : l'avant-bras plie comme un plongeoir et tremble ; il lâche : il reste en bas ; soupir, yeux fermés (14 images) ; ses yeux y vont AVANT qu'il bouge ; il remonte en 2 images, dépasse la poignée, onde ; la porte s'ouvre pour personne ; regard tenu | 39 S17 |
| L'interrupteur au bout du bras, puis le noir | la main guidée va chercher l'interrupteur à l'autre bout de la pièce ; au clic : plan `dark` (grade en post), seuls ses yeux restent (`darkEyes`), la caméra glisse vers eux | 40 S01 |
| Des yeux qui marchent dans le noir | deux yeux traversent le cadre, se cognent à une porte vitrée (spirales), glissent ; une ville qui s'éteint par vagues, puis la tour (`cityNight keys`, `towerLag`), des yeux dans les fenêtres | 40 S02, S03 |
| La cravate tirée comme le cordon d'une lampe (gag à répétition, trois variations) | canal `tie [longueur, avant, côté]` : l'électricien la tire (deux paires d'yeux dans le noir) ; il la tire lui-même au balcon, Paris s'éteint derrière lui ; à la bougie : la flamme et les yeux restent | 40 S08, S11, S17 |
| L'étiquette claquée sur le front | accessoire attaché à la tête (`[0, 0.4, 0.094]`), `squash` à l'impact, la tête part en arrière | 40 S09 |
| Ce qui reste dans le noir | deux cambrioleurs éclairés par une allumette ; elle s'éteint : leurs sourires restent ; les amoureux : des yeux en cœur, puis une troisième paire | 40 S12, S13 |
| Entrer fin comme du papier, se regonfler en trois souffles | `paperThin` posé à 0 avec un déplacement `glide=True`, tourné VERS l'autre personnage : de face caméra un corps plat a l'air normal, de profil c'est un trait. Il s'arrête, pivote à 64° de nous (une carte étroite qui bat : `flutter: 6`), le pouce dans la bouche (`touch`), trois souffles (`puffs [[t, 0.32], [t, 0.64], [t, 1.14], [t, 1.0]]`, un rebond à chacun) pendant qu'il revient à 32° ; l'autre recule un peu plus à chaque souffle ; puis la paume tendue | 40 S16 |
| Le soleil a un visage, et s'éteint comme une ampoule | `sunLamp` (disque avec visage, `scareAt`, `offAt`) ; la main qui monte à la cravate, la foule qui tend le bras ; noir : les yeux de tous | 40 S18 à S22 |
| Des yeux de pièce noire | `darkEyes` au-dessus de 1,9 (sur le plan, ou sur un acteur : `act(..., darkEyes=2.9)`) : la peau éclairée des yeux est agrandie autour du point entre les yeux, ils débordent de la tête ; pupilles trois fois plus grandes. Plancher : 5 % de la largeur du cadre pour un œil qui porte un battement (2,2 à 3 à trois ou quatre mètres ; 4,6 vu de loin en contre-plongée ; 5,2 à six mètres) | 40 S04, S08, S12, S13, S21 à S25 |
| Toute la rue le regarde | lui seul à gauche du cadre, reculé à six mètres DERRIÈRE les autres ; dix paires `eyesPair` (accessoire sans visage : `s`, `tall`, `gap`, `openAt`, `blinks`, `look` / `lookY`, `narrow` : paupières qui tombent en biais) qui s'ouvrent en vague à partir de lui (0,05 à 0,28 s), dont deux à des fenêtres (`frame [l, h]`, yeux ronds) et un chat (`slit`, `color`) ; à 0,36 s toutes les pupilles claquent sur lui et les paupières se plissent ; regard à gauche, à droite (3 images chacun) ; il sort en trois pas glissés, ses yeux plongent à chaque pas (`sq` écrit à la main, `auto: 0`), toutes les pupilles le suivent | 40 S22 |
| La flaque de lumière | réglage de plan `darkPool={'prop': 'match' ou 'actor': 'mec', 'lift', 'r' (m), 'k' (nombre ou clés [[t, k, rampe]]), 'tint'}` : autour d'un point l'image revient, puis retombe au noir ; le plan reste `dark` à 1. Allumette : r 1,25, k 0,92 ; bougie : r 0,5, k 0,6 ; clair de lune sur un dormeur dans une nuit graduée : r 1,9, k 0,5 | 40 S12, S17 ; 39 S12 |
| La maison d'en face | `nearHouse` : un mur sombre, une ligne de toit un peu sous le milieu du cadre, trois grandes fenêtres entre 58 et 72 % de la hauteur, qui s'éteignent une à une avec la ville (`keys`, `lag`) ; puis une paire d'yeux ronds s'ouvre dans chacune (`eyesAt`) | 40 S03, S05 |
| Il arrive en glissant sur les genoux | course (0,24 s) puis `to` en `glide` avec le clip `kneelGive` : il finit à genoux sous le bras tendu d'un autre, l'objet tenu à bout de bras devant celui qu'il vise (jamais devant son propre visage) | 40 S06 |
| Le doigt qui tombe d'en haut | l'accusateur sur la pointe des pieds (`sq [0.94, 1.1, 0.94]`), la main guidée haut au-dessus de la tête du personnage placé entre eux, coude vers le haut (direction du coude `[0, 1, 0.2]`), le doigt qui redescend sur l'accusé | 40 S06 |
| Écrasé contre une vitre, dans le noir | deux pas (un plongeon des yeux à chacun), puis la tête écrasée (`scl head [1.5, 0.74, 1]`) : deux yeux larges et plats quatre images, des étoiles à elles (`impactStars`, `r0` : elles partent d'un anneau autour des yeux), un reflet (`glassGlint`), puis les spirales qui glissent | 40 S02 |
| Le bâillement qui sort du cadre | mains guidées droit au-dessus des épaules, plus haut que le bord du cadre (`reach`, Y étroit), onde dans les bras, mâchoire au nœud de cravate (`jaw 0.95`, `jawLen 0.5`) ; l'horloge entière à sa gauche, la tour à sa droite, le bonnet qui tombe de l'autre côté (`nightCap side: -1`) | 40 S10 |
| Le double regard du film | gros plan : les yeux descendent sur l'objet, remontent vers nous, vides (4 images), reclaquent dessus (3 images), la tête suit deux images plus tard (`bend neck`), tenue sourcils levés | 40 S14 |
| Les amoureux dans le noir | deux paires de face, CHAQUE tête penchée de 30° pour que la paire soit horizontale (les yeux peints sont de travers), cœurs dès la troisième image, elles glissent l'une vers l'autre ; un cœur éclate entre elles ; une troisième paire, grosse (`darkEyes=2.9` sur l'acteur), s'ouvre derrière, entre elles : regard à gauche, à droite, descente lente derrière leurs têtes | 40 S13 |
| L'astronome | un œil à l'oculaire (l'autre fermé), un télescope de laiton dont le tube le plus large, côté ciel, monte en travers du cadre (`telescope` : `extend`, `tilt`, `len`, `h` : régler le pivot pour que l'oculaire soit à l'œil) ; rien ; un clignement ; il recule, deux yeux ; une torche tenue au-dessus de sa tête, faisceau peint à bords doux (`torchBeam flat`), qui balaie le ciel vide entre lui et le tube | 40 S23 |
| Le bras qui traverse le cadre pour l'arrêter | la dame À CÔTÉ de lui, presque à sa hauteur (derrière lui, le bras partait dans l'axe) ; coup d'œil, take (yeux sur tiges), puis la main guidée jusqu'à son poignet, avec une onde ; des notes sifflées (`whistleNotes`) pour celui qui n'a rien vu | 40 S20 |
| La statue qu'on tapote | clip `statueRock` (`hits`, `amp`, `dir`) : rien ne plie, l'homme entier oscille autour de ses pieds et se stabilise, le pigeon tient bon (remplace la tête qui bascule sur son cou, déjà servie par le doigt du maire) | 39 S13 (dernière passe) |
| L'étiquette claquée, avec élan et gros plan (troisième passe) | l'objet montré dans la main à hauteur de poitrine, armé au-dessus de la tête de celui qui frappe (il se penche en arrière), puis la main guidée va au front ; **à l'impact la tête s'écrase de 28 cm : une seconde clé `reach` descend la paume avec elle** (sinon la main reste en l'air au-dessus du crâne) ; coupe sur un gros plan à focale longue (`lens=28`, même place : ni main au bord ni décor collé à l'oreille), le mot occupe la moitié de la largeur, les yeux ouverts louchent vers lui (`cross`, `gy -0.9`, `pupilSize`) jusqu'à la coupe : un seul battement | 40 S09 |
| Le coup sur la vitre, vu de l'intérieur | caméra dans le bus, contre la paroi opposée, par-dessus l'épaule d'un passager coupé par le bord latéral ; il court à côté, le poing guidé sur la vitre (`reach` : une image de contact, deux de recul, la main grossit à chaque coup : 1,3 – 1,45 – 1,75), étoiles SUR la vitre (`impactStars` qui avance avec le bus), le bus tangue (`rock`), le passager sursaute ; au freinage (bus et caméra en `ease='out'`) il glisse hors de la porte, le passager est projeté dans le cadre et se retourne vers nous | 41 S01 |
| Il freine des talons sans ralentir | clip `heelBrake` en `glide` linéaire (`cruise`), fumée née sous les semelles (`heelSmoke`, `marks`), la caméra recule devant lui ; à la fin, le même freinage sur un autre homme qui le croise (variation) | 41 S02, S22 |
| La casquette toupie | double take du chauffeur (yeux sur tiges), canal `hat [lift, tilt, spin]` : quatre tours et demi, elle finit à l'envers | 41 S03 |
| Le panneau girouette | le panneau seul, lui six images devant, puis 0,7 s de rotation (`townSign` : `spinAt`, `turns` 2,07, `spinDur`) qui s'arrête de travers | 41 S04 |
| Le crochet du parapluie | `crookUmbrella` (manche épais, grosse crosse jaune : sa cravate est rouge) levé au-dessus des têtes puis abattu ; accrochage tenu quatre images (clip `flag`, `dir: -1` : à plat, pieds devant), les bras de la dame sortent des manches (`bend` : `stretch 1.35`) ; départs à trois images d'écart, un bras qui s'étire avant que les pieds quittent le trottoir ; le panneau de tours reste en l'air huit images, tourné vers nous, puis tombe | 41 S05-S06 |
| Le bureau tranché | deux mains jointes en hache (`reach` avec direction du coude), une tenue qui continue de monter, deux images de descente, `splitDesk`, les objets sautent, il s'époussette les mains | 41 S07 |
| L'afficheur sur la tête (gag à répétition) | `headSign` posé sur la tête (`sway`) : 12 BIS, ARRÊT DEMANDÉ, 12 BIS, HORS SERVICE ; à l'arrêt de bus : 1 MIN, 0 MIN, 8 MIN | 41 |
| Le contrôleur surfeur et le gros poinçon | contre-plongée sur le ciel ; un seul ticket au bout d'un bras qui s'allonge ; le poinçon est un accessoire à part (orienté par calcul, mâchoires le long du ticket), la main proche guidée sur son manche ; il monte ouvert, mord (tenu trois images : le ticket saute, un trou), recule ; un confetti part au vent | 41 S12 |
| Le bouton d'arrêt sur le nœud de cravate | trois images : visage (langue au vent en ruban, les yeux descendent), insert (le bout du doigt attend à côté du bouton, tremble, recule, saute dessus : anneau rouge), visage (l'afficheur change ; espoir : sourire, pupilles × 3) | 41 S13 |
| Deux visages dont un à l'envers | clip `batHang` : le contrôleur descend dans le cadre, pendu par les pieds ; sa cravate lui retombe sur le visage (canal `tie`), il la chasse d'un revers ; il parle la tête en bas | 41 S14-S15 |
| Les pupilles qui tombent | très gros plan : pupilles larges tenues six images (`pupilSize 1.5`), puis têtes d'épingle (`-1.15`) en six images ; un sourcil cède, les paupières du bas montent, une larme | 41 S16 |
| L'arrêt au poteau | prise basse à deux mains, le corps continue à l'horizontale, pieds devant (`flag`, `then='flag'`), le poteau se plie en arc (`bend`, tenue de huit images qui tremble), retour en trois images, à plat cinq images au pied du poteau (`sq [1.55, 0.26, 1.55]`) pendant que la caméra se rapproche, regonflage avec dépassement (1,15), étoiles | 41 S18 |
| Les passagers qui continuent | lui debout au poteau, eux traversent le cadre à plat dans l'air ; puis le banc de la gare : quatre chutes en 0,3 s, quatre poignets (montres), quatre regards tenus dix-sept images | 41 S19-S20 |
| Les bras qui s'étirent (l'arrêt au poteau, troisième mise en scène) | il prend le poteau à deux mains et continue : `reach` sur deux points du poteau plié (`pole_pt`), le corps repart (`to=` à 3 m, `ease='out'`), les bras suivent (l'IK étire) ; il court sur place au bout de ses bras huit images (`clip='run'` sans déplacement, `freq 7`), penché, les yeux sur nous ; ça claque : retour en trois images (`path`, `arc`), `auto: 0` sur toutes les clés du vol ; caméra de trois quarts, basse, côté route : lui gros au tiers gauche, le poteau au tiers droit | 41 S18 |
| La crêpe puis l'accordéon | coupe deux images avant l'atterrissage ; à plat neuf images (`sq [1.8, 0.2, 1.8]`) avec un clignement sur le visage plat, la caméra s'avance de 6 % ; il remonte en accordéon (`sq [0.86, 1.22, 0.86]` → `[1.12, 0.82, 1.12]` → `[0.95, 1.08, 0.95]`, `settle`), la caméra recule en 0,16 s (`glide`) pour le garder entier ; étoiles | 41 S18 |
| Le corps écrasé sur la vitre | escalade par la taille : phalanges, poing gros comme la tête (`scl handL 1.7`), puis tout le corps : clip `pressGlass` en `glide` contre la vitre, `sq [1.22, 1.02, 0.5]`, tête `[1.3, 1, 0.5]`, mains écartées, onze images ; huit étoiles ; ses yeux glissent vers la passagère ; au freinage il glisse le long de la vitre (`sq [1.5, 1, 0.5]`) et se décolle | 41 S01 |
| Le crochet par le cou, vu de face | caméra au bord du trottoir, en aval : il court vers nous, la dame un pas hors de la file (la file reste derrière elle), le parapluie d'abord vertical au-dessus de sa tête ; elle le fauche en travers : la crosse à plat autour du cou (rotation calculée avec `axes_euler`, bout du manche à un rayon de crosse du cou mesuré par `debugJoints`) ; tenu quatre images : lui pendu au tiers droit, bras en l'air, langue dehors, elle arc-boutée au tiers gauche, le manche rayé traverse le milieu vide ; puis ils partent vers nous l'un après l'autre | 41 S06 |
| Le panneau laissé en l'air | après le départ de celui qui le tenait : seul dans le cadre contre la façade, il pend douze images en se balançant (`rotTo` alternés qui s'amortissent), tombe en cinq images, rebondit une fois | 41 S06 |
| La casquette qui saute, pend et retombe en toupie | canal `hat [lift, tilt, spin]` : 0,2 m en deux images, elle pend en tournant quatre images, retombe, tourne encore et s'arrête à l'envers ; il faut de la hauteur libre (`cityBus top: 2.65`) | 41 S03 |
| La larme qui roule | canal de visage `drop` (sous l'œil gauche) ou `dropR` : 0..1 = le chemin parcouru sur la joue, `dropSize` 1,25 = un peu plus haute que l'œil ; elle perle, grossit, roule pendant un clignement en laissant une trace | 41 S16 |
| La vapeur encrée | `face.steam` avec `steamInk: 1` : bouffées opaques cernées d'un trait, lisibles sur un mur clair comme sur le ciel | 41 S18 |
| Quatre têtes vers l'horloge | les quatre regardent leur montre (cadrans blancs, `wristWatch bright`), puis leurs têtes se lèvent vers l'horloge de la gare à 0,03 s d'écart, puis un clignement chacun, en cascade | 41 S20 |
| Le poids sur une hanche, à la main | canal toon `hip` (-1,8..1,8 ; au-delà de 1 : un vrai contrapposto) : le bassin passe sur une jambe, l'autre genou cède, les épaules repartent à l'opposé. À répéter dans chaque clé du plan qui doit le tenir ; dès qu'une clé le porte, l'appui automatique est coupé pour ce personnage. Pour « il reste » : le regard revient, puis le poids change de jambe en 0,24 s (`inOut`), les épaules tombent (`sq [1.03, 0.96, 1.03]`, `settle`) | 41 S19, S21, S22 |
| Le demi-tour en trois temps | les yeux partent (`gx`), puis la tête (`look` vers un point derrière lui, du côté où ils sont partis), puis les épaules : deux clés `face` enchaînées avec leur durée (`k(t, face=180, turn=0.14)`, `k(t + 0.12, face=70, turn=0.16)`) : il tourne du côté où il regardait, en neuf images | 41 S19 |
| Le poteau tiré par une main | `trafficLight bendGrip: 1.3` (et `pole_pt(..., grip=1.3)` côté script pour les mains) : le poteau plie depuis le pied jusqu'à la main, droit au-dessus ; le déplacement de la lampe double. Tenue de onze images, le tremblement grandit (`TR18`) | 41 S18 |
| Le cadre qui s'élargit avec l'étirement | la caméra part plus près, sur le poteau, et recule pendant qu'il s'éloigne (`ease='out'`) ; une seconde caméra sans coupe (`glide(..., 0.0)`) la fige à l'instant de l'étirement complet : la tenue se joue dans un cadre immobile. Caméra à 46° de sa ligne, côté visage, calculée sur les articulations mesurées : les bras couvrent 55 % de la largeur | 41 S18 |
| Le surfeur contre le ciel | caméra basse sur le trottoir (0,45 m), à 2,7 m, levée de 33°, focale 65 : la dame à l'horizontale en bas du cadre, le contrôleur debout sur son dos, genoux pliés, bras écartés (clip `surfRide` sans main guidée), quatre images ; puis un bras entre par la gauche avec le ticket, la pince lui saute dans la main (`scale` 0,01 → 1) | 41 S12 |
| L'ombre est un personnage | acteur `silhouette` (une seule couleur d'ombre, deux yeux blancs), aplati contre le mur (`sq [0.03, 1, 1]`) et animé à la main : en retard de 0,6 s sur son propriétaire (les mêmes clés décalées), qui regarde sa montre après lui, qui tourne la tête vers nous, qui hausse les épaules, qui pend à un cintre, qui revient avec un avocat (rabat blanc, serviette). Le héros ne projette pas d'ombre (`castShadow: False`) | 42 |
| L'ombre qui se lève | elle est à plat au sol (`lieBack`, `sq [1, 1, 0.05]`), un bras plat éteint le réveil ; elle s'assoit (`sitFloor`, `sq` z → 0,45), se lève à l'endroit de ses pieds (`stand`, `then='stand'`) : la figure plate devient un corps ; lui, sur le lit, devient plat comme un drap (`sq` z 0,07) et glisse au sol derrière elle, ses pieds aux pieds de l'ombre | 42 S20-S21 |
| Traîné par les pieds, vu du dessus | caméra presque à la verticale (4,6 m au-dessus, 0,3 m de côté) : elle est une forme sombre vue du dessus en bas du cadre, lui est à plat derrière ses talons, en diagonale, le visage à l'endroit ; pouce levé sur le goudron ; sur les pavés il tressaute (`sq`, `bend`, `pupilShake`, `tremble`) et la caméra descend vers lui | 42 S23-S25 |
| Le retard retourné | au feu rouge elle s'arrête, lui continue entre ses pieds (sa tête s'arrête sous elle), revient comme un élastique ; elle regarde sa montre (cadran blanc au poignet de la silhouette) | 42 S26 |
| L'ombre en aplat violet (cycle 7, remplace l'ombre teintée) | une seule teinte pour toutes les ombres du film (acteurs `silhouette: '#6A5878'`, accessoires `silhouette=`, pictogrammes, cases ELLE du calendrier) : un violet à mi-chemin, en valeur, entre le costume marine et le mur ; yeux = ovales blancs plats avec un trou pour pupille (`silhouetteEyes: 2`, `darkEyes: 1.8`), paupière lourde = un tiers de l'ovale au plus, fermés = disparus ; de profil, un seul œil blanc sur le côté de la tête (automatique) ; liseré plus clair (`silhouetteRim`) seulement quand elle devient un corps | 42 |
| La règle posée par un objet | au premier plan, un potelet et son ombre violette sur le mur, à l'heure (`P(..., silhouette=SHADE, flat=[0.03, 1, 1])`) : on sait à quoi ressemble une ombre normale ; plus tard le corps d'ombre passe devant ce potelet : lui a une ombre, elle non | 42 S01, S04-S05, S22 |
| Le cadran face caméra | une montre au poignet montre sa tranche ou son bracelet : poser un cadran blanc (`watchFace`) là où est le poignet pendant qu'on le regarde, face à la caméra, avec un `scale` qui apparaît et disparaît avec le bras ; sur une ombre : liseré et aiguilles dans la teinte de l'ombre | 42 S02, S10-S11, S26 |
| L'ombre sur échasses | jambes étirées 1,9 fois (`bend` legL/shinL/legR/shinR), dos 1,25, cou 1,3, et hanches relevées d'autant (y = 0,86 m) : la silhouette du héros (mèche, cravate) à la taille d'un autre ; l'autre homme a une autre silhouette (chapeau, 1,5 fois la taille du héros) | 42 S10-S11 |
| Le demi-tour d'une chose plate | une ombre de profil se tourne face à nous en une image (`face=-90, turn=0.0` et `sq` permuté le même instant) : haussement d'épaules à deux mains, mains 1,5 fois, puis retour de profil en une image | 42 S11 |
| Le double regard devant l'ombre | coup d'œil ennuyé, retour vers nous, puis la tête revient d'un coup : `pop` 0,8, tête écrasée en largeur, cou 1,22, deux images ; il se penche en arrière pour la voir en entier | 42 S10 |
| Le portant vu de face, le client devant | le héros 1,3 m devant le portant et à son bout (moitié de la hauteur du cadre), le bras passe au-dessus des têtes sur le mur nu, s'allonge jusqu'au dernier cintre ; chaque ombre refusée sursaute (`pick`), la choisie est décrochée (`gone`) et revient pendue au bout du bras (`hangBar`) | 42 S12 |
| Le sifflet dans le dos | l'agent arrive par derrière : arrêt net, deux images en l'air, retombée aplatie, demi-tour en deux temps ; la place de l'ombre manquante est alors entre les deux hommes : tout se joue là sans que personne ne pointe à travers personne | 42 S14 |
| Le bras de la loi | plan plus serré sur le mur : l'agent est hors champ, son bras entre dans l'image le long du mur : un doigt tape le mur nu, la main à plat descend deux fois sur la petite (« haut comme ça »), ressort, revient avec l'amende et la colle au-dessus d'elle, juste sous le pochoir DÉFENSE D'AFFICHER | 42 S15 |
| Le décollage | à plat au sol, elle se décolle fine comme du papier (déplacement vers l'endroit de ses pieds avec `clip='stand'`, `blend` de la durée du geste, `sq` z 0,05), se tient debout comme un carton, puis se remplit d'un coup (`sq [1.2, 0.9, 1.3]` puis rebond) ; huit images de regard vers nous | 42 S21 |
| L'homme-feuille | sur le lit il devient plat (`sq` z 0,06), quitte le lit et se met debout en l'air au bord du lit, son plat vers nous (`clip='stand'`, `face` vers la caméra), reste suspendu quatre images, les yeux vers le sol, puis glisse et se couche aux pieds de l'ombre | 42 S21 |
| Les talons seuls | vue du dessus avec une inclinaison plus faible que la moitié du champ vertical (8° pour 22°) et le bas du cadre passant par les talons de celle qui marche : d'elle on ne voit que deux talons ; lui est couché vers le haut du cadre, visage à l'endroit (`topcam`) ; les joints du trottoir, les tirets de la chaussée défilent | 42 S23-S25 |
| La vague du cahot | une dalle dépasse : talons, hanches, tête se soulèvent l'un après l'autre (0,12 s d'écart), la tête reste deux images en l'air, retombe à plat | 42 S23 |
| Sortir entre ses pieds | elle s'arrête au bord du trottoir, lui continue entre ses pieds sur les bandes blanches du passage piéton, s'allonge (`sq` y 1,36), s'arrête la tête entre ses pieds ; elle se penche ; retour élastique, il se tasse, se pose ; caméra derrière elle et sur son côté ; puis gros plan vu du dessus sur son visage plat : regard, clignement lent | 42 S26 |
| La laisse-cravate | une cravate prise dans une porte devient une ligne rouge de la nuque à la jointure des battants (`tieRope` : `on` nuque, `to` la jointure) ; le héros un pas devant la porte et bien à côté, pour que la ligne traverse le cadre à côté de sa tête ; le nœud reste sur la poitrine (cast `tieKnot`) ; chaque gag est la laisse qui le tire ou lui qui tire dessus | 43 |
| Le cou qui reste | il sort de l'ascenseur, la cravate flotte derrière lui (`toKeys` qui le suivent), les portes se ferment dessus ; deux pas : la laisse se tend : le corps continue de 30 cm (`glide`), la tête reste (cou plié en arrière, étiré 2,5), tremblement, yeux sortis | 43 S01 |
| La course sur place puis la traînée | décollé du mur (`poster` puis pop), il court sur place penché en avant (`scramble`, poussière) ; l'ascenseur monte : la laisse le ramène à reculons sur les talons (`heelBrake`, `heelSmoke` avec traces) jusqu'à la porte où il s'aplatit (un étage de plus : plus plat) | 43 S02-S03 |
| Le linge sur la corde verticale | la voisine du troisième, dans la coupe de l'immeuble, épingle sa lessive sur la cravate qui monte dans la cage (`tieRope` `items`, chaque pièce surgit) ; en bas, chaque pince le tire : une secousse, une plus forte, la serviette : il part en arrière sur les talons (`teeter`) | 43 S11-S12 |
| La corde pincée | le petit du cinquième pince la cravate comme une contrebasse (`pluck` au point de la main, notes) ; l'onde descend et l'atteint : il tremble comme une gelée (`jelly`), puis l'air l'emporte : il danse, impassible (`dance`) | 43 S13-S14 |
| Le cou jusqu'au panneau | retenu par la laisse, il se tourne vers le panneau d'affichage et son cou fait le reste (cou étiré 2,4, yeux sur tiges) ; vu de profil depuis le mur de droite ; puis la convocation en gros plan, sa tête étirée entre par la gauche | 43 S15-S16 |
| Le virevoltant en réunion | la chaise vide de l'absent, son chevalet REZ-DE-CHAUSSÉE ; un virevoltant traverse la salle de réunion au ras du sol | 43 S19 |
| Le bras jusqu'au plafond | il vote seul dans le hall : la main guidée jusqu'au plafond (`reach` à 3,55 m, le bras s'étire), la paume s'écrase dessus (`scl` handR) ; personne ne le voit | 43 S20 |
| La peinture qui descend | le peintre roule le mur et la ligne : la couleur descend la corde (`tieRope` `paint`, `color2`) ; dans le hall le beige sort de la jointure et arrive à son col ; le nœud change de couleur (canal toon `knot`, à porter dans toutes les clés suivantes) ; double regard | 43 S22-S23 |
| La facture en tyrolienne | une enveloppe sort de la jointure et file le long de la laisse (clés `to`) jusqu'à l'arrière de sa tête : écrasement de l'enveloppe, sa tête qui part en avant ; il la récupère derrière lui | 43 S24 |

| La tête écrasée par un pigeon | le pigeon se pose (`to` en `ease out`) : la tête s'écrase sous son poids (`scl head [1.22, 0.78, 1.22]` en 0,04 s), revient un peu plus plate (`[1.07, 0.92, 1.07]`) et le reste tout le film ; seuls les yeux montent vers lui | 44 S02 |
| La main qui rampe, le sifflet | une démangeaison : la main guidée monte vers le nez par paliers lents (`reach` `inOut`, 0,4 s chacun) ; le coup de sifflet la fige en l'air (yeux qui filent de côté), puis elle redescend aussi lentement | 44 S06 |
| Le socle glissé dessous | deux ouvriers le soulèvent raide comme un poteau (`stiffStand`, déplacement `glide`), le socle glisse sous ses pieds, il se pose avec un petit écrasement ; puis quatre grilles tombent du ciel une à une et claquent autour (clés `to` de 0,1 s, `squash` à l'impact, secousse) | 44 S07-S08 |
| Le jet au visage, le pigeon au sec | lance `waterJet` (jet qui tremble, gouttes qui éclatent au point d'impact) visée sur le visage (`rotOrder 'YXZ'`), le pigeon sous un minuscule parapluie ; cheveux mouillés dressés | 44 S10 |
| La loupe sur le crâne vide | l'expert tend le bras jusqu'au-dessus de la tête de la statue (la main guidée étire le bras) ; la loupe est un accessoire LIBRE, calculé pour faire face à la caméra (`ry` vers la caméra, roulis `rot z` pour que le manche descende vers la main), la main guidée sur le manche ; à travers le verre, l'amende collée sur son front | 44 S14 |
| Raide comme un poteau au bout d'une grue | crochet `craneHook` avec élingue ; il monte d'un bloc en tournant lentement, pieds joints, les yeux vers le haut | 44 S15 |

| La tête qui reste au bout de la laisse (passe 2) | la corde attachée à la tête (`on` joint `head`, à l'arrière) et non au col ; le corps repart deux enjambées (`walk` sur 0,78 m) pendant que le cou s'enroule vers la porte (`bend neck [-2.1, 0, 0, 6.0, 0.6]` : plié de 2,1 rad, la tête finit derrière et un peu plus haut ; à -1,3 rad elle montait), dépassement à 6,7 puis retour, tremblement | 43 S01 |
| Aplati un peu plus à chaque étage | sur la porte, profondeur 62 -> 46 -> 30 %, visage qui s'élargit à chaque sonnerie ; caméra à 35° de la porte (de face, l'épaisseur ne se voit pas) ; les mains sous la laisse | 43 S03 |
| Les yeux sur tiges qui lisent | `pop` 0,75 avec `eyeYaw` (pupilles ramenées vers la caméra qui filme les tiges de côté) et `eyeRoll` qui descend de -0,55 à +0,55 en quatre clés : les pupilles descendent les quatre lignes de l'affiche | 43 S16 |
| La forêt de bras au plafond | même vote, nouvelle image : caméra basse dans le coin, le plafond dans le cadre ; chaque bras plonge d'abord (creux), jaillit jusqu'au plafond, la main s'y écrase (`scl hand [1.4, 0.5, 1.4]`), redescend de 10 cm et remonte (dépassement) | 43 S21 |
| Embarqué par le col | le crochet de la dépanneuse tombe derrière sa nuque ; il remonte : jambes, dos et cou s'étirent (×1,45) pendant que les pieds restent sur la route ; puis ils lâchent : il monte d'un coup et pend comme une nouille (`noodle`) pendant que la dépanneuse l'emporte | 45 S04-S05 |
| La voiture-personnage | `carToon` : phares-yeux (pupilles `gaze`, paupières `lids` avec inclinaison, clignements), warnings, klaxon qui l'écrase et la fait sauter avec des anneaux, essuie-glaces qui moulinent et s'allongent vers ce qu'elle ne peut pas atteindre (elle penche sur deux roues : `rotOrder 'YXZ'`, roulis `rotTo[0]`) | 45 |
| Le compas | le pied pris dans le sabot ne bouge pas : il fait un tour complet autour, huit pas de 45° (`face` et `to` en glissé autour du pied, mollet qui s'agite), puis des étoiles | 45 S09 |
| La carte grise à la photo | la caissière plaque la carte grise contre la vitre : PROPRIÉTAIRE : et une voiture miniature en guise de photo (le même accessoire à l'échelle 0,085) ; contrechamp de l'intérieur du guichet, à travers la vitre : `doubleTakeToon` | 45 S11-S12 |
| Trois semaines en accéléré | `daynight` (période 0,42 s), le klaxon toutes les 0,14 s, les contraventions qui s'empilent sous l'essuie-glace (`pv`), les feuilles mortes, les fenêtres d'en face qui s'allument la nuit (`flatsWall lit`) | 45 S15 |
| Les voisins usés (gag à répétition dans un plan) | à la fenêtre : premier klaxon, ils sautent (étirés, cheveux dressés, yeux sortis) ; deuxième, à peine (paupières lourdes) ; puis ensemble la feuille PLAINTE, yeux en points ; le troisième klaxon ne les fait plus bouger | 45 S16 |
| L'homme-ballon retenu par son sabot | les plaintes collées sur la poitrine, il gonfle d'indignation (`inflate`), monte d'un mètre ; la jambe prise dans le sabot s'étire jusqu'au sol (×1,9) comme la ficelle du ballon ; le corps décalé du côté opposé (le clip écarte la jambe) | 45 S17 |
| Garée sur lui | temps suspendu sous la voiture qui pend au-dessus de sa tête (il déglutit, petit salut) ; elle tombe en 0,1 s, rebondit sur ses ressorts, poussière, étoiles ; sa tête aplatie dépasse devant le pare-chocs, langue déroulée, filmée d'au-dessus (au ras du sol ce n'était qu'un trait) ; la baguette aplatie à côté | 45 S20-S21 |
| Le bras jusqu'à l'horodateur | couché sous la voiture, son bras s'étire jusqu'à la fente de la borne, prend le ticket et le tient près de son visage plat ; la voiture le regarde, cligne et donne un tout petit coup de klaxon | 45 S22 |

| La tête aplatie à moitié | le pigeon se pose : `scl head [1.55, 0.5, 1.55]` en 0,03 s, yeux exorbités (`eye 0.7`), tenu deux images, regonflé au-delà du rond (`[0.9, 1.16, 0.9]`), posé un peu plus plat ; la tête ne tourne pas, seuls les yeux montent (il ne doit pas bouger) | 44 S02 (passe 2) |
| Soulevé comme une planche | deux ouvriers de trois quarts, accroupis, une main sous l'aisselle et une à la hanche (`reach` sur les points du corps soulevé, aux mêmes temps que son `to`) ; il monte raide en penchant (`lay [0, 0.26]`), tenu en tremblant pendant que le socle glisse dessous ; lâché : écrasement 1,16 / 0,82 ; le pigeon s'écrase et bat des ailes | 44 S07 (passe 2) |
| La file pour le selfie | caméra dans l'axe de la file (elle s'enfonce dans le cadre, chacun de trois quarts) ; le premier tourne le dos à la statue, téléphone à bout de bras levé ; flash : `fx flash` + `burstLines` blancs au téléphone ; coupe immédiate sur ses pupilles en têtes d'épingle et ses larmes | 44 S09 (passe 2) |
| Le jet aux yeux grands ouverts | le jet jaillit (`waterJet ramp 0.15`) ; gros plan : yeux écarquillés qui pleurent (`tears`, `pupilShake`), joues qui ondulent, cheveux et cravate soufflés dans l'axe du jet ; il ne cligne pas : c'est le plan suivant | 44 S10 (passe 2) |
| Le clignement qui lutte | les paupières tremblent et résistent (cinq clés de `lid` entre 0,12 et 0,55 en 0,3 s), tombent lourdement (0,22 s, `in`) sur un clac, se rouvrent sur « oh non » | 44 S11 (passe 2) |
| Le bras par-dessus la grille | l'agent, hors de la grille et de trois quarts, tend un bras étiré trois fois jusqu'au front et y colle l'amende, attachée à la tête : elle suit le boing et la grue | 44 S12 (passe 2) |
| Le boing à 140 % | l'oiseau s'envole : tête `[0.8, 1.42, 0.8]` sur un cou étiré ×1,5, puis trois rebonds qui décroissent (0,8 / 1,18 / 0,93 / 1,04), l'amende battant sur le front | 44 S13 (passe 2) |
| L'écharpe INCOMPLÈTE | un expert regarde le crâne vide à travers une loupe géante (×1,5) en secouant la tête ; l'autre colle en travers de la poitrine une bande INCOMPLÈTE (attachée au torse, `rot z -0.5`) comme une écharpe d'élu ; elle reste jusqu'au rond-point avec l'autocollant et l'amende : la pile de paperasse paie à la fin | 44 S14-S17 (passe 2) |
| Les yeux sur tiges qui suivent le bus | caméra du trottoir : le bus passe entre nous et lui (on le devine à travers les vitres) ; avant, les yeux sortent vers lui (`pop`, `eyeYaw`), après, ils sont tournés vers où il file, cheveux et cravate couchés dans le sens du vent ; ils rentrent d'un coup ; plan serré : le dernier pigeon l'aplatit à 42 %, regard résigné vers le haut | 44 S17 (passe 2) |
| L'affiche qui se décolle | une carte sur le mur (`sq z 0.15`) en X, tenue quatre images ; elle glisse (`to` vers le bas, `sq y 0.86`) ; le haut se décolle d'abord (`lay [0.22, 0]`), puis il se détache en se regonflant au-delà du rond (1,3 / 0,84) avec deux rebonds | 43 S02 (passe 3) |
| L'écrasement étage par étage, vu de face | à chaque étage : 20 % plus large, plus court (il s'enfonce le long de la porte), genoux qui partent en dehors (`legL`/`legR` en `bz`, `shinL`/`shinR` en sens inverse) ; un à-coup dépassé de 0,03 s à chaque tic | 43 S03 (passe 3) |
| La voiture sur deux roues | `carToon` basculée de 20° (roulis en `rotTo` et 0,3 m de remontée sur ses roues droites), essuie-glaces qui quittent la vitre et s'étirent vers le clavier de l'horodateur (`reach`, `reachTo`) et s'arrêtent à une main (`reachShort`), tremblants ; tenue neuf images, retombée avec rebond | 45 S13 (passe 2) |
| La chute vue du capot | le visage aplati filmé depuis l'arrière du capot, caméra qui regarde vers l'avant : le haut du crâne monte dans le cadre, le visage se lit à l'endroit ; gros plan sur le ticket FRAIS DE GARDE tenu face caméra (`face: 'camera'` dans l'attache) ; puis la voiture : clignement, petit klaxon | 45 S21-S22 (passe 2) |
| Les yeux qui descendent la marge | la tête basculée par-dessus le panneau (hors cadre, en haut à gauche), les tiges pendent à côté de l'avis et s'allongent ligne par ligne (`popLen` 0,36 → 0,54 en quatre crans) : les yeux descendent la marge, pupilles vers nous (`eyeYaw` ≈ -2,4 quand on filme les tiges de dos) et qui baissent (`eyePitch`) ; l'avis épinglé à droite pour leur laisser la place | 43 S16 (passe finale) |
| Le crochet verrouillé sur le col | le corps s'étire ×1,8 (jambes ×1,8, colonne ×1,5, cou ×2,3) en sept images avec la même durée et la même courbe que le crochet (hauteur = repos + montée × étirement) ; tenu cinq images en frissonnant entre 100 et 104 % (jamais au repos) ; les pieds lâchent : traînée de deux images (`sq [0.7, 1.45, 0.7]`), il pend mou, bras et jambes en ondulation | 45 S04 (passe 3) |
| Le sursaut sur un pied pris | clac : écrasé deux images, puis claqué à l'extrême (jambes ×1,45 vers le haut, le pied pris reste, bras en l'air avec la baguette, cheveux dressés), tenu neuf images en frissonnant, retombé en écrasement dépassé, posé ; l'agent à genoux de profil, bien à l'écart, caméra qui pousse vers la pince | 45 S08 (passe 3) |
| Les petits bras qui n'atteignent pas | essuie-glaces en deux segments avec un coude levé et une lame en travers au bout qui bat ; ils s'arrêtent à une main du clavier (`reachShort` 0,32 : du mur clair entre les deux), traits de tremblement aux bouts ; un insert serré sur les lames tremblantes devant le clavier, puis le plan large pour la retombée | 45 S13 (passe 3) |
| Le klaxon qui ramasse | 0,1 s avant : écrasée de 20 %, yeux plissés ; puis étirée, elle décolle (0,3 m, `honkHop`) et retombe avec un rebond ; les anneaux partent de la calandre sous les yeux et montent en grandissant (pour une rafale en accéléré : `honkHop: 0.12`) | 45 S14-S15 (passe 3) |
| Le ballon qui gonfle face à nous | les joues d'abord (0,1 s), puis la tête rouge, le corps rond en neuf images (`balloonSuit` 0,55 puis 1 en `outBack`), les plaintes collées sur le devant une fois rond ; il ne décolle qu'après, toujours face caméra (`face=` sur le déplacement), la jambe pincée tirée en ficelle | 45 S17 (passe 3) |
| La photo du radar | vue du radar lui-même (caméra devant le boîtier, objectif 52) : il court vers nous ; le saut part 0,4 s avant l'éclair (`run` puis `dashOff`) pour être figé en grand écart de face à quatre mètres, yeux exorbités (`pop 0.5`), langue au vent ; `fx flash` puis `freeze {at: éclair + 0,1 s, filter: 'saturate(0.18) sepia(0.25) contrast(1.08)'}` : la photo lavée tient jusqu'à la coupe | 46 S02 (passe 2b) |
| La plaque vissée dans le dos | de dos et de trois quarts : l'agent visse quatre fois au tournevis jaune (`screwdriver` tenu avec `rot [π, 0, 0]`, la main reculée de la longueur de l'outil), un sursaut écrasé-étiré à chaque vis, paupières qui retombent, impassible | 46 S08 (passe 2b) |
| Le pont qui le monte par les aisselles | les bras du pont sous ses aisselles d'un bout à l'autre (`carLift lift` en hauteurs absolues, `smoothstep`), raide comme un poteau, pieds qui pendent, petit à-coup en bas, rebond en haut ; une seule caméra frontale qui monte avec lui (`drift y`) | 46 S09 |
| La jambe en caoutchouc | le mécanicien, filmé du côté où il ne cache rien, arme et shoote dans la chaussure qui pend : la jambe fait quatre allers-retours qui décroissent (`bend` + `wave` sur `legR`/`shinR`) ; deux coups, puis pouce levé vers nous avec la main éloignée | 46 S10 (passe 2b) |
| Les portes qui se ferment devant lui | le bus entier à l'arrêt, vu de devant le long de ses portes (`doorSide: 'left'` pour qu'elles donnent sur le trottoir) : elles se ferment alors qu'il court encore loin derrière, puis plan serré sur lui qui court vers nous, langue au vent, le bus qui sort du cadre | 46 S01 (passe 2b) |
| Le trou bleu ciel dans le mur | filmé dans l'axe du vol, de derrière lui : il part des rouleaux bras en l'air, s'écrase à plat sur le mur (`sq` z 0,25 pendant quatre images, un frisson, une regonfle) puis le mur éclate : `burstWall` `holeColor` bleu ciel saturé, `holeEdge` brique, `edgeW 0.16`, `debrisColor` brique ; le trou au centre du cadre, à mi-hauteur ; puis le mécanicien se retourne vers nous, la feuille REFUSÉ à hauteur de poitrine sous le bandeau, le trou derrière lui | 46 S13 (passe finale) |
| Le gobelet levé vers nous | `takeawayCup` tenu avec `face: 'camera', faceFlat: True` (debout, manchon vers nous, ×2,1) : à la poitrine quand le bus le pousse, à la bouche pour la gorgée, à côté du visage pour le toast final | 46 S15-S16 (passe finale) |
| Le « moi ? » en haussement d'épaules | une tenue impassible vers nous (9 images), un écrasement, la tête qui claque vers le panneau yeux sur tiges tenus 9 images, puis les deux mains écartées hors de sa silhouette, paumes en l'air, sourcils levés | 46 S04 (passe finale) |
| Les couverts qui volent en arc | chaque couvert frissonne, part étiré le long de sa trajectoire (`squash [0.75, 1.5, 0.75]`), suit un arc (deux clés `to` avec un point haut) et s'écrase à l'impact ; manches noirs pour le contraste sur un mur pâle ; un sursaut avec la tête qui claque en arrière à chaque coup | 47 S02-S03 (passe 2) |
| Les lampadaires qui saluent | filmés dans l'axe du trottoir : un petit contre-penché, puis ils s'inclinent au-dessus de lui quand il passe, repassent la verticale et se posent | 47 S06 (passe 2) |
| La rangée de boussoles | caméra haute (3,4 m) : il marche derrière la rangée et dépasse au-dessus des têtes, un trou dans la rangée là où il est sur « lui » ; chaque aiguille le suit (`compass upright path`) | 47 S08 (passe 2) |
| La grue jusqu'à sa fenêtre | sur les randonneurs qui lèvent leurs boussoles à côté de la tête (cadran face à nous, aiguille vers le haut), puis la caméra monte en grue (`cam` avec `to` plus haut et `look2` sur la fenêtre) jusqu'à lui, accoudé à sa rambarde | 47 S09 (passe 2b) |
| Le fanion planté au pôle Nord | vu de haut dans la cage d'escalier : deux explorateurs pliés en deux montent la dernière volée ; l'un tire le fanion de son sac, le lève et l'enfonce dans le paillasson PÔLE NORD d'un bras élastique ; la porte s'ouvre sur lui | 47 S16 (passe 2) |
| L'étiquette au pistolet | le pistolet claque sur son front endormi : tête écrasée (`scl head [1.18, 0.78, 1.18]`), il dort toujours ; gros plan sur l'étiquette 2,49 € | 48 S02 |
| Le film sous vide qui colle | `vacuumBag parts` (jambes, buste bras collés, tête) : sur « vide » le film se plaque sur chaque partie, avec reflets et plis ; son visage écrasé dessus (`scl head [1.3, 0.95, 0.5]`, joues gonflées, yeux exorbités), sur un présentoir rouge | 48 S09 (passe 2) |
| Le tampon qui le fait regonfler | le tampon écrase le paquet en accordéon, puis le sachet regonfle d'un coup (`tight` au-dessus de 1,35) et lui avec, la tête qui reprend sa forme en dépassant : le défaut de fabrication | 48 S11 (passe 2) |
| Le diable en boîte | il jaillit du carton étiré à 140 %, bras jetés en l'air, rabats qui s'ouvrent d'un coup (`cardboardBox flapsAt`), dépasse puis deux oscillations qui décroissent ; les yeux de sa mère descendent avant sa tête | 48 S13 (passe 2) |
| Les coups qui traversent le corps | `JOLTS(times)` : le buste tiré vers le métal une image avant, enfoncé au contact (bras rejetés en arrière, genoux qui plient : `sq` aplati), un recul après le dernier coup ; jamais une tête qui claque sur un mannequin figé | 47 S01-S05 (passe 3) |
| La poêle qui s'imprime | il se retourne vers nous, la poêle arrive carrée sur tout son visage, tête en crêpe (`scl head [1.5, 1.22, 0.42]`), bras jetés ; quatre images, puis elle se décolle par le haut et pend sous son menton trois images (`rotTo` + `to`), l'anneau rouge imprimé sur le visage (`panPrint`), et tombe sur sa poitrine ; la tête regonfle au-delà du rond, yeux sur tiges | 47 S05 (passe 3) |
| Les lampadaires en tiges | `stemLamp` (huit segments, la courbure plus forte vers le haut) : à tour de rôle ils s'inclinent jusqu'à ce que la tête arrive à son visage (-1,4 rad), puis se redressent en dépassant la verticale quand il passe dessous | 47 S06 (passe 3) |
| Les couverts qui volent étirés | ils tremblent sur le plan de travail (petits sauts, bascules `rotTo`), puis chacun se tourne dans l'axe de son vol (`rotOrder 'YXZ'`, `[π/2, cap, 0]`), s'étire 2,4 fois et s'aplatit à l'arrivée | 47 S02-S03 (passe 3) |
| Le bateau qui pique du nez | `sailboat brake` : la coque pique sur sa remorque et se balance (amortie), le mât fouette un temps après ; le skipper part en avant puis en arrière (`lay`), la boussole toujours levée à côté de sa tête | 47 S10 (passe 3) |
| La maison qui monte au pôle | `globe houseLat` : son immeuble fait le tour du globe qui tourne, puis glisse jusqu'au pôle quand le globe s'arrête (posé au pôle dès la première image, la rotation ne montrait rien) | 47 S14 (passe 3) |
| La caisse vue d'au-dessus de sa poitrine | une caméra qui voyage avec lui le long du tapis, au-dessus de sa poitrine et tournée vers son visage : visage droit et grand, l'écran client tourné vers nous à côté (`face: 'camera'`), la douchette à poignée pistolet (`handScanner`) qui passe au-dessus de l'étiquette ; les yeux jaillissent vers nous | 48 S04 (passe 3) |
| La colère en accents | des coups tenus plutôt qu'un va-et-vient de deux poses : un recul, le coup (`outBack`), tenu ; buste penché, tête en avant, rouge qui monte ; la dernière pose (bras levés, bouche ouverte) passe la coupe et le laser le fige dedans, tremblant, le rouge qui se vide | 48 S05-S06 (passe 3) |
| Le rétrécissement en quatre temps | il s'étire, s'écrase sous la moitié (trois images), rebondit au-dessus, se pose à la moitié ; l'étiquette rétrécit au même instant (deux étiquettes, visibilité échangée) ; en gros plan il se regarde, puis yeux sur tiges vers nous | 48 S08 (passe 3) |
| Le tampon imprimé sur le film | un vrai tampon dans le poing (`rubberStamp`), levé haut, abattu sur le paquet : accordéon tenu quatre images, regonflé au-delà avec un tremblement ; DÉFAUT DE FABRICATION imprimé en rouge sur le film (`vacuumBag stamp`), plis visibles (`creaseN`, `creaseW`, `creaseL`), l'air qui sort par le haut (`dustPuff once`) | 48 S09-S11 (passe 3) |
| La poignée de main de profil | la copie face à nous, plate comme une feuille, tend le bras dans son propre plan avec une onde qui le descend (aplatie, elle ne peut pas tendre le bras vers l'avant) ; puis un insert au-dessus du bureau : le tampon tombe, EMBAUCHÉ | 49 S04 (passe 2) |
| Le recto verso en trois temps | la face tenue, un petit écrasement, un quart de tour jusqu'à la tranche (une ligne, tenue trois images), puis le dos : son visage imprimé là aussi, qui cligne (`backFace blinkAt`) | 49 S07 (passe 2) |
| La pile de réclamations | `paperFountain stack rain` : les feuilles tombent d'en haut en virevoltant et s'empilent autour de lui, bords en dents de scie, jusqu'au menton ; yeux sur tiges quand ça arrive au cou ; une dernière feuille se pose sur sa tête | 49 S12 (passe 2) |
| Les aiguilles qui le montrent | des boussoles tournées vers nous (`face: 'camera'`, `upright`), `north: [0, 1, 0]` pour partir du N, puis `path` qui garde l'aiguille sur lui ; recalculées après l'orientation caméra (`afterFace`, l'heure du plan prise dans `Pp.lastT`) ; il s'arrête dans le trou de la rangée et se tourne vers nous | 47 S07-S08 (finale) |
| L'homme couché comme un article | caméra fixe au-dessus de sa poitrine : tout son corps raide sur le tapis parmi les courses, le visage droit au milieu, l'écran client entier en haut à droite tourné vers nous, la douchette qui arrive par le haut et repart avant que les yeux jaillissent | 48 S04 (finale) |
| Une seule grande prise | des yeux sur tiges partout ne font plus rire : une petite prise ailleurs, une grande en vrai gros plan (le visage au tiers du cadre, mâchoire tombée, yeux vers l'objectif, tenue), et d'autres réactions (étoiles qui tournent, grimace, ta-da) | 48 S08 (finale) |
| Le sous-vide qui aspire | la tête aspirée 30 à 40 % plus étroite (`scl head [0.66, 1.1, 0.72]`), yeux exorbités, bouche en cul de poule (`kiss`), le film étroit sur la tête ; un clignement, des regards de côté | 48 S09 (finale) |
| Le hoquet d'un mètre | `HICK()` : un ramassé sur le canapé, un mètre droit en l'air dans la pose assise, étiré, le haut tenu, la chute, l'écrasement ; la bulle « HIC ! » (`hicBurst`) ; un repère « 1 m » au mur | 50 (cycle 12) |
| Collé au plafond en étoile | `lay [π/2, 0]` face vers le sol à hauteur du plafond, aplati (`sq` z 0,6), bras et jambes écartés ; un plafond (`plainWall` tourné vers le bas) ; caméra au sol qui regarde en l'air, les pompiers bouche bée en bas du cadre | 50 S10 (cycle 12) |
| La double prise | `doubleTake(t0, cible)` : un coup d'œil, retour vers nous, puis la tête qui revient d'un coup, yeux sur tiges, tenue | 50 S11 (cycle 12) |
Gags du rig pas encore servis (la langue au vent et la vapeur aux oreilles l'ont été dans la 41) : langue déroulée, vapeur aux oreilles, `inflate`, `noodle`, `stretchGrab` horizontal, `doubleTakeToon`, expressions `zap`, `dotEyes` (`paperThin` : servi dans la 40). Versions de la première passe remplacées (ne pas les reprendre telles quelles non plus) : crêpe verticale `pancake`, take du policier, bras levé tendu du maire, `periscope` en poteau droit.
| Le hoquet impassible | le corps fait toute la violence (ramassé, un mètre en l'air étiré, sommet tenu quatre images, chute, écrasé à l'atterrissage), le visage reste las (joues qui gonflent, bouche « hic », paupières lourdes) ; la grande prise gardée pour la peur et le préfet ; `HICK()` dans `story_hoquet.py` | 50 S01-S13 |
| Les joues pleines d'eau | le verre à l'envers : gorgées (`puff` 0,55 par coups de 0,16 s), puis le hoquet le jette en l'air les joues pleines (`puff` 1, bouche `kiss`), l'eau gicle | 50 S08 |
| La jambe collée qui s'étire | `plant` : le pied tenu au point de la gomme pendant qu'il marche, la jambe s'étire au double (IK hanche-genou), puis le poids passe à 0 en 0,05 s : la jambe claque, onde `wave` sur la cuisse et le tibia (phase 0 à 2 en 0,3 s, `free`), le fil naît au même instant | 51 S02 |
| La jambe-manivelle | `plant` en cercle (12 clés par tour à 1,5 tour/s) synchronisé avec le fil qui tourne (`spin`) : il lit son journal, impassible, la jambe tourne comme la corde à sauter des enfants à l'autre bout | 51 S06-S07 |
| Pendu par le pied, il tape encore | `lay: [0, π]` (tête en bas, face à nous), balancement par clés, jambe libre repliée, mains guidées sur le clavier ; le visage au-dessus du bureau (dessous, il disparaissait derrière) | 51 S09 |
| Le rouleau collé | le rouleau de peinture (accessoire libre qui suit l'ouvrier, ses mains sur le manche) peint des tirets blancs sur le fil, puis colle : un fil rose s'étire du rouleau (`tether` de l'accessoire au fil) et casse ; la plaque se balance | 51 S05 |
| Le vol à l'horizontale | caméra qui le suit à la même vitesse au-dessus des toits, centrée sur le milieu du corps ; `lay [0, -π/2]`, traînée de vitesse `smear` 0,6, cheveux dressés, impassible ; le fil part de son pied devant lui | 51 S12 |
| Planté comme une fléchette | il tombe tête en bas et s'enfonce la tête la première dans son canapé (la tête dans le coussin), écrasement à l'impact, poussière, les jambes tremblent (`wave`) puis s'affaissent | 51 S13 |
| Recto verso | deux copies plates dos à dos, décalées de 2 cm, qui tournent ensemble ; le décalage s'inverse pendant le quart de tour (la tranche) : l'autre face est le même visage imprimé, qui cligne | 49 S07 |
| Le pied à coulisse qui pince | accessoire à l'échelle 1,6, mâchoires sur la poitrine et le dos dès la première image, pincé à la moitié de son épaisseur en quatre images (`sq` z 0,45, élargi), corps poussé contre la mâchoire fixe, regonfle au-delà et repousse les mâchoires, affichage tourné vers l'objectif (`dispRy`) | 49 S10 |
| L'assoupi qui sursaute (début et fin) | la tête qui tombe lentement (`neck` 0,4 à 0,45 en presque une seconde, paupières à 0,85-1) puis remonte d'un coup (0,06 s, sourcils levés) ; repris au dernier plan, la canette à la main : le film finit comme il a commencé | 50 S01, S13 |

| L'escalade dans le corps | un plan règle (deux sauts identiques, une règle jaune « 1 M » dont la plaque saute au repère, `heightRuler`), puis chaque reprise change le corps : plus haut et le ruban du cordon qui casse (`cordon snap`), en portefeuille, aplati dans le plâtre, suspendu 0,4 s en respirant (`HICK(..., hang=0.4)`), le chèque laissé en l'air | 50 (cycle 14) |
| La peur en une seule image | cheveux dressés (`hairUp` 1,3), yeux sur tiges et cri (`jaw` 0,8 : bouche `scream`) sur la même image, tenus huit images en tremblant, puis le départ ; celui qui fait peur lève les bras en V à côté de sa tête (croisés, ils cachaient son cri) | 50 S09 (cycle 14) |
| Le portefeuille | sauté hors des mains des pompiers : il s'ouvre en montant (`spine` -0,6, jambes en arrière), se referme en haut (`spine` 1,25, jambes à 1,1), redescend plié ; l'eau bleue jaillit de ses joues (`waterDrops`) | 50 S08 (cycle 14) |
| Aplati dans le plâtre | déjà collé au plafond, le hoquet l'y enfonce : `sq [1.32, 1.06, 0.22]` et 8 cm plus haut en une image, fissures qui rayonnent en 0,08 s (`ceilingCracks`), écailles de plâtre qui flottent (`waterDrops` g 2,5), puis il se regonfle au-delà (`outBack`) | 50 S10 (cycle 14) |
| La plume qui s'envole | le sismographe à l'encre épaisse (`ink`), le montant décalé (`postX`), au deuxième pic la plume part en arc (`penOff`) ; le sismologue a le nez sur le papier huit images avant que sa tête remonte, yeux sur tiges | 50 S03 (cycle 14) |
| La révélation sur le mot | le zoom de la carte en 0,7 s (`zoomDur`, `ease.inOut`) se pose sur le mot ; l'étiquette surgit sous le point sur le mot (`labelAt`, `labelBelow`), l'en-tête entier en haut ; rien sur la carte du plan d'avant | 50 S05 (cycle 14) |
| La façade qui saute | tout l'immeuble (et sa porte) saute de 22 cm trois images (`to` par clés) avec un écrasement ; la cause à l'image : « HIC ! » à sa fenêtre, de la poussière et des gravats | 50 S06 (cycle 14) |
| Le chèque géant en feuille morte | `bigCheque` (le montant sur la moitié de sa hauteur) tenu par un coin ; au saut il monte avec lui, reste en l'air, puis redescend en feuille morte (`flutter`) | 50 S12 (cycle 14) |
| Le doigt sur le seul bouton vert | l'insert filmé de l'autre côté du panneau, d'en haut : le doigt descend vers nous sur le bouton, appui tenu six images (`pressDur`) ; l'écran du panneau n'est plus vert, le bouton est le seul vert | 49 S06 (cycle 14) |
| Recto verso d'un seul contour | les deux moitiés raides (`stiffStand`), sans regard ni balancement (`toon: {shift: 0, holdLife: 0}`), séparées de 12 mm : un seul contour, le quart de tour en trait | 49 S07 (cycle 14) |
| Le pied à coulisse presque de profil | à 53° du profil, son épaisseur devient une largeur à l'écran ; la règle à 1,5 fois son épaisseur, l'affichage déporté au-delà du coulisseau (`dispX`), la copie devant lui tournée par la tranche vers l'objectif | 49 S10 (cycle 14) |
| Les pieds rattrapent la tête | au départ d'un saut, une image de traînée (`sq` [0,76 ; 1,42 ; 0,76]) ; la tête atteint le sommet sur l'étirement et y reste pendant que le corps monte du reste (les pieds rattrapent) ; à la chute, l'étirement attend que le corps soit lancé : plus d'accroc au sommet | 50 (cycle 14, passe 3) |
| La tête-ballon | la grande inspiration : la tête enfle (`scl: head` ×1,3) avec le visage `puffed` (yeux ouverts, sourcils froncés) ; elle reste gonflée pendant l'effort (visage `strain` : yeux plissés, dents, veine) et se dégonfle d'un coup quand les yeux sortent | 51 S10-S11 (cycle 14) |
| Le ruban qui fouette | le ruban du cordon casse en deux moitiés qui reviennent en fouettant vers leurs poteaux, une onde le long de chacune, puis pendent ; la plaque fait un tour complet vers l'objectif en tombant (`cordon` `snap`) | 50 S07 (cycle 14) |
| Le stylo qui s'envole | l'aiguille du sismographe part en arc vers le haut, grossit du double en route et laisse trois copies qui s'effacent derrière elle : une traînée (`seismograph` `penOff`) | 50 S03 (cycle 14) |
| Le drap qui se froisse | `unveilCloth` : un drap souple à plis et ourlet festonné qui se balance ; tiré, il se froisse, son bord haut s'enroule et il se ramasse au tiers de sa hauteur pendant que ses clés l'emportent. Accroché à une tête (`on` joint `head`), c'est aussi le drap noir du photographe | 50 S11, 52 S12 (cycle 14) |
| La prise vers nous | la double prise d'un homme qui marche : coup d'œil à la chose derrière lui, retour au téléphone, il s'arrête, et la prise vers l'objectif, yeux sur tiges, bras ouverts, avant-bras baissé (l'objet quitte le visage) | 51 S02 (cycle 14) |
| Le saut image par image | un saut clé à clé à 30 images/s : la tête monte sur une seule courbe jusqu'au sommet sans jamais redescendre, les pieds la suivent sur une courbe plus lente, et l'étirement n'est que l'avance de la tête sur les pieds (la tête ne dépasse jamais le sommet ; la première image en l'air est la traînée) ; à la descente les pieds mènent, la tête suit deux images plus tard ; l'écrasement à l'arrivée est dosé par la hauteur. `autoSq: 0` dans chaque clé du saut | 50 (cycle 15, passe finale) |
| Chaque saut sa silhouette | le même gag qui revient change de pose en l'air : boule jambes repliées et bras en ailes, flottement lent bras écartés avec la cravate et les cheveux qui montent (`wind` vers le haut), torsion qui rattrape l'objet laissé en l'air | 50 S07, S11, S12 (cycle 15) |
| Il tape même la tête en bas | pendu par le pied au-dessus de son bureau, il se balance et ses deux mains restent sur le clavier, en frappe alternée (cibles miroir, sans balancement de poids) | 51 S09 (cycle 15) |
| Le « oh-oh » à plat | arraché du trottoir, il se retrouve à l'horizontale face à nous, bras au-dessus de la tête le long du fil, cinq images de suspension, puis il part étiré hors du cadre en laissant des traits de vitesse et une petite poussière | 51 S11 (cycle 15) |
| Le fil qui s'étire jusqu'à casser | le rouleau colle : l'ouvrier se penche en arrière à 35 degrés, un pied levé, le fil de gomme s'étire à longueur de bras, casse, il recule en titubant et la plaque oscille sur sa dernière vis | 51 S05 (cycle 15) |
| Le V sous la cabine | un téléphérique accroché au fil de chewing-gum : les ancrages proches (±20 m) font un V net sous la pince (13 degrés), la cabine se balance, les passagers regardent en bas | 51 S08 (cycle 15) |
| Le cratère qui s'agrandit | collé au plafond : la bosse de la frayeur est déjà là au début du plan, le hoquet l'agrandit (fissures ramifiées, éclats pâles, contour de cratère) ; une corniche et un lustre qui se balance au choc donnent la perspective vue d'en bas | 50 S10 (cycle 15) |
| L'eau en larmes cernées | l'eau qui sort de la bouche : des gouttes en larmes cernées de noir, la pointe en arrière, et un filet de gouttes plus lentes qui relie la gerbe aux lèvres ; le verre d'un bleu franc dont le niveau baisse à chaque gorgée | 50 S08 (cycle 15) |
| Le lancer en élastique | le bras tiré deux fois sa longueur derrière lui (`reach` + `hose`), la colonne enroulée, la langue sortie, cinq images de tremblement, le fouet, le boomerang qui quitte la main lentement puis accélère (huit images dans le cadre) | 52 |
| La toupie de la suite du lancer | un tour et demi sur place (clés `face` successives), la tête mène, les hanches et les jambes traînent, genoux pliés, trois oscillations d'étourdi, la main en visière à côté de la tête (vue de dos) | 52 |
| La main tamponnée en crêpe | le tampon REFUSÉ s'abat sur le formulaire et les doigts : la main aplatie (`scl.handR` [2, 0,18, 1,7]) tenue huit images, REFUSÉ imprimé dessus, puis regonflée au-delà avec deux tremblements, le tout dans un insert vu d'en haut | 52 |
| La tête qui suit le boomerang tout autour | le boomerang fait le tour de la pièce une tête au-dessus de la sienne (caméra plus haute : une ellipse) ; la tête suit d'un tour complet sur un cou étiré en spirale (twist 2π, stretch 1,8), puis revient au-delà en ressort | 52 |
| L'avion qui freine comme une voiture | l'avion de ligne pile devant un passage piéton peint dans les nuages (panneau bleu `crossingSign`) : nez plongé, fuselage écrasé de 18 %, petit rebond poli, salut de l'aile, puis accroupi et étiré en repartant | 52 |
| La tête en disque, le boomerang en rotor | le boomerang tombe sur sa tête : tête écrasée en disque (`scl.head` [1,45, 0,42, 1,45]), le boomerang tourne dessus comme un rotor (disque de flou dense), les cheveux des invités soufflés vers le haut, les sourires figés ; il s'envole avec un plongeon, un rebond et les jambes en balancier | 52 |
| Le CRAC à 180 degrés | une lente rotation par-dessus l'épaule, un cran en arrière (anticipation), puis la tête fait le tour en une image jusqu'à son dos, 20 degrés au-delà, cinq images de frisson ; le visage reste sur le dos tout le film | 53 |
| La cuillère qui se trompe de trou | le visage sur le dos : la cuillère monte par-dessus l'épaule au bout d'un bras plié à l'envers, dans la bouche, puis dans l'oreille (giclée de lait, la tête écrasée, un clin d'œil) | 53 |
| La marche à reculons et son témoin | le cycle de marche joué à l'envers (`speed: -1`), filmé sur son chemin à hauteur de hanche, à côté d'un passant qui marche à l'endroit ; la dame qu'il croise : regard, regard ailleurs, retour avec étirement et mâchoire jusqu'au col | 53 |
| Le permis en miroir | un permis rose dont tous les mots sont à l'envers, la photo d'un arrière de tête, tenu à plat face à l'objectif à côté de son visage sur le dos | 53 |
| La marche arrière au boulevard | la petite décapotable rouge descend le boulevard en marche arrière, son visage par-dessus le siège, la circulation de face ; le conducteur doublé : chapeau qui saute, mâchoire sur le volant | 53 |
| Les trois tours de toupie | le CRAC de l'ostéopathe remet la tête devant, puis elle continue : trois tours, la cravate lancée autour par un vent qui tourne avec la tête, traînées de vent, pause de cinq images au-delà du troisième tour, retour en ressort, yeux en spirale ; bloquée renversée vers le plafond, il finit présentateur météo sous la caméra du plafond | 53 |
| La mâchoire en bloc (cycle 19) | `face: {jaw: 1, jawLen: 0,7-0,75, jawBlock: 1}` : sous la bouche, le menton tombe d'un bloc jusque sous le col et l'écart devient une bouche ouverte sombre ; la langue sortie (`tongue: 0,8`) tombe avec le bloc ; à poser sur une prise étalée (regard, détour, trois images d'écrasement, prise, tenue 0,6 s) | 54 |
| La caméra embarquée dans la porte (cycle 19) | clé de caméra `ride: {prop}` sur un accessoire qui pivote (porte tournante, manège) : la caméra placée au milieu du compartiment qu'il regarde tourne avec lui ; il reste de face, impassible, la rue défile derrière lui ; à 2,4 tours/s la rue devient un tourbillon pendant qu'une carte reste collée sur son visage | 57 |
| Le sac qui tombe d'en haut | au virage de l'avion, le sac posé sur la valise derrière lui bascule et lui tombe sur la tête : il s'écrase large et court (1,6 × 0,5, tête comprise par `scl.head`), bras à plat au sol, tenu ; le sac glisse, il remonte au-delà de sa taille deux fois ; la caméra basse le voit de face | 54 |
| Le bras élastique vu de côté | filmé à angle droit de la ligne du bras, depuis le côté de ce bras : le bras court devant les jambes de l'épaule au couvercle, d'une seule épaisseur (`bend` fat 0,95 sur le bras et l'avant-bras), l'autre main en appui au sol derrière lui | 54 |
| La chaussette seule sur le tapis | au tapis à bagages vide, une chaussette rayée molle sort debout des lamelles et défile devant lui, impassible (`sockL` o.flop : le haut plie et oscille) | 54 |
| La gifle des lamelles | plié en deux, la tête passée entre les lamelles du tunnel (`pin` de la tête), il ressort ; une lamelle revient et lui écrase la tête sur sa propre hauteur (moitié), yeux croisés, tenue huit images | 54 |
| L'objet qui vit la vie du héros | la valise fait le tour du monde sans lui : selfie sous la tour Eiffel (flash), bronzage sur une serviette devant les pyramides (le couvercle soupire), orbite autour de la Terre, un autocollant par vol qui saute sur elle ; elle voyage en première avec une flûte qui se remplit pendant que lui voyage en soute | 54 |
| La carte qui passe au-dessus des doigts | la carte de fidélité tendue loin, le bras qui s'étire deux fois sa longueur ; la carte file en arc au-dessus de ses doigts jusqu'à l'étiquette de la valise ; le poing se ferme sur le vide deux images trop tard | 54 |
| Le débouchoir qui retombe sur le front | POP : le débouchoir sort de l'évier en tournant et retombe manche en premier sur son front (SCHLOUP) ; tête rejetée et écrasée, yeux sortis sur leurs tiges ; plan serré sur la coupe rouge plantée comme une corne, ses yeux louchent dessus | 55 |
| Le cou en chewing-gum | il tire le manche à deux mains : le cou s'étire 4,4 fois sa longueur (`bend.neck` stretch 4,4, fat 0,9), la tête droite face à nous, les coudes pliés et écartés (`hose` 0,3 + pôle de `touch`) encadrent le visage ; les mains glissent : elles partent en l'air, la tête revient au-delà de sa place, quatre oscillations | 55 |
| La pichenette au guichet | le bras de l'employée sort de son épaule, de son côté, en quatre images (`hose`), le doigt armé tenu trois images, la pichenette ; le manche vibre, sa tête frissonne avec (inclinaison du cou qui décroît), lui reste avachi | 55 |
| Le front collé au réverbère | en marchant, la coupe se colle au réverbère : `pin` du front sur le poteau, les jambes partent en l'air et se balancent de moins en moins (`lay` et jambes pliées) | 55 |
| Le pigeon dans la ventouse | un pigeon fonce droit dans la coupe et y reste collé : chaque battement d'ailes tire sa tête de côté, le corps suit en retard dans l'autre sens ; impassible | 55 |
| La poignée de métro humaine | suspendu au plafond de la rame par son débouchoir (`pin`), deux passagers tiennent ses mains comme des poignées ; au freinage, ils partent d'abord, lui plus loin que tout le monde ; POP : décollé, il reste huit images en l'air une main sous le pommeau, tombe, crêpe tenue, trois coups de pompe pour se regonfler | 55 |
| L'accessoire qui garde le poste | le débouchoir resté au plafond : une passagère s'y tient comme à une poignée en lisant son journal ; lui, au chômage, sur le banc du quai pendant que la rame s'en va | 55 |
| La bosse qui fait POC trois fois | après le BONG, la bosse sort du crâne en trois battements (`skullBump` o.grow), chacun plus gros, dépassant et retombant ; les yeux grands ouverts, pupilles visibles, remontent vers elle | 56 |
| Le médecin qui mesure à genoux sur la boule | la boule de peau de trois mètres sur sa tête, le médecin agenouillé au sommet déroule le mètre ruban à la main sur sa face avant ; lâché, le ruban remonte en six images, le crochet traîné de trois copies jaunes se colle à son nez (accessoire `tapeHook` sur la tête) : CLAC, mains au visage | 56 |
| La plaque qui écrase | la plaque COLLINE tombe sur le sommet : TCHAC, tout le bonhomme écrasé à 64 % de sa hauteur quatre images, puis rebond au-delà ; l'herbe descend du sommet | 56 |
| La colline sur la tête, vue en entier | caméra à hauteur de poitrine, assez loin pour le dôme entier avec du ciel des deux côtés : sentier, plaque, drapeau, randonneurs (`figH` 0,26), puis la station de ski enneigée et son télésiège | 56 |
| Le skieur qui hésite sur le bord | au bord du dôme au-dessus de sa tête, le skieur moulinette des bras et vacille (trois clés de roulis), puis plonge devant son visage ; la tête reste droite sous la colline, les yeux seuls suivent | 56 |
| La colline qui se dégonfle | PSCHHH : le dôme se dégonfle sur vingt images en ondulant ; le cou, libéré, jaillit à deux fois et demie sa longueur et revient ; un pansement sur le crâne | 56 |
| Les skieurs restés en l'air | plus de colline : les skieurs tiennent debout sur le vide là où était la pente, regardent en bas, l'un fait un petit signe, moulinent, puis tombent ; deux plantés tête la première dans la neige avec une bouffée blanche, le troisième assis sur sa tête écrasée (POF) | 56 |
| La facture sans fin | la note des forfaits se déroule de ses mains jusqu'à la neige et file vers l'objectif, ruban crème bordé de brun (`billScroll`), caméra haute qui avance lentement pendant qu'il cligne | 56 |

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
- (cycle 4) **Une image seule à la coupe** : une clé `dark=[[0, 1, 0.001]]` laissait la PREMIÈRE image du plan éclairée (la rampe partait de zéro à
  l'instant même de la clé) : un éclair d'une image à chaque coupe vers le noir, dans deux films, invisible sur les images fixes et pris pour « la
  dernière image du plan précédent » sur les bandes. Corrigé dans le moteur (une clé sans rampe vaut dès son image). **Contrôle à lancer sur chaque
  brouillon et sur le film final** : `python3 absurd-shorts/tools/cut_flash_check.py FILM.mp4 scripts-fr/story_x.json` (il compare la première image de
  chaque plan aux deux suivantes ; il signale aussi parfois un geste très rapide juste avant une coupe : regarder les images avant de conclure). Sur
  les bandes d'aperçu, la vignette 0.00 d'un plan doit montrer SON décor dans SON état.
- (cycle 4) Une réaction qui porte le gag (la dame qui voit la main monter à la cravate) doit avoir son VISAGE dans le cadre : au bord, il n'entrait
  que ses yeux sortis. `proj.py` sur la tête du personnage qui réagit, dans chaque cadre du plan, avant de rendre.
- (cycle 4) Un corps aplati d'avant en arrière ne se voit plat que de profil ou de trois quarts serré (64° et plus) : de face, c'est un personnage
  normal. Mettre en scène la minceur de côté, le regonflage en revenant vers la caméra.
- (cycle 4, 2e relecture de « La porte » : 7,4 / 7,5) **`bend` d'une pièce = [avant, côté, torsion, étirement, grosseur]** : un coup reçu de côté est le
  DEUXIÈME nombre ; écrit dans le troisième (une torsion), la tête tournait à peine et les relecteurs ont noté « coups reçus mollement ». Signe : un `côté`
  positif envoie le sommet de la tête vers SA droite. Toujours rendre une image à l'instant du coup avant de régler le reste (le premier sens était faux
  dans les deux plans). Un regard de côté « avec un peu la tête » est une torsion du cou (0,3), pas une flexion (elle penche la tête).
- (cycle 4) **Un personnage plaqué debout sur un mur se lit « debout à côté du mur »** : pour qu'on voie qu'il y a été jeté, une pose qu'on ne peut pas
  tenir debout (à l'horizontale, pendu par un bras, les pieds loin du sol), et une forme sombre sur un fond clair (fenêtre au clair de lune, bande pâle
  sur le mur). Ne rien pendre sous lui : une couverture qui tombait faisait un bloc sombre : il semblait couché sur un meuble.
- (cycle 4) **Dans une nuit graduée, les yeux qui restent allumés dans le noir se lisent ouverts** (un dormeur avait les blancs les plus clairs de
  l'image) : `darkEyes=False` sur l'acteur dans ces plans, et paupières fermées par le canal `lid`.
- (cycle 4) **Un take ne sert qu'une fois par film** (règle « jamais deux fois le même gag ») : le second doit changer de mécanique (yeux sur tiges, puis
  corps qui décolle + accessoire laissé en l'air + mâchoire dans la paume). Un accessoire attaché ne se détache pas : le cacher et montrer un jumeau libre.
- (cycle 4) Une barbe (ou tout accessoire du menton) ré-attachée sous une mâchoire descendue se pose EN AVANT du torse (z 0,14) : à la profondeur du
  visage (0,09) elle est à l'intérieur de la poitrine, et le personnage perd sa barbe pendant le take.
- (cycle 4) Un doigt pointé qui s'arrête loin du visage ne donne aucun coup : guider la main jusqu'au visage (`reach`), le bras traverse le cadre, et la
  tête répond à chaque contact, plus fort la seconde fois.
- (cycle 4) Texte porté par un membre (plaque sur une manche) : du côté de la caméra, d'équerre avec l'objectif, un tiers de la largeur du cadre, seul à
  l'image pendant 0,4 s avant qu'autre chose arrive, et rien d'autre dans la même zone (toile d'araignée ôtée pour ce plan).
- (cycle 4) Un métier se lit à trois signes : la coiffe (casque de chantier `hardhat2` : dôme, arête, visière devant seulement ; le casque à bord
  plat était un panama), un mot sur la poitrine (`chestPatch`), un outil en main. Un outil attaché à la main suit l'avant-bras et disparaît : le poser
  dans le monde, debout, là où va le poing guidé, et le faire apparaître quand la main y arrive.
- (cycle 4) **Poses debout** : `idleShift=1.8` dans `st.write` (au-dessus de 1 : vrai déhanché, poitrine tournée, tête en contrepoids) ; à 1 les
  relecteurs voyaient encore « des planches aux jambes parallèles ». Une révérence plie le dos (`bend spine 0.64`) et occupe la main libre (sur le ventre).
- (cycle 4) Un plan final de plus de 2 s en un seul cadre large, dans une série qui coupe toutes les 1 à 2 s : couper à un plan rapproché pour le geste
  qui porte la chute (la main posée sur l'avant-bras devant la porte claire), puis pousser lentement sur le dernier regard. Compter 2,4 s après la voix.
- (cycle 4) Avant qu'un bras tendu ne le ramène : cinq images immobiles, les yeux vers nous. La course sur place enchaînée directement sur le retour ne
  laissait pas le temps de comprendre. Et couper sur la pose tenue (l'affiche) plutôt que sur un demi-geste de 0,2 s après elle.
- (cycle 4, deuxième passe de la 40) **Un commentaire `//` glissé dans une fonction écrite sur une ligne avale la fin de la ligne** (trois fois déjà :
  accolades perdues, « missing ) after argument list »). Le commentaire va sur sa propre ligne, au-dessus ; `node --check` après chaque retouche du moteur.
- (cycle 4) **Une expression forte commence par un clignement automatique de 0,09 s** : posée sur un battement de quatre images dans le noir, elle donne
  quatre images noires. Garder l'expression en place et n'agir que par les canaux du visage (`eye`, `lid`, `gx`).
- (cycle 4) **Des pas rapides écrits par `to`** (0,24 m en 0,07 s, avec des hauteurs) nourrissent les couches automatiques du rig (traînée de la colonne,
  écrasement vertical) : le personnage se couche sur le côté. Un `glide` par pas, les plongeons en `sq` écrits à la main, et `auto: 0` dans ces clés.
- (cycle 4) **Dans le noir, un corps cache encore ce qui est derrière lui** (la passe de profondeur du monde solide) : des paires d'yeux placées « à ses
  pieds » avaient disparu. Reculer le personnage derrière elles et agrandir ses yeux d'autant.
- (cycle 4) **Les canaux du visage par côté : `L` est la GAUCHE DE L'IMAGE quand il nous fait face** (son œil droit, celui du haut), `R` la droite de
  l'image (son œil gauche, celui du bas). Pour un œil à l'oculaire, vérifier lequel est du côté de l'instrument.
- (cycle 4) **Les yeux peints sont de travers** (l'un 10 cm plus haut que l'autre) : deux têtes penchées l'une vers l'autre donnent une paire horizontale
  et une paire verticale, un tas de cœurs. Pour une paire horizontale dans le noir : pencher la tête de 30° (`bend neck [0, 0.52, 0, 1]`) ; ce penché
  emporte les yeux de 0,26 m vers la gauche de l'image : décaler le corps d'autant.
- (cycle 4) Un nuage juste derrière une tête se lit comme un chapeau, un nuage posé sur un rayon du soleil colle les deux : `parisStreet` accepte
  `clouds: 0` (ciel nu) ou `cloudSeed`.
- (cycle 4) **Un objet présenté à quelqu'un ne passe jamais devant le visage de celui qui le tient**, et un bras tendu derrière un personnage plus proche
  est perdu : le faire passer par-dessus (accusateur sur la pointe des pieds, main haute), ou baisser l'autre (à genoux).
- (cycle 4) Contenu de gag dans la bande des sous-titres (fenêtres d'une ville vue de haut, cadran d'un appareil tenu à la ceinture, tube d'un
  télescope) : le remonter entre 55 et 72 % de la hauteur, quitte à ajouter un premier plan fait pour (une maison en face, un appareil tenu à la poitrine).
- (cycle 4) Les rares lumières d'un plan noir doivent avoir leur logique : une allumette n'éclaire pas la rue (flaque `darkPool`), une bougie éclaire
  la main qui la tient, une torche se voit, un télescope a une lentille et le tube le plus large côté ciel.
- (méthode, demande de l'utilisateur) **Toujours lancer la génération complète** (3D 1080 × 1920 puis HyperFrames) dès que la dernière revue est demandée,
  sans attendre les rapports : la dernière passe se fait ensuite, et chaque version terminée est envoyée. Les relecteurs n'écrivent pas leur fichier de
  rapport : recopier leur message dans le dossier de revue. S'ils sont coupés par la limite d'usage, les relancer plus tard sur les mêmes pièces.
- (méthode) Un plan peut commencer avant ses mots : `st.plan([... ('S12', 15.0333, 0) ...])` (un temps absolu, multiple de 1/30 s) pour prendre des images
  au plan précédent ; le carton suit alors avec `st.card('S12', 'MOT', at=0.42)` (secondes dans le plan), sinon il tombe à la coupe, avant le mot.
- (cycle 5) **Un canal du visage ne peut que fermer une paupière** (`lid`, `lidL`, `lidR` prennent le maximum avec l'expression en place) : sur une
  expression aux yeux mi-clos (`unimpressed`, `smug`, `suspicious`), des yeux « qui louchent » ou « qui regardent en haut » restent deux fentes vides.
  Changer d'expression à la clé (une expression qui n'est pas forte, `worried` par exemple : pas de clignement automatique), puis régler les canaux.
- (cycle 5) **Une main guidée qui frappe une tête doit suivre l'écrasement de cette tête** : la cible calculée sur la tête au repos se retrouve 20 à 30 cm
  au-dessus du crâne à l'image de l'impact. Poser une seconde clé `reach` (même instant et même durée que l'écrasement) sur la position écrasée.
- (cycle 5) **Nettoyer un gros plan par la focale, pas par le décor** : même place de caméra, `lens=28` au lieu de 44 : le cadre ne garde que les 62 %
  du centre ; ce qui traînait aux bords (une main coupée, un rideau, un cadre) sort, le mot ou le visage grossit de 1,6 fois.
- (cycle 5) Une image fixe peut tomber sur un clignement ou sur une image de passage : avant de « corriger » des yeux fermés ou une pose molle, relire les
  clés autour de cet instant (ici : des « fentes » dans le noir qui étaient un clignement voulu).
- (cycle 5, méthode) **Un battement par plan de moins de 1,2 s** ; un accent tenu vaut six images au moins ; avant la mise en scène, écrire la **liste des
  mécaniques du film, une fois chacune** (deux takes à yeux sur tiges, deux sourires dans le noir, deux coups de doigt : relevés par les revues) ; **un mur nu
  derrière les têtes d'un plan à deux**, et un mot qui porte la chute occupe 30 % de la largeur ou a son gros plan.
- (cycle 5, méthode) **Une passe écrite pendant un rendu final est un correctif de texte** (`rep(ancien, nouveau)` avec `assert count == 1`) appliqué à
  une COPIE du script pour les images fixes, puis au vrai script seulement après la construction du projet HyperFrames de la version en cours :
  régénérer le script entre le rendu 3D et le projet désynchronise repères sonores, cartons et plans. Ne pas valider la copie dans le dépôt.
- (cycle 5, méthode) **Une seule génération complète à la fois** : deux rendus 1080p en parallèle doublent la durée de chacun ; les mettre en file
  (`queue2.sh A B`), et réserver le parallèle aux images fixes et aux brouillons.
- (cycle 5) **Cadre vertical et véhicules** : un bus de 7,6 m et un coureur côte à côte ne tiennent pas dans 25° de champ horizontal, et une vue rasante
  le long du flanc ne se lit pas comme un bus. Ce qui marche : le véhicule en fond d'un travelling de trois quarts face (la caméra recule devant le
  personnage, le flanc et la porte derrière lui), ou le véhicule qui rapetisse derrière lui (trois quarts avant : girouette et chauffeur visibles).
  Un trajet rapide se filme dans l'axe ou en travelling à sa vitesse ; en travers d'un cadre fixe il dure quatre images.
- (cycle 5) Un personnage assis au volant (`drive`) : régler la hauteur de l'acteur pour que sa tête reste sous le plafond (siège du bus : 0,3 m),
  et filmer à sa hauteur : vu d'en dessous, le bandeau du pare-brise coupe le haut du crâne dès qu'il s'étire.
- (cycle 5) **Un trait fin et vertical dans de grands yeux du noir** n'est pas une bavure de sprite : les cheveux et les oreilles, sur les côtés de la tête,
  passaient devant la peau des yeux agrandie (posée 12 mm devant le visage). Corrigé dans le moteur (45 mm). Pour chercher ce genre de défaut : sortir le
  canevas 2D seul (`node tools/glow_dump.mjs sortie.png 5.2`, dans `absurd-shorts`) ; s'il est propre, la cause est dans la scène 3D (quelque chose devant, un bord).
- (cycle 5) **Raccords aux coupes** : une marque portée par un personnage (bosse, étiquette, chapeau de travers) et la lumière d'un même lieu doivent être
  les mêmes des deux côtés d'une coupe ; relire les `face`, `look` et accessoires du plan d'avant en écrivant le suivant. Deux relevés de la troisième
  revue de l'histoire 40 : la bosse disparue une image avant la claque, le balcon qui change de couleur entre deux plans.
- (cycle 5) **Bord droit** : sur TikTok et Reels la colonne des boutons couvre la droite entre 45 et 65 % de la hauteur : rien d'essentiel à moins de 8 % du
  bord droit (un œil d'amoureux y était collé).
- (cycle 5) « Le doigt s'arrête à une main de l'interrupteur » : à l'écran l'écart doit faire 5 à 6 % de la largeur du cadre, sinon il semble déjà
  toucher ; grossir la main (`scl handL 1.7`) pendant la tenue.
- (cycle 5, méthode) Quand la génération complète est en file derrière un autre rendu et que les rapports arrivent avant son départ, la retenir le temps
  d'intégrer la dernière passe (un fichier témoin surveillé par la boucle d'attente), vingt minutes au plus : c'est plus court que de rendre une version
  dépassée puis de recoller des plages.
- (cycle 5) **Course vue de près** : l'écrasement automatique à chaque appui (clip `run`, rebond en |sinus|) tombe sur une image isolée, jamais la
  même (à 4,4 foulées par seconde : un appui toutes les 3,4 images) : le corps perd jusqu'à 24 % de sa hauteur pendant une image, la tête descend de
  40 cm et sort du cadre d'un gros plan, un panneau porté devient illisible. Mettre `'autoSq': 0.3` dans la base « toon » de la course (toutes ses
  clés) : il reste un rebond, plus de saccade. Une image fixe de contrôle peut tomber sur l'image écrasée : avant de recadrer, vérifier la pose.
- (cycle 5) **Un passant qui croise le héros se filme de face** : venu de derrière la caméra, il n'est qu'un bras au bord du cadre puis un dos qui
  s'éloigne, et le héros lui tourne le dos pour le suivre. Le faire arriver du fond, derrière le héros (on le voit venir, pas lui : ses yeux sont
  fermés), le faire passer à 50 cm de son épaule puis sortir à côté de la caméra ; cadre assez large au passage, puis avancée sur celui qui reste.
- (cycle 5) **Une file dans la profondeur** (un contrôleur et deux voyageurs derrière un coureur) : la caméra à hauteur du premier, sur le côté, le
  héros hors champ : le sujet du plan en grand au bord, les autres en diagonale vers le fond ; des tickets de 50 cm, pas de 34.
- (cycle 5) **Un personnage qui traverse tout le plan en courant ne démarre pas à la première image et ne s'arrête pas à la dernière** : sinon le
  moteur lui penche la colonne (traînée), lance les bras en pendule et change de cycle sur les deux ou trois images qui bordent chaque coupe : un
  « plongeon » à chaque raccord (vu sur les planches image par image : dernière vignette de chaque plan). Mettre `cruise=True` sur la clé de
  déplacement (`k(0.0, to=…, dur=D, clip='run', ease='linear', cruise=True)`) : avant la clé et après la fin, la position continue sur la même
  droite et le cycle garde la même horloge. Pour un trajet en deux tronçons, une seule clé `path=[…]` (deux clés relancent le cycle).
- (cycle 5) **Personne ne passe à moins d'un mètre de l'objectif** : un corps qui remplit le cadre pendant une image est un flash. Calculer le bord
  du champ (à la distance d, la demi-largeur vaut 0,227·d à la focale 44) et faire sortir le passant par le côté au moins 2 m avant la caméra ;
  caméra fixe pendant le passage, l'avancée ensuite (`glide`).
- (cycle 5) Une fin de plan vide (le héros est passé, il reste une demi-seconde) : y laisser une trace qui bouge (une plume du pigeon parti :
  accessoire `feather`, 40 cm pour être lue), pas un décor figé.
- (cycle 5, méthode) **Une tâche de fond est coupée à sa limite de durée** (30 min par défaut, 2 h au plus, l'attente dans une file comprise) : un
  rendu complet a été tué à 740 images sur 904. Lancer les rendus longs détachés (`nohup bash -c "…" > /dev/null 2>&1 &`) et les suivre par leur
  journal. Si un rendu est coupé : ses segments `out/work/story_<S>_render/seg_N.mp4` sans index se récupèrent avec
  `python3 tools/recover_mp4.py seg_N.mp4 <un segment terminé ou un ancien rendu de même format> seg_N.h264` (les images sont dans l'ordre : le
  segment N commence à l'image N × ceil(total / workers)) ; ré-encoder chaque flux récupéré (`ffmpeg -r 30 -i seg_N.h264 -c:v libx264 -crf 12
  -r 30 rec_N.mp4` : donné brut au filtre `concat`, il ressort avec 40 000 images), écarter les huit dernières images de chaque segment récupéré,
  rendre les plages manquantes avec `--range`, tout réunir en un seul encodage (filtre `concat`), vérifier le nombre d'images, puis la continuité
  de la luminance moyenne de part et d'autre de chaque raccord.
- (cycle 5) **La lumière d'un plan** (sonde de lumière rebondie, exposition automatique) est mesurée sur la première image rendue dans ce plan :
  une plage `--range` commencée au milieu d'un plan sortait plus sombre d'un diaphragme pendant deux images (l'enveloppe blanche emplissait le
  cadre au moment de la mesure). Corrigé dans le moteur : en entrant dans un plan par son milieu (plage, part d'un processus de rendu, image
  fixe), il mesure d'abord sur la première image du plan. Les images fixes de contrôle ont donc maintenant la lumière du film.
- (cycle 5) **Une route posée sur un champ** (un ruban de 500 m quelques millimètres au-dessus d'un sol de 9 km) se bat avec lui pour la profondeur :
  elle clignote dans le brouillon, disparaît en aspect final, ou n'apparaît qu'en partie même relevée de 5 cm avec un décalage de polygone. Ne pas
  compter sur le tampon de profondeur : dessiner le sol en premier (`renderOrder = -2`), puis peindre le ruban sans test de profondeur
  (`depthTest: false, depthWrite: false`, `renderOrder` entre -2 et 0), couche par couche ; ce qui est posé dessus se dessine ensuite normalement
  (accessoire `roadStrip`, décor `grassland`). Regarder le sol d'un plan large sur trois images espacées avant le brouillon.
- (cycle 5) Un déplacement en deux clés (`glide`) dont seule la première porte le clip : à la fin de la première, le personnage reprend la pose du clip
  de base (trois passagers « volants » redevenaient debout en plein vol). Répéter `clip=` et `params=` sur chaque clé du trajet.
- (cycle 5, méthode) Dans une boucle d'attente, `pgrep -f nom` lancé depuis `bash -c "… nom …"` se trouve lui-même (attente sans fin), et
  `pgrep -f "a\|b"` ne fait pas d'alternative (il n'a rien trouvé alors que le rendu tournait) : attendre une ligne dans un journal, ou deux
  appels séparés.
- (cycle 5, histoire 41) **Un geste de main pendant une course** (frapper une vitre, appuyer sur un bouton, poinçonner) ne se lit pas dans le cycle de
  course vu de profil ou de trois quarts : le corps cache le poing. Trois sorties : filmer de l'autre côté de la surface frappée (de l'intérieur du
  bus : le poing vient vers nous) ; un insert d'une demi-seconde sur l'objet ; un seul objet au bout d'un bras allongé, sur le ciel.
- (cycle 5, histoire 41) **Index pointé** : `tip` 0,15 dans `touch` / `reach` (0,1 est le bout d'une main ouverte : le poing recouvrait le bouton).
  Sur un insert de face, le bout du doigt attend à côté de la cible, du côté d'où vient l'avant-bras (6 à 8 cm), puis saute dessus ; une cible
  placée derrière la surface de l'objet fait disparaître la main dans le torse.
- (cycle 5, histoire 41) **Un outil dont l'orientation compte** (poinçon, pince), attaché à la main, suit l'avant-bras : tenu à l'envers, mâchoires le
  long de la manche, il mordait derrière le ticket. Le poser comme accessoire du monde : position et rotation calculées (une base : X = la
  normale du ticket tournée de 50° autour de l'outil pour que les deux mâchoires se voient, Y = le sens des mâchoires ; angles d'Euler XYZ →
  `rot[0]`, `ry` en degrés, `rot[2]`), et la main guidée sur son manche. Sur un groupe qui avance : clés en `ease='linear'` seulement (un amorti
  déforme aussi le déplacement commun), aux mêmes instants pour l'outil et pour la main.
- (cycle 5, histoire 41) **Pupilles** : à 576 px de large une pupille peinte fait 2 à 3 pixels. Option du film `pupil=0.5` ; un regard qui porte un
  temps fort : `pupilSize` de 1 à 1,5 ; une chute de pupilles : de 1,5 à -1,15, les grandes pupilles tenues six images avant la chute, dans un
  plan à elles (`lens 46`, les yeux au tiers haut, la bouche au-dessus de 75 % : sous les sous-titres la lèvre qui tremble est perdue).
- (cycle 5, histoire 41) **Une expression forte** (`surprisedHappy`, `surprised`, `scared`…) passe par un clignement d'environ trois images : la poser
  trois images avant le moment où elle doit se lire, et la donner comme expression de base du plan suivant si l'émotion continue (l'espoir tient
  la fin d'un plan et le début du suivant, puis meurt quand l'autre entre).
- (cycle 5, histoire 41) **Cravate d'un uniforme** : la tenue `mao` (préréglage `officiel`) n'a qu'une cravate rigide : ni vent ni canal `tie`.
  `clothTie=True` dans le cast pour une cravate en volume. Pendu la tête en bas : `tie [1.15, 1.3, 0.1]` la fait retomber sur le visage,
  `[1, 0, 0]` la rend au vent.
- (cycle 5, histoire 41) **Roue de jambes** (`legWheel`, les jambes rétrécies par `bend`) : de profil seulement. De trois quarts face c'est un disque
  gris et deux boîtes noires : garder les vraies jambes.
- (cycle 5, histoire 41) **Après un `glide`, le clip de base revient** (encore) : projeté au pied du poteau, il « courait sur place » à mi-hauteur.
  `then='stand'` sur le déplacement ; même piège pour une pose tenue (`then='flag'`).
- (cycle 5, histoire 41) **Passager en amorce** (par-dessus l'épaule) : coupé par le bord latéral, jamais par le haut du cadre (une tête sans front) ;
  à moins de 30 cm de la vitre, la caméra contre la paroi opposée ; il peut entrer dans le cadre à la fin (le freinage le projette) pour se
  retourner vers nous. Placé en entier dans le cadre, il cache le héros.
- (cycle 5, histoire 41) **Gag horizontal en cadre vertical** (un corps à l'horizontale et un poteau plié : 3,3 m de large) : le personnage ne dépasse
  pas 30 % de la hauteur. Se rapprocher dès que l'action redevient verticale : un `glide` de 0,22 s sur la pose tenue ; vérifier les pieds
  au-dessus de 76 % de la hauteur et la tête sous le bord au dépassement (étirement 1,15 et non 1,32).
- (cycle 5, histoire 41) `lens` est l'angle de champ vertical en degrés (44 = 44°) : hauteur du cadre à d mètres = 2 d tan(lens / 2), largeur = 9/16
  de la hauteur. Calculer où tombent une tête, des pieds, un texte avant de rendre l'image de contrôle.
- (cycle 5, histoire 41) **Texte dans le cadre** (carte tenue en main, afficheur sur une tête) : aucun mot coupé par le bord ; reculer la caméra de
  30 cm plutôt que de laisser « RRÊT DEMANDÉ ».
- (cycle 5, méthode) `flash_check.py` signale à tort un plan à deux caméras (large puis serré), et son « image 0 » d'un plan est la dernière du
  plan précédent (arrondi) : confirmer par `cut_flash_check.py` et par les images avant de corriger.
- (cycle 5, histoire 41) **Un personnage porté par un véhicule** (déplacement `glide` sans `face=`) se tourne dans le sens de la marche pendant les
  trois premières images : sur la première image du film la passagère pivotait devant le héros. Lui donner dès le départ l'orientation du trajet
  (`ry` = sens de la marche) ou `face=` sur le déplacement.
- (cycle 5, histoire 41) **Première image du film** (c'est aussi la vignette) : un regard (`look`) met quelques images à s'installer : le poser avant
  le début par une clé à temps négatif (`k(-0.4, look=…)`) pour que le visage soit tourné vers nous dès l'image 0. Rendre l'image 0 et la regarder
  avant le brouillon.
- (cycle 5, méthode) Tracer une valeur du moteur : la page ne remonte que `console.warn` et `console.error` (`[page] …` dans le journal du rendu) ;
  ajouter un `console.warn` temporaire sur une copie de sauvegarde du fichier, rendre trois images, restaurer le fichier aussitôt.
- (cycle 5, méthode) Deux rendus d'images fixes du même script se marchent dessus (chaque rendu vide `out/work/story_<nom>/stills`) : pendant qu'un
  lot tourne, tester sur une copie du JSON sous un autre nom, et la supprimer ensuite.
- (cycle 6, méthode) **Calculer le cadre avant de rendre** : `project(frm, look, lens, p)` et `st.where(sid, t, p)` (`scripts-fr/story_kit.py`) donnent
  où un point du monde tombe dans le cadre (x, y en fractions depuis le coin haut gauche, et la distance) ; `frame_size(lens, d)` la largeur et la
  hauteur du cadre à d mètres. Repères : sous-titres entre y 0,77 et 0,83 ; carte de titre d'une ligne entre 0,07 et 0,18 ; rien d'essentiel au-delà
  de x 0,92 entre y 0,45 et 0,65 ; une tête debout monte à 2,2 – 2,4 m (cheveux compris), un afficheur posé dessus à 2,6 m. Vérifier ainsi les
  pieds, le haut d'une tête, les deux bords d'un texte, puis seulement rendre l'image de contrôle. Ne pas relancer le script d'une histoire pour
  « tester le kit » pendant que sa génération complète tourne (il réécrit les repères lus au montage du projet).
- (cycle 6, 2e relecture de la 41 : 7,7 / 7,6) **Le sommet de l'histoire doit être le plan le plus grand et le plus clair, pas le plus petit** : l'arrêt
  au poteau était filmé de côté depuis l'autre trottoir (corps sombre de 8 % de la hauteur sur le bitume, visage caché par le poteau, pieds hors cadre)
  et répétait une pose déjà vue deux fois (à plat dans l'air, pieds devant). Refaire le sommet de près, bas, de trois quarts, le visage vers nous, les
  pieds dans le cadre, sur le fond le plus clair disponible (trottoir crème : 13,8:1 contre 3,4:1 sur la route), avec une pose que le film n'a pas servie.
- (cycle 6) **Un accessoire long pointé vers la caméra est un moignon** : le parapluie allait de la main de la dame au col du héros dans l'axe de vue
  (1,25 m devenu 30 px). Placer la caméra pour que la ligne main → cible soit en travers du cadre, et pour que le fond derrière cette ligne soit vide
  (la file d'attente derrière celle qui frappe, pas dans l'intervalle). Mesurer le cou ou le col avec `debugJoints` avant de poser la crosse : un cou
  étiré × 2 monte la tête à 2,05 m, la crosse réglée « au col » à 1,3 m finissait sous la taille.
- (cycle 6) **Un visage à la fois** : la passagère qui se penchait vers nous pendant qu'il était collé à la vitre couvrait la moitié de son visage
  (sa tête, plus près de la caméra, fait la moitié de la largeur). Lui pendant l'écrasement ; elle après son départ, dix images, les yeux grands ouverts.
- (cycle 6) **La hauteur libre d'un intérieur** : le plafond du bus est à 2,3 m, une tête debout sur son plancher à 2,22 m : une casquette qui saute, une
  passagère qui se redresse passent à travers et disparaissent (« pas d'yeux », « la casquette sort du cadre » étaient cela). `cityBus top: 2.65`. Avant
  un gag vertical dans un véhicule ou une pièce, comparer la hauteur du gag à celle du plafond.
- (cycle 6) Un grand changement de regard (`look`) emporte déjà un clignement automatique entre 0,05 et 0,3 s après la clé : un clignement dessiné
  dans cette fenêtre donne huit images d'yeux fermés. Pour « des yeux ouverts sur nous dix images » : la clé `look` dès le début, rien d'autre avant 0,35 s.
- (cycle 6) **L'élan gardé en mémoire** : la suite du mouvement (`follow`) se souvient 0,75 s des accélérations ; après un retour en arrière violent
  dessiné à la main, les bras et la cravate ressortaient une demi-seconde plus tard, quand une clé sans `auto: 0` rallumait les couches automatiques
  (un bras tendu et le buste renversé sans raison, trois images avant la coupe). Le moteur pèse désormais chaque accélération par l'`auto` de sa clé :
  mettre `auto: 0` sur TOUTES les clés d'un mouvement chorégraphié (le vol compris), et la mémoire reste vide.
- (cycle 6) Le rebond de la course vu de près : `bounce`, `sq` (écrasement à chaque appui) et `autoSq` s'additionnent ; mesurer le trajet de la tête sur
  huit images consécutives avec `debugJoints` (colonne y). Cible 3 à 4 % de la hauteur du cadre : `bounce 0.9`, pas de `sq`, `autoSq 0` (8 à 9 %
  avec les trois ; 1 % avec `bounce 0.3` seul : figé). Un insert sur la poitrine : `bounce 0.06`.
- (cycle 6) `heelBrake` vu de côté : les talons pendent à 0,4 m de la route (jambes à l'horizontale) alors que la fumée et les traces sont au sol :
  `params={'drop': 0.4}`. À 14 m/s la cravate passe par-dessus la tête et se lit comme détachée du col : un vent arrière partiel dans le plan
  (`fx wind` de 9 m/s dans le sens de la course) la laisse décollée du torse sans la perdre.
- (cycle 6) L'écart entre deux objets dans le cadre (l'afficheur sur sa tête et le boîtier du feu) dépend de la POSITION de la caméra, pas de sa
  visée : tourner la caméra déplace les deux ensemble. Pour l'ouvrir : décaler la caméra de côté, ou éloigner le personnage du poteau (0,2 m de plus
  suffit dans tous les plans). Deux objets de même teinte qui se touchent se lisent comme un seul : changer la teinte de l'un (poteau gris galvanisé,
  boîtier vert sombre, cadre clair autour de l'afficheur) ET garder un intervalle d'au moins 7 % de la largeur.
- (cycle 6, méthode) Sens de la visée : pour une caméra qui regarde vers +Z, +X est à GAUCHE de l'image. Avant d'itérer sur une cible de caméra,
  projeter un point avec `project()` pour deux cibles et lire de quel côté il part (deux corrections sont parties dans le mauvais sens).
- (cycle 6, méthode) **`debugJoints`** : clé du script (`debugJoints: 'mec'` ou une liste, à mettre dans une copie du JSON) : à chaque image rendue
  le journal donne la position dans le monde et dans le cadre (fractions) de la tête, du cou, des mains et des pieds. Avec `project()`, on règle un
  cadrage ou l'emplacement d'un accessoire en un rendu au lieu de quatre. `axes_euler(X, Y, Z)` (kit) donne la rotation d'un accessoire tenu dans
  l'espace à partir de ses trois axes (un manche pointé d'une main vers un cou, sa crosse à plat).
- (cycle 6) Une larme peinte (`tear`) fait 2 % de la largeur : en très gros plan, prendre `drop` (dessinée, de la taille de l'œil, elle roule). De la
  vapeur blanche sur un mur clair mesure 1,1:1 : `steamInk`. Des arbres derrière une tête ou un feu : étendre `clear` du décor à la zone du plan.
- (cycle 6) **Un déplacement sans `then=` rend le clip d'avant** à la fin du déplacement : l'ombre qui se levait (`to=..., clip='stand'`) se recouchait
  (`lieBack`) à l'arrivée. Toute clé `to=` qui change d'attitude porte `then=` (assis, debout).
- (cycle 6) **Un demi-tour par une seule clé `face`** prend le chemin le plus court avec une sortie rapide : dos puis face en deux images, et du mauvais
  côté si le regard venait de partir de l'autre. Deux clés `face` avec `turn`, en passant par la direction du regard.
- (cycle 6) **Silhouette : un bras devant le corps est noir sur noir.** Le geste se joue en contour (bras écartés, mains sur les hanches) ou avec un
  accessoire blanc (le cadran de la montre). De même une ombre debout devant un personnage à plat le cache : la poser à ses pieds, lui en diagonale.
- (cycle 6) **Ne pas changer un signal pendant un mouvement de caméra** (le feu passait au vert pendant l'avancée : la dernière idée du film tenait en
  quinze images sur un cadre qui bougeait). Finir le mouvement, trois images, puis le changement ; huit images pour le regard, douze pour le retour.
- (cycle 6) L'expression `relieved` a les yeux fermés : pour un regard final vers nous, `neutral` avec `mouth: 'smirk'`.
- (cycle 6) Signe de `gx` : négatif = vers SA droite. Un feu à sa droite (à gauche de l'image quand il nous fait face) demande `gx` négatif ; l'inverse
  le faisait regarder à l'opposé du feu pendant trois versions. Vérifier sur une image avec le feu dans le cadre.
- (cycle 6) La vapeur en ronds blancs de taille croissante se lit comme une bulle de pensée : bouffées à lobes, en jet depuis l'oreille, qui
  s'amincissent en montant. Un panneau tenu en l'air à côté d'un poteau se lit comme un panneau fixé au poteau : le poteau hors du cadre, le
  panneau plus clair que le mur (`lapBoard bright`), et il retombe dans le cadre, à plat, lisible.
- (cycle 6) Les mains au sommet d'un geste (les deux poings levés du maire) montent dans le bandeau : vérifier l'image du sommet contre toute
  inscription placée au-dessus ; écarter les coudes pour que le visage reste visible entre les bras.
- (cycle 6) Le champ horizontal d'un cadre vertical est étroit (26° à la focale 44) : un trajet de 3,5 m en travers ne tient pas à 5 m. Le mettre
  sur la diagonale du cadre (caméra en avant et au-dessus, le trajet part vers le fond), ou le raccourcir ; l'extrême doit rester dans le cadre.
- (cycle 6) Lancer un geste depuis la moitié libre du cadre : il s'élançait vers la vitre derrière la passagère du premier plan. Il prend d'abord
  0,3 m d'avance (moitié gauche), se ramasse trois images, puis saute vers le milieu ; elle ne se penche que trois images après le freinage.
- (cycle 7) Un personnage-ombre fait d'un modèle teinté n'est pas un aplat : le rig du visage écrivait sa texture dans le matériau partagé
  (visage, cravate, barbe imprimés sur les bras et les jambes). Corrigé dans le moteur : un acteur `silhouette` garde un matériau uni et son
  visage n'est que la couche des yeux. Vérifier un aplat sur un agrandissement, pas sur une vignette.
- (cycle 7) Une ombre de la même valeur que le costume du héros se confond avec lui dès qu'ils se touchent : choisir sa teinte à l'écran (rendre
  quatre candidates sur la même image et mesurer) pour qu'elle soit à mi-chemin entre le costume et le mur.
- (cycle 7) La coque d'encre de la tête, passée dans le matériau de l'ombre, cachait les yeux dès que l'ombre n'était plus aplatie (elle est
  12 mm devant le visage) : elle est masquée sans liseré, vue de l'intérieur avec.
- (cycle 7) Le transfert de poids automatique (`idleShift`) décale le bassin de 7 cm de côté : un personnage aplati en travers des épaules
  entrait dans son mur et disparaissait dès qu'il s'arrêtait face à +Z. Le moteur ne l'applique plus aux acteurs aplatis en x.
- (cycle 7) Un accessoire attaché à un porteur aplati était divisé par son échelle x (0,03) : une montre de deux mètres. Le moteur prend
  l'échelle médiane du porteur.
- (cycle 7) Étirer les jambes ne relève pas les hanches (l'étirement part de la hanche vers le bas) : sans décalage de y les pieds sont sous
  le trottoir. Jambes 1,9 fois : y = +0,86 m.
- (cycle 7) Vu de la chaussée, un geste vers le mur part vers le fond de l'image : un doigt pointé sur le mur se lit comme un poing près du
  menton. Jouer le geste le long du mur, ou faire entrer le bras depuis le hors-champ.
- (cycle 7) De dos et de haut, un corps debout cache le sol devant ses pieds jusqu'à l'endroit où la ligne de visée qui passe au-dessus de
  sa tête touche le sol (cinq mètres pour une caméra à 4,4 m) : ce qui sort devant lui est invisible. Décaler la caméra sur le côté.
- (cycle 7) Une vue du dessus pas assez verticale montre celui qui est debout comme une masse posée sur celui qui est couché : faire passer
  le bas du cadre par ses talons et garder l'inclinaison sous la moitié du champ vertical.
- (cycle 7) Un homme de la série mesure 2,2 m au sommet de la mèche (2,45 m vu de la chaussée, à hauteur du mur) : une inscription sur le
  mur à 2 m est cachée par qui passe. La mettre entre 2,45 m et le bandeau, ou relever la caméra.
- (cycle 7) Un cadran blanc sur un mur clair ou sur une bande blanche ne se voit pas : lui donner un liseré dans la teinte de l'ombre.
- (cycle 7) `fit()` visait le milieu du cadre : avec une bande de sous-titres à dégager, le quart haut de l'image restait vide et la focale
  s'ouvrait trop. Il vise maintenant le milieu de la fenêtre autorisée ; donner les points extrêmes (bras levés, objet tenu) et non le corps
  entier quand le sujet est un visage.
- (cycle 7) Une chose plate couchée en l'air est vue par la tranche depuis une caméra à sa hauteur : la mettre debout, son plat vers la
  caméra, pour le temps suspendu.
- (cycle 7) Le clip du marteau du juge lève le bras derrière la tête : de face rien ne monte. Guider le poing (`reach`) à côté de la
  perruque, du côté du bloc, pendant l'élan ; poing sur le manche après le coup.
- (cycle 7) Une ligne qui part de la nuque d'un personnage et file droit derrière lui est cachée par sa tête depuis une caméra en face :
  placer le personnage sur le côté de l'endroit où va la ligne, pour qu'elle traverse le cadre à côté de sa tête (la cravate prise dans la
  porte : le héros un pas devant la porte et 1,3 m à sa droite).
- (cycle 7) Une caméra au-delà d'un mur du décor voit l'envers du mur : des images entièrement unies. Garder la caméra dans la pièce, ou
  monter l'objectif (60) au lieu de reculer.
- (cycle 7) `fit()` moyennait les relèvements sans tenir compte du passage par ±180° : une caméra qui regarde vers −Z visait derrière elle et
  rien n'entrait dans le cadre. Corrigé dans le kit (relèvements pris autour de celui du centre des points).
- (cycle 7) Une ombre (cast `silhouette`) est retirée du tampon d'occlusion ambiante : debout devant des objets, leur occlusion s'imprimait
  sur son corps (le potelet, le lit « à travers » elle : elle semblait transparente). `silhouetteAO: true` pour une ombre qui se tient dans une
  pièce ou sur un trottoir ; la laisser hors du tampon quand elle est plate sur un mur (sinon un halo sombre entoure sa silhouette).
- (cycle 7) Il n'y a pas d'effet `sfx:ding` : la cloche (`sfx:bell`) pour un ascenseur, la sonnerie (`sfx:ring`) pour un réveil. Vérifier les
  noms dans `tools/audio3.py`.
- (cycle 7) Une feuille accrochée à une main se présente par la tranche : la poser libre devant la poitrine, face caméra (`ry` vers la
  caméra), les mains guidées sur ses bords.
- (cycle 7) Les feuilles déjà épinglées d'un panneau d'affichage du décor recouvrent une feuille posée à la même profondeur : décaler la
  feuille de l'histoire de 2 à 3 cm vers la caméra.
- (cycle 7) Le clip `pokeUp` lève les deux bras : il se lit comme une acclamation. Pour un index levé : `stand` + `reach` d'une main au-dessus
  de l'épaule + `hands` `point`.
- (cycle 7) Un pas de course sur place (`scramble`) ou un clip « one-shot » donné comme clip de base est fini avant le début du plan :
  le poser par une clé `k(0.0, clip=..., params=...)`.
- (cycle 7) Un corps aplati couché (`sq` 0,1 dans sa profondeur, qui est verticale quand il est couché) aplatit aussi ses propres plis : une
  bosse qui soulève talons, hanches et tête reste invisible. Gonfler son épaisseur au passage de la bosse (`sq` z jusqu'à 0,7) ; et la
  filmer de trois quarts d'en haut : vu au ras du sol il n'est qu'un trait, vu d'aplomb il semble debout contre un mur.
- (cycle 7) Le bus `cityBus` est construit le long de X : pour rouler le long de la rue (Z), `ry=-90` (vers +Z) ou `90` (vers -Z). Avec
  `ry=0` il traversait la rue en travers, sortait du cadre en quatre images et ne figurait sur aucune image de contrôle.
- (cycle 7) Un accessoire tenu en main se présente souvent par la tranche (loupe, feuille, carte) : le poser libre, orienté par calcul vers la
  caméra, et guider la main dessus ; s'il est hors de portée, la main guidée étire le bras (c'est un gag de plus).
- (cycle 7, histoire 45) « no lens fits » : `fitBack(frm, points, ...)` du kit recule la caméra le long de la ligne centre des points ->
  caméra jusqu'à ce qu'une focale tienne tout, et imprime la distance ; la reporter dans le script quand elle dépasse un ou deux pas.
- (cycle 7, histoire 45) Le moteur n'avait pas de klaxon : `sfx:honk`, `sfx:honkLong`, `sfx:honkTiny` (deux notes carrées nasales à une
  tierce mineure) ont été ajoutés à `tools/audio3.py`.
- (cycle 7) Le clip `phoneEar` laisse la main du rig cartoon à l'épaule (sur la laisse, elle semblait la tenir) : guider la main jusqu'à
  l'oreille (`reach`, ajouté à toutes les clés du plan) et donner au téléphone une coque vive (`smartPhone` `case`) : une coque sombre sur un
  costume marine ne se voit pas.
- (cycle 7) Une feuille (`paperSheet`) est imprimée des deux côtés : vue de dos (contrechamp derrière une vitre), son texte apparaît en
  miroir. La retirer du contrechamp.
- (cycle 7) Les façades de `parisStreet` sont vers x = 10,2 : des pièces derrière un mur placé à 10,1 étaient dans les maisons (on voyait la
  façade peinte par les fenêtres, et aucun voisin). Mettre le mur de façade à 8,6 au plus.
- (cycle 7) Une caméra reculée sans limite sort de la pièce et filme le dos d'un mur (image unie) : `fitBack(..., inside=(x0, x1, y0, y1,
  z0, z1))` ; une caméra basse peut aussi se retrouver dans une voiture garée : vérifier les emprises des accessoires devant elle.
- (cycle 7) `cd dossier && A; nohup B &` : B part de l'ancien dossier (rendu en échec immédiat) ; mettre le `cd` dans chaque commande.
- (cycle 7) Quatre rendus à la fois : un navigateur s'est fermé à 540/877 images ; trois au plus.
- (cycle 8) Un accessoire attaché (`on={...}`) ignore son `ry` : l'orientation se donne dans l'attache (`'rot': [...]`). Le pigeon de 44,
  attaché sans `rot`, regardait la caméra (une boule grise) ; posé à 0,34 au lieu de 0,5 (la hauteur de la tête), il était à moitié dans le crâne.
- (cycle 8) Un accessoire qui tombe (clés `to` à t0) rejoue sa chute à chaque plan qui le reprend avec les mêmes temps : un état « posé » sans
  clés (`None`) pour les plans suivants (les grilles de 44 retombaient à chaque coupe).
- (cycle 8) `look={'exposure': 1.0}` coupe l'exposition automatique (base 1,32 en intérieur) : la salle de réunion de 43 était brune. Pour
  éclaircir, `fill`, et laisser l'exposition automatique.
- (cycle 8) Une corde `tieRope` en 48 segments fait avancer une frontière de couleur par bonds de 11 % du cadre : `n: 280`.
- (cycle 8) La cloison pleine d'`immeubleCoupe` : la tête d'une voisine qui se penche dans la cage la traversait ; `doorZ: [z0, z1]` ouvre une
  porte palière à chaque étage.
- (cycle 8) L'écharpe tricolore par défaut (`sashW` 0,055) fait 2 cm par bande : invisible ; `sashW: 0.15`.
- (cycle 8) Pour qu'un personnage qui en regarde un autre montre son visage, la caméra et celui qu'il regarde doivent être du même côté de lui
  (angle caméra-lui-cible sous 70°) ; sinon, finir sur un regard caméra (le préfet de 44 S05).
- (cycle 8) Un visage couché, filmé du côté du sommet de sa tête, est à l'envers (45 S21 : « une tuile ») : filmer du côté des pieds ou d'au-dessus.
- (cycle 8) Une main `point` vue de dos, un doigt levé, peut passer pour un doigt d'honneur (43 S09) : main ouverte (`spread`).
- (cycle 8) Deux sangles dans un même plan, vues de profil, font une seule tige : il « pend par la tête » (44 S15) ou ce sont des antennes
  (45 S18) ; crochet bien au-dessus de la tête, sangles sous les bras, ou quatre brins (`craneHook slingD`).
- (cycle 8) Les accessoires de 46 : `speedCamera`, `speedDisplay`, `licensePlate`, `zoneSign`, `speedGauge`, `carLift`, `brakeRollers`,
  `burstWall`, `garageBay`, `wheelChock` (props_radar.js) ; et `burstLines` (traits de choc autour d'un son, props_statue.js).
- (cycle 8) Un commentaire `#` au milieu d'un dictionnaire sur plusieurs lignes avale la suite de la ligne sans erreur : l'avis de 43 a perdu
  CONVOCATION et ASSEMBLÉE GÉNÉRALE, la jauge de 46 sa variable. Commentaire sur sa propre ligne ; contrôle : chercher dans les commentaires
  (module `tokenize`) des motifs `'clé':`, `k(` ou `P('`.
- (cycle 8) Sur des yeux sortis (`pop`), la pupille est au bout de la tige, tournée vers où il regarde : filmés de dos, ce sont des boules
  blanches (43 S16) ; `eyeYaw` ≈ ±(π − l'angle tige-caméra) les retourne vers nous, `eyePitch` les fait descendre.
- (cycle 8) Un déplacement (`to`) sans `face=` tourne le personnage dans le sens de la marche, même en `glide` : le ballon de 45 montrait
  sa nuque. Donner `face=` pour qu'il reste face caméra.
- (cycle 8) Une clé de toon de premier niveau inconnue (`'tremble'` hors de `face`) : le corps étiré de 45 S04 est revenu au repos au milieu
  de la tenue (cause probable). `tremble` va dans `face` ; le frisson du corps, en clés alternées.
- (cycle 8) Des paupières en planche plus grandes que le phare font du ruban adhésif sur les yeux : calotte dans le cercle, bord courbe avec
  un trait de cils (`carToon`, passe 3 de 45) ; fermée, il reste un arc de cils en bas.
- (cycle 8) Un essuie-glace tendu en ligne droite jusqu'au clavier se lit comme un câble de recharge : coude, lame au bout, un vide clair
  avant la cible, et un insert.
- (cycle 8) Les voitures de la bibliothèque (`car`) ont une cabine presque transparente (`glass` 0,07) : de loin, des cages ouvertes ;
  `'glass': 0.82` pour des voitures garées fermées.
- (cycle 8) Une grosse goutte de sueur doit faire trois fois sa taille pour se lire sur un téléphone : clé `fx={'sweat': 1, 'sweatSize': 3}`.
- (cycle 8) Trois rendus sur quatre processeurs : le rendu final 1080p tombe à 0,1 image/s (2 h 30 pour 30 s). Le final avec au plus un
  brouillon à côté ; les images de contrôle attendent.
- (cycle 9) Une géométrie faite à la main sans normales sous un matériau éclairé donne des NaN, et le bloom les étale sur toute l'image :
  images noires (les paupières de la voiture de 45, à chaque clignement). Toujours `setAttribute('normal', ...)`.
- (cycle 9) Un étirement de jambe (`bend` stretch sur legL/shinL) pousse le pied sous le sol : relever la racine de 0,956 m par unité
  d'étirement des deux segments (jambes × 1,8 : + 0,76 m), sinon le corps garde sa taille (45 S04, 45 S08).
- (cycle 9) En look naturel le grade vaut `none`, et `none saturate(...)` n'est pas un filtre valide : le gel « photo du radar » de 46
  restait en couleurs. Corrigé dans director3 ; `freeze: {at, filter}` choisit l'aspect du gel.
- (cycle 9) `face='keep'` sur un déplacement (`to`) garde l'orientation du corps ; l'audit de `st.write()` signale les glissés sans `face=`
  qui le tournent de plus de 45°, les têtes coupées, les pieds dans la bande des sous-titres et le héros de dos.
- (cycle 9) `beat(t, EXTRÊME, hold=0.3)` (story_kit) écrit l'anticipation, l'extrême, la tenue frissonnante, le dépassement et le retour ;
  le canal toon `hose` (0,1 à 0,3) garde un coude aux bras guidés qui vont loin (cinq bras tendus en tige raide : « le même bâton »).
- (cycle 9) Le bus de la bibliothèque (`cityBus`) a ses portes sur son flanc droit ; dans notre rue il roule sur la voie de droite vers +Z, portes vers la chaussée : vu du trottoir, « les portes se ferment devant lui » ne se voit pas. `doorSide: 'left'` (corps en miroir, afficheurs retournés pour rester lisibles).
- (cycle 9) Un outil attaché à la main (`on: {hand}`) se couche le long de l'avant-bras : le feutre agrandi de 46 S08 faisait une bande jaune sur la manche et la main visait la nuque. `rot: [π, 0, 0]` dans `on` pour qu'il dépasse des doigts, et la cible de la main reculée de la longueur de l'outil.
- (cycle 9) Un accessoire de la couleur d'un élément du costume disparaît : la tasse sarcelle de 46 se lisait comme une manchette à côté des revers sarcelle. Blanc ou une couleur absente du personnage.
- (cycle 9) Un gel pris à l'instant de l'éclair fige aussi le halo du flash (un disque blanc sur le radar) : geler 0,1 s après.
- (cycle 9) Un personnage secondaire entre la caméra et le gag le cache (le mécanicien devant la jambe en caoutchouc de 46 S10) : la caméra passe du côté où il ne couvre rien, et son geste vers nous se fait avec la main éloignée.
- (cycle 9) Un commentaire collé au milieu d'un appel avale aussi des arguments nommés sans erreur de syntaxe : au plan 13 de 45, `# ... gaze=[[...]], lids=[[...]],` avait effacé le regard et les paupières (les deux relecteurs ont vu des yeux « ronds et calmes » sur le gag principal). `lint_comments.py` repère maintenant `nom=[[` et `nom={'` dans un commentaire ; le lancer après chaque passe. Même piège dans un correctif du moteur : un commentaire inséré avant la fin d'une ligne JS avale la suite (`node --check` l'attrape).
- (cycle 9) Une clé `touch` juste après une clé `reach` fait retomber la main au début de la transition (le toucher remplace la portée avec son poids qui monte de 0) : la main de 47 S01 tombait au lieu d'aller à la bouche. Garder le même repère d'une clé à l'autre (`touch` 'face' → `touch` 'face').
- (cycle 9) Des couverts à taille réelle ne se voient pas en plan large sur un téléphone : taille cartoon (×2,2), et les épaules du personnage dans les points de cadrage (son centre seul laissait la moitié du corps hors champ).
- (cycle 9) Un mouvement dans l'axe de la caméra ne se lit pas : les lampadaires qui s'inclinent vers lui, filmés de côté, s'inclinaient dans la profondeur ; filmés dans l'axe de la rue, ils saluent.
- (cycle 9) Des passants vus de dos cachent ce qu'ils tiennent : la rangée face à la caméra, le héros qui passe derrière eux (plus grand, on le voit entre eux), et l'aiguille qui le suit (`compass path`). Une caméra « par-dessus l'épaule » collée derrière la tête cadre le crâne : la monter et la décaler jusqu'à voir l'objet en grand.
- (cycle 10) Un personnage secondaire entre la caméra et le héros cache le gag sans que rien ne le signale : l'audit de `st.write()` le dit maintenant (« X stands in front of mec and covers N % of him », boîtes projetées aux temps de chaque axe ; il a retrouvé l'agent qui couvrait 81 % du ballon de 45). C'est une question à vérifier sur une image : un héros qui passe derrière une rangée exprès (47 S08) le déclenche aussi.
- (cycle 10) Les personnages secondaires qui restent figés pendant le gag (« l'agent garde la même pose pendant le clac et le saut ») : `react(t, s, keep=..., look=...)` (story_kit) donne leurs clés de réaction (sursaut : écrasement deux images, épaules qui sautent, yeux qui sortent, cheveux dressés, frisson, retour ; `kind='wince'` : yeux fermés, épaules montées). `keep` porte l'état toon qu'il tient déjà (une main guidée), sinon elle tombe.
- (cycle 10) Des poses tenues raides et symétriques entre les gags : `idleShift` au-dessus de 1 (1,6) donne un vrai contrapposto (poids sur une jambe, buste tourné à l'opposé, tête qui revient, bras libre écarté) ; 1 ne fait qu'un léger balancement qu'un plan d'une seconde ne montre pas. Les mouvements de bras guidés (`reach`, `touch`) n'ont pas de traînée automatique (le smear ne lit que les poses des clips) : pour un bras qui part très vite, une clé intermédiaire étirée (`hose`, bras plus long) sur une image.
- (cycle 10) Un effet sonore au nom inconnu du mixeur ne casse rien avant la toute fin : la génération finale de 45 a échoué après deux heures de rendu 1080p sur `st.cue('splat', ...)` (sans `sfx:`). `st.write()` signale maintenant tout effet que le mixeur ne sait pas jouer (intégrés : thunder, thud, clack, clang, pop, rain, whoosh, gust, engine ; les autres en `sfx:<nom>`). Si la couche 3D finale est déjà rendue, `s7/hf_only.sh HISTOIRE NUM "Titre"` refait seulement le projet et le rendu HyperFrames.
- (passe finale 46) Un commentaire mis après `bottom=0.7,` avalait `inside=(...))])` jusqu'au bout de la ligne : `lint_comments.py` signale maintenant `drift=(`, `inside=(`, `lenses=` et `))])` dans un commentaire. Même piège en JS (`node --check` le voit) : un commentaire toujours sur sa propre ligne ou en toute fin.
- (passe finale 46) Une feuille tenue avec `face: 'camera'` et un décalage vertical dans le repère de la main monte au-dessus de la tête quand le bras se lève (le repère de la main tourne avec l'avant-bras) : décalage nul, la main placée là où doit être la feuille. Un gobelet tenu se couche le long de l'avant-bras et se lit comme un poignet rayé : `face: 'camera', faceFlat: True` le garde debout, face à nous.
- (passe finale 46) Le climax filmé de côté tombait au bord du cadre et le trou « avec du jour » était crème sur crème (contraste 1,05:1) : filmer dans l'axe du vol pour mettre l'impact et le trou au centre ; un bleu ciel saturé, un bord brique épais, des débris couleur brique.
- (cycle 9) Une scène profonde dans un cadre vertical (une porte au fond, un escalier devant) réduit ses personnages en miettes vue de côté : la filmer de haut dans l'axe de la profondeur, qui monte alors dans le cadre. Un battant ouvert vers la caméra cache celui qui sort : filmer du côté opposé aux gonds.
- (cycle 9) Un héros debout derrière une rambarde disparaît en contre-plongée : l'accouder à la rambarde (dos penché, mains dessus). Un plan qui doit tenir des randonneurs au sol et une fenêtre au troisième étage en fait des points : deux temps, les randonneurs puis une grue jusqu'à la fenêtre.
- (cycle 10) Un accessoire attaché garde sa taille quand le personnage rétrécit (`placeAttached` divise par l'échelle du porteur) : à mi-taille, l'étiquette du front lui couvrait les deux yeux ; réduire de moitié les accessoires portés et les remonter.
- (cycle 10) Une porte ouverte à la fin d'un plan doit l'être dès la première image du suivant : `open: 1`, pas `openAt: 0` (elle se refermait puis se rouvrait à travers sa mère).
- (cycle 10) Des rayons de blocs colorés aléatoires se lisent comme des bibliothèques : `grocerShelf` (rangées de produits identiques en facings, bandes de prix, étiquettes promo jaunes) pour le supermarché français (`fr: True`). Un sous-vide en une seule boîte qui rétrécit se lit comme une vitrine : `vacuumBag parts` colle le film partie par partie.
- (cycle 10) Des réactions clés filmées de dos ou de profil ne passent pas (le scan, la colère, les yeux qui louchent) : chaque réaction du héros de face ou de trois quarts, en plan moyen ; un contrechamp par-dessus l'épaule de celui qui agit (le laser du gérant) garde les deux.
- (cycles 9 à 11) Deux modules d'accessoires qui définissent le même nom : le dernier remplace l'autre en silence dans la table fusionnée (le tampon de la 49 changeait celui des anciennes histoires ; `ringMark`, `speedDisplay` de même). Nommer chaque nouvel accessoire de façon unique et passer `prop_collisions.py` après chaque ajout.
- (cycle 9) Un accessoire attaché qui se dessine selon sa propre orientation (l'aiguille d'une boussole) était calculé avant d'être tourné vers la caméra : il pointait n'importe où (aiguilles rouges vers le bas). `userData.afterFace` le recalcule une fois tourné.
- (cycle 11) Un personnage aplati (`sq` z 0.05) ne peut pas tendre le bras vers l'avant : l'écrasement le plaque dans son plan. Le tourner pour que le geste soit dans son plan (face à la caméra, le bras vers le côté).
- (cycle 11) Une tête de boîte vue de profil n'a pas de visage (le visage peint n'est que devant) : elle se lit comme une nuque. Trois quarts au moins.
- (cycle 10) Une caméra au-dessus d'un homme couché, au-delà de sa tête, montre son visage à l'envers ; au-dessus de sa poitrine, tournée vers son visage, il est droit.
- (cycle 10) Un écran tourné vers la caméra (`face: 'camera'`) tout près d'elle mange le cadre : petit, un peu en retrait.
- (cycles 9 à 11) Un commentaire qui finit par une virgule a avalé la virgule du code qu'on venait de remplacer (le texte remplacé s'arrêtait avant elle) : `lint_comments.py` le signale.
- (cycle 11) Des copies en gris sous la lumière chaude du look naturel se lisent sépia : `monoTint` froid et `monoContrast` pour la copie en 3D (son visage peint était délavé), `cool` sur les copies dessinées.
- (cycle 10) Un battant de porte ouvert vers la caméra cache ce qui est posé juste devant le mur à côté : avancer l'objet devant le bord libre du battant.
- (cycle 9) Un état rangé dans `userData` par l'usine d'un accessoire est perdu : `buildProp` remonte ce `userData` sur une enveloppe. Garder les états du moteur sur l'objet du directeur (`Pp.lastT`), pas dans la fermeture de l'accessoire (les aiguilles visaient comme à t = 0, figées sur le départ).
- (cycle 10) Le carton de titre posé sur le pic d'un étirement cache la prise : le poser après le retour au calme.
- (cycle 10) Du lettrage dans le bandeau des sous-titres (le bandeau d'un comptoir) se bat avec les sous-titres : pas de texte à cette hauteur.
- (machine) Quatre cœurs : trois rendus à la fois font ramper la génération complète en 1080p (0,1 image par seconde) ; enchaîner les générations complètes (`chain_*.sh`) plutôt que de les lancer ensemble.
- (cycle 13) Un accessoire modélisé à plat (le journal, posé sur une table) attaché à une main avec `face: 'camera'` montre sa tranche : le
  tenir debout en accessoire libre devant lui (`rot` x ≈ 1,3), ses mains sur ses bords.
- (cycle 13) Un outil long attaché à la main (le manche d'un rouleau) pointe là où pointent les axes de la main, en l'air : en faire un
  accessoire libre qui suit l'acteur (mêmes clés `to`), sa tête posée sur le sol, et poser les mains sur le manche (`reach` par clés).
- (cycle 13) `then='walk'` à la fin d'un déplacement : il marche sur place (le moteur le signale) ; `then='stand'`, ou un déplacement qui dure
  jusqu'à la coupe. Et quatre personnes envoyées au même point d'arrivée s'empilent : une ligne chacune.
- (cycle 13) S'accroupir en pliant le dos montre le dessus de la tête de boîte : tenir les pieds (`plant`) et baisser les hanches, les genoux
  plient d'eux-mêmes.
- (cycle 13) Le tapis rouge du salon mange un tiers de l'image dans les plans larges ou plongeants : `livingRoom carpet: False`.
- (cycle 13) Un visage la tête en bas derrière un bureau disparaît : le monter au-dessus du meuble et cadrer serré sur lui.
- (cycle 13) Une ligne trop longue pour son écran est rétrécie jusqu'à tenir (`lcdScreen`) : le prix qui devait être le plus gros sortait plus
  petit ; le mettre seul sur sa ligne.
- (cycle 13) Viser le vrai bouton : le doigt visait 10 cm à côté et c'est la manche qui appuyait. Et la caméra d'un insert sur un bouton ne se
  met pas du côté du bras (la manche remplit l'image) : de l'autre côté, d'en haut.
- (cycle 13) La sonde mesurait d'abord toute la tête avec ses effets cachés rangés à l'écart à l'échelle zéro (59 % de l'image) : mesurer la
  tête seule. Sa part « vue » est fausse sur un accessoire fin et ouvert (un pied à coulisse) : regarder l'image.
- (cycle 13) Un brouillon envoyé en revue avec des temps morts y perd la moitié de l'animation : `freeze_check.py` avant la revue.
- (cycle 14) Deux doubles plats dos à dos se séparent en deux têtes et trois mains : le balancement de repos et la vie des tenues sont en miroir.
  `toon: {shift: 0, holdLife: 0}` dans leur distribution, `look=None`, la posture `stiffStand`.
- (cycle 14) Un fil fin (laisse, gomme, ficelle) fait 1 ou 2 px sur un téléphone et disparaît par endroits : `minPx` (au moins 4 à 5 px d'une image
  de 1920) et `rim` (un liseré sombre) sur le `tether` ; des boucles au sol par `via` (un seul fil), pas des segments droits.
- (cycle 14) La sonde dit « vu à 100 % » d'un visage tourné de profil ou de dos : regarder l'orientation du visage aux sommets des gags (les
  revues de 51 l'ont relevé deux fois) et tricher le corps de 30 à 45° vers l'objectif dans chaque réaction.
- (cycle 14) Une caméra qui démarre dans un immeuble donne 0,2 s de gris uni : un travelling au-dessus des toits passe au-dessus du plus haut
  (20 m dans `parisStreet`) ; l'alerte « caméra dans un accessoire » ne couvre pas le décor.
- (cycle 14) Un commentaire ajouté en remplaçant le début d'une ligne avale la fin de la ligne (des clés entières disparues sans erreur) :
  le mettre sur sa propre ligne et lancer `lint_comments.py` après chaque correctif (six fois dans ce cycle).
- (cycle 14) Un effet `whoosh` écrit de l'aigu vers le grave (3000, 800) faisait échouer tout le mix : `mix.py` trie maintenant la bande ; un
  projet seul se relance avec `hf_only.sh` sans refaire la couche 3D.
- (cycle 14) Des vitres opaques cachent les passagers d'une cabine : `glassOpacity`. Une cible de main (`reach`) sur un corps à l'envers envoie les
  bras au plafond : plier les bras dans son propre repère (`bend`).
- (cycle 14) Les yeux sur tiges prêtés aux pompiers et à l'assureur affaiblissaient les trois prises du héros : aux autres une grimace
  (`react(kind='wince')`) ou une mâchoire qui tombe.
- (cycle 14) Une étiquette à côté d'un point sort du cadre au zoom et sa boîte mord le point : sous le point, sa boîte derrière ; et un texte de
  3 ou 7 px (un post-it, un chèque) se refait en version géante (règle de hauteur, chèque géant).
- (cycle 14) Le tableau du salon derrière sa tête au sommet de chaque saut : le déplacer hors de l'axe (`pictureX`) ou le retirer du plan.
- (cycle 14) L'écrasement-étirement se fait autour des pieds : un étirement qui se relâche au sommet d'un saut fait redescendre la tête, et l'étirement
  de chute posé au début d'une chute en ease-in la fait remonter : haut, bas, haut, choc (la revue de 50 a mesuré les épaules remonter de 4 à 10 %
  du cadre avant chaque chute). La tête atteint le sommet sur l'étirement et y reste pendant que les pieds rattrapent ; l'étirement de chute attend
  que la chute soit lancée.
- (cycle 14) Une double prise dont le regard vide dure 2 à 4 images se lit comme une seule prise : 6 à 8 images de regard vide vers nous, puis les
  yeux sortent vers la chose, tenus 8 à 12 images (`doubleTake(..., blank=0.25, hold=0.4)`).
- (cycle 14) Une double prise visée sur ce qui est derrière lui ne montre que l'arrière de sa tête : la prise vers l'objectif (ou la caméra du côté
  de la chose), et il s'arrête pour la prendre (une prise en marchant se perd).
- (cycle 14) Les joues gonflées seules (`puff`) font deux parenthèses à la bouche : la tête enfle (`scl: head`) avec le visage `puffed`.
- (cycle 14) Le décor `skyHigh` a des cumulus jusqu'à 50 m de haut : une caméra à 1,5 m est dans un nuage, le plan est gris uni. Tout le plan à 60 m,
  au-dessus de la mer de nuages ; et des barres blanches sur des nuages blancs ne se voient pas (un ruban d'asphalte sous le passage piéton).
- (cycle 14) Ce qui descend du ciel doit traverser le cadre : avec un objectif de 30°, un point à 26 m de haut reste au-dessus du bord haut jusqu'aux
  dernières images, et les mariés sur les marches sous le bord bas. Calculer l'angle (`lens` est le champ vertical en degrés) ou élargir.
- (cycle 14) Un plafond vu d'en dessous, éclairé par la pièce, sort brun et boueux (luminance 125 contre 150-173 ailleurs) : `ceilingPlaster`, un plâtre
  pâle non éclairé ; des fissures épaisses (`thick`) au bord clair ; des éclats qui tombent du contour du héros, pas d'un seul point.
- (cycle 14) Des spectateurs placés sous le héros qui regardent derrière eux pour le voir nous montrent leur nuque : les placer de façon que regarder le
  héros les tourne vers l'objectif (au fond, le regard vers le haut et vers nous).
- (cycle 14) Le préréglage `gamin` seul a la taille d'un homme : `build` height 0,52, headScale 1,5, des habits vifs.
- (cycle 14) Deux bras droits à l'horizontale pendant une vrille se lisent comme la pose en T d'un modèle : un bras enroulé sur la poitrine, l'autre
  jeté en arrière, la colonne vrillée.
- (cycle 14) Une main « tendue » à 0,42 m devant et 1,12 m de haut pend à la hanche : 0,55 m devant, 1,32 m de haut (à la poitrine).
- (cycle 15) `st.at(shot, ligne, mot)` donne déjà le temps dans le plan : lui retirer encore le début du plan (`- st.SH[...][0]`) met le temps fort
  avant le plan, et il ne se joue jamais (52 : le boomerang ne tombait pas sur la tête du marié, l'avion freinait hors champ, la pièce tombait avant
  la passante). `st.write` le signale maintenant (« keys before the shot starts »).
- (cycle 15) Recoller plutôt que tout refaire : un brouillon dont seuls deux plans changent se corrige par `render3 --range a:b` et
  `tools/splice_range.sh` (deux plans en 20 min au lieu de 105 min pour le film entier).
- (cycle 15) Le moteur ajoute son propre écrasement-étirement selon la vitesse verticale (jusqu'à ×1,32) : il se multiplie à celui qu'on clé à la main.
  Dans un saut clé à la main, mettre `autoSq: 0` dans chaque clé (50 : la tête dépassait le sommet de 0,9 m au départ et remontait au début de la
  chute ; l'« accroc au sommet » des trois revues venait de là). Mesurer le saut image par image avec `debugJoints` avant de le juger.
- (cycle 15) Sur un corps couché ou la tête en bas (`lay`), l'IK des mains est résolu avant la rotation : donner à `reach` le point que la rotation
  amène sur la cible (miroir autour des pieds), et couper le balancement de poids (`hip: 0`), qui faisait glisser les mains du clavier.
- (cycle 15) `lay` fait pivoter le corps autour de ses pieds : couché, il s'étend sur 1,9 m (2,5 m bras compris) depuis ses chaussures. Placer les pieds
  pour que le corps entier tienne dans le cadre (51 : le « oh-oh » sortait du cadre par la tête).
- (cycle 15) Pas de traînée de vitesse (`smear`) sur un corps couché sur le côté : son étirement latéral le redresse à la verticale.
- (cycle 15) Un accessoire tenu (`on` main + `offset`) : l'axe y de la main descend le long de l'avant-bras ; un téléphone centré sur le poing est
  caché par le poing et l'avant-bras. Le monter hors du poing (y négatif) et le mettre devant (z négatif), puis vérifier sur une image.
- (cycle 15) `touch` sur le visage peut laisser la main derrière la cible ; pour un objet tenu devant la poitrine ou le menton pendant la marche, guider
  la main dans le repère du torse (`['torso', x, y, z]`).
- (cycle 15) Des yeux qui se ferment pile sur un sursaut se lisent comme une grimace : `face: {noBlink: 1}` dans les clés du plan, et le clignement clé
  six à huit images après.
- (cycle 15) Dans un intérieur, une caméra basse qui regarde vers le haut cadre le plafond sombre : 40 % du cadre bleu marine au plan 10 de 53, la
  scène cachée. Monter la caméra et regarder vers le bas (par-dessus l'épaule de quelqu'un, à 2,5 m).
- (cycle 15) Un coin noir dans le ciel : la caméra regarde trop haut, vers le sommet sombre du dôme. Baisser la visée, garder la cible plus bas.
- (cycle 15) Un gag de direction (il marche à reculons, il roule en marche arrière) se lit de profil, ou dans l'axe avec un contraste : sa voiture
  vient vers nous par l'arrière pendant que celle d'à côté vient par l'avant. De face, ou en travers de la rue, l'arrière ressemble à l'avant.
- (cycle 15) Un visage dans une voiture fermée tombe dans l'ombre de la carrosserie (« une pièce sombre ») : une décapotable le met au soleil.
- (cycle 15) Une main près d'un visage tourné (la tête sur le dos) : la guider dans le repère de la tête (`['head', x, y, z]`, son avant est là où est
  le visage), pas sur le visage, qui peut laisser la main à la poitrine.
- (cycle 15) Un triangle fait d'un cône à trois côtés aplati (un fronton) : une de ses faces tombe dans l'ombre, la moitié droite noire. Une
  extrusion plate face à la rue s'éclaire d'un seul ton.
- (cycle 15) Un flash d'appareil photo en disque translucide se lit comme une bulle de savon : un éclair blanc plein cadre (`fx: flash`).
- (cycle 15) Un objet tenu ne doit couvrir ni la main ni le visage : le tenir par un coin (l'accessoire décalé de la main), à côté du visage.
- (cycle 16) Le haut du ciel noir ou brun en extérieur venait d'objectifs très larges (69°) : passé 56°, le haut du cadre atteint le haut sombre
  du dôme. Limiter `lenses` à 56 en extérieur (`range(30, 57)`) et reculer la caméra plutôt qu'ouvrir.
- (cycle 16) `fitBack` recule la caméra jusqu'à ce que tout tienne : elle peut passer derrière un décor (au plan 7 de 53, derrière un montant noir de
  la vitre du guichet : une barre sombre au milieu de l'image). Lui donner la pièce où rester (`inside=(x0, x1, y0, y1, z0, z1)`) : au bord, il ouvre
  l'objectif au lieu de reculer.
- (cycle 16) Un point très lointain dans les points de cadrage (là où file un boomerang, à 16 m) pousse le personnage au bord du cadre, coupé : garder
  la trajectoire de l'objet dans le cadre (la ramener plus près, plus bas) et ne cadrer que des points proches.
- (cycle 16) Un insert sur une main filmé du côté du personnage filme le dos de sa veste (deux tiers du cadre bleu marine) : passer de l'autre côté de
  la main, et déclarer le gag sur la main (`st.gag(..., joint='handR')`) pour que la sonde mesure ce qui la cache.
- (cycle 16) Un accessoire tenu en main part le long de l'avant-bras par défaut (une cuillère invisible, cachée par le bras) : le retourner hors du
  poing (`'rot': [3.1416, 0, 0]` sur `on`) et le colorer sombre sur un mur clair.
- (cycle 16) Un accessoire sur trépied tourné d'un quart de tour pour pendre au plafond : ses pieds deviennent trois barres noires et son corps part à
  1,5 m de là où on l'a mis ; utiliser sa variante sans pieds (`tvCamera` `legs: false`).
- (cycle 16) Le héros qui fait face à un tapis, un comptoir, une vitrine tourne le dos à une caméra placée de notre côté (l'audit : « turned 170 deg
  away ») : mettre l'action derrière l'objet, face à nous, ou filmer par-dessus l'épaule de celui d'en face.
- (cycle 16) Dans la cabine d'une caméra de plateau qu'on « devient » (le plan suivant est sa vue), cacher l'accessoire à la coupe : il bouchait la
  moitié du plan en grue.
- (cycle 16) Un visage tourné vers le plafond, filmé de loin, fait 70 px et se lit comme une boîte vide : plus près et plus haut, cadré aux genoux.
- (cycle 16) Une passante ou un enfant qui traverse doit marcher au-delà de la coupe (la durée du déplacement plus longue que le plan) : arrivé avant
  la fin, il piétine sur place.
- (cycle 16) Un commentaire collé au milieu d'une ligne de code avale la fin de la ligne : dans `props_valise.js`, `// ...` posé devant
  `hatch.position.set(...); g.add(hatch);` a fait disparaître le tunnel du tapis à bagages de tous les plans. Après chaque modification :
  `python3 tools/lint_comments.py` (scripts Python) et `python3 tools/lint_js_comments.py` (moteur JavaScript).
- (cycle 16, passe 3 de 53) Un nom de pose de main inconnu ne fait aucune erreur : la main garde la pose de repos. `'flat'` n'existe pas (les mains
  de l'ostéopathe « flottaient » à côté de la tête, la claque sur le réveil s'arrêtait une main au-dessus) ; les poses sont `rest`, `open` (main à
  plat), `spread`, `fist`, `point`, `two`, `pinch`, `thumbUp`, `grip` (agripper), `claw` (gratter).
- (cycle 16, passe 3 de 53) Un `reach` vise un point du monde : sur un personnage qui roule (voiture, tapis), la main reste sur place derrière lui.
  Pour un bras posé sur le dossier, une main sur la hanche, utiliser `touch` dans le repère de son propre buste (`['torso', x, y, z, 1, tip]`).
- (cycle 16, passe 3 de 53) Un accessoire tenu en main pointe où pointe le poignet : la cuillère arrivait « cuilleron en l'air » au-dessus de la tête,
  jamais dans la bouche. Pour un contact précis (cuillère dans la bouche, puis dans l'oreille), échanger à l'arrivée la cuillère de la main contre
  une copie fixée à la tête (`on={'actor', 'joint': 'head', 'offset', 'rot'}`, clés `visible`), la main posée sur le manche (voir `SPOONAT` dans
  `story_torticolis.py` : le cuilleron à un point, le manche dans une direction, le creux tourné vers le haut). Mesures de la tête du héros :
  0,24 m de large, 0,5 de haut, 0,17 de profondeur, l'articulation au menton ; la bouche à 0,115 m au-dessus, le visage à 0,085 m devant.
- (cycle 16, passe 3 de 53) Un papier qu'on doit lire (un permis à l'envers) tenu dans la main finit au bord du cadre, à moitié derrière le poing, et
  le travelling avant le perd : en faire un accessoire à part, `face='camera'`, posé à côté du visage, la moitié de la largeur du cadre, la main
  qui le pince par un coin, le travelling avant qui atterrit dessus avant le mot.
- (cycle 16, passe 3 de 52) L'ordre du canal `bend` est `[bx, bz, torsion, étirement, gras]` : un tour complet de la tête se met dans la torsion
  (3e valeur). Mis dans `bz` (2e), c'est une flexion de côté : la tête passe sous les épaules et le personnage paraît sans tête neuf images (plan 6
  du boomerang). Pour qu'elle reste au-dessus du col pendant le demi-tour arrière, étirer le cou (4e valeur, 1,8) puis le rendre en rebondissant.
- (cycle 16, passe 3 de 52) Un voile en cône rond accroché à la tête balance son ourlet devant le ventre dès qu'elle tourne la tête (« une cloche
  blanche », lu comme une grossesse) : `brideVeil` `drape: True` l'aplatit dans son dos.
- (cycle 16, passe 3 de 52) Un « passage piéton » se lit seulement si le piéton coupe la trajectoire à l'écran : vu de trois quarts, le boomerang qui
  file dans le sens de l'avion « passe devant » au lieu de traverser ; le faire venir vers nous pendant que l'avion va à droite, juste devant son nez,
  et poser la route sous les roues (`skyCrossing` `roadLen`, `stopLine`).
- (cycle 16, passe 3 de 52) Un personnage qui doit passer « loin dans le ciel » au-dessus d'un autre : calculer sa trajectoire à partir du cadre
  (`AT16` dans `story_boomerang.py` : le point d'un plan de profondeur que la caméra met à telle fraction du cadre) au lieu de la poser à la main
  (posée à la main, elle passait sur le chignon de la mariée).
- (cycle 16) `render3 --probe` s'arrêtait après la sonde : les images `--stills` du même appel n'étaient jamais faites (le dossier gardait celles d'un
  rendu précédent). Corrigé : sonde et images dans le même appel ; vérifier tout de même l'heure des fichiers.
- (cycle 16) En corrigeant un script par remplacement de texte, ne jamais terminer un remplacement par un commentaire quand le texte remplacé
  s'arrête au milieu d'une ligne : la suite de la ligne passe dans le commentaire sans erreur (trois fois en une passe : des clés de regard, une
  constante `VEILOFF`, des clés de caméra). `tools/lint_comments.py` attrape maintenant aussi `; NOM = ...` dans un commentaire.
- (cycle 17, passe 2 de 54) L'étiquette de la valise pendait de la poignée au milieu de la coque : la carte dorée était **dans** la valise, aucune
  revue ne l'a jamais vue. Avant de compter sur un détail d'accessoire, le regarder sur une image de contrôle rapprochée ; l'étiquette pend
  maintenant devant le couvercle (`tagScale` pour l'agrandir, `tagGlint` pour un scintillement).
- (cycle 17) Le poids d'un `reach` (4e valeur) au-delà de 1 n'allonge pas le bras : il extrapole la main au-delà du point, le bras pend à côté
  (la main « sortie » du couvercle qui mord). Toujours 1 ; pour un bras élastique, éloigner le corps (`lay`, colonne en arrière) pendant que la
  main reste au point.
- (cycle 17) `fitBack` collé à un mur rend un objectif plus large que permis sans erreur (77°, 85° au comptoir de la valise) : le `FC` des
  histoires affiche désormais un AVERTISSEMENT ; resserrer les points ou avancer tout le décor (le comptoir avancé d'1,2 m).
- (cycle 17) Un accessoire dirigé droit vers la caméra se lit comme un disque (la ventouse sur le front, vue de face : une boule rouge) :
  l'incliner (40° vers le haut) pour montrer sa longueur.
- (cycle 17) Une enseigne lisible d'un seul côté (ENREGISTREMENT, tourné vers les clients) ne peut pas être cadrée depuis l'autre côté : ne pas
  promettre le mot dans un plan pris de derrière le comptoir.
- (cycle 17) Un personnage collé face à une surface (vitre d'un bus) ne montre jamais son visage : préférer un gag où c'est la chose qui vient
  se coller à lui (un pigeon qui s'écrase sur la ventouse), visage vers nous.
- (cycle 17) En écrivant une liste `actors=[act(...), act(...)]`, le dernier `act` se ferme par `)])],` avant `props=` : l'oublier donne
  « closing parenthesis ')' does not match » trois lignes plus bas (trois fois dans l'histoire 55).
- (cycle 18) **Main guidée + bascule ou épingle** : le moteur posait la bascule (`lay`) et l'épingle (`pin`) après le calcul des bras, si bien
  qu'une main guidée ratait son point dès que le corps basculait ou pendait (le bras élastique sorti du couvercle de la petite valise, les
  mains des passagers à côté des siennes). Corrigé au cycle 18 : `lay` est posé avant le rig, `pin` est résolu dans le rig avant les mains.
  Les histoires livrées avant réglaient leurs mains à l'œil avec ce défaut : à re-rendre, vérifier leurs mains guidées.
- (cycle 18) **Script de revue** : une description entre apostrophes simples qui contient une apostrophe (« plane's path ») casse le heredoc
  Python ; la chaîne affiche quand même son marqueur et les critiques partent sans consignes. Écrire les dictionnaires avec `repr()` ou des
  apostrophes typographiques, et vérifier que `prompt_anim.txt` et `prompt_art.txt` existent avant de lancer les critiques.
- (cycle 18) Un coup reçu quand le personnage est penché en deux (la tête dans le tunnel) : son visage regarde le sol, la caméra voit le dessus
  du crâne. Tordre le cou vers l'objectif au moment où il ressort (canal twist du cou, ici −1,2 rad) : la gifle tombe sur un visage.
- (cycle 18) Écrasement « en tranche » dans un décor sombre : costume sombre sur fond sombre, lampe derrière lui, il ne se lit pas. Lampe
  devant lui, caméra plus près, une onomatopée au choc (SCHLAC !).
- (cycle 18) Un personnage d'avant-plan coupé à la tête par le bord du cadre (plan par-dessus l'épaule) : l'inclure en entier ou le sortir du
  cadre sauf le bras (l'agente déplacée de 0,6 m suffisait).
- (cycle 18) Le contrôle à l'écriture se trompe sur les poses assises au sol : « tête coupée » alors que l'image est bonne. La sonde du rendu
  (`--probe`) et les images font foi.
- (cycle 18) Une rame vue du quai : ses vitres sombres remplissaient le cadre comme un mur noir pendant le passage. Vitres claires (`metroCar`
  o.glass) et train parti plus loin : sa queue passe en un tiers de seconde.
- (cycle 18) Dans ce monde les adultes mesurent 2,1 à 2,2 m (le front à 1,99 m) : un point de cadrage à 1,9 m coupe les têtes. Viser le haut
  réel des têtes (2,25 m).
- (histoire 53, passe finale) Deux prises de témoin pareilles (yeux sur tiges, bouche ouverte) dans un même film : c'est un gag réutilisé. En
  varier les moyens (étirement et mâchoire jusqu'au col pour la dame, chapeau qui saute et mâchoire sur le volant pour le chauffeur).
- (histoire 53, passe finale) Un figurant qui ressemble au héros (même peau, cheveux noirs, barbe de trois jours) se fait attribuer la prise, et
  la règle « il reste impassible » se casse : chapeau, moustache, cheveux gris.
- (histoire 53, passe finale) Un cabinet d'ostéopathe dans le décor `hospital` : moniteur cardiaque et croix rouge disent hôpital (et la croix
  sortait de la tête de l'ostéopathe). Options `monitor: False`, `cross: False`.
- (histoire 53, passe finale) Une marche à reculons ne se lit qu'avec un repère : un passant qui marche à l'endroit à côté de lui, dans le même
  sens, caméra sur son chemin à hauteur de hanche (seul et petit dans un cadre aux deux tiers vide, il « marchait », tout simplement).
- (cycle 18) Dans un accessoire, `Object3D.lookAt` prend des points du **monde** : appelé avec des coordonnées locales dans un `update(t)`,
  il couche les objets dès que l'accessoire est attaché à une articulation (les randonneurs allongés sur la colline posée sur sa tête).
  Orienter à la main (`rotation.set(0, atan2(dx, dz), 0)`), ou n'appeler `lookAt` qu'à la construction, avant tout rattachement.
- (cycle 18) Un commentaire collé en fin de ligne après une modification automatique avale encore la fin de la ligne (`],` du `props=[...]`
  de S01, histoire 56) : le lint ne voit rien quand le fichier ne s'analyse même plus ; lancer le script tout de suite après chaque modification.
- (histoires 52, 54, 55) Un sol d'accessoire posé exactement à y = 0 dans le décor `whiteVoid` (quai, plancher de rame) se bat avec le sol du
  vide pour les mêmes pixels : il clignote d'une image à l'autre entre les deux couleurs (bleu nuit et beige, tout le plan final). Monter le
  dessus de ces sols d'un centimètre.
- (histoire 54) Écraser une tête le long de l'axe de la caméra ne se voit pas (écrasée d'avant en arrière, visage tourné vers l'objectif : même
  taille avant et après la gifle). Écraser le long d'un axe visible dans l'image, ici sa propre hauteur, couchée à l'horizontale.
- (histoire 54) Un assistant de prise (`doubleTake`) et des clés `toon` du plan aux mêmes instants se battent : la mâchoire tombait à 1,60 s sur
  1,63. Écrire la prise à la main, ou laisser l'assistant seul.
- (histoire 54) Un objet héros couché sur un tapis roulant ne se lit pas (un liseré rouge de 40 × 50 px) : le mettre debout, face à l'objectif,
  et le faire sortir des lamelles dès la coupe.
- (histoire 52) Un voile en cône dont la pointe dépasse de 12 cm au-dessus de la tête : de face, une corne blanche sur le chignon. Le faire partir
  d'un anneau au bandeau (`brideVeil` o.ring).
- (cycle 18) L'espace disque de la session se remplit (segments de rendu, images des critiques, calques 3D en double) et le rendu HyperFrames
  refuse de partir sous 1 Go libre. Après chaque livraison, supprimer les segments assemblés et les images de travail des critiques ; ne jamais
  toucher aux sorties de la réplique de la tornade.
- (cycle 19) `fitBack(..., inside=...)` rendait tel quel un point de départ hors de la pièce (avec l'objectif le plus large) : le plan filmait le
  dos du mur du hall. Il ramène maintenant le départ dans la pièce et l'écrit (`WARNING ... brought inside`) ; corriger alors le départ dans le script.
- (cycle 19) Le sol du décor `whiteVoid` est maintenant 4 mm sous y = 0 : les sols d'accessoires posés à y = 0 ne se battent plus avec lui.
- (cycle 19) Poser un personnage sur un accessoire porté par la tête d'un autre (le médecin sur la bosse) d'après une hauteur estimée : la boule
  n'était pas écrasée avec l'homme (`sq` ne touche pas la chaîne de la tête) et le médecin avait les jambes dedans. Mesurer avec `debugJoints`
  (une image fixe suffit) avant de poser quoi que ce soit dessus.
- (cycle 19) Une échelle « appuyée » contre une sphère dont le haut entre dans la sphère, avec un personnage dessus : le corps dans la boule.
  Le point de contact d'une échelle inclinée de L radians est à L au-dessus de l'équateur ; ou poser le personnage sur le sommet.
- (cycle 19) Un poteau central dans une porte tournante où l'homme tourne à l'axe : il ressort par son visage dans les plans embarqués.
- (cycle 19) Dans un cadre vertical, une chute de travers sort du champ en trois ou quatre images (le skieur de 56) : faire tomber de haut en
  bas, devant le visage, et cadrer le point de départ en entier.
- (cycle 19) Un personnage qui recule derrière une poutre basse après le choc garde son visage caché par la poutre : le faire passer dessous,
  écrasé, vers l'objectif, et ressortir la tête devant.
- (cycle 19) Une carte tendue par une main se cache derrière le corps de celle qui la tient quand la caméra est derrière son épaule : la tenir
  de son côté vers la caméra.
- (cycle 20) Laisser `fitBack` reculer la caméra sans `inside=` dans un décor fait d'accessoires (le quai de métro et son mur carrelé) : elle
  est passée 7 cm derrière le mur, vu de dos comme un voile gris sur quatre images, jusqu'à ce que le plan proche le coupe (55, S15).
  L'alerte « camera inside prop » du rendu le signalait ; `tools/grey_scan.py` trouve ces chutes de saturation dans une vidéo.
- (cycle 20) Courber les bras avec `bend` pour les écarter : `bend` courbe une partie, il ne tourne pas l'articulation, et les bras sont restés
  le long du corps (57). Pour une pose en T, placer les mains avec `touch` dans le repère du torse (à ±0,8 m, hauteur des épaules 0,55).
- (cycle 20) Un bras guidé plus loin que sa longueur devient une ligne droite : les deux bras tendus vers le manche au-dessus de la tête ont
  fait un A devant le visage. Garder le coude plié avec `hose` (0,3) et le diriger vers l'extérieur avec le pôle de `touch`.
- (cycle 20) Un nom de chapeau inconnu du rig (`bowler`) : pas de chapeau du tout, et le gag du chapeau envolé a disparu. Vérifier le nom
  (`fedora`, `beanie`, `hardhat`, `cap`).
- (cycle 20) Plier les genoux avec `sq` et `bend` sur les jambes : l'écrasement d'ensemble et les jambes courbées soulèvent les pieds, le
  genou ne descend que de 1 % du cadre. Épingler la tête plus bas (`pin`) en gardant les pieds au sol (`plant`) : l'IK plie les jambes.
- (cycle 20) Un ciel qui vire au noir dès que la caméra regarde vers le haut (56 : S07, S08, S10, S14) : le « ciel approfondi » du rendu
  naturel lisait le rayon d'un dôme sans sphère englobante calculée et prenait 180 m pour un dôme de 3 km (`skyFollow`) ; au-dessus de 29°
  la luminosité tombait sous zéro. Corrigé dans `look.js` ; un point noir en haut du ciel ou une nuit au milieu d'une scène de jour vient de là.
- (cycle 20) Une clé `toon` agit APRÈS son instant (le mélange dure `toonDur` à partir de la clé) : un accroupissement clé à 0,22 avec 0,2 de
  durée n'était bas qu'à 0,42, trop tard pour la relève (58). Placer la clé `toonDur` plus tôt que la pose voulue.
- (cycle 20) Pencher le buste quand une mâchoire tombée (`jawBlock`) pend jusqu'au sol : elle est solidaire de la tête et part derrière les
  hanches. Pour la ramasser, s'accroupir (tête épinglée plus bas, pieds plantés) et raccourcir `jaw` pour garder le menton au sol.
- (cycle 20) Insérer un commentaire en fin de ligne avant la suite du code (`}` ou `,`) : le commentaire avale la suite (deux fois encore).
  Le placer après tout le code de la ligne, ou sur sa propre ligne.
- (cycle 21) `fitBack` garde par défaut la caméra de niveau (`level=True`) : une caméra basse ne peut pas poser le sujet au pied du cadre, il
  reste vers le milieu (57 S08 : la porte à 68 %, le tiers bas en sol vide). Passer `level=False` pour qu'elle s'incline.
- (cycle 21) Un personnage incliné (`reclineBack`) a la tête 0,4 m derrière son siège : posé 0,2 m devant un fond (la bouche sombre de 58),
  sa tête s'enfonce dedans et il paraît décapité. Décaler le siège de la longueur du buste.
- (cycle 21) Une lettre qui « sort de la bouche comme un toast » : une carte ne peut pas cacher sa moitié basse derrière le visage (devant,
  elle couvre le visage ; dedans, on ne la voit pas). La faire jaillir d'une fente de la bouche jusqu'au-dessus de la tête, la tenir en l'air,
  la rattraper.
- (cycle 21) Encore une clé avalée par un commentaire (57 S14 : la facture apparaissait dans sa main sans que le bras bouge). Vérifier avant
  chaque rendu : `grep -nE "#.*\bk\(" scripts-fr/story_X.py` ne doit trouver que des commentaires voulus.
- (cycle 21) Des mains levées sous un auvent : à 1,45 dans le repère du buste, étiré de 1,18, elles montaient dans l'auvent sombre de la
  porte et disparaissaient (57 S12). Comparer la hauteur des mains au plafond du décor.
- (cycle 21) Un déplacement en course (`clip='run'`) terminé par `then='run'` : il court sur place après (le moteur le signale). Finir sur
  `stand`, ou allonger le déplacement jusqu'à la sortie du cadre.
