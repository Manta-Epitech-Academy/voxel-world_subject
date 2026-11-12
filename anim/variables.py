# Étape 3, « Les variables » : SOL est une boîte avec un nom ; on change sa
# valeur une fois, et les blocs qui l'utilisent suivent.
#
#   capture.py anim anim/variables.py LesVariables -o img/outil-variables.webp
from manim import *
from commun import *


class LesVariables(Scene):
    def construct(self):
        self.next_section("SOL = 20")
        prog = bloc_code(["local SOL = 20", "set_block(64, SOL, 64, HERBE)", "set_block(64, SOL - 1, 64, TERRE)"], 26).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.6)
        self.play(Write(prog), run_time=1.4)
        boite = RoundedRectangle(width=2.2, height=1.1, corner_radius=0.15, stroke_color=ALERTE, fill_color=PANNEAU, fill_opacity=1).to_edge(RIGHT, buff=1.2).shift(UP * 1.6)
        nom = Text("SOL", font="DejaVu Sans Mono", font_size=22, color=DOUX).next_to(boite, UP, buff=0.1)
        val = code("20", 34, ALERTE).move_to(boite)
        self.play(FadeIn(boite), FadeIn(nom), FadeIn(val))
        g = Grille(cases=5, hauteur=18, largeur=2.2, haut=4.0, origine=DOWN * 1.0 + RIGHT * 0.6, y0=12)
        self.play(FadeIn(g.lignes(opacite=0.2)), FadeIn(g.axe_y(pas=2)), run_time=0.6)
        herbe = g.bloc(2, 20, "HERBE"); terre = g.bloc(2, 19, "TERRE")
        e1 = code("SOL = 20", 18, COULEURS["HERBE"]).next_to(herbe, RIGHT, buff=0.25).shift(UP * 0.1)
        e2 = code("SOL - 1 = 19", 18, COULEURS["TERRE"]).next_to(terre, RIGHT, buff=0.25).shift(DOWN * 0.1)
        self.play(FadeIn(herbe), FadeIn(e1), run_time=0.6)
        self.play(FadeIn(terre), FadeIn(e2), run_time=0.6)
        ph = phrase("SOL vaut 20 : l'herbe se pose à 20, la terre juste dessous", CIEL)
        self.play(FadeIn(ph))
        self.wait(1.4)

        self.next_section("on change SOL une seule fois")
        self.play(Transform(prog[0], code("local SOL = 26", 26).move_to(prog[0], aligned_edge=LEFT)),
                  Transform(val, code("26", 34, ALERTE).move_to(boite)), run_time=0.8)
        herbe2 = g.bloc(3, 26, "HERBE"); terre2 = g.bloc(3, 25, "TERRE")
        self.play(Transform(herbe, herbe2), Transform(terre, terre2),
                  Transform(e1, code("SOL = 26", 18, COULEURS["HERBE"]).next_to(herbe2, RIGHT, buff=0.25).shift(UP * 0.1)),
                  Transform(e2, code("SOL - 1 = 25", 18, COULEURS["TERRE"]).next_to(terre2, RIGHT, buff=0.25).shift(DOWN * 0.1)), run_time=1.2)
        self.play(FadeOut(ph), FadeIn(phrase("un seul nombre changé, et tout le code qui utilise SOL suit", ALERTE)))
        self.wait(1.8)
