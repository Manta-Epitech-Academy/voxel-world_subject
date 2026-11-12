# Étape 10, « perlin3d : creuser des grottes » : sur une tranche du monde, le
# bruit 3D donne un nombre par case ; là où il dépasse le seuil, on ne pose
# rien, et un trou apparaît. Plus le seuil baisse, plus les grottes grandissent.
#
#   capture.py anim anim/grottes.py LesGrottes -o img/outil-grottes.webp
import math, random
from manim import *
from commun import *
from perlin import perlin2d


def perlin3d_tranche(x, y, z=40):
    # Une tranche à z fixe : un bruit 2D (x, y) joue le rôle de perlin3d(x, y, z) sur cette tranche.
    return perlin2d(x + 0.37 * z, y + 0.11 * z)


class LesGrottes(Scene):
    def construct(self):
        self.next_section("un nombre par case")
        prog = bloc_code(["if perlin3d(x / 16, y / 10, z / 16) > 0.3 then", "  -- grotte : on ne pose rien", "else", "  set_block(x, y, z, PIERRE)", "end"], 20).to_corner(UL, buff=0.4)
        self.play(Write(prog), run_time=1.2)
        g = Grille(cases=32, hauteur=16, largeur=8.4, haut=4.2, origine=DOWN * 1.0 + RIGHT * 0.6)
        self.play(FadeIn(g.lignes(opacite=0.12)), FadeIn(g.axe_y(pas=4)), run_time=0.5)
        valeurs = {}
        cases = VGroup()
        for y in range(16):
            for x in range(32):
                v = perlin3d_tranche(x / 16, y / 10)
                valeurs[(x, y)] = v
                teinte = interpolate_color(ManimColor("#1e2a3a"), ManimColor(CIEL), (v + 0.7) / 1.4)
                c = Square(side_length=g.pas, fill_color=teinte, fill_opacity=0.9, stroke_width=0).move_to(g.centre(x, y))
                cases.add(c)
        self.play(FadeIn(cases), run_time=1.2)
        ph = phrase("perlin3d donne un nombre entre -1 et 1 à chaque case : clair, c'est haut", CIEL)
        self.play(FadeIn(ph)); self.wait(1.4)

        def creuser(seuil, section, texte):
            self.next_section(section)
            pierre = VGroup(); vide = VGroup()
            for (x, y), v in valeurs.items():
                (vide if v > seuil else pierre).add(g.bloc(x, y, "PIERRE"))
            return pierre, vide

        pierre, vide = creuser(0.3, "seuil 0,3 : au-dessus, on ne pose rien", "")
        self.play(FadeOut(ph), FadeIn(pierre), run_time=1.0)
        trous = VGroup(*[Square(side_length=g.pas, stroke_color=ALERTE, stroke_width=1.5).move_to(c.get_center()) for c in vide])
        self.play(Create(trous), run_time=0.8); self.wait(0.4)
        self.play(FadeOut(trous), FadeOut(cases), run_time=0.5)
        ph = phrase("seuil 0,3 : les cases au-dessus restent vides, ce sont les grottes", ALERTE)
        self.play(FadeIn(ph)); self.wait(1.4)

        pierre2, vide2 = creuser(0.1, "seuil 0,1 : des grottes plus grandes", "")
        self.play(FadeOut(ph), Transform(pierre, pierre2), run_time=1.0)
        self.play(FadeIn(phrase("seuil 0,1 : plus de cases dépassent, les grottes grandissent", CIEL)))
        self.wait(1.8)
