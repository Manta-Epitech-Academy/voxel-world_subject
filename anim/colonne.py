# Étape 3, « Une boucle vers le haut » : la même boucle for, mais sur y, et
# une colonne monte bloc par bloc. Puis étape 4, « Penser en colonnes » : une
# colonne, c'est une pile avec ses couches, et le monde en est fait.
#
#   capture.py anim anim/colonne.py LaColonne -o img/outil-colonne.webp
#   capture.py anim anim/colonne.py LesColonnes -o img/outil-colonnes.webp
from manim import *
from commun import *


class LaColonne(Scene):
    def construct(self):
        self.next_section("y monte de 1 à 16")
        prog = bloc_code(["for y = 1, 16 do", "  set_block(64, y, 64, PIERRE)", "end"], 28).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.8)
        self.play(Write(prog), run_time=1.2)
        g = Grille(cases=5, hauteur=18, largeur=2.4, haut=4.6, origine=RIGHT * 2.5 + DOWN * 0.6)
        self.play(FadeIn(g.lignes(opacite=0.2)), FadeIn(g.axe_y(pas=2)), run_time=0.6)
        valeur = code("y = 1", 30, ALERTE).next_to(prog, DOWN, buff=0.6, aligned_edge=LEFT)
        self.play(FadeIn(valeur))
        for y in range(1, 17):
            self.play(Transform(valeur, code(f"y = {y}", 30, ALERTE).move_to(valeur, aligned_edge=LEFT)),
                      FadeIn(g.bloc(2, y, "PIERRE"), scale=0.6), run_time=0.18)
        self.play(FadeIn(phrase("seize tours : une colonne de pierre, de y = 1 à y = 16", CIEL)))
        self.wait(1.6)


class LesColonnes(Scene):
    def construct(self):
        self.next_section("une colonne : une pile avec ses couches")
        g = Grille(cases=16, hauteur=24, largeur=10, haut=4.6, origine=DOWN * 0.3)
        self.play(FadeIn(g.lignes(opacite=0.15)), FadeIn(g.axe_x(pas=2)), FadeIn(g.axe_y(pas=4)), run_time=0.6)
        couches = [(0, "BEDROCK")] + [(y, "PIERRE") for y in range(1, 17)] + [(y, "TERRE") for y in range(17, 20)] + [(20, "HERBE")]
        x = 7
        col = VGroup(*[g.bloc(x, y, t) for y, t in couches])
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in col], lag_ratio=0.06), run_time=2)
        etiq = VGroup(
            code("HERBE", 16, COULEURS["HERBE"]).next_to(g.centre(x, 20), RIGHT, buff=0.6),
            code("TERRE ×3", 16, COULEURS["TERRE"]).next_to(g.centre(x, 18), RIGHT, buff=0.6),
            code("PIERRE", 16, COULEURS["PIERRE"]).next_to(g.centre(x, 9), RIGHT, buff=0.6),
            code("BEDROCK", 16, DOUX).next_to(g.centre(x, 0), RIGHT, buff=0.6),
        )
        self.play(FadeIn(etiq))
        ph = phrase("une colonne : la bedrock, la pierre, 3 terre, l'herbe, posée en (x, z)", CIEL)
        self.play(FadeIn(ph)); self.wait(1.6)

        self.next_section("la double boucle pose toutes les autres")
        self.play(FadeOut(etiq), FadeOut(ph))
        prog = bloc_code(["for x = 0, TAILLE - 1 do", "  for z = 0, TAILLE - 1 do", "    -- la colonne, en x et z", "  end", "end"], 20).to_corner(UL, buff=0.4)
        self.play(FadeIn(prog))
        autres = VGroup()
        for cx in range(16):
            if cx == x: continue
            autres.add(VGroup(*[g.bloc(cx, y, t) for y, t in couches]))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in autres], lag_ratio=0.08), run_time=2.2)
        self.play(FadeIn(phrase("si tu sais construire une colonne, la double boucle construit les 16 384 autres", ALERTE)))
        self.wait(1.8)
