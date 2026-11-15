# Étape 9, « perlin2d » : le bruit le long d'une ligne du monde (z = 7), puis
# les trois mêmes curseurs qu'à l'étape 7, ÷ largeur, × amplitude, + niveau. À
# la fin, les curseurs deviennent la ligne de code :
# h = niveau + amplitude * perlin2d(x / largeur, z / largeur).
# Puis « L'échelle », en 3D : avec z fixé, chaque ligne du monde a la même
# courbe ; avec z / largeur, le relief change dans les deux sens.
# Même bruit que l'application (prélude Lua), permutation tirée de la seed.
#
#   capture.py anim anim/perlin.py LePerlin -o img/etape9-perlin.webp   # + .webm et .vtt
#   capture.py anim anim/perlin.py LeReliefPerlin -o img/etape9-relief.webp
import math
import random
from manim import *
from commun import *

SEED = 1

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
        def reperes(y_range, pas_y, bas):
            a = Axes(x_range=[0, 128, 16], y_range=y_range, x_length=11, y_length=3.4,
                     axis_config={"color": DOUX, "include_tip": False}, tips=False).shift(DOWN * 0.55)
            gr = VGroup(*[texte(str(v), 18, DOUX).next_to(a.c2p(v, bas), DOWN, buff=0.15) for v in range(0, 129, 32)],
                        *[texte(str(v), 18, DOUX).next_to(a.c2p(0, v), LEFT, buff=0.15) for v in pas_y])
            return a, gr

        axes, grads = reperes([-1.5, 1.5, 0.5], (-1, 0, 1), -1.5)
        etiq_x = texte("x", 26, DOUX).next_to(axes.x_axis, RIGHT, buff=0.2)
        zero = axes.plot(lambda x: 0, x_range=[0, 128], color=DOUX, stroke_width=1.5, stroke_opacity=0.6)
        self.play(Create(axes), FadeIn(grads), FadeIn(etiq_x), Create(zero), run_time=1)
        larg = Reglage("÷ largeur", 1, 40, 1, CIEL).placer(LEFT * 4.4 + UP * 3.0)
        amp = Reglage("× amplitude", 0, 16, 1, ALERTE).placer(UP * 3.0)
        niv = Reglage("+ niveau", 0, 40, 0, VERT).placer(RIGHT * 4.4 + UP * 3.0)

        def note(t, couleur):
            return texte(t, 26, couleur).next_to(axes, DOWN, buff=0.62)

        def regler(r, valeur, duree=1.2):
            self.play(r.t.animate.set_value(valeur), run_time=duree)

        self.next_section("z reste fixe : une seule ligne du monde")
        brut = axes.plot(lambda x: perlin2d(x, 7), x_range=[0, 127, 0.25], color=CIEL, stroke_width=4).set_stroke(opacity=0.35)
        self.play(Create(brut), run_time=1.3)
        n = note("une seule ligne du monde : celle où z vaut 7", CIEL)
        self.play(FadeIn(n)); self.wait(1.6)

        self.next_section("à chaque nombre entier : 0")
        points = VGroup(*[Dot(axes.c2p(x, perlin2d(x, 7)), radius=0.05, color=ALERTE) for x in range(0, 128)])
        n2 = note("à chaque nombre entier, il vaut exactement 0 : terrain plat", ALERTE)
        self.play(FadeOut(n), LaggedStart(*[FadeIn(d, scale=0.3) for d in points], lag_ratio=0.01), run_time=1.6)
        self.play(FadeIn(n2)); self.wait(1.6)

        self.next_section("÷ largeur : des collines larges ou serrées")
        courbe = always_redraw(lambda: axes.plot(lambda x: perlin2d(x / larg.t.get_value(), 7 / larg.t.get_value()), x_range=[0, 127, 0.25], color=CIEL, stroke_width=4))
        self.play(FadeOut(points), FadeOut(brut), FadeOut(n2), FadeIn(larg), FadeIn(courbe), run_time=1.0)
        regler(larg, 40, 2.0)
        n = note("÷ largeur : on regarde entre les entiers, les collines s'élargissent", CIEL)
        self.play(FadeIn(n)); self.wait(1.0)
        regler(larg, 10, 1.4)
        n2 = note("petite largeur : des collines serrées", CIEL)
        self.play(FadeOut(n), FadeIn(n2)); self.wait(0.8)
        regler(larg, 25, 1.2); self.wait(0.5)

        # Le bruit va de -1 à 1 : sur une échelle en blocs, à peine un bloc de haut.
        self.next_section("× amplitude : plus haut, autour de 0")
        axes2, grads2 = reperes([-16, 48, 16], (-16, 0, 16, 32, 48), -16)
        sol = axes2.plot(lambda x: 0, x_range=[0, 128], color=DOUX, stroke_width=1.5, stroke_opacity=0.6)

        def f(x):
            return niv.t.get_value() + amp.t.get_value() * perlin2d(x / larg.t.get_value(), 7 / larg.t.get_value())

        def trace():
            return axes2.plot(f, x_range=[0, 127, 0.25], color=CIEL, stroke_width=4)

        courbe2 = always_redraw(trace)
        self.remove(courbe)
        fige = axes.plot(lambda x: perlin2d(x / 25, 7 / 25), x_range=[0, 127, 0.25], color=CIEL, stroke_width=4)
        self.add(fige)
        self.play(FadeOut(n2), FadeOut(zero), ReplacementTransform(axes, axes2), ReplacementTransform(grads, grads2),
                  ReplacementTransform(fige, trace()), FadeIn(sol), FadeIn(amp),
                  etiq_x.animate.next_to(axes2.x_axis, RIGHT, buff=0.2), run_time=1.6)
        self.remove(*[m for m in self.mobjects if isinstance(m, ParametricFunction) and m is not sol])
        self.add(courbe2)
        n = note("en blocs, le bruit fait à peine un bloc de haut", ALERTE)
        self.play(FadeIn(n)); self.wait(1.0)
        regler(amp, 16, 1.6)
        n2 = note("× amplitude : plus haut… mais autour de 0, à moitié sous le sol", ALERTE)
        self.play(FadeOut(n), FadeIn(n2)); self.wait(1.0)
        regler(amp, 13, 1.0)

        self.next_section("+ niveau : à la bonne hauteur")
        self.play(FadeOut(n2), FadeIn(niv))
        regler(niv, 30, 1.6)
        n = note("+ niveau : les collines montent, posées au bon niveau", VERT)
        self.play(FadeIn(n)); self.wait(0.6)
        regler(niv, 20, 1.0); self.wait(0.6)

        self.next_section("les colonnes suivent la courbe")
        blocs = VGroup()
        for x in range(0, 128, 2):
            h = math.floor(f(x))
            bas, haut = axes2.c2p(x, 0), axes2.c2p(x + 2, h)
            r = Rectangle(width=haut[0] - bas[0], height=haut[1] - bas[1], fill_color=VERT, fill_opacity=0.85, stroke_width=0.5, stroke_color=FOND)
            blocs.add(r.move_to((bas + haut) / 2))
        n7 = note("un relief naturel : change la seed pour en découvrir un autre", VERT)
        self.play(FadeOut(n), LaggedStart(*[GrowFromEdge(b, DOWN) for b in blocs], lag_ratio=0.01), run_time=2)
        self.play(FadeIn(n7)); self.wait(1.6)

        self.next_section("les trois réglages, dans une ligne de code")
        # La courbe ne bouge plus : on la fige avant de défaire les curseurs.
        self.remove(courbe2); self.add(trace())
        ligne = code("h = niveau + amplitude * perlin2d(x / largeur, z / largeur)", 24).move_to(UP * 2.35)
        ligne[40:47].set_color(CIEL)    # le second « largeur » : z se divise comme x
        n8 = note("les trois réglages deviennent une ligne de code", WHITE)
        self.play(FadeOut(n7), FadeIn(n8), run_time=0.6)
        ranger_les_reglages(self, ligne, [(niv, (2, 8)), (amp, (9, 18)), (larg, (30, 37))])
        self.wait(2.2)


