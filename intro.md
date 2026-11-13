# World Generator

Minecraft ne range pas ses mondes bloc par bloc : il les **calcule**. Quelques formules décident où se dressent les montagnes, où s'arrête la mer, où poussent les arbres et où se cachent les diamants.

Dans cet atelier, c'est toi qui écris ce générateur, en **Lua**. Tu commences par poser un seul bloc. Ton code dessine des collines, des mers bordées de plages, des sommets enneigés, des forêts, des grottes et des minerais. Et tu peux te promener dedans.

Rien à installer : tout se passe dans ton navigateur, à côté de ces instructions.

## Le glossaire

Tout ce que World Generator met entre tes mains est rassemblé ici. Tu y reviens quand tu as oublié un nom.

<!-- ws:glossary -->
## Ce que World Generator te donne

Ces noms viennent de World Generator, pas de Lua. Ils existent déjà quand ton code démarre.

| Terme | Signification |
| --- | --- |
| `set_block(x, y, z, BLOC)` | Pose un bloc du type `BLOC` à la position (x, y, z). Un nombre à virgule est arrondi vers le bas ; un bloc hors du monde est ignoré |
| `get_block(x, y, z)` | Le type du bloc qui se trouve en (x, y, z). `AIR` s'il n'y a rien, ou si c'est hors du monde |
| `perlin2d(x, z)` | Un hasard tout doux : un nombre entre -1 et 1, qui change un peu quand x ou z change un peu. Même seed, même résultat |
| `perlin3d(x, y, z)` | Le même, en trois dimensions. C'est lui qui creuse les grottes |
| `random(a, b)` | Un nombre entier entre a et b, comme un dé. `random(a)` tire entre 1 et a, `random()` un nombre à virgule entre 0 et 1. Dépend de la seed |
| `print(...)` | Écrit dans la console, sous l'éditeur. Plusieurs valeurs séparées par des virgules s'affichent sur la même ligne |
| `TAILLE` | La largeur du monde : 128. x et z vont de 0 à `TAILLE - 1` |
| `HAUTEUR` | La hauteur du monde : 64. y va de 0 à `HAUTEUR - 1` |
| `SEED` | Le nombre qui règle le hasard de `perlin2d`, `perlin3d` et `random`. Le bouton dé en tire un autre ; même seed, même monde |
| `AIR` | Rien du tout. Poser `AIR` efface un bloc |
| `BEDROCK` `PIERRE` `TERRE` `HERBE` `SABLE` `GRAVIER` `EAU` `GLACE` `NEIGE` | Les blocs du paysage |
| `BOIS` `FEUILLES` | De quoi faire un arbre |
| `CHARBON` `FER` `DIAMANT` | Les minerais |
<!-- /ws:glossary -->
