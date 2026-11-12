# Étape 8, « Les octaves » : un grand bruit pour les montagnes, un moyen pour
# les bosses, un petit pour les détails, et leur somme.
#
#   capture.py anim anim/octaves.py LesOctaves -o img/outil-octaves.webp
import math
from manim import *
from commun import *
from perlin import perlin2d


class LesOctaves(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 128, 32], y_range=[-30, 30, 10], x_length=11, y_length=4.4,
                    axis_config={"color": DOUX, "include_tip": False}, tips=False).shift(DOWN * 0.5)
        grads = VGroup(*[Text(str(v), font="DejaVu Sans", font_size=18, color=DOUX).next_to(axes.c2p(v, -30), DOWN, buff=0.15) for v in range(0, 129, 32)],
                       *[Text(str(v), font="DejaVu Sans", font_size=18, color=DOUX).next_to(axes.c2p(0, v), LEFT, buff=0.15) for v in (-20, 0, 20)],
                       Text("x", font="DejaVu Sans", font_size=24, color=DOUX).next_to(axes.x_axis, RIGHT, buff=0.2))
        self.play(Create(axes), FadeIn(grads), run_time=0.8)

        def courbe(f, couleur, epaisseur=4):
            return axes.plot(f, x_range=[0, 127, 0.5], color=couleur, stroke_width=epaisseur)

        self.next_section("un grand bruit : les montagnes")
        f1 = formule("perlin2d(x / 60, z / 60) * 24", 26)
        c1 = courbe(lambda x: perlin2d(x / 60, 7) * 24, CIEL)
        self.play(Write(f1), Create(c1), run_time=1.4)
        ph = phrase("÷ 60, × 24 : un grand bruit, large et haut, les montagnes", CIEL)
        self.play(FadeIn(ph)); self.wait(1.3)

        self.next_section("un moyen : les bosses")
        f2 = formule("+ perlin2d(x / 24, z / 24) * 6", 26)
        c2 = courbe(lambda x: perlin2d(x / 24, 7) * 6, ALERTE, 3)
        self.play(Transform(f1, f2), Create(c2), FadeOut(ph), run_time=1.2)
        ph = phrase("÷ 24, × 6 : un bruit moyen, les bosses", ALERTE)
        self.play(FadeIn(ph)); self.wait(1.2)

        self.next_section("un petit : les détails")
        f3 = formule("+ perlin2d(x / 8, z / 8) * 1.5", 26)
        c3 = courbe(lambda x: perlin2d(x / 8, 7) * 1.5, COULEURS["HERBE"], 2)
        self.play(Transform(f1, f3), Create(c3), FadeOut(ph), run_time=1.2)
        ph = phrase("÷ 8, × 1.5 : un petit bruit, les détails", COULEURS["HERBE"])
        self.play(FadeIn(ph)); self.wait(1.2)

        self.next_section("on les additionne")
        f4 = formule("n = grand + moyen + petit", 26)
        somme = courbe(lambda x: perlin2d(x / 60, 7) * 24 + perlin2d(x / 24, 7) * 6 + perlin2d(x / 8, 7) * 1.5, WHITE, 5)
        self.play(Transform(f1, f4), FadeOut(ph), c1.animate.set_stroke(opacity=0.3), c2.animate.set_stroke(opacity=0.3), c3.animate.set_stroke(opacity=0.3), run_time=0.8)
        self.play(Create(somme), run_time=1.6)
        self.play(FadeIn(phrase("additionnés : des montagnes avec des bosses et des détails, comme la nature", WHITE)))
        self.wait(2.0)