class LeReliefPerlin(ThreeDScene):
    """Comme les collines de l'étape 8 : le terrain en 3D, d'abord avec z fixé
    (la même courbe sur toutes les lignes), puis avec z / largeur."""

    def construct(self):
        # Un peu plus loin que les collines : en tournant, l'axe vertical
        # passerait sur le titre.
        self.set_camera_orientation(phi=62 * DEGREES, theta=-50 * DEGREES, zoom=0.8)
        axes = ThreeDAxes(
            x_range=[0, 128, 32], y_range=[0, 128, 32], z_range=[0, 40, 10],
            x_length=7, y_length=7, z_length=2.4,
            axis_config={"color": DOUX, "include_tip": False},
        )
        ex = texte("x", 28, DOUX).next_to(axes.x_axis.get_end(), RIGHT)
        ez = texte("z", 28, DOUX).next_to(axes.y_axis.get_end(), UP)
        self.add(axes)
        self.add_fixed_orientation_mobjects(ex, ez)
        sombre = "#2f6a23"

        def relief(f):
            s = Surface(
                lambda u, v: axes.c2p(u, v, f(u, v)),
                u_range=[0, 127], v_range=[0, 127], resolution=(48, 48),
                fill_opacity=0.95, stroke_width=0.3, stroke_color=sombre, checkerboard_colors=False,
            )
            s.set_fill_by_value(axes=axes, colorscale=[(sombre, 12), (VERT, 30)], axis=2)
            return s

        def fixe(m, haut):
            m.to_edge(UP if haut else DOWN, buff=0.4 if haut else 0.5)
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)          # fixé dans le cadre, mais montré seulement quand on l'anime
            return m

        self.next_section("z fixé : la même courbe sur toutes les lignes")
        f1 = fixe(code("perlin2d(x / largeur, 7)", 30), True)
        s1 = relief(lambda x, z: 20 + 13 * perlin2d(x / 25, 7))
        self.play(Create(s1), FadeIn(f1), run_time=2)
        n1 = fixe(texte("z fixé : en avançant vers le fond (z), rien ne change", 26, ALERTE), False)
        self.play(FadeIn(n1))
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(2.4)
        self.stop_ambient_camera_rotation()

        self.next_section("z / largeur : du relief dans les deux sens")
        f2 = fixe(code("perlin2d(x / largeur, z / largeur)", 30), True)
        s2 = relief(lambda x, z: 20 + 13 * perlin2d(x / 25, z / 25))
        n2 = fixe(texte("z divisé comme x : des sommets et des vallées dans les deux sens", 26, CIEL), False)
        # Des fondus pour les textes fixés dans le cadre : transformés, ils
        # seraient dessinés en 3D pendant l'animation.
        self.play(FadeOut(n1), FadeOut(f1), FadeIn(f2), Transform(s1, s2), run_time=2)
        self.play(FadeIn(n2))
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(3.2)
        self.stop_ambient_camera_rotation()
