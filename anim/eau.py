# Étape 10, « Une boucle qui ne fait aucun tour » : l'eau remplit les cases
# vides entre le sol et le niveau de la mer ; là où le sol dépasse la mer, il
# n'y a rien à remplir. Sans code : la boucle d'eau est à l'élève.
#
#   capture.py anim anim/eau.py LEau -o img/outil-eau.webp
import math
from manim import *
from commun import *


class LEau(Scene):
    def construct(self):
        g = Grille(cases=22, hauteur=24, largeur=8, haut=4.6, origine=RIGHT * 3.3 + DOWN * 0.2, y0=6)
        self.play(FadeIn(g.lignes(opacite=0.12)), run_time=0.5)
        hauteurs = [round(19 + 7 * math.sin((i + 1.5) / 3.0)) for i in range(22)]
        MER = 20
        for x, h in enumerate(hauteurs):
            self.add(VGroup(*[g.bloc(x, y, "PIERRE") for y in range(6, h - 3)] + [g.bloc(x, y, "TERRE") for y in range(h - 3, h)] + [g.bloc(x, h, "HERBE")]))
        mer = DashedLine(g.coin(0, MER + 1), g.coin(22, MER + 1), color=COULEURS["EAU"], stroke_width=2.5)
        etiq = texte("niveau\nde la mer", 18, COULEURS["EAU"]).next_to(mer, RIGHT, buff=0.12)
        self.play(Create(mer), FadeIn(etiq))
        compte = texte("·", 30).move_to(LEFT * 3.4 + UP * 0.9)
        geste = texte("·", 24, DOUX).move_to(LEFT * 3.4 + UP * 0.2)
        compte.set_opacity(0); geste.set_opacity(0)
        self.add(compte, geste)
        vu_eau = vu_sec = False
        for x, h in enumerate(hauteurs):
            n = max(0, MER - h)
            if n and not vu_eau:
                self.next_section("sous la mer : on remplit les cases vides"); vu_eau = True
            if not n and not vu_sec:
                self.next_section("le sol dépasse la mer : rien à remplir"); vu_sec = True
            if n:
                t1 = texte(f"{n} case{'s' if n > 1 else ''} vide{'s' if n > 1 else ''}", 30, COULEURS["EAU"])
                t2 = texte("entre le sol et la mer : on remplit", 22, DOUX)
            else:
                t1 = texte("0 case vide", 30, ALERTE)
                t2 = texte("le sol dépasse la mer : rien à remplir", 22, DOUX)
            t1.move_to(LEFT * 3.4 + UP * 0.9); t2.move_to(LEFT * 3.4 + UP * 0.2)
            cadre = Rectangle(width=g.pas, height=g.pas * max(n, 0.15), stroke_color=ALERTE, stroke_width=2.5).move_to(g.coin(x + 0.5, h + 1 + max(n, 0.15) / 2))
            # Le texte change d'un coup : un morphing entre deux textes est illisible.
            compte.become(t1); geste.become(t2)
            self.play(Create(cadre), run_time=0.3)
            if n:
                self.play(LaggedStart(*[FadeIn(g.bloc(x, y, "EAU", 0.8), scale=0.6) for y in range(h + 1, MER + 1)], lag_ratio=0.15), FadeOut(cadre), run_time=0.45)
            else:
                self.play(FadeOut(cadre), run_time=0.35)
        self.play(FadeIn(phrase("l'eau remplit les cases vides entre le sol et le niveau de la mer", CIEL)))
        self.wait(1.8)
