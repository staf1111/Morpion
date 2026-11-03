import pygame
import sys

LARGEUR, HAUTEUR = 600, 820
TAILLE_CASE = 160
MARGE_X = (LARGEUR - 3 * TAILLE_CASE) // 2
MARGE_Y = 190

FOND = (24, 26, 38)
GRILLE = (52, 56, 78)
CASE = (34, 37, 54)
CASE_SURVOL = (44, 48, 70)
COULEUR_X = (255, 92, 122)
COULEUR_O = (80, 200, 255)
TEXTE = (235, 236, 245)
TEXTE_DOUX = (140, 145, 170)
OR = (255, 210, 90)


class Morpion:
    def __init__(self):
        self.j1 = "X"
        self.j2 = "O"
        self.scores = {"X": 0, "O": 0, "nul": 0}
        self.nouvelle_partie()

    def nouvelle_partie(self):
        self.plateau = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.joueur_en_jeu = self.j1
        self.resultat = None
        self.ligne_gagnante = None
        self.animations = {}

    def jouer(self, x, y):
        if self.resultat or self.plateau[x][y] != '-':
            return
        self.plateau[x][y] = self.joueur_en_jeu
        self.animations[(x, y)] = 0.0
        fin = self.test_fin_jeu(self.joueur_en_jeu)
        if fin:
            self.resultat = fin
            self.scores[fin if fin in ("X", "O") else "nul"] += 1
        else:
            self.changer_joueur()

    def test_fin_jeu(self, joueur):
        lignes = [[(x, y) for y in range(3)] for x in range(3)]
        lignes += [[(x, y) for x in range(3)] for y in range(3)]
        lignes.append([(i, i) for i in range(3)])
        lignes.append([(i, 2 - i) for i in range(3)])
        for ligne in lignes:
            if all(self.plateau[x][y] == joueur for x, y in ligne):
                self.ligne_gagnante = ligne
                return joueur
        if all(self.plateau[x][y] != '-' for x in range(3) for y in range(3)):
            return "nul"
        return False

    def changer_joueur(self):
        if self.joueur_en_jeu == self.j1:
            self.joueur_en_jeu = self.j2
        else:
            self.joueur_en_jeu = self.j1


