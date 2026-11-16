# Étape 11, « if : faire un choix » : d'abord l'idée, trois questions posées
# dans l'ordre à un nombre ; puis les mêmes questions écrites en Lua, avec if,
# elseif et else. Et « Choisir le bloc avant de le poser » : au-dessus d'un
# seuil, le bloc du dessus change. Sans code : le test est à l'élève.
#
#   capture.py anim anim/choix.py LeChoix -o img/outil-if.webp
#   capture.py anim anim/choix.py LeBlocDuDessus -o img/outil-dessus.webp
import math
from manim import *
from commun import *


class LeChoix(Scene):
    def construct(self):
        def boite(t, pos, largeur=4.2, couleur=DOUX):
            r = RoundedRectangle(width=largeur, height=0.9, corner_radius=0.15, stroke_color=couleur, stroke_width=3, fill_color=PANNEAU, fill_opacity=1).move_to(pos)
            return VGroup(r, texte(t, 24).move_to(pos))

        ys = (1.9, 0.2, -1.5)
        q = [boite("plus petit que 20 ?", LEFT * 1.6 + UP * ys[0]), boite("plus grand que 35 ?", LEFT * 1.6 + UP * ys[1]), boite("sinon", LEFT * 1.6 + UP * ys[2])]
        r = [boite("« bas »", RIGHT * 4.4 + UP * ys[0], 2.6), boite("« haut »", RIGHT * 4.4 + UP * ys[1], 2.6), boite("« au milieu »", RIGHT * 4.4 + UP * ys[2], 2.6)]
        oui = [Arrow(q[i].get_right(), r[i].get_left(), buff=0.12, color=DOUX, stroke_width=3, max_tip_length_to_length_ratio=0.1) for i in range(3)]
        non = [Arrow(q[i].get_bottom(), q[i + 1].get_top(), buff=0.08, color=DOUX, stroke_width=3, max_tip_length_to_length_ratio=0.25) for i in range(2)]
        e_oui = [texte("oui", 20, DOUX).next_to(oui[i], UP, buff=0.08) for i in range(2)]
        e_non = [texte("non", 20, DOUX).next_to(non[i], RIGHT, buff=0.12) for i in range(2)]
        self.next_section("deux questions, posées dans l'ordre")
        self.play(*[FadeIn(m) for m in q + r + oui + non + e_oui + e_non], run_time=1.2)
        place = [m.get_left() + LEFT * 1.0 for m in q]
        jeton_fond = RoundedRectangle(width=1.6, height=0.62, corner_radius=0.3, fill_color=ALERTE, fill_opacity=1, stroke_width=0)
        jeton_txt = code("h = 30", 20, FOND)
        jeton = VGroup(jeton_fond, jeton_txt).move_to(place[0] + UP * 1.3)
        self.play(FadeIn(jeton))

        def essai(h, reponses, section):
            self.next_section(section)
            self.play(jeton.animate.move_to(place[0] + UP * 1.3), run_time=0.4)
            self.play(Transform(jeton_txt, code(f"h = {h}", 20, FOND).move_to(jeton_fond)), run_time=0.4)
            allumes, elu = [], 2
            for i, rep in enumerate(reponses):
                self.play(jeton.animate.move_to(place[i]), q[i][0].animate.set_stroke(color=ALERTE), run_time=0.5)
                allumes.append(q[i][0])
                self.wait(0.4)
                if rep:
                    self.play(oui[i].animate.set_color(VERT), e_oui[i].animate.set_color(VERT), run_time=0.4)
                    allumes += [oui[i], e_oui[i]]
                    elu = i
                    break
                self.play(non[i].animate.set_color(ERREUR), e_non[i].animate.set_color(ERREUR), run_time=0.4)
                allumes += [non[i], e_non[i]]
            else:
                self.play(jeton.animate.move_to(place[2]), q[2][0].animate.set_stroke(color=ALERTE), oui[2].animate.set_color(VERT), run_time=0.5)
                allumes += [q[2][0], oui[2]]
            self.play(r[elu][0].animate.set_stroke(color=VERT).set_fill(VERT, opacity=0.25), run_time=0.4)
            self.wait(1.0)
            self.play(*[m.animate.set_color(DOUX) for m in allumes if not isinstance(m, RoundedRectangle)],
                      *[m.animate.set_stroke(color=DOUX) for m in allumes if isinstance(m, RoundedRectangle)],
                      r[elu][0].animate.set_stroke(color=DOUX).set_fill(PANNEAU, opacity=1), run_time=0.4)

        essai(30, [False, False], "h = 30 : non, non, donc sinon")
        essai(12, [True], "h = 12 : oui à la première question")
        essai(40, [False, True], "h = 40 : oui à la deuxième")
        ph = phrase("les questions sont posées dans l'ordre, et le premier « oui » décide", CIEL)
        self.play(FadeIn(ph)); self.wait(1.6)

        # Les mêmes questions, écrites en Lua : chaque boîte devient sa ligne.
        self.next_section("les mêmes questions, écrites avec if, elseif et else")
        prog = bloc_code(["h = 40", "if h < 20 then", '  print("bas")', "elseif h > 35 then", '  print("haut")', "else", '  print("au milieu")', "end"], 24).to_edge(LEFT, buff=0.8).shift(UP * 0.3)
        self.play(FadeOut(ph), *[FadeOut(m) for m in oui + non + e_oui + e_non], run_time=0.5)
        # Une question après l'autre, pour qu'on voie laquelle devient quelle ligne.
        self.play(*[FadeOut(m[0]) for m in q + r], FadeOut(jeton_fond), FadeTransform(jeton_txt, prog[0]), run_time=0.7)
        for i in range(3):
            self.play(FadeTransform(q[i][1], prog[2 * i + 1]), FadeTransform(r[i][1], prog[2 * i + 2]), run_time=1.0)
            self.wait(0.3)
        self.play(FadeIn(prog[7]), run_time=0.4)
        self.wait(0.8)
        hval = code("h = 40", 34, ALERTE).to_edge(RIGHT, buff=1.4).shift(UP * 2.2)
        self.play(FadeIn(hval))

        def essai_code(h, tests, elu, sortie, section):
            self.next_section(section)
            self.play(Transform(hval, code(f"h = {h}", 34, ALERTE).move_to(hval)),
                      Transform(prog[0], code(f"h = {h}", 24).move_to(prog[0], aligned_edge=LEFT)), run_time=0.5)
            for ligne, verdict in tests:
                cadre = SurroundingRectangle(prog[ligne], color=ALERTE, buff=0.06)
                v = texte(verdict, 24, VERT if verdict == "vrai" else ERREUR).next_to(cadre, RIGHT, buff=0.3)
                self.play(Create(cadre), FadeIn(v), run_time=0.5); self.wait(0.5)
                self.play(FadeOut(cadre), FadeOut(v), run_time=0.3)
            cadre = SurroundingRectangle(prog[elu], color=VERT, buff=0.06)
            ecrit = code(sortie, 28, VERT).next_to(hval, DOWN, buff=0.8)
            self.play(Create(cadre), FadeIn(ecrit), run_time=0.6); self.wait(1.0)
            self.play(FadeOut(cadre), FadeOut(ecrit), run_time=0.3)

        essai_code(30, [(1, "faux"), (3, "faux")], 6, '"au milieu"', "en Lua, h = 30 : ni bas ni haut, donc else")
        essai_code(12, [(1, "vrai")], 2, '"bas"', "en Lua, h = 12 : la première condition est vraie")
        essai_code(40, [(1, "faux"), (3, "vrai")], 4, '"haut"', "en Lua, h = 40 : la deuxième")
        self.play(FadeIn(phrase("if teste dans l'ordre, et exécute le premier bloc dont la condition est vraie", CIEL)))
        self.wait(1.8)


