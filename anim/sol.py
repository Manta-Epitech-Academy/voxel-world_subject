# Étape 7, « get_block et while : trouver le sol » : une sonde part du ciel et
# descend d'une case tant que la case est de l'air. Sans code : le code du
# while est dans la boîte à outils, l'animation montre l'idée.
#
#   capture.py anim anim/sol.py TrouverLeSol -o img/outil-sol.webp
from manim import *
from commun import *


class TrouverLeSol(Scene):
    def construct(self):
        self.next_section("on part du ciel")
        g = Grille(cases=7, hauteur=24, largeur=3.2, haut=4.6, origine=RIGHT * 3.0 + DOWN * 0.3, y0=40)
        self.play(FadeIn(g.lignes(opacite=0.15)), FadeIn(g.axe_y(pas=4)), run_time=0.6)
        for x in range(7):
            h = 48 + (x % 3)
            for y in range(40, h - 3): self.add(g.bloc(x, y, "PIERRE"))
            for y in range(h - 3, h): self.add(g.bloc(x, y, "TERRE"))
            self.add(g.bloc(x, h, "HERBE"))
        sonde = Square(side_length=g.pas, stroke_color=ALERTE, stroke_width=3).move_to(g.centre(3, 63))
        titre = texte("get_block regarde une case :", 22, DOUX).move_to(LEFT * 3.4 + UP * 2.0)
        vignette = Square(side_length=0.9, stroke_color=ALERTE, stroke_width=3).next_to(titre, DOWN, buff=0.35)
        contenu = code("AIR", 22, DOUX).next_to(vignette, RIGHT, buff=0.3)
        verdict = texte("de l'air : on descend", 30, CIEL).next_to(vignette, DOWN, buff=0.5)
        yval = code("y = 63", 30, ALERTE).next_to(verdict, DOWN, buff=0.45)
        self.play(FadeIn(sonde), FadeIn(titre), FadeIn(vignette), FadeIn(contenu), FadeIn(yval))
        self.wait(0.6)
        self.next_section("tant que c'est de l'air, on descend d'une case")
        self.play(FadeIn(verdict))
        for y in range(62, 47, -1):
            self.play(sonde.animate.move_to(g.centre(3, y)), Transform(yval, code(f"y = {y}", 30, ALERTE).move_to(yval)), run_time=0.24)
        self.next_section("de l'herbe : on s'arrête")
        self.play(sonde.animate.set_stroke(color=VERT),
                  vignette.animate.set_fill(VERT, opacity=0.95).set_stroke(color=VERT),
                  FadeOut(contenu), FadeIn(code("HERBE", 22, VERT).move_to(contenu, aligned_edge=LEFT)),
                  FadeOut(verdict), FadeIn(texte("de l'herbe : on s'arrête", 30, VERT).move_to(verdict)), run_time=0.7)
        self.play(FadeIn(phrase("le sol est à y = 48 : le premier bloc qui n'est pas de l'air", CIEL)))
        self.wait(1.8)
