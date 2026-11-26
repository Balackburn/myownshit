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
| La porte qui l'emporte | il pousse le battant : la porte accélère et il tourne en son axe (`yaw` en tours), bras jetés en T, cravate à l'horizontale, cheveux dressés, son visage impassible revient face à nous à chaque tour | 57 |
| Le chapeau soufflé par le vent de la porte | le chapeau d'un passant se soulève, reste cinq images en l'air (ses yeux montent d'abord), puis file en tournoyant sous la bande du carton pendant qu'il attrape le vide d'un bras étiré | 57 |
| La barbe de trois ans filmée de l'intérieur | caméra qui tourne avec le compartiment (`ride`) : son visage reste face à nous, la rue défile derrière ; une barbe en touffes pointues gris-brun pousse et traîne dans la rotation | 57 |
| Le technicien électrocuté | il enfonce la prise : BZZT, raide, étiré, bras et jambes écartés, tenue qui vibre, casque qui monte sur sept images et flotte au-dessus des cheveux dressés, gerbe d'étincelles | 57 |
| Le quartier qui s'allume | la nuit, la porte lumineuse au pied du cadre, les fenêtres de toute la ville s'allument en vague de gauche à droite, caméra basse inclinée vers le haut | 57 |
| La carte d'abonnement collée sur la figure | le coach tend la carte, un battant la lui arrache et la plaque sur le visage du tournoyant, vu de l'intérieur du compartiment | 57 |
| Le balai dans la porte | CLANG : le manche du balai bloque le battant, la porte s'arrête net, les yeux du concierge sortent ; lui continue de tourner au milieu comme une toupie, bras en V sous l'auvent | 57 |
| La vrille qui sort de la porte | il sort de la porte en vrille, penché, et fait tourner deux fois une passante qui finit face à nous, les yeux qui louchent | 57 |
| La galette à l'arrêt | il s'arrête net : quatre images de suspension étiré, puis le haut retombe sur lui, aplati à 45 % douze images, rebond au-delà de sa taille, oscillation, grandes étoiles à hauteur des yeux | 57 |
| La facture sortie de la poche | le technicien porte la main à sa poche et lève la facture « PANNE DU QUARTIER, 9 999 € », tampon À PAYER ; impassible, un clignement | 57 |
| La mâchoire qui tombe en bloc (cycle 20) | `face.jawBlock` : le bas du visage devient un bloc pendu devant le corps ; un bâillement étiré trois temps, puis le bloc descend jusqu'au trottoir en 0,1 s, CLONK, poussière, yeux qui sortent ; il le remonte à deux mains, le lâche : il retombe (même chute, plus sèche) | 58 |
| La langue déroulée en tapis | accessoire `tongueSlide` : la langue se déroule sur le trottoir comme un tapis rouge pendant que le maire en écharpe (`mayorSash`, bleu au col) coupe un ruban aux grands ciseaux (`bigScissors`) ; le panneau TOBOGGAN surgit | 58 |
| La mamie qui glisse dans sa bouche | la file du dimanche attend au pied d'une échelle posée contre lui ; une mamie glisse de sa lèvre au bout de la langue, bras levés, YOUPI ! au-dessus d'elle (texte accroché au torse, décalé vers la caméra) ; siège décalé de 0,38 m pour que sa tête ne s'enfonce pas dans la fente | 58 |
| Les lettres qui tombent dans la fente | le facteur glisse les lettres entre ses lèvres ; accessoire `slotLetters` accroché à l'articulation de la tête : trois lettres tombent dans la fente l'une après l'autre en tournoyant, dans son repère (posées dans le monde, elles passaient à côté de lui quand il respirait) | 58 |
| SNAP : la bouche qui se referme sur le facteur | le facteur penché tête la première avec un colis ; la mâchoire remonte d'un coup (0,06 s), SNAP, le facteur a disparu, sa casquette redescend seule en papillonnant ; carte CLAC sur un seul angle | 58 |
| Le poing qui bombe la chemise | accessoire `bellyBulge` (chemise blanche, plis) : une bosse remonte le long de sa chemise, puis trois coups de plus en plus forts la bombent de l'intérieur (TOC, TOC, TOC de plus en plus grands) ; lui impassible, les pupilles qui suivent | 58 |
| Le courrier qui sort comme un toast | une lettre monte entre ses lèvres comme une tranche de pain d'un grille-pain, à moitié sortie, puis saute ; il la prend et la lit, impassible, une respiration | 58 |
| La grimace qui reste quand le vent tourne | les doigts aux coins de la bouche, la grimace tirée en cinq images avec dépassement (bouche étirée, langue sortie, yeux qui louchent, un œil gros, tête élargie) ; tenue qui tremble, langue qui remue à contretemps ; coupe sur la girouette qui grince puis tourbillonne ; il lâche : la grimace reste | 59 |
| Le visage remis en place qui ressaute | appui frontal des deux paumes à plat sur les joues, coudes écartés, tête écrasée en hauteur, yeux exorbités vers le haut, le corps qui force ; il lâche sur un visage normal tenu treize images avec un soupir de soulagement, puis BOING : la grimace revient plus large, trois oscillations | 59 |
| La photo d'identité jumelle | l'employée tient la photo grimaçante à côté de son visage (la même grimace) ; double prise, yeux grossis derrière les lunettes, suspendue quatre images en haut de sa prise ; le tampon REFUSÉE s'abat et la photo saute dessous | 59 |
| La poignée de main qui fait claquer la grimace | le patron du carnaval s'illumine (prise avant la poignée de main), puis secoue si fort que quatre grosses secousses remontent le bras jusqu'à la tête et font claquer la grimace ; confettis tombés d'en haut | 59 |
| La girouette qui se dévisse en hélicoptère | le coq de fer s'enfonce et tremble (creux d'anticipation `dip`), puis se dévisse et décolle en tournant comme un rotor, feuilles soufflées dans l'autre sens que la première fois | 59 |
| La rafale qui grimace la foule, sauf lui | la rafale traverse la foule : chaque visage claque dans sa propre grimace l'un après l'autre ; sur lui, la langue rentre d'un coup, la tête reprend sa taille en ressort, un clignement : son visage normal est la chute | 59 |
| Le doigt du patron qui traverse la rue | le patron grimaçant le chasse : son bras s'étire en travers de l'image et sort par le bord, le doigt qui pique ; pointé vers le fond de la rue, il était dans l'axe de l'objectif et ne se voyait pas | 59 |
| La frayeur des enfants grimaçants | les enfants en grimace regardent son visage normal huit images, puis hurlent, sautent hors de leur peau à des hauteurs différentes (casquette en arc sur le ciel) et sortent du cadre l'un après l'autre ; il reste seul, impassible | 59 |
| Le mot qui gonfle jusque dans l'objectif (cycle 22) | accessoire `shoutLetters` : des lettres découpées « OHÉ ! » jaillissent de la bouche grande ouverte (`jaw`), plan buste en contre-plongée contre une chaîne de sommets proches ; le mot grossit sur l'axe de l'objectif jusqu'à remplir l'image, son souffle couche ses cheveux et sa cravate (`wind` vers l'avant) | 60 |
| L'oreille en coupelle (cycle 22, passe finale) | canal `earScale` au-dessus de 1,3 : l'oreille devient une vraie coupelle couleur de peau (bol, intérieur sombre, rebord, pli), sortie trois fois sur des deux-images, chaque fois rentrée au-delà de sa taille ; la main en cornet sur l'oreille côté caméra ; grillons | 60 |
| Le cri muet au guichet | il mime son cri au gendarme, bras ouverts en V hors de la silhouette du gendarme ; entre ses mains, le cri silencieux (bouche ouverte, pas de son) ; le gendarme note | 60 |
| L'avis claqué au mur, PAF | l'avis de recherche (une bulle « OHÉ ! ») porté dans la main qui frappe, laissé là où la paume touche ; PAF au contact ; double prise tenue sur l'avis | 60 |
| Le mot qui traverse les vallées | un randonneur (sac, bâton) et un fermier (casquette, fourche, vache qui se retourne) lèvent la tête : les lettres passent dans leur ciel avec des traits de vitesse le long de leur trajectoire ; la casquette du fermier s'envole en tournant et retombe de travers | 60 |
| La crêpe, la planche, POP | le mot redescend la rue en grossissant : yeux sur tiges de profil ; SPLAT, aplati sur le trottoir (vu de trois quarts depuis ses pieds, bras écartés), décollé du trottoir, relevé raide comme une planche vue par la tranche, puis POP : il reprend sa forme d'un coup en plan moyen | 60 |
| La rue qui crie trois jours | la nuit, les lettres géantes cognent entre les immeubles dans des flaques de lumière de réverbère, les voisins se bouchent les oreilles ; le jour, cernes sous ses yeux, mains sur les oreilles | 60 |
| L'amende plaquée sur le front | le gendarme arme le geste, l'amende portée dans la main qui frappe et laissée sur le front tourné vers nous, au-dessus des yeux ; gros plan final : un tout petit « ohé » blanc descend à côté de son visage, clignement lent | 60 |
| BOING : écrasé sur le banc, yeux sur tiges | assis, le ressort sort du banc : `sq` [1,38, 0,6, 1,38], tête étirée en hauteur, yeux sortis sur tiges (`pop` 0,85), mâchoire ouverte, mains jetées à côté de la tête (`touch` ['head', ±0,4, 0,3, ...]), cheveux dressés, tenu cinq images en tremblant ; puis étiré comme un élastique, bras en l'air, parti en trois images ; le banc vide et son ressort qui oscille | 61 S02 |
| L'accordéon sur le toit | il retombe sur un toit en zinc : crêpe (le corps aplati, la cravate qui dépasse), rebond plus haut que sa taille, amorti en accordéon qui s'éteint (hauteurs de tête 204, 251, 190, 200 px) ; les pigeons s'envolent, plumes qui tombent | 61 S04 |
| Le saut par-dessus la passante | de profil, sauts à pieds joints en pogo (`hops_ball` : étirement qui s'éteint pendant la montée, sommet rond, écrasement tenu deux images) ; une passante s'accroupit, mains sur la tête, il passe au-dessus d'elle au milieu du cadre, puis elle se relève en le suivant des yeux | 61 S05 |
| La tasse qui reste en l'air | au café, il part d'un bond hors du cadre : la tasse reste suspendue seule une dizaine d'images ; il retombe sous elle, main ouverte, et la referme au fond de l'écrasement, la tasse plongeant un peu ; regard vers nous | 61 S06 |
| La coche OBJET VOLANT | insert du formulaire vu d'en haut : DÉCLARATION, OISEAU, AVION, OBJET VOLANT ; la main de l'employée sur la case, le stylo rouge qui suit le trait de la coche | 61 S07 |
| L'autocollant claqué au rebond | l'employée suit ses rebonds de la tête, puis son bras élastique (`touch` ['@mec.torso', ...]) colle F-MEC sur sa poitrine à l'atterrissage, sa main et son écrasement tenus trois images ensemble, CLAC dans le cadre à côté ; il repart avec | 61 S08 |
| CLONK dans l'abat-jour | un bond de trop au fauteuil d'examen : tête aplatie dans l'abat-jour deux images, l'ampoule nue qui se balance sur son fil, il retombe assis coiffé de l'abat-jour rouge, impassible | 61 S10 |
| L'arrêt net en plein vol, puis le nid | trois bonds de plus en plus hauts vers nous, arrêt net au sommet (écrasement, cravate relevée, cheveux qui retombent), balancier lent dans le vide ; gros plan : les pigeons se posent sur sa tête, nid, trois œufs qui apparaissent un par un avec un dépassement, clignement lent | 61 S12-S14 |
| Rouge comme un thermomètre qui monte | le canal `skin` (`fill` de 0 à 1) fait monter le rouge par niveaux : les mains, puis le cou, puis toute la tête ; vapeur encrée qui sort des oreilles (`steam` 1, `steamInk` 1) ; il reste impassible dans son transat | 62 S01 |
| L'œuf cuit sur le front | la voisine casse un œuf sur son front (main guidée, CRAC entier dans le cadre) ; l'œuf s'étale au plat et grésille (`friedEgg`, coquilles qui s'écartent `shellSpread`) ; ses yeux montent vers l'œuf et louchent (`expr` surprised 0,6, `gy` −0,6, `cross` 0,85) | 62 S02 |
| Le quartier éclairé par sa tête | la nuit, sa tête rouge est la lampe de la rue (`skin` lueur 1, `glowLight`, `halo`) ; des papillons de nuit tournent autour (`moths`) ; la voisine lit son journal à sa lumière (`glowPaper` LE SOIR / NUIT ROUGE), un coup d'œil vers lui | 62 S03 |
| Porté raide comme une planche | deux ouvriers le portent à plat sur le dos (`lay` −π/2), au-dessus de leurs casques, bras levés ; caméra de côté et en plongée qui suit le porteur ; le maire, en costume clair, montre le trou du haut d'un feu vide | 62 S04 |
| La tête dans le feu rouge | sa tête seule (`headOnly`) remplit le trou rouge d'un feu tricolore (`headLight`), élargie au diamètre du trou ; elle surgit avec un dépassement ; carton FEU ROUGE | 62 S05 |
| La file qui pile à son rouge, puis plus fort | la file monte la rue et s'arrête voiture par voiture à sa lumière, nez qui plonge, petit rebond (`STOPS` ; `ts` fait démarrer le mouvement dans le plan) ; le rappel garde le cadre mais pile plus fort (`hard` 1,6), traces de pneus | 62 S06, S11 |
| Le soleil qui file au-dessus du feu | contre le ciel, le soleil traverse en arc et se couche dans le ciel libre pendant que la nuit tombe sur l'image ; ses yeux le suivent, son halo grossit, un clignement lent à la nuit | 62 S07 |
| Le klaxon qui aplatit le visage | camion de trois quarts face, deux trompes chromées, le chauffeur visible dans la cabine éclairée qui tire la corde (`cabLight`) : TUUUT ; coupe sur son visage poussé hors du trou et écrasé (tête [1,62, 0,6, 0,62]), grands yeux blancs (`eye` 1,1, `pupilSize` −0,45), joues qui ondulent, cheveux à l'horizontale (`wind`) ; retour lent puis rebond à 115 %, cheveux en bataille | 62 S08 |
| Vert de peur, trou par trou | le rouge vire à l'orange puis au vert (`skin`) pendant que sa tête descend du trou rouge au trou orange (tenu cinq images) puis au vert | 62 S09 |
| Toutes les voitures passent au vert | caméra basse à côté du feu : les voitures filent l'une après l'autre avec des traits de vitesse, ses cheveux fouettés dans le trou du bas, vert franc (`GREEN`, pas un vert pâle qui tourne à l'olive) | 62 S10 |
| Repeint en rouge au rouleau | un peintre sur une échelle passe le rouleau sur son visage vert : à chaque passage la couleur se rapproche du rouge et ses yeux se ferment ; puis il recule pour admirer, rouleau baissé, et le dernier clignement se voit | 62 S11 |
| La bouche de dessin animé qui avale | un poisson aux lèvres pincées (`bigMouth`) : la lèvre du bas descend comme un tiroir (`q.pos.jaw`), l'intérieur sombre apparaît, les lèvres grossissent (`mouth`), mâchoires ouvertes dix images au-dessus de ce qu'il mange, fermeture en deux images, le corps gonfle au-delà du rond et ondule (`wobble`), yeux fermés de plaisir (`bliss`) | 65 S12, S15 |
| L'onomatopée qui grandit avec le gag | même gag répété trois fois, mot différent et taille croissante : quatre petits MIAM, un GLOUPS, un énorme SCRONCH ; puis au rappel final un minuscule « miam. » en minuscules : la chute sèche | 65 S08-S19 |
| La bouche géante qui prend trois grains | une bouche haute comme un garage s'entrouvre lentement devant un fonctionnaire tremblant qui tend trois grains ; petite fermeture qui ne prend que les grains, il sursaute ; coupe sur le visage entier qui cligne de satisfaction | 65 S19 |
| Le panneau qui interdit l'absurde | un panneau officiel avec pictogramme barré (un poisson rouge barré, INTERDIT AUX POISSONS) planté par le maire : le gag se lit sans lire, et le mot du carton n'est pas répété | 65 S06 |
| L'araignée en élastique | le feu passe au vert sous elle : bond étiré, pattes écartées suspendue à son fil (`thread` à longueur clé), regard vers nous, clignement, chute, rebonds sur le fil | 66 S14 |
| Le déverrouillage qui grince | immobile depuis des années, il repart par à-coups : trois secousses du dos et du genou avec des craquements, puis le premier pas, la barbe qui balance, la poussière solide qui tombe de lui jusqu'au trottoir | 66 S16 |
| Le bras en guimauve | un policier tire sa main ; ses pieds restent plantés, seul son bras s'étire (`reach` hors de portée) : traction, glissade, traction ; la prise lâche, le bras revient en tremblant, le policier vole et s'écrase à plat, puis se regonfle | 66 S07 |
| L'amende plaquée sur la poitrine | le collègue claque une grande contravention sur sa poitrine : écrasement, puis mâchoire jusqu'au torse et yeux sur tiges vers nous | 66 S08 |
| La foule en fontaines | trois visages de trois quarts, deux jets de larmes en arc par visage (`tearFountain`), sanglots qui soulèvent les épaules, un mouchoir tordu, confettis qui pleuvent devant l'objectif (`confettiRain`) | 66 S17 |
| La tour de tasses qui monte à chaque gorgée (cycle 25) | `cupTower` (une tasse vide de plus à chaque aller-retour du bras, dépassement à l'apparition, la tour penche et oscille en grandissant) ; à chaque tasse un cran de plus : visage tiré vers `surprised` (`exprW`), yeux plus grands, pupilles plus petites, cheveux qui montent (`hairUp`) ; le bras fait dix allers-retours en 1,3 s (traînées) ; ding au dixième | 63 |
| La vibration en copies fantômes | canal `buzz` (environ 24 Hz, trois sinus incommensurables) sous le flou de bougé du plan (`blur` [[t0, t1, 0,016]], `blurSamples` 3) : trois copies nettes et décalées de lui (cinq faisaient une bouillie) ; dents serrées qui claquent (`mouth: 'clench'` + `tremble` : le croissant `teeth` se lisait comme un sourire), pupilles qui tremblent ; les tasses de la tour cliquettent l'une sur l'autre (`rattle`) ; VRRR ! | 63 |
| Le mur en gelée | `jellyWall` : d'abord le papier peint poussé en forme d'homme (`press` : tête, épaules, tasse, jambes ; une bosse ronde se lisait comme un ballon), qu'il crève ; il sort du mur sans le trouer ; des anneaux partent de son point de passage (`ripple`), poussent la paroi vers l'avant et la décalent sur le côté (`shear`) : la cimaise et le tableau peints dessus ondulent ; la vieille dame lève les yeux, revient à son thé, puis ses yeux sortent | 63 |
| La poignée de main qui transmet la vibration | la main du maire posée sur la sienne (`touch` ['@mec.handR', ...] : elle suit sa main qui tremble) ; le maire vibre plus fort que lui, cheveux dressés, cravate soulevée (`wind`), yeux exorbités, dents qui claquent ; EMBAUCHÉ | 63 |
| L'homme-marteau-piqueur | un ouvrier derrière lui le tient par les épaules comme des poignées (`touch` sur `@mecC.torso`) ; tous deux vibrent ; il s'enfonce droit dans la chaussée jusqu'aux genoux, des fissures partent en étoile par à-coups (`roadCracks`), des éclats volent ; le casque de l'ouvrier saute | 63 |
| Le front de taille qui recule | `metroTunnel` avec `faceMove` : de profil, il appuie les mains sur la roche qui s'effrite devant lui, petites bouffées de poussière pâle, les lampes s'allument derrière lui à mesure (`litFollow`) | 63 |
| Une nuit en coupe de terrain | `groundCut` : vue en coupe sous la rue de nuit, le tunnel file à travers l'image derrière lui, éclats de roche, lampes qui s'allument, une rame qui le suit déjà ; au-dessus la lune traverse le ciel, les fenêtres et les réverbères s'éteignent, l'aube monte, le soleil se lève | 63 |
| Le déca servi dans le tunnel | un serveur en veste, serviette blanche sur le bras, plateau haut sur la main, arrive derrière son épaule, petite courbette ; il prend la tasse (main sur `@serveur.handL`) et la lève devant lui, DÉCA tourné vers nous ; carte DÉCA | 63 |
| La rame en accordéon | `metroNose` (`crumple`, `stagger`, `rebound`, `foldShade`) : la rame lui rentre dans le dos et se plie tronçon après tronçon sur cinq images (d'un coup, c'était une coupe), dépasse et revient un peu, plis ombrés un sur deux, toit en tôle ondulée, pare-brise fendu, un phare pendu à son ressort ; lui ne bouge pas d'un millimètre, seul son casque saute ; SCRONCH ! | 63 |
| Les cous tendus vers le tunnel | sur le quai éclairé, les voyageurs penchés au-dessus de la voie tendent le cou à l'horizontale, cinq fois sa longueur, la tête restée droite au bout (`bend.neck` sixième valeur `lvl` : couchée sur le côté, elle se lisait comme une lampe de bureau), les yeux au niveau du tunnel ; au-dessus, le panneau compte les minutes jusqu'à « 3 427 MIN » de plus en plus vite et clignote ; BLOQUÉE | 63 |
| Les gobelets comme des cierges | dans le tunnel, la rame pliée derrière lui : des gobelets à emporter tout autour de ses pieds, deux de plus posés ; une voyageuse à côté de lui porte un gobelet à ses lèvres (`touch` sur `@mecC.head`) ; il boit ; sa paupière tressaute, son casque cliquette, la rame avance d'un pouce | 63 |
| Le pigeon qui se pose sur la tête | la créature `pigeon` vole jusqu'au sommet mesuré de son crâne (2,33 m pour `lemec` ; 2,5 m le laissait flotter devant une rambarde du fond), freine (`ease: 'out'`), et à l'impact sa tête s'écrase (`scl.head` à 74 %, 110 %, puis 100 %) pendant que le pigeon descend et remonte avec elle par trois clés `to` ; regard à nous et lent clignement ensuite |
| La barbe en fouet | `beardHair` avec `swing` et `whip` : chaque point de la mèche tourne d'un angle qui grandit vers la pointe et retarde sur elle, et le balancement s'éteint après sa fin (une rotation d'un bloc se lisait comme une faux figée) |
| Les yeux qui jaillissent sur tiges (créature) | `params.popAt: [t0, t1]` et `popLen` sur la clé de clip d'une créature : les yeux partent en avant sur des tiges de la couleur du corps, dépassent, vibrent et reviennent à t1 ; le papier tenu devant le corps sous les yeux, ils passent par-dessus |
| Le tableau des résultats à soixante pour cent | `resultsBoard` avec `pct` : la barre du gagnant s'arrête à `pct` %, celle des autres (rouge) prend le reste, les chiffres suivent (100 % / 0 % contredisait la réplique) |
| Le cadrage résolu par projection | quand la composition est dictée (sa tête en bas à droite, le feu dans le tiers gauche), chercher l'orientation et l'objectif qui posent deux cibles sur deux points de l'image (`projshot.solve`) au lieu de laisser `fitBack` cadrer tous les points au bord |
| La file vue au long foyer | lui au premier plan au bout de la file, les touristes en diagonale qui s'éloignent vers le fond, le photographe dans la rue devant sa porte, un enfant qui saute sur place dans la file, chacun avec un geste à lui |
| Le regard mené par les yeux (moteur) | une clé `look` fait d'abord partir les yeux (3 images), puis la tête tourne en douceur sur 0,3 s ; `lookDur` (0,06) pour un mouvement sec, comme dans les doubles prises |
| La musique d'attente qui coule du téléphone | `holdNotes` accroché à la tête près de l'oreille, tourné vers la caméra : des notes sortent sans fin, montent de côté en ondulant et s'effacent ; `until` coupe le flot net (le « clic » de la reprise d'appel) |
| Le téléphone collé à l'oreille | le téléphone passe de la main à la tête (`joint: 'head'`) : la main s'écarte et revient vide ; quand il tire à deux mains, sa tête s'étire de côté (`scl.head`) et revient d'un coup |
| La course poursuite qui ne finit pas | coureur et bus avancent à la même vitesse sur une route droite (`floorSlab`) avec la caméra qui dérive d'autant ; la chute renvoie au premier plan : le numéro du bus (21) n'était pas celui de son arrêt (12) |
| Le pull à l'envers | `knitJumper` accroché au torse avec `inside` : coutures pâles dehors, grande étiquette blanche qui dépasse du col ; `flipAt` le remet à l'endroit avec un écrasement ; tout le monde le copie, du bureau au président et au défilé |
| Le mauvais bouton sans regarder | il appuie sur le gros bouton rouge « 400 ANS » à côté du vert « 1 H » en regardant l'écran, puis nous ; insert par-dessus l'épaule : l'écran défile d'une heure à quatre cents ans, un tic à chaque palier, un « ding » à l'arrivée |
| Le ticket qui ne s'arrête pas | `ticketRibbon` posé à la fente : le papier sort, s'enroule jusqu'au trottoir et file le long d'un chemin jusqu'au point de fuite (vue d'avion : bande élargie à 0,22 m pour se lire à cent mètres) ; les marques imprimées avancent avec le papier, la tête se soulève et frémit |
| La voiture devenue maison | `carHome` posé sur la voiture : rideaux vichy noués, tuyau de poêle qui fume, géranium et antenne sur le toit, paillasson BIENVENUE, courrier glissé sous l'essuie-glace (`letterAt`), linge tendu jusqu'à l'horodateur |
| Le visage écrasé contre la vitre | caméra dans la cabine de la fourgonnette garée à côté, à travers sa fenêtre ouverte : sa tête aplatie contre sa propre vitre (`scl.head` [1,16, 1,1, 0,6]), les deux mains à plat, puis il glisse vers le bas en grinçant |
| Le pays entier tondu | `mowFrance` (props_tondeuse) vu de très haut : la silhouette de la France en vert non tondu sur la mer, des bandes claires et foncées qui la balaient du nord au sud, bande après bande, derrière une tondeuse rouge et son sillage ; un damier de champs carrés ne se lisait pas à 165 m |
| La forêt en ligne droite | caméra de poursuite derrière et au-dessus de la tondeuse : les arbres devant elle tombent à gauche et à droite au moment où elle les atteint ; de face, les arbres qui tombaient la cachaient |
| La moustache qui part seule | créature `moustache` avec `sheen`, bras courts et fins finis par des gants blancs (`hand: 'glove'`, `handW`) : elle se lit comme une moustache vivante, pas comme une araignée à quatre pattes ; nœud papillon sur un col blanc (une cravate sous la moustache se lisait comme une langue) |
| La carrière qui monte | à chaque échelon plus haut, la créature est plus grande dans le cadre et l'action plus franche : sur les échelons les plus hauts (ministre, président), cadrer bas et serré, à plus de la moitié de la largeur |
| La bouchée qui reste bouche fermée | après le claquement des mâchoires, `gulp` avec `bliss` long (jusqu'à la coupe) : les yeux fermés en arc, la bouche close, le corps qui gonfle et oscille ; les déplacements du poisson pendant ce temps glissent (`glide=True`), sinon le geste repart et la bouche se rouvre |
| Le bouchon qui retombe pile dans le verre | deux plans dans le même plan narratif : un insert de 0,3 s par-dessous sur le trou du plafond où le bouchon dépasse et tremble, puis un plan serré au-dessus du verre posé sous le trou : le bouchon tombe du haut du cadre dans le verre (PLOUF), le vin saute au visage penché sur le côté (jamais au-dessus du verre : la tête serait sur la trajectoire). Un seul plan « trou + verre » oblige à un cadre large où le verre fait 7 % de la largeur |
| La moustache qui cache ses pattes | sur la lèvre, la créature tient le clip `pose` (jambes et bras repliés vers l'arrière, dans le visage) : ce n'est qu'une moustache jusqu'à l'ouverture des yeux ; les pattes sortent au milieu de la chute (`airborne`), elle s'aplatit à l'atterrissage puis regonfle un peu plus grosse (clé `scale`) ; la caméra la suit vers le bas jusqu'au bord du lavabo, elle de face et grande |
| La pièce vide derrière la porte | `door` avec `inside: 'empty'` : en s'ouvrant, la porte montre une pièce nue éclairée par une ampoule au bout de son fil (un appartement qu'on vient de trouver), au lieu du fond noir du modèle |

- (cycle 40, « Le bocal ») Escalade « moyens énormes contre petit objet » : chaque tentative casse le moyen, jamais l'objet (la cuillère se tord, la
  pince hydraulique éclate, le char crève, les astronautes partent en toupie, le laser revient sur le savant) ; le retournement vient de la personne
  la plus modeste (la grand-mère, d'une pichenette : POP), la chute est sèche (il n'aime pas les cornichons).
- (cycle 40) Caméra cachée dans un meuble (sous le canapé, dans le frigo) : la poser dans le volume libre avec `inside=(...)` à ses bornes et
  `lenses=range(26, 86)` ; ne cadrer que le visage (les bords de l'ouverture font le cadre, ils n'entrent pas dans les points du cadrage) ; la tête doit
  tenir dans l'interstice (frigo plein : étagères à 0,81 et 1,21 m, donc personnage à genoux, tête vers 1,0 m).
- (cycle 40) Robinet qui coule : `islandSink` + `tapStream` posé à la bouche du robinet (0, H + 0,26, −D/2 + 0,22 dans le repère de l'évier), longueur
  jusqu'au couvercle ; la vapeur en trois petits `dustPuff` blancs au-dessus des mains (posés sur les mains, on voyait des boules blanches).
- (cycle 40) Cadrage calculé avant le rendu : `story_kit.project(frm, look, lens, point)` donne la position d'un point à l'écran ; s'en servir pour
  mettre une étiquette au-dessus des sous-titres et des pieds hors de la bande 0,77-0,86 sans passer par des images de contrôle.
- (cycle 40) Accessoire tenu qui doit se lire (cuillère, outil) : un accessoire libre animé avec les mêmes clés que la main (`to` aux mêmes instants)
  plutôt qu'un accessoire attaché dont l'orientation dans le poing est inconnue ; la cuillère pend la tête en bas au-dessus du couvercle.
- (cycle 40) Clignement, coup d'œil ou grimace pendant que les mains tiennent quelque chose : `k(t, toon={'face': {...}}, keepPose=True)`. La clé
  reprend la pose de la clé précédente de l'acteur (reach, touch, hands, bend) et ne change que ce qu'elle nomme ; un clignement écrit avec le seul
  visage faisait retomber les bras (« Le robinet », « Le centime »). Les fonctions BLINK des scripts l'emploient.

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
- (cycle 22) Un accessoire tourné vers la caméra (`face='camera'`) pivote autour de son origine : une trajectoire calculée à l'intérieur de
  l'accessoire tourne avec lui et part ailleurs. Le faire voler avec des clés de déplacement (`to`, `dur`) en coordonnées du monde.
- (cycle 22) Des décalages de visage seuls (`cross`, `eyeL`, `browL`, `tongue`…) posés sur les paupières lourdes du mec : la grimace se lisait
  comme son air blasé habituel (59). Les poser sur une expression peinte (`'expr': 'grimace', 'exprW': 0.9`) ; une base différente par
  figurant (`angry`, `disgusted`, `shocked`, `suspicious`, `scared`) varie une foule de grimaces.
- (cycle 22) Une main sur l'oreille donnée dans le repère de la tête (`['head', 0.9, 0.55, 0]`) : ce repère compte en mètres, la main partait
  presque un mètre au-dessus de la tête et le bras se dressait (60 : « mains sur les oreilles » devenues bras levés). Utiliser le repère du
  visage : `['face', ±0.58, 0.55, -0.06]` (juste derrière le bord du visage, à hauteur des yeux).
- (cycle 22) Un panneau en `canvasPlane` (double face) vu de dos se lit en miroir (« SOMMET » à l'envers). Deux plans dos à dos en face avant
  seulement, ou orienter le panneau vers la caméra.
- (cycle 22) Grossir les pupilles avec `'pupil'` dans `face` : ce canal ne règle que les yeux sortis sur tiges ; les yeux peints lisent
  `'pupilSize'` (0,5 = moitié plus grandes, en plus du `pupil` du script). Des pupilles de 3 px disparaissaient sur un téléphone (58, 59).
- (cycle 22) Des accessoires placés dans le monde autour d'un personnage qui respire et se balance (lettres qui tombent dans sa bouche) :
  ils passent à côté et derrière lui (58 : les lettres sur le revers). Les accrocher à son articulation (`on: {actor, joint: 'head'}`) et les
  animer dans ce repère (accessoire `slotLetters`).
- (cycle 22) Un portrait d'un personnage dessiné à la main (la photo d'identité de 59) ne lui ressemble pas : yeux ronds, sans barbe. Le faire
  peindre par son propre rig facial (`makeFaceRig` + `faceState`, avec les mêmes décalages de visage que le script).
- (cycle 22) `'hat': 'cap'` dans la distribution : ce chapeau n'existe pas (liste `HATS` de `engine/human.js`) et rien ne s'affiche, sans
  erreur (60 : le fermier sans casquette, son envol prévu impossible). Une casquette = `'maocap'` avec `'hatColor'`. Vérifier le nom dans
  `HATS` avant de bâtir un gag sur un chapeau.
- (cycle 22) En look naturel, une nuit (`'night': True`) est éclairée comme le jour : `setupLights` remet le soleil à 3,0 et chaud quel que
  soit le préréglage de nuit (60 : chaussée de nuit à 92 contre 89 de jour, seul le ciel noir). Donner au plan son propre réglage
  `look={'sun': 0.3, 'sunColor': '#9DB4EC', 'fill': 0.75, 'exposure': 0.9}` et des réverbères avec `'light'` et `'pool'`.
- (cycle 22) Un personnage aplati (`'lay'` + `'sq'` à 0,04 en profondeur) posé à y = 0 : la crêpe tient dans ±1 cm autour du sol et le
  trottoir est à 6 mm, elle disparaît dedans (60 : seuls la cravate et les jambes, la tête et les bras en pointillés). Le soulever de 4 cm
  par une clé de position pendant qu'il est à plat, le reposer au moment où il se relève.
- (cycle 22) Filmer de profil « pour que la mâchoire se voie » ou « pour que les tiges des yeux sortent » : le côté d'une tête-boîte n'a pas
  de visage peint et se lit comme l'arrière de la tête (l'audit le signale). Rester de trois quarts (45° au plus), ou tourner le personnage
  vers nous par le canal `'yaw'` au moment où l'on doit voir son visage.
- (cycle 22) Un « sommet » de 3 m sur un pré entouré de chaînes de 30 m : un rocher dans une vallée (60). Bâtir la montagne sous lui
  (accessoire `summitPeak`, 14 m), garder les chaînes autour de l'horizon (`h` 19 à 80 m) et montrer le fond de la vallée (rivière, village).
- (cycle 22) Une main en cornet derrière l'oreille du côté opposé à la caméra : on lit « il se gratte la tête ». Prendre la main et l'oreille
  du côté caméra, et décoller l'oreille sur le ciel.
- (cycle 22) L'onomatopée d'une gifle (PAF) posée près de la tête de celui qui frappe : c'est lui qui semble frappé (60, deux fois). La poser
  là où la main touche, sans couvrir le texte de l'affiche.
- (cycle 22) Un mot qui s'envole « loin sur la vallée » filmé de face ou de profil : il sort du cadre en un tiers de seconde et le reste du
  plan montre une vallée vide. Couper sur une caméra par-dessus l'épaule qui le regarde rapetisser jusqu'à la fin du plan.
- (cycle 22) `fitBack(level=False)` avec une caméra basse qui regarde en l'air : en reculant sur la ligne 3D elle passe sous le sol
  (y = -0,09). Garder `level=True` pour une contre-plongée.
- (cycle 23) Un bras qui « montre le fond de la rue » filmé par une caméra qui regarde déjà dans cette direction : il est dans l'axe de
  l'objectif et disparaît (59). Faire traverser l'image au bras, perpendiculaire à l'axe, et laisser la main sortir par le bord.
- (cycle 23) Les clés `toon` sont des états complets : une petite clé de frisson posée juste après une pose d'appui (paumes sur les joues)
  efface l'appui. Placer les clés secondaires avant la pose, ou répéter la pose dedans.
- (cycle 23) Un écrasement sur un siège pivote sur l'origine de l'acteur, au sol : le personnage s'enfonce à travers l'assise jusqu'au
  trottoir (61, quatre fois). Le soulever pendant l'écrasement de ce que celui-ci retire à la hauteur de ses hanches, environ
  0,47 × (1 − sq_y) assis, avec une clé `to` en `clip='sit'`.
- (cycle 23) Un écrasement du corps entier écrase aussi les yeux en fentes au moment même où ils doivent sortir : étirer la tête contre
  l'écrasement (`scl.head` [0,84, 1,28, 0,84]) et grossir les yeux (`eyeScale` 1,7).
- (cycle 23) Un personnage aplati vu exactement de dessus se lit comme un personnage debout (60) : filmer la crêpe de trois quarts en
  plongée depuis ses pieds, bras écartés au sol (`reach` sur des points du trottoir) ; le visage reste à l'endroit.
- (cycle 23) Des mains en porte-voix pendant que la mâchoire s'étire : la touche `face` suit la tête non étirée, les mains couvrent la
  bouche et le haut du visage. Jeter les bras en avant et en dehors avec le cri.
- (cycle 23) Un mot qui grossit pendant qu'il s'éloigne ne rapetisse presque pas : garder sa taille et l'envoyer à 40 m.
- (cycle 23) Un petit mot jaune ou orange sur une peau orangée disparaît (contraste 1,3:1) : le blanc cerné de foncé, et un trajet à côté du
  visage, pas devant les yeux.
- (cycle 23) Un « gros plan » dont les points de cadrage comprennent le point de départ d'un objet qui tombe devient un plan moyen : laisser
  l'objet entrer par le bord du cadre.
- (cycle 23) Le rig toon ignore `build.height` : un enfant à 83 % de sa mère se lit comme un petit adulte. Le faire avec `act(..., scale=0.62)`
  et lui donner sa propre tête (un bonnet).
- (cycle 23) Une main en cornet derrière l'oreille se lit comme un grattage de tête, même grosse, même du côté caméra : faire grandir l'oreille
  elle-même (`earScale`, avec le creux sombre qui apparaît au-delà de 1,25).
- (cycle 23) Dans un insert sur un formulaire posé à plat, la ligne qui porte la chute est la dernière, donc en bas du cadre, dans la bande
  des sous-titres : filmer plus haut et plus raide pour la remonter vers 60 % de la hauteur, avec 10 % de marge sur les côtés.
- (cycle 23) Une flèche de vitesse cernée de foncé, debout entre un siège et le trottoir, se lit comme un pied de banc : des traînées douces
  en coin (`speedLines` `soft`, `taper`, `alpha` 0,6) à côté du personnage, pas sous lui.
- (cycle 23) Un nid posé au-dessus de la tête par sa position dans le monde flotte dès que la tête bouge : l'attacher à la tête (`on` …
  `joint: 'head'`) avec la cuvette sur les cheveux, et poser les pigeons sur ses bords pour qu'ils ne le cachent pas.