class Interface:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Morpion")
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        self.horloge = pygame.time.Clock()
        self.police_titre = pygame.font.SysFont("arial", 46, bold=True)
        self.police = pygame.font.SysFont("arial", 26, bold=True)
        self.police_petite = pygame.font.SysFont("arial", 18)
        self.jeu = Morpion()
        self.bouton = pygame.Rect(LARGEUR // 2 - 110, HAUTEUR - 85, 220, 54)
        self.progression_ligne = 0.0

    def case_sous_souris(self, pos):
        mx, my = pos
        for x in range(3):
            for y in range(3):
                if self.rect_case(x, y).collidepoint(mx, my):
                    return x, y
        return None

    def rect_case(self, x, y):
        return pygame.Rect(MARGE_X + y * TAILLE_CASE + 6, MARGE_Y + x * TAILLE_CASE + 6,
                           TAILLE_CASE - 12, TAILLE_CASE - 12)

    def texte(self, contenu, police, couleur, centre):
        surface = police.render(contenu, True, couleur)
        self.ecran.blit(surface, surface.get_rect(center=centre))

    def dessiner_entete(self):
        self.texte("MORPION", self.police_titre, TEXTE, (LARGEUR // 2, 50))
        cartes = [("X", COULEUR_X, 150), ("Nul", TEXTE_DOUX, 300), ("O", COULEUR_O, 450)]
        for nom, couleur, cx in cartes:
            cle = "nul" if nom == "Nul" else nom
            actif = not self.jeu.resultat and self.jeu.joueur_en_jeu == nom
            rect = pygame.Rect(cx - 60, 95, 120, 70)
            pygame.draw.rect(self.ecran, CASE, rect, border_radius=14)
            if actif:
                pygame.draw.rect(self.ecran, couleur, rect, 3, border_radius=14)
            self.texte(nom, self.police_petite, couleur, (cx, 115))
            self.texte(str(self.jeu.scores[cle]), self.police, TEXTE, (cx, 145))

    def dessiner_x(self, rect, t, couleur):
        m = 38
        a = (rect.left + m, rect.top + m)
        b = (rect.right - m, rect.bottom - m)
        c = (rect.right - m, rect.top + m)
        d = (rect.left + m, rect.bottom - m)
        t1 = min(t * 2, 1)
        t2 = max(0, min((t - 0.5) * 2, 1))
        pygame.draw.line(self.ecran, couleur, a, (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1), 14)
        if t2 > 0:
            pygame.draw.line(self.ecran, couleur, c, (c[0] + (d[0] - c[0]) * t2, c[1] + (d[1] - c[1]) * t2), 14)

    def dessiner_o(self, rect, t, couleur):
        rayon = int((rect.width // 2 - 34) * (0.4 + 0.6 * t))
        pygame.draw.circle(self.ecran, couleur, rect.center, rayon, 13)

    def dessiner_plateau(self):
        survol = self.case_sous_souris(pygame.mouse.get_pos())
        for x in range(3):
            for y in range(3):
                rect = self.rect_case(x, y)
                vide = self.jeu.plateau[x][y] == '-'
                fond = CASE_SURVOL if survol == (x, y) and vide and not self.jeu.resultat else CASE
                pygame.draw.rect(self.ecran, fond, rect, border_radius=18)
                symbole = self.jeu.plateau[x][y]
                t = self.jeu.animations.get((x, y), 1.0)
                if symbole == "X":
                    self.dessiner_x(rect, t, COULEUR_X)
                elif symbole == "O":
                    self.dessiner_o(rect, t, COULEUR_O)
                elif survol == (x, y) and not self.jeu.resultat:
                    fantome = (*([c // 3 + 30 for c in (COULEUR_X if self.jeu.joueur_en_jeu == "X" else COULEUR_O)]),)
                    if self.jeu.joueur_en_jeu == "X":
                        self.dessiner_x(rect, 1, fantome)
                    else:
                        self.dessiner_o(rect, 1, fantome)

    def dessiner_ligne_gagnante(self):
        if not self.jeu.ligne_gagnante:
            return
        debut = self.rect_case(*self.jeu.ligne_gagnante[0]).center
        fin = self.rect_case(*self.jeu.ligne_gagnante[-1]).center
        t = self.progression_ligne
        point = (debut[0] + (fin[0] - debut[0]) * t, debut[1] + (fin[1] - debut[1]) * t)
        pygame.draw.line(self.ecran, OR, debut, point, 10)

    def dessiner_pied(self):
        if self.jeu.resultat == "nul":
            message, couleur = "Match nul !", TEXTE
        elif self.jeu.resultat:
            message = "Victoire de " + self.jeu.resultat + " !"
            couleur = COULEUR_X if self.jeu.resultat == "X" else COULEUR_O
        else:
            message = "Au tour de " + self.jeu.joueur_en_jeu
            couleur = COULEUR_X if self.jeu.joueur_en_jeu == "X" else COULEUR_O
        self.texte(message, self.police, couleur, (LARGEUR // 2, MARGE_Y + 3 * TAILLE_CASE + 32))
        survol = self.bouton.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(self.ecran, OR if survol else GRILLE, self.bouton, border_radius=27)
        self.texte("Rejouer", self.police, FOND if survol else TEXTE, self.bouton.center)

    def mettre_a_jour(self, dt):
        for case in self.jeu.animations:
            self.jeu.animations[case] = min(1.0, self.jeu.animations[case] + dt * 4)
        if self.jeu.ligne_gagnante:
            self.progression_ligne = min(1.0, self.progression_ligne + dt * 3)
        else:
            self.progression_ligne = 0.0

    def lancer(self):
        while True:
            dt = self.horloge.tick(60) / 1000
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                    if self.bouton.collidepoint(evenement.pos):
                        self.jeu.nouvelle_partie()
                    else:
                        case = self.case_sous_souris(evenement.pos)
                        if case:
                            self.jeu.jouer(*case)
                if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_r:
                    self.jeu.nouvelle_partie()
            self.mettre_a_jour(dt)
            self.ecran.fill(FOND)
            self.dessiner_entete()
            self.dessiner_plateau()
            self.dessiner_ligne_gagnante()
            self.dessiner_pied()
            pygame.display.flip()


if __name__ == "__main__":
    Interface().lancer()
