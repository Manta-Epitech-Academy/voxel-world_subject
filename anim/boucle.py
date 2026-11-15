# Étape 2, boîte à outils « La boucle for » et « Une boucle dans une boucle » :
# x compte de 0 à 9 et un bloc se pose à chaque tour ; puis une boucle dans
# l'autre, et pour chaque x tous les z : un carré. Chaque boucle est montrée
# par un compteur à rouleaux, comme un compteur kilométrique.
#
#   capture.py anim anim/boucle.py LaBoucle -o img/outil-boucle.webp --fps 30
#   capture.py anim anim/boucle.py LaDoubleBoucle -o img/outil-double-boucle.webp --fps 60
from manim import *
from commun import *


class LaBoucle(Scene):
    def construct(self):
        self.next_section("x compte de 0 à 9")
        prog = bloc_code(["for x = 0, 9 do", "  set_block(x, 0, 0, PIERRE)", "end"], 28).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.8)
        self.play(Write(prog), run_time=1.2)
        g = Grille(cases=12, hauteur=3, largeur=9, haut=2.3, origine=DOWN * 1.2)
        tours = ValueTracker(0)
        rx = Compteur("x", tours.get_value)
        rx.next_to(prog, RIGHT, buff=1.4).align_to(prog, UP)
        self.add(rx)
        self.play(FadeIn(g.lignes()), FadeIn(g.axe_x()), FadeIn(g.axe_y(etiquette="y")), run_time=0.8)
        surl = SurroundingRectangle(prog[1], color=ALERTE, buff=0.08)
        self.play(Create(surl), run_time=0.4)
        for x in range(10):
            if x:
                self.play(tours.animate.set_value(x), run_time=0.35)
            self.play(FadeIn(g.bloc(x, 0), scale=0.6), run_time=0.22)
        self.play(FadeOut(surl))
        self.play(FadeIn(phrase("dix tours, dix blocs : une ligne le long de x", CIEL)))
        self.wait(1.5)


class LaDoubleBoucle(Scene):
    def construct(self):
        # Un seul nombre de tours pour tout : z avance de 1 à chaque tour, x
        # quand z passe de 9 à 0. Le rouleau de z tourne dix fois plus vite.
        tours = ValueTracker(0)

        def z():
            return roule(min(tours.get_value(), 99.6)) % 10

        def x():
            v = roule(min(tours.get_value(), 99.6))
            return v // 10 + max(0, v % 10 - 9)

        rx = Compteur("x", x, legende=("la boucle", "extérieure"))
        rz = Compteur("z", z, couleur=CIEL, legende=("la boucle", "intérieure"))
        duo = VGroup(rx, rz).arrange(RIGHT, buff=1.1).scale(1.3).move_to(LEFT * 3.2 + UP * 0.5)
        # Vue de dessus : x vers la droite, z vers le haut de l'image.
        g = Grille(cases=10, hauteur=10, largeur=4.2, haut=4.2, origine=RIGHT * 3 + DOWN * 0.3)
        blocs = VGroup(*[g.bloc(k // 10, k % 10) for k in range(100)])

        def poser(m):
            # Le bloc du tour k apparaît pendant la première moitié de ce tour.
            t = tours.get_value()
            for k, b in enumerate(m):
                a = min(1, max(0, (t - k) / 0.5))
                b.set_fill(opacity=0.95 * a).set_stroke(opacity=a)

        blocs.add_updater(poser)
        poser(blocs)
        # add, pas FadeIn : les caches du compteur, couleur du fond, feraient
        # des fantômes sombres pendant le fondu.
        self.add(duo)
        self.play(FadeIn(g.lignes()), FadeIn(g.axe_x()), FadeIn(g.axe_y(etiquette="z")), run_time=0.9)
        self.add(blocs)
        note = texte("quand z a fait tous ses tours, x augmente de 1", 21, DOUX).next_to(VGroup(rx.legende, rz.legende), DOWN, buff=0.5)
        self.play(FadeIn(note))

        self.next_section("x vaut 0 : z passe de 0 à 9")
        self.play(tours.animate.set_value(10), run_time=5.5, rate_func=linear)
        self.next_section("x augmente de 1, et z recommence à 0")
        # Même vitesse au départ, puis de plus en plus vite : 90 tours en 15 secondes.
        a = (10 / 5.5) * 15 / 90
        self.play(tours.animate.set_value(100), run_time=15, rate_func=lambda u: a * u + (1 - a) * u * u)
        self.play(FadeIn(phrase("10 × 10 = 100 blocs : un carré, posé ligne après ligne", CIEL)))
        self.wait(1.6)
