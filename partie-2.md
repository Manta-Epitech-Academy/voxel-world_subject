# Partie 2 : des collines au monde entier

Cinq étapes de plus : les vagues, le vrai relief, la mer et la neige, puis les forêts, les grottes et les minerais. Même fonctionnement : les outils, les pièges, le défi, et le code de l'encadrant quand c'est réussi.

## Étape 6 : La vague
<!-- ws: {type: exercise, id: collines, points: 200, token_id: "4"} -->

Ta pente monte tout droit, comme une rampe. La nature, elle, fait des bosses et des creux : il est temps d'améliorer le relief de ton monde.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **`math.sin` « la vague »**
> `math.sin(t)` monte et descend entre -1 et 1, comme une vague. Trois nombres la règlent : le `20` dit à quelle hauteur elle flotte, le `5` sa **hauteur**, le `/ 8` sa **largeur**.
>
> ```lua
> for x = 0, TAILLE - 1 do
>   local h = 20 + 5 * math.sin(x / 8)
>   set_block(x, h, 0, HERBE)
> end
> ```
>
> ![La vague, terme par terme : ÷ 8 l'élargit, × 5 la grandit, + 20 la monte, et les colonnes suivent la courbe.](img/etape6-vague.webp)
> <!-- ws:anim {src: img/etape6-vague.webm, chapters: img/etape6-vague.vtt} -->

<!-- /ws:toolbox -->

### Pièges

- `math.sin(x)` tout seul ondule beaucoup trop vite : une vague tous les 6 blocs. Divise x pour élargir.
- Avec une vague trop haute, `h` peut dépasser 63 (le ciel) ou descendre sous 5 (plus de place pour les couches).

### Défi
<!-- ws:doit -->

Fais onduler ton terrain le long de x avec `math.sin` : au moins **8 hauteurs différentes**, et jamais une marche de plus de **2 blocs** entre deux colonnes voisines. Les couches de l'étape 4 restent obligatoires.

Ce que tu dois avoir pour valider cette étape :
- Des collines douces avec les bonnes couches

Tu dois obtenir quelque chose comme ça :

![Des vagues de plage : le terrain ondule de gauche à droite, et chaque vague traverse le monde d'un bord à l'autre.](img/etape6-resultat.png)
<!-- ws:scene {src: scenes/etape6.glb, show_axis: true, camera: {from: [-30, 72, -30], to: [64, 12, 64]}} -->

<!-- ws: {type: hint} -->
<details><summary>Indice 1</summary>

Garde ta fonction `colonne` telle quelle : seule la ligne qui calcule `h` change.

</details>

<!-- ws: {type: hint} -->
<details><summary>Indice 2</summary>

Commence avec une petite hauteur de vague, par exemple `2 * math.sin(x / 8)`, génère, puis augmente-la.

</details>

<!-- ws: {type: hint} -->
<details><summary>Indice 3</summary>

Si la vérification parle d'une marche trop haute, **divise** x par un plus grand nombre.

</details>

## Étape 7 : Les collines
<!-- ws: {type: exercise, id: collines-deux-sens, points: 150, validation: checkpoint} -->
<!-- étape de modelage : la formule à deux vagues est donnée volontairement dans la boîte à outils -->

Ton monde ressemble à une **tôle ondulée** sur un seul axe. Il manque des bosses et des creux sur l'autre axe horizontal.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **Une vague en x, une vague en z**
> Avec `math.sin(x / 8)` seul, toutes les colonnes qui ont le même x ont la même hauteur, quel que soit z : rien ne change quand tu avances vers le fond. Pour que ça bouge aussi dans ce sens, ajoute une deuxième vague qui, elle, regarde z. Les deux s'additionnent : la tôle ondulée devient une **boîte d'œufs**.
>
> ```lua
> local h = 20 + 4 * math.sin(x / 8) + 4 * math.sin(z / 11)
> ```
>
> ![Avec une seule vague en x, le terrain est une tôle ondulée : rien ne change en avançant vers le fond. La vague en z s'ajoute, et les bosses apparaissent dans tous les sens.](img/etape7-collines.webp)
> <!-- ws:anim {src: img/etape7-collines.webm, chapters: img/etape7-collines.vtt} -->

> 🧰 **Pourquoi 8 et 11 ?**
> Deux largeurs différentes, pour que les bosses ne tombent pas toutes au même endroit. Essaie `8` et `8`, puis `8` et `11`, et regarde la différence depuis le ciel.
<!-- /ws:toolbox -->

### Pièges

- Deux vagues de hauteur 4 font une hauteur totale de 8 : vérifie que `h` reste entre 5 et 63.
- Si tu écris `math.sin(x / 8 + z / 11)`, c'est **une seule** vague, en diagonale. Il faut deux `math.sin`.

### Défi
<!-- ws:doit -->

Ajoute une deuxième vague qui dépend de z. Ton terrain doit onduler **dans les deux sens** : le long de x, et aussi quand tu voles vers le fond.

L'application vérifie encore la douceur du terrain, pas le deuxième sens : c'est toi qui vérifies, en volant.

- vole vers le fond du monde : ça monte et ça descend ;
- vu du ciel, des bosses et des creux partout, comme une boîte d'œufs.

Tu dois obtenir quelque chose comme ça :

![Des collines rondes et régulières, alignées comme une boîte d'œufs.](img/etape7-resultat.png)
<!-- ws:scene {src: scenes/etape7.glb, show_axis: true, camera: {from: [-30, 72, -30], to: [64, 12, 64]}} -->

<!-- ws: {type: hint} -->
<details><summary>Indice 1</summary>

Ta ligne `h` a déjà une vague qui dépend de x. Ajoute `+ 4 * math.sin(z / 11)` juste après.

</details>

<!-- ws: {type: hint} -->
<details><summary>Indice 2</summary>

Si le terrain fait des marches trop hautes, baisse les deux `4`, ou augmente les deux largeurs.

</details>

### Bonus

Multiplie les deux vagues au lieu de les additionner. Que se passe-t-il ?

## Étape 8 : Le vrai relief
<!-- ws: {type: exercise, id: relief, points: 250, token_id: "5"} -->

Vole tout en haut et regarde : tes collines sont alignées comme une boîte d'œufs. La nature ne se répète pas comme ça.

En 1983, pour les effets spéciaux du film *Tron*, Ken Perlin invente un **bruit** qui ressemble au hasard tout en restant doux. Il reçoit un Oscar pour ça. Minecraft s'en sert pour dessiner tous ses terrains.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **`perlin2d(x, z)` « un hasard tout doux »**
> `perlin2d` renvoie un nombre entre -1 et 1. Si x et z bougent *un peu*, le résultat bouge *un peu* : c'est ce qui rend les collines douces.
>
> ```lua
> print(perlin2d(10.5, 3.2))
> print(perlin2d(10.6, 3.2))
> print(perlin2d(50.1, 80.7))
> ```
>
> ![Le bruit de Perlin : à chaque nombre entier il vaut 0, d'où le terrain plat ; ÷ 40 donne des collines larges, ÷ 10 des collines serrées, × 12 les rend douze fois plus hautes mais autour de 0, et + 24 les pose à la bonne hauteur.](img/etape8-perlin.webp)
> <!-- ws:anim {src: img/etape8-perlin.webm, chapters: img/etape8-perlin.vtt} -->

> 🧰 **L'échelle**
> Le `/ 40` règle la **largeur** des collines, le `* 12` leur **hauteur**.
>
> ```lua
> local h = 24 + math.floor(perlin2d(x / 40, z / 40) * 12)
> ```

> 🧰 **Les octaves**
> Un seul bruit donne des collines lisses. On en **additionne** plusieurs : un grand pour les montagnes, un moyen pour les bosses, un petit pour les détails. Chaque couche s'appelle une **octave**.
>
> ```lua
> local n = perlin2d(x / 60, z / 60) * 24
>         + perlin2d(x / 24, z / 24) * 6
>         + perlin2d(x / 8, z / 8) * 1.5
> local h = math.floor(26 + n)
> ```
>
> ![Un grand bruit, un moyen, un petit, et leur somme.](img/outil-octaves.webp)
> <!-- ws:anim {src: img/outil-octaves.webm, chapters: img/outil-octaves.vtt} -->

> 🧰 **La seed**
> La **seed** (la graine, en haut du monde) choisit un bruit parmi des milliards. Même code et même seed : exactement le même monde. Change-la pour en découvrir un autre.
<!-- /ws:toolbox -->

### Pièges

- `perlin2d` avec des nombres **entiers** renvoie toujours 0 : `perlin2d(3, 7)` vaut 0. Divise toujours x et z.
- Plus tu divises x et z, plus les collines sont **larges**. Plus tu multiplies le résultat, plus elles sont **hautes**.

### Défi
<!-- ws:doit -->

Remplace `math.sin` par `perlin2d` : un relief naturel d'au moins **15 blocs de dénivelé** entre le point le plus bas et le plus haut, sans falaise de plus de 3 blocs. Les couches restent obligatoires.

Ce que tu dois avoir pour valider cette étape :
- Un relief naturel fait avec perlin2d

Tu dois obtenir quelque chose comme ça :

![Avec bruit, les collines n'ont plus rien de régulier : des vallées, des sommets, des pentes douces.](img/etape8-resultat.png)
<!-- ws:scene {src: scenes/etape8.glb, show_axis: true, features: [orbit, zoom, pan, reset, cut], cut: {axis: x}, camera: {from: [-30, 72, -30], to: [64, 12, 64]}} -->

<!-- ws: {type: hint} -->
<details><summary>Indice 1</summary>

Écris une fonction `hauteur(x, z)` qui renvoie (`return`) la hauteur de la colonne.

</details>

<!-- ws: {type: hint} -->
<details><summary>Indice 2</summary>

Si ton terrain est plat, affiche `perlin2d(x, z)` : as-tu oublié de diviser ?

</details>

<!-- ws: {type: hint} -->
<details><summary>Indice 3</summary>

Pas assez de dénivelé ? Multiplie davantage le grand bruit.

</details>

### Bonus

Mets `math.abs(perlin2d(...))` pour le grand bruit : tu obtiens des crêtes de montagne.

## Étape 9 : Mers, plages et neige
<!-- ws: {type: exercise, id: mers-plages-neige, points: 250, token_id: "6"} -->

Tu as de jolies collines en relief, mais avec de l'herbe partout en surface. Il manque la **mer**, des **plages** et des **sommets enneigés**.

Le bloc du dessus ne sera plus toujours le même : il va dépendre de l'altitude.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **`if` « faire un choix »**
> `if` exécute du code seulement si une condition est vraie. `elseif` teste une autre condition, `else` s'occupe de tous les autres cas.
>
> ```lua
> local h = 30
> if h < 20 then
>   print("bas")
> elseif h > 35 then
>   print("haut")
> else
>   print("au milieu")
> end
> ```
>
> ![Pour h = 30, 12 puis 40 : la première condition vraie l'emporte.](img/outil-if.webp)
> <!-- ws:anim {src: img/outil-if.webm, chapters: img/outil-if.vtt} -->

> 🧰 **Choisir le bloc du dessus**
> On range le type de bloc dans une variable, et on la change si besoin avant de poser.
>
> ```lua
> local dessus = HERBE
> if h >= 34 then
>   dessus = NEIGE
> end
> set_block(x, h, z, dessus)
> ```
>
> ![Au-dessus de 34, le dessus devient NEIGE.](img/outil-dessus.webp)
> <!-- ws:anim {src: img/outil-dessus.webm, chapters: img/outil-dessus.vtt} -->

> 🧰 **Remplir d'eau**
> De l'eau de `h + 1` jusqu'au niveau de la mer. Si le sol est plus haut que la mer, la boucle ne fait **aucun tour** : pas d'eau. Pratique !
>
> ```lua
> NIVEAU_MER = 22
> for y = h + 1, NIVEAU_MER do
>   set_block(x, y, z, EAU)
> end
> ```
>
> ![De h + 1 jusqu'à NIVEAU_MER : sous la mer la boucle remplit, au-dessus elle ne fait aucun tour.](img/outil-eau.webp)
> <!-- ws:anim {src: img/outil-eau.webm, chapters: img/outil-eau.vtt} -->

> 🧰 **Les comparaisons**
> `<` plus petit, `>` plus grand, `<=` et `>=` « ou égal », `==` égal, `~=` différent.
<!-- /ws:toolbox -->

### Pièges

- `=` range une valeur, `==` compare. On écrit `if h == 20 then`.
- L'eau se pose **au-dessus** du sol, jamais à sa place.
- Si `NIVEAU_MER` est plus bas que tout ton terrain, il n'y aura pas de mer du tout.

### Défi
<!-- ws:doit -->

Ajoute une **mer** à hauteur fixe, du `SABLE` partout où la terre touche l'eau, et de la `NEIGE` au sommet des montagnes.

Ce que tu dois avoir pour valider cette étape :
- Une mer, des plages et de la neige

Tu dois obtenir quelque chose comme ça :

![Une mer à hauteur fixe, du sable là où la terre touche l'eau, et de la neige sur les sommets.](img/etape9-resultat.png)
<!-- ws:scene {src: scenes/etape9.glb, show_axis: true, features: [orbit, zoom, pan, reset, cut], cut: {axis: z}, camera: {from: [-30, 72, -30], to: [64, 12, 64]}} -->

<!-- ws: {type: hint} -->
<details><summary>Indice 1</summary>

Choisis `NIVEAU_MER` pour qu'une partie de ton terrain soit dessous. Affiche quelques hauteurs pour t'aider.

</details>

<!-- ws: {type: hint} -->
<details><summary>Indice 2</summary>

Une plage, c'est une colonne à peine plus haute que la mer : `h <= NIVEAU_MER + 1`.

</details>

<!-- ws: {type: hint} -->
<details><summary>Indice 3</summary>

Sous l'eau, mets aussi du sable à la place de l'herbe et de la terre.

</details>

### Bonus

Pose de la `GLACE` à la surface de l'eau quand la mer est entourée de neige.

## Étape 10 : Forêts, grottes et minerais
<!-- ws: {type: exercise, id: forets-grottes-minerais, points: 350, token_id: "7"} -->

Ton monde a des mers, des plages et des montagnes. Il est prêt à accueillir la vie… et les mineurs.

Il manque des **arbres** en surface et, sous tes pieds, des **grottes** remplies de **trésors**. Dernière ligne droite avant un générateur complet !

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **`random(a, b)` « lancer un dé »**
> `random(1, 6)` donne un nombre entier entre 1 et 6, comme un dé. Il dépend de la seed : même seed, mêmes tirages, donc même monde.
>
> ```lua
> print(random(1, 6), random(1, 6), random(0, TAILLE - 1))
> ```

> 🧰 **`get_block` et `while` « trouver le sol »**
> `get_block(x, y, z)` dit quel bloc se trouve à un endroit. `while` répète *tant que* la condition est vraie : on descend depuis le ciel jusqu'au premier bloc.
>
> ```lua
> local x, z = 64, 64
> local y = HAUTEUR - 1
> while y > 0 and get_block(x, y, z) == AIR do
>   y = y - 1
> end
> print("le sol est à y =", y)
> ```
>
> ![y descend du ciel tant que la case est de l'air, et s'arrête sur l'herbe.](img/outil-sol.webp)
> <!-- ws:anim {src: img/outil-sol.webm, chapters: img/outil-sol.vtt} -->

> 🧰 **Une fonction arbre**
> Un tronc de 5 blocs, puis des feuilles autour du haut. À toi de compléter la couronne.
>
> ```lua
> function arbre(x, y, z)
>   for i = 0, 4 do
>     set_block(x, y + i, z, BOIS)
>   end
>   set_block(x, y + 5, z, FEUILLES)
> end
> ```
>
> ![Un tronc de cinq blocs, une feuille au sommet, puis une couronne.](img/outil-arbre.webp)
> <!-- ws:anim {src: img/outil-arbre.webm, chapters: img/outil-arbre.vtt} -->

> 🧰 **`perlin3d` « creuser des grottes »**
> Même idée que `perlin2d`, mais en 3D. Là où il dépasse un seuil, on **ne pose pas** de pierre : ça fait un trou. Plus le seuil est bas, plus les grottes sont grandes.
>
> ```lua
> if perlin3d(x / 16, y / 10, z / 16) > 0.3 then
>   -- grotte : on ne pose rien
> else
>   set_block(x, y, z, PIERRE)
> end
> ```
>
> ![Un nombre par case ; au-dessus du seuil, on ne pose rien, et baisser le seuil agrandit les grottes.](img/outil-grottes.webp)
> <!-- ws:anim {src: img/outil-grottes.webm, chapters: img/outil-grottes.vtt} -->

> 🧰 **`return` « une fonction qui répond »**
> Une fonction peut **renvoyer** une valeur. Ici, elle choisit quel bloc poser.
>
> ```lua
> function pierre(y)
>   if y < 12 and random(1, 200) == 1 then
>     return DIAMANT
>   end
>   return PIERRE
> end
>
> print(pierre(5))
> ```
<!-- /ws:toolbox -->

### Pièges

- Une boucle `while` dont la condition reste toujours vraie ne s'arrête jamais : ton code est coupé au bout de 5 secondes.
- Si une grotte touche la surface, elle fait un trou dans le sol, et l'eau se retrouve à flotter au-dessus.
- Les arbres poussent sur l'herbe : pas dans l'eau, ni sur le sable, ni dans le vide.

### Défi
<!-- ws:doit -->

Trois défis : au moins **10 arbres** plantés sur l'herbe, des **grottes** creusées avec `perlin3d`, et des **minerais** : du `CHARBON`, et du `DIAMANT` seulement tout au fond (y < 12).

Ce que tu dois avoir pour valider cette étape :
- Au moins 10 arbres
- Des grottes creusées avec perlin3d
- Charbon, et diamants tout au fond

Tu dois obtenir quelque chose comme ça :

![Des arbres partout où il y a de l'herbe, et aucun dans l'eau ni sur le sable.](img/etape10-resultat.png)
<!-- ws:scene {src: scenes/etape10.glb, show_axis: true, features: [orbit, zoom, pan, reset, cut], cut: {axis: x}, camera: {from: [-18, 58, -18], to: [50, 20, 50]}} -->

Et sous tes pieds :

![Dans une grotte, tout au fond : le charbon en points noirs, les diamants en bleu, et la bedrock sous tes pieds.](img/etape10-grotte.png)

<!-- ws: {type: hint} -->
<details><summary>Indice 1</summary>

Pour planter un arbre : tire x et z au hasard, cherche le sol avec `while`, et plante seulement si `get_block(x, y, z) == HERBE`.

</details>

<!-- ws: {type: hint} -->
<details><summary>Indice 2</summary>

Plante les arbres **après** la double boucle du terrain, sinon il n'y a pas encore de sol.

</details>

<!-- ws: {type: hint} -->
<details><summary>Indice 3</summary>

Pour les grottes, ne creuse pas trop près de la surface : par exemple seulement si `y < h - 5`.

</details>

<!-- ws: {type: hint} -->
<details><summary>Indice 4</summary>

Pour les minerais, remplace `PIERRE` par l'appel d'une fonction qui renvoie parfois un minerai.

</details>

### Bonus

**Défi libre** : invente des biomes. Un deuxième bruit très large peut décider d'une zone de désert (sable, pas d'arbres) ou d'une forêt dense. Puis partage ta seed préférée !

## Et maintenant

Tu es parti d'un bloc. Ton code dessine maintenant un monde entier, avec ses montagnes, ses mers, ses forêts et ses grottes, et il tient en quelques dizaines de lignes. C'est exactement comme ça que Minecraft fabrique les siens.

Change la seed, promène-toi, et garde ton code : la prochaine idée est la tienne.
