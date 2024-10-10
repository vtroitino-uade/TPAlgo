'''
. -> Vacio
S -> Es el punto de aparicion del personaje
P -> Pasillo que conecta las habitaciones
X -> Es donde puede aparecer un tipo de habitacion
RY...Y -> Indica que es una habitacion, se debe especificar el tipo de la misma en la Y.
          Se puede poner mas de una Y si se desea una habitacion de varios tipos.
RE -> Habitacion de Enemigos
RP -> Habitacion de Puzzle
RM -> Habitacion de Criatura
RC -> Habuitacion de Recompensa
B -> Boss Final
'''

import random

TILE_SIZE = 5

LAYOUT_1 = [
    ['RM','.','X','P','B'],
    ['P','.','P','.','.'],
    ['X','P','X','P','RM'],
    ['P','.','P','.','.'],
    ['S','P','X','P','RM'],
]
LAYOUT_2 = [
    ['RM','.','X','P','B'],
    ['P','.','P','.','.'],
    ['X','P','S','P','RM'],
    ['P','.','P','.','X'],
    ['RM','P','X','P','P'],
]
LAYOUT_3 = [
    ['RM','.','X','P','B'],
    ['P','.','P','.','.'],
    ['X','P','X','P','RM'],
    ['P','.','P','.','.'],
    ['S','P','X','P','RM'],
]

LAYOUTS = [ LAYOUT_1, LAYOUT_2, LAYOUT_3 ]

selected_layout = LAYOUTS[random.randint(0, len(LAYOUTS) - 1)]

for row in selected_layout:
    for tile in row:
        print(tile.lstrip())
    print("", end='\n')
