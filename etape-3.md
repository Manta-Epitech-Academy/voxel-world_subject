# Étape 3 — Les couches

*Durée : 20 min*

## Histoire

Creuse dans Minecraft : sous l'herbe il y a de la terre, puis de la pierre, et tout au fond le **socle** que rien ne peut casser.

Ton monde, lui, n'a qu'une pellicule d'un bloc d'épaisseur. Un coup de pelle et on tombe dans le vide.

## Boîte à outils

### Les variables

Une **variable** est une boîte avec un nom. Change la valeur de `SOL` une seule fois, et tout le code qui l'utilise suit.

```lua
local SOL = 20
bloc(64, SOL, 64, HERBE)
bloc(64, SOL - 1, 64, TERRE)
```

### Une boucle vers le haut

La même boucle `for`, mais sur y : une colonne de pierre de y = 1 à y = 16.

```lua
for y = 1, 16 do
  bloc(64, y, 64, PIERRE)
end
```

### Calculer avec les variables

On peut faire des calculs partout où on attend un nombre : `+`, `-`, `*` (fois), `/` (divisé).

```lua
local SOL = 20
afficher(SOL - 4, SOL - 3, SOL - 1)
```

## Pièges

- Si la pierre va jusqu'à `SOL - 4`, la terre commence à `SOL - 3`. Un chiffre de travers et les couches se chevauchent.
- Si tu poses deux blocs au même endroit, c'est **le dernier** qui gagne.

## Défi

Dans chaque colonne, de bas en haut : `SOCLE` à y = 0, de la `PIERRE`, exactement 3 blocs de `TERRE`, puis l'`HERBE` au sommet.

Vérifié automatiquement au clic sur « ▶ Générer » :

- Socle, pierre, 3 terre, herbe

## Indices

1. Avec `SOL = 20` : socle à 0, pierre de 1 à 16, terre de 17 à 19, herbe à 20.
2. Tu as déjà les deux boucles x et z de l'étape 2. C'est **à l'intérieur** que tu empiles la colonne.
3. Il te faut une boucle sur y pour la pierre, et une autre pour la terre.

## Bonus

Vole sous ton monde (<kbd>Maj</kbd>) et regarde la tranche : on voit les couches sur les bords.
