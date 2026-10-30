# Étape 6 — Mers, plages et neige

*Durée : 25 min*

## Histoire

Tes collines sont belles, mais tout est vert. Il manque la **mer**, des **plages** là où elle touche la terre, et des **sommets enneigés**.

Le bloc du dessus ne sera plus toujours le même : il va dépendre de l'altitude.

## Boîte à outils

### if : faire un choix

`if` exécute du code seulement si une condition est vraie. `elseif` teste une autre condition, `else` s'occupe de tous les autres cas.

```lua
local h = 30
if h < 20 then
  afficher("bas")
elseif h > 35 then
  afficher("haut")
else
  afficher("au milieu")
end
```

### Choisir le bloc du dessus

On range le type de bloc dans une variable, et on la change si besoin avant de poser.

```lua
local dessus = HERBE
if h >= 34 then
  dessus = NEIGE
end
bloc(x, h, z, dessus)
```

### Remplir d'eau

De l'eau de `h + 1` jusqu'au niveau de la mer. Si le sol est plus haut que la mer, la boucle ne fait **aucun tour** : pas d'eau. Pratique !

```lua
NIVEAU_MER = 22
for y = h + 1, NIVEAU_MER do
  bloc(x, y, z, EAU)
end
```

### Les comparaisons

`<` plus petit, `>` plus grand, `<=` et `>=` « ou égal », `==` égal, `~=` différent.

## Pièges

- `=` range une valeur, `==` compare. On écrit `if h == 20 then`.
- L'eau se pose **au-dessus** du sol, jamais à sa place.
- Si `NIVEAU_MER` est plus bas que tout ton terrain, il n'y aura pas de mer du tout.

## Défi

Ajoute une **mer** à hauteur fixe, du `SABLE` partout où la terre touche l'eau, et de la `NEIGE` au sommet des montagnes.

Vérifié automatiquement au clic sur « ▶ Générer » :

- Une mer, des plages et de la neige

## Indices

1. Choisis `NIVEAU_MER` pour qu'une partie de ton terrain soit dessous. Affiche quelques hauteurs pour t'aider.
2. Une plage, c'est une colonne à peine plus haute que la mer : `h <= NIVEAU_MER + 1`.
3. Sous l'eau, mets aussi du sable à la place de l'herbe et de la terre.

## Bonus

Pose de la `GLACE` à la surface de l'eau quand la mer est entourée de neige.
