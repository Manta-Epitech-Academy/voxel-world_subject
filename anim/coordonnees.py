# Étape 1, « Les coordonnées x, y, z » : x et z avancent sur le sol, y monte ;
# set_block(64, 10, 64, PIERRE) compte 64 en x, 10 en y, 64 en z.
#
#   capture.py anim anim/coordonnees.py LesCoordonnees -o img/outil-coordonnees.webp
from manim import *
from commun import *


class LesCoordonnees(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=62 * DEGREES, theta=-120 * DEGREES, zoom=0.85)
        axes = ThreeDAxes(x_range=[0, 128, 32], y_range=[0, 128, 32], z_range=[0, 64, 16],
                          x_length=6, y_length=6, z_length=3, axis_config={"color": DOUX, "include_tip": True})
        sol = Surface(lambda u, v: axes.c2p(u, v, 0), u_range=[0, 128], v_range=[0, 128], resolution=(8, 8),
                      fill_opacity=0.06, stroke_width=0.5, stroke_color=DOUX, checkerboard_colors=False, fill_color=CIEL)
        ex = Text("x", font="DejaVu Sans", font_size=30, color="#ff5555").next_to(axes.x_axis.get_end(), RIGHT)
        ez = Text("z", font="DejaVu Sans", font_size=30, color="#5599ff").next_to(axes.y_axis.get_end(), UP)
        ey = Text("y", font="DejaVu Sans", font_size=30, color="#55dd55").next_to(axes.z_axis.get_end(), UP)
        self.add_fixed_orientation_mobjects(ex, ey, ez)
        self.remove(ex, ey, ez)
        self.next_section("x et z sur le sol, y vers le ciel")
        self.play(Create(axes), FadeIn(sol), FadeIn(ex), FadeIn(ey), FadeIn(ez), run_time=1.5)
        f = code("set_block(64, 10, 64, PIERRE)", 30).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(f); self.remove(f)
        self.play(Write(f))
        self.wait(0.8)

        def fleche(a, b, couleur):
            # Un demi-bloc au-dessus du sol, pour ne pas se battre avec lui.
            return Arrow3D(axes.c2p(a[0], a[1], a[2] + 0.5), axes.c2p(b[0], b[1], b[2] + 0.5), color=couleur, thickness=0.02, height=0.25, base_radius=0.06)

        def etiquette(t, couleur, pos):
            m = Text(t, font="DejaVu Sans", font_size=26, color=couleur).to_edge(DOWN, buff=0.5).shift(pos)
            self.add_fixed_in_frame_mobjects(m); self.remove(m)
            return m

        self.next_section("64 en x")
        e1 = etiquette("64 en x", "#ff5555", LEFT * 3)
        self.play(Create(fleche((0, 0, 0), (64, 0, 0), "#ff5555")), FadeIn(e1), run_time=1.0)
        self.next_section("10 en y, vers le ciel")
        e2 = etiquette("10 en y", "#55dd55", ORIGIN)
        self.play(Create(fleche((64, 0, 0), (64, 0, 10), "#55dd55")), FadeIn(e2), run_time=1.0)
        self.next_section("64 en z")
        e3 = etiquette("64 en z", "#5599ff", RIGHT * 3)
        self.play(Create(fleche((64, 0, 10), (64, 64, 10), "#5599ff")), FadeIn(e3), run_time=1.0)
        bloc = Cube(side_length=0.25, fill_color=COULEURS["PIERRE"], fill_opacity=1, stroke_width=0).move_to(axes.c2p(64, 64, 10))
        self.play(FadeIn(bloc, scale=0.3), run_time=0.6)
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(2.5)
        self.stop_ambient_camera_rotation()
