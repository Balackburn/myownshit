# Journal des cycles — mise en scène cartoon

Travail autonome et continu : analyse → rigs → animations → histoire → skill → journal, puis cycle suivant. Les types d'histoires et
leur structure ne changent pas (skill `lowpoly-story-style`) ; seule la mise en scène évolue.

Décisions prises sans poser de question (règle : la plus raisonnable, consignée ici) :

- **Skill d'histoires** : `.claude/skills/lowpoly-story-style`. Il nomme deux types d'histoires (le remake d'un short existant à
  partir de son script, et l'histoire nouvelle dans le style) et une structure unique (accroche qui nomme le mec et l'événement
  absurde, logique absurde poussée pas à pas par une institution qui prend tout au pied de la lettre, escalade, retournement, aparté
  sec). Je les respecte tels quels. Les ajouts au skill sont faits en fin de fichier et dans un fichier de référence à part.
- **« Le bouchon »** : la demande d'annulation portait sur `engine/props_bouchon.js` et `scripts-fr/story_bouchon.py` ; ces deux
  fichiers ont été retirés (copie de secours hors dépôt, dans le dossier de travail de la session). La narration déjà enregistrée
  (`stories7/bouchon/lines.json`, `timeline.json`) est conservée (règle : ne supprimer aucun travail existant) et l'histoire reste en
  attente : je ne recrée pas ces fichiers de ma propre initiative. Le cycle 1 produit une histoire nouvelle.
- **Rig cartoon en option** : aucune ancienne histoire ne passe par le nouveau code (`rig: 'toon'` par histoire ou par personnage).
  Après chaque modification du moteur, des images de contrôle des anciennes histoires sont comparées à une référence.

---

## Cycle 1 — « Le trou » (histoire 37)

### 1. Analyse (dernières histoires : La canicule, Le ver de terre, Les chaussettes)

Faiblesses relevées sur pellicules image par image :

1. **Corps rigides** : aucune déformation, ni écrasement ni étirement, membres en barres. → corrigé
2. **Visages en diapositives** : une texture entière remplacée d'un coup, pas de regard, clignement d'une image, sourcils et bouche
   figés entre deux expressions, pas de take. → corrigé (première version du rig facial)
3. **Mouvements sans anticipation ni suite** : départs et arrêts secs, rien qui traîne, pas de respiration. → corrigé (couches automatiques)
4. **Gags trop sages** : aucune chute suspendue, aucun aplatissement, aucun double regard. → corrigé par l'histoire
5. **Silhouettes de profil qui cachent le visage peint.** → traité dans la mise en scène (face ou trois quarts), à poursuivre
6. **Bogue** : `then=<le clip du déplacement>` rejouait le clip (double chute dans La canicule, plan S10). → corrigé dans le moteur

### 2. Rigs

- **Corps** (`engine/toon.js`) : chaque partie longue (colonne, cou, bras, avant-bras, cuisses, tibias) devient une bande qui se
  courbe, se tord et s'étire ; écrasement et étirement du corps entier à volume constant ; tête qui se déforme ; bas du visage qui
  s'étire quand la mâchoire tombe (la bouche peinte s'étire avec) ; yeux sur tiges, langue, vapeur aux oreilles, bosse sur le crâne,
  étoiles autour de la tête ; contrôles secondaires : oreilles, chapeau.
- **Visage** (`engine/facerig.js`, `tools/face/gen_rig.py`) : le visage peint découpé en calques. Au repos, le rig redonne le visage
  mesuré (ses propres sourcils, contours d'yeux, pupilles et bouche sont découpés dans la texture d'origine). Paupières continues
  (dans le style d'origine : un trait plat au-dessus du bas de l'œil), pupilles mobiles, yeux ×0,8 à ×1,9, sourcils (décalage,
  inclinaison, trois formes), 33 formes de bouche, joues, joues gonflées ; 69 expressions (les 56 du jeu de visages + 13 propres au rig).
  Les variantes (teint, moustache, barbe, lunettes, rouge à lèvres) portent le même rig.
- **Vérification des anciennes animations** : images de contrôle de quatre anciennes histoires avant/après. « La file d'attente » :
  0,00 % de pixels modifiés ; les trois autres : 0,52 % au plus, sous le bruit de mesure (0,54 %) du rendu naturel.

### 3. Animations

- **Couches automatiques** : respiration ; écrasement/étirement tirés du mouvement vertical ; colonne qui traîne à l'accélération et
  qui continue à l'arrêt ; membres qui s'arquent dans les gestes rapides ; traînée (smear) au-delà de 5,5 m/s ; chevauchement
  (coudes, mains, tête en retard de quelques images).
- **Micro-mouvements du visage** : le regard précède la tête de 0,07 s et annonce les virages du corps ; petits coups d'œil ;
  clignement sur 7 images (2 pour fermer, 1 fermé, 4 pour rouvrir), parfois double, et un clignement d'élan avant une réaction forte ;
  transitions d'expression en 0,15 s (les sourcils partent d'abord et dépassent, les yeux suivent, la bouche en dernier).
- **25 clips cartoon** : take, double take, départ sur place, traînée, chute suspendue, crêpe, feuille de papier, ballon, bras
  élastique, périscope, accordéon, gelée, bras en nouilles, fonte, élan, marche en lisant, marche en écrivant, marche pompeuse,
  freinage, vacillement, plongeon du cygne, bombe, saut en se pinçant le nez, serré, tampon au téléphone.
- **Clés cartoon depuis l'histoire** : `k(t, toon={...})` (étirer une jambe, un cou, un bras à un instant donné sans écrire un clip).

### 4. Histoire : « Le trou »

Texte (12 lignes, 23,7 s) : Ce mec est tombé dans un trou en allant au travail. / Il a appelé la mairie. / La mairie a répondu : /
« Ce trou n'existe pas. » / Elle a envoyé un agent pour vérifier. / Il est tombé dedans. / Puis un pompier. Pareil. / Puis le maire.
Avec dignité. / Officiellement, ils n'étaient nulle part. / Donc ils ne payaient plus d'impôts. / Alors toute la ville a sauté dans
le trou. / Aujourd'hui, le trou affiche complet.

