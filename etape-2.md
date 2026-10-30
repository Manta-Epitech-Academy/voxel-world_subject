# Étape 2 — Le sol plat

*Durée : 20 min*

## Histoire

Un bloc flotte, tout seul dans le vide. Pour un monde entier, il en faudrait **16 384** rien que pour le sol. À la main, tu y serais encore à Noël.

Heureusement, un ordinateur adore répéter.

## Boîte à outils

### La boucle for

Une **boucle** répète le code écrit entre `do` et `end`. Ici, `x` vaut 0, puis 1, puis 2… jusqu'à 9 : une ligne de 10 blocs.

```lua
for x = 0, 9 do
  bloc(x, 0, 0, PIERRE)
end
```

### Une boucle dans une boucle

Pour chaque valeur de `x`, la boucle intérieure fait tous les `z`. 10 × 10 = un carré de 100 blocs.

```lua
for x = 0, 9 do
  for z = 0, 9 do
    bloc(x, 0, z, PIERRE)
  end
end
```

### TAILLE

`TAILLE` vaut 128, la largeur du monde. Les colonnes vont de `0` à `TAILLE - 1`, c'est-à-dire 127.

```lua
afficher(TAILLE)
afficher(TAILLE - 1)
```

### afficher

`afficher` écrit dans la console, sous l'éditeur. C'est ta loupe : quand ton code ne fait pas ce que tu crois, affiche tes variables.

```lua
for x = 0, 3 do
  afficher("x vaut", x)
end
```

## Pièges

- `for x = 0, TAILLE do` fait **129** tours, pas 128 : le dernier bloc tombe hors du monde. La console te le signale.
- Chaque `for` a son `end`. Décale le code à l'intérieur vers la droite pour voir qui ferme quoi.

## Défi

Recouvre tout le sol du monde (y = 0) d'`HERBE` : les 128 × 128 colonnes.

Vérifié automatiquement au clic sur « ▶ Générer » :

- Les 16 384 colonnes ont un bloc à y = 0

## Indices

1. Commence par une seule ligne de 128 blocs le long de x. Vole pour vérifier qu'elle touche les deux bords.
2. Mets ensuite cette boucle **à l'intérieur** d'une autre boucle, sur z.
3. ```lua
for x = 0, TAILLE - 1 do
for z = 0, TAILLE - 1 do
...
end
end
```

## Bonus

Fais un damier : `HERBE` et `SABLE` en alternance. Indice : `(x + z) % 2` vaut 0 ou 1.