- (cycle 23) « Arrêté en plein vol » à 4 m au-dessus de la rue, filmé à sa hauteur : la rue derrière ses jambes, il semble debout. Le monter
  plus haut et le filmer d'au-dessus, la rue loin en dessous, ou d'en dessous sur le ciel.
- (cycle 24) La couleur de peau (`skin`) multipliée sur le matériau de la tête teignait aussi le blanc des yeux : un œil ouvert disparaissait
  dans un visage rouge. Le moteur teinte désormais le visage peint sous le dessin des traits (`extras.tint`). Vérifier l'œil ouvert en image
  de contrôle à chaque nouvelle couleur.
- (cycle 24) Les mains faites de doigts n'étaient pas des pièces de peau : un coup de soleil s'arrêtait aux poignets. Toute nouvelle pièce de
  corps doit être marquée pour les canaux de peau (`skinPart` ou `fingerSkin`).
- (cycle 24) `eyeScale` n'agrandit que des yeux sortis de leur orbite (`pop`). Sans `pop`, il ne fait rien : une prise aux « yeux
  exorbités » restait aux yeux en fente. Pour un œil peint plus grand, `eye` (0 à 0,9). Pour des yeux qui jaillissent, `pop` avec de
  courtes tiges (`popLen` 0,05).
- (cycle 24) Une tête qui doit apparaître dans un trou d'accessoire : mesurer la tête dans le moteur (`debugJoints`), parce que son centre
  n'était pas là où la taille le laissait croire. Couper le balancement au repos (`hip` 0), qui faisait glisser le visage de 8 cm hors du
  trou. Élargir la tête (`scl.head`) pour remplir un trou rond.
- (cycle 24) Une boîte ouverte à l'arrière montre le ciel par ses trous : lui mettre un fond sombre.
- (cycle 24) De petits accessoires éclairés prennent la couleur de la lueur voisine : dans une lueur rouge, des papillons de nuit devenaient
  des bouts de papier rouge. Pour ce qui doit rester pâle, un matériau non éclairé.
- (cycle 24) Le vent propre d'un personnage (`wind`) se donne dans son repère, +Z devant lui. Un souffle qui vient d'en face pousse donc
  vers -Z : en +Z, la cravate passait à travers la vitre devant lui.
- (cycle 24) Le cadre vertical est trois fois plus étroit que haut. Une voiture et un feu côte à côte, à deux mètres l'un de l'autre, ne
  tiennent ensemble qu'à neuf mètres. De près, de derrière, de côté ou d'en face, la voiture remplissait l'image : aligner les deux sujets
  en profondeur (un long foyer dans l'axe de la rue) ou les montrer dans deux plans.
- (cycle 24) Un mot qui doit « remplir l'image » doit voler dans l'axe de l'objectif, vers lui. Lancé à hauteur de la tête, il sortait par
  le haut du cadre à la moitié de sa taille.
- (cycle 24) Un objet qu'on claque sur quelque chose (une affiche sur un mur, une amende sur un front) se porte dans la main qui frappe et
  reste là où la paume se pose. Apparu sous une main vide, il se lit comme une erreur de montage.
- (cycle 24) Une tête frappée qui part en arrière dans les quatre images du contact emporte avec elle ce qu'on y colle, et la main reste
  dans le vide : la tête s'écrase sous la paume trois images, la main s'en va, et c'est seulement ensuite que la tête repart.
- (cycle 24) Les cheveux dressés (`hairUp`) font d'un chignon la brosse du héros : 0 pour un personnage dont la coiffure est la silhouette.
- (cycle 24) Une oreille agrandie en gardant la forme d'une boîte se lit comme une planche. Une coupelle (bol, creux sombre, bord, repli) se
  lit comme une oreille.
- (cycle 24) Une planche vue de face ressemble à un homme maigre. Tournée de chant vers l'objectif, c'est une ligne, et le POP qui suit lui
  rend tout son volume.
- (cycle 25) Une caméra placée au-delà d'un accessoire qui ferme le décor (le front de taille d'un tunnel) est dans la roche : image noire
  (63). Garder la caméra derrière le plan de ce qui ferme le décor, et les rochers d'un front au bord de la galerie, pas au milieu.
- (cycle 25) Un plan à deux en travers d'un tunnel de 4,8 m ne tient pas dans une image verticale : objectif de 80° ou caméra dans le mur.
  Filmer dans l'axe du tunnel, le second personnage qui arrive derrière l'épaule du premier, et allonger le décor pour reculer (63).