Structure du skill respectée : accroche (le mec + l'événement), institution au pied de la lettre (la mairie nie le trou), escalade
(agent, pompier, maire), retournement (nulle part = plus d'impôts, toute la ville saute), aparté sec (complet).

Gags visuels (chacun s'appuie sur le rig) : voir le tableau « Catalogue de gags et techniques » du skill. Le gag à répétition est la
chute suspendue, quatre fois, quatre façons (caramel, pierre, vacillement, ascenseur).

Décors et accessoires nouveaux : rue de Paris avec un vrai trou (le sol est découpé : on tombe réellement dedans), coupe du sol
façon dessin animé (strates, tuyau, os, fossiles, une chaussette perdue de l'histoire 36), bureau de la mairie, plan officiel
« AUCUN TROU », dossier tamponné INEXISTANT, tableau NULLE PART, avis d'impôts à 0 €, panneau COMPLET.

### 5. Skill

- `references/cartoon-rig.md` (nouveau) : activer le rig, ce qui bouge tout seul, les canaux, les clips, le rig facial, les tests.
- `SKILL.md` : une ligne d'orientation vers ce fichier, et deux sections ajoutées en fin de fichier : « Catalogue de gags et
  techniques » (17 gags, avec la technique moteur et le plan où ils ont servi) et « Erreurs à éviter » (11 entrées).

### 5 bis. Revue par deux critiques, puis seconde passe (une seule histoire aboutie plutôt que d'enchaîner)

Deux critiques indépendants ont noté l'aperçu : direction artistique **7,2/10**, direction d'animation **6,8/10**. Verdict de l'animation :
« un vrai progrès par rapport aux pantins rigides, mais l'accroche est sous-mise en scène, trois chutes de gag sont dans la bande des
sous-titres, quatre déformations passent en six images, deux gags annoncés sont des images fixes ». Décision (sans poser de question) :
ne pas publier en l'état, reprendre les dix-huit plans, puis rendre une seule fois.

Ce que la revue a fait trouver, au-delà des remarques elles-mêmes :

- **Deux gags ne jouaient jamais.** Un clip à déroulement unique donné comme clip de départ d'un acteur démarre « il y a un million de
  secondes » : le coup de tampon (S04) et le temps suspendu (S02) étaient déjà finis à la première image. Ils sont posés par clé.
- **Mon modèle du rig était faux sur un point** : une jambe étirée pousse les pieds vers le bas (le bassin ne bouge pas) ; je croyais
  l'inverse. La chute « les jambes partent, la tête reste » est réécrite sur cette base.
- **Les couches automatiques contrariaient les chutes chorégraphiées** (étirement à la vitesse, écrasement à la décélération : la tête
  montait de plus d'un mètre puis retombait). Les clés `toon` acceptent maintenant `auto: 0..1`.
- **Une erreur de ma main pendant la passe** : un commentaire inséré au milieu d'une ligne de `toon.js` neutralisait le placement des
  globes oculaires au bout des tiges. Vue sur une image agrandie avant le rendu final, corrigée ; d'où la règle ajoutée au skill :
  pour un doute, rendre les images une à une et en grand avant de conclure.

Moteur (ajouts, anciennes histoires inchangées : 0,00 % de pixels modifiés sur « La file d'attente », 0,50 % au plus sur les trois
autres, sous le bruit de mesure de 0,54 %) :

- clé de clip `blend` (fondu propre à la clé : `blend=0.02` = impact dur, sans anticipation), `thenBlend` ; pivot aux hanches conservé
  pendant un fondu (acteurs cartoon) ; `cadence` sur un déplacement (petits pas rapides) ;
- clés `toon` : `auto` (dose les couches automatiques) ;
- accessoires : après `detach`, des clés `to` déplacent l'objet depuis l'endroit où il a été lâché (`None` garde une coordonnée),
  `worldRot` le tourne vers la caméra, `wobble` le fait osciller ; tiges des yeux épaisses quand elles sont longues ;
- 9 clips : `fallDrag`, `splat`, `royalWave`, `stampDesk`, `hangPhone`, `reachHigh`, `headStuck`, `meltDown`, `hoseNeck` ;
  options `hit` (accordéon : impact dur, trois rebonds de soufflet), `spin` / `pop` (moulinets) ; accessoire `fedoraHat`.

Plans repris (tous, sauf S06 et S11) :

| Plan | Avant | Après |
| --- | --- | --- |
| S01-S02 | 1,27 s d'approche, 4 images au-dessus du vide ; S02 ouvrait bras écartés | deux pas sur le trottoir, quatre petits pas sur le vide (0,7 s) ; plan serré : les yeux, la tête, regard caméra tenu 12 images ; les jambes partent, la tête reste 3 images sur le cou ; le téléphone attend seul 6 images au-dessus du trou, puis tombe |
| S03 | crêpe vue par la tranche, dans la bande des sous-titres | caméra en plongée (30°) : aplati comme un tapis d'un mur à l'autre, étoiles, deux clignements ; le téléphone rebondit sur le crâne et il le rattrape à l'oreille |
| S04 | le tampon ne bougeait pas | élan bras étiré au-dessus de la tête (5 images), descente en 2 images, tasses qui sautent, la feuille bondit face caméra, INEXISTANT entier |
| S07 | take bras en l'air (comme S05), tête hors cadre | de profil : la tête bascule, les yeux descendent au bout de leurs tiges jusqu'au trou, remontent ; regard caméra ; chute ; képi et bloc-notes restent en l'air |
| S08-S09 | un tour de moulinet, visage neutre ; atterrissage en une image | deux tours et demi, yeux sortis ; chute bras en rubans, impact dur, trois rebonds de soufflet |
| S10 | bras levé tendu (lisible comme un salut sur image arrêtée) | salut du poignet, coude plié ; la main reste seule 9 images au-dessus du bord, un coup de poignet, aspirée |
| S12-S13 | lettre attrapée en 4 images juste au-dessus des têtes | la lettre s'arrête en haut du puits, le bras monte jusqu'à elle (×3,7) et y reste 6 images, le recul fait tanguer la rangée ; S13 commence 8 images plus tôt |
| S15-S16 | plongeons en 4 à 6 images qui se chevauchent ; arrivées en T | un plongeur à la fois, suspendu 2 images, la file avance ; chacun arrive dans sa pose, le plongeur reste planté tête en bas, trois étages, ceux du dessous de plus en plus plats |
| S17-S18 | fonte en 6 images, cou en poteau devant le maire | fonte en 13 images, le chapeau reste 3 images puis tombe sur la flaque ; cou en tuyau qui se balance, à côté du panneau ; toute la pile regarde la flaque, puis nous |

Skill : catalogue de gags refait pour la version livrée (19 lignes), 13 entrées ajoutées aux « Erreurs à éviter », section « Keys added
for staging » et clips de la seconde passe dans `references/cartoon-rig.md`.

### 5 ter. Seconde revue (7,8 et 7,7), troisième passe avant l'envoi

Les deux critiques ont revu le film fini (1080 px) : direction artistique **7,8/10** (7,2 au premier tour), direction d'animation **7,7/10**
(6,8). Verdict de l'animation : « treize des seize gags se lisent à la taille d'un téléphone, avec de vraies anticipations ; trois gags nommés
(les yeux sur tiges de S07, la dernière main du maire en S10, la fonte et le cou de S18) sont trop brefs, trop petits ou trop près du bord ».
Décision (sans poser de question) : troisième passe sur ces trois plans et sur les entrées trop longues, puis un seul rendu.

Deux points que les critiques renvoyaient vers l'utilisateur, tranchés ici :

- **Le carton « AUJOURD'HUI » reste sur S17** (c'est le mot de ce plan et le saut dans le temps) ; c'est le panneau qui s'écarte : le plan est
  refait dans l'axe du trottoir, panneau à 27-35 % de la hauteur, carton à 7-18 %.
- **Le pompier était lu comme un ouvrier** : casque à cimier et écusson dorés, nuquière longue (chapeau `firecrest`, au choix : le casque
  d'origine des anciennes histoires ne change pas). La veste sable est gardée (c'est elle qui fait la palette de la rangée).
- **Fin allongée de 0,4 s** (24,07 s) : le dernier regard caméra tient 17 images avec un clignement lent. La narration ne bouge pas.

Plans repris :

| Plan | Deuxième passe | Troisième passe |
| --- | --- | --- |
| S01-S02 | 0,8 s sur le trottoir, regard caméra 9 images | il part à deux pas du bord (0,2 s de trottoir, 0,55 s sur le vide) ; coupe 0,25 s plus tôt : regard caméra tenu 17 images, un clignement, puis la chute au même mot (« travail ») |
| S06-S07 | cinq idées en 1,17 s ; caméra à hauteur d'homme : le trou est un trait, les globes sans pupille sur le trottoir clair, tiges couleur peau, képi sous la barre du haut | coupe 0,25 s plus tôt ; caméra à 2,3 m, 17° en plongée : le trou est un disque sombre ; tiges roses, globes qui plongent DANS le trou, pupilles tournées vers nous, regard à gauche, à droite, un clignement (16 images) ; les yeux reviennent et redressent la tête ; il disparaît en 2 images, raide ; un seul objet reste (le képi, sur le mur clair) |
| S10 | la main restait 6 images au ras du bord, 7 % du cadre, sur des gravats de même valeur | marche raccourcie de deux enjambées ; l'avant-bras s'allonge à la verticale aussi vite que le maire descend : la main reste où elle saluait, grossit, seule 13 images devant la vitrine bleue, un coup de poignet, aspirée ; la caméra se resserre sur elle |
| S13 | personne ne regardait la lettre ; bras de 17 px | trois cous qui se tendent vers la lettre, à 2 images d'écart, et redescendent avec elle ; bras deux fois plus épais |
| S14 | dix images figées avant les yeux en euros | ils lisent l'avis : deux lignes, de gauche à droite, l'un après l'autre (le regard entraîne un clignement) |
| S16 | pile finie 5 images, sous-titre sur les torses | atterrissages resserrés, pile finie 8 images, caméra abaissée : le sous-titre passe sur les jambes |
| S17-S18 | retardataire coupé par le bord droit, flaque en rectangles sur un visage, cou en bâton de dos | dans l'axe du trottoir : il court vers nous ; **double regard** : LIBRE (ravi), il se tourne vers le trou et prend son élan, COMPLET, la tête revient au panneau (chapeau en l'air, yeux sortis, mâchoire) ; 4 images après le dernier clignotement il fond en 15 images en une **flaque ronde aux couleurs de sa chemise, qui garde ses yeux et sa moustache** ; le chapeau attend, puis se pose dessus ; un cou de cygne sort de la pile (visage de trois quarts), regard en coin vers la flaque, puis vers nous ; tout le monde aussi, la flaque comprise |

Moteur et accessoires (anciennes histoires inchangées : 0,00 % sur « La file d'attente », 0,52 % au plus ailleurs, bruit de mesure 0,54 %) :

- visage : `eyeYaw` / `eyeRoll` (les globes tournent au bout de leurs tiges : pupilles vers une caméra de profil, regard circulaire),
  `popBlink` (paupières sur les yeux sortis), `stalkRed`, `stalkBow`, `lid` (clignement posé par clé : le clignement lent de la fin) ;
- `scl.handL` / `handR` (une main qui grossit) ; `royalWave` : `fore` (avant-bras vertical) et `foreAmp` ; `meltDown` : `flat` ;
  `hoseNeck` : `curve` et `lean` (un arc permanent : un cou de cygne, plus un bâton) ;
- accessoire `meltPuddle` (flaque qui s'étale, tremble quand le chapeau s'y pose, yeux qui suivent une liste de regards et clignent) ;
- décor de la coupe du trou : cailloux assombris, sans contour (ils étaient les formes les plus claires du plan, sur la ligne du sous-titre) ;
- sous-titres : l'espace française avant les deux-points (« répondu : ») est acceptée par le constructeur de sous-titres.

Erreurs trouvées pendant la passe (consignées dans le skill) :

- **Encore un commentaire inséré au milieu d'une ligne** (clip `sneezeUp` : la tête, le torse et le cou n'étaient plus animés). Deuxième
  fois : la règle devient un contrôle (chercher `//` suivi de code dans le diff avant chaque commit).
- **Une clé dont l'instant devient négatif ne joue pas** : en avançant les atterrissages de S16, la première tombée commençait à −0,04 s ;
  la mamie n'apparaissait plus. Vu sur la bande, corrigé.
- **Un avant-bras étiré de 3,5 m balaie un mètre** pour un balancement de 0,1 radian : la main sortait du cadre. Le balancement se dose
  (`foreAmp`), et le membre est mis à la verticale avant d'être étiré.

### 5 quater. Troisième revue (7,5 et 7,5) sur le brouillon, quatrième passe, puis envoi

Troisième et dernière revue, cette fois **sur le brouillon complet à 360 px** et sur seize images en grand, pendant que le rendu final
tournait (c'est la leçon du tour précédent ; elle a servi : le rendu en cours a été jeté sans regret). Direction artistique **7,5/10**,
direction d'animation **7,5/10** : plus bas qu'au deuxième tour (7,8 et 7,7), parce que la troisième passe avait introduit ou révélé deux
défauts de finition que les deux critiques ont relevés indépendamment, chiffres à l'appui.

- **La chaussée clignotait** : sur 15 des 99 images échantillonnées des plans S01, S02, S17 et S18, l'asphalte passait au beige pâle. La
  route était posée 4 mm au-dessus du sol général du décor : en vue longue dans l'axe de la rue, les deux surfaces se disputent la
  profondeur. Le sol général de la rue de Paris est maintenant 12 cm plus bas.
- **Le cou de cygne traversait la tête** : la partie du cou logée dans la tête (2,4 cm) était étirée huit fois, comme le reste, et
  ressortait par le visage dès que le cou était courbé. La partie d'un membre qui dépasse l'articulation suivante reste désormais rigide.
- La fonte se lisait comme un homme qui se plie en deux ; le visage souriant du maire traversait la bande des sous-titres ; le képi sortait
  du cadre par le haut ; AUCUN TROU débordait de son cadre (« AUCUN TROL ») ; COMPLET, dernier mot du film, était plus petit que LIBRE ;
  la pile changeait de pose à la coupe S17/S18 ; le regard final du groupe ne tenait que 6 images et finissait en plein clignement ; le
  bras de S13 (2,3 % de la largeur) et le freinage de S08 restaient en dessous du reste.

Décisions (sans poser de question) :

- **Pas de quatrième revue** : le protocole en prévoit trois au plus. Les corrections sont vérifiées par mes soins sur bandes et sur images
  en grand ; les notes annoncées à l'envoi sont celles du troisième tour (7,5 et 7,5), pas une estimation de ce qu'elles seraient après.
- **Durée conservée** (24,07 s) : le regard final est payé à l'intérieur du plan (le chapeau ne reste plus en l'air après la fonte, le cou
  monte pendant qu'il se pose).
- **Visage du figurant à peau foncée** (S16) : les traits noirs se perdent sur ce ton à petite taille. Je ne l'éclaircis pas pour
  contourner le problème ; c'est le rig du visage qui doit donner un liseré clair aux traits ou des blancs d'yeux plus grands (piste du
  cycle suivant, notée ci-dessous).

Quatrième passe :

| Plan | Troisième passe | Quatrième passe |
| --- | --- | --- |
| S03 | à plat 8 images, étoiles de 3 px | à plat 10 images, étoiles presque deux fois plus grandes |
| S04 | feuille à 98 % de la largeur, tampon vert qui déborde | feuille plus petite et recentrée, texte du tampon ajusté à son cadre |
| S07 | le képi sort par le haut, puis pend comme une plaque noire | saut du képi réduit, cadre abaissé ; le képi pend incliné vers nous (dessus bleu éclairé), sans tourner |
| S08 | arrêt sans inversion, moulinets qui « clignotent » (140° par vignette) | sprint plus court, coupe franche vers le dérapage (`thenBlend=0.03`) : il glisse encore, penché en arrière, s'écrase, bascule sur la pointe des pieds ; moulinets plus lents (ils tournent), inclinaison qui grandit, bras allongés |
| S10 | le visage du maire traverse la bande des sous-titres | le bord du trou reste à 70-76 % : son sourire disparaît derrière le bord proche, juste au-dessus du sous-titre ; la caméra se resserre moins |
| S12-S13 | bras tendu 6 images, 13 px de large ; têtes qui tressautent | S13 prend 0,2 s à S12 ; creux de 3 images, bras tenu 9 images, deux fois plus épais ; les trois cous restent tendus (ils visent un point fixe, plus la lettre attachée à la main : sa position sautait une image) ; la lettre à l'endroit |
| S17-S18 | changement de pose à la coupe ; seuls la tête et le chapeau réagissent ; fonte pliée ; cou qui dépasse ; regard final 6 images | les têtes sont déjà tournées (clés avant 0), il finit son dérapage de S17 ; tout le corps saute au take ; fonte droite comme une bougie (la tête rentre dans les épaules, le tronc raccourcit et s'élargit, il descend dans ses chaussures) ; flaque dégagée des gravats ; panneau plus large (les deux mots à la même hauteur), à 5 % du bord ; regard caméra du groupe tenu 17 images, clignement fini 6 images avant la fin |

**Livraison** : `hyperframes/37-trou/renders/trou.mp4`, 1080×1920, 24,07 s, −16,0 LUFS, 0 erreur aux contrôles HyperFrames, aucun éclair de
chaussée détecté sur les plans à caméra fixe (`tools/flash_check.py` ; les images de S02 qu'il signale correspondent au recul de la
caméra, vérifiées à l'œil). Rendu 3D : 44 minutes. Film envoyé avec les notes du troisième tour, sans prétendre à mieux.

Erreurs trouvées (consignées dans le skill) : deux surfaces à 4 mm l'une de l'autre ; la partie d'un membre au-delà de l'articulation ;
un regard vers un accessoire qu'on attache en cours de plan ; une coupe sans changement de cadre exige la continuité des poses ; un
moulinet à plus de 60° par image ne tourne pas, il clignote.

### 6. Pistes pour le cycle 2

- Cravate, pans de veste et cheveux en mouvement secondaire (la cravate est peinte : il faut une cravate en volume).
- Poses clés dessinées pour les mains (doigts : pointer, pouce levé) ; aujourd'hui des moufles.
- Arcs : faire passer les mains par des trajectoires courbes entre deux poses (aujourd'hui interpolation d'angles).
- Rig des créatures (chaussettes, animaux) : même écrasement/étirement.
- Visage : phonèmes pour les répliques citées, joues qui suivent la mâchoire, sourcils qui se courbent (aujourd'hui trois formes).
- Re-rendre « La canicule » sans la double chute du plan S10 (version 2, sans retirer la version livrée).
- (après la seconde passe) Mains : toujours des moufles ; le tâtonnement de S13 et le salut de S10 gagneraient des doigts.
- (après la seconde passe) Tiges des yeux droites : une tige en deux segments permettrait de regarder vers le bas sans basculer la tête.
- (après la seconde passe) Un acteur dont le clip de départ est à déroulement unique devrait être signalé par le moteur (avertissement), comme
  les démarches sans déplacement.
- (après la seconde passe) Faire la revue des critiques sur un brouillon complet AVANT de lancer un rendu d'une heure : c'est le brouillon à
  360 px (5 minutes) qui doit passer la revue, pas le film fini.
- (après la quatrième passe) Visages à peau foncée : les traits noirs se perdent à petite taille. Donner au rig du visage un liseré clair
  ou des blancs d'yeux plus marqués selon la luminance de la peau, et le vérifier à la taille d'un téléphone.
- (après la quatrième passe) Un contrôle automatique des « éclairs » (une surface qui change de couleur une image sur N) sur le brouillon :
  `scratchpad/tools/roadflick.py` est un début ; à intégrer aux outils du dépôt.
- (après la quatrième passe) Traînées multiples pour les membres qui tournent vite (moulinets) : aujourd'hui seulement l'allongement.

---

## Cycle 2 — « L'éternuement » (histoire 38)

### 1. Analyse (dernière histoire : « Le trou », seconde passe ; rigs et clips du cycle 1)

Faiblesses relevées (sur les images finales de « Le trou » et sur le retour des deux critiques) :

1. **Des moufles** : aucune pose de doigts. Le salut du maire, la main qui tâtonne en haut du puits, le nez pincé : la même palette plate.
   → corrigé ce cycle (mains à doigts : pointer, poing, pincer, pouce levé, éventail).
2. **Rien ne traîne sur le personnage lui-même** : la cravate est peinte, les cheveux sont un bloc. Dans une chute ou un sprint, seuls les bras
   bougent. → corrigé ce cycle (cravate en trois segments, mèche sur le crâne, pilotées par le vent apparent).
3. **Les groupes au repos sont des piquets** (« aucun transfert de poids visible dans les alignements »). → corrigé ce cycle (changement
   d'appui par à-coups, à des instants différents pour chacun).
4. **Les yeux sortis ne regardent rien** : la pupille reste au centre du globe. → corrigé ce cycle (pupilles qui visent, yeux qui louchent).
5. **Le moteur laisse passer en silence un clip à déroulement unique donné comme clip de départ** (deux gags perdus au cycle 1).
   → corrigé ce cycle (avertissement).

Reporté : phonèmes pour les répliques citées, sourcils courbes, rig des créatures, tiges des yeux en deux segments.

Leçon de méthode appliquée dès ce cycle : la revue des critiques se fait sur le brouillon complet (360 px, 5 minutes), avant le rendu d'une heure.

### 2. Rigs (tout est au choix : `fingers`, `cloth`, `idleShift` ; sans ces options un personnage est exactement celui du cycle 1)

- **Mains à doigts** (`engine/fingers.js`) : paume, quatre doigts à deux phalanges, pouce à deux phalanges, à la place de la moufle. Canal `hands`
  (une pose par main, par nom ou en six nombres) ; dix poses : repos, ouverte, éventail, poing, index pointé, deux doigts, pince, pouce levé,
  prise, griffe. Les clips du cycle 1 qui en profitent le plus : le salut, la main qui tâtonne, le doigt sous le nez.
- **Ce qui traîne** (`engine/cloth.js`) : une cravate en trois segments (la cravate peinte est retirée de la veste du héros : texture sans
  cravate) et une mèche sur le crâne, toutes deux pilotées par le vent apparent (vent de la scène moins la vitesse du personnage), calculé sans
  état, dans le repère du torse et de la tête. La cravate pend, part en avant à l'arrêt, monte dans une chute, ne passe par-dessus l'épaule que
  par vent de face fort ; la mèche se dresse et penche. Canal `hairUp` pour laisser quelqu'un décoiffé.
- **Vent de scène** (`fx` de type `wind`) et **changement d'appui au repos** (`idleShift`) : chacun à son moment, par à-coups.
- **Visage** : yeux qui louchent (`cross`), paupière posée par clé (`lid`), globes orientables au bout des tiges (`eyeYaw`, `eyeRoll`), paupières
  sur les yeux sortis (`popBlink`). **Corps** : une main qui grossit (`scl.handL / handR`).
- **Visages à peau foncée** (piste ouverte par la troisième revue de « Le trou ») : option `faceRim` par personnage : un contour clair net autour
  des sourcils, des yeux et de la bouche. Un premier essai en halo flou était invisible à petite taille ; le contour net se lit à un cinquième
  de la taille. L'ingénieur de l'histoire 38 l'utilise.
- **Garde-fous** : le moteur avertit quand un clip à déroulement unique est donné comme clip de départ ; la partie d'un membre qui dépasse
  l'articulation suivante ne s'étire plus.
- Anciennes animations : 0,00 % de pixels modifiés sur « La file d'attente », 0,52 % au plus sur les trois autres histoires de contrôle
  (bruit de mesure 0,54 %), après chaque lot de modifications.

### 3. Animations (clips écrits pour l'histoire 38, réutilisables)

`sneezeUp` (trois inspirations de plus en plus grandes : le torse gonfle, la tête part en arrière, il monte sur la pointe des pieds puis
décolle, l'index vient sous le nez), `sneeze` (deux images pour partir, tenu plié et tremblant), `sniff`, `poster` (plaqué contre un mur comme
une affiche, puis il se décolle par le haut et glisse), `spinTop` (toupie), `headHammer` (la tête rentre dans les épaules, tenue 4 images,
ressort trop loin et oscille, les yeux louchent), `blownBack`, `leanAway` (le corps en C pour s'écarter de quelqu'un), `stampDown` (grand
tampon abattu à hauteur de tête, avec élan sur la pointe des pieds et reprise), `shakeHands` (une poignée de main trop franche : la secousse
remonte le bras de l'autre comme une vague, jusqu'à la tête), `meltDown` en mode `sink`.

Principes appliqués : anticipation avant chaque geste fort (les trois inspirations, l'élan du tampon, le creux avant le bras élastique),
impact en deux images sans fondu, tenue de la pose forte 8 à 16 images, retombée avec dépassement, actions décalées de 2 images dans les
groupes, regard qui précède la tête.

### 4 (commencé en avance, pendant le rendu final de « Le trou »). Histoire : texte et voix

Type du skill : histoire nouvelle dans le style. Structure respectée : accroche (le mec + l'événement absurde), institution au pied de la
lettre (la météo : au-dessus de cent kilomètres-heure c'est une tempête, une tempête porte un prénom, le suivant sur la liste est Josiane),
escalade (vigilance rouge, évacuation, catastrophe naturelle), retournement (les éoliennes l'embauchent), aparté sec (le pollen, le printemps).

Texte (12 lignes, 26,7 s de voix) : Ce mec a éternué et il a décoiffé toute la ville. / La météo a mesuré : / « Deux cents
kilomètres-heure. » / Au-dessus de cent, c'est une tempête. / Et une tempête, ça porte un prénom. / Le suivant sur la liste, c'était
Josiane. / Depuis, Josiane est en vigilance rouge. / Quand Josiane renifle, on évacue sa rue. / Son assurance l'a classé catastrophe
naturelle. / Puis les éoliennes l'ont embauché. / Aujourd'hui, Josiane éclaire trois villes. / Il est allergique au pollen. Le printemps
arrive.

Décisions : « la météo » plutôt qu'un nom d'organisme réel ; « parc éolien » était entendu « parquet au lien » à la vérification de la
voix, remplacé par « les éoliennes » ; « officiellement » retiré de la ligne 4 pour tenir le rythme.

### 4 bis. Histoire : mise en scène de « L'éternuement » (19 plans, 28,2 s)

Gags visuels (chacun s'appuie sur le rig ; aucun n'est repris tel quel de « Le trou ») :

| Plan | Gag | Ce que le rig apporte |
| --- | --- | --- |
| S01 | Trois inspirations, chacune plus grande : il gonfle, décolle, un doigt sous le nez | torse qui s'épaissit (colonne `fat`), index pointé (mains à doigts), cravate et mèche qui suivent |
| S02-S03 | Le souffle plaque trois passants sur l'affiche d'un coiffeur ; ils y restent comme des affiches, décoiffés, puis se décollent | `blownBack`, `poster` (plat comme du papier), `hairUp`, vent de scène |
| S04 | La présentatrice lève son anémomètre : c'est elle qui tourne, comme une toupie | `spinTop` (colonne et jambe vrillées derrière la rotation) |
| S06-S08 | Le curseur de l'échelle monte en deux fois sous le doigt du chef ; il réfléchit, trouve, tire la liste des prénoms ; le doigt descend les prénoms barrés | index pointé, bras étiré, accessoires qui répondent au geste |
| S09 | Le badge TEMPÊTE JOSIANE claqué sur la poitrine : tout le corps tremble | `jelly`, regard vers le badge puis vers nous |
| S10 | Le bras de la présentatrice part comme une baguette télescopique jusqu'à la carte | bras et avant-bras ×1,5 et ×2 |
| S11 | Gyrophare sur la tête : les passants s'écartent l'un après l'autre, courbés en C | `leanAway`, décalés selon sa marche |
| S12-S13 | Il renifle : trois paires d'yeux sortent ; les jambes moulinent sur place, ils disparaissent un à un, une perruque reste en l'air ; des sacs de sable surgissent autour de lui | `sniff`, yeux sortis, `scramble`, `dashOff`, accessoire laissé en l'air |
| S14 | Le très gros tampon de l'assureur, levé lentement sur la pointe des pieds : la tête rentre dans les épaules, ressort marquée CAT. NAT., étoiles ; il bascule en arrière, raide | `stampDown`, bras étiré à l'impact, `headHammer`, yeux qui louchent, `plankFall` |
| S15 | Une poignée de main trop franche : la secousse remonte son bras et le traverse comme une vague ; pouce levé | `shakeHands` (onde bras, colonne, cou), pose de main `thumbUp` |
| S16-S17 | Au crépuscule, une poivrière au bout d'une canne à pêche ; l'éternuement lance les éoliennes l'une après l'autre et allume trois villes | les trois inspirations en rappel, souffle, éoliennes à vitesse variable, fenêtres qui s'allument ville par ville |
| S18 | Un grain de pollen descend jusqu'au bout de son nez : ses yeux le suivent jusqu'à loucher | regard qui suit un accessoire, `cross`, paupière posée |
| S19 | Le printemps : il gonfle d'un cran à chaque inspiration jusqu'à deux fois sa taille et s'élève ; on coupe avant l'éternuement | écrasement-étirement par paliers, tout ce qui traîne vole vers lui |

Décisions de mise en scène : la fin ne montre pas l'éternuement (temps suspendu, coupe au sommet) ; les passants gardent les cheveux dressés
jusqu'au bout (gag à répétition : la ville reste décoiffée) ; le héros tourné en diagonale vers le fond pour le plan des éoliennes (lui en
bas à gauche, éoliennes et villes dans la hauteur du cadre) ; carton « JOSIANE » sur le plan du badge.

### 4 ter. Première revue par les deux critiques (6,8 et 6,8 sur le brouillon), puis passe de mise en scène

Les deux lecteurs (direction artistique, animation) ont noté le même brouillon 6,8. Leurs reproches se recoupent : **le visage, surface de jeu
principale du rig, était caché ou de profil dans 9 plans sur 19** ; le gag du tampon perdait sa chute ; la poignée de main ne se serrait pas ;
plusieurs tenues étaient des images arrêtées ; des textes d'accessoires étaient couverts ou coupés. Tout a été repris avant un second brouillon.

| Reproche | Ce qui a été fait |
| --- | --- |
| Le gyrophare posé sur le front cache les yeux pendant trois plans (S11 à S13) | Le décalage d'un accessoire attaché se compte dans le repère de la tête (0,5 de haut) : `offset [0, 0.565, 0]`, au-dessus des cheveux ; plus gros, deux faisceaux qui tournent, relevés (`beamTilt`) pour passer au-dessus des visages |
| S12 : deux visages sur trois, coupés par les bords ; sa main cache un œil | Caméra de trois quarts, trois têtes en rang derrière son épaule gauche (positions calculées avec `proj.py`), vrai double regard (coup d'œil, ailleurs, retour brusque les yeux sortis) |
| S13 : quatre idées en 1,17 s, sacs de sable sous les sous-titres, fin figée | Les jambes moulinent dès la fin de S12 ; sacs en U derrière lui (entre 53 et 74 % de la hauteur) ; ses yeux suivent chaque départ, clignement, dernier reniflement ; la perruque reste, au centre, à la place de la tête |
| S11 : visage trop petit, passants de dos | Travelling arrière partiel (visage de 12 à 17 % de la largeur) ; les passants font face à la caméra et se plient vers l'extérieur sans le regarder |
| S14 : le tampon redescend devant le visage quand la tête ressort ; chute de 0,2 s qui s'éloigne ; assureur de profil et immobile ; diplôme à moitié visible dès le début ; même bureau que la météo | Le tampon suit sa propre trajectoire et la main est guidée sur son pommeau : frappe exacte, rebond vers l'assureur, tête qui ressort dans le vide avec la marque pendant que la caméra s'approche ; diplôme hors champ puis sur le mur libre ; assureur derrière l'épaule du héros, de trois quarts, qui continue à lever le tampon en tremblant, lit sa marque, hoche la tête deux fois, sort ; chute dans un plan à part, de trois quarts : 5 images penché, 8 pour tomber, rebond, jambes en l'air 10 images ; bureau vert-gris avec son enseigne ASSURANCES ; tampon ×1,6 |
| S15 : les mains ne se serrent pas, deux profils, pas de retard d'une articulation à l'autre | `shakeHands2` : un seul point tenu, amplitude croissante, 2 images de retard par articulation, il décolle sur les derniers coups, trois oscillations après le lâcher ; les deux hommes à 55° de l'axe ; gros pouce pompé deux fois ; l'éolienne entre eux, plus derrière son dos |
| S16, S19 : tête renversée vue de côté et d'en bas : pas de visage ; poivrière illisible devant un nuage | Caméra de face, un peu haute ; `back: 0.6` ; l'ingénieur tient la canne par-dessus l'épaule du héros (derrière le canon), la poivrière étiquetée POIVRE pend au-dessus du nez, contre le ciel, le poivre tombe ; il se baisse à la troisième inspiration ; une éolienne dans le fond ; S19 de face (ry 25), panneau coupé retiré, éoliennes écartées de sa tête |
| S17 : le recul est caché, le matelas est une caisse crème, les trois villes font une seule ligne | Deux temps : de trois quarts de côté, il part assis le premier dans un matelas rayé à boutons qui se creuse et le renvoie (l'ingénieur à l'abri derrière : son casque saute) ; puis l'autre bout du champ : trois éoliennes, une ville avec son clocher derrière chacune, qui s'allume quand elle tourne |
| S18 : le grain se pose sur un œil | Position mesurée sur une image : 0,13 m plus bas, sur les narines ; grain d'un tiers plus petit |
| La détente n'est jamais payée sur le personnage (deux éternuements vus de dos en moins de 0,15 s) | Les 3 dernières images de S01 et de S16 sont la détente, face à nous (`sneeze` avec `fold` et `chin`) ; le plan suivant continue le clip |
| Textes : aiguille sur le « 200 », bandeau MÉTÉO sous le carton, VIGILANCE cachée par la manche, slogan couvert | Chiffres hors de la course de l'aiguille, « 200 » en marine et plus gros ; pas de bandeau derrière le carton de S09 ; bandeau rouge en haut de la carte ; tout le texte du panneau dans une bande au-dessus des têtes |
| Mur de la météo de la teinte des peaux ; cheveux dressés = un fez ; cravate et cheveux inertes à l'inspiration ; tenues mortes | Mur refroidi (34°, 23 % de saturation mesurés, contre 31°, 42 %) ; cinq mèches ; canal `wind` du clip ; une action par tenue (tapes du doigt, « attendez », hochement, pouce) |

Décisions prises sans demander (consignées ici) : le visage reste peint sur la face avant seulement (modèle de la série) : on règle par la mise en
scène ; la saturation du rendu « naturel » reste celle des histoires 34 à 37 ; la narration enregistrée ne bouge pas (aucune pause ajoutée) ; la
trace hachurée dans le ciel de la rue était un bord de la tour dans la brume : tour retirée pour les plans S11 à S13.

Outils du moteur ajoutés pour cette passe : canaux `reach` / `touch` (main guidée, voir cycle 3), `wind` ; option `rotOrder` des accessoires ;
`mairie` avec couleurs et sans bandeau ; accessoires : `nameList unroll` (store à corde), `windScale side`, `adPanel textH`, `stormMap bandTop / tapAt`,
`beacon beams / beamTilt`, `pepperRod` étiqueté, `mattressWall` en tranches, `townLights sites`, perruque redessinée ; clips : `shakeHands2`,
`plankFall hang / feet`, `sneeze fold / chin`, `sneezeUp ik / back`, `sniff ik`.

### 4 quater. Deuxième revue (animation 7,6 ; direction artistique 8,0), puis troisième passe

Les deux relectures indépendantes du second brouillon ont donné 7,6 (animation) et 8,0 (direction artistique), contre 6,8 et 6,8 au premier
tour. Leurs comptes rendus sont dans le dossier de travail de la revue (non versionné). Troisième passe, reproche par reproche :

| Reproche (relecteur) | Correction |
| --- | --- |
| L'inspiration, qui ouvre, revient et ferme le film, « pulse » au lieu de monter ; le film finit une demi-seconde après son image la plus forte (anim) | `sneezeUp` devient un cliquet (`times`, `last`, `tremble`) : chaque inspiration garde ce qu'elle a gagné. Trois rythmes : S01 trois qui se resserrent, S16 une longue puis une courte, S19 cinq qui se resserrent ; le film finit sur le sommet tenu 6 images, en tremblant. Toute la prairie se penche vers lui (`flowerMeadow`) |
| Le matelas : six images, ni entrée ni sortie lisibles ; la troisième ville s'allume à la coupe (anim) | S17 passe à 1,63 s (S16 raccourci à deux inspirations) : entrée assis, matelas tenu creusé 4 images, recraché en boule sur une cloche, atterrissage écrasé ; villes allumées d'un coup, une par éolienne, à côté des mâts, plus grandes, sous un halo, la dernière 13 images avant la coupe |
| Le bras télescopique se lit comme un bras ordinaire, puis le plan se fige (anim) | la carte en haut du mur, la présentatrice au coin opposé : le bras monte la diagonale, dépasse, la carte bascule à chaque tape, une ondulation redescend le bras |
| Le double regard se lit comme un seul (anim) | premier reniflement à la 2e image ; premier regard des trois ensemble, cou tendu, tenu 6 images ; retour ; second reniflement ; yeux sortis décalés |
| Après la poignée de main il est au repos en deux images ; le pouce ne se lit pas ; les tenues sont sans vie (anim, DA) | il sonne 12 images après le lâcher (pieds plantés, tête en dernier, étoiles dès le lâcher) ; pouce guidé dans le ciel libre entre les têtes, droit, pompé deux fois ; l'ingénieur sourit à la caméra comme pour une photo |
| S06-S08 : 5 s de petits gestes sans chute (anim) ; le chef montre le côté sans visage de sa tête (DA) | le tableau passe à droite du bureau et plus haut : S06 en plan moyen de trois quarts, le chef présente à la caméra ; S07 plus large : la boule est hors de portée, il saute, redescend avec la liste, qui remonte comme un store et l'emporte : il pend, pieds décollés, jambes qui balancent |
| La chute se joue petite et la tête disparaît contre le bureau (DA) | caméra basse et proche, de trois quarts : il tient la hauteur du cadre, la caméra descend avec lui, jambes en V sur 39 % de la hauteur ; bureau déplacé et repeint en gris-vert ; à la fin il relève la tête : le visage tamponné revient vers nous sous le certificat |
| Le héros tourne la tête sur son côté sans visage pendant que le tampon monte (DA) | nouveau canal du visage `face.gx / gy` : la tête reste vers nous, seules les pupilles suivent le tampon ; il déglutit et se tasse |
| La prairie de printemps n'a pas d'identité ; la perruque se lit comme une boîte sur le mât (DA) | prairie fleurie (560 fleurs, touffes), deux arbres en fleurs, éoliennes repoussées aux bords ; perruque et journal arrivent lentement avec le vent, dans le ciel libre |
| Finitions (DA) | fin du fouetté de S16 au-dessus des sous-titres ; une seule étiquette sur la poivrière ; bandeau MÉTÉO remonté ; flou de rotor en trois fantômes ; S01 décollé du sol plus tôt ; mur de la météo gris-bleu (mesuré : 215°, 10 %) ; costume gris et cravate verte pour le chef |

Décisions prises sans question (règle du mode autonome) :
- **Costume du chef** : le relecteur signalait un quasi-double du héros et renvoyait la décision à l'utilisateur si les costumes secondaires
  étaient des modèles fixes. Ils ne le sont pas (chaque histoire règle ses seconds rôles) : gris et cravate verte.
- **Désaccord entre relecteurs sur S15** (l'un demandait de couper la fin, l'autre un pouce lisible) : on garde la fin, corrigée.
- **Troisième et dernier tour de relecture** lancé sur le brouillon corrigé, en parallèle du rendu final : les corrections éventuelles seront
  rendues par plages et recollées (`tools/splice_range.sh`).

Régression après les modifications du moteur : 0,5 % au pire (le bruit de fond habituel est de 0,54 %).

### 4 quinquies. Troisième et dernière revue (animation 8,2 ; direction artistique 8,4), dernière passe, rendu

Troisième tour (le dernier permis par le protocole) sur le brouillon de la troisième passe : **8,2** en animation (6,8 puis 7,6 aux tours
précédents) et **8,4** en direction artistique (6,8 puis 8,0). Aucun des deux n'atteint 8,5 ; leurs dernières remarques ont été appliquées
sans nouvelle relecture, puis le film a été rendu.

| Remarque du troisième tour | Correction |
| --- | --- |
| Le passant en costume noir est une silhouette découpée (DA) | anthracite avec revers peints ; une bande de trottoir entre lui et le héros en S11 |
| Un arbre du décor exactement derrière la poignée de main (DA, anim) | autre tirage des arbres pour ce plan |
| Les coupelles rouges de l'anémomètre disparaissent sur le rouge du bandeau (DA) | coupelles jaunes, moyeu sombre |
| Poses au bord du cadre ou dans la bande des sous-titres : index « attendez », pieds pendus, atterrissage, enseigne (DA, anim) | index près du visage sur du mur libre ; caméra de S07 visée plus bas (le vide sous ses pieds au-dessus des sous-titres) ; atterrissage remonté ; marge à droite de l'enseigne |
| Quatre accessoires qui ne se lisent pas : sacs de sable, villes, perruque, grain de pollen (DA) | sacs de jute affaissés en quinconce ; un monument par ville (beffroi, dôme, château d'eau) ; perruque avec raie et frange roulée ; grain citron pâle cerné, plus gros |
| Mèches à plat vues par la tranche : un trait noir flottant (DA) | les mèches à plat ne sont plus dessinées et ne penchent qu'une fois dressées |
| Sortie du matelas illisible (anim) | deux images de moins dans le matelas ; la boule part sur une seule cloche dans le ciel libre ; crêpe tenue six images ; plus de relevé (décision prise seul : on finit le gag sur la crêpe) |
| Le bras télescopique se lit comme un bras tendu (anim) | elle au pied du mur, bras ordinaire tenu huit images un bon mètre trop court, coup d'œil à la carte, puis le bras part en deux images, dépasse : la carte se balance comme un pendule ; chaque tape plus forte, la carte reste de travers |
| La peur « par les yeux seuls » ne se lit pas ; le visage de l'assureur est caché par son bras (anim) | yeux grands ouverts, deux paliers des pupilles et des sourcils, il s'enfonce dès 0,2 s ; l'assureur tient le tampon à deux mains, le visage entre les bras |
| Les deux « chutes » de gag ont le moins d'images (anim) | la liste descend plus tôt (sur « ça porte un ») : seize images pendu, deux balancements des jambes, un regard et un clignement vers nous ; après la poignée de main, trois balancements plus lents (22 rad/s), la cravate et les cheveux après la tête |
| Divers (anim) | la main descend la liste nom par nom ; premier regard des passants les yeux ouverts, un écrasement avant les yeux sortis ; la présentatrice se grandit avant la rafale ; la première inspiration garde son gain (cheveux et cravate suivent la racine du niveau) ; il recule devant le nuage au début du dernier plan ; gonflement final plus fort |

Régression après ces modifications du moteur : 0,52 % au pire (bruit habituel).

### 4 sexies. Rendu final et envoi de l'histoire 38

- Rendu 1080 × 1920 en 44 min (seul sur la machine : un brouillon lancé en même temps l'avait fait tomber à 0,05 image par seconde ; règle
  ajoutée au skill au cycle 3), habillage HyperFrames, mixage à −16,1 LUFS (crête −4,0 dBFS), contrôle : aucune erreur, aucune saute d'image.
- Envoyé avec les notes réelles des relecteurs sur les brouillons : 6,8 / 6,8, puis 7,6 / 8,0, puis 8,2 / 8,4 ; leurs dernières remarques ont été
  appliquées après le troisième tour, sans nouvelle relecture (trois tours au plus).

## Cycle 3 — rig : la main guidée (commencé pendant la revue de l'histoire 38)

### 1. Analyse (ce que les histoires 37 et 38 ont montré)

1. **Les contacts de mains se règlent à la main** : chaque geste qui doit toucher (doigt sous le nez, tampon sur un crâne, curseur, corde) demandait
   des angles d'épaule et de coude ajustés image par image, et cassait dès que la tête ou le torse bougeaient. Choisi pour ce cycle.
2. Les accessoires tenus n'arrivent jamais exactement où il faut (tampon à côté du crâne, redescendu devant le visage). Choisi (même solution).
3. Les membres rapides n'ont pas de traînée propre (seul le corps entier s'étire à la vitesse). À faire.
4. Les accessoires sont rigides à l'impact (seul le matelas se creuse depuis cette passe). À faire au cas par cas.
5. Les bouches ne suivent pas les sons (ouverture seule). À étudier.

### 2. Rig

- **Canal `reach`** : une main amenée à un point du monde par un calcul à deux os (épaule, coude), avec étirement automatique des deux segments quand le
  point est trop loin, une longueur de bout de doigts (`tip`), une direction de coude, un poids pour entrer et sortir du geste.
- **Canal `touch`** : la même chose vers un point de son propre corps, donné dans le repère d'une articulation ou en unités du visage
  (`['face', travers, hauteur, mètres devant]`) : le doigt reste sous le nez quand la tête part en arrière et que le torse gonfle.
- Canal `wind` : un vent propre au personnage sur la cravate et les cheveux (l'inspiration les aspire).
- Cheveux dressés en cinq mèches.
- **Traînée des membres rapides** (`limbSmear`, au choix) : au-delà de 9 rad/s environ aux articulations, la moitié éloignée du membre s'étire (bras
  jusqu'à ×1,6, jambe ×1,5) et s'affine, en plus des arcs de retard : jambes en moulinet, bras en hélice, toupie. Sans effet sur une main guidée.
- Corrections : une pièce du rig appliquée deux fois doublait la rotation des articulations filles ; l'échelle de la tête est posée avant le calcul
  des mains ; la solution à deux os est exacte (plus d'itérations).
- Vérification des anciennes histoires après chaque lot : 0,50 %, 0,50 % puis 0,55 % de pixels changés au pire (bruit habituel : 0,54 %).
- Ajouts faits pendant la troisième passe de l'histoire 38 : **regard par les pupilles seules** (`face.gx / gy` : la tête reste vers la caméra) ;
  `sneezeUp` en cliquet ; oscillation lente après un lâcher ; pouce guidé ; matelas qui garde son creux ; liste qui remonte comme un store ; carte
  qui se balance comme un pendule ; prairie dont les fleurs se penchent vers un point ; bureau déplaçable dans le décor de mairie.

### 3. Animations (cycle 3)

- Principe retenu : **l'accessoire a sa trajectoire, la main est guidée dessus** (mêmes instants, mêmes courbes). Tous les contacts de l'histoire 39
  sont faits ainsi : la main ne quitte pas la poignée, quoi que fasse le corps ; c'est le bras qui s'étire.
- Clips réutilisés avec de nouveaux paramètres plutôt que de nouveaux clips : `poster` (décollé comme du papier peint), `cannonball` (un tour sur
  le vol), `pancake`, `pressGlass` (pressé derrière une vitre), `scramble`, `doubleTakeToon`, `stiffStand` (le garde impassible).

### 4. Histoire 39 — « La porte » (type : un geste banal qu'une institution prend au pied de la lettre, escalade, retournement, aparté sec)

Texte (11 lignes, 25,4 s) : « Ce mec a tenu la porte à une dame. Il la tient encore. / Derrière elle, il y avait la ville. / La mairie a compté : /
« Quatre mille passages par jour. » / À ce niveau-là, c'est un service public. / Et un service public, ça ne ferme pas. / Son remplaçant est dans la
file. / Le soir, il rentre. Le bras reste. / La porte est classée monument historique. Le bras aussi. / Hier, un technicien est passé : elle était
automatique. / La dame n'a jamais dit merci. »

Mise en scène (17 plans), gags appuyés sur le rig :
1. la barbe qui pousse d'un cran à chaque passant, une toile d'araignée entre le bras et la porte (S02) ;
2. la file jusqu'à l'horizon, puis son visage : yeux sortis, mâchoire tombée (S03, S04) ;
3. l'agent de la mairie au compteur : la tête comme à un match de tennis, le pouce qui enfle, le compteur qui fume (S05, S06) ;
4. la plaque « SERVICE PUBLIC » vissée par-dessus l'enseigne ; la casquette qui lui tombe sur la tête : il s'enfonce, seuls ses yeux montent (S08) ;
5. **le bras corde à linge** : il s'éclipse en crabe, la main toujours sur la poignée ; au bout du bras ses pieds moulinent ; le bras le ramène, la
   porte se rabat sur lui : **pressé entre le mur et la vitre comme une fleur dans un livre** ; la porte revient, il reste collé au mur (S09) ;
6. le remplaçant, même casquette, le cou étiré au-dessus des têtes, ticket à la main (S10) ;
7. le soir il rentre : le bras se dévide derrière lui, des pigeons dessus ; dans son lit, le bras sort par la fenêtre ; quelqu'un pousse la porte :
   le bras le tire du lit et le plaque au mur ; il ne se réveille pas (S11, S12) ;
8. le touriste et son autoportrait avec le garde impassible, le doigt dans la joue ; la plaque « BRAS CLASSÉ » (S13, S14) ;
9. le technicien et le bouton AUTO ; la porte s'en va toute seule, sa main reste en l'air, double regard (S15, S16) ;
10. la dame ressort sans un regard ; il rabaisse son bras de l'autre main : il remonte tout seul (S17).

Décisions prises sans question : la boulangerie est « nationalisée » à l'image (la plaque bleue recouvre l'enseigne à partir de S08) ; une seule
carte de titre, « LE BRAS RESTE », sur le plan de la chambre ; l'enseigne réduite à la largeur de la porte (elle coupait tous les plans serrés).


## Cycle 4 — rig : un visage réglable élément par élément, des membres qui ondulent, le noir (commencé pendant le rendu final de l'histoire 38)

### 1. Analyse (troisième revue de l'histoire 38, premier brouillon de l'histoire 39, rigs des cycles 1 à 3)

Faiblesses relevées, et ce qui est corrigé dans ce cycle :

| # | Faiblesse | Où | Correction |
|---|-----------|----|------------|
| 1 | **Expressions pauvres dès que la tête fait moins de 15 % de la largeur** : le rig ne savait que tirer tout le visage vers une expression nommée ; impossible de lever un seul sourcil, de fermer un seul œil, de changer la bouche sans changer les yeux. Résultat : des visages symétriques, et un « regard d'effroi » lu comme deux fentes (38, S14). | 38 S06, S14 ; 39 S02, S05 | **Corrigé** : canaux de visage par élément et par côté (voir Rigs). |
| 2 | **Un membre étiré est une tringle** : le bras télescopique (38, S10) et le bras corde à linge (39) restent droits ; le relecteur demandait « une onde visible le long du bras ». | 38 S10 ; 39 S03 à S12 | **Corrigé** : canal `wave` (une onde le long d'un membre, d'un cou, du buste). |
| 3 | **Aucun gag possible dans le noir** : la seule nuit du moteur est un décor bleu ; pas de noir de dessin animé où il ne reste que les yeux. | — | **Corrigé** : plan `dark` (voir Rigs), pour l'histoire 40. |
| 4 | Les relances (« toppers ») ont le moins d'images ; des gags posés au bord du cadre ou trop petits. | 38 S06, S07, S15, S17 | Règle d'écriture déjà au skill (cycle 3) ; appliquée dès le découpage de l'histoire 40 (chaque gag a son plan et au moins six images de tenue). |
| 5 | Plusieurs poses debout symétriques (« twinning »). | 38 | Reporté au cycle 5 (appui sur une jambe par défaut, épaules désaxées). |

### 2. Rigs (ajouts ; rien ne change pour les histoires existantes)

- **Visage, un élément à la fois, un côté à la fois** (`engine/director3.js`, canal `face` du rig cartoon). Chaque valeur est un écart par rapport à
  l'expression en place (0 = inchangé), donc une clé déforme une expression au lieu de la remplacer : `brow`, `browL`, `browR` (1 = jusqu'aux
  cheveux, −1 = sur l'œil), `browTilt…` (degrés), `lidL`, `lidR` (un clin d'œil, un œil lourd), `low…` (paupière du bas : un plissement), `eye`,
  `eyeL`, `eyeR` (un œil plus gros que l'autre), `mouth` (une bouche par son nom : O, teeth, wavy, kiss, whistle, smirk…), `mouthW`, `mouthH`,
  `mouthTilt`, `mouthDx`, `mouthDy` (une bouche tirée d'un côté), `cheeks`, `puff`, `sweat`, `blush`, `tears`, `tear`, `vein`, `shadow`.
  Attention : L = le côté gauche **de l'image** quand il nous fait face (son œil droit, celui qui est haut).
- **Onde le long d'un membre** (`engine/toon.js`, canal `wave`) : `{armL: [amplitude (m), nombre d'ondes, phase (tours), libre, axe]}`. Les deux
  bouts restent en place (une main guidée garde son point) ; `libre: 1` laisse fouetter le bout (une tête au bout d'un cou en nouille). On fait
  voyager l'onde en animant la phase. Axe π/2 = onde verticale sur un bras tendu à l'horizontale (celle qui se lit de face).
- **Le noir** (`engine/look.js`, `engine/facerig.js`, `engine/human.js`) : `dark=[[t, k, rampe]]` sur un plan éteint ou rallume la lumière en une
  image ; l'image tombe à des silhouettes froides à peine visibles (`darkFloor`, 0 = noir complet). **Les yeux restent** : le rig de visage dessine
  les yeux seuls (et une bouche qui montre les dents) sur une seconde peau de la tête, non éclairée, tracée par-dessus l'image assombrie et cachée
  par ce qui est devant elle. Dans le noir les yeux grossissent (×1,3) et une paupière lourde se lève ; un clignement les fait disparaître ; les
  yeux dessinés (croix, spirales, arcs) passent en clair, les cœurs et les étoiles gardent leur couleur ; les yeux sortis sur tiges se voient
  aussi. Un accessoire marqué `inDark` reste visible (une flamme, une torche, une enveloppe blanche).
- Essais : trois planches d'images (visage, onde, noir) avant d'écrire l'histoire 40 ; non-régression lancée dès que le processeur est libre.

### 2 bis. Rigs : compléments ajoutés pendant la mise en scène des histoires 39 et 40

- **La cravate se tire** (`engine/toon.js`, `engine/cloth.js`, canal `tie [longueur, avant, côté]`) : le nœud reste à 1,61 m, la pointe (1,18 m au repos)
  descend, s'avance ou part de côté ; une main guidée vient la prendre. Sert à un gag à répétition de l'histoire 40 (la cravate tirée comme le cordon
  d'une lampe, trois fois, trois variations).
- **Les yeux sortis regardent quelque part** : `face.eyeYaw` (déjà là) et **`face.eyePitch`** (ajout, > 0 = vers le bas) font tourner les globes au
  bout de leurs tiges : un take peut garder la tête vers la caméra et envoyer les pupilles sur la cause.
- **Le noir sert aussi de nuit** : `dark=[[0, 0.62 à 0.72, 0.001]]`, `darkFloor=0.5`, `darkTint='#7A98F0'` donne une nuit graduée (la moitié de la
  lumière du jour, froide) ; les accessoires `inDark` (lampadaires, flaques, fenêtres) gardent leur couleur. Pour qu'ils gardent le même aspect dans un
  plan éclairé du même lieu : `dark=[[0, 0, 0.001]]`.
- Accessoires : `shopDoor` (`glass` : opacité de la vitre ; `signHide` : enseigne rangée pendant un cadre serré ; `signEdge` et enseigne sur deux
  lignes ; `inner: False` : sans barre intérieure), `streetLamp pool` (flaque de lumière au sol), `pigeon` redessiné (`flap`, `sleep`), `pillow`,
  fenêtre de la chambre de nuit (`pane`, `paneGlow`), et tout le module `props_interrupteur.js` (ville de nuit, balcon, interrupteur, compteur, pince,
  horloge, bougie, soleil à visage, télescope, torche, enveloppe, allumette, paires d'yeux, bandeau).
- **Non-régression** : anciennes histoires 0,49 % d'écart moyen (plancher de bruit 0,54 %) ; histoires 37 et 38 (rig cartoon) comparées aux films
  livrés : 0 à 0,33 % (1,15 % sur une image aux ombres de pales en mouvement). La comparaison se fait à des instants exacts d'image (f / 30) : entre
  deux images elle donnait 3 à 11 % et faisait croire à une casse.

### 3. Animations (cycle 4)

- **Le regard précède le geste**, partout où un geste porte un gag : les pupilles vont au bras deux images avant qu'il remonte (39 S17), à la boîte
  avant le bras du technicien (39 S15), au poing avant le take (39 S16), à l'interrupteur avant la main (40 S01).
- **Prise d'élan avant chaque take** : deux images tassées, paupières fermées, puis la détente avec dépassement ; le take retombe sur les premières
  images du plan suivant au lieu d'être coupé.
- **Tenues qui jouent** : hochements de tête sur les mots (39 S06), recul de la tête à chaque coup de doigt (39 S07), tête qui bascule comme un
  punching-ball (39 S13), ronflement qui soulève la poitrine (39 S12), pigeons qui respirent, salut de la main en deux allers-retours (39 S11).
- **Temps suspendu** : après le geste, une tenue de soulagement de 10 à 14 images, puis le retour en 2 images (39 S17) ; une pose tassée tenue 7 images
  pendant que la caméra descend avec elle (39 S08).

### 4. Histoire 40 — « L'interrupteur » (type : un geste banal qu'une institution prend au pied de la lettre, escalade, retournement, aparté sec)

Texte (12 phrases, 30,1 s, voix de la série) : « Ce mec a éteint la lumière en sortant. Toute la ville s'est éteinte. Il a rallumé. Elle s'est rallumée.
La mairie a fait venir un électricien : « L'interrupteur général, c'est lui. » Depuis, il éteint Paris tous les soirs à vingt-deux heures. Les
cambrioleurs l'adorent. Les amoureux aussi. La facture arrive à son nom. Toute la facture. Il a demandé une augmentation. Il a eu une prime de nuit.
Hier à midi, il est sorti de chez lui. Par réflexe, il a éteint. Il fait nuit depuis. Les astronomes cherchent. La facture, elle, est déjà arrivée. »

Mise en scène (25 plans), gags visuels prévus, chacun sur une capacité du rig :
1. l'interrupteur au bout d'un bras élastique, le noir, ses yeux seuls, la caméra qui glisse vers eux (S01) ;
2. des yeux qui marchent dans le noir et se cognent à une porte vitrée ; la ville qui s'éteint par vagues, la tour en dernier, des yeux aux fenêtres (S02, S03) ;
3. la pince de l'électricien sur son nez, l'aiguille du compteur, le take (S07) ;
4. gag à répétition, trois variations : la cravate tirée comme le cordon d'une lampe (par l'électricien, deux paires d'yeux ; par lui-même au balcon,
   Paris s'éteint derrière lui ; à la bougie, la flamme et ses yeux restent) (S08, S11, S17) ;
5. l'étiquette « GÉNÉRAL » claquée sur le front (S09) ;
6. ce qui reste dans le noir : les sourires des cambrioleurs après l'allumette, les yeux en cœur des amoureux et une troisième paire (S12, S13) ;
7. l'enveloppe de la facture qui grandit et lui tombe dessus, des yeux dans sa fenêtre (S14, S15) ;
8. l'entrée fine comme une feuille dans le bureau du maire, puis le regonflage (S16) ;
9. le soleil a un visage : la main monte à la cravate, la dame tend le bras (« NOOON »), le soleil s'éteint comme une ampoule ; dans le noir, les yeux de
   toute la rue ; il s'en va sur la pointe des pieds (S18 à S22) ;
10. l'astronome, son télescope, sa torche ; l'enveloppe « LE SOLEIL / CHEZ CE MEC » qui arrive, des yeux dans sa fenêtre (S23 à S25).

Décisions prises sans question : pas de carte de titre arrêtée pour l'instant (elle sera choisie sur le brouillon) ; les cambrioleurs portent un bonnet
noir et un bandeau (le premier bonnet rouge se lisait comme un fez) ; la ville de nuit est un accessoire à part (rangées de toits en gradins sous une
ligne d'horizon), placé à l'intérieur du dôme du décor.


## Cycle 3, suite — histoire 39 « La porte » : revues et passes de mise en scène

### Première revue (animation 6,6 ; direction artistique 6,6, sur le brouillon)

Les deux relecteurs s'accordent : une mise en scène dense, un vrai gag à répétition (le bras), six gags qui se lisent du premier coup, mais les deux
moments qui portent la fin sont ratés. Dans l'ordre :
1. le take de S16 regarde à l'opposé de sa cause, plus petit que le premier take du film, coupé après 8 images ;
2. la chute (S17) n'a ni temps suspendu ni silhouette : les deux mains devant le torse, le bras remonte entre deux images, dernière tenue de 0,2 s ;
3. les aplatissements passent trop vite ou ne sont pas plats (casquette de S08, pressé de S09) ; S12 reprend la pose de S09 ; yeux en spirale quatre fois ;
4. la déformation sous la bande des sous-titres (le cou de S10, les pieds de S09) ;
5. S11 et S12 se lisent comme le jour ; S13 et S14 (tape, autoportrait, pigeon) ne se lisent pas ;
6. des tenues gelées (S06, S07, S13, S01) ; des enseignes coupées par les cadres serrés.

### Deux passes de mise en scène avant la deuxième revue

- **S16** : coupe au gros plan plus tôt, caméra presque de face (24° de son axe), le poing vide levé devant la poitrine, regard sur le poing, la porte,
  le poing ; élan ; le take vers nous, yeux ×1,3, pupilles baissées sur le poing ; il retombe au début de S17.
- **S17** : le doigt se lève une fois la dame passée ; il pousse son bras de côté, devant la porte claire (l'avant-bras plie et tremble) ; il lâche,
  soupir de 14 images ; ses yeux vont au bras, qui remonte en 2 images et dépasse, avec une onde ; la porte s'ouvre pour personne ; regard tenu.
  **Décision : le film gagne 0,7 s d'image après la voix (26,06 s, queue de 2,0 s)** ; le relecteur d'animation l'avait signalé comme nécessaire.
- **S08** : la casquette traverse le haut du cadre (4 images), la pose tassée est tenue 7 images, la caméra descend avec lui et remonte.
- **S09** : il part dès la coupe ; pressé à presque deux fois sa largeur derrière une vitre éclaircie ; l'affiche est tenue puis se décolle par le haut.
- **S10** : la course de caméra commence à la coupe ; le cou monte quand elle arrive, la tête contre le ciel.
- **S11** : remis en scène trois fois. De dos à hauteur d'homme, le bras partait dans l'axe et les pigeons étaient des boîtes ; version retenue : à travers
  la vitre du battant, caméra à 2,3 m, la main sur la poignée en bas, la manche qui monte jusqu'à lui ; nuit graduée, flaques de lumière, pigeons redessinés.
- **S12** : chambre de nuit ; il garde sa pose de sommeil sur le mur, avec son oreiller ; bulle « Zzz ».
- **S13, S14** : coupe à un plan à deux, trois tapes et la tête qui bascule, téléphone et flash ; plaque sur l'avant-bras ; pigeon de profil qui bat des ailes.
- **S05, S06, S07, S01, S02, S15** : passants entiers dans le cadre ou en traînées au premier plan ; hochements et compteur brandi ; le maire dans le cadre
  dès la coupe, de trois quarts, deux coups de doigt et la tête du héros qui recule ; regard vers la rue en fin de S01 ; technicien en bleu, casque blanc.
- **Enseignes** : la plaque qui claque en S08 et l'enseigne des plans suivants sont maintenant le même objet (deux lignes, liseré crème) ; l'insert
  contient la plaque entière. **Décision : une enseigne dont un cadre serré ne montrerait qu'un coin est rangée pour ce cadre** (`signHide`), plutôt que coupée.

### Deuxième revue (animation 7,4 ; direction artistique 7,5), puis troisième passe

Ce que les deux relecteurs demandaient encore, et ce qui a été fait :
- **S12 (sous le carton « LE BRAS RESTE »)** : il semblait debout près de la fenêtre, le bras ne se voyait pas. → il arrive à l'horizontale sur le mur
  (clip `wallBunk`), paupières fermées, oreiller collé, tache de lune ; la couverture, qui faisait un bloc sombre sous lui, est retirée.
- **S16** : le take de la chute reprenait celui de S03. → un autre take : il décolle des talons, la casquette reste en l'air quatre images, la mâchoire
  descend dans la paume, la casquette retombe et l'écrase ; regards poing, porte, poing de quatre à cinq images ; barbe sous le menton.
- **S13, S14** : les deux plaques illisibles. → la plaque du mur arrive avec le touriste, plan à deux ; « BRAS CLASSÉ » à plat côté caméra, seule une
  demi-seconde, puis le pigeon se pose plus haut.
- **S07, S13** : des coups reçus mollement. → le doigt du maire atteint le nez, la tête bascule sur un cou étiré ; même bascule en S13, plus loin.
  (Erreur trouvée ici : la flexion latérale était écrite dans la case de la torsion ; l'ordre est `[avant, côté, torsion, étirement, épaisseur]`,
  et un côté positif envoie le haut de la tête vers la DROITE du personnage.)
- **S11** : le réverbère derrière le bras, la manche sur le ciel. → réverbères déplacés, flaques de lumière au sol, lune basse derrière la main.
- **S15** : le technicien ressemblait au touriste. → casque de chantier jaune à visière, bleu de travail, tournevis, écusson MAINTENANCE.
- **S17** : la main qui pousse le bras ne se voyait pas. → caméra plus près, de côté, les deux mains devant le battant clair ; contact tenu quatre images.
- **Décision : la queue après la voix passe à 2,4 s (film de 26,46 s)** pour que le dernier gag ait le temps de respirer. La narration reste
  enregistrée sans pauses (règle de la série) : les battements secondaires qui ne tenaient pas dans les mots ont été retirés plutôt que les mots espacés.

### Deux erreurs du moteur trouvées pendant cette passe (corrigées, sans effet sur les histoires déjà rendues)

- **Une image éclairée à chaque coupe vers un plan sombre.** Une clé `dark` sans rampe (0,001 s) n'était atteinte qu'à l'image suivante : la première
  image du plan restait éclairée. Les deux relecteurs l'ont vue dans les planches. Une clé sans rampe tient maintenant dès sa propre image
  (`darkAt`) ; nouvel outil `tools/cut_flash_check.py FILM.mp4 scripts-fr/story_x.json` (une image isolée, différente de ses deux voisines, à une coupe).
  Les histoires 37 et 38 passent ce contrôle.
- **Le `darkEyes` d'un plan n'était jamais lu** (dans la boucle des acteurs, `sc` est l'échelle de l'acteur, pas la scène) : tous les yeux dans le noir
  étaient à 1,3. Lu maintenant par `S.sc.darkEyes`. Au-dessus de 1,9, la peau éclairée des yeux est agrandie autour du point entre les yeux : des « yeux
  de pièce noire », plus larges que la tête, pupilles trois fois plus grandes.

### Troisième et dernière revue (animation 7,7 ; direction artistique 8,0)

Blocage noté : les deux relecteurs du troisième tour ont d'abord été coupés par la limite d'usage du compte ; ils ont été relancés plus tard, sur les
mêmes pièces, et ont rendu leur rapport. (Ils n'écrivent pas leur fichier eux-mêmes : les deux rapports sont recopiés dans le dossier de revue.)

**Instruction de l'utilisateur, reçue pendant cette revue : toujours lancer la génération complète de la vidéo.** Décision de méthode, valable pour toutes
les histoires à venir : dès que la dernière revue est demandée, le rendu final complet (3D en 1080 × 1920, puis HyperFrames avec sous-titres, carton et
musique) part sans attendre les rapports ; la dernière passe se fait ensuite par plages re-rendues et recollées (`tools/splice_range.sh`), et chaque
version terminée est envoyée.

Ce que les deux rapports gardent : la casquette qui l'écrase (S08), le bras en corde à linge et l'affiche (S09), le premier take (S03), le cou en périscope
(S10), le plan à deux du touriste (S13), la plaque seule puis le pigeon (S14), le coup d'œil et l'appui à l'aveugle (S15), toutes les plaques sauf AUTO,
les décors de jour, les gags à répétition (le bras sous cinq formes, la barbe, la toile d'araignée, le pigeon).

Ce qu'ils demandent encore (dernière passe, par plages) :
1. **S16** : la porte ne travaille seule que huit images, le double regard est trop court, le haut du take dure quatre images, la paume est devant la
   bouche et non sous la mâchoire ; la casquette en l'air tombe sur les rayures de la banne (rouge sur rouge).
2. **S12** : le trajet du lit au mur ne se voit pas, pas d'amorti à l'arrivée, le bras qui le tient est un moignon dans la fenêtre ; il manque une flaque
   de lune sur lui, un cadre à la fenêtre, une tache de lumière au sol.
3. **S15** : le mot AUTO, sur lequel repose le retournement, n'est jamais net (derrière le coude du technicien).
4. **S17** : le doigt levé monte le long de la tête et retombe à la visière : un salut de portier, pas une protestation qui s'éteint ; le soulagement et
   le tressaillement des doigts sont trop courts.
5. **S13 contre S07** : le même coup deux fois (un doigt, la tête qui bascule). La règle « jamais deux fois le même gag » s'applique : S13 doit changer
   de mécanique (l'homme entier qui oscille, raide, comme une statue).
6. Tenues gelées (S15 après l'appui, les deux takes dont le bras libre ne bouge pas, S02 où cravate et cheveux ne réagissent pas aux passants).

## Cycle 4, suite — histoire 40 « L'interrupteur » : première revue (animation 7,0 ; direction artistique 6,8) et deuxième passe

Les deux relecteurs gardent : la cravate tirée comme le cordon d'une lampe, quatre fois et jamais pareil ; le take de l'électricien contre le flegme du
héros ; l'homme plat qui se regonfle en trois souffles (S16) ; l'enveloppe qui grandit à chaque mot (S15) ; S11 (la silhouette devant la ville qui
s'éteint, la tour dernière allumée : « la meilleure image du film ») ; le soleil qui s'éteint comme une ampoule ; les yeux ronds dans une fenêtre comme
règle à part (S03, S15, S25).

Ce qui ne passait pas, et la réponse :
1. **Les yeux dans le noir sont trop petits et trop immobiles** (2 à 4 % de la largeur du cadre, pupilles de 3 px ; S22 surtout : trois paires au lieu de
   « tous les yeux de la rue »). → un plancher de 5 % de la largeur pour tout œil qui porte un battement ; `darkEyes` de 2,2 à 3 dans tous les plans
   sombres ; S22 refait : le héros seul à gauche, dix paires qui s'ouvrent en vague (deux fenêtres, des passants, un chat), toutes se plissent sur lui,
   regard à gauche, à droite, trois pas sur la pointe des pieds avec un plongeon des yeux à chaque pas, toutes les pupilles le suivent.
2. **L'accroche (S01, S04)** : le bras étiré partait dans l'axe de l'objectif, l'interrupteur crème sur mur crème. → mise en scène en travers du cadre,
   interrupteur orange sur plaque claire et panneau gris, doigt retenu quatre images avant la tape.
3. **S15** : les yeux dans la fenêtre de l'enveloppe n'avaient que cinq images. → l'enveloppe tombe 0,1 s plus tôt, les yeux s'ouvrent deux images après,
   clignent avant la coupe.
4. **S13** : les amoureux brouillés. → de face, cœurs dès la troisième image, ils se penchent (flexion latérale, cette fois dans la bonne case) et
   glissent l'un vers l'autre, le cœur éclate où ils se touchent, la troisième paire s'ouvre entre eux, regard à gauche, à droite, descente lente.
5. **Contenu dans ou sous la bande des sous-titres** (fenêtres de S03 et S05, cadran de S07, tube de S23). → une maison en face avec trois grandes
   fenêtres entre 58 et 72 % de la hauteur (`nearHouse`) ; compteur tenu à hauteur de poitrine ; télescope refait (laiton, le plus large côté ciel,
   bagues, reflet sur la lentille), oculaire à hauteur d'œil, faisceau de torche peint à bords doux, vers le ciel vide.
6. **Recouvrements** : l'électricien devant le maire (S06) → il arrive en glissant sur les genoux, le doigt du maire passe au-dessus de lui ; têtes de
   profil trois plans de suite → l'électricien reste de trois quarts, seuls ses yeux vont au héros ; l'homme au chapeau derrière la tête du héros
   (S20, S21) → la foule est replacée, la dame à côté de lui, son bras traverse le cadre jusqu'à son poignet ; étiquette GÉNÉRAL sur un œil → plus
   petite, sur la ligne des cheveux ; bâillement grandeur nature (S10) → bras qui sortent du cadre en Y étroit, mâchoire au nœud de cravate.
7. **Les rares lumières dans le noir** : l'allumette éclairait toute la rue, la bougie n'éclairait rien. → nouveau réglage de plan `darkPool` : une
   flaque de lumière autour d'un accessoire (rayon en mètres, teinte), qui retombe au noir vers les bords.
8. **Tenues gelées** → la paume qui fait signe (S16), le hochement de tête de celui qui s'endort (S11), le gros plan de la facture devient le double
   regard du film (S14).

Erreur trouvée dans cette passe : des pas rapides écrits par `to` (0,24 m en 0,07 s) nourrissent les couches automatiques du rig (traînée de la colonne,
écrasement vertical) au point de coucher le personnage sur le côté. Réponse : un glissé par pas et les plongeons écrits à la main, avec `auto: 0`.
Autre erreur : à trois mètres de la caméra, le corps noir du héros cachait les paires d'yeux placées « à ses pieds » ; il est reculé derrière elles et ses
yeux sont agrandis d'autant (`darkEyes` 5,2).

### Histoire 39 : version 1 livrée, dernière passe écrite

- **Version 1 envoyée** : génération complète (1080 × 1920, 26,47 s, −16,1 LUFS, sous-titres, carton « LE BRAS RESTE »), contrôles passés (aucune image
  isolée aux coupes ; les alertes de `flash_check.py` sont le flash de l'autoportrait et trois changements de cadre à l'intérieur d'un plan).
- **Dernière passe (version 2), écrite d'après la troisième revue** ; le rendu complet suivra celui de l'histoire 40 :
  S12 : le lit est retourné (`bedFlip`) pour que sa tête reste du même côté du lit au mur (elle changeait de côté en une image), le bras sort par le coin
  haut d'une fenêtre de nuit (`nightWindow` : ciel, lune, croisillons) et traverse la vitre en diagonale, trajet en quatre images, écrasement, puis le
  bras libre, les jambes et la cravate oscillent et s'arrêtent, l'oreiller arrive en retard, clair de lune sur lui (`darkPool` qui suit un acteur) et
  au sol ; le plan prend six images à S11 et le carton tombe au moment où il est emporté (`st.card(..., at=0.42)`).
  S13 : le touriste ne fait plus basculer sa tête (c'était le coup du maire) : l'homme entier oscille, raide, comme une statue (`statueRock`).
  S15 : boîte à hauteur de tête à côté du casque, AUTO deux fois plus grand sur sa propre plaque, coupe six images après le voyant vert.
  S16 : sept images de plus prises à S15 : la poignée lui échappe des doigts, la porte travaille seule seize images ; vrai regard vers la porte puis
  retour au poing ; le haut du take tenu six images ; la mâchoire tombe sur une paume placée dessous, qui plie ; casquette en l'air devant la vitre sombre.
  S17 : la mâchoire reste dans la paume jusqu'à ce que la dame paraisse ; le doigt se lève à l'écart de la tête, vers elle ; la main retombe jusqu'à la
  hanche avant la coupe (elle s'arrêtait à la visière : un salut) ; soupir de quinze images, tressaillement de sept ; le bras remonte, dépasse, rebondit.
  S01 (révérence de trois quarts), S02 (cravate, cheveux et épaules réagissent à chaque passant), S03 (cou en avant : la mâchoire passait derrière le
  col ; la main libre sursaute), S05 (la tête de l'agent balaie vraiment), S09 (onze images au bout du bras avant le rappel).
- **Décision** : pas de quatrième revue pour l'histoire 39 (trois au plus) ; la version 2 sera envoyée après contrôle sur images fixes.

### Histoire 40 : deuxième et troisième séries de corrections, deuxième revue demandée, génération complète lancée

- Sur images fixes : S02 (les quatre images d'yeux écrasés étaient noires : une expression forte commence par un clignement automatique), S06 (le
  compteur cachait le visage de l'électricien ; le bras du maire passe maintenant par-dessus son casque), S10 et S11 (bonnet de nuit de l'autre côté,
  lune au-dessus de l'horloge), S13 (les deux paires étaient un tas de cœurs : chaque tête penchée de 30° pour une paire horizontale, corps décalés
  d'autant), S20 et S21 (foule replacée, ciel sans nuage, yeux à 4,6 vus de loin), S23 (torche dans l'autre main, au-dessus de sa tête).
- Erreur ancienne trouvée par l'avertissement « NaN » du rendu : les mâchoires de la pince du compteur n'avaient jamais été visibles (option `taper`
  donnée sans `z`). Leçon : un avertissement de géométrie dans le journal de rendu se traite avant le rendu final.
- Brouillon 3 (30,13 s) : aucune image isolée aux coupes. Deuxième revue demandée aux deux relecteurs sur 73 pièces.
- **Conformément à la consigne « toujours lancer la génération complète », le rendu final de l'histoire 40 est parti en même temps que la revue** ;
  les corrections de la revue seront faites par plages, ou par une version 2.

### Histoire 40 : deuxième revue (animation 7,8 ; direction artistique 7,5) et troisième passe

Gardé par les deux relecteurs : le noir comme procédé graphique, avec des yeux à la bonne taille (12 à 15 % de la largeur dans S01, S02 et pour la
troisième paire de S13 ; 5 à 6 % par œil pour les dix paires de S22, où ses yeux crème et de travers le distinguent de tous) ; la cravate tirée comme le
cordon d'une lampe, quatre fois et jamais pareil ; le take de l'électricien ; S11 (« la meilleure image du film ») ; la flaque de l'allumette et celle
de la bougie ; le double regard de S14 ; l'enveloppe ; le soleil-ampoule ; le télescope et le faisceau ; l'enveloppe aux deux yeux comme dernière image.

Demandé, et réponse (troisième passe, écrite pendant le rendu de la version 1) :
1. **S22 : six battements en 1,13 s.** → la vague, puis les regards plissés tenus huit images pendant que ses pupilles glissent UNE fois, lentement, sur
   toute la rue ; deux grands pas au lieu de trois ; les yeux de la foule un peu moins blancs que les siens.
2. **S16 joué au bord du cadre et trop vite.** → lui à 60 % de la largeur, sous le blanc de la bande MAIRIE ; le trait tenu neuf images ; trois souffles
   espacés de 0,14 s ; la paume ne fait signe qu'une fois.
3. **Tenues mortes.** → la dame tremble et son chapeau sautille ; les deux passants s'éloignent en marchant puis sortent du film ; les cœurs battent
   (la tête grossit de 16 % trois fois) ; l'électricien tend la main vers la cravate dès la première image ; les yeux de la dernière enveloppe vont à
   chaque bout de la fenêtre, huit images, reviennent, clignent tard.
4. **Accents de quatre images ou moins.** → S01 : le doigt retenu huit images (le lancer part 0,12 s plus tôt) ; S02 : yeux écrasés six images, les
   spirales s'arrêtent au-dessus des sous-titres ; S09 : un élan avec l'étiquette visible dans la main ; S12 : le pouce disparaît, reste le clin
   d'œil ; S15 : un regard vers nous avant que les genoux cèdent.
5. **Silhouettes et répétitions.** → S10 : clair de lune de face sur les manches (bleu marine sur ciel bleu marine : aucune silhouette), bouche aussi
   large que le bas du visage ; S17 : son visage reste de trois quarts, le maire se penche dans la lumière de la bougie (le sourire dans le noir était
   celui des cambrioleurs) ; **le take de la dame était celui de l'électricien** (yeux sur tiges) : elle se tasse sous son chapeau, qui reste en
   l'air et retombe en retard ; télescope qui sort du cadre ; notes crème dans le ciel.
6. **Décor sur les têtes** : plus de tableau derrière les deux têtes de S06 à S09, tableau déplacé dans l'accroche ; S09 coupe à un gros plan du
   front : GÉNÉRAL occupe un tiers du cadre.
7. **S13** : deux paires d'yeux ronds cinq images, puis des cœurs posés sur le blanc de l'œil (moteur : un cœur dans le noir garde son blanc) ; un
   cœur plat et clair entre elles, qui éclate avant que la troisième paire descende. S04 : gros plan sur ses yeux dans le noir, puis coupe au large.
8. **Finitions** : faisceau de la tour en coin de lumière additif (c'était une barre grise), halos doux, pompon du bonnet attaché et coloré (il
   flottait : une seconde lune), lune dans le cadre, soleil plus haut (un rayon finissait sur le chapeau de la dame), plus rien du facteur dans le noir.

Erreur de moteur trouvée grâce à la revue : **un trait sombre dans les yeux agrandis**. Une pupille dessinée trois fois sa taille prenait le bord du
sprite voisin dans la planche ; les sprites agrandis sont maintenant tirés d'une copie isolée (marge de 2 px).

Note des relecteurs transmise sans décision de ma part (elle touche au texte enregistré, qui est fixe) : 39 % du film est noir, les 6,5 dernières
secondes sans interruption ; le relecteur ne demande pas de changement.

## Cycle 5 — ce qui pend suit, ce qui se pose s'amortit (commencé pendant les rendus des histoires 39 et 40)

### 1. Analyse (troisième revue de l'histoire 39, deux revues de l'histoire 40, rigs des cycles 1 à 4)

Faiblesses relevées, par ordre de fréquence dans les rapports :
1. **Les poses s'arrêtent net et rien ne suit.** « Characters stop dead between poses » (39), « holds that die » (40) : après un coup, un rappel, une
   pose atteinte, le bras libre, les jambes, la cravate, les cheveux, un oiseau sur une casquette restent inertes. Le rig a une traînée des membres
   sur la vitesse de leurs propres articulations, mais rien ne répond aux accélérations du corps, et rien ne continue après l'arrivée. **Corrigé dans ce cycle.**
2. **Trop de battements par plan.** La narration sans pause laisse 1,1 à 1,5 s par plan ; trois battements y sont illisibles. **Corrigé par la méthode** :
   un battement par plan de moins de 1,2 s ; un plan qui en porte deux commence avant ses mots (coupe à un temps absolu) ; un accent tenu vaut six
   images au moins.
3. **La même mécanique deux fois dans un film** (deux coups de doigt, deux takes à yeux sur tiges, deux sourires dans le noir) : la règle de
   l'utilisateur. **Corrigé par la méthode** : avant la mise en scène, la liste des mécaniques du film, une seule fois chacune.
4. **Pupilles trop petites, regards qui ne se lisent pas de loin.** **Corrigé dans ce cycle** (canal `pupilSize`).
5. **Décor et figurants sur les têtes, texte trop petit** : relevé à chaque revue. **Méthode** : un mur nu derrière les têtes d'un plan à deux ; un mot qui
   porte la chute occupe 30 % de la largeur ou a son gros plan.
Choix : 1 et 4 par le rig, 2, 3 et 5 par des règles ajoutées au skill.

### 2. Rigs (ajouts en option ; sans eux un personnage est exactement celui du cycle 4)

- **Suite du mouvement** (`st.write(..., follow=1)` ou `toon: {follow: 1}` sur un personnage) : les bras libres se comportent en pendules amortis.
  Il démarre, ils restent en arrière ; il s'arrête net, ils continuent, reviennent, s'arrêtent en deux ou trois oscillations ; l'avant-bras suit le
  bras avec 0,05 s de retard ; la tête retarde sur le cou ; la cravate et les cheveux reçoivent le même élan (`wind`). Sans état, comme tout le
  moteur : l'accélération de sa position sur les 0,75 dernières secondes, pondérée par la réponse d'un pendule (12,5 rad/s, amortissement 0,2).
  Une main guidée (`reach`, `touch`) ou un bras levé par le clip ne balance pas.
- **Amorti d'une pose** (`'settle': 0.6` dans une clé `toon`) : une fois la clé atteinte, la colonne oscille encore et meurt en 0,5 s, le corps cède
  un peu : une pose qui se pose n'est pas une pose qui s'arrête.
- **Accessoires qui ne sont pas cloués** (`on={..., 'sway': 1}`) : un oiseau sur une casquette, une enseigne sur une tête, un sac : ils basculent
  autour de leur pied avec l'élan de celui qui les porte.
- **Taille des pupilles peintes** (`face.pupilSize`, `pupilSizeL`, `pupilSizeR`) : 1 = deux fois plus grosses (un regard qui se lit de loin),
  −0,5 = des têtes d'épingle (la peur).
- Compléments du cycle 4 faits pendant les revues : flaque de lumière (`darkPool`), yeux de pièce noire, `eyesPair` (paupières, regard, fenêtre),
  `statueRock`, `nightWindow`, `bedFlip`, cœurs sur le blanc de l'œil dans le noir, sprites agrandis sans bavure.

### Histoire 40 : version 1 livrée ; troisième passe contrôlée sur images fixes, appliquée, brouillon 4

- **Version 1 livrée** (rendu complet 1080×1920, 30,13 s, −16,0 LUFS, aucune image isolée aux coupes ; `hyperframes/40-interrupteur`). Revues sur
  brouillon : 7,0 / 6,8 puis 7,8 (animation) / 7,5 (direction artistique).
- **Troisième passe** écrite comme un correctif de texte du script (appliqué seulement après la construction du projet de la version 1 : on ne
  régénère jamais un script entre le début de son rendu final et son projet), vérifiée sur deux planches d'images fixes rendues depuis une copie.
  Ce que les images fixes ont encore montré, corrigé avant le brouillon :
  - S09 : au moment de la claque la tête s'enfonçait de 28 cm sous une main restée en l'air → la main guidée descend avec le front ; l'étiquette
    montrée à hauteur de poitrine (elle cachait le menton) ; l'élan au-dessus de sa tête, dans le cadre.
  - S09, gros plan : les yeux « qui louchent vers l'étiquette » étaient deux fentes grises : l'expression `unimpressed` a les paupières à mi-course
    et **un canal de visage ne peut que fermer une paupière, jamais l'ouvrir** → changement d'expression (`worried`, qui n'est pas une expression
    forte : pas de clignement automatique), pupilles agrandies (`pupilSize`). Focale plus longue (28 au lieu de 44, même place) : plus de main coupée
    au bord, plus de rideau rouge collé à l'oreille, le mot occupe la moitié de la largeur.
  - S01 : le héros était coupé par le bord gauche (main droite hors cadre), l'interrupteur à 3 % du bord droit → lui 18 cm plus à droite,
    l'interrupteur 10 cm plus à gauche, le tableau recentré dans l'intervalle.
  - S10 : le pied de la tour touchait son oreille → tour plus petite, au bord droit.
  - S08 : ce qui ressemblait à des yeux « en fentes » de l'électricien était son clignement (l'image fixe tombait dessus) : rien à corriger, mais
    son texte se dit maintenant avec l'expression neutre (yeux ouverts dans le noir).
- **Décision** : pas de quatrième revue (trois au plus). La troisième revue se fait sur le brouillon 4 ; la génération complète de la version 2 est
  mise en file derrière celle de « La porte » version 2 (une seule génération complète à la fois : deux en parallèle doublent la durée de chacune).

### 3. Animations (cycle 5)

Trois clips nouveaux pour un homme qui ne peut pas s'arrêter et ceux qu'il transporte (dans `engine/animations.js`) :
- `heelBrake` : freinage aux talons qui ne freine pas (penché en arrière sur des jambes tendues, pointes levées, bras en moulinets l'un après
  l'autre, tout le corps qui broute sur le sol à 15 Hz) ; se pose sur un déplacement rapide en `glide`. Ce n'est pas le `skidStop` de l'histoire 37
  (un arrêt en 0,4 s) : celui-ci dure, c'est le gag.
- `flag` : accroché des deux mains derrière un coureur, le corps à l'horizontale comme un drapeau, jambes qui flottent, tout le corps en pendule
  (`swing`, `freq`, `phase` pour décaler plusieurs passagers) ; `dir: -1` : sur le dos, les pieds devant (emporté au-delà d'un poteau qu'on tient).
- `shoulderRide` : assis sur les épaules d'un autre, rebond calé sur sa foulée.
La suite du mouvement (cycle 5, rig) sert sur ces clips : bras libres en pendules, cravate et cheveux au vent du déplacement.

### 4. Histoire 41 — « L'élan » (type : un geste banal qu'une institution prend au pied de la lettre, escalade, retournement, aparté sec)

**Texte** (13 phrases, 27,97 s, narration faite) : « Ce mec a couru pour attraper son bus. Il n'a pas réussi à s'arrêter. Il a dépassé le bus. Puis la
ville. Au troisième tour, des gens sont montés. La mairie a tranché : « C'est une ligne. » Depuis, il passe toutes les huit minutes. Il a un
numéro. Il a des contrôleurs. Il a demandé à descendre. On lui a répondu : « Au terminus. » Il n'y a pas de terminus. Hier, il a enfin réussi à
s'arrêter. Pas ses passagers. Ils sont arrivés en avance. C'est une première. »

**Décisions de mise en scène** (consignées ici, sans question à l'utilisateur) :
- **Le bus est modélisé à la main** (`cityBus`). La banque sand3d a été consultée d'abord, comme le veut le skill : 56 bus trouvés (planche vue),
  aucun n'a de cabine transparente où asseoir un chauffeur et des passagers, ni de girouette à texte, ni de portes qui s'ouvrent : le rôle demande
  les trois. Aucun feu tricolore dans l'index : modélisé aussi (il doit changer d'état et plier).
- **Cadre vertical et bus** : un bus de 7,6 m et un coureur côte à côte ne tiennent pas dans 25° de champ horizontal. L'accroche est donc en deux
  cadrages dans le même plan : d'abord lui, gros, de trois quarts face, la caméra reculant devant lui (première image forte) ; puis, de derrière, le
  bus à son arrêt et les portes qui se ferment devant lui (« son bus »). Les trajets rapides sont filmés dans l'axe (vers la caméra ou en s'en
  éloignant) ou en travelling à sa vitesse, jamais en travers d'un cadre fixe (il le traverserait en quatre images).
- **Liste des mécaniques, une fois chacune** (règle du cycle 5) : course en roue et bras levé ; freinage aux talons qui ne freine pas (il garde la
  pose jusqu'à la sortie de la ville) ; double regard du chauffeur avec la casquette qui tourne comme une toupie ; panneau de sortie de ville en
  girouette ; compteur de tours et embarquement à la volée ; le maire qui « tranche » son bureau ; l'afficheur à 0 minute et le poteau qui plie
  dans son sillage ; enseigne de ligne sur la tête ; contrôleur sur ses épaules et tickets levés ; langue au vent et bouton d'arrêt sur le nœud
  de cravate ; le contrôleur à l'envers ; pupilles en têtes d'épingle ; arrêt au feu rouge en s'accrochant au poteau (étirement horizontal) ;
  passagers qui continuent sans lui ; rangée de montres ; « hors service » et un second coureur qui ne peut pas s'arrêter.

### Histoire 39 : version 2 livrée

Rendu complet de la dernière passe (1080×1920, 26,47 s, −16,0 LUFS, aucune image isolée aux coupes), envoyé ; `hyperframes/39-porte` mis à jour.
Pas de quatrième revue (trois au plus) : les notes restent 7,7 (animation) et 8,0 (direction artistique) sur le brouillon de la troisième revue.

### Histoire 40 : troisième et dernière revue (animation 8,1 ; direction artistique 7,7) et dernière passe

Progression : 7,0 / 6,8 → 7,8 / 7,5 → **8,1 / 7,7**. Seuil visé (8,5) non atteint ; trois revues au plus : la dernière passe ci-dessous est faite sans
nouvelle revue, vérifiée sur images fixes, puis la version 2 est rendue en entier.

**Décision d'ordonnancement.** La génération complète de la version 2 a été mise en file dès la demande de la revue, derrière celle de « La porte »
(un seul rendu complet à la fois). Les deux rapports sont arrivés pendant que le processeur était encore pris : la file a été retenue vingt minutes
(un fichier témoin que la boucle d'attente surveille) pour que le rendu parte avec les corrections, plutôt que de rendre 55 minutes une version déjà
dépassée puis de recoller des plages sur plus de la moitié du film.

**Ce que les relecteurs ont relevé, et ce qui a été fait :**
- *Traits fins dans les yeux agrandis du noir* (relevé deux revues de suite) : ce n'était ni la feuille de sprites ni le dessin 2D (vérifié en
  sortant le canevas des yeux seul : propre). **Cause : les cheveux et les oreilles, sur les côtés de la tête, passaient 12 mm devant la peau des
  yeux agrandie et y découpaient un trait vertical.** Corrigé dans le moteur : la peau agrandie est posée 45 mm devant le visage. Le trait de
  l'enveloppe finale disparaît du même coup. Les ovales des yeux en cœur, coupés à plat par le bord du canevas du visage, glissent maintenant vers
  l'intérieur comme les yeux ouverts.
- *Amoureux (S13)* : un œil touchait le bord droit du cadre ; la troisième paire traversait leur ligne. → cadre décalé de 7 cm, paires 14 % plus
  petites, la troisième paire rétrécit en descendant, s'arrête au-dessus d'eux et ferme les paupières.
- *Raccords* : la bosse disparaissait à la coupe S08/S09 → il l'a encore à l'ouverture de S09 et la claque l'écrase ; l'homme du balcon changeait de
  couleur entre S10 et S11 → même lumière de lune sur les deux plans.
- *Détails trop petits* : le doigt s'arrêtait à 1 % de la largeur de l'interrupteur (il semblait le toucher) → 6 %, main grossie ; étoiles de la bosse
  doublées ; œil de l'astronome trop petit → le plan s'ouvre plus près et recule quand il recule ; paume de S16 grossie.
- *Poses* : doigt du maire redescendu au-dessus du front ; pouce de l'électricien sorti à gauche du cadre ; yeux de la dame avec des pupilles.
- *Rythme* : S08 (un petit essai de traction avant la vraie, et dans le noir un seul regard échangé, sans clignement) ; S09 (étiquette montrée quatre
  images, armée au-dessus du casque) ; S14 (double regard plus dur : pupilles en têtes d'épingle, tête étirée) ; S16 (ligne tenue cinq images de
  moins, souffles de quatre à cinq images, le maire recule à chacun) ; S22 (la foule s'ouvre en deux groupes, le regard noir se pose à 0,3 s et tient) ;
  S24-S25 (l'enveloppe arrive en deux pas marqués, une seule arrivée ; les yeux de la fenêtre : un regard vif d'un côté tenu dix images, de l'autre
  cinq, un retour lent, un clignement tardif, une petite déglutition de l'enveloppe).
- *Finitions* : halo de la bougie éteint tant que la pièce est éclairée ; soleil décalé (rayons coupés par les façades) ; mains dans le cadre en vue
  de dessus (S15).
- **Laissé de côté, noté pour mémoire** : le coussin rouge derrière sa hanche (élément du décor), deux fenêtres allumées derrière ses mains (S10),
  la fin du faisceau de la tour, l'arbre entre deux têtes (S20).
- **Remarques « pour l'utilisateur » des relecteurs, consignées sans question** : (1) garder libre la colonne des boutons à droite sur TikTok et
  Reels : retenu comme règle de cadrage (rien d'essentiel à moins de 8 % du bord droit) ; (2) le casque de l'électricien lu comme un chapeau jaune à
  bord : à reprendre si le personnage revient ; (3) plus d'un tiers du film est noir : choix assumé de l'épisode, à ne pas répéter sans un liseré sur
  les silhouettes.

### Histoire 41 — mise en scène : ce que les images fixes ont changé (deux passes avant le premier brouillon)

- **Accroche** : la première version (lui de face, puis le bus vu de derrière) ne montrait pas un bus lisible et cachait le héros derrière le poteau
  d'arrêt. Version retenue : un seul cadrage de trois quarts face, la caméra recule devant lui ; **le bus roule à côté de lui** (porte, girouette « 12 »,
  une passagère qui lui fait signe derrière la vitre) pendant qu'il frappe trois fois à la porte ; puis le bus freine et sort du cadre : sa main reste
  en l'air. Le plan suivant (freinage aux talons) regarde en arrière : le bus arrêté rapetisse derrière lui, girouette et chauffeur visibles.
- **Le maire « tranche »** : un bras levé tendu sous une écharpe tricolore se lit comme un salut (règle du skill) : les deux mains jointes au-dessus de la
  tête, comme une hache ; le bureau se fend en V.
- **Le contrôleur** : assis sur les épaules du héros, il remplissait tous les gros plans d'une masse bleue et cachait l'afficheur ; plié en avant « tête en
  bas devant son visage », il ne montrait que son dos. Version retenue : il **surfe sur le dos de la passagère** pour contrôler les tickets (S12), puis
  **descend dans le cadre pendu tête en bas comme une chauve-souris**, à côté de la tête du héros, les deux visages vers nous (S14, S15) ; il remonte
  hors cadre au début de S16 ; au feu rouge il continue tout droit.
- **L'arrêt au feu** se joue de profil avec une focale large (le trottoir n'a que 5 m de recul) : le poteau à gauche, la route pour s'étirer ; puis un
  gros plan pour la vapeur aux oreilles. « Pas ses passagers » reprend le même profil : il est planté au poteau, ils traversent le cadre à l'horizontale.
  Vus de face, des corps qui volent vers la caméra ne se lisaient pas.
- **Fin** : vue d'en amont, le feu au-dessus de lui (ses lentilles vers nous : on le voit passer au vert), l'afficheur « HORS SERVICE » ; le second
  coureur qui ne peut pas s'arrêter passe et s'éloigne.
- Pièges notés : après un déplacement `glide`, le clip redevient `idle` (quatre passagers « assis » sur un banc étaient debout) : clé de clip explicite à
  l'arrivée ; `checkWatch` est debout : clip `sitWatch` ajouté ; le siège d'un chauffeur trop haut lui met la tête au plafond ; en gros plan, viser la tête
  réelle d'un coureur (0,45 m devant ses pieds, 0,3 m plus bas que debout), pas ses pieds.

### Histoire 41 — troisième passe sur images fixes ; cycle 5 : contrôle de non-régression

- **Trouvaille (moteur)** : en course, l'écrasement automatique de chaque appui tombe sur une seule image, jamais la même (4,4 foulées par seconde :
  un appui toutes les 3,4 images) ; mesuré : hauteur du corps 0,76 · 1,05 · 1,02 · 0,91 · 0,98 · 1,01 · 1,04 · 0,82… La tête du héros descendait de 40 cm
  pendant une image, sortait des gros plans, et l'afficheur sur sa tête devenait illisible (un tiers du film est en gros plan sur un coureur).
  Ajout au moteur, optionnel (sans lui rien ne change) : `autoSq` dans une clé « toon » dose l'écrasement et l'étirement automatiques seuls ;
  0,3 dans la base de course du héros : il reste un rebond, la tête tient en place (vérifié sur 14 images de gros plans).
- **Contrôleurs (S12)** : les tickets faisaient 8 % de la largeur et le héros était coupé au bord. Décision : caméra à hauteur du héros, sur le côté ;
  le héros hors champ (seul le parapluie va vers lui), le contrôleur en pied sur le dos de la passagère, les deux voyageurs et leurs tickets (50 cm) en
  diagonale vers le fond.
- **Tête en bas (S14–S16)** : le contrôleur pendait une demi-tête trop bas et son bras cachait la moitié de l'afficheur : remonté de 48 cm, écarté de
  14 cm, caméra plus de face ; l'afficheur reste dans le cadre pendant le resserrement de S16.
- **Au feu (S18, S19)** : poteau un peu plus dans le cadre, balancement raccourci (les pieds sortaient à droite) ; « Pas ses passagers » a son propre
  cadre, plus serré : lui en pied au quart gauche, ils passent derrière lui.
- **Gare (S20)** : les quatre resserrés sur le banc et caméra reculée : plus personne dans les 8 % du bord.
- **Fin (S22)** : le second coureur n'était qu'un bras au bord du cadre, puis un dos, et le héros nous tournait le dos pour le suivre. Décision : il
  arrive **du fond de la rue, de face**, derrière le héros qui a les yeux fermés (on le voit venir, pas lui), passe à 50 cm de son épaule et sort à
  gauche de la caméra ; le vent de son passage ouvre les yeux du héros, sa tête le suit vers nous et revient ; cadre large au passage, puis la caméra
  avance sur celui qui reste ; feu vert, regard au feu, regard vers nous : il reste. (Le coureur va en sens inverse de la ligne : assumé, c'est un
  autre départ.)
- **Non-régression du cycle 5** (anciennes histoires rendues avec le moteur actuel, comparées à leurs images de référence) : au pire 0,49 % de pixels
  changés ; « Le trou » 0,16 % ; « L'éternuement » : mêmes écarts qu'au cycle 4, au centième près (écarts connus entre le script actuel et la couche 3D
  livrée) : les ajouts du cycle (suite du mouvement, amorti, oscillation des accessoires, pupilles, langue au vent, dosage de l'écrasement) sont tous
  optionnels et ne modifient aucune ancienne animation.
- Skill : trois règles ajoutées aux « Erreurs à éviter » (course vue de près, passant filmé de face, file dans la profondeur) ; `autoSq` documenté dans
  la référence du rig.

### Premier brouillon de l'histoire 41 : ce que les planches image par image ont montré ; rendu de l'histoire 40 coupé puis récupéré

- **Sursaut à chaque coupe (moteur)** : sur les planches, la dernière vignette de chaque plan de course montrait le héros qui « plonge », la première
  un corps penché en arrière. Cause : le moteur lit la vitesse et l'accélération par différences sur deux ou trois images ; un déplacement qui
  commence à la première image du plan et finit à la dernière est vu comme un départ arrêté et un arrêt net (colonne qui traîne, bras en pendule,
  changement de cycle avec anticipation). Ajout optionnel `cruise` sur une clé de déplacement : avant la clé et après la fin, la position continue
  sur la même droite, le cycle garde la même horloge, pas de fondu d'entrée. Appliqué aux 19 déplacements de l'histoire qui traversent leur plan
  (41 clés) ; vérifié sur 28 images de début et de fin de plan. Les anciennes histoires n'utilisent pas l'option (contrôle de non-régression relancé).
- **Dernier plan** : le second coureur recouvrait tout le cadre pendant une image en passant devant l'objectif : sa trajectoire s'écarte de 1,3 m
  (une seule clé à deux tronçons, pour que ses bras ne repartent pas de zéro), caméra fixe pendant le passage, avancée ensuite.
- **S10** : la demi-seconde vide après son passage reçoit une plume du pigeon qui redescend (accessoire `feather`). **S01** : le bus a un bruit de
  moteur.
- **Incident** : la génération complète de la version 2 de « L'interrupteur » a été tuée à 740 images sur 904 par la limite de durée des tâches de
  fond (la tâche comptait aussi l'attente dans la file). Décision : ne pas tout relancer (une heure) ; les images déjà encodées ont été récupérées
  dans les segments sans index (outil `tools/recover_mp4.py` : 239 + 229 + 272 images, alignement vérifié contre l'ancien rendu), trois plages
  manquantes rendues (dont le plan S08 avec son correctif, qui n'a donc plus besoin d'un recollage), un seul encodage pour réunir les six morceaux.
  Règle ajoutée au skill : lancer les rendus longs détachés de la tâche de fond et les suivre par leur journal.
- **Suite de l'incident** : (1) la première jonction a donné 40 302 images (les flux récupérés, donnés bruts, étaient mal horodatés) : le
  garde-fou sur le nombre d'images l'a arrêtée ; refaite à partir des flux ré-encodés. (2) Au contrôle des raccords, deux images (523-524) étaient
  plus sombres d'un diaphragme : la sonde de lumière et l'exposition d'un plan sont mesurées sur la première image rendue dans ce plan, et la plage
  commençait au milieu du plan de l'enveloppe. Décision : corriger le moteur plutôt que la plage (en entrant dans un plan par son milieu, il mesure
  d'abord sur la première image du plan), puis re-rendre les trois plages et refaire la jonction. Le défaut existait en puissance dans tout rendu
  découpé entre plusieurs processus ; les images fixes de contrôle ont désormais la lumière du film. (3) Une boucle d'attente qui cherchait son
  propre nom ne se terminait pas : la génération complète de l'histoire 41 attendait pour rien ; remplacée par l'attente d'une ligne de journal.
