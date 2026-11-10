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

