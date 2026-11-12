# Ce que les animations partagent : les couleurs de l'application, une formule
# écrite comme le code, une phrase sous la figure, et une vue de côté du monde
# où les blocs sont des carrés.
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
    return Text(texte, font="DejaVu Sans", font_size=taille, color=couleur).to_edge(DOWN, buff=0.45)


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
