# Étape 6, « Une fonction arbre » : un tronc de 5 blocs, de y à y + 4, puis
# des feuilles autour du sommet. Sans code : la fonction est à l'élève.
#
#   capture.py anim anim/arbre.py LArbre -o img/outil-arbre.webp
from manim import *
from commun import *


class LArbre(Scene):
    def construct(self):
        self.next_section("le tronc : 5 blocs, de y à y + 4")
        g = Grille(cases=9, hauteur=12, largeur=4.2, haut=4.6, origine=RIGHT * 2.4 + DOWN * 0.3, y0=18)
        self.play(FadeIn(g.lignes(opacite=0.15)), FadeIn(g.axe_y(pas=2)), run_time=0.6)
        for x in range(9):
            self.add(g.bloc(x, 19, "TERRE"), g.bloc(x, 20, "HERBE"), g.bloc(x, 18, "TERRE"))
        depart = texte("y : la case juste\nau-dessus de l'herbe", 22, ALERTE).move_to(LEFT * 3.9 + DOWN * 1.2)
        vise = Arrow(depart.get_right(), g.centre(4, 21) + LEFT * g.pas * 0.6, buff=0.15, color=ALERTE, stroke_width=3, max_tip_length_to_length_ratio=0.08)
        self.play(FadeIn(depart), GrowArrow(vise))
        self.wait(0.6)
        etiqs = VGroup()
        for i in range(5):
            e = code("y" if i == 0 else f"y + {i}", 18, ALERTE).next_to(g.centre(4, 21 + i), RIGHT, buff=0.35)
            etiqs.add(e)
            self.play(FadeIn(g.bloc(4, 21 + i, "BOIS", 1).set_stroke(BLANC, 1), scale=0.6), FadeIn(e), run_time=0.45)
        ph = phrase("un tronc de 5 blocs de BOIS : il part de y et monte jusqu'à y + 4", CIEL)
        self.play(FadeIn(ph)); self.wait(1.4)
        self.next_section("des feuilles autour du sommet")
        feuilles = VGroup(*[g.bloc(4, 26, "FEUILLES", 0.9)] + [g.bloc(x, y, "FEUILLES", 0.9) for y in (24, 25) for x in (2, 3, 5, 6)] + [g.bloc(x, 26, "FEUILLES", 0.9) for x in (3, 5)])
        self.play(FadeOut(ph), FadeOut(depart), FadeOut(vise), FadeOut(etiqs), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(f, scale=0.6) for f in feuilles], lag_ratio=0.1), run_time=1.8)
        self.play(FadeIn(phrase("des FEUILLES autour du sommet : à toi de choisir leur forme", ALERTE)))
        self.wait(1.8)
