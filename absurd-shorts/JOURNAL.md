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