class LeBlocDuDessus(Scene):
    def construct(self):
        self.next_section("le bloc du dessus dépend de la hauteur")
        g = Grille(cases=28, hauteur=28, largeur=4.8, haut=4.8, origine=RIGHT * 2.2 + DOWN * 0.2, y0=10)
        self.play(FadeIn(g.lignes(opacite=0.12)), run_time=0.5)
        seuil = DashedLine(g.coin(0, 32), g.coin(28, 32), color=ALERTE, stroke_width=2.5)
        etiq = texte("seuil", 22, ALERTE).next_to(seuil, RIGHT, buff=0.15)
        self.play(Create(seuil), FadeIn(etiq))

        def legende(type_, t, pos):
            c = Square(side_length=0.45, fill_color=COULEURS[type_], fill_opacity=1, stroke_color=FOND, stroke_width=1)
            return VGroup(c, texte(t, 24).next_to(c, RIGHT, buff=0.25)).move_to(pos, aligned_edge=LEFT)

        haut = legende("NEIGE", "au-dessus du seuil : NEIGE", LEFT * 6.3 + UP * 1.0)
        bas = legende("HERBE", "sous le seuil : HERBE", LEFT * 6.3 + UP * 0.1)
        self.play(FadeIn(haut), FadeIn(bas))
        haut.set_opacity(0.3)
        hauteurs = [round(26 + 9 * math.sin(i / 3.5)) for i in range(28)]
        etat = "HERBE"
        for x, h in enumerate(hauteurs):
            dessus = "NEIGE" if h >= 32 else "HERBE"
            if dessus != etat:
                self.next_section("au-dessus du seuil : NEIGE" if dessus == "NEIGE" else "sous le seuil : HERBE")
                (haut if dessus == "NEIGE" else bas).set_opacity(1)
                (bas if dessus == "NEIGE" else haut).set_opacity(0.3)
                etat = dessus
            col = VGroup(*[g.bloc(x, y, "PIERRE") for y in range(10, h - 3)] + [g.bloc(x, y, "TERRE") for y in range(h - 3, h)])
            self.play(FadeIn(col), run_time=0.14)
            self.play(FadeIn(g.bloc(x, h, dessus), scale=0.6), run_time=0.16)
        haut.set_opacity(1); bas.set_opacity(1)
        self.play(FadeIn(phrase("au-dessus du seuil, le bloc du dessus change ; ailleurs, il reste le même", CIEL)))
        self.wait(1.8)
