# Étape 5, « Écrire sa propre fonction » : colonne(x, z, h) range du code sous
# un nom ; chaque appel donne ses valeurs aux paramètres, et une colonne
# apparaît à la hauteur demandée.
#
#   capture.py anim anim/fonction.py LaFonction -o img/outil-fonction.webp
from manim import *
from commun import *


class LaFonction(Scene):
    def construct(self):
        self.next_section("une fonction : du code sous un nom")
        prog = bloc_code(["function colonne(x, z, h)", "  set_block(x, 0, z, BEDROCK)", "  -- ... les couches, jusqu'à h", "  set_block(x, h, z, HERBE)", "end"], 22).to_corner(UL, buff=0.5)
        cadre = SurroundingRectangle(prog, color=DOUX, buff=0.18, corner_radius=0.1)
        self.play(Write(prog), Create(cadre), run_time=1.4)
        params = SurroundingRectangle(prog[0][16:23], color=ALERTE, buff=0.05)
        self.play(Create(params))
        ph = phrase("x, z et h sont les paramètres : des variables remplies à chaque appel", CIEL)
        self.play(FadeIn(ph)); self.wait(1.4)

        g = Grille(cases=16, hauteur=28, largeur=6.4, haut=4.4, origine=RIGHT * 3.2 + DOWN * 0.5)
        self.play(FadeIn(g.lignes(opacite=0.15)), FadeIn(g.axe_x(pas=2)), FadeIn(g.axe_y(pas=4)), FadeOut(params), run_time=0.6)

        def appel(nom, x, z, h, section):
            self.next_section(section)
            ligne = code(nom, 26, ALERTE).next_to(prog, DOWN, buff=0.7, aligned_edge=LEFT)
            self.play(FadeIn(ligne))
            valeurs = code(f"x = {x}   z = {z}   h = {h}", 20, ALERTE).next_to(ligne, DOWN, buff=0.25, aligned_edge=LEFT)
            fleche = Arrow(ligne.get_top(), prog.get_bottom(), buff=0.1, color=ALERTE, stroke_width=3, max_tip_length_to_length_ratio=0.2)
            self.play(FadeIn(valeurs), GrowArrow(fleche), run_time=0.7)
            couches = [(0, "BEDROCK")] + [(y, "PIERRE") for y in range(1, h - 3)] + [(y, "TERRE") for y in range(h - 3, h)] + [(h, "HERBE")]
            col = VGroup(*[g.bloc(x, y, t) for y, t in couches])
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.08) for b in col], lag_ratio=0.04), run_time=1.3)
            self.wait(0.6)
            self.play(FadeOut(ligne), FadeOut(valeurs), FadeOut(fleche), run_time=0.4)

        self.play(FadeOut(ph))
        appel("colonne(10, 10, 20)", 10, 10, 20, "colonne(10, 10, 20)")
        appel("colonne(11, 10, 25)", 11, 10, 25, "colonne(11, 10, 25)")
        self.play(FadeIn(phrase("le même code, appelé deux fois avec d'autres valeurs : deux colonnes", ALERTE)))
        self.wait(1.8)
