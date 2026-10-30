# Étape 7 — Forêts, grottes et minerais

*Durée : 35 min*

## Histoire

Ton monde a des mers, des plages et des montagnes. Il est prêt à accueillir la vie… et les mineurs.

Il manque des **arbres** en surface et, sous tes pieds, des **grottes** remplies de **trésors**. Dernière ligne droite avant un générateur complet !

## Boîte à outils

### hasard(a, b)

`hasard(1, 6)` donne un nombre entier entre 1 et 6, comme un dé. Il dépend de la graine : même graine, mêmes tirages, donc même monde.

```lua
afficher(hasard(1, 6), hasard(1, 6), hasard(0, TAILLE - 1))
```

### lire et while : trouver le sol

`lire(x, y, z)` dit quel bloc se trouve à un endroit. `while` répète *tant que* la condition est vraie : on descend depuis le ciel jusqu'au premier bloc.

```lua
local x, z = 64, 64
local y = HAUTEUR - 1
while y > 0 and lire(x, y, z) == AIR do
  y = y - 1
end
afficher("le sol est à y =", y)
```

### Une fonction arbre

Un tronc de 5 blocs, puis des feuilles autour du haut. À toi de compléter la couronne.

```lua
function arbre(x, y, z)
  for i = 0, 4 do
    bloc(x, y + i, z, BOIS)
  end
  bloc(x, y + 5, z, FEUILLES)
end
```

### bruit3d : creuser des grottes

Même idée que `bruit`, mais en 3D. Là où il dépasse un seuil, on **ne pose pas** de pierre : ça fait un trou. Plus le seuil est bas, plus les grottes sont grandes.

```lua
if bruit3d(x / 16, y / 10, z / 16) > 0.3 then
  -- grotte : on ne pose rien
else
  bloc(x, y, z, PIERRE)
end
```

### return : une fonction qui répond

Une fonction peut **renvoyer** une valeur. Ici, elle choisit quel bloc poser.

```lua
function pierre(y)
  if y < 12 and hasard(1, 200) == 1 then
    return DIAMANT
  end
  return PIERRE
end

afficher(pierre(5))
```

## Pièges

- Une boucle `while` dont la condition reste toujours vraie ne s'arrête jamais : ton code est coupé au bout de 5 secondes.
- Si une grotte touche la surface, elle fait un trou dans le sol, et l'eau se retrouve à flotter au-dessus.
- Les arbres poussent sur l'herbe : pas dans l'eau, ni sur le sable, ni dans le vide.

## Défi

Trois défis : au moins **10 arbres** plantés sur l'herbe, des **grottes** creusées avec `bruit3d`, et des **minerais** : du `CHARBON`, et du `DIAMANT` seulement tout au fond (y < 12).

Vérifié automatiquement au clic sur « ▶ Générer » :

- Au moins 10 arbres
- Des grottes creusées avec bruit3d
- Charbon, et diamants tout au fond

## Indices

1. Pour planter un arbre : tire x et z au hasard, cherche le sol avec `while`, et plante seulement si `lire(x, y, z) == HERBE`.
2. Plante les arbres **après** la double boucle du terrain, sinon il n'y a pas encore de sol.
3. Pour les grottes, ne creuse pas trop près de la surface : par exemple seulement si `y < h - 5`.
4. Pour les minerais, remplace `PIERRE` par l'appel d'une fonction qui renvoie parfois un minerai.

## Bonus

**Défi libre** : invente des biomes. Un deuxième bruit très large peut décider d'une zone de désert (sable, pas d'arbres) ou d'une forêt dense. Puis partage ta graine préférée !
