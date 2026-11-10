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
