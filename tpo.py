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
Uso de colores para poder printear las habitaciones ya vistas y posicion actual:

class bcolors:
    Red = '\033[91m'
    Green = '\033[92m'
    Blue = '\033[94m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Yellow = '\033[93m'
    Magenta = '\033[95m'
    Grey = '\033[90m'
    Black = '\033[90m'

    ENDC = '\033[0m' # finalizar
    BOLD = '\033[1m' # negrita
    UNDERLINE = '\033[4m' # subrayado

print("Texto de color " f"{bcolors.Red}rojo{bcolors.ENDC}")
print(f"{bcolors.Yellow}Ahora todo el texto es de color amarillo!{bcolors.ENDC}")
print(f"{bcolors.Black}{bcolors.BOLD}Ahora todo el texto es de color negro y en negritas!{bcolors.ENDC}")
print(f"{bcolors.Blue}Ahora todo el texto es de color azul y y solo {bcolors.UNDERLINE}esto en subrayado!{bcolors.ENDC}")
print("Texto normal")
'''

import random
import math
import os
import time

# -------- Mapa y posiciones --------------
ROOM_WIDTH = 9
ROOM_HEIGHT = 5
MAP_DIMENSION = 5

map_grid = []
is_boss_unlocked = False

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
        ['.P','.','.P','.','.'],
        ['.RM','.P','X','.P','X'],
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

def generate_map():
    '''
        Genera el mapa completo.
    '''
    for y in range(len(layout)):
        for x in range(len(layout[y])):
            if 'P' == layout[y][x]:
                create_path(check_available_ways([x, y]), x * ROOM_WIDTH, y * ROOM_HEIGHT)
            else:
                create_room(layout[y][x], x * ROOM_WIDTH, y * ROOM_HEIGHT)

def create_room(cell_type: str, map_x: int, map_y: int) -> list:
    '''
        Crea una habitación dentro del mapa.
    '''

    if '+' == cell_type[0]:
        map_grid[map_y + 2][map_x + 4] = '8'
    else:
        map_grid[map_y + 2][map_x + 4] = ' '

    horizontal_wall = ' '
    vertical_wall = ' '
    border = ' '

    if '.' != cell_type[0]:
        if cell_type.count('S'):
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

def create_path(available_ways: list, map_x: int, map_y: int) -> None:
    '''
        Crea un pasillo entre habitaciones.
    '''
    if 'derecha' in available_ways or 'izquierda' in available_ways:
        for x in range(map_x, map_x + ROOM_WIDTH):
            map_grid[map_y + 2][x] = '-'
    elif 'arriba' in available_ways or 'abajo' in available_ways:
        for y in range(map_y, map_y + ROOM_HEIGHT):
            map_grid[y][map_x + 4] = '|'

def display_map() -> None:
    '''
        Muestra el mapa en la pantalla.
    '''
    current_pos = check_current_pos()
    unhide_avilable_ways(current_pos)
    generate_map()
    for row in map_grid:
        for cell in row:
            print(cell, end='')
        print()

# -------- Consola - Input y prints --------------
def delayed_print(text, delay_char=0.03):
    '''
        Imprime caracteres uno a la vez.
    '''
    for character in text:
        print(character, end="")
        time.sleep(delay_char)
    print()

def story(chapter):
    '''
        Textos relevantes para la historia
    '''
    text = [
        'Atrapado en las profundidades de unas catacumbas ancestrales, el viajero despertó sin' +
        'recordar cómo había llegado allí. La única salida estaba sellada por una magia oscura' +
        'y antigua. En la penumbra, una voz resonó advirtiendo que tres seres poderosos'  +
        'custodiaban su libertad. Para escapar, debía encontrarlos y enfrentarse a sus pruebas.'
    ]
    delayed_print(text[chapter])

def input_with_validation(input_text: str, error_text: str, input_range: range) -> int:
    """
        Valida el input segun los parametros
    """
    while True:
        var = input(input_text)
        time.sleep(0.1)
        if not var.isdigit():
            print(error_text)
            time.sleep(1)
            os.system("cls")
            continue
        var = int(var)
        if not input_range or var not in input_range:
            print(error_text)
            continue
        return var

def iterate_options(options: list) -> None:
    """
        Itera varias opciones en menúes que lo requieran
    """
    for i in range(len(options)):
        print(f"{i+1}. {options[i]}")

def menu(options, input_text, header) -> None:
    """
        Muestra un menú y pide un input
    """
    response = "error"
    os.system("cls")
    print(header)
    iterate_options(options)
    time.sleep(0.3)
    response = input_with_validation(input_text,'Error de ingreso, vuelve a intentarlo.', 
                                     range(1,len(options) + 1))

    return response

# ------ Movimiento del jugador ------

def check_current_pos():
    '''
        Devuelve la posición actual del personaje
    '''
    actual_cell = 0
    actual_row = 0

    for row in layout:
        for cell in row:
            if '+' in cell:
                actual_row = layout.index(row)
                actual_cell = row.index(cell)
    current_pos = [actual_cell, actual_row]
    return current_pos

def update_current_pos(old_pos, new_pos):
    '''
        Busca la posicion vieja para reemplazar el caracter especial en la nueva posicion
    '''
    x,y = old_pos
    character_pos = layout[y][x]
    layout[y][x] = character_pos.replace('+', '')

    x,y = new_pos
    character_pos = layout[y][x]
    if '.' in character_pos:
        layout[y][x] = character_pos.replace('.', '+')
    else:
        layout[y][x] = '+' + character_pos

def check_available_ways(current_pos):
    '''
        Revisa las opciones de movimiento disponibles
    '''
    actual_cell = current_pos[0]
    actual_row = current_pos[1]

    move_options = []
    bottom_row_index = len(layout) - 1
    rightmost_cell_index = len(layout[actual_row]) - 1

    if actual_row < bottom_row_index:
        if layout[actual_row + 1][actual_cell] != '.':
            move_options.append('abajo')
    if actual_row > 0:
        if layout[actual_row - 1][actual_cell] != '.':
            move_options.append('arriba')
    if actual_cell < rightmost_cell_index:
        if layout[actual_row][actual_cell + 1] != '.':
            move_options.append('derecha')
    if actual_cell > 0:
        if layout[actual_row][actual_cell - 1] != '.':
            move_options.append('izquierda')
    return move_options

def unhide_avilable_ways(current_pos) -> None:
    '''
        Muestra los pasillos.
    '''
    actual_cell = current_pos[0]
    actual_row = current_pos[1]

    bottom_row_index = len(layout) - 1
    rightmost_cell_index = len(layout[actual_row]) - 1
    if actual_row < bottom_row_index:
        if layout[actual_row + 1][actual_cell] != '.':
            layout[actual_row + 1][actual_cell] = layout[actual_row + 1][actual_cell].replace('.', '')
    if actual_row > 0:
        if layout[actual_row - 1][actual_cell] != '.':
            layout[actual_row - 1][actual_cell] = layout[actual_row - 1][actual_cell].replace('.', '')
    if actual_cell < rightmost_cell_index:
        if layout[actual_row][actual_cell + 1] != '.':
            layout[actual_row][actual_cell + 1] = layout[actual_row][actual_cell + 1].replace('.', '')
    if actual_cell > 0:
        if layout[actual_row][actual_cell - 1] != '.':
            layout[actual_row][actual_cell - 1] = layout[actual_row][actual_cell - 1].replace('.', '')

def move_input(options, current_pos):
    '''
        Input para moverse
    '''
    for i in range(len(options)):
        print(str(i+1) + '. ' + options[i])
    choice = input_with_validation('¿Para donde vas? ', 'Ah, buscando burlar el sendero, ¿crees ' +
                                  'que el destino se distrae tan fácilmente?', 
                                  range(1, len(options)+1))
    new_pos = move_character(choice - 1, current_pos, options)
    new_x, new_y = new_pos
    while 'B' in layout[new_y][new_x] and not is_boss_unlocked:
        print('El camino esta bloqueado, debes encontrar a los guardianes para poder avanzar.')
        choice = input_with_validation('¿Para donde vas? ', 'Ah, buscando burlar el sendero, ¿crees ' +
                                    'que el destino se distrae tan fácilmente?', 
                                    range(1, len(options)+1))
        new_pos = move_character(choice - 1, current_pos, options)
        new_x, new_y = new_pos
    return new_pos

def move_character(index, current_pos, options):
    '''
        Funcion que mueve al personaje
    '''
    x_change = 0
    y_change = 0

    if options[index] == 'arriba':
        y_change = -2
    elif options[index] == 'abajo':
        y_change = 2
    elif options[index] == 'izquierda':
        x_change = -2
    elif options[index] == 'derecha':
        x_change = 2

    x, y = current_pos[0], current_pos[1]
    x += x_change
    y += y_change

    current_pos = [x, y]

    return current_pos

def character_movement():
    '''
        Controla el movimiento y posicion del personaje dentro del juego
    '''
    current_pos = check_current_pos()
    new_pos = move_input(check_available_ways(current_pos), current_pos)
    update_current_pos(current_pos, new_pos)
    os.system('cls')

# ----- Inicio y controlador de juego ------
def start_menu():
    """
        Menu de inicio
    """
    options = ["Jugar", "Ver tutorial", "Opciones", "Salir"]
    selection = menu(options, "Seleccione una opción: ", "Bievenido a DnD Rogue si fuera bueno")
    if selection == 1:
        game()

def game():
    '''
        Controlador del juego
    '''
    os.system('cls')
    # Crea un mapa vacío
    for _ in range(ROOM_HEIGHT * MAP_DIMENSION):
        map_grid.append([' '] * (ROOM_WIDTH * MAP_DIMENSION))

    print('Empecemos...')
    time.sleep(1)
    #story(0)
    while True:
        display_map()
        print()
        character_movement()

# ------ Combate -----
def create_character():
    '''a'''
    character = [crit_hit]

def crit_hit():
    '''a'''

def main():
    """
    main qcyo
    """
    start_menu()


#main()
#check_available_ways()

# input_with_validation("Ingrese:","int", [1, 4])
game()
