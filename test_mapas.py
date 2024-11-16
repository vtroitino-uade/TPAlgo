'''
. -> Vacío / No se muestra nada
+ -> Posición del personaje
S -> Es el punto de aparición del personaje
P -> Pasillo que conecta las habitaciones
X -> Es donde puede aparecer un tipo de habitación
RY...Y -> Indica que es una habitación, se debe especificar el tipo de la misma en la Y.
          Se puede poner mas de una Y si se desea una habitación de varios tipos.
RE -> Habitación de Enemigos
RP -> Habitación de Puzzle
RM -> Habitación de Criatura
RC -> Habitación de Recompensa
B -> Boss Final
'''

import random

ROOM_WIDTH = 9
ROOM_HEIGHT = 5
MAP_DIMENSION = 5

map_grid = []
for _ in range(ROOM_HEIGHT * MAP_DIMENSION):
    map_grid.append([' '] * (ROOM_WIDTH * MAP_DIMENSION))

def generate_random_map() -> list:
    '''
        Selecciona un diseño de mapa aleatorio y lo prepara para su representación.
    '''
    layout_1 = [
        ['.RM','.','X','.P','.B'],
        ['.P','.','.P','.','.'],
        ['X','.P','X','.P','.RM'],
        ['.P','.','.P','.','.'],
        ['+S','.P','X','.P','.RM'],
    ]
    layout_2 = [
        ['.RM','.','X','.P','.B'],
        ['.P','.','.P','.','.'],
        ['X','.P','+S','.P','.RM'],
        ['.P','.','.P','.','X'],
        ['.RM','.P','X','.P','.P'],
    ]
    layout_3 = [
        ['.RM','.','X','.P','.B'],
        ['.P','.','.P','.','.'],
        ['X','.P','X','.P','.RM'],
        ['.P','.','.P','.','.'],
        ['+S','.P','X','.P','.RM'],
    ]

    layouts = [ layout_1, layout_2, layout_3 ]
    selected_layout = random.choice(layouts)

    possible_rooms = ['.RE', '.RP', '.RC', '.REC', '.RPE', '.REE', '.RPC']

    for y in range(len(selected_layout)):
        for x in range(len(selected_layout[y])):
            if selected_layout[y][x] == 'X':
                selected_layout[y][x] = random.choices(possible_rooms,
                                              weights=[0.5, 0.1, 0.1, 0.1, 0.05, 0.1, 0.05],
                                              k=1)[0]
    return selected_layout

layout = generate_random_map()

print('Generated layout:', layout)

def generate_map():
    '''
        Genera el mapa completo.
    '''
    for y in range(len(layout)):
        for x in range(len(layout[y])):
            create_room(layout[y][x], x, y)

def create_room(cell_type: str, layout_x: int, layout_y: int) -> list:
    '''
        Crea una habitación dentro del mapa.
    '''
    map_x = layout_x * ROOM_WIDTH
    map_y = layout_y * ROOM_HEIGHT

    horizontal_wall = ' '
    vertical_wall = ' '
    border = ' '

    if cell_type.startswith('.'):
        horizontal_wall = ' '
        vertical_wall = ' '
        border = ' '
    elif cell_type.count('S'):
        horizontal_wall = '-'
        vertical_wall = '|'
        border = '@'
    elif cell_type.count('B'):
        horizontal_wall = '%'
        vertical_wall = '%'
        border = '6'
    elif cell_type.count('RM'):
        horizontal_wall = '-'
        vertical_wall = '|'
        border = 'M'
    elif cell_type.count('R'):
        horizontal_wall = '-'
        vertical_wall = '|'
        border = '°'

    if cell_type.startswith('+'):
        map_grid[map_y + 2][map_x + 4] = '8'
    else:
        map_grid[map_y + 2][map_x + 4] = ' '

    map_grid[map_y][map_x] = border
    map_grid[map_y][(map_x + ROOM_WIDTH) - 1] = border
    map_grid[(map_y + ROOM_HEIGHT) - 1][map_x] = border
    map_grid[(map_y + ROOM_HEIGHT) - 1][(map_x + ROOM_WIDTH) - 1] = border

    for x in range(map_x + 1, map_x + ROOM_WIDTH - 1):
        map_grid[map_y][x] = horizontal_wall
        map_grid[map_y + (ROOM_HEIGHT - 1)][x] = horizontal_wall

    for y in range(map_y + 1, map_y + ROOM_HEIGHT - 1):
        map_grid[y][map_x] = vertical_wall
        map_grid[y][(map_x + ROOM_WIDTH) - 1] = vertical_wall

def display_map() -> None:
    '''
        Muestra el mapa en la pantalla.
    '''
    generate_map()
    for row in map_grid:
        for cell in row:
            print(cell, end='')
        print()

display_map()
