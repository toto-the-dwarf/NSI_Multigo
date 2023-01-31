import pygame
from pygame.locals import *
from config import *



class pierre:
    def __init__(self, x, y, col_id) -> None:
        self.coord = (x, y)
        self.col_id = col_id
    
    def check(self, Map):
        lst_voisins = []
        for (x, y) in [(-1, 0), (1, 0), (0, -1), (0,1)]:
            if Map[self.coord[0]+x][self.coord[1]+y] != -1:
                for i in lst_pierres:
                    if i.coord == (self.coord[0]+x, self.coord[1]+y):
                        lst_voisins.append(i)
        return lst_voisins

class couleur:
    def __init__(self, col_id, rgb) -> None:
        self.col_id = col_id
        self.rgb = rgb

COULEURS = [couleur(i, RGB[i]) for i in range(len(RGB))]
lst_pierres = []



def main():
    """
        Boucle principale
    """
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode((L, L))
    pygame.display.set_caption("MultiGo")
    Turn = 0
    while True:
        SCREEN.fill(BEIGE)
        drawGrid()
        update(map_pierres)
        Hover = hover()
        if Hover != False and map_pierres[int(Hover[1]/ECART-1)][int(Hover[0]/ECART-1)] == -1:
            circle = pygame.draw.circle(SCREEN, COULEURS[Turn].rgb, Hover, SIZE)
            Turn = click(map_pierres, Hover, Turn)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.flip()

def drawGrid():
    """
        Dessine la grille 9x9 en fonction de la longueur L pour que les cases soient egalement espacées
    """
    for x in range(ECART, L-ECART, ECART):
        for y in range(ECART, L-ECART, ECART):
            rect = pygame.Rect(x, y, ECART, ECART)
            pygame.draw.rect(SCREEN, (0, 0, 0), rect, 1)

def hover() -> bool or tuple:
    """
        Vérifie si la sourie est proche d'une des intersections.
        Si c'est le cas, elle renvoie les coordonnées (x, y) de cette intersection.
        Sinon, elle renvoie False.
    """
    mos_x, mos_y = pygame.mouse.get_pos()
    for x in range(ECART, L, ECART):
        for y in range(ECART, L, ECART):
            if (mos_x > x-ECART/2) and (mos_x < x+ECART/2):
                if (mos_y > y-ECART/2) and (mos_y < y+ECART/2):
                    return (x, y)
    return False

def update(Map: list):
    """
        Affiche les pierres qui ont déjà été posées grâce à la map_pierres
    """
    for ligne in range(len(Map)):
        for colonne in range(len(Map[0])):
            if Map[ligne][colonne] != -1:
                circle = pygame.draw.circle(SCREEN, COULEURS[Map[ligne][colonne]].rgb, (ECART*(colonne+1), ECART*(ligne+1)), SIZE)

def click(Map: list, pos: tuple, Turn: int) -> int:
    """
        Prend en entrée la map, les coordonnées de l'intersection sur laquelle la souris est,
        et la couleur qui doit être jouée. Si le bouton gauche de la souris est appuyé,
        la map est mise à jour pour que la pierre soit placée au prochain update(),
        et la variable TURN est mise à jour pour que ce soit à la prochaine couleur
        de jouer.
    """
    if pygame.mouse.get_pressed()[0]:
        Map[int(pos[1]/ECART-1)][int(pos[0]/ECART-1)] = Turn
        lst_pierres.append(pierre(int(pos[1]/ECART-1), int(pos[0]/ECART-1), Turn))
        if Turn == 1:
            return 0
        else:
            return Turn + 1
    else:
        return Turn



main()