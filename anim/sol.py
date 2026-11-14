# Étape 6, « get_block et while : trouver le sol » : y part du ciel, et
# descend tant que la case est de l'AIR.
#
#   capture.py anim anim/sol.py TrouverLeSol -o img/outil-sol.webp
from manim import *
from commun import *


class TrouverLeSol(Scene):
    def construct(self):
        self.next_section("on part du ciel")
        prog = bloc_code(["y = HAUTEUR - 1", "while y > 0 and get_block(x, y, z) == AIR do", "  y = y - 1", "end", 'print("le sol est à y =", y)'], 22).to_edge(LEFT, buff=0.5).shift(UP * 0.9)
        self.play(Write(prog), run_time=1.4)
        g = Grille(cases=7, hauteur=24, largeur=3.2, haut=4.6, origine=RIGHT * 3.6 + DOWN * 0.4, y0=40)
        self.play(FadeIn(g.lignes(opacite=0.15)), FadeIn(g.axe_y(pas=4)), run_time=0.6)
        for x in range(7):
            h = 48 + (x % 3)
            for y in range(40, h - 3): self.add(g.bloc(x, y, "PIERRE"))
            for y in range(h - 3, h): self.add(g.bloc(x, y, "TERRE"))
            self.add(g.bloc(x, h, "HERBE"))
        sonde = Square(side_length=g.pas, stroke_color=ALERTE, stroke_width=3).move_to(g.centre(3, 63))
        yval = code("y = 63", 28, ALERTE).next_to(prog, DOWN, buff=0.6, aligned_edge=LEFT)
        verdict = code("get_block = AIR → on descend", 20, DOUX).next_to(yval, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(sonde), FadeIn(yval), FadeIn(verdict))
        self.next_section("tant que c'est de l'air, y = y - 1")
        for y in range(62, 47, -1):
            self.play(sonde.animate.move_to(g.centre(3, y)), Transform(yval, code(f"y = {y}", 28, ALERTE).move_to(yval, aligned_edge=LEFT)), run_time=0.22)
        self.next_section("get_block ≠ AIR : on s'arrête")
        self.play(sonde.animate.set_stroke(color=COULEURS["HERBE"]),
                  Transform(verdict, code("get_block = HERBE → stop", 20, COULEURS["HERBE"]).move_to(verdict, aligned_edge=LEFT)), run_time=0.6)
        self.play(FadeIn(phrase("le sol est à y = 48 : le premier bloc qui n'est pas de l'air", CIEL)))
        self.wait(1.8)
