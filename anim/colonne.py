# Étape 3, « Une boucle vers le haut » : la même boucle for, mais sur y, et un
# poteau monte bloc par bloc. Puis étape 4, « Penser en colonnes » : une
# colonne, c'est une pile avec ses couches, et le monde en est fait. Les
# boucles sont montrées sans code, par des compteurs à rouleaux.
#
#   capture.py anim anim/colonne.py LePoteau -o img/outil-poteau.webp --fps 30
#   capture.py anim anim/colonne.py LesColonnes -o img/outil-colonnes.webp --fps 30
from manim import *
from commun import *


class LePoteau(Scene):
    def construct(self):
        self.next_section("y monte de 5 à 12")
        tours = ValueTracker(0)
        # Le compteur passe au y suivant pendant la fin de chaque tour.
        b = Compteur("y", lambda: 5 + roule(min(tours.get_value(), 7.6)), chiffres=2).scale(1.2).move_to(LEFT * 3.2 + UP * 1.2)
        g = Grille(cases=5, hauteur=16, largeur=2.4, haut=4.6, origine=RIGHT * 2.5 + DOWN * 0.4)
        tour = always_redraw(lambda: texte(f"tour {min(int(tours.get_value() + 1e-6), 7) + 1} sur 8", 30).next_to(b.fenetre, DOWN, buff=0.6))
        geste = texte("à chaque tour : un bloc, posé en y", 22, DOUX).next_to(tour, DOWN, buff=0.25)
        blocs = VGroup(*[g.bloc(2, y, "BOIS", 1).set_stroke(BLANC, 1) for y in range(5, 13)])

        def poser(m):
            t = tours.get_value()
            for k, bloc in enumerate(m):
                a = min(1, max(0, (t - k) / 0.5))
                bloc.set_fill(opacity=a).set_stroke(opacity=a)

        blocs.add_updater(poser)
        poser(blocs)
        self.add(b)
        self.play(FadeIn(g.lignes(opacite=0.2)), FadeIn(g.axe_y(pas=2)), FadeIn(tour), FadeIn(geste), run_time=0.9)
        self.add(blocs)
        self.wait(0.4)
        self.play(tours.animate.set_value(8), run_time=6.4, rate_func=linear)
        self.play(FadeIn(phrase("la même boucle, mais sur y : un poteau qui monte, de y = 5 à y = 12", CIEL)))
        self.wait(1.6)


class LesColonnes(Scene):
    def construct(self):
        self.next_section("une colonne : une pile avec ses couches")
        g = Grille(cases=16, hauteur=24, largeur=10, haut=4.6, origine=DOWN * 0.3 + RIGHT * 1.2)
        self.play(FadeIn(g.lignes(opacite=0.15)), FadeIn(g.axe_x(pas=2)), FadeIn(g.axe_y(pas=4)), run_time=0.6)
        couches = [(0, "BEDROCK")] + [(y, "PIERRE") for y in range(1, 17)] + [(y, "TERRE") for y in range(17, 20)] + [(20, "HERBE")]
        x_deja = 7
        col = VGroup(*[g.bloc(x_deja, y, t) for y, t in couches])
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in col], lag_ratio=0.06), run_time=2)
        etiq = VGroup(
            code("HERBE", 16, COULEURS["HERBE"]).next_to(g.centre(x_deja, 20), RIGHT, buff=0.6),
            code("TERRE ×3", 16, COULEURS["TERRE"]).next_to(g.centre(x_deja, 18), RIGHT, buff=0.6),
            code("PIERRE", 16, COULEURS["PIERRE"]).next_to(g.centre(x_deja, 9), RIGHT, buff=0.6),
            code("BEDROCK", 16, DOUX).next_to(g.centre(x_deja, 0), RIGHT, buff=0.6),
        )
        self.play(FadeIn(etiq))
        ph = phrase("une colonne : la bedrock, la pierre, 3 terre, l'herbe, posée en (x, z)", CIEL)
        self.play(FadeIn(ph)); self.wait(1.6)

        self.next_section("la double boucle pose toutes les autres")
        self.play(FadeOut(etiq), FadeOut(ph))
        # Les deux compteurs de l'étape 2. Vu de côté, un tour de x pose une
        # colonne ; z fait ses dix tours pour les colonnes derrière elle.
        tours = ValueTracker(0)
        fin = 16 * 10 - 0.4

        def z():
            return roule(min(tours.get_value(), fin)) % 10

        def x():
            v = roule(min(tours.get_value(), fin))
            return v // 10 + max(0, v % 10 - 9)

        rx = Compteur("x", x, chiffres=2, legende=("la boucle", "extérieure"))
        rz = Compteur("z", z, couleur=CIEL, legende=("la boucle", "intérieure"))
        duo = VGroup(rx, rz).arrange(RIGHT, buff=0.45, aligned_edge=DOWN).move_to(LEFT * 3.9 + UP * 0.9)
        # La colonne déjà posée est reposée au même endroit : rien ne change.
        autres = VGroup(*[VGroup(*[g.bloc(cx, y, t) for y, t in couches]) for cx in range(16)])

        def poser(m):
            t = tours.get_value()
            for cx, colonne in enumerate(m):
                a = 1 if cx == x_deja else min(1, max(0, (t - 10 * cx) / 0.5))
                for bloc in colonne:
                    bloc.set_fill(opacity=0.95 * a).set_stroke(opacity=a)

        autres.add_updater(poser)
        poser(autres)
        self.add(duo)
        self.remove(col)
        self.add(autres)
        # Le premier x lentement, pour lire z ; puis de plus en plus vite.
        self.play(tours.animate.set_value(10), run_time=4.5, rate_func=linear)
        a = (10 / 4.5) * 10 / 150
        self.play(tours.animate.set_value(160), run_time=10, rate_func=lambda u: a * u + (1 - a) * u * u)
        self.play(FadeIn(phrase("si tu sais construire une colonne, la double boucle construit toutes les autres", ALERTE)))
        self.wait(1.8)
