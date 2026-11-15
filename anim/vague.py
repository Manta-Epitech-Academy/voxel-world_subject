# Étape 7, « La vague » : trois curseurs, ÷ largeur, × amplitude, + niveau.
# Chacun passe par plusieurs valeurs et la courbe suit. Les colonnes prennent
# la hauteur de la courbe. À la fin, les trois curseurs deviennent la
# ligne de code : h = niveau + amplitude * math.sin(x / largeur).
#
#   capture.py anim anim/vague.py LaVague -o img/etape7-vague.webp   # + .webm et .vtt des chapitres
import math
from manim import *
from commun import *


class LaVague(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 128, 16], y_range=[0, 40, 10], x_length=11, y_length=3.6,
                    axis_config={"color": DOUX, "include_tip": False}, tips=False).shift(DOWN * 0.6)
        grads = VGroup(*[texte(str(v), 18, DOUX).next_to(axes.c2p(v, 0), DOWN, buff=0.15) for v in range(0, 129, 32)],
                       *[texte(str(v), 18, DOUX).next_to(axes.c2p(0, v), LEFT, buff=0.15) for v in range(10, 41, 10)])
        etiq_x = texte("x", 26, DOUX).next_to(axes.x_axis, RIGHT, buff=0.2)
        etiq_h = texte("h", 26, DOUX).next_to(axes.y_axis, UP, buff=0.12)
        self.play(Create(axes), FadeIn(grads), FadeIn(etiq_x), FadeIn(etiq_h), run_time=1)
        larg = Reglage("÷ largeur", 1, 20, 1, CIEL).placer(LEFT * 4.4 + UP * 3.0)
        amp = Reglage("× amplitude", 0, 10, 1, ALERTE).placer(UP * 3.0)
        niv = Reglage("+ niveau", 0, 40, 20, VERT).placer(RIGHT * 4.4 + UP * 3.0)

        def f(x):
            return niv.t.get_value() + amp.t.get_value() * math.sin(x / larg.t.get_value())

        def trace():
            return axes.plot(f, x_range=[0, 127, 0.25], color=CIEL, stroke_width=4)

        def note(t, couleur):
            return texte(t, 26, couleur).next_to(axes, DOWN, buff=0.62)

        def regler(r, valeur, duree=1.2):
            self.play(r.t.animate.set_value(valeur), run_time=duree)

        self.next_section("math.sin(x) seul : trop serré")
        c0 = trace()
        self.play(Create(c0), run_time=1.3)
        courbe = always_redraw(trace)
        self.remove(c0); self.add(courbe)
        n = note("math.sin(x) tout seul : une vague tous les 6 blocs, trop serré", ALERTE)
        self.play(FadeIn(n)); self.wait(1.2)

        self.next_section("÷ largeur : la vague s'étire")
        self.play(FadeOut(n), FadeIn(larg))
        regler(larg, 5)
        n = note("÷ largeur : plus elle est grande, plus la vague s'étire", CIEL)
        self.play(FadeIn(n))
        regler(larg, 18, 1.4); self.wait(0.5)
        regler(larg, 10, 1.0); self.wait(0.6)

        self.next_section("× amplitude : la vague grandit")
        self.play(FadeOut(n), FadeIn(amp))
        regler(amp, 4)
        n = note("× amplitude : plus elle est grande, plus la vague est haute", ALERTE)
        self.play(FadeIn(n))
        regler(amp, 9, 1.4); self.wait(0.5)
        regler(amp, 6, 1.0); self.wait(0.6)

        self.next_section("+ niveau : la vague monte ou descend")
        self.play(FadeOut(n), FadeIn(niv))
        regler(niv, 3, 1.4)
        n = note("niveau trop bas : la vague passe sous le sol", ALERTE)
        self.play(FadeIn(n)); self.wait(0.8)
        regler(niv, 30, 1.6)
        n2 = note("+ niveau : toute la vague monte", VERT)
        self.play(FadeOut(n), FadeIn(n2)); self.wait(0.5)
        regler(niv, 18, 1.0); self.wait(0.6)

        self.next_section("les colonnes suivent la courbe")
        blocs = VGroup()
        for x in range(0, 128, 2):
            h = math.floor(f(x))
            bas, haut = axes.c2p(x, 0), axes.c2p(x + 2, h)
            r = Rectangle(width=haut[0] - bas[0], height=haut[1] - bas[1], fill_color=VERT, fill_opacity=0.85, stroke_width=0.5, stroke_color=FOND)
            blocs.add(r.move_to((bas + haut) / 2))
        n = note("chaque colonne prend la hauteur de la vague, arrondie vers le bas", VERT)
        self.play(FadeOut(n2), LaggedStart(*[GrowFromEdge(b, DOWN) for b in blocs], lag_ratio=0.01), run_time=2.2)
        self.play(FadeIn(n)); self.wait(1.6)

        self.next_section("les trois réglages, dans une ligne de code")
        # La courbe ne bouge plus : on la fige avant de défaire les curseurs.
        self.remove(courbe); self.add(trace())
        ligne = code("h = niveau + amplitude * math.sin(x / largeur)", 30).move_to(UP * 2.35)
        n3 = note("les trois réglages deviennent une ligne de code", WHITE)
        self.play(FadeOut(n), FadeIn(n3), run_time=0.6)
        ranger_les_reglages(self, ligne, [(niv, (2, 8)), (amp, (9, 18)), (larg, (30, 37))])
        self.wait(1.6)

        self.next_section("la hauteur du sol vient de math.sin(x)")
        fin = texte("La hauteur du sol est calculée grâce à math.sin(x)", 28, WHITE).next_to(axes, DOWN, buff=0.62)
        self.play(FadeOut(n3), FadeIn(fin), run_time=1.0)
        self.wait(2.0)
