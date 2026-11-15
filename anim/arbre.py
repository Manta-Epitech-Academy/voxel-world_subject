# Étape 6, « Une fonction arbre » : le tronc, puis les feuilles étage par étage.
# Chaque étage se pose vu de dessus, avec x - 1, x, x + 1 et z - 1, z, z + 1 au
# bord ; quand il est terminé, la caméra passe sur le côté et fait le tour de
# l'arbre, puis revient au-dessus pour l'étage suivant. Pas de coordonnées sous
# les feuilles : l'élève les écrit lui-même. Pas d'herbe au sol : on la
# confondrait avec les feuilles.
# Coordonnées du monde (x, y vers le haut, z) -> manim (x, z, y).
#
#   capture.py anim anim/arbre.py LArbre -o img/outil-arbre.webp --fps 30
from manim import *
from commun import *

C = 0.55                      # côté d'un bloc, en unités manim
AUTOUR = [(dx, dz) for dz in (-1, 0, 1) for dx in (-1, 0, 1) if (dx, dz) != (0, 0)]
# Les étages : (hauteur au-dessus du pied du tronc, cases). Au milieu des deux
# premiers étages, c'est le tronc.
ETAGES = [(3, AUTOUR), (4, AUTOUR), (5, [(0, 0)])]
NOMS_X = {-1: "x - 1", 0: "x", 1: "x + 1"}
NOMS_Z = {-1: "z - 1", 0: "z", 1: "z + 1"}


def bloc(x, y, z, sorte):
    c = Cube(side_length=C, fill_color=COULEURS[sorte], fill_opacity=1, stroke_color=FOND, stroke_width=1)
    return c.move_to(np.array([x * C, z * C, y * C]))


class LArbre(ThreeDScene):
    def fixe(self, m):
        self.add_fixed_in_frame_mobjects(m)
        self.remove(m)          # fixé dans le cadre, mais montré seulement quand on l'anime
        return m

    def titre(self, t, couleur):
        return self.fixe(texte(t, 28, couleur).to_edge(UP, buff=0.4))

    def construct(self):
        cote = dict(phi=72 * DEGREES, theta=-100 * DEGREES)
        dessus = dict(phi=0, theta=-90 * DEGREES)
        self.set_camera_orientation(**cote, zoom=1.35, frame_center=np.array([0, 0, 2.0 * C]))
        # Le sol : un quadrillage, pas d'herbe. Des cases et pas des traits :
        # la caméra 3D range les cases par profondeur avec les faces des blocs,
        # alors que des traits seraient dessinés par-dessus le tronc.
        sol = VGroup(*[Square(side_length=C, fill_color=FOND, fill_opacity=1, stroke_color=DOUX, stroke_width=1.5, stroke_opacity=0.6)
                       .move_to(np.array([i * C, j * C, -C / 2])) for i in range(-2, 3) for j in range(-2, 3)])
        sol.set_shade_in_3d(True)
        self.add(sol)

        self.next_section("le tronc : de y à y + 4")
        t = self.titre("le tronc : 5 blocs de BOIS, de y à y + 4", CIEL)
        self.play(FadeIn(t))
        for h in range(5):
            self.play(FadeIn(bloc(0, h, 0, "BOIS"), scale=0.6), run_time=0.3)
        self.wait(0.6)

        for n, (h, cases) in enumerate(ETAGES, start=1):
            self.next_section(f"étage {n} : les feuilles en y + {h}")
            t2 = self.titre(f"étage {n} : les feuilles en y + {h}, vues de dessus", ALERTE)
            self.play(FadeOut(t), run_time=0.3)
            self.move_camera(**dessus, run_time=1.4)
            # Les noms des cases, posés à plat à la hauteur de l'étage : lisibles de dessus.
            etiq = VGroup(*[code(NOMS_X[d], 12, DOUX).move_to(np.array([d * C, -2.9 * C, h * C])) for d in (-1, 0, 1)],
                          *[code(NOMS_Z[d], 12, DOUX).move_to(np.array([-3.3 * C, d * C, h * C])) for d in (-1, 0, 1)])
            self.play(FadeIn(t2), FadeIn(etiq), run_time=0.4)
            t = t2
            for dx, dz in cases:
                self.play(FadeIn(bloc(dx, h, dz, "FEUILLES"), scale=0.6), run_time=0.35)
                self.wait(0.3)
            self.play(FadeOut(etiq), run_time=0.3)

            self.next_section(f"étage {n} terminé")
            t3 = self.titre(f"étage {n} terminé", CIEL)
            self.play(FadeOut(t), run_time=0.3)
            self.move_camera(**cote, run_time=1.4)
            self.play(FadeIn(t3), run_time=0.3)
            t = t3
            self.move_camera(theta=cote["theta"] + TAU, run_time=4.5, rate_func=linear)
            self.set_camera_orientation(theta=cote["theta"])

        self.play(FadeOut(t), run_time=0.3)
        self.play(FadeIn(self.titre("un étage à la fois : de dessus pour poser, de côté pour vérifier", CIEL)))
        self.wait(1.5)
