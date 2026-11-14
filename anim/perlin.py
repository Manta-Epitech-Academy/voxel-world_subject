# Le bruit de Perlin, en trois idées : à chaque nombre entier il vaut 0, donc
# on divise x et z ; plus on divise, plus les collines sont larges ; plus on
# multiplie le résultat, plus elles sont hautes. Même bruit que l'application
# (prélude Lua), permutation tirée de la seed.
#
#   capture.py anim anim/perlin.py LePerlin -o img/etape9-perlin.webp   # + .webm et .vtt
import math
import random
from manim import *

FOND = "#14161b"
HERBE = "#5fb946"
HERBE_SOMBRE = "#2f6a23"
CIEL = "#9fd3ff"
ALERTE = "#f2c14e"
DOUX = "#9aa1ad"
SEED = 1

config.background_color = FOND

# ---- le bruit de Perlin 2D du prélude (lua/prelude.lua), en Python ----
rnd = random.Random(SEED)
p = list(range(256))
for i in range(255, 0, -1):
    j = rnd.randint(0, i)
    p[i], p[j] = p[j], p[i]
p += p


def fondu(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def grad2(h, x, y):
    h %= 8
    return [x + y, -x + y, x - y, -x - y, x, -x, y, -y][h]


def perlin2d(x, z):
    fx, fz = math.floor(x), math.floor(z)
    X, Z = fx % 256, fz % 256
    x, z = x - fx, z - fz
    u, v = fondu(x), fondu(z)
    a, b = p[X] + Z, p[X + 1] + Z
    n00, n01 = grad2(p[a], x, z), grad2(p[a + 1], x, z - 1)
    n10, n11 = grad2(p[b], x - 1, z), grad2(p[b + 1], x - 1, z - 1)
    nx0 = n00 + u * (n10 - n00)
    nx1 = n01 + u * (n11 - n01)
    return nx0 + v * (nx1 - nx0)


class LePerlin(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 128, 16], y_range=[-1.5, 1.5, 0.5],
            x_length=11, y_length=3.6,
            axis_config={"color": DOUX, "include_tip": False},
            tips=False,
        ).shift(DOWN * 0.4)
        grads = VGroup(
            *[Text(str(v), font="DejaVu Sans", font_size=18, color=DOUX).next_to(axes.c2p(v, -1.5), DOWN, buff=0.15)
              for v in range(0, 129, 32)],
            *[Text(str(v), font="DejaVu Sans", font_size=18, color=DOUX).next_to(axes.c2p(0, v), LEFT, buff=0.15)
              for v in (-1, 0, 1)],
        )
        etiq_x = Text("x", font="DejaVu Sans", font_size=26, color=DOUX).next_to(axes.x_axis, RIGHT, buff=0.2)
        zero = axes.plot(lambda x: 0, x_range=[0, 128], color=DOUX, stroke_width=1.5, stroke_opacity=0.6)
        self.play(Create(axes), FadeIn(grads), FadeIn(etiq_x), Create(zero), run_time=1)

        def formule(t):
            return Text(t, font="DejaVu Sans Mono", font_size=32, color=WHITE).to_edge(UP, buff=0.45)

        def note(t, couleur):
            return Text(t, font="DejaVu Sans", font_size=26, color=couleur).next_to(axes, DOWN, buff=0.45)

        def courbe(f, couleur=CIEL):
            return axes.plot(f, x_range=[0, 127, 0.25], color=couleur, stroke_width=4)

        # 0. Le 7 de la formule : z ne bouge pas, on regarde une seule ligne.
        self.next_section("z reste fixe : une seule ligne du monde")
        f = formule("h = perlin2d(x, 7)")
        vrai = courbe(lambda x: perlin2d(x, 7), couleur=CIEL).set_stroke(opacity=0.35)
        points = VGroup(*[Dot(axes.c2p(x, perlin2d(x, 7)), radius=0.05, color=ALERTE) for x in range(0, 128)])
        self.play(Write(f), Create(vrai), run_time=1.3)
        n0 = note("z reste fixe à 7, pour voir une seule ligne du monde", CIEL)
        self.play(FadeIn(n0)); self.wait(1.8)

        self.next_section("avec des entiers : toujours 0")
        # 1. Avec des entiers : 0, toujours. Le bruit existe entre les entiers,
        # mais on ne l'y regarde jamais.
        n = note("entre deux nombres entiers, le bruit ondule…", DOUX)
        self.play(FadeOut(n0), FadeIn(n)); self.wait(1.0)
        n2 = note("mais à chaque nombre entier, il vaut exactement 0 : terrain plat", ALERTE)
        self.play(FadeOut(n), LaggedStart(*[FadeIn(d, scale=0.3) for d in points], lag_ratio=0.01), run_time=1.6)
        self.play(FadeIn(n2)); self.wait(1.6)

        # 2. Diviser x : on regarde le bruit entre les entiers, et large.
        self.next_section("une grande largeur : des collines larges")
        f2 = formule("h = perlin2d(x / largeur, 7)")
        c = courbe(lambda x: perlin2d(x / 40, 7))
        n3 = note("largeur 40 : les entiers sont loin l'un de l'autre, des collines larges", CIEL)
        self.play(FadeOut(points), FadeOut(vrai), FadeOut(n2), Transform(f, f2), Create(c), run_time=1.6)
        self.play(FadeIn(n3)); self.wait(1.4)

        self.next_section("une petite largeur : des collines serrées")
        f3 = formule("h = perlin2d(x / largeur, 7)")
        c3 = courbe(lambda x: perlin2d(x / 10, 7))
        n4 = note("largeur 10 : des collines plus serrées", CIEL)
        self.play(Transform(f, f3), Transform(c, c3), FadeOut(n3), run_time=1.4)
        self.play(FadeIn(n4)); self.wait(1.2)

        # 3. Multiplier le résultat : plus haut. On revient à ÷ 40, sur des axes
        # en blocs : × 12 fait des collines douze fois plus hautes, mais autour
        # de 0, donc à moitié sous le sol ; + 24 les pose à la bonne hauteur.
        axes2 = Axes(
            x_range=[0, 128, 16], y_range=[-16, 48, 8],
            x_length=11, y_length=3.6,
            axis_config={"color": DOUX, "include_tip": False}, tips=False,
        ).shift(DOWN * 0.4)
        grads2 = VGroup(
            *[Text(str(v), font="DejaVu Sans", font_size=18, color=DOUX).next_to(axes2.c2p(v, -16), DOWN, buff=0.15)
              for v in range(0, 129, 32)],
            *[Text(str(v), font="DejaVu Sans", font_size=18, color=DOUX).next_to(axes2.c2p(0, v), LEFT, buff=0.15)
              for v in (-12, 0, 12, 24, 36, 48)],
        )
        sol = axes2.plot(lambda x: 0, x_range=[0, 128], color=DOUX, stroke_width=1.5, stroke_opacity=0.6)

        self.next_section("× amplitude : plus haut, autour de 0")
        f4 = formule("h = amplitude * perlin2d(x / largeur, 7)")
        c4 = axes2.plot(lambda x: 12 * perlin2d(x / 40, 7), x_range=[0, 127, 0.25], color=CIEL, stroke_width=4)
        n5 = note("× amplitude : plus haut… mais autour de 0, à moitié sous le sol", ALERTE)
        self.play(Transform(f, f4), FadeOut(n4), FadeOut(zero),
                  ReplacementTransform(axes, axes2), ReplacementTransform(grads, grads2),
                  Transform(c, c4), FadeIn(sol), run_time=1.8)
        self.play(FadeIn(n5)); self.wait(1.4)

        self.next_section("+ niveau : à la bonne hauteur")
        f5 = formule("h = niveau + amplitude * perlin2d(x / largeur, 7)")
        c5 = axes2.plot(lambda x: 24 + 12 * perlin2d(x / 40, 7), x_range=[0, 127, 0.25], color=CIEL, stroke_width=4)
        n6 = note("+ niveau : les collines montent, posées au bon niveau", CIEL)
        self.play(Transform(f, f5), Transform(c, c5), FadeOut(n5), run_time=1.4)
        self.play(FadeIn(n6)); self.wait(1.2)

        self.next_section("les colonnes suivent la courbe")
        blocs = VGroup()
        for x in range(0, 128, 2):
            h = math.floor(24 + 12 * perlin2d(x / 40, 7))
            bas, haut = axes2.c2p(x, 0), axes2.c2p(x + 2, h)
            r = Rectangle(width=haut[0] - bas[0], height=haut[1] - bas[1],
                          fill_color=HERBE, fill_opacity=0.85, stroke_width=0.5, stroke_color=FOND)
            r.move_to((bas + haut) / 2)
            blocs.add(r)
        n7 = note("un relief naturel : change la seed pour en découvrir un autre", HERBE)
        self.play(FadeOut(n6), LaggedStart(*[GrowFromEdge(b, DOWN) for b in blocs], lag_ratio=0.01), run_time=2)
        self.play(FadeIn(n7)); self.wait(1.6)
