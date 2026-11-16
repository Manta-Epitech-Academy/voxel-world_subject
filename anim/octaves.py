# Étape 10, « Les octaves » : un grand bruit pour les montagnes, un moyen pour
# les bosses, un petit pour les détails. On les additionne un par un, pour voir
# ce que chacun ajoute. Sans nombres : les largeurs et les amplitudes sont à
# l'élève.
#
#   capture.py anim anim/octaves.py LesOctaves -o img/outil-octaves.webp
import math
from manim import *
from commun import *
from perlin import perlin2d


# Une ligne du monde où les trois bruits remplissent bien le graphique.
Z = 33.5


def grand(x):
    return perlin2d(x / 40, Z) * 32


def moyen(x):
    return perlin2d(x / 14, Z) * 13


def petit(x):
    return perlin2d(x / 5, Z) * 5


class LesOctaves(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 128, 32], y_range=[-30, 30, 10], x_length=11, y_length=4.4,
                    axis_config={"color": DOUX, "include_tip": False}, tips=False).shift(DOWN * 0.5)
        grads = VGroup(*[texte(str(v), 18, DOUX).next_to(axes.c2p(v, -30), DOWN, buff=0.15) for v in range(0, 129, 32)],
                       *[texte(str(v), 18, DOUX).next_to(axes.c2p(0, v), LEFT, buff=0.15) for v in (-20, 0, 20)],
                       texte("x", 24, DOUX).next_to(axes.x_axis, RIGHT, buff=0.2))
        self.play(Create(axes), FadeIn(grads), run_time=0.8)

        def courbe(f, couleur, epaisseur=4):
            return axes.plot(f, x_range=[0, 127, 0.5], color=couleur, stroke_width=epaisseur)

        def titre(t):
            return texte(t, 28, WHITE).to_edge(UP, buff=0.45)

        self.next_section("un grand bruit : les montagnes")
        t = titre("un grand bruit : grande largeur, grande amplitude")
        c1 = courbe(grand, CIEL)
        self.play(FadeIn(t), Create(c1), run_time=1.4)
        ph = phrase("un grand bruit, large et haut : les montagnes", CIEL)
        self.play(FadeIn(ph)); self.wait(1.3)

        self.next_section("un moyen : les bosses")
        c2 = courbe(moyen, ALERTE, 3)
        self.play(FadeOut(t), FadeOut(ph), run_time=0.4)
        t = titre("un moyen : largeur et amplitude moyennes")
        self.play(FadeIn(t), Create(c2), run_time=1.2)
        ph = phrase("un bruit moyen : les bosses", ALERTE)
        self.play(FadeIn(ph)); self.wait(1.2)

        self.next_section("grand + moyen")
        # La somme part du grand bruit, puis prend les bosses du moyen.
        somme = courbe(grand, WHITE, 5)
        self.play(FadeOut(t), FadeOut(ph), FadeIn(somme), run_time=0.5)
        t = titre("grand + moyen")
        self.play(FadeIn(t), c1.animate.set_stroke(opacity=0.35), c2.animate.set_stroke(opacity=0.35),
                  Transform(somme, courbe(lambda x: grand(x) + moyen(x), WHITE, 5)), run_time=1.8)
        ph = phrase("additionnés : les montagnes ont des bosses", WHITE)
        self.play(FadeIn(ph)); self.wait(1.4)

        self.next_section("un petit : les détails")
        c3 = courbe(petit, VERT, 2.5)
        self.play(FadeOut(t), FadeOut(ph), run_time=0.4)
        t = titre("un petit : petite largeur, petite amplitude")
        self.play(FadeIn(t), Create(c3), run_time=1.2)
        ph = phrase("un petit bruit, serré et bas : les détails", VERT)
        self.play(FadeIn(ph)); self.wait(1.2)

        self.next_section("grand + moyen + petit")
        self.play(FadeOut(t), FadeOut(ph), run_time=0.4)
        t = titre("grand + moyen + petit")
        self.play(FadeIn(t), c3.animate.set_stroke(opacity=0.35),
                  Transform(somme, courbe(lambda x: grand(x) + moyen(x) + petit(x), WHITE, 5)), run_time=1.8)
        self.play(FadeIn(phrase("additionnés : des montagnes avec des bosses et des détails, comme la nature", WHITE)))
        self.wait(2.0)