- (cycle 25) Un flou de bougé de 0,022 s sur un plan moyen change la vibration en bouillie : 0,01 à 0,016 s, et seulement pendant la
  vibration (le flou s'arrête à l'image où il s'arrête net).
- (cycle 25) Des bouffées de poussière opaques et grises autour des pieds se lisent comme des rochers (63) : les retirer, laisser les éclats.
- (cycle 25) Un témoin qui regarde quelque chose derrière lui montre sa nuque (la vieille dame tournée vers le mur, 63) : le placer de trois
  quarts entre la caméra et ce qu'il regarde, le visage vers nous quand il le voit.
- (cycle 25) Une passante qui tend un gobelet à ses lèvres en se plaçant devant lui le cache entièrement (63) : à côté de lui, du côté
  opposé à la caméra, le bras en travers.
- (cycle 25) Un homme assis aux cheveux dressés dépasse du haut du cadre même quand l'audit le croit debout : mettre dans le cadrage un point
  au sommet des cheveux (2,3 m pour un homme assis à `hairUp` 1).
- (cycle 25) Un rendu HyperFrames refuse de partir sous 1 Go de disque libre (« Low disk space ») : vider d'abord le cache d'extraction
  d'images (`/tmp/hyperframes-extract-cache-0/hfcache-*`), puis relancer à partir de la couche 3D déjà calculée.
- (cycle 25) `face.mouth: 'flat'` n'existe pas : la bouche disparaît (62, « pas de trait de bouche du tout »). La bouche droite s'appelle
  `line` (et `line_m6`, `line_p6`... pour une courbe légère).
- (cycle 25) Le canal `eye` agrandit l'œil peint mais garde les paupières lourdes de l'expression de base : sur un visage blasé, des yeux
  « grands ouverts » demandent `expr: 'surprised'` avec `exprW` vers 1 (63).
- (cycle 25) Un cou étiré (`bend.neck` étirement 4) qui plie vers l'avant fait des gens qui saluent : pour « tendre le cou », le plier sur
  le côté vers ce qu'on regarde et viser le regard à hauteur des yeux (visé vers le sol, les têtes tombaient, 63).
- (cycle 25) En recopiant un dossier de revue pour le tour suivant, changer aussi la phrase du tour dans le script qui écrit les consignes
  des critiques (build.sh), pas seulement le brief : la revue 3 de 61 s'est appelée « deuxième revue » dans la consigne.
- (cycle 25) Un visage dans un trou de feu tricolore : tout ce qui n'est pas la tête se voit par les trous et les parois au moindre
  écrasement ou saut (chemise, jambes, mains). Canal `headOnly` : la tête seule (62).
- (cycle 25) `hops_ball` atterrit `hold` secondes avant le décollage suivant (atterrissage n° i à t0 + dt × i − hold) : un événement calé
  sur l'ancien atterrissage (`hops`, à t0 + dt × i) tombe au décollage. La gifle de 61 frappait un homme déjà étiré en l'air. Recaler
  chaque gifle, son ou réaction, et allonger `hold` pour tenir l'écrasement sous la main (0,1 s = trois images).
- (cycle 25) Un sommet de saut au ras du bord d'un accessoire se lit comme un appui : ses semelles arrêtées pile au haut du dossier, il
  semblait debout dessus (61). Dépasser le bord d'au moins un tiers de la hauteur du corps, ou décaler la caméra pour décoller les deux.
- (cycle 25) Une main posée sur le torse (`touch` ['torso', ...]) se compte dans les unités du torse, écrasement compris : à 0,6 sur le côté,
  les bras écrasés partaient à hauteur de taille, paume en l'air, et reprenaient le geste du plan d'avant (61). Pour un sursaut, les mains
  montent à côté de la tête (`touch` ['head', ±0,4, 0,3, ...]).
- (cycle 25) Un bras qui va chercher un objet du côté opposé barre la poitrine comme une écharpe (61, la tasse) : prendre l'objet avec la
  main du côté où il se trouve à l'image, ou déplacer l'objet.
- (cycle 25) Un accessoire qui tremble en pivotant sur son pied (`headLight` `shake`) déplace son sommet bien plus que prévu : 0,08 rad
  font 27 cm de côté au trou du haut, à 3,4 m, alors que la tête de l'acteur reste en place. L'intérieur noir du boîtier apparaissait et
  son oreille dépassait (62). Calculer le tremblement à la hauteur de ce qu'il contient (quelques centimètres) ou y attacher l'acteur.
- (cycle 25) Les yeux sur tiges (`face.pop`) suivent l'écrasement de la tête : avec `scl head` [1,7, 0,7, 0,5], leur pupille s'étale en
  une grande tache noire sur la moitié du visage (62). Pas d'yeux sur tiges sous un écrasement non uniforme ; agrandir les yeux peints
  (`eyeScale`) à la place.
- (cycle 25) Le panneau du visage peint n'est pas éclairé (matériau de base, sans émission) : une lueur posée en émission ne change rien.
  La lueur de la peau (`skin.glow`) éclaircit maintenant sa couleur au-delà du blanc, les traits restant noirs. Un visage qui doit être la
  chose la plus chaude de l'image la nuit demande aussi une teinte pâle (rose-blanc) et un halo moins fort que lui (62).
- (cycle 25) `look: 'camera'` suit la caméra active : dans un plan à deux caméras dont l'une est derrière le personnage, sa tête se tourne
  vers elle et reste tournée quelques images après la coupe (62, ses cheveux plein le trou du feu). Fixer un point de regard devant lui.
- (cycle 26) Correction de l'entrée précédente : `eyeScale` et `pupil` ne règlent que les yeux sur tiges. Sur le visage peint, c'est `eye`
  (0,4 = 40 % plus grand) et `pupilSize` (−0,45 : pupilles en tête d'épingle). Une tête écrasée en hauteur écrase aussi les yeux peints :
  avec `scl head` [1,62, 0,6, 0,62], il faut `eye` 1,1 pour qu'ils restent de grands yeux blancs (62).
- (cycle 26) Un retour rapide après une poussée en avant fait déborder la suite du mouvement : la tête, poussée de 0,2 m hors du feu puis
  ramenée en 0,06 s, est partie 0,25 m derrière le boîtier, et le trou est resté noir quatre images (62). Pousser moins (0,12 m), revenir
  en 0,14 s (`inOut`) et vérifier la position de la tête image par image avec `debugJoints`.
- (cycle 26) Un personnage placé dans un volume plein ne se voit pas à travers une vitre transparente : la vitre montre la face du volume
  derrière elle (le chauffeur dans une cabine pleine : un panneau bleu clair, 62). Faire la cabine en coque ouverte derrière la vitre,
  avec un fond sombre et une lumière dedans (`truck` `cabLight`).
- (cycle 26) `lens` est l'angle de champ vertical en degrés, pas une focale : 34 donne 34° en hauteur et 19,5° en largeur en 9:16. À 6 m,
  un boîtier de 0,6 × 1,6 m prend déjà un quart de la largeur ; un rappel « plus près » a mis le dos du feu en grand carré rouge (62).
  Calculer le cadre avec ces angles avant de rendre.
- (cycle 26) `FC` (fitBack) cadre la hauteur entre `top` et `bottom` : un sujet couché plus large que l'image au recul choisi sort par les
  côtés (le visage du porté coupé au bord droit, 62). Mettre l'extrémité qui compte (la tête) dans les points, faire suivre la caméra
  (`drift`), ou tourner le sujet dans l'axe de l'image.
- (cycle 26) Un gris moyen (#6B6E76) sous le ciel bleu du look naturel se lit bleu marine, comme le costume du héros : le maire passait
  encore pour lui (62). Pour séparer deux personnages, changer de valeur et de chaleur (gris clair chaud #A9A397, cravate bordeaux), pas
  seulement de teinte.
- (cycle 26) La fin d'un arc (soleil, lune, objet lancé) doit tomber dans le ciel libre de ce cadre-là : le soleil qui se couchait à gauche
  passait derrière le boîtier du feu (62). Vérifier la dernière position contre la caméra ; si le ciel libre est de l'autre côté, inverser
  l'arc, et le regard qui le suit avec.
- (cycle 26) Un remplacement scripté qui ajoute un commentaire `#` au milieu d'une ligne avale la fin de la ligne (quatre fois en deux
  histoires). Le script de correction refuse maintenant un commentaire si le texte remplacé ne termine pas sa ligne.
- (cycle 26) Un rappel filmé dans le même cadre ne vaut que si l'action monte (plus dur, plus vite, dans le plan) : la file qui s'arrêtait
  avant la coupe se lisait comme une image figée (62). La construction signale maintenant une caméra reprise d'un plan précédent.
- (cycle 27) L'échelle d'un accessoire est un seul nombre : une liste comme [1,5, 5,4, 1,5] ne dessine rien du tout (la barbe de 66). Pour une
  forme non uniforme, ajouter `flat` [x, y, z] par-dessus l'échelle. Cela marche maintenant aussi sur un accessoire porté.
- (cycle 27) Un accessoire porté garde sa propre taille (l'échelle du porteur est divisée), mais son décalage se compte dans le repère mis à
  l'échelle de l'articulation. Sur un poisson à l'échelle 62 (65), une casquette à 0,7 faisait 17 cm et un décalage de 0,1 la mettait à 6 m.
  Pour une créature géante, poser l'accessoire dans le monde avec des clés qui la suivent, ou lui donner la taille de la créature.
- (cycle 27) La nageoire caudale d'un poisson dépasse son corps d'environ la moitié de sa longueur : le poisson géant de la piscine débordait sur
  la plage devant le panneau (65). Garder son centre à une longueur de corps du bord de ce qui le contient.
- (cycle 27) La construction mesure les créatures à la hauteur d'un homme : ses alertes « tête coupée par le haut » et « petit sur téléphone »
  sont fausses pour des canards, une moustache ou un poisson géant. Juger ces cas sur les images.
- (cycle 27) Vue exactement de côté, une tête-boîte ne montre aucun visage : le poteau léché, le front de taille, les voyageurs qui regardent le
  tunnel (63, 64). Pour un gag qui passe par le visage, filmer de trois quarts face, ou tourner la tête vers un point entre la cible et la
  caméra ; quand le profil est inévitable, des yeux sur pédoncules se lisent encore.
- (cycle 27) Un lien qui se rembobine alors que tout reste en place dessus ne montre rien en plan serré tant que son bout n'arrive pas, quatre
  images avant la fin (64). Avec `reel`, les ampoules glissent dans la bouche dès la première image.
- (cycle 27) Dans la fenêtre de flou d'un plan, tout ce qui bouge se brouille. Une main qui tient un gobelet contre une tête qui vibre
  (`touch` '@id.head') tremblait avec elle et devenait une traînée violette (63). Retirer la main avant l'ouverture de la fenêtre.
- (cycle 27) Assombrir une nuit après coup (`dark`) écrase tout vers le noir, lumières comprises, et laisse la première image non étalonnée
  (64). Construire la nuit avec un fond froid et de vraies lumières : les ampoules, plus des lumières colorées qui changent sur le temps.
- (cycle 27) La bouche 'teeth' (un croissant de dents relevé) se lit comme un sourire sous des yeux grands ouverts (63). Pour des dents qui
  claquent, prendre 'clench' (une barre plate).
- (cycle 29) Une expression peinte poussée à 85 % (`exprW` 0.85) garde 15 % de l'expression du plan : la paupière d'un « impassible »
  reste en trait sur un œil, et des yeux « survoltés » ont l'air sceptiques (63). Pour une expression franche, `exprW` 1.0.
- (cycle 29) Une vibration latérale sous le flou de mouvement aligne les copies fantômes des deux yeux en une paire de lunettes (63).
  Réduire la part latérale sur le personnage dont on doit lire le visage (`buzzXZ` 0.45) et la reporter en haut et en bas (`buzzY`).
- (cycle 29) Une forme qui pousse un mur doit avoir la silhouette du personnage (tête-boîte, mèches, accessoire) et durer six à huit
  images : une bosse ronde de quatre images se lit comme un fantôme ou un bonhomme de neige (63).
- (cycle 29) Un panneau ou un tableau qui porte le gag ne doit pas tomber dans le bandeau du titre : le carton le recouvre au moment
  où le compte grimpe (63). Le placer juste sous le bandeau (19 à 26 % de la hauteur).
- (cycle 30) Une facture qui se déroule (`billScroll`) a son pivot au bord du haut : posée au sol, elle pend sous le plancher et ne se
  voit pas (68). La placer à la hauteur des mains.
- (cycle 30) Des fissures épaisses et peu nombreuses autour d'un trou au plafond se lisent comme une araignée (68) : plus nombreuses
  et plus fines.
- (cycle 30) Une télé dont le gag est l'écran doit montrer l'écran : de dos, le passage de la neige à l'image nette n'existe pas (68).
  La tourner vers la caméra et vers ceux qui la regardent, de côté dans le cadre.
- (cycle 30) Le fond de la salle de presse répète ses mots en grand : un mot long se chevauche lui-même (67, 68). Un seul mot et
  `fontScale` 0.55.
- (cycle 30) La zone dégagée d'une rue (`clear`) ne couvre que les abords : un lampadaire à vingt mètres sort encore de la tête d'un
  personnage cadré de face dans l'axe de la rue (64). L'étendre loin derrière lui.
- (cycle 30) Une créature petite filmée de loin au sol est un point à l'écran (67) : la filmer à sa hauteur et de près, ou faire du
  premier plan un gros plan sur l'endroit où elle naît.

- (cycles 27-28) La mâchoire d'un nageur articulée derrière la surface de son corps rentre dans le ventre en s'ouvrant : aucun gobage ne
  se voyait (65). Mettre les lèvres devant le corps, faire descendre la lèvre du bas (`q.pos.jaw`) et montrer un intérieur sombre.
- (cycles 27-28) Les créatures ignoraient les canaux `lay` et `sq` des clés `toon` (réservés aux humains) : les canards « renversés » ne
  bougeaient pas (65). Ils sont pris en charge depuis ; un nageur tourne et s'écrase autour de son corps (`pivotY`), pas du point sous lui.
- (cycles 27-28) L'élan d'un gobage (`root.z`) grandit avec l'échelle : à 62, il avançait le poisson de huit mètres, jusque dans la caméra
  (65). Mettre `lunge` à 0 et déplacer l'acteur soi-même pour que la bouche arrive pile sur sa cible.
- (cycles 27-28) Deux accessoires du même nom dans deux modules : le dernier fusionné gagne. Les confettis « en boîte » étaient remplacés
  par une gerbe d'un seul confetti (66). Vérifier le nom avant de s'en servir.
- (cycles 27-28) La taille des gouttes de `waterDrops` est `r` (pas `s`) : les éclaboussures faisaient deux centimètres à trente mètres (65).
- (cycles 27-28) Un objet opaque dans un bocal transparent est délavé par les couches de verre et d'eau (le poisson orange passait crème) :
  le dessiner après elles (`renderOrder`, matériau transparent à opacité 1).
- (cycles 27-28) Le décalage d'un accessoire posé sur une articulation de créature est dans les unités de l'articulation (avant l'échelle de
  l'acteur) : une casquette décalée « en mètres » partait à des centaines de mètres au-dessus du poisson (65).
- (cycles 27-28) Un char dont l'avant est +Z, roulé vers nous avec `ry` 180, roulait à reculons : canon caché derrière la tourelle (65).
- (cycles 27-28) Le mot du carton répété sur un panneau et dans la légende (FERMÉE trois fois, AMENDE) : écrire autre chose sur l'objet
  (INTERDIT AUX POISSONS, CONTRAVENTION).
- (cycles 27-28) La nuit, la sonde de lumière capte la neige éclairée et rallume les façades comme en plein jour (64) : baisser `probe` et
  `hemi` dans le look de nuit, et poser des flaques de lumière chaude sous les lampadaires.
- (cycles 27-28) Une barbe faite de lattes plates régulières se lit comme un râteau ou des rayures de pantalon (66) : des mèches effilées qui
  ondulent, plus pleines au menton, deux tons, bombées pour passer devant la poitrine, la pointe enroulée au sol.
- (cycles 27-28) Les rôles d'un dossier de critique recopiés d'une autre histoire emportent la liste de gags de cette autre histoire (64) :
  écrire les rôles pour chaque histoire.
- (cycles 31-33) Une caméra basse devant une clôture de jardin ne montre que des piquets : le pied de la tondeuse, les jambes, le nain
  disparaissent (70). Mettre la caméra dans le jardin, ou retirer la clôture du plan (`pavillon` : `fence: False`, `mailbox: False`).
- (cycles 31-33) Une caméra près du portail se retrouve avec la boîte aux lettres rouge en premier plan (70) : vérifier ce que le décor pose
  autour du point de départ de la caméra avant de la reculer (`fitBack` recule le long de l'axe de visée).
- (cycles 31-33) Filmer « sous le canapé » est impossible si son socle va jusqu'au sol : la caméra était dans le tissu, image toute verte
  (69). Canapé sur pieds (`sofaProp` : `legs`), caméra dans l'espace libre, personnage à quatre pattes (`crawl`) pour que sa tête passe
  sous la ligne du socle.
- (cycles 31-33) Une caméra dans un frigo plein se retrouve dans un carton (69) : la placer au-dessus de la nourriture de l'étagère du haut.
- (cycles 31-33) Un accessoire posé au niveau du sol (lit de rivière vidée, flaque, tapis) passe sous le sol du décor et devient de l'herbe
  (69) : le relever de quelques centimètres.
- (cycles 31-33) Un enfant qui « montre la tête » d'un adulte avec `reach` sur la tête étire son bras en bâton rouge (69) : bras levé
  au-dessus de sa propre tête, la cible à sa portée.
- (cycles 31-33) Le bureau du décor `mairie` cache tout ce qui se tient derrière lui (69 : le chèque géant) : `desk: False` pour une
  estrade ou une salle de cartes.
- (cycles 31-33) De grosses lunettes « relevées » à hauteur du front se lisent comme portées (69) : les poser sur le dessus du crâne,
  inclinées vers l'arrière (`rot` sur l'accessoire attaché).
- (cycles 31-33) Les plans larges en vertical (stade, champ vu du ciel, pays, tourbillon sur la ville) ne trouvent pas de focale : resserrer
  les points à cadrer, monter la caméra presque à la verticale et autoriser des focales jusqu'à 72-74.
- (cycles 31-33) Les savants filmés de dos, le président de dos qui épingle la médaille (70) : orienter la scène pour que l'action se fasse
  face à la caméra (l'accessoire entre le personnage et nous), ou passer la caméra de l'autre côté.
- (cycles 31-33) Un champ de blé de 26 m vu de haut reste un carré brun au milieu du vert (70) : champ jusqu'aux bords du cadre, brins plus
  larges et plus nombreux, sol doré, bandes coupées pâles pour le contraste.
- (cycle 33, revue 2 de 65) Les yeux en boule aplatis laissent dépasser la pupille à travers la paupière fermée : un « yeux fermés de plaisir »
  se lit comme un regard fixe (moteur corrigé : pupille cachée dès que la paupière est presque baissée, trait d'œil fermé en arche).
- (cycle 33) Une créature qui recule avec l'orientation par défaut (`face` 'move') fait demi-tour : après le gobage, on voyait le dos du poisson et
  une nageoire en planche devant l'objectif (65). `face='keep'` sur tout déplacement qui n'est pas une marche en avant.
- (cycle 33) Un saut sur place (déplacement vertical seulement) prenait un cap nul et retournait le personnage vers +Z : les canards sautaient de
  dos (65). Corrigé dans le moteur ; sur un ancien moteur, `face='keep'`.
- (cycle 33) Le clignement automatique d'une créature tombe au même instant dans chaque plan (même phase) : mécanique. Donner ses clignements
  au plan (`params={'blinks': [...]}`), un double de temps en temps.
- (cycle 33) Une onomatopée posée à la profondeur d'une grosse créature finit dans sa tête et ne se voit jamais (65 : aucun MIAM) : la mettre
  devant, du côté de la caméra.
- (cycle 33) Un objet d'échelle (voilier, pédalo) placé derrière le sujet géant ne se voit pas : le faire passer devant, sur toute la durée.
- (cycle 33, images de 71) Le décor `skyHigh` pose une couche de nuages blancs : sous des toits « au ras de l'eau », tout le bas de l'image
  devient blanc. Pour une ville noyée, `grassland`, une nappe d'eau de 600 m et des immeubles enfoncés jusqu'à leur dernier étage.
- (cycle 33) Une caméra sous la surface d'une nappe (`floodWater`) ne voit plus l'eau du tout (les faces de la boîte disparaissent vues de
  l'intérieur) : une rue sèche au lieu d'une rue inondée. Garder la caméra au-dessus du niveau final (`inside` avec un plancher).
- (cycle 33) La clé de look `tint` donne des images noires ou bleues avec le look naturel : ne pas l'utiliser.
- (cycle 33) Dans une petite pièce, `fitBack` recule la caméra à travers le mur (image d'une seule couleur) ; avec `inside`, elle reste
  dedans mais passe en très grand angle (80°) : élargir la pièce (`half`) plutôt que d'accepter la déformation.
- (cycle 33) Un accessoire posé contre le mur du fond d'un décor doit être devant ce mur (`back` + 5 cm) : derrière, il ne se voit pas
  (la carte de 71 était derrière le mur de la mairie).
- (cycle 28) Une créature ne prend ni `reach` ni `touch` : ses bras ne bougent que par des clips (`stampDesk`, `giveItem`, `drawMid`, `royalWave`,
  `point`, `shakeHead`, `readPhone`) et seules les voies `lay` et `sq` lui arrivent ; un tampon « tenu » bras ballants se lit comme un objet qui flotte.
- (cycle 28) Les clignements automatiques d'une créature tombent au même instant dans chaque plan (même phase) : donner `params.blinks` plan par plan.
- (cycle 28) Un nuage de poussière ou de brume à trente centimètres de l'objectif voile toute l'image : le mettre près des mains ou des genoux,
  loin de la caméra.
- (cycle 28) Un accessoire de sol posé à 3 cm (la vase d'une rivière vidée) laisse passer l'herbe du décor : le monter au-dessus du relief du décor
  et relever d'autant ce qui est posé dessus.
- (cycle 28) Un seul plan pris de l'autre côté de l'axe inverse le sens du regard (le feu passait de gauche à droite) : garder la caméra du même côté
  de la ligne entre lui et ce qu'il regarde dans tout le film.
- (cycle 28) `drift` sur une caméra cadrée au plus juste fait sortir le héros du cadre (sa tête coupée par le bord pendant tout le crochet) : pas de
  dérive quand un point d'ancrage touche le bord, ou des points de marge autour de lui.
- (cycle 28) Pour une contravention ou une lettre collée sur la poitrine, la clé `attach` doit répéter `face: 'camera'` : sans elle le papier passe
  de profil (une tranche rose de 15 px).
- (cycle 34) Avant de créer le dossier d'une histoire, vérifier que son nom n'existe pas déjà : `attente` était l'histoire 32, et le placement de la
  narration a réécrit son minutage (restauré depuis git).
- (cycle 34) Un personnage de 2,45 m debout dans le bus de ville passe la tête par le plafond (2,3 m) : `top` à 2,8 pour les plans intérieurs, ou
  la scène prise à la porte, de l'extérieur.
- (cycle 34) Un coureur filmé de côté sur une route droite est de profil, et le côté de sa tête en boîte se lit comme l'arrière : placer la caméra
  de trois quarts devant lui en dérivant à sa vitesse.
- (cycle 36) Un préréglage de personnage inconnu (`suit`, `farmer`, `tracksuit`, `waiter`) ne provoque aucune erreur : le moteur rend un inconnu
  générique. La construction le signale désormais (`audit_presets`) ; prendre un nom défini dans `engine/human.js`.
- (cycle 37) Un accessoire inconnu (`pavilion`, `coffeeCup`) disparaît au rendu : la construction le signale désormais (`audit_props`) ; chercher
  le nom dans `engine/props*.js` (`cottage`, `hotMug`).
- (cycle 37) Dans le cadre vertical, l'angle horizontal ne fait qu'environ 26° à 45° de focale : un personnage à 23° de l'axe sort du champ. Un plan
  par-dessus l'épaule doit poser l'épaule presque sur l'axe, et alors elle couvre le sujet : asseoir le personnage de premier plan et monter la caméra.
- (cycle 37) Une fourgonnette en double file à côté d'une voiture : aligner sa cabine sur le siège du conducteur (son centre décalé de la longueur
  du capot), sinon la caméra placée « dans la cabine » tombe dans la caisse de chargement.
- (cycle 34) `fitBack` recule la caméra jusqu'à ce que tous les points tiennent : si les points sont larges et que la caméra est du côté des maisons,
  elle recule jusque dans une maison et l'image devient un aplat sombre ou de la couleur de la façade (une image noire, une violette). Mettre la
  caméra du côté ouvert (de l'autre côté de la route) ou la borner avec `inside=`.
- (cycle 31) Les points de cadrage se donnent aux hauteurs réelles des articulations (la tête vers 1,8 m debout, plus bas penché ou à genoux) : des
  points à 2,95 m cadrent du vide au-dessus de lui et le poussent en bas de l'image. L'audit de la tête coupée ignore la pose : à genoux ou penché,
  il signale à tort une tête coupée ; vérifier sur les images.
- (cycle 28) Des gardes du corps placés juste derrière les personnages principaux se confondent avec eux en silhouettes à deux têtes : les décaler
  d'une demi-largeur vers l'extérieur et d'un pas en arrière, pour que leurs lunettes noires se voient toujours.
- (cycle 28) Une barbe ou des cheveux faits de cylindres enchaînés laissent un coin vide à chaque pliure et se lisent comme des tuyaux segmentés :
  une boule à chaque articulation, de l'épaisseur de la mèche (`beardHair` le fait par défaut, `joints: false` l'enlève).
- (cycle 29) Dans un patch Python, ne jamais coller un commentaire `#` au milieu d'une ligne qui continue par `; X = ...` : tout ce qui suit devient
  commentaire et la variable n'existe plus (NameError au premier usage). Mettre le commentaire en fin de ligne.
- (cycle 34) Un nom d'effet sonore inconnu (`sfx:skid`, `sfx:cheer`) est ignoré au mixage : l'audit le signale ; prendre un nom de la liste.
- (cycle 27, passe finale) Un déplacement (`to=`) sans `glide=True` joue la marche pendant le trajet puis rend au personnage son geste précédent
  en le relançant du début : un geste ponctuel (`gulp`, un saut, une bouchée) déjà joué recommence (la bouche se rouvre, les yeux se rouvrent).
  Pendant un geste ponctuel, tout déplacement du même personnage doit glisser (`glide=True`).
- (cycle 27, passe finale) Les mains guidées se croisent si l'on se trompe de côté : un personnage tourné vers +Z a sa main droite du côté des X
  négatifs. Une cible `R` à droite de l'écran et une cible `L` à gauche font des avant-bras en X (des bras croisés, pas une frappe au clavier).
- (cycle 27, passe finale) Un poisson qui tourne en rond dans un sac transparent se montre de face une fois sur deux et sa queue traverse le sac s'il
  est aussi long que lui : le faire nager de gauche à droite, toujours de profil, plus petit que la moitié du sac (`fishBag` avec `v2`).
- (cycle 38) Avant d'écrire un nouveau fichier (script de file, accessoire, histoire), vérifier qu'il n'existe pas déjà (`ls`, `git log -- fichier`) :
  `queue11.sh` existait déjà pour deux histoires et a été remplacé par une version plus large ; sans le vérifier, on peut écraser un travail.
- (cycle 38) Une barbe faite d'un éventail plat de mèches attachée à la tête disparaît de profil et se lit comme des planches sur l'épaule : lui donner
  du volume (`beardHair` avec `depth`, racines en U le long de la mâchoire) et garder les têtes à moins de 45° de la caméra dans les plans clés.
- (cycle 38) Un « double » qui doit être le même homme doit avoir le même modèle, les mêmes cheveux, le même fauteuil et le même plaid ; ne changer
  qu'un détail (la cravate). Un autre préréglage (chauve, costume gris) se lit comme un autre personnage et casse la chute.
- (cycle 38) Un ascenseur ouvert sur un rectangle noir avec le soubassement du hall dessous se lit comme « pas de cabine » : `immeubleHall` avec
  `car` (ouverture dans le mur, cabine éclairée, portes qui rentrent dans le mur).
- (passe finale de 67) Un commentaire `#` glissé au milieu d'une ligne de code Python efface tout ce qui suit : dans « La moustache », l'esquive du bocal (S10)
  et les deux drapeaux (S14) n'existaient plus, et les relecteurs ont vu « une rotation sur place » et « un liseré rouge pour deux drapeaux ». Après chaque
  correctif, chercher dans le script les lignes où du code suit un commentaire (`grep -n "#.*), \(k\|SQ\|MK\|P\)("`) et les remettre en fin de ligne.
- (passe finale de 67) `diff -q A B && cp ...; commande suivante` : quand le diff échoue, la suite après le `;` tourne quand même ; une copie maître
  périmée a été installée par-dessus le moteur (une ligne récente perdue, remise à la main). Toujours `if ...; then ...; fi`, et `git diff --stat engine/`
  après chaque installation pour voir que seules les lignes voulues ont changé.
- (passe finale de 68) Une loupe ou un rasoir tenus par le manche : le verre ou la tête sont au bout du manche, (manche + rayon) × échelle plus loin que la main
  (43 cm pour la loupe à l'échelle 2) ; pour la loupe devant l'œil, la main va sous le menton (`touch` face, hauteur ≈ −0,25), sinon le verre passe au-dessus du chapeau.
- (passe finale de 68) Un verre de champagne derrière une paroi blanche à 50 % devient un milkshake pêche : `flute` avec `straw` (paroi à 0,16, vin paille
  translucide légèrement émissif, dernière bulle cerclée de blanc dessinée par-dessus le vin). Vu de haut, le verre tenu reste une cloche blanche : le tenir à
  hauteur du visage, la caméra à la hauteur du verre.
- (passe 2 de 76) Une tête peinte (atlas) avec des cheveux blancs : les cheveux noirs sont peints sur les côtés et l'arrière de la texture ; `hairColor`
  les recolore maintenant (côtés et arrière), en plus du dessus en bloc ; sans cela le vieux avait le dessus blanc et les côtés noirs.
- (passe finale de 67) Un carton de titre en haut du cadre sur un panneau de la même couleur (TRIBUNAL bleu marine) se fond dedans : `courtroom` avec
  `sign: False` (ni panneau ni sceau au-dessus du juge) et le nom du tribunal sur la façade du banc, sous le carton.
- (passe finale de 68) Un accessoire tenu (`on={...}`) ignore `face='camera'` passé à côté : le moteur ne lit l'orientation face caméra que dans
  l'attache. Écrire `on={'actor': ..., 'hand': 'L', 'face': 'camera'}` (et `'faceFlat': True` pour un verre qui doit rester droit, vu de profil) ;
  sinon l'objet prend la rotation de la main : la loupe pendait sous le poing, le verre tenu penchait vers la caméra et se lisait comme une cloche blanche.
- (revue 1 de 77, revue 2 de 71) Chaque clé `toon` remplace la pose entière : une clé de battement qui ne porte que `sq` (ou un clignement `BLINK` qui ne
  porte que le visage) lâche les mains et les joues. La fanfare de « Le centime » ne jouait plus après le premier temps (trompette à la hanche, joues
  plates), les mains de l'homme tombaient pendant son clignement et la facture restait en l'air. Mettre `reach`, `hands` et le visage voulu dans chaque clé
  d'un plan où quelqu'un tient quelque chose (une fonction de pose par plan : `PLAY7(i)`, `HOLD22(face)`).
- (revue 1 de 77) Une clé d'attache plus tardive s'écrit `k(t, attach='mec', hand='R', offset=[...])` : avec un dictionnaire (`attach={'actor': ...}`)
  le moteur ne trouve personne et l'objet reste par terre (la lettre jamais ramassée).
- (revue 2 de 71) `fishSchool` lit ses hauteurs dans `y0` / `y1` (0,5 à 2,5 m par défaut) : une option `y` est ignorée et les poissons nagent dans l'air,
  au-dessus de l'eau. Plus généralement, quand un relecteur dit « la correction n'a rien changé », lire le code de l'accessoire pour vérifier le nom de l'option.
- (revue 2 de 71) `waterBill` : `stampDelay` compte à partir de `popAt` ; avec `popAt: -1` le tampon était posé dès la première image, avant le coup.
  `stampScale` (1,8) et `stampRot` (0,35) pour un tampon de chute en grand, en travers.
- (revue 1 de 77) Un garde-corps fait d'un pavé sombre (`slab` couleur fer, 1,3 m de large) devant un personnage se lit comme un trou noir : prendre le
  `balcony` (dalle de pierre, barreaux de fer). Une voiture vue de près : `glass` 0,85 et `glassColor` sombre, sinon on voit l'acteur debout dedans.

- (cycle 40) Une option d'accessoire au mauvais format plante l'accessoire en silence et laisse à l'écran une étiquette portant son nom de code
  (« monthCalendar » : `months` attend une liste de noms de mois, pas un nombre). Lire la signature de l'accessoire avant de l'employer.
- (cycle 40) Deux accessoires du même nom dans deux fichiers : le dernier passé à `Object.assign` gagne. `confetti` est la gerbe d'une couleur de
  props_elan.js (o.n vaut 1 par défaut : un seul point blanc sur une estrade) ; la pluie de confettis multicolores s'appelle maintenant `confettiRain`.
- (cycle 40) Le préréglage `cop` porte déjà sa casquette : un `copCap` ajouté par-dessus flotte au-dessus de la tête.
- (cycle 40) `bigCheque` sans `text` ni `amount` affiche « ASSURANCE 3 000 € » (le chèque d'une autre histoire) ; la carte officielle de `mairie`
  garde le tampon d'un autre épisode : `map: False` quand on n'en veut pas.
- (cycle 40) Une caméra de rue que `fitBack` fait reculer peut passer derrière une façade (tout le cadre bouché par un mur) : lui donner
  `inside=(...)` aux limites de la rue et resserrer ce qu'elle doit montrer.
- (cycle 40) Un script shell qu'un bash est en train d'exécuter ne s'édite pas en place (bash le lit au fil de l'eau) : écrire la nouvelle version à
  côté puis `mv` (nouvel inode, le processus en cours garde l'ancien fichier).
- (cycle 40) File de rendu : un verrou `flock` seul ne garde pas l'ordre d'arrivée (un brouillon a attendu 9 h pendant que des plus récents
  passaient). La file `runq4.sh` donne un ticket à chaque attente (fichier horodaté avec le pid) et ne démarre que le plus ancien ticket vivant ;
  pour remettre des attentes dans l'ordre : arrêter d'abord la chaîne parente (sinon elle continue et annonce « READY » sans brouillon), puis son
  attente, et relancer les copies `_q4` une à une dans l'ordre voulu.
- (cycle 40) Un brouillon lit le JSON au moment où son rendu démarre, pas quand on le met en file. Ne le mettre en file qu'une fois les corrections
  des images de contrôle faites et le script reconstruit : le brouillon 1 du « Bocal » a démarré cinq minutes avant elles, et ses deux critiques
  ont noté une version déjà corrigée (cuillère invisible, char vu de derrière un mur, astronautes de dos).

- (cycle 41) Une bande d'images nommée d'après un groupe de plans (`S11_S13`) couvre TOUS les plans du groupe, pas ses deux bornes : l'outil qui
  prépare la revue suivante ne gardait que S11 et S13, et les critiques signalaient des plans « absents des planches » trois revues de suite.
  Quand un critique dit qu'un plan manque, vérifier d'abord la liste de preuves avant de corriger le film. Les outils de revue sont dans
  `absurd-shorts/tools/review/` (voir son LISEZ-MOI) : ne plus les laisser dans un dossier temporaire.
- (cycle 41) L'accessoire qui porte le gag récurrent (téléphone à l'oreille, étiquette, ticket) doit se lire à la taille d'un téléphone tenu à
  bout de bras : deux tiers de la hauteur de la tête au moins, couleur saturée, du côté de l'objectif, coude écarté. Un poing sous le menton se
  lit comme une toux. Le vérifier sur l'image de contrôle du PREMIER plan avant tout le reste (« Le service client », revue 1 : 5,4).

- (cycle 41) Ce qui PEND d'une articulation (longue barbe, médaille, cordon, pendentif) se fixe avec `'hang': True` dans `on={…}` :
  `on={'actor': who, 'joint': 'head', 'offset': [0, 0.02, 0.1], 'hang': True, 'hangYaw': 0.4}`. L'accessoire reste vertical quelle que soit
  l'inclinaison de l'articulation, devant le porteur, à la hauteur de son vrai point d'attache, et ne suit que `hangYaw` (0,35 par défaut) de la
  rotation de la tête. Clouée à la tête, une barbe jusqu'aux genoux entrait dans le torse dès que la tête tournait de 90° (« L'ascenseur »,
  revue 2 : « la barbe tombe en moignons au col »). Les lunettes, elles, restent clouées, mais SUR le visage : la face avant de la tête est à
  z ≈ 0,094 (profondeur 0,17 × 1,1) ; un décalage z de 0,16 les faisait flotter six centimètres devant le profil.

- (cycle 41) Le visage peint n'existe que sur la face AVANT de la tête : un personnage de profil montre une face vide avec une oreille. L'accroche
  et le dernier plan doivent montrer le héros de trois quarts face (au pire de trois quarts), jamais de profil ni de dos, même s'il appuie sur
  un bouton ou joue aux cartes : il agit de la main la plus éloignée et nous regarde (« Le parcmètre », revue 2 : « le visage du héros n'est
  jamais à l'écran dans le premier ni dans le dernier plan »). Et le mot que la voix prononce (« quatre cents ans ») doit être dégagé PENDANT
  qu'elle le dit : ni tête ni manche devant.
- (cycle 41) Une chute se place entre 40 et 55 % de la durée du plan, puis se tient : quatre plans du « Parcmètre » posaient leur chute dans
  les 0,2 dernières secondes (ciseaux levés, sourire à la caméra, doigt qui lâche), invisible au rythme d'un plan par phrase.
- (cycle 41) La rotation d'un accessoire attaché se donne DANS `on={…, 'rot': […]}` ; passée en dehors (`rot=` sur l'accessoire), elle est
  ignorée dès qu'il est porté (« Le service client » : le téléphone restait de chant).

- (cycle 41) Un gag qui se propage (tout le monde imite le héros) doit changer de COMPORTEMENT à chaque étape, pas seulement de porteur ou de
  taille : une action différente de l'accessoire par plan (il jaillit quand le collègue s'arrête ; une vague d'un bureau à l'autre ; il rebondit à
  contretemps des pas ; il se lève lentement comme un drapeau). Et quand une phrase tient sur deux plans, le premier ne montre pas ce que le
  second révèle. « Le pull », revue 2 : 40 % du film en « tableaux où l'étiquette est déjà dressée et oscille ».

- (cycle 41) Une caméra « à l'intérieur » d'un meuble (frigo, placard, canapé) doit MONTRER le meuble : bords flous d'étagères, deux ou trois
  objets au premier plan sur les bords, sa lumière propre (bleutée pour un frigo). Sans eux, le plan montre juste le héros devant sa cuisine et
  le gag disparaît (« Les lunettes », revue 3 : « on n'est jamais dans le frigo »). Et quand un accessoire remplace la bouche (porte-clés,
  sifflet, paille), masquer la bouche peinte : sinon le visage a deux bouches.

- (cycle 41) Le rappel d'un gag doit être PLUS fort que sa mise en place : l'étirement de la chute du « Service client » (×1,3, deux images)
  était plus faible que celui du plan 7 qu'il rappelle (×2, tenu une demi-seconde), et la prise de conscience du plan 14 reprenait celle du plan
  6 telle quelle (revue 2). Écrire la valeur de la mise en place à côté du rappel dans le script et la dépasser.

- (cycle 41) Le visage peint du héros est de travers (l'œil gauche environ 0,1 m plus bas que le droit sur la tête mise à l'échelle). Des
  lunettes posées à plat laissent l'œil bas dépasser sous le verre, et il se lit comme un sourire avec une dent. Incliner les lunettes comme
  le visage (environ 37° dans « Les lunettes »), un verre sur chaque œil, et le vérifier sur une image de face en gros plan.

- (cycle 41) Mémoire : un rendu final (`story_X_render.json`, `--workers 3`) ouvre trois navigateurs d'environ 0,8 Go chacun. Deux rendus finaux et
  neuf séries d'images de contrôle en même temps ont fait tuer le navigateur du premier par le noyau après deux heures (« Target crashed »). Un
  seul rendu final à la fois, et des files qui le comptent pour trois rendus (`tools/review/runq4.sh`, `runqP.sh`).

- (cycle 41) HyperFrames refuse de rendre sous 1 Go libre (dans /tmp ET dans le dossier `renders` du projet) : le rendu final échoue alors
  APRÈS une heure et demie de rendu 3D, sur « Low disk space ». Vérifier l'espace avant de lancer un rendu final ; si la couche 3D est faite,
  relancer seulement l'étape HyperFrames (`npx hyperframes@0.9.13 render -o renders/X.mp4 --fps 30 --workers 2` dans le projet).

- (cycle 42) Un objet qui saute sous un choc (bocal, boîte, cocotte) se déplace EN ENTIER : animer le couvercle seul, ou le corps seul, le
  décolle de l'autre et on lit « le couvercle s'ouvre » au lieu de « le bocal sursaute » (« Le bocal », S08).
- (cycle 42) Un gros véhicule contre un petit objet (char contre bocal, rouleau contre pièce) : caméra au ras du sol, à moins de 0,5 m, l'objet
  au premier plan et au moins 15 % de la hauteur du cadre ; vu à hauteur d'homme le bocal ne faisait que 35 pixels et le gag disparaissait. Le
  véhicule ne doit pas traverser l'objet : une clé de 0,06 s qui lève l'avant (le nez monte sur l'objet) au contact.
- (cycle 42) Un saut sur un pied (orteil cogné) : les clés de position du saut ont besoin de `glide=True`, sinon un cycle de marche joue sous le
  saut. Face caméra, la jambe repliée est vue en raccourci et le saut se lit mal : tourner le corps d'environ 0,6 rad pendant le saut (les cibles
  des mains suivent cette rotation).
- (cycle 42) Rappel : `lens` est l'angle de champ VERTICAL en degrés (plus grand = plus large), pas une focale. L'agent de « La table basse » l'a
  encore lu comme une focale au premier tour : tous les plans étaient trop serrés. Le redire dans chaque consigne de mise en scène déléguée.
- (cycle 42) Planche de contrôle d'images extraites par ffmpeg : `dsheet.py` (fait pour les images de `render3 --stills`) rend une planche noire ;
  utiliser `ffmpeg -pattern_type glob -i 'f_*.jpg' -vf tile=7x2 planche.jpg`.
- (cycle 42) Saut sur un pied qui s'effondre une image au décollage : ce n'est pas un chevauchement de clés. Le moteur ajoute deux couches automatiques
  calculées sur l'accélération du corps (inclinaison de la colonne jusqu'à 0,5 rad, écrasement jusqu'à 38 %). Une réception en ease-in suivie
  d'une montée en ease-out inverse la vitesse en une image et le corps se plie. Remède : chaque moitié de saut en ease-in-out ET `'auto': 0.15`
  dans la pose du saut. Vérifier sur des images prises aux instants exacts de décollage.
- (cycle 42) Un pied qui doit rester en l'air (plâtre, jambe tenue derrière) : un `plant` toon à un point du monde surélevé. Une flexion seule
  est écrasée par les autres couches.
- (cycle 42) Rangée d'immeubles troués « en enfilade » : le décalage latéral de chaque bloc vu par la caméra doit dépasser la demi-largeur du bloc
  plus le rayon du trou, sinon les trous se cachent derrière le bloc précédent (ici 40° hors de l'axe, pas 28°). Vérifier les unités de `ry`.
- (cycle 42) Cône de faisceau d'hélicoptère près de la caméra : il remplit le cadre (le rendu avertit « camera inside prop »). L'enlever ou
  placer la caméra loin du cône.
- (cycle 43) Un personnage tourné vers +Z a sa main DROITE en −X. Un accessoire posé en +X passe dans sa main gauche et bloque le bras qui montre.
- (cycle 43) Les flexions de jambes toon ne descendent pas le bassin. Pour accroupir des soldats derrière des sacs de sable : enfoncer l'acteur
  (`pos y −0.42`), le sol cache les jambes.
- (cycle 43) `missileSalvo` est en ease-in : les images prises au milieu du plan ratent les missiles. En ralenti, passer en `lin`.
- (cycle 43) Décors muraux (affiches, plaques) : devant la couche du bandeau (z −3.53, pas −3.58), sinon ils disparaissent derrière.
- (cycle 43) Caméra plongeante qui regarde un peu vers +Z : l'image se retourne (le fond se retrouve en bas). Viser légèrement vers −Z.
- (cycle 43) `kitchenDay` : la suspension à y 2,7 bloque toute caméra placée au-dessus de la table.
- (cycle 43) Passer `story_kit.project()` sur CHAQUE caméra avant les images de contrôle : trois cadrages calculés à l'œil (S14, S15, S17 de
  « La guêpe ») étaient hors champ ou bouchés.
- (cycle 43) Un brouillon mis en file derrière un rendu final peut attendre une heure son créneau : la limite de 2 h d'une tâche de fond compte
  aussi l'attente, et l'arrêt de la tâche ferme le navigateur du rendu (« Target page, context or browser has been closed » vers 80 %). Lancer
  les chaînes longues détachées (`setsid nohup bash chain.sh > log 2>&1 < /dev/null &`) et les surveiller par un guetteur séparé qui attend le
  mot READY dans le journal.
- (cycle 42) Format 9:16 : une grosse réaction étirée (yeux qui jaillissent compris) a besoin d'environ 10 % de marge en haut. Élargir l'objectif
  et viser plus haut, ou plafonner `popLen`. Vérifier sur l'image du pic de l'étirement, pas sur la pose de repos.
- (cycle 42) Rangée de blocs en diagonale : chaque trou se cache deux fois, derrière le bloc de devant ET derrière son mur latéral qui court sur
  toute sa profondeur. En plus du décalage latéral, réduire la profondeur des blocs (`d`).
- (cycle 42) Les clés d'un accessoire ne font qu'une échelle uniforme : pour un écrasement (tampon, marteau), l'accessoire a besoin de sa propre
  option animée, et sa géométrie doit pendre depuis la face de contact.
- (cycle 42) Rendre lisible la face d'un tampon avant qu'il frappe une plaque verticale : le suspendre incliné vers la caméra, puis le rabattre
  à plat avec `rotTo` (un arc de marteau).
- (cycle 42) Un gardien qui pousse quelqu'un par une porte se tient À CÔTÉ de l'embrasure, jamais derrière la personne : sinon les deux têtes
  s'empilent à l'image.
- (cycle 43) Personnage noirci par une explosion (laser, bombe, four) : de la SUIE gris charbon avec des taches et des bords irréguliers, la
  peau d'origine visible par endroits, des cheveux en pétard qui fument. Jamais une teinte brune uniforme sur tout le visage : elle se lit comme
  un changement de couleur de peau, pas comme de la suie (vu sur le savant du « Bocal »).
- (cycle 43) Un point de main (`reach`) en coordonnées monde recopié d'un autre plan tire la main jusque-là : avec l'acteur à 16 m, ça fait un
  bras géant dont l'ombre est une tache inexpliquée au sol. Chaque acteur placé a ses propres points de main.
- (cycle 43) Le héros assis : sa tête-boîte va du menton à y ≈ 1,33 jusqu'au sommet à 1,87 (yeux ≈ 1,65), pas 1,45. Cadrer avec ces valeurs,
  plus ≈ 0,15 pour un bonnet de neige.
- (cycle 43) Un fanion est un plan : vu par la tranche il disparaît. Tourner sa face vers la caméra.
- (cycle 43) Missiles tirés de derrière la caméra : on ne voit que des flammes et des traînées en bout. Les faire traverser l'image de profil.
- (cycle 43) Caméra derrière les tas d'un sol en ruine : elle est devant les volutes de fumée, qui remplissent le cadre de boules sombres.
  Couper les volutes pour ce plan, et donner à la fumée une teinte émissive pour que son côté à l'ombre ne devienne pas noir.
- (cycle 43) Le clip `writeOnHeld` plus une cible de regard fait basculer la tête : utiliser `stand` avec un `reach` sur le porte-bloc.
- (cycle 43) Gag d'échelle (un porte-avions dans un évier) dans un cadre 9:16 étroit : caméra haute et en diagonale, robinet et rebord du bac
  dans le champ, chercher les candidats avec `project()` sur les accessoires et le visage du héros, et sortir la suspension du cadre.
- (cycle 42) `lay` = [bascule avant/arrière, bascule latérale] dans le repère du personnage. Une bascule avant d'un personnage tourné en
  diagonale par rapport à la caméra déplace sa tête de côté à l'écran (c'est ce qui empilait sa tête sur celle du gardien).
- (cycle 42) Une cible de regard (`look`) basse ou très hors axe fait rouler la tête sur le côté (« cou cassé »). Regarder à niveau, à hauteur
  de tête, et tourner le corps vers la cible.
- (cycle 42) Un pied tenu qui doit se lire à côté d'un plateau de table : point d'appui planté sur le côté (`side_pose`), pas la pose de saut
  tenue devant (devant, le pied se cache derrière le plateau et les mains se rejoignent à l'entrejambe : ça se lit comme un coup bas).
- (cycle 42) Un accessoire attaché à la main suit l'avant-bras : pour une loupe ou une pancarte qui doit faire face à la caméra, un accessoire
  libre animé avec la main.
- (cycle 42) Une poignée vue en bout se lit comme un disque : frapper une plaque verticale en biais pour que le côté du tampon se voie au contact.
- (cycle 42) `fitBack` vise le milieu des points : un cadrage pieds et têtes laisse le tiers bas vide. Pour un sujet bas dans le cadre, placer la
  caméra à la main et vérifier avec `story_kit.project()`.
- (cycle 43) Disque plein : ne pas compacter tout le dépôt git pour gagner de la place. Les gros objets sont des vidéos déjà compressées
  (4,25 Go ici), un pack ne les réduit pas, et le pack temporaire remplit le disque. Chercher d'abord les doublons octet pour octet
  (`cmp -s`) entre `out/` (ignoré par git) et `examples/`, les dossiers `out/work/story_*` et les calques `out/story_*_3d.mp4` des histoires
  déjà livrées. Un redémarrage du conteneur tue aussi les rendus lancés avec `setsid nohup` : relancer la chaîne entière.
- (cycle 43) Caméra juste au-dessus d'un grand accessoire (frigo, armoire) : la pièce derrière son bord est cachée et le dessus remplit le cadre.
  Monter haut derrière lui ; chercher la caméra avec un test d'occultation et un score sur la part du cadre occupée par le dessus.
- (cycle 43) Casque sur une tête à cheveux : les cheveux traversent le dôme en boîte noire. Mettre `hair: 'bald'` sous le casque.
- (cycle 43) Trous à côté d'une tête vue de face : des trajectoires droites venues de derrière l'objectif finissent hors champ. Trajectoires
  courbes (`ctrl`) passant à côté de la cible, trous placés là où ils se projettent près de la tête, `v0` pour le ralenti près du sujet, et
  `bodyColor` sombre (les missiles pâles disparaissent sur un mur pastel).
- (cycle 43) `shake` sur une caméra est une amplitude de tremblement (un nombre), pas une houle : utiliser la dérive from/to de la clé ou `roll`.
- (cycle 43) Neige sur des sacs de sable : un disque par sac se lit comme une assiette ; deux petites plaques bosselées se lisent comme de la neige.
- (cycle 43) `grade` et `light` par plan fonctionnent avec le rendu naturel : de quoi faire tout un bloc d'hiver gris et froid.
- (cycle 43) Collision de noms : une nouvelle constante `RIM` a écrasé en silence celle du bord du sucrier. Vérifier les noms avant d'ajouter.
- (cycle 43) Tour Eiffel lointaine dans `parisStreet` : à 175 m sa moitié haute disparaissait (seul le contour encré restait, comme un fil de
  fer dans le ciel). La rapprocher et la réduire par plan (`eiffelZ`/`eiffelH`/`eiffelX`).
- (cycle 43) Accessoire sur le flanc d'un petit personnage (médaille sur la mouche) : hors de la sphère du corps (x ≥ 0,03 unité mouche) et du
  côté de la caméra. Avec `ry` > 0, le −X local tourne vers une caméra en +Z. Sinon la médaille est dans le thorax et ne se voit jamais.
- (cycle 43) Les clés toon remplacent tout l'état : une clé sans `reach` lâche ce que la main tient. Répéter `reach` et `hands` dans chaque clé.
- (cycle 43) Passer d'un `reach` monde à un `touch` relatif au visage fait sauter la main en une image : `reach` monde dans les deux sens avec
  `toonEase` `inOut` (la tasse qui monte et descend sans saut).
- (cycle 43) Tenir le passage d'un missile au ralenti : deux étapes `missileSalvo` (approche lente linéaire, puis rapide) ; une troisième entrée
  `body: false, head: false, hide: false` garde la traînée de la première.
- (cycle 43) Tissu blanc sur la neige : il lui faut un fond sombre derrière (pan de mur), un contour épais et un bâton clair (un bâton sombre
  disparaît sur le fond sombre).
- (cycle 43) Le moteur ramène dans le cadre un acteur placé près du bord : il se rend plus à l'intérieur que `project()` ne le prédit.
  Vérifier sur une image fixe.
- (cycle 44) Sol plat sur le terrain `grassland` : à 1 cm ou moins il disparaît (le terrain s'affiche), à 2-3 cm il tient vu de haut mais
  clignote en vue rasante. Le surélever d'au moins 5 cm, ou colorer l'herbe du décor (`grass`) comme le sol voulu.
- (cycle 44) Gros objet qui entre dans un petit trou (sous-marin dans une flaque) : réduire son épaisseur à la largeur du trou au moment du
  passage ; le sol cache le reste, pas besoin de plan de découpe.
- (cycle 44) Dalle percée qu'on soulève : chaque surface posée dessus (route, trottoir) doit être percée du même trou ; aucune coque sous le
  trou ; sol sous la dalle sombre, sinon la paroi du puits montre de l'herbe.
- (cycle 44) Puits vu d'en haut : caméra à environ 60° vers le bas, acteur du côté opposé à la caméra, sinon le bord proche le cache.
- (cycle 44) Nuage de pluie vu de dessus : il cache sa propre pluie. Caméra à 64 m : nuage entre 8 et 26 m d'altitude.
- (cycle 44) Feuille qui pend d'un pupitre : faire passer le trajet devant la face avant (+0,25 m du centre), sinon elle pend dans le pupitre.
- (cycle 44) `node --check` ne voit ni les erreurs d'import ni les erreurs d'exécution d'un accessoire : seule une image fixe rendue le confirme.
- (cycle 44) `explosionBurst` suit l'horloge du plan et ignore son heure de départ : il est déjà sorti à la première image. L'envelopper
  (caché avant `at`, horloge `t - at`), comme `timedBurst` dans props_flaque.js.
- (cycle 44) Les personnages font environ 2,3 m avec la tête en boîte : pour cadrer avec `project()`, prendre le haut de la tête vers
  2,35 m, sinon la tête tombe dans la bande du carton ou sort du cadre.
- (cycle 44) Une découpe de `THREE.Shape` plus large que le contour est ignorée (la rue a recouvert le trou) : si le trou déborde,
  construire la bande en deux morceaux qui s'arrêtent sur le cercle.
- (cycle 44) Gros objet aspiré par un petit trou : garder toute sa largeur jusqu'au contact, puis rétrécir en 0,2 s environ. Déjà mince
  au contact, l'effet d'échelle disparaît.
- (cycle 44) Détail proche et bas (une flaque) puis impact lointain et haut (une façade) : un `glide` rapide qui suit le projectile.
- (cycle 44) Décor haut (beffroi) et personnage à plus de 25 % ne tiennent pas dans un cadre bas : plan large puis plan serré dans
  le même plan.
- (cycle 44) Tourner un personnage sur place vers la caméra : un déplacement vers sa propre position avec `face` ; `look='camera'` ne
  tourne que la tête. Une main tenue à l'oreille se règle par rapport au visage (`['face', across, up, fwd]`).
- (cycle 45) `buildProp` remplace un accessoire qui plante par un cube et un simple avertissement : construire chaque accessoire sous
  Node avec un DOM simulé (`Image`, canvas) et appeler `update` attrape ces erreurs (outil : `$SP/s7/barbecue/fix/prop_smoke.mjs`).
- (cycle 45) Cadre 9:16 à 4-5 m : à peine 2 m de large. Une action horizontale (soldat et cible, officier et suspect) n'y tient pas :
  la mettre en profondeur (par-dessus l'épaule, le long de l'axe) ou rapprocher les deux parties en X.
- (cycle 45) Deux porteurs de dos cachent ce qu'ils portent : caméra en grue à 4 m environ, vue à 45°.
- (cycle 45) Ruban de fumée près de la caméra : bouffées de rayon 0,11 au plus, au-dessus des têtes, sinon il cache le fond. Pas de
  bouffées claires sur les genoux d'un acteur assis (elles se lisent comme une anatomie) : derrière lui, plus sombres.
- (cycle 45) Accessoire attaché au torse : le +Z local du torse est l'avant de l'acteur (une voile qui doit tomber derrière va en −Z).
- (cycle 45) Arbres ou décor sombre juste hors cadre : leurs branches entrent dans le coin comme des traits noirs ; à 3 m au moins.
- (cycle 45) `face: 'camera'` garde +Y en haut : une assiette posée à plat reste vue par la tranche, l'incliner autour de X (≈ 0,95).
- (cycle 45) Salut assis : main droite à 0,12 devant, 0,15 sur le côté, hauteur de l'acteur + 1,6 m (plus bas : main sur la bouche).
  Clip `sit` : racine décalée de −0,45, mettre l'acteur à `y` = hauteur du siège − 0,45.
- (cycle 45) `--stills cams` ne rend pas le début du plan : pour vérifier une action, donner des instants explicites.
- (cycle 44) Accessoire attaché à un acteur : il est mis à l'échelle 1 / échelle de l'acteur, et `buildProp` l'emballe dans son propre
  groupe. Une copie de maillage posée en coordonnées locales finit trop petite, dans le maillage : la placer depuis la matrice monde.
- (cycle 44) Un moteur de test fait de liens symboliques teste `engine/` (Node suit les liens) : copier les fichiers, lier seulement
  `node_modules`.
- (cycle 44) `reach` n'accepte pas les points du visage (`['face', …]`), seul `touch` le fait (téléphone à la tempe).
- (cycle 44) Eau d'un chenal derrière un quai : la caméra doit plonger plus que hauteur du quai / distance, ou élargir le chenal à 1,5 m.
  Une corde vers une tour en retrait passe derrière la façade : avancer la tour au ras de la façade.
- (cycle 44) Écume ou poussière près de l'objectif : réduire la taille et la durée, sinon elle masque le décor.
- (cycle 44) Sol caché sous un décor qu'on soulève : le poser au moins 5 cm au-dessus du terrain, sinon il clignote (flash vert).
- (cycle 45) Orienter un bâton ou une lance par lacet + tangage : `ry` puis `rot` sur X ne penche que dans le plan YZ ; viser l'axe avec
  `axes_euler(X, Y, Z)`.
- (cycle 45) `project()` sous-estime le décalage des acteurs proches de la caméra (≈ 0,1 de largeur) : garder une marge ou vérifier.
- (cycle 45) Traînée de mouvement couleur manche sur un costume sombre : invisible. Lignes de vitesse claires, traînée plus claire.
- (cycle 45) Mur de mots derrière un personnage : opacité 0,08 au plus, sinon les mots se lisent dans la bande du carton.
- (cycle 45) Bras qui claque une porte depuis le hors-champ : saisir la porte près des gonds (rayon 0,4 m) ; au bord libre, le bras
  s'étire de 2 m et se lit comme un bâton.
- (cycle 44) Corde raide entre un quai et une tour : sa courbure tombe dans l'axe de la vue et elle se lit comme un bâton. La faire
  traverser l'image de côté, pente faible.
- (cycle 44) Objet tenu à l'oreille : le fixer à la tête (`joint: 'head'`), à côté, et y poser la main ; gros et contrasté (combiné
  rouge), sinon il disparaît.
- (cycle 44) Cylindre de lumière additif d'alpha uniforme : il se lit comme un bocal. Le dégrader en hauteur et sur les bords, halo au sol.
- (cycle 44) Approche lente puis rapide en Hermite : distance de départ > vitesse × durée / 3, sinon l'objet recule d'abord.
- (cycle 44) `worldRot` sur la clé de lâcher pose à plat un objet relâché (PV glissé sous une porte).
- (cycle 44) Bitte d'amarrage vue d'en haut : tête large = chapeau. Fût haut, tête à peine plus large, fonte noire.
- (cycle 45) Scène sombre avec une flaque de lumière : le moteur l'a déjà (`dark=[[0, k, 0.001]]`, `darkFloor`, `darkTint`,
  `darkPool={'at','r','k','tint'}`) ; ajouter un cône additif depuis la lampe.
- (cycle 45) `fx` de type `flash` : plein écran, sous les sous-titres. Trois flashs par seconde au plus (épilepsie photosensible).
- (cycle 45) Têtes « politique » hautes : bouche vers 2,2 m ; porter une fourchette à la bouche = main vers 1,67 m, devant le visage.
- (cycle 45) Téléphone fixé à la tête (`on={'joint':'head','offset':[0.135,0.2,0]}`) + main en `touch` : toujours à l'oreille ; tourner
  le personnage de 50-60° pour que l'oreille se voie.
- (cycle 45) Dômes à fuseaux rayonnants = parasols. Voile tombée : froissée (icosaèdre déformé, aplati) avec suspentes ; des soldats
  pendus à leurs suspentes vendent le parachute.
- (cycle 45) Figurants près de l'objectif : à 1,5 m le cadre fait 0,6 m de large, les placer un par un.
- (cycle 45) Masquer des pièces d'un accessoire partagé sans le modifier : parcourir le groupe construit et masquer par position.
- (cycle 45) Fumée de toux ou poussière : sprites à dégradé radial (`softDust`), pas des sphères `toonPuff` (elles se lisent comme des balles).
- (cycle 46) Mots anglais cachés dans le moteur : le gilet de la tenue `swat` (human.js) portait « SWAT », lisible sur les CRS de
  « La guêpe » (81) ; l'hélicoptère de base portait aussi « SWAT ». Remplacés par « POLICE », comme MILK → LAIT, GLUE → COLLE,
  ATM → RETRAIT, SOLD → SOLDES, WANTED → RECHERCHÉ, NO PAIN NO GAIN → TOUJOURS PLUS FORT. Avant chaque rendu final, chercher tout texte
  visible sur les tenues et accessoires utilisés (`grep -n "label(\|textLabel(" engine/*.js`) et vérifier qu'il est en français.
- (cycle 44) Un repère `rain` sans durée faisait échouer tout le mixage, donc la génération finale après 1 h 45 de rendu 3D. `mix.py` prend
  maintenant 1,5 s par défaut, mais donner la durée (`st.cue('rain', sid, t, gain, dur)`). Si seule l'étape HyperFrames échoue, ne pas
  relancer le rendu 3D : relancer `make_project.py` puis le rendu HyperFrames (voir `$SP/s7/hf_flaque.sh`).
- (cycle 45) `mat()` met en cache un matériau par couleur : un accessoire qui change sa couleur ou son émission (gril qui noircit) doit
  demander `unique: true`, sinon il change tous les objets de cette couleur dans les plans suivants du même rendu.
- (cycle 45) Surface émissive à 6 cm du terrain `grassland` : elle clignote image après image. La poser à 20 cm ; vérifier sur quatre
  images consécutives.
- (cycle 45) Fumée en sphères alignées = perles ou boules. Filet : tube effilé (`smokeTendril`) ; volute : sprites doux continus
  (`softWisp`). Pas de fumée sous un personnage assis : elle monte à hauteur de poitrine.
- (cycle 45) Salut assis, main ouverte : 0,06 devant, 0,2 sur le côté, hauteur + 1,6 (à 0,15 la main couvre un œil).
- (cycle 45) Une clé toon qui fixe `mouth` écrase le `talk` : pour faire parler, des clés toon alternées sur les mots, en répétant l'état
  de la main à chaque clé. Tête « politique » baissée : `bend: {'neck': [rx, 0, 0, 1, None]}` (rx positif vers le bas).
- (cycle 45) Cloche ou bulle de verre : un liseré lumineux de type Fresnel (0,2 de face, + 0,75 au bord), pas une opacité uniforme.
- (cycle 46) Avant de lancer un rendu final de 1 h 45, tester le mixage seul (`mix.py timeline cues out --bed …`) : il prend quelques
  secondes et évite de perdre le rendu sur un repère mal écrit.
- (cycle 46) Tête droite sur un corps penché : une tête épinglée sur un dos courbé garde la courbure si le cou ne l'annule pas en entier ;
  regardée par une caméra hors axe, cette inclinaison devient un roulis visible. Annuler la courbure au cou et garder les gros plans dans
  l'axe du visage.
- (cycle 46) Deux têtes-boîtes face à face : de profil, les deux visages peints disparaissent. Mettre la confrontation en V, ou empilée
  verticalement dans le 9:16, les deux visages vers les trois quarts face caméra.
- (cycle 46) Plans minces (vitre, rambarde, panneau) : une caméra dans leur plan voit la tranche comme une barre pleine. Rester à au moins
  vingt degrés de ce plan.
- (cycle 46) Gag d'arrière-plan lointain (échelle géante, nuage) : le vérifier contre la ligne de toit de la façade la plus proche ; si la
  façade le cache, planter l'élément devant elle ou relever la caméra vers le ciel.
- (cycle 46) Action en ligne de douze mètres (tir à la corde, file d'attente) dans le 9:16 : la couper en un angle proche et un angle en
  bout de ligne ou plongée large. Les arbres de `parisStreet` sont à x ±6,6 m tous les vingt-six mètres : refuser une caméra à moins de
  sept mètres d'un arbre dans le champ.
- (cycle 46) Orienter un accessoire libre : pour pointer son +Z selon la direction d, rot = [atan2(−dy, dz), asin(dx), 0].
- (cycle 46) Fin face caméra après une action de profil : couper dans le plan vers une caméra frontale plus proche et tourner le
  personnage avec une clé `face` ; `look` seul est bridé.
- (cycle 47) Un atelier d'écriture peut couronner une histoire qui refait un épisode publié avec un autre objet (le paquet de chips
  impossible à ouvrir refaisait le bocal : même escalade, même rebond, même ouverture facile par un tiers). Avant la production,
  comparer la structure du gagnant (problème, escalade, retournement, chute) à tous les épisodes publiés, pas seulement les mots ; si
  elle est identique, passer au second et le réécrire.
- (cycle 46) Élément lointain répété dans chaque plan (échelle géante, nuage) : ne l'afficher que pendant la caméra qui le montre, sinon
  deux exemplaires apparaissent d'un plan à l'autre ; borner sa longueur pour que le haut reste au-dessus des toits, planter son pied dans
  la rue devant la façade la plus proche, l'épaissir avec la distance.
- (cycle 46) Corps ou ligne horizontale de trois mètres ou plus dans le 9:16 : caméra à la verticale pour qu'il descende le cadre, ou grue
  haute de trois quarts. Une vue de profil ne le tient pas.
- (cycle 46) Un accessoire attaché à une articulation mise à l'échelle n'hérite pas de son échelle : animer ses décalages pour suivre la
  largeur de la tête.
- (cycle 46) Un petit personnage à côté d'un grand paraît de même taille s'il est un peu plus près de l'objectif : aligner leur profondeur
  sur l'axe de la caméra, pas seulement leur position au sol.
- (cycle 46) Un renflement sans éclairage sur un visage peint (joues pincées) prend une couleur choisie à la main, proche du visage rendu :
  la valeur de la texture sort beaucoup plus pâle.
- (cycle 47) Grandes dalles au sol (parking, asphalte) sur `grassland` : même six centimètres au-dessus, l'herbe perce par endroits. Les
  peindre en couches sans test de profondeur (renderOrder −1,5, marquages à −1,2), comme `roadStrip`.
- (cycle 47) Un utilitaire qui passe ses `**kwargs` aux opts d'un accessoire avale aussi `keys`, et l'accessoire reste immobile sans erreur :
  retirer `keys` avant de construire les opts.
- (cycle 47) Voitures : la distribution de 2,3 m n'entre pas dans une voiture à taille réelle. Mettre les voitures à l'échelle 1,25 environ
  et donner à celle du héros un pare-brise clair et un toit plat.
- (cycle 47) Caméra derrière une voiture visant sa cible : la voiture et la rangée garée cachent la cible. Monter la caméra de trois à quatre
  mètres pour voir par-dessus les toits.
- (cycle 47) Avions au-dessus puis impact au sol dans le 9:16 : regarder en l'air sur la première clé, puis glisser vers la cible.
- (cycle 47) Drapeaux inventés : les comparer aux vrais. Orange, blanc, vert ou bleu avec un disque central se lit comme l'Inde ; rouge et
  blanc en deux bandes comme la Pologne ou l'Indonésie. Des paires rares (violet et jaune, sarcelle et rose) sont sûres.
- (cycle 47) Boucle de défilé dans une petite surface (une place de parking) : elle se lit de six mètres de haut en trois quarts, pas à
  hauteur d'œil.
- (cycle 47) Tout objet monté sur une enseigne qui tombe (une horloge) doit basculer et se poser avec elle, sinon il flotte au-dessus du tas.
- (cycle 46) Caméra posée sur un balcon ou une terrasse : la placer devant le cadre de la porte-fenêtre ; une traverse à quelques
  centimètres au-dessus de l'objectif remplit le haut de l'image d'un coin noir.
- (cycle 46) Montrer « l'immeuble a disparu » dans une rue : reculer la rangée voisine pour ce plan, sinon un plan large depuis le trottoir
  d'en face montre le bloc suivant dans le trou.
- (cycle 46) Caméra au milieu d'un accessoire de gravats : lui donner des zones interdites, sinon des débris (surtout les poutres) tombent
  juste devant l'objectif.
- (cycle 46) Une tête passée entre des barreaux regarde de l'autre côté de la rambarde : aucune caméra ne voit à la fois ce visage et le
  corps dégagé des barreaux ; choisir ce que le plan raconte.
- (cycle 46) Une courbe d'accélération qui dépasse sa cible charge le mouvement au début : un balancement de 0,3 s se lit comme un saut.
  Pour un balancement visible, accélérer et ralentir, puis un petit dépassement à la fin.
- (cycle 46) Accessoire levé puis abattu (tampon géant) : le personnage l'écarte ensuite pour qu'il ne cache pas son visage.
- (cycle 47) Vérifier le sol sous chaque acteur : dans un parking plein d'épaves aplaties, une place choisie à l'image peut tomber sur
  une épave. Garder les acteurs sur les allées.
- (cycle 47) Objet qui tombe : une caméra finale tournée vers le bas ne montre que les derniers mètres. Faire suivre la visée de la
  caméra en deux ou trois glissés.
- (cycle 47) Canon « braqué sur lui » : de côté, il ne se lit qu'en profil. Pour l'arrêt, placer la caméra sur la ligne canon-cible pour
  que la bouche devienne un cercle face à l'objectif.
- (cycle 47) Tête-boîte qui montre quelque chose derrière elle : le bras se cache derrière le corps. Montrer vers le côté du cadre où
  est la cible, avec le bras de ce côté, tendu et un peu en arrière.
- (cycle 47) Clignotant vu à travers un pare-brise : une flèche qui clignote sur le tableau de bord se lit mieux qu'un feu extérieur,
  qui sort du cadre.
- (cycle 47) Bâtiment aplati vu d'en haut : le toit doit reprendre les couleurs et la bande des murs, sinon la dalle se confond avec
  l'asphalte.
- (cycle 47) Accessoire 3D partagé qui porte le marquage d'une vraie armée (étoiles) : le masquer avec un accessoire enveloppe qui cache
  les plans de décalque, sans modifier l'accessoire partagé.
- (cycle 48) Quand un audit de structure fait retirer la colonne vertébrale d'une histoire (procès, prison, blessure finale), la version
  corrigée perd souvent ce qui faisait rire : la force disproportionnée avec ses dégâts collatéraux dits comme un détail, et une chute
  qui retombe sur le héros. Après la correction, relancer en trois versions (escalade, chute, images) jugées avec la version corrigée.
- (cycle 48) Index de la main à doigts : dans le repère de `handR`, l'index est à x −0,031 et sa pointe vers y −0,136 ; un pansement ou
  une entaille se fixe sur `joint: 'handR'` avec un décalage d'environ [−0,031, −0,105, 0,017].
- (cycle 48) Feuille blanche comme accessoire clé : elle disparaît sur la pierre pâle ou un sol clair. La placer devant un fond sombre
  (porte, toise sombre, sol gris moyen), au besoin avec une caméra basse ; posée à plat, elle se lit d'environ 25 à 30° au-dessus.
- (cycle 48) Objets fins alignés (feuilles dans une rangée de suspects) : l'écart doit dépasser leur largeur, sinon ils se fondent en une
  bande.
- (cycle 48) Accessoire plan recto verso avec texture canvas : deux matériaux FrontSide et BackSide sur la même géométrie ; ne pas
  retourner la texture du dos, dessiner le dos sans texte avec la même découpe et la tache du même côté géométrique.
- (cycle 48) Décor `interrogation` : sa table centrale cache tout ce qui est sous 0,8 m derrière elle ; pour une rangée de suspects,
  prendre `whiteVoid` avec une toise à soi.
- (cycle 48) Rouleau compresseur (ou tout ce qui écrase une rangée) : le filmer de face pendant qu'il avance vers la caméra ; de côté,
  l'engin masque la rangée. Camion à l'arrière ouvert : ajouter un panneau sombre juste à l'extérieur de la face arrière.
- (cycle 47) Un SpriteMaterial sans texture se rend en carré plein : une lueur (clignotant, lampe) a besoin d'une texture en dégradé
  radial (`glowSprite` de props.js), sinon elle se lit comme une carte.
- (cycle 47) Gag de clignotant : un seul côté, tourné vers l'objectif. Retourner la voiture plutôt que montrer les deux côtés qui
  clignotent (on lit des feux de détresse).
- (cycle 47) Formation d'avions vue de dessous : elle se fond en une masse sombre. La montrer de face et d'en dessous, à 30-40° et à
  25-35 m, et réduire les avions pour qu'ils ne se chevauchent pas.
- (cycle 47) Gros plan sur quelqu'un devant un décor : vérifier d'abord de quel côté il regarde ; couper depuis le côté du décor montre
  l'arrière de sa tête. Ajouter une clé `face` à la coupe et recalculer les cibles de main guidée.
- (cycle 47) Portefeuille ouvert face à l'objectif : il paraît plat. Le tourner d'environ 35°, l'intérieur vers l'objectif ; après un
  retournement, tourner autour de Z et non de X.
- (cycle 47) Mât de navire fin avec une vergue : il se lit comme une croix d'église. Tour en treillis, radôme, radar qui tourne, vergue
  courte et basse, pavillons.
- (cycle 48) Une entrée de distribution sans `preset` retombe sans prévenir sur le costume bleu marine du héros : ses couleurs sont
  ignorées. Toujours donner un preset aux personnages secondaires (sinon on les prend pour le héros).
- (cycle 48) Colonnade vue de face : l'écart entre deux colonnes est une fenêtre qui s'élargit avec la profondeur ; garder tout ce qui
  est derrière la ligne des colonnes dans cette fenêtre angulaire, sinon les colonnes le cachent.
- (cycle 48) Portes arrière d'un fourgon ouvertes à 1,9 rad : vues de côté, elles font un mur ; les rabattre contre les flancs (environ
  3,0 rad).
- (cycle 48) Rangées aplaties derrière des objets debout : caméra à au moins 2,4 m qui regarde vers le bas ; à 1,1 m la rangée debout
  les cache. Pour un gag de « crêpe », un objet aplati se regonfle à moitié après les autres.
- (cycle 48) Objet important fin (feuille, lettre) : ni `transparent` ni alphaTest. L'occlusion ambiante de look.js ignore ces objets et
  on voit l'ombrage de ce qui est derrière. Découper la forme dans la géométrie (coin corné) et garder un matériau opaque.
- (cycle 48) Montrer le visage d'un personnage penché (joue sur un capot) : faire rouler le cou (rz) pour poser la joue vers la caméra ;
  tourner la tête ne suffit pas.
- (cycle 48) Machine qui écrase une rangée : la caméra précède la machine ; si elle la suit, la machine cache la rangée.
- (cycle 48) Dans une liste Python, un commentaire placé après un élément avale la virgule qui suit sur la même ligne : mettre le
  commentaire sur sa propre ligne.
- (cycle 50) Accessoire transparent animé par clés : il peut disparaître dans le film complet tout en s'affichant quand son plan est
  rendu seul ; couper le test de profondeur ne suffit pas, l'animer dans la mise à jour propre de l'accessoire règle le problème.
- (cycle 50) `earthGlobe` repose sur son pôle sud (centre à y = rayon) : tout ce qui est collé au globe va dans un groupe placé à ce
  centre, sinon il est dessiné sous le globe.
- (cycle 50) Rayon bas incliné (environ 26°) vu de côté : il remplit et délave tout le cadre 9:16 ; filmer depuis derrière la zone
  éclairée, dans l'axe du rayon, pour qu'il se dresse.
- (cycle 50) Ciel en dôme vu d'une caméra basse : son pied se lit comme un mur ; le fondre en gris près de l'horizon.
- (cycle 50) Foule dans un cadre 9:16 : vérifier chaque personnage avec `project()` ; 5 pique-niqueurs sur 9 étaient hors champ.
- (cycle 50) Tournesols filmés d'en bas : têtes plus grandes et moins penchées, caméra à hauteur de tête, sinon on ne voit que des
  disques plats.
- (cycle 49, « Le chat ») Croix rouge = emblème protégé : des secouristes portent une bande verte ou bleue et un casque blanc, jamais de croix.
  Une combinaison orange se lit comme celle d'un détenu.
- (cycle 49) Moustaches du chat créature qui se croisent : elles forment un « x » sur le museau, lu comme un œil KO ; écarter les deux de chaque côté.
- (cycle 49) Le chat créature remet les échelles de ses articulations à zéro à chaque image : pour une queue pendante, un accessoire séparé
  (effilé, annelé, bout pâle, oscillation en S) ; une colonne droite segmentée se lit comme un tuyau.
- (cycle 49) riotHelmet sur la tête-boîte se lit comme des cheveux foncés, un casque carré gris comme un seau : casque gris clair à bord, visière
  sombre opaque.
- (cycle 49) Le rig toon ignore la rotation de la racine : le clip « crawl » enterre le personnage ; le remplacer (accroupi qui avance).
- (cycle 49) Une vraie nuit vient des réglages par plan (ciel marine, lune, lumière chaude sur le sujet, appoint froid), pas du cycle jour-nuit
  (jour gris). Une aube se lit par un ciel bas rose-orangé et des ombres longues.
- (cycle 49) Obus qui frôle : petit obus allongé avec traînée qui traverse en 2-3 images l'espace que la tête vient de quitter ; l'impact va sur
  la façade, synchronisé avec l'effondrement ; au moins 0,5 m entre la bouche du canon et le personnage en gros plan.
- (cycle 49) Explosions au sol loin des personnages, sinon on croit qu'on les bombarde.
- (cycle 49) Le gag de fin a sa propre caméra : un plan rapproché, pas un plan large où le sujet fait 8 % de la hauteur.
- (cycle 49) Garder la carte sans action (l'objet sort avant que la carte tombe) ; objets clés entre 60 et 70 % de la hauteur, au-dessus des
  sous-titres.
- (cycle 49, « Le cheveu ») Faisceaux additifs : les dessiner entre le décor et les acteurs (onTopActors), sinon les costumes semblent
  transparents. Un fantôme gris sur un costume sombre peut venir des sprites d'éblouissement ou d'étoiles, pas du cône.
- (cycle 49) Descente vers la caméra : placer chaque point de la trajectoire sur un rayon de caméra ; un déplacement en profondeur reste minuscule
  ou passe derrière une tête.
- (cycle 49) Grands plans de poussière flous devant les acteurs : lus comme des jambes qui s'effacent ; poussière petite et au sol.
- (cycle 49) Le transfert de poids automatique au repos fait glisser une tête tenue pendant une action rapprochée : le couper par plan.
- (cycle 49) Un contour blanc garde lisible un accessoire noir et fin sur tous les fonds.
- (cycle 49) Chien rose rasé au museau carré = cochon : museau long, oreilles pointues, queue, collier.
- (cycle 49) Photo d'identité de profil : garder les yeux de face pour que « le même » se lise. Vapeur en fins gribouillis blancs, pas en disques
  flous.
- (cycle 50) Main en visière : le bras du côté opposé à l'objectif, doigts à plat sur le front ; le bras proche traverse le visage et le cache.
- (cycle 50) `pavillon` ajoute toujours des nuages (dalles beiges flottantes) : un accessoire de l'histoire peut cacher les objets nommés
  'cloud' de la scène.
- (cycle 50) Petite toile pastel vue d'en dessous : elle prend le rebond vert de la pelouse ; utiliser un matériau non éclairé.
- (cycle 50) Contact avec un accessoire qui s'ouvre : calculer où passe le bord à l'instant du choc et ouvrir à vitesse constante, pas en outBack.
- (cycle 50) Gag en caméra fixe avant un panoramique filé (recul d'un canon) : lui laisser environ 7 images, sinon il ne se lit pas.
- (cycle 50) Ombre sombre translucide = image seulement assombrie ; un calque gris moyen à 80 % rend le « gris » (couleurs vidées).
- (cycle 50) Menottes sur des objets couchés face à l'objectif : on ne voit que des lentilles ; les mettre debout pour que les anneaux se lisent.
- (cycle 50) Les clips à main levée (`podium`) peuvent cacher le visage pendant un étirement : fixer les deux mains avec reach.
- (cycle 50) Personnage face à +Z : vérifier gauche et droite avec `right(ry)` ; les mains d'un reach dans une porte étaient inversées.
- (cycle 50) Caméra basse sur une foule d'accessoires hauts identiques : ils s'empilent à l'écran ; décaler les départs (rangs du fond d'abord)
  pour qu'ils se séparent en montant.
- (cycle 50) Caméra basse près d'une maison : le toit se voit à peine, ce qui passe derrière apparaît au-dessus de l'avant-toit ; mesurer sur
  des images fixes plutôt que calculer.
- (cycle 50) Points blancs isolés sur un décor aérien instancié lointain : ombrage plat de triangles sous-pixel ; donner à ces maillages une
  copie de matériau lissé.
- (cycle 50) Le moteur pilote la visibilité de la racine de chaque accessoire : pour en cacher une partie en cours de plan, agir sur ses
  enfants, jamais sur `g.visible`.
- (cycle 50) Parasol vu dans l'axe : son mât ne se voit que si L·sin(inclinaison) > R·cos(inclinaison) ; allonger le mât ou incliner au-delà
  d'environ 25°.
- (cycle 50) Voisins qui écrasent le héros : à côté et un peu derrière, penchés de 0,3 au plus, sans chapeau, sinon leurs têtes cachent son
  visage.
- (cycle 50) Texte ajusté à une bannière d'écran étroite = plus petit ; pour grossir un mot, lui donner sa propre plaque murale.
- (cycle 50) Tournesol penché vu à hauteur de tête : on voit son dos ; vu d'en dessous : un disque plat ; aucun des deux ne se lit comme un visage.
- (cycle 50) Secouer ou lever une lampe tenue : animer l'accessoire par clés aux mêmes instants et courbes que le reach de la main.
- (cycle 50) Une image de traînée d'environ 0,035 s avant une prise ne se voit qu'à 30 i/s : la vérifier sur le rendu final, pas sur le
  brouillon à 15 i/s.
- (cycle 50) Bord d'ombre qui doit passer à l'écran au bon moment : calculer image par image où le sol croise la hauteur visée (avec une
  entrée en douceur) et déplacer le disque sur un chemin à clés, pas un smoothstep en mètres.
- (cycle 50) Très grand disque d'ombre : bord doux de largeur fixe en mètres ; des anneaux proportionnels au rayon font de larges marches grises.
- (cycle 50) Réaction sous une ombre vue d'avion : des feux stop dessinés après l'ombre (sans test de profondeur) se lisent là où de petites
  voitures seules ne se voient pas.
- (cycle 50) Plan rapproché de chute au bout d'une grue : seconde caméra en glissé (0,3 s de large, environ 0,6 s de glissé), puis tenue ; un
  seul long mouvement passe tout le plan dans un milieu encombré.
- (cycle 50) Fond net derrière la tête du héros dans une foule : laisser un trou dans les rangs sur la ligne caméra finale → sa tête.
- (cycle 50) Écrasement en deux temps : la tête bascule à l'opposé du premier voisin, puis se redresse longue et fine au second ; le second
  voisin ne le regarde qu'un instant avant son temps.
- (cycle 50) Fleurs qui se fanent tristes : caméra trois-quarts un peu basse, tige en arc, une fleur héroïne avec un petit visage ; une
  charnière à la tête seule se lit comme un couvercle.
- (cycle 50) canvasPlane est opaque sauf transparent : peindre son fond de la couleur de la surface où il est posé.
- (cycle 50) Clés `squash` d'un accessoire : elles reviennent vite (cos 11u) ; pour un aplatissement tenu 0,1 s, donner une longue durée à
  cette clé (environ 2 s) et laisser la clé suivante reprendre.
- (cycle 50) Mains au premier plan près de l'objectif : elles brûlent sous les flashs proches ; les garder à environ 2 m, poignets à
  0,84-0,88 de la hauteur, et les flashs plus loin.
- (cycle 51, « La pizza ») Gros plan de téléphone : une cravate entre deux formes de peau se lit comme un entrejambe ; faire sortir le
  téléphone par le bas du cadre.
- (cycle 51) Un avion de chasse entier et un gros accessoire ne tiennent pas ensemble en 9:16 : montrer l'avion en partie, ou en deux plans.
- (cycle 51) L'effet de souffle lumineux délave les visages-boîtes : petites bouffées seulement.
- (cycle 51) Garnitures posées sur la surface de la part, sinon on lit un cornet de glace. Un trottoir roulé montre son bout en spirale.
- (cycle 51) Le drapeau par défaut de pressRoom ressemble à un vrai drapeau et fighterJet porte un lettrage anglais : vérifier et masquer
  les deux dans chaque histoire.
- (cycle 51) Le grey-scan signale un flash blanc voulu comme un creux : le vérifier image par image, et le garder à 0,12 s ou moins.
- (cycle 51) Le brouillon de contrôle après la passe finale vaut son coût : il a trouvé deux défauts que la troisième revue n'avait pas vus.
- (cycle 50) Avant un rendu final, vérifier qu'il reste au moins 1,2 Go libre : HyperFrames refuse de démarrer sous 1 Go (« Low disk
  space ») après l'heure de rendu 3D. Si ça arrive, ne relancer que l'assemblage HyperFrames (le calque 3D est déjà dans assets/), après avoir
  vidé le cache npm (`npm cache clean --force`), jamais les vidéos livrées.
- (cycle 51, « Le stylo ») Une clé de visibilité sur un accessoire réaffiche tous ses enfants : pour basculer entre deux variantes, passer
  par l'échelle, pas par la visibilité.
- (cycle 51) Mains de figurants ciblées en coordonnées monde : pendant une chute du support, elles restent en l'air et les bras s'étirent ;
  faire suivre les cibles avec le support.
- (cycle 51) Personnages en tenue sombre la nuit : même gris foncé pour tous plus une lumière d'appoint froide par personnage, sinon ils se
  fondent en une masse noire ; yeux blancs avec pupilles.
- (cycle 51) Une même réaction (« yeux sur tiges ») réutilisée trois fois est relevée par les critiques : une seule par film, varier les
  prises (mâchoire qui tombe, double take, affaissement).
- (cycle 51) Poussé avant sur le plan final : vérifier la dernière image, il rogne facilement l'accessoire clé au bord du cadre.
- (cycle 51) Écharpe tricolore inventée : vert émeraude + jaune se lit comme un vrai drapeau ; violet + or ne correspond à aucun.
- (cycle 51) Projecteur d'hélicoptère : le faisceau descend sur la cible, sinon le plan perd son sens ; hélicoptère plein, pas en contour.
- (cycle 51) Piles « jusqu'au plafond » : caméra basse et proche du personnage, sinon les piles s'arrêtent au milieu du cadre.
- (cycle 51, « La tache ») Plastron de chemise fixé au torse : le faire commencer environ 0,1 m sous l'origine du torse, sinon les boutons
  noirs du costume dépassent.
- (cycle 51) Planche pliée : le moteur l'a retournée bout pour bout contre le calcul (une rotation z de −π/2 l'a redressée) et une extrusion
  centrée s'enfonce à moitié dans le sol : la lever de la moitié de sa longueur et vérifier sur une image fixe.
- (cycle 51) Caméra « derrière l'accusé, face au juge » dans `replicaCourt` : rester devant le banc (z > −13,3), sinon l'image est noire.
- (cycle 51) Montrer des gens derrière un objet proche : monter la caméra et regarder vers le bas ; d'une caméra basse, l'objet cache leurs têtes.
- (cycle 51) Boucliers anti-émeute à hauteur de tête = grosses lentilles qui cachent les visages : à hauteur de poitrine, visières visibles.
- (cycle 51) Décor blanchi blanc sur blanc : ne se lit que sur ciel bleu ou porte sombre ; garder chaque temps blanchi bas contre le ciel.
- (cycle 51) Une main qui tient un accessoire devant la poitrine cache un gag de poitrine : l'écarter vers le bas à l'image du choc.
- (cycle 51) Chemise posée à plat sur une planche : `rotOrder='YXZ'` avec rot `[-π/2, π/2, 0]` la couche face visible le long de +x.
- (cycle 51) Main de salut ou de visière posée sur le visage (`touch ['face', …]`) : elle suit la tête pendant les petits mouvements ; un
  reach vers un point fixe du monde s'enfonce dans la tête.
- (cycle 51) Étirement du cou à 2,6 : la tête-boîte sort du cadre 9:16 ; 1,5-1,6 avec une tête à 1,16 se lit comme une prise, visée devant
  avec les pupilles en bas pour garder la mâchoire visible.
- (cycle 51) Étalonnage chaud + soleil chaud = tissu blanc pêche ; base froide (#E2EBF8), émissif froid et sans grain = blanc.
- (cycle 51) Accessoire blanchi qui garde sa carte de grain = bois beige ; retirer la carte une fois blanchi et ajouter un léger émissif bleu.
- (cycle 51) `townHall` : `gable: 'v2'` (sinon une dérive dépasse) ; il porte un vrai drapeau à masquer ; son enseigne MAIRIE disparaît
  une fois blanchie, la couvrir d'une plaque à bord sombre.
- (cycle 51) Déplacement avec `clip='walk'` : l'acteur se tourne dans le sens de la marche ; `face='keep'` pour reculer face caméra.
- (cycle 51) Clés de déplacement : chaque mouvement commence à la clé précédente, pas à son heure de fin.
- (cycle 51) Projectile qui continue après l'impact = deuxième balle : longue clé d'écrasement (2 s) et le cacher 0,05 s après le contact.
- (cycle 51) `st.at(shot, line, i)` compte les mots à partir de 0 : afficher le mot avant d'y caler un temps fort (la nuit tombait sur « jour »).
  Caler les temps forts sur les vrais temps des mots de timeline.json, jamais sur une estimation par syllabes.
- (cycle 51) `daynight` avec `once` atteint la nuit à mi-période : période 0,04 s et `from` 0,01 s avant le mot = bascule en une image.
- (cycle 51) `kitchenDay` suspend une lampe en (0, 2,7, −1,0) : une prise qui étire la tête vers le haut doit se tenir à l'écart.
- (cycle 51) Mâchoire tombante (`jawBlock`) cachée par un plastron : `jawFwd` d'environ 0,4 pour qu'elle pende devant la poitrine.
- (cycle 51) Feuille transparente sur une couleur clé (carte sur la tache) : elle la teinte ; découper la forme dans la vitre (destination-out).
- (cycle 51) Une clé keepPose fait tomber le visage : une clé de respiration doit porter le visage et éviter les fenêtres de clignement.
- (cycle 51) Outil pointu (fer à repasser) : le pointer dans le sens du déplacement, sinon son nez recouvre ce qu'il contourne.
- (cycle 51) Animer un élément d'un accessoire d'une autre histoire : l'envelopper dans un accessoire de son histoire, sans toucher l'autre fichier.
- (cycle 51) Une main qui repasse le bord proche d'une feuille posée, vue d'une caméra placée derrière, traverse toujours le milieu : placer
  la marque clé haut sur la feuille et changer de main ou se décaler pour que chaque bras arrive de son côté.
- (cycle 51) Vue à 40° : les parties en relief (fer, poing sur la poignée) montent à l'écran d'environ 1,2 fois leur hauteur ; garder cette marge.
- (cycle 51) Soleil chaud + étalonnage chaud tuent le bleu d'un rouge : le repeindre plus froid (#D03A3C) et le mesurer sur l'image.
- (cycle 51) Passer un accessoire de main en main : l'animer dans le monde aux mêmes instants et courbes que les deux reach ; permuter la
  visibilité de deux copies attachées aux mains donne un saut.
- (cycle 51) Couper le transfert de poids automatique dans les plans de jeu rapprochés avec `hip: 0` dans la première clé toon.
- (cycle 51) Objet qui tombe devant la main qui le lâche : l'avant-bras le cache ; écarter la main au lâcher.
- (cycle 51) Chute par gravité d'un accessoire : quatre clés `to` linéaires aux positions u² ; un ease-in cubique met toute la chute dans la
  dernière image.
- (cycle 51) Boucliers anti-émeute : reflets et poignée horizontale à embouts = cadran d'horloge ; face laiteuse unie, bord épais, poignée verticale.
- (cycle 51) Bourrelets sur les quatre bords d'un tissu posé = plateau ou cadre ; bourrelets effilés sur les côtés seulement.
- (cycle 51) Accessoire porté avec une étiquette par défaut (REGISTRE MARIAGES) : vérifier ses options de texte pour chaque histoire.
- (cycle 51, « Le faux numéro ») make_config1.py et round_config.py plantent sur les plans scindés (S04b, S12b) : lire le numéro avec
  int(re.match(r'\d+', sid[1:])) et reporter les plans scindés dans les configs des tours suivants.
- (cycle 51) Moteur toon : une clé qui ne nomme que le `reach` d'une main remplace tout le dict reach, et keepPose ne fusionne que le niveau
  supérieur ; reporter reach et hands pour chaque acteur.
- (cycle 51) Crâne rasé sur une tête-boîte : calotte plus pâle et rosée, reflet fixe, sommet arrondi, sinon on lit un chapeau.
- (cycle 51) Téléphone de bureau : socle vide quand le combiné est décroché ; des écouteurs sombres se lisent comme des yeux.
- (cycle 51) Un pays vu de l'espace se lit comme une île sauf s'il remplit environ 70 % du cadre, sans lagon, sous une forte courbe d'horizon.
- (cycle 51) Animaux (vaches) : pas de clés d'écrasement, et leur lecture reste fragile (chèvres, moutons) ; les garder grands et de profil.
- (cycle 51) Pelleteuse : flèche claire et cernée, sinon on lit un char. Casque qui projette son ombre = hachures vertes sur le visage.
- (cycle 51) Après tout redémarrage du conteneur, vérifier le log du rendu final et le relancer : il est tué sans prévenir.
- (cycle 52, « Le chifoumi ») Les aides de type `HAND()` qui passent `**o` dans `opts` avalent `keys` : sortir `keys`, sinon l'accessoire
  ne bouge jamais.
- (cycle 52) Une clé keepPose fait tomber le visage : répéter `face` sur chaque clé keepPose pendant une expression.
- (cycle 52) BufferGeometry posée à plat dans le plan XZ : facile à orienter vers le bas et cachée par le culling ; `DoubleSide` pour les
  calques peints au sol.
- (cycle 52) Mains en accessoire : cacher les deux moufles de chaque acteur avec `scl`, sinon un bloc de peau traîne près de la main accessoire.
- (cycle 52) Stade qui se fend en deux le long de X : ne se lit que d'une caméra dans l'axe Z (la fente monte au milieu du cadre vertical).
- (cycle 52) Tableaux et panneaux d'un décor qui tombent derrière les têtes ou dans la bande des cartons : les couper par plan (`board: None`).
- (cycle 52) Gens penchés à la fenêtre d'un bâtiment plein : un appui saillant par fenêtre ouverte et l'acteur debout dedans.
- (cycle 52) Poing-moufle : il se lit du côté replié (plis et pouce plus clair), levé et tourné vers la caméra ; de dos c'est une boîte.
  Main plate levée : la tourner d'environ 0,9 rad paume vers la caméra, de profil c'est une gélule.
- (cycle 52) `fitBack` sur une caméra de chute recule de 4-5 m et rapetisse le gag : placer la caméra à la main et vérifier avec `project()`.
- (cycle 52) Deux-plan 9:16 : au niveau des mains le cadre ne fait qu'environ 1 m de large ; vérifier les positions de départ des mains, pas
  seulement le point de rencontre. Les coins hauts sont occupés par les têtes : reculer la caméra pour y loger un gag de fond.
- (cycle 52) Travelling de caméra (accessoire) visé sur un objet et vu de face : il le cache ; faire entrer le rail en travers de la ligne de vue.
- (cycle 52) Une tape donnée depuis le rang de derrière sur un poing disparaît derrière le corps ; une tape sur la tête se lit, et écraser la
  tête à chaque tape ajoute une réaction.
- (cycle 52) Dans un accessoire, une référence rangée dans `g.userData` pendant la construction peut avoir disparu dans `update` : la garder
  dans une variable locale.
- (cycle 52) Objet du gag juste derrière l'acteur dans un gros plan : l'action se joue cachée par sa tête ; le décaler d'environ 0,8 largeur
  d'écran du côté opposé à l'accessoire tenu.
- (cycle 52) Un contour en pointillés du volume perdu rend lisible en 0,3 s un avant-après « a perdu deux étages ».
- (cycle 52) Carton calé juste avant un glissé de caméra : il tombe pendant que la tête bouge ; le caler après le glissé et vérifier la tête du
  plan suivant sous la bande du carton.
- (cycle 52) Plans scindés (S09b) : round_config/next_config les perdent au tour 2 (SHOTS, PAIRS) ; régénérer une config de tour 1 fraîche
  avec make_config1 et recopier SHOTS, STILLS, STILL_DESC, PAIRS, PAIR_DESC dans la config du tour suivant.
- (cycle 52) Gerbe d'eau : beaucoup de petites gouttes étirées sur des paraboles rapides (environ 0,11 s jusqu'au sommet) ; un cylindre se lit
  comme un rayon de lumière, de grosses sphères comme des œufs.
- (cycle 52) Main en anneau : une plaque en C vue du côté du pouce, pouce plus foncé qui rejoint le bout des doigts ; un tore se lit comme un beignet.
- (cycle 52) Mot clé tardif + plan large d'au moins 0,6 s : la coupe tombe avant le mot ; le geste clé doit alors se jouer dans le plan large.
- (cycle 52) Acteur téléporté à une coupe : son reach vise encore l'ancien point (bras étiré en travers du cadre) ; reposer le reach à la coupe.
- (cycle 52) Lumière d'appoint devant une fenêtre : 9 brûle le mur ; environ 2,5 à 1,6 m suffit à éclairer les visages.
- (cycle 52) Bras de robot à deux segments étirés : il reste droit et plonge loin du trou ; viser un L, coude au-dessus du trou.
- (cycle 52) `mix.py` écrit un dossier au nom de la sortie (mix et pistes) : le supprimer par chemin littéral après un pré-test.
- (cycle 52, « Le distributeur ») Rig toon : le clip de départ d'un acteur est ignoré dès que des reach de main sont clés ; ajouter une clé
  k(0.0, clip=...).
- (cycle 52) L'agenouillement abaisse le corps après la résolution du bras : compenser la cible de la main.
- (cycle 52) Volet de distributeur : il pivote vers l'intérieur et aucune bande décorative ne couvre le renfoncement, sinon le bras dedans ne se lit pas.
- (cycle 52) Le moteur rééclaircit les images sombres : éclairer un panneau sombre plutôt que jouer sur la transparence.
- (cycle 52) Reflet sur une tête-boîte : discret (15-20 %) et à côté du sujet, pas au-dessus.
- (cycle 52) Couloir avec rangées de machines en plan large : mettre en scène en profondeur, caméra basse.
- (cycle 52) Feuille tamponnée : la tourner face caméra et la faire grandir (au moins 25 % de la largeur) pour qu'elle se lise.
- (cycle 52, « Le chifoumi » passe 3) Main géante en accessoire au bout d'un bras d'acteur : un poignet nu couleur peau et une manchette
  entre la manche et la main (`wristL`), sinon la main flotte comme un objet détaché ; le pouce en bloc séparé plus foncé.
- (cycle 52) Lumière d'appoint d'une fenêtre (PointLight) : l'allumer à la coupe du plan rapproché (`fillAt`) ; dans le plan large elle
  fait une tache blanche sur la façade.
- (cycle 52) « Se pencher à la fenêtre » ne se lit pas de face (le buste se raccourcit) : caméra de trois quarts.
- (cycle 52) Clés `life()` après un affaissement : elles remettent `sq` près de 1 et annulent l'écrasement ; respirer autour de la pose
  affaissée avec des clés complètes.
- (cycle 52) Acteur déplacé (`to`) à la coupe : il se tourne et se plie vers sa cible dans les dernières images du plan d'avant ; s'il sort
  du cadre du plan suivant, le cacher à la coupe au lieu de le déplacer.
- (cycle 52) Gonflement d'une main de robot pointée vers le haut : agrandir les trois axes ; un étirement le long de l'axe local Y part
  vers la caméra et ne se voit pas.
- (cycle 52) Médaille épinglée sur un poing géant : la décaler vers la caméra d'au moins la profondeur du poing, sinon il la cache.
- (cycle 52) Mouettes qui tournent en sens contraires = croix en X à l'écran : même sens, une hauteur par mouette (`gullLane`).
- (cycle 53) Plan 9:16 chargé : chaque élément doit tenir dans environ 26° à l'horizontale ; chercher position, cible et focale
  par une petite grille contre des cadres par point (project()) au lieu de deviner — dix caméras sur seize corrigées d'un coup.
- (cycle 53) Personnage penché à une fenêtre : fenêtre plus haute que sa tête (appui à 1,0 m → linteau à 2,6 m ou plus), sinon le
  mur au-dessus lui coupe la tête.
- (cycle 53) Rebord de télévision partiel : jamais une plaque pleine largeur devant l'écran, elle cache le petit décor à l'intérieur.
- (cycle 53) Assistant qui passe `**kwargs` dans les `opts` d'un accessoire : il avale `scale` comme il avale `keys` (sac visible dès
  la première image) ; extraire les deux.
- (cycle 53) Tableau sur le mur du fond orienté +Z : une caméra qui regarde vers +Z voit son dos vide ; ry=180.
- (cycle 53) « Les yeux grands ouverts au lit » : un homme allongé vu du pied du lit à 35° n'est qu'un trait ; l'asseoir contre la
  tête de lit et donner à la couette un pli qu'il remonte.
- (cycle 53) Sprite de charnière vu d'une caméra basse de côté : il se cache derrière son propre chambranle ; le poser devant le
  cadre (ou `onTop`) et le vérifier sur la première image.
- (cycle 53) Deux maisons dans le même plan ne peuvent pas être premier plan et fond en vertical : avancer celle du premier plan et
  vérifier la ligne de vue au coin avec project().
- (cycle 53) Volet ouvert qui dépasse du bout de son mur : il cache le gag du fond ; pas de volets sur cette fenêtre.
- (cycle 53, session 87 « Le pneu ») Vérifier les noms d'effets sonores contre audio3.py / audio.py / FX de mix.py avant le brouillon :
  un nom inconnu tombe en silence.
- (cycle 53) Préfixer les accessoires nouveaux par histoire : props.js fusionne par Object.assign, une collision écrase sans erreur.
- (cycle 53) Vague de voitures filmée de face = masquée par la plus proche : caméra en diagonale depuis la bande d'arrêt, premières
  chutes dès 0,3 s, voiture proche vers 1,0 s.
- (cycle 53) Cibles de main gauche et droite inversées = bras en X ; vérifier sur la planche.
- (cycle 53) Étiquette « sans chiffres » = sans symbole monétaire non plus.
- (cycle 53) Pompe à pied : baril rond, pédale et cadran, sinon elle se lit comme une guillotine.
- (cycle 53) Plan de rappel cadré comme un plan précédent : garder un espace entre les têtes, sinon elles fusionnent.
- (cycle 53) Bitume en conflit de profondeur = scintillement : dessiner l'asphalte sans test de profondeur.
- (cycle 53) Visage dans l'entrebâillement d'une porte : calculer avec project() la position écran du bord libre du battant ; vu du
  côté des gonds, le visage doit tomber entre le chambranle et ce bord, sinon le battant le cache.
- (cycle 53) Battant à deux creux sombres = persienne ; quatre panneaux en relief à moulures claires = porte, lisible au téléphone.
- (cycle 53) Sac qui s'aplatit puis regonfle : clés `flat` propres à l'accessoire, pivot sur son bord bas ; la clé `squash` du
  moteur rebondit toute seule.
- (cycle 53) Accessoire posé sur un pupitre qui s'écrase : caler sa hauteur image par image sur la courbe de rebond du pupitre,
  sinon il flotte.
- (cycle 53) Barbe accrochée à la tête avec un petit décalage z : elle disparaît dans la veste ; l'avancer d'environ 0,17 et
  relever sa pointe.
- (cycle 53) Livre fermé posé à plat, vu à hauteur de pupitre = rouleau ; incliner livre et pupitre d'environ 0,38 rad vers la
  caméra.
- (cycle 53) Un 9:16 ne tient pas côte à côte un personnage qui marche, une porte au fond et un camion : longue focale de loin
  (18 m, 36°) pour garder la porte grande à côté du personnage.
- (cycle 53) Pages qui tournent : matière opaque pour la vraie page, clone transparent seulement pour les fantômes ; des pages
  transparentes se lisent comme du verre gris.
- (cycle 53) Torse qui se gonfle : `bend.spine` gras (≈ 1,6) avec un léger recul, sinon la tête sort du cadre.
- (cycle 53) Une clé toon doit répéter reach et mains pour chaque main utilisée : changer la main de la poignée oblige à reprendre
  toutes les clés du plan.
- (cycle 53) Visage qui passe par l'entrebâillement : ne jamais pencher le corps vers la caméra (la perspective repousse la tête
  derrière le battant) ; se pencher de côté dans l'ouverture et élargir le battant tant que le visage doit se lire.
- (cycle 53) La clé toon `lay` incline tout le corps alors que les mains restent sur leurs points du monde : 15-20° sur une
  poignée donnent gratuitement un recul et un bras étiré.
- (cycle 53) Lent « non » de la tête qui traverse d'autres clés : clés denses (toutes les 0,067 s) qui portent la rotation, sinon
  chaque clé intermédiaire la casse.
- (cycle 53) Mains posées sur le dessus d'une couette relevée = plateau ; les faire agripper la face avant sous un bord drapé.
- (cycle 53) De dos, des têtes assises n'encadrent une télévision que si elle est plus haute qu'elles (pied haut) ; vue d'au-dessus,
  une télévision basse tombe entre les têtes.
- (cycle 53) Personnage qui doit grandir à l'écran en marchant : le faire marcher dans l'axe de la caméra à mi-distance du fond, en
  longue focale, et remplacer la route vide du premier plan par une bande de trottoir.
- (cycle 54, « La pelle ») `cruise=True` sur une clé de marche extrapole le trajet en arrière avant la clé : les amis partaient
  devant l'objectif et cachaient le héros ; réservé aux traversées.
- (cycle 54) Héros enterré : acteur à y −1,63 avec `headOnly`, `hip: 0`, pas de `sq` du corps (il pivote aux pieds cachés) ; jouer
  avec `scl head` autour du menton et des flexions du cou.
- (cycle 54) Accessoire accroché à une tête mise à l'échelle : il n'hérite pas de `scl head` ; donner aux lunettes ou aux ovales
  leurs propres clés d'écrasement copiées de la tête.
- (cycle 54) Les yeux peints du héros penchent d'environ 30° : lunettes avec roulis −0,55 et centre à 0,31 au-dessus du menton.
- (cycle 54) Le bronzage passe par le canal `skin` du toon ; les ovales pâles se dessinent par-dessus le visage, yeux redessinés.
- (cycle 54) Couches de mer et de sable mouillé sur la prairie : opaques et sans test de profondeur ; une couche transparente est
  dessinée après les acteurs et les recouvre.
- (cycle 54) Cacher les arbres de la prairie depuis l'update d'un accessoire (`rt.traverse`, nom 'tree'), sinon ils poussent dans
  la mer.
- (cycle 54) Pelle accrochée à une moufle = couchée le long de l'avant-bras (deux bâtons croisés devant le visage) ; accessoire
  libre dans le monde avec clés copiées des points d'atteinte.
- (cycle 54) La génuflexion toon garde les hanches hautes : enfoncer de 0,3 m un figurant agenouillé pour sortir sa tête de la
  bande des cartes.
- (cycle 54) Cible de regard proche ou sous la tête d'un figurant = tête roulée à 90° (« cou cassé ») ; `look='camera'` ou cible à
  hauteur de tête.
- (cycle 54) Caler les temps de pose d'un objet sur la durée du plan : la pierre tombale se posait 0,1 s après la coupe.
- (cycle 54) Foule alignée en profondeur vers la caméra = elle se cache elle-même ; recherche caméra avec une boîte x par tête
  (16 % d'écart), résolu en une passe.
- (cycle 54) Héros enterré dont le soleil est derrière la pierre : son visage n'est jamais au soleil ; simuler « l'ombre lui tombe
  dessus » avec une lumière chaude cachée sur le visage qui s'éteint quand l'ombre arrive.
- (cycle 54) Mouettes qui tournent au-dessus d'une caméra basse = grandes ombres floues qui balaient le sable ; pas d'ombre, et
  loin au-dessus de la mer.
- (cycle 54) Figurant posé là où l'accessoire ira ensuite : il fait de l'ombre au héros avant et tue le moment ; le faire sortir
  de l'axe du soleil.
- (cycle 54) Deux porteurs d'une dalle : de profil, face à face ; de face, les manches noires disparaissent sur les costumes noirs.
- (cycle 54) Acteur qui entre avec des reach pointés vers sa place finale = bras étirés à travers l'image ; reach vides jusqu'à
  l'arrivée.
- (cycle 54) Lunettes baissées d'une valeur fixe : sur une tête étirée elles restent sur les yeux ; prise avec tête agrandie =
  descente plus profonde.
- (cycle 54) Affaissement d'un enfant avec un reach vers un point fixe du monde : le bras s'étire quand il repart ; reach vides
  pour les affaissements et les sorties.
- (cycle 54) Accessoire noir sur serviettes sombres = invisible ; serviettes de deuil à rayures claires pour que maillots et ballon
  noirs se lisent.
- (cycle 54) Foulard sur une figurante aux longs cheveux clairs : les cheveux traversent le dessus ; assombrir les cheveux.
- (cycle 53) Couche transparente dessinée sans test de profondeur (tache au sol en canvas) : elle couvre tous les acteurs sur son
  emprise ; anneaux opaques dessinés en premier.
- (cycle 53) Plan délavé : soupçonner d'abord le dernier accessoire transparent ajouté (test en le retirant), pas l'exposition auto.
- (cycle 53) Caméra garée loin dans une prairie enneigée : elle peut se trouver dans un arbre blanc et blanchir l'image.
- (cycle 53) De dos, une tête-boîte ne se lit comme une personne qu'avec des cheveux contrastés avec la veste, une nuque nue et une
  oreille ; caméra haute, têtes dans le quart bas.
- (cycle 53) Personnage assis dans une télévision vue d'au-dessus : il se cache derrière le bord haut ; baisser le décor intérieur
  ou agrandir le poste, vérifier la tête avec project().
- (cycle 53) Camion vu de l'arrière : caisse creuse, sinon les cartons à l'intérieur ne se voient jamais ; portes ouvertes à
  ≈ 265° pour qu'elles se rabattent à plat sur les côtés.
- (cycle 53) Étirement du corps (`sq` y > 1) d'un personnage assis au lit : les genoux traversent la couette ; étirer la tête
  (`scl head`).
- (cycle 54) Étoile de mer posée au centre d'un monument funéraire = étoile rouge politique à taille téléphone (et la coquille
  Saint-Jacques rappelle une marque) ; aucun motif sur un monument : boule ou tourelle de sable unie.
- (cycle 54) Pages de calendrier qui s'envolent : dos vierge, sinon le mois se lit à l'envers en écriture miroir.
- (cycle 54, session 87 « La fuite ») Accessoire imbriqué dans un autre : il n'est pas animé si le parent ne le pilote pas (ruban
  invisible).
- (cycle 54) Les clés de main ne partent qu'à leur propre temps : sur un acteur qui marche, une clé toutes les 0,2 s visée en
  avant, sinon l'objet sort du cadre.
- (cycle 54) Objet porté = accessoire séparé, pas attaché à la main : attachée, l'assiette se présentait toujours par la tranche.
- (cycle 54) Coulée de béton : arc de gravité depuis une goulotte en haut du cadre, sinon elle se lit comme un tuyau horizontal.
- (cycle 54) Coin de frigo qui dépasse : grand, incliné, avec joint, sinon il se lit comme un micro-ondes.
- (cycle 54) Vérifier les affirmations des critiques sur les images rendues avant de corriger.
- (cycle 54) Les accessoires de tête disparaissent quelques images quand un mouvement `to` commence après l'apparition de l'acteur.
- (cycle 54) draft.sh régénère scripts-fr/story_X.json : le commiter ensuite.
- (cycle 54) Ombres VSM (look natural) : three.js dessine aussi les maillages qui REÇOIVENT l'ombre dans la carte d'ombre ; une
  tache floue ne part qu'avec castShadow ET receiveShadow coupés (`plNoShadow`).
- (cycle 54) Accessoire plat à quelques cm au-dessus du grand plan de sol : il clignote image par image ; décalage de polygone
  (`plTowel`), pas y + 0,02.
- (cycle 54) `off(p, ry, f, s)` : s > 0 = droite du personnage ; une main droite avec s négatif traverse le corps.
- (cycle 54) Double prise serrée par une ligne courte : poser la mise en place sur ~60 % du plan, travelling avant pour la prise, et
  faire sortir le figurant qui serait coupé au bord pendant le travelling.
- (cycle 54) Figurants allongés vus d'une grue : torsion du cou ≈ 1 rad plus un regard gx pour un mouvement de tête synchronisé ;
  0,5 rad ne se voit pas.
- (cycle 54) Réutiliser l'accessoire d'une autre histoire avec un changement : l'envelopper dans un accessoire préfixé qui importe
  son export, sans toucher le fichier de l'autre histoire.
- (cycle 54) Gag peint sur le visage (marques de bronzage, maquillage) : dans la texture du visage elle-même — copier le canvas du
  visage à chaque image après l'évaluation des acteurs, modifier la copie, échanger la map ; découpé au visage, éclairé comme lui,
  paupières conservées. Restaurer la texture quand l'accessoire part.
- (cycle 54) Éclaircir la peau sous le trait sans l'effacer : multiplier chaque pixel par cible/peau avec un poids qui protège
  l'encre ; l'encre reste sombre, le blanc des yeux sature à blanc.
- (cycle 54) Lunettes relevées sur les cheveux : hauteur qui suit l'écrasement de la tête et branches repliées, sinon elles flottent
  ou pendent en barre à côté du visage.
- (cycle 54) Pages de calendrier arrachées : petites feuilles séparées qui tournent et disparaissent en ≈ 0,3 s ; des pages qui
  restent se lisent comme un panneau vide.
- (cycle 54) Enseigne d'un accessoire coupée par le bord du cadre = mot cassé (« GLA ») : la vider ou déplacer l'accessoire.
- (cycle 54) Bras élastiques tendus loin vers l'objectif : ils s'affaissent en barre diagonale sauf avec `hose` à 0 et les deux mains
  sur le bord proche.
- (cycle 54) Palier de bronzage : le mesurer contre la lumière de chaque plan ; une lumière chaude sur le visage annule un pas de 0,06.
- (cycle 55, « La tartine ») Le preset `lemec` garde son costume marine quel que soit `suit` ; héros dans une autre couleur :
  `lemec_charcoal` avec `atlas: 'lemec', atlasBody: False`.
- (cycle 55) Étiquette de cou fixée au torse à z 0,165 : elle disparaît dans la veste des agents agenouillés à l'échelle 0,78 ;
  l'avancer d'environ 0,1 m.
- (cycle 55) Rabat de nappe soulevé : il pivote vers l'extérieur et cache la poitrine de celui qui est agenouillé devant ; le
  laisser baissé quand une étiquette doit se lire.
- (cycle 55) Objet tenu (chronomètre) dans la moufle de son côté ; la moufle opposée traverse la poitrine et cache l'étiquette.
- (cycle 55) Corps allongé dans l'axe de la caméra, vu d'une caméra haute de face = debout en 9:16 ; une suspension en l'air demande
  une vue de côté ou de trois quarts.
- (cycle 55) Personnage tombé à plat à une coupe (`splat` avec `popAt: 99`) et relevé dans le plan suivant depuis le clip `splat`,
  pour que les deux plans raccordent.
- (cycle 55) Tartines au sol : points d'atterrissage ≈ 0,5 m plus près de la table que de la caméra, sinon elles tombent dans la
  bande des sous-titres ; beurre lisible d'en bas seulement avec la tartine inclinée ≈ 0,9 rad vers l'objectif ; anneau
  d'éclaboussure plus large que la tartine.
- (cycle 55) L'outil de planche plante sur un cards.txt vide : filtrer les entrées sans '@'.
- (cycle 55, session 87 « Le régime ») Le prop `suitcase` disparaît avec une échelle à trois valeurs : vérifier qu'un accessoire
  mis à l'échelle s'affiche, sinon en faire un propre.
- (cycle 55) Objet passé de main en main = UN seul accessoire qui suit la main puis reste posé ; une copie portée plus une copie
  posée donnent deux objets à l'écran au transfert.
- (cycle 55) story_kit arrondit les coupes à 4 décimales (242/30 → 8,0667, après l'image) : la première image du plan montre le
  plan précédent ; caler chaque coupe juste sous son image dans le script de l'histoire.
- (cycle 55) Personnage « autre » (président) qui réutilise l'acteur du héros = copie ; modèle distinct (silhouette et visage) dès
  le premier brouillon.
- (cycle 55) Chute de statue : socle et tige dans le cadre, anticipation, arc vers la caméra, rebond suspendu ; poussière après le
  rebond, jamais dessus.
- (cycle 55) Rayures peintes sur une moufle = visage de grenouille ; moufle unie.
- (cycle 55) Scène éclairée par un objet (appareil à raclette) : l'objet est la lumière principale, pas une porte surexposée.
- (cycle 55) Respirations de maintien d'un personnage très rond trop petites pour le détecteur de figés : ajouter une poussée de
  caméra lente.
- (cycle 55) Vérifier les points récurrents sur des images isolées extraites du brouillon, la planche réduite ne suffit pas.
- (cycle 55) Avant un deuxième mouvement `to`, l'acteur se penche et se tourne vers sa cible quelques images plus tôt ; pour quelqu'un
  qui rampe sous une table la tête traverse le plateau : un seul mouvement, changements de pose par clip et clés toon.
- (cycle 55) Tourner un corps penché par `lay` : clé toon `yaw`, pas un changement de facing (il balance le corps vers l'objectif).
- (cycle 55) Ramper sous une table : clip kneel, `lay` ≈ 0,56 plus spine 0,5 et neck −1,0, départ enfoncé ; la flexion du dos seule
  laisse le héros trop grand pour 1,04 m.
- (cycle 55) Passer au clip `splat` avec un `lay` encore appliqué : le corps bascule vers une caméra haute pendant une image ; fondre
  clip et retour du lay ensemble sur ≈ 0,12 s, linéaire.
- (cycle 55) Moufle qui tient un objet par le centre = cadran caché ; prise sous et derrière l'objet, tapes sur le bord.
- (cycle 55) Cravate qui pend sur l'étiquette de cou : `tieHide` sur chaque clé toon de ceux dont l'étiquette doit se lire.
- (cycle 55) Pieds de chaise et glissade derrière une nappe vus d'une caméra basse : nappe raccourcie (`ttTable` `gap` ≈ 0,6).
- (cycle 56, « La poule ») Cible de regard sous la tête d'un acteur penché ou agenouillé : la tête roule de 60-90° ; viser
  lerp(cible à hauteur de tête, caméra, 0,4).
- (cycle 56) Preset médecin : glasses False quand on lui donne des lunettes ou un miroir frontal, sinon deux paires.
- (cycle 56) Animation de chute interne d'un accessoire (tas) + chute dans le monde = chute doublée ; option dropH 0.
- (cycle 56) Dents dans un bec fermé : elles traversent le bec supérieur effilé ; ne les montrer que bec ouvert. Dent en or sur bec
  jaune = invisible : bec inférieur assombri, dent en or devant.
- (cycle 56) Porte peinte sombre dans un mur plein : elle cache les acteurs derrière ; découper une vraie ouverture avec un renfoncement.
- (cycle 56) Chaise pliante portée attachée à la main : elle cache le visage en marchant ; l'attacher au flanc du torse, face caméra.
- (cycle 56) Enseigne plus large que le cadre à sa profondeur = mot coupé (« MUTUELL ») ; option de largeur, vérifier chaque plan.
- (cycle 56) Recherche caméra : boîtes x par tête ET distance maximale, sinon elle recule jusqu'à rendre les dents illisibles.
- (cycle 56) Cinq voisins dans une rangée de maisons en 9:16 : façades étroites (1,6 m) et caméra lointaine à 45°.
- (cycle 56) Bouche du héros en surimpression : sur l'articulation de la tête à (y 0,12, z 0,1, 0,21 × 0,105 m), pile sur la bouche
  peinte. Prises du héros bouche fermée quand la bouche est un gag (doubleTake de story_kit ouvre la mâchoire).
- (cycle 55) Le canal `lay` pivote aux pieds et le clip `splat` aux hanches : décaler la racine d'une longueur de hanche au
  changement, sinon le corps saute d'≈ 1 m vers l'objectif (« visage géant »). Image d'impact d'un corps couché à plat : le relever
  de ≈ 0,12, sinon la moitié passe sous le sol.
- (cycle 55) `ttShine` avec un fort décalage de polygone peint par-dessus les éclaboussures au sol en rasant ; décalage réduit quand
  des accessoires au sol doivent se voir.
- (cycle 55) Reflets au sol : quadrilatères en dégradé peints dans le canvas du brillant pour une caméra donnée ; un décalque séparé
  ne s'est jamais affiché.
- (cycle 55) Caméra basse sous une table : personnage assis renversé ou coussin derrière lui = tête cachée ; coussin sur le côté.
- (cycle 55) Panneau mi-ton devant une fenêtre : bleu-gris = vitre ; ton chaud avec grille = graphique.
- (cycle 55) « Yeux levés » dans un plan final : les yeux seuls (gy −1, paupières ouvertes) ; une cible qui renverse la tête montre
  le dessus du crâne.
- (cycle 55) Tête maintenue écrasée sous un plateau : une seule montée verticale avec couches automatiques coupées, et le corps qui
  rampe reste enfoncé tout du long.
- (cycle 55) Enseigne au-dessus d'un store coupée par le haut du cadre : écrire le mot sur la vitrine.
- (cycle 55) story_kit réécrit shots.json, cues.json et cards.txt à chaque exécution : vérifier que les fenêtres de plans restent
  identiques à l'octet.
- (cycle 56) Portes qui s'ouvrent à ≈ 109°, vues le long d'une rangée = mur de panneaux qui cache la rangée ; les rabattre presque à
  plat contre la façade (≈ 3,06 rad) avec un rebond.
- (cycle 56) Deux mains sur un objet plat tenu : le long de l'axe de largeur de l'objet, pas de l'axe X du monde.
- (cycle 56) Traction au bras élastique : tirer le point de traction de côté à travers le cadre, à hauteur de poitrine et à la
  profondeur du tenant ; vers l'objectif, l'étirement se perd en raccourci.
- (cycle 56) Cible de regard vers un partenaire : un corps de trois quarts repasse de profil ; viser à ≈ 60 % vers l'objectif et
  pousser les pupilles (`gx`) vers le partenaire.
- (cycle 56) Moufle douloureuse levée pour souffler dessus = visage caché ; la tenir de côté à hauteur du menton, étoiles accrochées
  à la main.
- (cycle 56) Canne à pêche pointée en l'air = hors cadre ; tenue de côté et affaissée autour de son z, elle tombe dans le plan de
  l'image.
- (cycle 56) Poussière : icosaèdres translucides à opacité décroissante ; sphères opaques = balles ; poussière qui monte = visage
  du souffleur caché.
- (cycle 56) Plan final 9:16 avec hublot, cochon et héros : ≈ 1,8 m de largeur (caméra 4,5-5 m, focale 40) ; avancer le hublot
  vers la caméra pour qu'il soit à côté de la tête du cochon.
- (cycle 56, « La tartine ») Corps suspendu en l'air vu d'une caméra haute de face : un lacet toon d'environ 0,7 et une bascule au-delà du plat (≈ −1,86) le rendent horizontal à l'écran ; ajouter une ombre de contact et garder aussi les images de chute en lacet.
- (cycle 56) Retourner un graphique montant de 180° garde sa pente : le mettre aussi en miroir pendant qu'il tourne, et peindre une pointe de flèche dans le tableau.
- (cycle 56) Plusieurs corps qui glissent en 9:16 : des diagonales parallèles en échelon, trouvées par une recherche d'écarts, se lisent séparées ; des couloirs dans l'axe de la caméra se fondent.
- (cycle 56) La place pour séparer des objets au sol dépend de la hauteur de caméra : objectif bas, les rangées en profondeur s'écrasent sur une seule bande.
- (cycle 56) Les reflets au sol d'objets proches de l'objectif bavent en bas du cadre : réserver les éléments réfléchis au fond du décor.
- (cycle 56) Une bande brune en haut d'un plan rapproché vient d'un mur trop bas : rehausser le mur.
- (cycle 56) Une cible de regard sous une tête écrasée la fait basculer comme un couvercle : ne bouger que les yeux (gx/gy).
- (cycle 56) Un scintillement du sol d'une image à l'autre dans un rendu séquentiel peut ne pas apparaître sur des vues fixes : le mesurer sur les images du brouillon.
- (cycle 56) Un bras élastique qui arme en visant au-delà d'un autre acteur laisse un coude à angle droit sur son corps : armer au-dessus de la cible, de son propre côté.
- (cycle 56, « La poule ») Deux personnages qui s'écrasent sur la même image se lisent comme un saut de caméra (un zoom) : décaler les impacts d'au moins deux images, ou n'écraser que celui qui encaisse.
- (cycle 56) Une poule (un bec saillant) filmée d'en dessous cache ses yeux derrière le bec et les dents : caméra à hauteur des yeux ou un peu au-dessus, sans plisser les yeux sur la pose du sourire.
- (cycle 56) En 9:16, le cadre ne tient pas trois éléments en ligne (hublot, cochon, héros) à 50 % de la hauteur : ramener le décor derrière le sujet (glisser le hublot le long de la paroi) au lieu d'élargir ; vérifier avec `fit()` avant de rendre.
- (cycle 56) Un nuage translucide devant un corps se lit comme un fantôme : des bouffées opaques et cernées, au ras du meuble, qui rétrécissent jusqu'à rien au lieu de s'effacer.
- (cycle 56) Mâchoire qui tombe quand la bouche ne doit plus montrer de dents (gag de dents qui compte les apparitions) : `face.jawTeeth: 0` ouvre une cavité vide.
- (cycle 56, session 87, « Le pardon ») Le rig cartoon ignore les rayures et couleurs de tenue : un costume rayé est un accessoire peint posé sur le torse, sinon les détenus sortent en costume.
- (cycle 56) Des clés « path » avec rotation le long du chemin ne déplacent plus l'acteur après le premier segment : enchaîner des clés « to » avec leurs rotations.
- (cycle 56) Twist « c'est lui » : le corps caché du coupable a la même silhouette que le personnage révélé (corps rond, tête détournée), jamais un torse générique.
- (cycle 56) Un flash « doux » en halo devient un disque gris plat : petits rayons blancs au bord du cadre, jamais devant un visage.
- (cycle 56) Les cibles de main d'un acteur qui tombe restent en l'air si elles ne descendent pas avec lui (les bras se lisent comme des jambes) ; une chute qui finit à pleine vitesse donne une image « tête au sol ».
- (cycle 56) Une carte de titre peut couvrir le gag précis (le cran d'une horloge) : vérifier la bande de la carte sur l'image du gag et recadrer.
- (cycle 56) Jambes assises qui traversent une cloison de box : reculer l'acteur dans un box plus profond.
- (cycle 56, atelier 106) Pièges des décors et accessoires existants dont le contenu par défaut enfreint les règles :
  - Décor salle de classe : le tableau affiche « 6 + 7 = 67 » par défaut, et une chaîne vide rétablit ce défaut. Mettre une espace ou un dessin.
  - Décor hôpital : il accroche une croix rouge sauf avec `cross: false`.
  - Avis et ticket d'amende : ils impriment « 135 € » (et « AMENDE »).
  - Billets : `money` porte un « $ » et `banknote` imprime « 100 ». Faire des feuilles vertes unies ou à motifs.
  - Croix de pharmacie : elle alterne avec une température en chiffres. Ne pas la réutiliser.
  - Décor mairie : il a une banderole tricolore et un drapeau. Il ne peut pas servir de place de village.
  - Vérifier les options par défaut de tout décor réutilisé avant le premier brouillon.
- (cycle 56, « La tartine ») Ne jamais poser un plan décoratif quelques millimètres au-dessus du grand sol de 300 m sans polygonOffset. Exemple : le carrelage de `kitchenDay`, posé à 3 mm. Sous SwiftShader, la profondeur de cet immense quad découpé dérive de plusieurs millimètres, et le sol uni recouvre tout le carrelage environ une image sur dix, selon la caméra et la définition.
  - Ajouter `P('carrelage', 'ttTileOffset')` (props_tartine) à chaque plan `kitchenDay` : 13 autres histoires utilisent ce décor.
  - Tout ce qui est posé à plat au sol prend un polygonOffset (ttSplat, ttShine).
  - Vérifier le sol image par image sur une plage rendue en continu, pas sur des images fixes isolées.
- (cycle 56, « La poule », passe finale) En 9:16, un plan taille et un étirement en travers du cadre s'excluent : la largeur limite tout. Choisir l'étirement (plan large, mur clair derrière le bras) ou le plan taille, et le mesurer avec project() avant de rendre.
- (cycle 56) Un étirement dans la profondeur vu d'une caméra haute ne gagne presque rien à l'écran (environ 1,3 fois) : il faut une vraie distance latérale entre l'épaule et la main.
- (cycle 56) Un accessoire fin (une canne de 2 cm) disparaît à 8 m : l'agrandir pour le plan (`scale`), et le porter dans le monde plutôt qu'à la main quand la main sort du cadre.
- (cycle 56) Une poussière faite de boules qui se dispersent redevient des boules en rétrécissant : la faire se resserrer vers son cœur en disparaissant.
- (cycle 56) Écraser tout le corps (`sq`) enfonce la tête dans le col : écraser aussi la tête (`scl head`), allonger le cou (étirement de `bend neck`) et le pencher vers l'avant pour garder le visage vers nous.
- (cycle 56) Allonger le cou d'un personnage filmé de face le fait monter, pas suivre un objet qui vient vers la caméra : déplacer l'objet en travers du cadre, sinon renoncer.
- (cycle 56) Cheveux bouclés rendus comme une plaque plate au-dessus de la tête : passer à une coiffure plaquée (`slick`) et vérifier la bande de la carte de titre sur ce plan.
- (cycle 57, session 87, « Le mot ») `build_hf.py` cassait sur un point après un guillemet fermant (« pin-pon ».) : corrigé, le « . » ou la « , » isolés se rattachent au mot précédent. Si un autre signe casse, le mettre dans les guillemets dans le texte.
- (cycle 57) Le helper de placement des mains ajoutait deux fois la hauteur du sol de l'acteur : tout personnage sur une estrade ou un plateau de camion levait les mains. Vérifier les mains d'un acteur surélevé.
- (cycle 57) Un « chut » ne se lit qu'avec l'index vertical en travers du milieu de la bouche, visage vers la caméra : près de l'oreille, c'est un téléphone ; levé, c'est un vote.
- (cycle 57) Rayures multicolores sur un accessoire : à éviter (lecture de drapeau ou de symbole) ; un cône orange et blanc se lit comme un plot de signalisation.
- (cycle 57) Une goutte de sueur sous une visière, devant l'œil, se lit comme un monocle : la poser sur la tempe, détachée.
- (cycle 57) Un écrasé-regonflé doit montrer la crêpe 3-4 images à découvert, sinon il se lit comme « enseveli ».
- (cycle 57) Un objet qu'on berce se couche en travers des deux bras, sinon il se lit comme un sac à dos.
- (cycle 57) Les dormeurs d'un immeuble en coupe sont trop petits pour porter un gag d'accessoire : pousser la caméra jusqu'à la taille d'une tête.
- (cycle 57, « La notice ») Le correctif « coupe juste sous l'image » de la poule ne fait rien : st.cut arrondit déjà à 4 décimales (53/30 → 1,7667, après l'image). Repartir de l'indice d'image : floor(round(t·30)/30·10⁴)/10⁴.
- (cycle 57) Une fonction d'aide qui reçoit **o pour les opts avale aussi `keys` (la boîte ne bougeait jamais). Sortir `keys` en paramètre nommé dans chaque fabrique d'accessoire de l'histoire.
- (cycle 57) Papier ou drapé posé sur le dessus d'un accessoire (falaise, dalle) : le décoller de 5 cm, sinon la couleur du dessous perce en grandes taches. Un texte lu « depuis le bord » doit courir vers −X pour une caméra côté mer : vérifier le sens sur une image.
- (cycle 57) Têtes au bord du cadre : donner à fit() une marge de 0,12 à 0,2. La marge porte sur le centre de la tête, et 0,05 laisse la moitié du visage dehors.
- (cycle 57) Les cartes de titre posées sur un plan à suffixe (S05b, S12b) cassaient le découpage de cards.txt. L'expression `,(?=S\d+@)` ne coupait pas avant « S12b@ ». Corrigé en `,(?=S\d+[a-z]*[@:])` dans build_hf.py, make_project.py (stories7 et pipeline), make_config1.py et make_critic.py. Tout nouvel outil qui lit cards.txt doit accepter ces suffixes.
- (cycle 57, « La notice ») Deux boîtes dont les faces du dessus sont dans le même plan (herbe et roche de la falaise, toutes deux à y 0) clignotent comme un sol posé à 3 mm : abaisser la boîte du dessous de 10 à 15 cm. Le mesurer sur une plage rendue image par image (`--range`, 30 i/s), en comparant d'une image à l'autre quelques carrés de fond.
- (cycle 57) Le clip `crawl` et `bend spine` au-delà d'environ 0,6 ne marchent pas avec le rig toon et une main guidée : le personnage tombe sur le dos, sous le sol, ou reste droit. Pour « à quatre pattes » : tibias repliés (`shin` 1,55), `lay` 0,55, cou en arrière (−1,0), acteur descendu de 0,3 m. Vérifier avec `debugJoints`.
- (cycle 57) Une clé de main au point `off(p, ...)` d'un acteur posé sur une marche compte deux fois la hauteur de la marche quand `p` porte déjà ce y : donner une hauteur relative au sol (0,95), pas `LAND + 0,95`.
- (cycle 57) Un ciel en papier qui « se retire » en 2 images doit balayer la partie visible en 4 à 6 images : calculer la position de son bord dans le cadre et poser les clés sur ces positions, pas sur la durée totale.
- (cycle 57) Un json de débogage au nom court (`dbg.json`) écrit dans `out/work/<nom>` et peut écraser un autre dossier de travail : préfixer chaque json de débogage du nom de l'histoire.
- (cycle 57, « La notice ») En 9:16, cinq personnages ne tiennent côte à côte que s'ils sont étagés en profondeur, avec une caméra éloignée et un objectif plus long : ils ont alors à peu près la même taille et des écarts lisibles.
- (cycle 57) Une pose de gag (le crabe) vient des jambes. Une pose tenue (clip `pose` : genoux écartés, corps abaissé) sous les clés toon se lit mieux qu'un écrasement du corps entier. Pour une pince qui claque, un accessoire tourné vers l'objectif vaut mieux qu'une forme de moufle.
- (cycle 57) Pour qu'un geste vers un décor se lise (taper le ciel), rapprocher le décor du personnage pour ce plan au lieu d'allonger le bras à l'infini.
- (cycle 57) Un personnage secondaire (ministre) habillé comme le héros (costume sombre, cravate rouge, tête haute en boîte) se lit comme « ce mec » au téléphone : lui donner un autre costume, une autre cravate, une autre silhouette.
- (cycle 58, session 87, « Le composteur ») Une étiquette rouge unie avec un disque blanc centré se lit comme un drapeau : trou décentré, coins arrondis.
- (cycle 58) Un outil en L tenu à l'horizontale vers quelqu'un se lit comme une arme en plan large : pince à deux branches, tenue vers le haut.
- (cycle 58) Des flammes devant un personnage le font lire « dans le feu » : écarter les gens du foyer, flammes basses, langues arrondies plutôt que cônes (des cônes se lisent comme des plots).
- (cycle 58) Une casquette posée à hauteur des yeux coupe la tête-boîte : visière au-dessus des yeux peints, sinon le personnage perd son regard et ses clignements.
- (cycle 58) Le helper de remise d'objet ajoutait sa propre clé à 0 s et écrasait la pose d'ouverture (bras levé au-dessus de la tête) : vérifier la première image de chaque plan avec remise.
- (cycle 58) Des yeux exorbités en disques noirs se lisent comme des lunettes de soleil : grands blancs, petites pupilles.
- (cycle 58) Ne pas lancer build.sh des critiques pendant qu'un brouillon rend : la construction des images fixes échoue en silence et les critiques jugent sans elles. Vérifier que frame_s*.jpg existent avant de lancer les critiques.
- (cycle 58, « Le sel ») En 9:16, deux personnages à angle droit (lui en bout de table, un convive sur le côté) ne tiennent pas ensemble de près : filmer dans l'axe de la table, ou tourner un peu le convive vers l'objectif.
- (cycle 58) Une bouffée blanche opaque qui passe devant un visage se lit comme des yeux exorbités : rien de blanc et rond à hauteur de visage.
- (cycle 58) Une salière qu'on incline doit tourner autour de la prise, pas autour de sa base : calculer la base à partir de la prise et de l'angle, puis guider la main sur la prise.
- (cycle 58) Depuis l'intérieur, une porte ouverte réduit le champ à son embrasure : tout ce qui se penche hors de la file se penche du côté libre, jamais derrière le battant.
- (cycle 57, « La notice », passe finale) Cadrage coupé aux genoux avec la caméra à hauteur des ventres : tous les ventres tombent à la même hauteur de l'image, quelle que soit leur distance. C'est la profondeur, pas l'alignement, qui fait tenir plusieurs personnages.
- (cycle 57) Un panneau lointain passe sous les têtes proches dès que la caméra descend : vérifier la hauteur du panneau avec `project()`, monter la façade pour ce plan si besoin.
- (cycle 57) Rapprocher un objet de la caméra le long de l'axe de visée ne le déplace pas dans l'image : pour qu'un geste « vers l'objectif » se lise, le décaler aussi en travers ou en hauteur.
- (cycle 57) Les épis de cheveux viennent du vent apparent d'un saut ou d'une course, pas d'une clé : pour un personnage dont la silhouette compte, mettre `cloth` à 0 ou 0,12 dans son casting.
- (cycle 58, atelier 111) Autres pièges des décors et accessoires existants dont le contenu par défaut enfreint les règles :
  - Décor `lab` : le tableau affiche toujours « C10H15N », « 99,1 % » et « T 80°C / 4 h », sans option pour l'enlever. Le masquer avec un accessoire (comme seHideSet dans props_sel) ou poser un tableau à soi devant.
  - Décor `office` : le tableau affiche « OBJECTIFS Q3 » et « +12% ».
  - `poste` : affiche « GUICHET 1/2/3 » et un ticket « 4000 ».
  - Décor `bank` : le distributeur affiche « INSERT CARD », en anglais.
  - `medal` : ruban bleu-blanc-rouge.
  - `globe` : petit drapeau rouge au sommet.
  - `parachute` et `parachuteSky` : parachutistes militaires olive.
  - `elevator` : afficheur d'étage chiffré.
  - `centCoin` : imprime « 1 CENT ».
  - Cinq personnes qui lèvent toutes un bras tendu se lisent comme un salut : ne jamais faire lever le bras droit à l'unisson.
  - Un sceau rouge uni centré sur un certificat blanc se lit comme un drapeau.
- (cycle 58, « Le sel ») Un sol de décor qui chevauche une route ou une allée à quelques millimètres clignote : percer le disque du sol sous les bandes (`seGroundCut` dans props_sel), plutôt que de déplacer les acteurs. Mesurer d'image en image sur une plage rendue à 30 i/s, en comparant chaque bloc à l'image d'avant et d'après.
- (cycle 58) `lens` est un angle vertical, pas une focale : en 9:16, une scène large à trois personnages demande 55 à 70, ou un point d'appui symétrique dans `fit()` pour centrer l'accessoire.
- (cycle 58) Une porte « ouverte » vers l'intérieur se dresse en travers de la pièce : avant de mettre en scène près d'elle, la faire ouvrir vers l'extérieur.
- (cycle 58) Un genou à terre vu de face ressemble à des jambes droites : tourner le personnage d'environ 40°. Une chaise attachée au torse à la mauvaise hauteur cache le visage : vérifier chaque objet porté sur une image avant de juger la pose.
- (cycle 58) Si HyperFrames refuse la composition faute de place (« Low disk space », moins d'1 Go), le calque 3D d'environ 2 h est déjà dans hyperframes/NNN/assets/layer3d.mp4 : ne pas relancer queue11. Libérer de la place (doublon out/story_X_3d.mp4, out/work/story_X_render), puis lancer seulement `npx hyperframes@0.9.13 render -o renders/X.mp4 --fps 30` dans le projet. hf_only.sh recopie out/story_X_3d.mp4 : ne pas l'utiliser si ce doublon a été supprimé. Avant une finale, prévoir au moins 1,3 Go libres, cache d'extraction compris, car le rendu 3D et l'audio consomment environ 200 Mo avant la composition.
- (cycle 58) Un agent de correction qui annonce « corrigé » sans image à l'instant précis cité par le critique peut se tromper (la rallonge de S12b flottait encore au tour suivant). Exiger des images fixes aux instants cités, et la liste des instants vérifiés dans le compte rendu.
- (cycle 59, histoire 108) Une tête posée au bord d'un trou à côté d'un costume enterré se lit comme une tête coupée : enterrer le personnage jusqu'à la taille, épaules, col et tête d'un seul bloc, le cou caché dans le col.
- (cycle 59) Bleu et blanc avec un col rouge se lisent comme un drapeau tricolore. Une règle « pas de rouge » se viole avec un seul coussin : faire la liste de chaque rouge du plan avant le rendu.
- (cycle 59) Une fourche tenue à l'horizontale se lit comme un fusil : la tenir verticale, dents visibles. Une sardine sans œil ni queue fourchue se lit comme une lame de couteau.
- (cycle 59) Des dômes vus d'en dessous avec des cordes pendantes se lisent comme des méduses ou des parachutes : faire voler les tentes de côté, cordes traînant derrière.
- (cycle 59) Des éclairs nocturnes plein cadre déclenchent le contrôle des chutes de luminosité : éclaircir brièvement la nuit à la place.
- (cycle 59) Un figurant à tête carrée et cheveux noirs passe pour le héros : donner aux figurants un chapeau et d'autres couleurs.
- (cycle 58, histoire 109) Un « carré translucide » dans un plan enneigé peut être un flocon à quelques centimètres de l'objectif. Déplacer les points dans `onBeforeRender` arrive une image trop tard : les écarter de la caméra dans le vertex shader (seSnowClear).
- (cycle 58) Un objet porté flotte quand les mains le lâchent avant qu'il tombe, pas parce que la cible des mains est fausse : garder les paumes ouvertes à sa hauteur deux images, puis une chute de moins de 0,15 s, un claquement et un rebond.
- (cycle 58) Avant de retoucher un objet que le critique dit « invisible », projeter sa position à l'écran : la rallonge de S04 était là depuis le début, cachée derrière la tête du héros.
- (cycle 58) Un camion se reconnaît à trois signes vus ensemble : un bout de pare-brise, l'arche de roue et l'intérieur éclairé de la cabine. Un volant sous le rebord de la vitre ne se voit pas : le remonter.
- (cycle 59, histoire 111) Une barrière vue dans l'axe de la caméra disparaît : en vue subjective, la tourner d'environ 40° et faire venir le saut en diagonale vers l'objectif.
- (cycle 59) Un personnage noir la nuit ne se lit qu'en silhouette : la lune juste derrière sa tête, ou une lumière d'appoint sur son visage.
- (cycle 59) Une foule de laine en blocs facettés à gros contour se lit comme du papier froissé : des lobes ronds, un blanc froid un peu émissif et un contour fin la font lire comme de la laine.
- (cycle 59) Avant de cadrer un accessoire posé dans un décor, vérifier ce que les accessoires d'ambiance placent au même endroit : la rangée de maisons de nuit avalait le toit où se tenait le mouton.
- (cycle 58, histoire 109) Un sol de décor fait d'un seul plan immense (grassland, 9 km, deux triangles) dérive en profondeur sous SwiftShader et repeint par moments un trottoir posé 12 cm au-dessus : dès que la caméra se rapproche, le remplacer par le disque fin troué (`seGroundCut` avec `plane`), puis vérifier le trottoir sur cinq images de suite.
- (cycle 58) Avec une main guidée (`reach`), les `bend` du bras sont ignorés : un bras en caoutchouc reste une planche droite. Pour un long bras qui doit s'affiner et plier au coude, laisser le personnage hors champ, bras au repos, et dessiner une manche à part (tube effilé qui fléchit, manchette, moufle) qui suit la prise image par image (seSleeve).
- (cycle 58) Une main agitée au-dessus de la tête, filmée de face, passe vite devant le visage ou derrière un chambranle : la faire agiter côté libre du cadre, à au moins 0,4 m du milieu de la tête.
- (cycle 58) En 9:16, un plan sur cinq portes est forcément trop large : en montrer trois, laisser les deux autres aux bords, plutôt que d'élargir et de rendre les personnages minuscules.
- (cycle 59, histoire 111) Un saut vu dans l'axe de la caméra se lit comme un bond sur place : faire courir le personnage en travers du cadre, la barrière à environ 55°, prise d'élan d'un côté et réception de l'autre. Pour garder le saut au milieu du cadre, donner à fit() un point miroir de l'accessoire décentré.
- (cycle 59) Un personnage sombre la nuit : un liseré clair (coque en face arrière légèrement agrandie, bleu lune) et une tache de sol éclairée derrière lui valent mieux qu'une forte lumière d'appoint, qui remonte sa couleur jusqu'à celle du sol (contraste 1,4:1 au lieu de 2,1:1).
- (cycle 59) Des lobes à gros contour noir dessinent une fissure à chaque contact, d'où l'effet de papier craquelé : pour de la laine, lobes ronds à normales lisses, motif de boucles et contour fin gris ardoise.
- (cycle 59) Sous les clés toon, plier les genoux (legL/shinL) plie le personnage à la taille : un accroupi d'élan, c'est un écrasement autour des pieds avec le buste penché. Un test `-nt` sur un fichier absent est vrai : attendre la fin d'une tâche, pas la date d'un fichier.
- (cycle 59, méthode) Pour libérer le disque, ne jamais effacer d'images dans critic/<modèle> (le TEMPLATE des configs, ex. feu1) : make_critic y copie style_reference_previous_episode.jpg à chaque revue. Un nettoyage « toutes les images des dossiers critic sauf ceux en cours » l'a effacé et a cassé la revue suivante. Exclure les dossiers modèles, ou garder une copie de cette image ailleurs.
- (cycle 59, méthode) Un brouillon à 15 i/s qui rend pendant une finale à 3 workers prend 95 min au lieu de 35 : ne pas compter sur la durée habituelle quand deux rendus se partagent le processeur.
