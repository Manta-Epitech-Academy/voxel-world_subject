# Étape 5 — Le vrai relief

*Durée : 25 min*

## Histoire

Vole tout en haut et regarde : tes collines sont alignées comme une boîte d'œufs. La nature ne se répète pas comme ça.

En 1983, pour les effets spéciaux du film *Tron*, Ken Perlin invente un **bruit** qui ressemble au hasard tout en restant doux. Il reçoit un Oscar pour ça. Minecraft s'en sert pour dessiner tous ses terrains.

## Boîte à outils

### bruit(x, z)

`bruit` renvoie un nombre entre -1 et 1. Si x et z bougent *un peu*, le résultat bouge *un peu* : c'est ce qui rend les collines douces.

```lua
afficher(bruit(10.5, 3.2))
afficher(bruit(10.6, 3.2))
afficher(bruit(50.1, 80.7))
```

### L'échelle

Le `/ 40` règle la **largeur** des collines, le `* 12` leur **hauteur**.

```lua
local h = 24 + math.floor(bruit(x / 40, z / 40) * 12)
```

### Les octaves

Un seul bruit donne des collines lisses. On en **additionne** plusieurs : un grand pour les montagnes, un moyen pour les bosses, un petit pour les détails. Chaque couche s'appelle une **octave**.

```lua
local n = bruit(x / 60, z / 60) * 24
        + bruit(x / 24, z / 24) * 6
        + bruit(x / 8, z / 8) * 1.5
local h = math.floor(26 + n)
```

### La graine

La **graine** (en haut du monde) choisit un bruit parmi des milliards. Même code et même graine : exactement le même monde. Change-la pour en découvrir un autre.

## Pièges

- `bruit` avec des nombres **entiers** renvoie toujours 0 : `bruit(3, 7)` vaut 0. Divise toujours x et z.
- Plus tu divises x et z, plus les collines sont **larges**. Plus tu multiplies le résultat, plus elles sont **hautes**.

## Défi

Remplace `math.sin` par `bruit` : un relief naturel d'au moins **15 blocs de dénivelé** entre le point le plus bas et le plus haut, sans falaise de plus de 3 blocs. Les couches restent obligatoires.

Vérifié automatiquement au clic sur « ▶ Générer » :

- Un relief naturel fait avec bruit

## Indices

1. Écris une fonction `hauteur(x, z)` qui renvoie (`return`) la hauteur de la colonne.
2. Si ton terrain est plat, affiche `bruit(x, z)` : as-tu oublié de diviser ?
3. Pas assez de dénivelé ? Multiplie davantage le grand bruit.

## Bonus

Mets `math.abs(bruit(...))` pour le grand bruit : tu obtiens des crêtes de montagne.
