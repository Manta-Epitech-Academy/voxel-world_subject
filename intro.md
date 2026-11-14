# World Generator

Minecraft ne dessine pas ses mondes à la main : il les **calcule**. Quelques formules décident où se dressent les montagnes, où s'arrête la mer, où poussent les arbres et où se cachent les diamants.

Tu vas écrire ce générateur toi-même, en **Lua**. Tu commences par poser un seul bloc. Ton code dessine des collines, des mers bordées de plages, des sommets enneigés, des forêts, des grottes et des minerais. Et tu peux te promener dedans.

Rien à installer : tout se passe dans ton navigateur, à côté de ces instructions.

## Le glossaire

Tout ce que World Generator met entre tes mains est rassemblé ici. Tu y reviens quand tu as oublié un nom.

<!-- ws:glossary -->
## Ce que World Generator te donne

Ces noms viennent de World Generator, pas de Lua. Ils existent déjà quand ton code démarre.

| Terme | Signification |
| --- | --- |
| `set_block(x, y, z, BLOC)` | Pose un bloc du type `BLOC` à la position (<var>x</var>, <var>y</var>, <var>z</var>). Un nombre à virgule est arrondi vers le bas ; un bloc hors du monde est ignoré, et la console te prévient |
| `get_block(x, y, z)` | Le type du bloc qui se trouve en (<var>x</var>, <var>y</var>, <var>z</var>). `AIR` s'il n'y a rien, ou si c'est hors du monde |
| `perlin2d(x, z)` | Un nombre entre -1 et 1 qui varie doucement : si <var>x</var> ou <var>z</var> change un peu, le résultat change un peu. Même seed, même résultat |
| `perlin3d(x, y, z)` | Le même, en trois dimensions. C'est lui qui creuse les grottes |
| `random(a, b)` | Un nombre entier entre a et b, comme un dé. `random(a)` tire entre 1 et a, `random()` un nombre à virgule entre 0 et 1. Dépend de la seed |
| `print(...)` | Écrit dans la console, sous l'éditeur. Plusieurs valeurs séparées par des virgules s'affichent sur la même ligne |
| `TAILLE` | La largeur du monde : 128. <var>x</var> et <var>z</var> vont de 0 à `TAILLE - 1` |
| `HAUTEUR` | La hauteur du monde : 64. <var>y</var> va de 0 à `HAUTEUR - 1` |
| `SEED` | Le nombre qui règle le hasard de `perlin2d`, `perlin3d` et `random`. Le bouton dé en tire un autre ; même seed, même monde |
| `AIR` | Rien du tout. Poser `AIR` efface un bloc |
| `BEDROCK` `PIERRE` `TERRE` `HERBE` `SABLE` `GRAVIER` `EAU` `GLACE` `NEIGE` | Les blocs du paysage |
| `BOIS` `FEUILLES` | De quoi faire un arbre |
| `CHARBON` `FER` `DIAMANT` | Les minerais |
<!-- /ws:glossary -->
