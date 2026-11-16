# Étape 12, « perlin3d : creuser des grottes » : sur une tranche du monde, le
# bruit 3D donne un nombre par case ; là où il dépasse le seuil, on ne pose
# rien, et un trou apparaît. Plus le seuil baisse, plus les grottes grandissent.
# Sans code : le test et les diviseurs sont à l'élève.
#
#   capture.py anim anim/grottes.py LesGrottes -o img/outil-grottes.webp
from manim import *
from commun import *
from perlin import perlin2d


class LesGrottes(Scene):
    def construct(self):
        self.next_section("un nombre par case")
        g = Grille(cases=32, hauteur=16, largeur=9.6, haut=4.8, origine=DOWN * 0.3)

        def titre(t, couleur=WHITE):
            return texte(t, 28, couleur).to_edge(UP, buff=0.4)

        t = titre("une tranche du monde, sous la terre")
        self.play(FadeIn(g.lignes(opacite=0.12)), FadeIn(t), run_time=0.6)
        valeurs, cases = {}, VGroup()
        for y in range(16):
            for x in range(32):
                # Un coin du bruit choisi pour ses poches : plusieurs petites grottes
                # au seuil 0.3, qui grandissent et se rejoignent au seuil 0.1.
                v = perlin2d(x / 7 + 47.95, y / 5 + 2.22)
                valeurs[(x, y)] = v
                teinte = interpolate_color(ManimColor("#1e2a3a"), ManimColor(CIEL), (v + 0.7) / 1.4)
                cases.add(Square(side_length=g.pas, fill_color=teinte, fill_opacity=0.9, stroke_width=0).move_to(g.centre(x, y)))
        self.play(FadeIn(cases), run_time=1.2)
        # Trois cases lues à voix haute : une claire, une moyenne, une sombre.
        ordre = sorted(valeurs, key=valeurs.get)
        lues = VGroup()
        for (x, y) in (ordre[-1], ordre[len(ordre) // 2], ordre[0]):
            c = Square(side_length=g.pas, stroke_color=ALERTE, stroke_width=3).move_to(g.centre(x, y))
            e = code(f"{round(valeurs[(x, y)], 1) + 0.0:.1f}", 22, ALERTE).next_to(c, UP, buff=0.1)
            fond = BackgroundRectangle(e, color=FOND, fill_opacity=0.85, buff=0.06)
            lues.add(VGroup(c, fond, e))
        self.play(LaggedStart(*[FadeIn(m) for m in lues], lag_ratio=0.4), run_time=1.4)
        ph = phrase("perlin3d donne un nombre entre -1 et 1 à chaque case : clair, nombre élevé", CIEL)
        self.play(FadeIn(ph)); self.wait(1.6)

        def pierre(seuil):
            return VGroup(*[g.bloc(x, y, "PIERRE") for (x, y), v in valeurs.items() if v <= seuil])

        self.next_section("seuil 0.3 : au-dessus, on ne pose rien")
        t2 = titre("seuil : 0.3", ALERTE)
        trous = VGroup(*[Square(side_length=g.pas, stroke_color=ALERTE, stroke_width=1.5).move_to(g.centre(x, y)) for (x, y), v in valeurs.items() if v > 0.3])
        self.play(FadeOut(ph), FadeOut(lues), FadeOut(t), FadeIn(t2), run_time=0.6)
        self.play(Create(trous), run_time=0.9); self.wait(0.5)
        p = pierre(0.3)
        self.play(FadeIn(p), FadeOut(trous), FadeOut(cases), run_time=1.0)
        ph = phrase("les cases dont le nombre dépasse 0.3 restent vides : ce sont les grottes", ALERTE)
        self.play(FadeIn(ph)); self.wait(1.6)

        self.next_section("seuil 0.1 : des grottes plus grandes")
        self.play(FadeOut(ph), Transform(t2, titre("seuil : 0.1", ALERTE)), Transform(p, pierre(0.1)), run_time=1.0)
        self.play(FadeIn(phrase("seuil plus bas : plus de cases le dépassent, les grottes grandissent", CIEL)))
        self.wait(1.8)
