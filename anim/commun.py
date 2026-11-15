# Ce que les animations partagent : les couleurs de l'application, une formule
# écrite comme le code, une phrase sous la figure, et une vue de côté du monde
# où les blocs sont des carrés.
import math
from manim import *

FOND = "#14161b"
PANNEAU = "#1b1d23"
CIEL = "#9fd3ff"
ALERTE = "#f2c14e"
ERREUR = "#ff6b6b"
DOUX = "#9aa1ad"
BLANC = "#e6e8ec"
COULEURS = {
    "BEDROCK": "#3c3c3c", "PIERRE": "#7d7d7d", "TERRE": "#86604a", "HERBE": "#5fb946",
    "SABLE": "#dbcfa3", "EAU": "#346edc", "BOIS": "#685232", "FEUILLES": "#3a7828",
    "NEIGE": "#f0f8ff", "DIAMANT": "#5decf5", "CHARBON": "#1e1e1e", "AIR": None,
}

config.background_color = FOND


def code(texte, taille=30, couleur=WHITE):
    """Une ligne de code, en monospace, telle que l'élève la tape."""
    return Text(texte, font="DejaVu Sans Mono", font_size=taille, color=couleur)


def formule(texte, taille=30):
    return code(texte, taille).to_edge(UP, buff=0.45)


def bloc_code(lignes, taille=24, couleur=WHITE):
    """Plusieurs lignes de code, alignées à gauche, l'indentation gardée.

    Un Text par ligne, pour pouvoir en entourer ou en changer une. Un espace
    n'a pas de glyphe, donc le bord gauche d'une ligne est sa première lettre :
    l'indentation est rendue en décalant la ligne d'autant de largeurs de
    caractère (police à chasse fixe)."""
    largeur = code("x", taille).width
    groupe = VGroup(*[code(l.strip() if l.strip() else "·", taille, couleur) for l in lignes])
    groupe.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    gauche = groupe.get_left()[0]
    for ligne, texte in zip(groupe, lignes):
        retrait = len(texte) - len(texte.lstrip(" "))
        ligne.shift(RIGHT * (gauche + retrait * largeur - ligne.get_left()[0]))
        if not texte.strip():
            ligne.set_opacity(0)
    return groupe


def phrase(texte, couleur=CIEL, taille=26):
    t = Text(texte, font="DejaVu Sans", font_size=taille, color=couleur)
    # Une phrase plus large que l'image serait coupée aux deux bords.
    if t.width > config.frame_width - 1:
        t.scale_to_fit_width(config.frame_width - 1)
    return t.to_edge(DOWN, buff=0.45)


class Grille:
    """Une vue de côté (ou de dessus) du monde : `cases` cases de large, `hauteur` de haut,
    posée dans un rectangle de `largeur` × `haut` unités manim, le coin (0, 0) en bas à gauche."""

    def __init__(self, cases=16, hauteur=10, largeur=8.0, haut=4.0, origine=ORIGIN, y0=0):
        self.cases, self.hauteur, self.y0 = cases, hauteur, y0
        self.pas = min(largeur / cases, haut / hauteur)
        self.origine = origine + LEFT * (cases * self.pas / 2) + DOWN * (hauteur * self.pas / 2)

    def coin(self, x, y):
        """Le coin bas-gauche de la case (x, y) ; y est une hauteur du monde, y0 la première montrée."""
        return self.origine + RIGHT * x * self.pas + UP * (y - self.y0) * self.pas

    def centre(self, x, y):
        return self.coin(x + 0.5, y + 0.5)

    def bloc(self, x, y, type_="PIERRE", opacite=0.95):
        r = Square(side_length=self.pas, fill_color=COULEURS[type_], fill_opacity=opacite,
                   stroke_color=FOND, stroke_width=1)
        r.move_to(self.centre(x, y))
        return r

    def cadre(self, couleur=DOUX):
        return Rectangle(width=self.cases * self.pas, height=self.hauteur * self.pas,
                         stroke_color=couleur, stroke_width=1.5).move_to(self.centre(self.cases / 2 - 0.5, self.y0 + self.hauteur / 2 - 0.5))

    def lignes(self, couleur=DOUX, opacite=0.25):
        g = VGroup()
        for i in range(self.cases + 1):
            g.add(Line(self.coin(i, self.y0), self.coin(i, self.y0 + self.hauteur), stroke_color=couleur, stroke_width=1, stroke_opacity=opacite))
        for j in range(self.y0, self.y0 + self.hauteur + 1):
            g.add(Line(self.coin(0, j), self.coin(self.cases, j), stroke_color=couleur, stroke_width=1, stroke_opacity=opacite))
        return g

    def axe_x(self, pas=1, couleur=DOUX):
        g = VGroup()
        for i in range(0, self.cases, pas):
            g.add(Text(str(i), font="DejaVu Sans", font_size=16, color=couleur).next_to(self.coin(i + 0.5, self.y0), DOWN, buff=0.12))
        return g

    def axe_y(self, pas=1, couleur=DOUX, etiquette="y"):
        g = VGroup()
        for j in range(self.y0, self.y0 + self.hauteur, pas):
            g.add(Text(str(j), font="DejaVu Sans", font_size=16, color=couleur).next_to(self.coin(0, j + 0.5), LEFT, buff=0.12))
        g.add(Text(etiquette, font="DejaVu Sans", font_size=20, color=couleur).next_to(self.coin(0, self.y0 + self.hauteur), LEFT, buff=0.15))
        return g


