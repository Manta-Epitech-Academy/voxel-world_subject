# Étape 4 — Les collines

*Durée : 25 min*

## Histoire

Ton monde est aussi plat qu'une table de billard. Il est temps de le **froisser**.

Pour ça, chaque colonne doit avoir *sa propre* hauteur.

## Boîte à outils

### Écrire sa propre fonction

Tu peux ranger du code sous un nom, puis le réutiliser. `x`, `z` et `h` sont les **paramètres** : des variables qui reçoivent les valeurs données à l'appel.

```lua
function colonne(x, z, h)
  bloc(x, 0, z, SOCLE)
  -- ... les couches, avec h au lieu de SOL
  bloc(x, h, z, HERBE)
end

colonne(10, 10, 20)
colonne(11, 10, 25)
```

### math.sin, la vague

`math.sin(t)` monte et descend entre -1 et 1, comme une vague.

Le `5` règle la **hauteur** de la vague, le `/ 8` sa **largeur**.

```lua
for x = 0, TAILLE - 1 do
  local h = 20 + math.floor(5 * math.sin(x / 8))
  bloc(x, h, 0, HERBE)
end
```

### math.floor, arrondir vers le bas

Les blocs sont à des hauteurs entières : `math.floor(4.7)` vaut `4`.

```lua
afficher(math.floor(4.7), math.floor(20 + 3 * math.sin(1)))
```

### Deux vagues qui se croisent

Une vague le long de x **plus** une vague le long de z : des collines dans les deux directions.

```lua
local h = 20 + math.floor(4 * math.sin(x / 8) + 4 * math.sin(z / 11))
```

## Pièges

- `math.sin(x)` tout seul ondule beaucoup trop vite : une vague tous les 6 blocs. Divise x pour élargir.
- Une fonction doit être écrite **avant** la ligne qui l'appelle.
- Avec une vague trop haute, `h` peut dépasser 63 (le ciel) ou descendre sous 5 (plus de place pour les couches).

## Défi

Fais onduler ton terrain avec `math.sin` : au moins **8 hauteurs différentes**, et jamais une marche de plus de **2 blocs** entre deux colonnes voisines. Les couches de l'étape 3 restent obligatoires.

Vérifié automatiquement au clic sur « ▶ Générer » :

- Des collines douces avec les bonnes couches

## Indices

1. Transforme le contenu de tes boucles en une fonction `colonne(x, z, h)`, où `SOL` devient `h`.
2. Dans la double boucle, calcule `h` pour chaque colonne, puis appelle `colonne(x, z, h)`.
3. Si la vérification parle d'une marche trop haute, **divise** x et z par un plus grand nombre.

## Bonus

Multiplie les deux vagues au lieu de les additionner. Que se passe-t-il ?
