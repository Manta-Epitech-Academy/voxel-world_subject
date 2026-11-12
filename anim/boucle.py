# Étape 2, boîte à outils « La boucle for » et « Une boucle dans une boucle » :
# x compte de 0 à 9 et un bloc se pose à chaque tour ; puis une boucle dans
# l'autre, et pour chaque x tous les z : un carré.
#
#   capture.py anim anim/boucle.py LaBoucle -o img/outil-boucle.webp
#   capture.py anim anim/boucle.py LaDoubleBoucle -o img/outil-double-boucle.webp
from manim import *
from commun import *


class LaBoucle(Scene):
    def construct(self):
        self.next_section("x compte de 0 à 9")
        prog = bloc_code(["for x = 0, 9 do", "  set_block(x, 0, 0, PIERRE)", "end"], 28).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.8)
        self.play(Write(prog), run_time=1.2)
        g = Grille(cases=12, hauteur=3, largeur=9, haut=2.3, origine=DOWN * 1.2)
        self.play(FadeIn(g.lignes()), FadeIn(g.axe_x()), FadeIn(g.axe_y(etiquette="y")), run_time=0.8)
        valeur = code("x = 0", 30, ALERTE).next_to(prog, RIGHT, buff=1.2)
        self.play(FadeIn(valeur))
        surl = SurroundingRectangle(prog[1], color=ALERTE, buff=0.08)
        self.play(Create(surl), run_time=0.4)
        for x in range(10):
            nouveau = code(f"x = {x}", 30, ALERTE).move_to(valeur)
            self.play(Transform(valeur, nouveau), run_time=0.15)
            self.play(FadeIn(g.bloc(x, 0), scale=0.6), run_time=0.22)
        self.play(FadeOut(surl))
        self.play(FadeIn(phrase("dix tours, dix blocs : une ligne le long de x", CIEL)))
        self.wait(1.5)


class LaDoubleBoucle(Scene):
    def construct(self):
        self.next_section("pour chaque x, tous les z")
        prog = bloc_code(["for x = 0, 9 do", "  for z = 0, 9 do", "    set_block(x, 0, z, PIERRE)", "  end", "end"], 26).to_edge(UP, buff=0.4).to_edge(LEFT, buff=0.6)
        self.play(Write(prog), run_time=1.2)
        # Vue de dessus : x vers la droite, z vers le haut de l'image.
        g = Grille(cases=10, hauteur=10, largeur=4.2, haut=4.2, origine=RIGHT * 3 + DOWN * 0.5)
        self.play(FadeIn(g.lignes()), FadeIn(g.axe_x()), FadeIn(g.axe_y(etiquette="z")), run_time=0.8)
        vx = code("x = 0", 26, ALERTE).next_to(prog, DOWN, buff=0.5, aligned_edge=LEFT)
        vz = code("z = 0", 26, CIEL).next_to(vx, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(FadeIn(vx), FadeIn(vz))
        for x in range(10):
            self.play(Transform(vx, code(f"x = {x}", 26, ALERTE).move_to(vx)), run_time=0.1)
            colonne = VGroup()
            for z in range(10):
                colonne.add(g.bloc(x, z))
            if x < 2:
                for z in range(10):
                    self.play(Transform(vz, code(f"z = {z}", 26, CIEL).move_to(vz)), FadeIn(colonne[z], scale=0.6), run_time=0.09)
            else:
                self.play(Transform(vz, code("z = 0 … 9", 26, CIEL).move_to(vz)), LaggedStart(*[FadeIn(b, scale=0.6) for b in colonne], lag_ratio=0.1), run_time=0.35)
        self.play(FadeIn(phrase("10 × 10 = 100 blocs : un carré, posé ligne après ligne", CIEL)))
        self.wait(1.6)