VERT = COULEURS["HERBE"]


def texte(t, taille=24, couleur=BLANC):
    """Des mots, pas du code : la police des phrases."""
    return Text(t, font="DejaVu Sans", font_size=taille, color=couleur)


def roule(cran):
    """Une valeur de compteur qui reste sur son chiffre au début de chaque cran,
    puis roule vers le suivant. `cran` est un nombre à virgule : 2.5, c'est le
    milieu du troisième cran."""
    k = int(cran + 1e-9)
    u = min(1, max(0, (cran - k - 0.6) / 0.4))
    return k + u * u * (3 - 2 * u)


class Compteur(VGroup):
    """Un compteur à rouleaux, comme un compteur kilométrique : un rouleau de
    chiffres de 0 à 9 par chiffre, dans une fenêtre. Quand les unités passent
    de 9 à 0, les dizaines roulent en même temps. Un zéro à gauche reste vide.

    `valeur()` est lue à chaque image ; entre deux entiers, les rouleaux sont
    entre deux chiffres. `nom` au-dessus, `legende` (des lignes) en dessous."""

    HAUT = 1.25
    PAS = 0.78

    def __init__(self, nom, valeur, chiffres=1, couleur=ALERTE, legende=()):
        super().__init__()
        self.valeur, self.n = valeur, chiffres
        large = 0.37 + self.PAS * chiffres
        self.fenetre = RoundedRectangle(width=large, height=self.HAUT, corner_radius=0.12, stroke_color=couleur,
                                        stroke_width=3, fill_color=PANNEAU, fill_opacity=1)
        c = self.fenetre.get_center()
        self.rouleaux = VGroup(*[VGroup(*[Text(str(d), font="DejaVu Sans Mono", font_size=56, color=couleur) for d in range(10)])
                                 for _ in range(chiffres)])
        # Deux caches de la couleur du fond : on ne voit les rouleaux que dans la fenêtre.
        caches = VGroup(*[Rectangle(width=large + 0.4, height=self.HAUT, fill_color=FOND, fill_opacity=1, stroke_width=0)
                          .next_to(self.fenetre, sens, buff=0) for sens in (UP, DOWN)])
        bord = self.fenetre.copy().set_fill(opacity=0)
        traits = VGroup(*[Line(c + RIGHT * x + UP * self.HAUT / 2, c + RIGHT * x + DOWN * self.HAUT / 2, stroke_color=couleur,
                               stroke_width=1.5, stroke_opacity=0.35)
                          for x in [self.PAS * ((chiffres - 1) / 2 - i - 0.5) for i in range(chiffres - 1)]])
        self.nom = texte(nom, 30, couleur).next_to(self.fenetre, UP, buff=0.25)
        self.legende = VGroup(*[texte(l, 20, DOUX) for l in legende]).arrange(DOWN, buff=0.1).next_to(self.fenetre, DOWN, buff=0.25)
        self.add(self.fenetre, self.rouleaux, caches, bord, traits, self.nom, self.legende)
        self.rouleaux.add_updater(self.rouler)
        self.rouler(self.rouleaux)

    def rouler(self, m):
        v = max(0.0, self.valeur())
        echelle = self.fenetre.height / self.HAUT      # le compteur a pu être agrandi
        for i, rouleau in enumerate(m):
            p = 10 ** i
            # Le rouleau i avance d'un chiffre quand tous ceux de droite passent de 9 à 0.
            r = math.floor(v / p) + max(0.0, (v % p) - (p - 1)) if i else v
            place = self.fenetre.get_center() + RIGHT * self.PAS * echelle * ((self.n - 1) / 2 - i)
            vide = i > 0 and v < p          # le zéro à gauche : rien
            for d, chiffre in enumerate(rouleau):
                ecart = (d - r + 5) % 10 - 5            # entre -5 et 5 : 0 au milieu de la fenêtre
                # Hors de la fenêtre, un chiffre reste juste derrière un cache :
                # il ne doit pas élargir la boîte du compteur.
                chiffre.move_to(place + DOWN * max(-1, min(1, ecart)) * self.fenetre.height)
                visible = abs(ecart) < 0.999 and not (vide and d == 0)
                chiffre.set_opacity(1 if visible else 0)


