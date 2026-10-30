# Étape 1 — Premier bloc

*Durée : 15 min*

## Histoire

Le serveur a planté. Quand tu te reconnectes, il ne reste **rien** : un ciel bleu, une grille au sol et trois flèches de couleur. Un message s'affiche : *« Monde introuvable. Mode architecte activé. »*

Ici, pas de pioche. Les blocs apparaissent quand tu **écris du code**.

## Boîte à outils

### Appeler une fonction

Une **fonction** est une action toute prête. On l'appelle en écrivant son nom, puis ses **paramètres** entre parenthèses, séparés par des virgules.

`bloc` pose un bloc. Ses quatre paramètres : x, y, z, puis le type de bloc.

```lua
bloc(64, 10, 64, PIERRE)
```

### Les coordonnées x, y, z

Regarde les flèches dans le monde : **x** et **z** avancent sur le sol, **y** monte vers le ciel.

Le monde va de `0` à `127` en x et en z, et de `0` à `63` en hauteur. Le coin des flèches, c'est (0, 0, 0).

```lua
bloc(0, 0, 0, HERBE)  -- dans le coin, au sol
bloc(0, 5, 0, HERBE)  -- 5 blocs plus haut
```

### Voler et marcher dans le monde

**Clique** sur le monde pour prendre le contrôle, puis :

- <kbd>Z</kbd> <kbd>Q</kbd> <kbd>S</kbd> <kbd>D</kbd> pour avancer et te décaler
- la **souris** pour regarder autour
- <kbd>Espace</kbd> pour monter, <kbd>Maj</kbd> pour descendre, <kbd>R</kbd> pour aller vite
- <kbd>F</kbd>, ou deux fois <kbd>Espace</kbd>, pour **atterrir et marcher** comme dans Minecraft (Espace saute), puis pour reprendre ton envol
- <kbd>Échap</kbd> pour rendre la souris et revenir au code

### Les types de bloc

Le type de bloc s'écrit en **MAJUSCULES** : `PIERRE`, `TERRE`, `HERBE`, `SABLE`, `EAU`, `BOIS`, `FEUILLES`, `NEIGE`, `GLACE`, `GRAVIER`, `CHARBON`, `FER`, `DIAMANT`, `SOCLE`, et `AIR` pour effacer.

```lua
bloc(64, 11, 64, DIAMANT)
```

## Pièges

- `PIERRE` s'écrit en majuscules et **sans guillemets**. `"pierre"` ne marche pas.
- Le monde ne change que quand tu cliques sur **▶ Générer** (ou <kbd>Ctrl</kbd> + <kbd>Entrée</kbd>).
- Tout ce qui suit `--` sur une ligne est un **commentaire** : Lua l'ignore. C'est pour les humains.

## Défi

Pose un bloc de `PIERRE` au centre du monde, à 10 blocs de hauteur : en (64, 10, 64).

Vérifié automatiquement au clic sur « ▶ Générer » :

- Un bloc de pierre en (64, 10, 64)

## Indices

1. Les trois nombres sont toujours dans l'ordre x, y, z. La hauteur est le **deuxième**.
2. Une seule ligne suffit : `bloc(64, 10, 64, PIERRE)`

## Bonus

Construis une petite tour de 5 blocs de haut, puis pose un `DIAMANT` au sommet.
