# Étape 9, « Remplir d'eau » : de h + 1 jusqu'à NIVEAU_MER ; quand le sol est
# plus haut que la mer, la boucle ne fait aucun tour.
#
#   capture.py anim anim/eau.py LEau -o img/outil-eau.webp
import math
from manim import *
from commun import *


class LEau(Scene):
    def construct(self):
        prog = bloc_code(["NIVEAU_MER = 22", "for y = h + 1, NIVEAU_MER do", "  set_block(x, y, z, EAU)", "end"], 24).to_edge(LEFT, buff=0.7).shift(UP * 0.8)
        self.play(Write(prog), run_time=1.2)
        g = Grille(cases=14, hauteur=32, largeur=5.6, haut=4.6, origine=RIGHT * 3.6 + DOWN * 0.4)
        self.play(FadeIn(g.lignes(opacite=0.12)), FadeIn(g.axe_y(pas=4)), run_time=0.6)
        hauteurs = [round(21 + 7 * math.sin(i / 2.0)) for i in range(14)]
        for x, h in enumerate(hauteurs):
            col = VGroup(*[g.bloc(x, y, "PIERRE") for y in range(1, h - 3)] + [g.bloc(x, y, "TERRE") for y in range(h - 3, h)] + [g.bloc(x, h, "HERBE"), g.bloc(x, 0, "BEDROCK")])
            self.add(col)
        mer = DashedLine(g.coin(0, 23), g.coin(14, 23), color=COULEURS["EAU"], stroke_width=2)
        etiq = code("NIVEAU_MER = 22", 16, COULEURS["EAU"]).next_to(mer, RIGHT, buff=0.12)
        self.play(Create(mer), FadeIn(etiq))
        hval = code("h = ?", 24, ALERTE).next_to(prog, DOWN, buff=0.6, aligned_edge=LEFT)
        tours = code("·", 18, DOUX).next_to(hval, DOWN, buff=0.2, aligned_edge=LEFT)
        self.add(hval, tours)

        self.next_section("sol sous la mer : la boucle remplit")
        for x, h in enumerate(hauteurs):
            n = max(0, 22 - h)
            self.play(Transform(hval, code(f"h = {h}", 24, ALERTE).move_to(hval, aligned_edge=LEFT)),
                      Transform(tours, code(f"y de {h + 1} à 22 : {n} tour{'s' if n > 1 else ''}", 18, COULEURS["EAU"] if n else ERREUR).move_to(tours, aligned_edge=LEFT)), run_time=0.25)
            if n:
                self.play(LaggedStart(*[FadeIn(g.bloc(x, y, "EAU", 0.8), scale=0.6) for y in range(h + 1, 23)], lag_ratio=0.15), run_time=0.4)
            else:
                if x == next(i for i, hh in enumerate(hauteurs) if hh >= 22):
                    self.next_section("sol au-dessus : aucun tour, pas d'eau")
                self.wait(0.35)
        self.play(FadeIn(phrase("de h + 1 à 22 : s'il n'y a rien entre les deux, la boucle ne pose rien", CIEL)))
        self.wait(1.8)