class Reglage(VGroup):
    """Un curseur : un nom, un rail, un bouton, et sa valeur à droite."""

    def __init__(self, nom, mini, maxi, valeur, couleur=CIEL, largeur=2.6):
        super().__init__()
        self.t = ValueTracker(valeur)
        self.rail = Line(LEFT * largeur / 2, RIGHT * largeur / 2, stroke_color=DOUX, stroke_width=4)
        self.nom = texte(nom, 22, couleur).next_to(self.rail, UP, buff=0.22)
        self.bouton = Dot(radius=0.13, color=couleur)
        self.bouton.add_updater(lambda m: m.move_to(self.rail.point_from_proportion((self.t.get_value() - mini) / (maxi - mini))))
        self.bouton.update()
        self.nombre = always_redraw(lambda: code(str(round(self.t.get_value())), 22, couleur).next_to(self.rail, RIGHT, buff=0.2))
        self.add(self.rail, self.nom, self.bouton, self.nombre)

    def placer(self, pos):
        """Pose le curseur pour que le milieu de son rail soit en pos."""
        self.shift(pos - self.rail.get_center())
        return self


def ranger_les_reglages(scene, ligne, reglages):
    """Les curseurs deviennent la ligne de code : les rails s'effacent, puis
    le nom de chaque réglage glisse jusqu'à son mot dans `ligne`, et le reste
    de la ligne apparaît. Placer `ligne` sous la rangée des curseurs : un nom
    qui descend ne passe pas sur les autres.

    `reglages` : des paires (curseur, (début, fin)), la tranche de glyphes de
    son mot dans `ligne` (un Text ne compte pas les espaces)."""
    pris = set()
    for r, (a, b) in reglages:
        scene.remove(r)
        scene.add(r.rail, r.nom, r.bouton, r.nombre)
    scene.play(*[FadeOut(m) for r, _ in reglages for m in (r.rail, r.bouton, r.nombre)], run_time=0.6)
    # Un nom après l'autre. Un fondu qui glisse, pas un morphing : entre deux
    # textes différents, le morphing donne une bouillie de lettres.
    for r, (a, b) in reglages:
        mot = ligne[a:b].set_color(r.nom.get_color())
        pris.update(range(a, b))
        scene.play(FadeTransform(r.nom, mot), run_time=0.9)
    reste = VGroup(*[g for i, g in enumerate(ligne) if i not in pris])
    scene.play(FadeIn(reste), run_time=0.8)
