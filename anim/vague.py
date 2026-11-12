# La vague, terme par terme : sin(x) → sin(x / 8) → 4 * sin(x / 8) → 20 + 4 * sin(x / 8),
# puis les blocs qui suivent la courbe. Style 3Blue1Brown : fond sombre, une courbe
# qui se transforme, la formule qui change en haut, un mot pour chaque changement.
#
#   ~/.claude/.venvs/manim/bin/python ~/.claude/skills/workshop-capture/scripts/capture.py \
#       anim anim/vague.py LaVague -o img/etape4b-vague.webp   # + .webm et .vtt des chapitres
import math
from manim import *

FOND = "#14161b"      # le fond de l'application
HERBE = "#5fb946"
CIEL = "#9fd3ff"
ALERTE = "#f2c14e"
DOUX = "#9aa1ad"

config.background_color = FOND


def formule(texte):
    t = Text(texte, font="DejaVu Sans Mono", font_size=34, color=WHITE)
    return t.to_edge(UP, buff=0.5)


class LaVague(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 128, 16], y_range=[0, 40, 10],
            x_length=11, y_length=4.2,
            axis_config={"color": DOUX, "include_tip": False, "font_size": 22},
            tips=False,
        ).shift(DOWN * 0.6)
        # Les graduations en Text (Pango) : add_coordinates passe par LaTeX, absent ici.
        grads = VGroup(*[Text(str(v), font="DejaVu Sans", font_size=18, color=DOUX).next_to(axes.c2p(v, 0), DOWN, buff=0.15)
                         for v in range(0, 129, 32)],
                       *[Text(str(v), font="DejaVu Sans", font_size=18, color=DOUX).next_to(axes.c2p(0, v), LEFT, buff=0.15)
                         for v in range(10, 41, 10)])
        etiq_x = Text("x", font="DejaVu Sans", font_size=26, color=DOUX).next_to(axes.x_axis, RIGHT, buff=0.2)
        etiq_h = Text("h", font="DejaVu Sans", font_size=26, color=DOUX).next_to(axes.y_axis, UP, buff=0.15)
        self.play(Create(axes), FadeIn(grads), FadeIn(etiq_x), FadeIn(etiq_h), run_time=1)

        def courbe(f, couleur=CIEL):
            return axes.plot(f, x_range=[0, 127, 0.25], color=couleur, stroke_width=4)

        def note(texte, couleur):
            return Text(texte, font="DejaVu Sans", font_size=26, color=couleur).next_to(axes, DOWN, buff=0.35)

        # 1. sin(x) : trop serré, et autour de zéro.
        self.next_section("math.sin(x) : trop serré")
        f = formule("h = math.sin(x)")
        c = courbe(lambda x: 20 + math.sin(x))   # dessinée à 20 pour rester visible
        self.play(Write(f), Create(c), run_time=1.3)
        n = note("une vague tous les 6 blocs : trop serré", ALERTE)
        self.play(FadeIn(n)); self.wait(1.0)

        # 2. / 8 : plus large.
        self.next_section("÷ 8 : plus large")
        f2 = formule("h = math.sin(x / 8)")
        c2 = courbe(lambda x: 20 + math.sin(x / 8))
        n2 = note("÷ 8 : la vague s'élargit", CIEL)
        self.play(Transform(f, f2), Transform(c, c2), FadeOut(n), run_time=1.4)
        self.play(FadeIn(n2)); self.wait(1.0)

        # 3. × 4 : plus haute.
        self.next_section("× 4 : plus haute")
        f3 = formule("h = 4 * math.sin(x / 8)")
        c3 = courbe(lambda x: 20 + 4 * math.sin(x / 8))
        n3 = note("× 4 : la vague grandit", CIEL)
        self.play(Transform(f, f3), Transform(c, c3), FadeOut(n2), run_time=1.4)
        self.play(FadeIn(n3)); self.wait(1.0)

        # 4. + 20 : à la bonne hauteur. Jusqu'ici la courbe était posée à 20 pour
        # qu'on la voie ; on la montre d'abord autour de 0, puis elle monte.
        self.next_section("+ 20 : à la bonne hauteur")
        f4 = formule("h = 20 + 4 * math.sin(x / 8)")
        c0 = courbe(lambda x: 4 * math.sin(x / 8))
        n4 = note("sans + 20, la vague est au ras du sol…", ALERTE)
        self.play(Transform(c, c0), FadeOut(n3), run_time=1.0)
        self.play(FadeIn(n4)); self.wait(1.0)
        c4 = courbe(lambda x: 20 + 4 * math.sin(x / 8))
        n5 = note("+ 20 : elle monte à la hauteur 20", CIEL)
        self.play(Transform(f, f4), Transform(c, c4), FadeOut(n4), run_time=1.4)
        self.play(FadeIn(n5)); self.wait(1.0)

        self.next_section("les colonnes suivent la courbe")
        # 5. Les blocs suivent la courbe : set_block arrondit vers le bas.
        blocs = VGroup()
        for x in range(0, 128, 2):
            h = math.floor(20 + 4 * math.sin(x / 8))
            bas, haut = axes.c2p(x, 0), axes.c2p(x + 2, h)
            r = Rectangle(width=haut[0] - bas[0], height=haut[1] - bas[1],
                          fill_color=HERBE, fill_opacity=0.85, stroke_width=0.5, stroke_color=FOND)
            r.move_to((bas + haut) / 2)
            blocs.add(r)
        n6 = note("chaque colonne prend la hauteur de la vague, arrondie vers le bas", HERBE)
        self.play(FadeOut(n5), LaggedStart(*[GrowFromEdge(b, DOWN) for b in blocs], lag_ratio=0.01), run_time=2.2)
        self.play(FadeIn(n6)); self.wait(1.6)
