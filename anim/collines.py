# Les collines dans les deux sens : le terrain vu en 3D, d'abord avec une seule
# vague en x (une tôle ondulée : rien ne change quand on avance en z), puis la
# vague en z qui s'ajoute et fait la boîte d'œufs.
#
#   capture.py anim anim/collines.py LesCollines -o img/etape4c-collines.webp   # + .webm et .vtt
import math
from manim import *

FOND = "#14161b"
HERBE = "#5fb946"
HERBE_SOMBRE = "#2f6a23"
CIEL = "#9fd3ff"
ALERTE = "#f2c14e"
DOUX = "#9aa1ad"

config.background_color = FOND
TAILLE = 128


class LesCollines(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=62 * DEGREES, theta=-50 * DEGREES, zoom=0.9)
        axes = ThreeDAxes(
            x_range=[0, TAILLE, 32], y_range=[0, TAILLE, 32], z_range=[0, 40, 10],
            x_length=7, y_length=7, z_length=2.4,
            axis_config={"color": DOUX, "include_tip": False},
        )
        ex = Text("x", font="DejaVu Sans", font_size=28, color=DOUX).next_to(axes.x_axis.get_end(), RIGHT)
        ez = Text("z", font="DejaVu Sans", font_size=28, color=DOUX).next_to(axes.y_axis.get_end(), UP)
        self.add(axes)
        # Les lettres restent face à la caméra pendant la rotation.
        self.add_fixed_orientation_mobjects(ex, ez)

        def relief(f):
            s = Surface(
                lambda u, v: axes.c2p(u, v, f(u, v)),
                u_range=[0, TAILLE], v_range=[0, TAILLE], resolution=(40, 40),
                fill_opacity=0.95, stroke_width=0.3, stroke_color=HERBE_SOMBRE, checkerboard_colors=False,
            )
            s.set_fill_by_value(axes=axes, colorscale=[(HERBE_SOMBRE, 14), (HERBE, 28)], axis=2)
            return s

        def formule(t):
            m = Text(t, font="DejaVu Sans Mono", font_size=30, color=WHITE).to_edge(UP, buff=0.4)
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)          # fixé dans le cadre, mais montré seulement quand on l'anime
            return m

        def note(t, couleur):
            m = Text(t, font="DejaVu Sans", font_size=26, color=couleur).to_edge(DOWN, buff=0.5)
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
            return m

        # 1. Une vague en x seulement.
        self.next_section("une vague en x : la tôle ondulée")
        f1 = formule("h = 20 + 4 * math.sin(x / 8)")
        s1 = relief(lambda x, z: 20 + 4 * math.sin(x / 8))
        self.play(Create(s1), Write(f1), run_time=2)
        n1 = note("une vague en x : en avançant vers le fond (z), rien ne change", ALERTE)
        self.play(FadeIn(n1))
        # On tourne autour pour montrer la tôle ondulée.
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(2.4)
        self.stop_ambient_camera_rotation()

        # 2. Plus une vague en z.
        self.next_section("+ une vague en z : la boîte d'œufs")
        f2 = formule("h = 20 + 4 * math.sin(x / 8) + 4 * math.sin(z / 11)")
        s2 = relief(lambda x, z: 20 + 4 * math.sin(x / 8) + 4 * math.sin(z / 11))
        n2 = note("+ une vague en z : des bosses et des creux dans tous les sens", CIEL)
        # FadeOut / FadeIn plutôt que Transform : un texte fixé dans le cadre
        # qui se transforme est dessiné en 3D pendant l'animation, et se retrouve
        # couché le long d'un axe.
        self.play(FadeOut(n1), FadeOut(f1), FadeIn(f2), Transform(s1, s2), run_time=2)
        self.play(FadeIn(n2))
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(2.6)
        self.stop_ambient_camera_rotation()
