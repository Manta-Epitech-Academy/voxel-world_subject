# Étape 9, « if : faire un choix » et « Choisir le bloc du dessus » : une
# condition vraie ou fausse décide ce qui est exécuté ; puis le bloc du dessus
# qui dépend de la hauteur.
#
#   capture.py anim anim/choix.py LeChoix -o img/outil-if.webp
#   capture.py anim anim/choix.py LeBlocDuDessus -o img/outil-dessus.webp
from manim import *
from commun import *


class LeChoix(Scene):
    def construct(self):
        prog = bloc_code(["local h = 30", "if h < 20 then", '  print("bas")', "elseif h > 35 then", '  print("haut")', "else", '  print("au milieu")', "end"], 24).to_edge(LEFT, buff=0.8).shift(UP * 0.3)
        self.play(Write(prog), run_time=1.6)
        hval = code("h = 30", 34, ALERTE).to_edge(RIGHT, buff=1.4).shift(UP * 2.2)
        self.play(FadeIn(hval))

        def essai(h, tests, elu, texte, section):
            self.next_section(section)
            self.play(Transform(hval, code(f"h = {h}", 34, ALERTE).move_to(hval)), run_time=0.5)
            resultat = None
            for ligne, verdict in tests:
                cadre = SurroundingRectangle(prog[ligne], color=ALERTE, buff=0.06)
                v = Text(verdict, font="DejaVu Sans", font_size=24, color=(COULEURS["HERBE"] if verdict == "vrai" else ERREUR)).next_to(cadre, RIGHT, buff=0.3)
                self.play(Create(cadre), FadeIn(v), run_time=0.5); self.wait(0.5)
                self.play(FadeOut(cadre), FadeOut(v), run_time=0.3)
            cadre = SurroundingRectangle(prog[elu], color=COULEURS["HERBE"], buff=0.06)
            sortie = code(texte, 28, COULEURS["HERBE"]).next_to(hval, DOWN, buff=0.8)
            self.play(Create(cadre), FadeIn(sortie), run_time=0.6); self.wait(1.0)
            self.play(FadeOut(cadre), FadeOut(sortie), run_time=0.3)

        essai(30, [(1, "faux"), (3, "faux")], 6, '"au milieu"', "h = 30 : ni bas ni haut, donc else")
        essai(12, [(1, "vrai")], 2, '"bas"', "h = 12 : la première condition est vraie")
        essai(40, [(1, "faux"), (3, "vrai")], 4, '"haut"', "h = 40 : la deuxième")
        self.play(FadeIn(phrase("if teste dans l'ordre, et exécute le premier bloc dont la condition est vraie", CIEL)))
        self.wait(1.8)


class LeBlocDuDessus(Scene):
    def construct(self):
        self.next_section("dessus = HERBE, sauf si h ≥ 34")
        prog = bloc_code(["local dessus = HERBE", "if h >= 34 then", "  dessus = NEIGE", "end", "set_block(x, h, z, dessus)"], 24).to_edge(LEFT, buff=0.7).shift(UP * 0.4)
        self.play(Write(prog), run_time=1.4)
        g = Grille(cases=14, hauteur=40, largeur=6.2, haut=4.6, origine=RIGHT * 3.2 + DOWN * 0.4)
        self.play(FadeIn(g.lignes(opacite=0.12)), FadeIn(g.axe_y(pas=8)), run_time=0.6)
        seuil = DashedLine(g.coin(0, 34), g.coin(14, 34), color=ALERTE, stroke_width=2)
        etiq = code("34", 16, ALERTE).next_to(seuil, RIGHT, buff=0.1)
        self.play(Create(seuil), FadeIn(etiq))
        import math
        hauteurs = [round(24 + 10 * math.sin(i / 2.2)) for i in range(14)]
        for x, h in enumerate(hauteurs):
            dessus = "NEIGE" if h >= 34 else "HERBE"
            cadre = SurroundingRectangle(prog[2 if dessus == "NEIGE" else 0], color=COULEURS[dessus] if dessus == "HERBE" else ALERTE, buff=0.05)
            col = VGroup(*[g.bloc(x, y, "TERRE") for y in range(h - 3, h)] + [g.bloc(x, y, "PIERRE") for y in range(1, h - 3)] + [g.bloc(x, 0, "BEDROCK")])
            self.play(FadeIn(col), Create(cadre), run_time=0.25)
            self.play(FadeIn(g.bloc(x, h, dessus), scale=0.6), FadeOut(cadre), run_time=0.25)
        self.play(FadeIn(phrase("au-dessus de 34, le dessus devient NEIGE ; ailleurs, il reste HERBE", CIEL)))
        self.wait(1.8)
