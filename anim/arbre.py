# Étape 10, « Une fonction arbre » : un tronc de 5 blocs, puis des feuilles
# autour du haut — à compléter.
#
#   capture.py anim anim/arbre.py LArbre -o img/outil-arbre.webp
from manim import *
from commun import *


class LArbre(Scene):
    def construct(self):
        self.next_section("le tronc : 5 BOIS, de y à y + 4")
        prog = bloc_code(["function arbre(x, y, z)", "  for i = 0, 4 do", "    set_block(x, y + i, z, BOIS)", "  end", "  set_block(x, y + 5, z, FEUILLES)", "end"], 22).to_edge(LEFT, buff=0.5).shift(UP * 0.8)
        self.play(Write(prog), run_time=1.4)
        g = Grille(cases=9, hauteur=12, largeur=4.2, haut=4.6, origine=RIGHT * 3.2 + DOWN * 0.3, y0=18)
        self.play(FadeIn(g.lignes(opacite=0.15)), FadeIn(g.axe_y(pas=2)), run_time=0.6)
        for x in range(9):
            self.add(g.bloc(x, 19, "TERRE"), g.bloc(x, 20, "HERBE"), g.bloc(x, 18, "TERRE"))
        appel = code("arbre(4, 21, z)", 24, ALERTE).next_to(prog, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(FadeIn(appel))
        ival = code("i = 0", 22, ALERTE).next_to(appel, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(ival))
        for i in range(5):
            self.play(Transform(ival, code(f"i = {i}  →  y + i = {21 + i}", 22, ALERTE).move_to(ival, aligned_edge=LEFT)),
                      FadeIn(g.bloc(4, 21 + i, "BOIS"), scale=0.6), run_time=0.4)
        self.next_section("une feuille au sommet, à y + 5")
        self.play(FadeOut(ival), FadeIn(g.bloc(4, 26, "FEUILLES"), scale=0.6), run_time=0.6)
        ph = phrase("un tronc et une feuille : c'est à toi de compléter la couronne", CIEL)
        self.play(FadeIn(ph)); self.wait(1.4)
        self.next_section("par exemple, des feuilles tout autour")
        feuilles = VGroup(*[g.bloc(x, y, "FEUILLES", 0.9) for y in (24, 25) for x in (2, 3, 5, 6)] + [g.bloc(x, 26, "FEUILLES", 0.9) for x in (3, 5)])
        self.play(FadeOut(ph), LaggedStart(*[FadeIn(f, scale=0.6) for f in feuilles], lag_ratio=0.08), run_time=1.5)
        self.play(FadeIn(phrase("deux boucles de plus, autour de x et z, et l'arbre a sa couronne", ALERTE)))
        self.wait(1.8)
