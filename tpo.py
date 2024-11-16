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
import os
import time

# -------- Mapa y posiciones --------------
ROOM_WIDTH = 9
ROOM_HEIGHT = 5
MAP_DIMENSION = 5

map_grid = []
stats = [50, 600, 75]
items = ['Poción de vida', 'Poción de vida']
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
    selected_layout = layouts[random.randint(0, len(layouts) - 1)]

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
def delayed_print(text: str, delay_char=0.03, color=None) -> None:
    '''
    Imprime caracteres uno a la vez.
    '''

    for character in text:
        if color:
            print(f'{color}{character}\033[0m', end="")
        else:
            print(f'{character}', end="")
        time.sleep(delay_char)
    print()

def story(chapter: int) -> None:
    '''
        Textos relevantes para la historia
    '''
    text = [
        'Atrapado en las profundidades de unas catacumbas ancestrales, el viajero despertó sin ' +
        'recordar cómo había llegado allí. La única salida estaba sellada por una magia oscura ' +
        'y antigua. En la penumbra, una voz resonó advirtiendo que tres seres poderosos '  +
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
        if var.isdigit():
            var = int(var)
            if input_range and var in input_range:
                return var
        delayed_print(error_text)
        time.sleep(1)

def iterate_options(options: list, delay_char: float = 0.03, color=None) -> None:
    """
        Itera varias opciones en menúes que lo requieran
    """
    for i in range(len(options)):
        if color:
            delayed_print(f"{i+1}. {options[i]}", color=color, delay_char=delay_char)
        else:
            delayed_print(f"{i+1}. {options[i]}", delay_char)

def menu(options:list, input_text:str, header:str) -> None:
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

def check_current_pos() -> list:
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

def update_current_pos(old_pos: list, new_pos: list) -> None:
    '''
        Busca la posicion vieja para reemplazar el caracter especial en la nueva posicion
    '''
    x,y = old_pos
    character_pos = layout[y][x]
    layout[y][x] = character_pos.replace('+', '')

    x,y = new_pos
    character_pos = layout[y][x]
    layout[y][x] = character_pos.replace('.', '+') if '.' in character_pos else '+' + character_pos

def check_available_ways(current_pos: list) -> list:
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

def move_input(options: list, current_pos: list) -> list:
    '''
        Input para moverse
    '''
    choice = 0
    options.append('Abrir inventario')
    while choice not in range(1, len(options)):
        iterate_options(options)
        choice= input_with_validation('¿Qué vas a hacer? ', 'Ah, buscando burlar el sendero, ¿crees ' +
                                  'que el destino se distrae tan fácilmente?', 
                                  range(1, len(options)+1))
        if choice == len(options):
            items_menu()
    new_pos = move_character(choice-1, current_pos, options)
    return new_pos


def move_character(index: int, current_pos: list, options: list) -> list:
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

# ----- Habitaciones ------
def check_room_type(current_pos: list) -> str:
    '''
        Devuelve el tipo de habitación en la que se encuentra el personaje
    '''
    layout = LAYOUT_2
    x,y = current_pos
    cell = layout[y][x]
    

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
    story(0)
    create_character_input()
    os.system('cls')
    while True:
        display_map()
        print()
        character_movement()

# ------- Clases y creacion de personaje y enemigos ----
def knight():
    '''
        Se crean los stats para el personaje caballero
        Stats segun el index = ['base_attack', 'base_hp', 'crit_hit']
    '''
    global stats
    stats = [50, 600, 75]

def assassin():
    '''
        Se crean los stats para el personaje asesino
        Stats segun el index = ['base_attack', 'base_hp', 'crit_hit']
    '''
    global stats
    stats = [50, 500, 110]

def boss():
    pass

def final_boss():
    pass

def base_enemy():
    '''
        Crea el enemigo base para la pelea
        stats segun el index = ['base_attack', 'base_hp', 'crit_hit']
    '''
    enemy_stats = [20, 200, 40]
    return enemy_stats

def create_character_input():
    '''
        Crea el personaje
    '''
    confirmation = 2
    options = ['Un caballero marcado por las sombras de aquellos sacrificios hechos en nombre de ' +
                'su rey.', 
                'Un asesino sombrío con una cuenta pendiente, experto en atacar los puntos débiles '
                + 'de sus presas.']
    while confirmation == 2:
        os.system('cls')
        delayed_print('Es hora de que pienses en quien fuiste antes de esta oscura caverna.')
        iterate_options(options)
        character_class = input_with_validation('¿Recuerdas quien eras? ', 'Tu pasado ya está '  +
                                            'definido, solo los elegidos por los Dioses pueden ' +
                                            'cambiarlo. Y creeme, no eres uno de ellos.',
                                            range(1,len(options)+1))
        confirmation = input_with_validation('¿Estás seguro?\n1. Si\n2. No\n', 'No evadas la pregunta',
                                             range(1,3))
    delayed_print('Así que eso eres... esperemos que tus pecados hoy te ayuden.')
    create_character_class(character_class - 1)

def create_character_class(character):
    '''
    Se selecciona una clase de las disponibles
    '''
    classes = [knight, assassin]
    classes[character]()

def create_enemy(enemy_type):
    '''
        Crea a los enemigos segun el tipo requerido por la pelea
    '''
    enemy_types = ['base', 'boss', 'final']
    enemy_classes = [base_enemy, boss, final_boss]
    enemy = enemy_classes[enemy_types.index(enemy_type)]

    return enemy()

# ------ Combate -----
def fight(enemy_type):
    '''
        Ejecuta la pelea
    '''
    global stats
    green = '\033[92m'
    red = '\033[91m'
    enemy_stats = create_enemy(enemy_type)
    turn_choice = who_attacks_first()
    turn_functions = [player_turn, enemy_turn]
    while enemy_stats[1] > 0 and stats[1] > 0:
        enemy_stats = turn_functions[turn_choice](enemy_stats)
        turn_choice = 1 - turn_choice
        os.system('cls')
        delayed_print(f'El enemigo tiene {enemy_stats[1]} de vida.', color=red)
        delayed_print(f'Tienes {stats[1]} de vida.', color=green)

    if stats[1] <= 0 and enemy_type == 'base':
        death_menu('Asesinado a manos de un simple esbirro... que verguenza.')
        time.sleep(1)


    delayed_print('¡Has vencido al enemigo!', color=green)
    delayed_print('Continuemos...')

    time.sleep(1)

def who_attacks_first():
    '''
        Determina quien ataca primero
    '''
    global stats
    delayed_print('¡Un enemigo salvaje ha aparecido! Probemos tu suerte...')
    enemy_dice = 0
    dice = 0
    green = '\033[92m'
    red = '\033[91m'
    while enemy_dice == dice:
        enemy_dice, dice = dice_roll()
        if enemy_dice == dice:
            delayed_print('Uno debe ser el primero, volvamos a intentarlo.')


    if dice > enemy_dice:
        delayed_print('¡Eres más rápido que tu enemigo! Atacas primero.',color=green)
        return 0
    delayed_print('El enemigo es más rápido, te ataca primero.', color=red )
    return 1

def death_menu(text):
    '''
        Menu de muerte
    '''
    red = '\033[91m'
    delayed_print(text, color=red)
    options = ['Volver a intentarlo', 'Salir']
    selection = menu(options, '¿Qué deseas hacer?', 'Has muerto...')
    if selection == 1:
        game()
    os.system('cls')
    delayed_print('Hasta la próxima...')

def player_attack(enemy_stats):
    '''
        Ataque del jugador
    '''
    global stats
    color = '\033[92m'
    delayed_print('Atacas al enemigo', color=color)
    enemy_dice, dice = dice_roll()
    attk, life, crit = stats
    enemy_attk, enemy_life,  enemy_crit = enemy_stats
    if dice > enemy_dice:
        if dice - enemy_dice >= 7:
            delayed_print('¡Golpe crítico!', color=color)
            delayed_print('Tu brazo retumba con la fuerza del golpe.', color=color)
            enemy_life -= crit
        else:
            delayed_print('¡Golpeas al enemigo!', color=color)
            enemy_life -= attk
    else:
        delayed_print('¡Fallaste el golpe!', color=color)
    if enemy_life <= 0:
        enemy_life = 0
    return [enemy_attk, enemy_life,  enemy_crit]

def player_turn(enemy_stats):
    '''
        Turno del jugador
    '''
    global stats
    enemy_attk, enemy_life,  enemy_crit = enemy_stats
    attk, life, crit = stats
    color = '\033[92m'
    options = ['Atacar', 'Objeto']
    delayed_print('Es tu turno.', color=color)
    iterate_options(options, color=color)
    choice = input_with_validation('¿Qué deseas hacer? ', 'No puedes huir de tu destino.',
                                    range(1,len(options) + 1))
    if choice == 1:
        enemy_stats = player_attack(enemy_stats)
    elif choice == 2:
        items_menu()
    return enemy_stats

def items_menu():
    '''
        menu de items
    '''
    global items
    iterate_options(items)
    item = input_with_validation('¿Qué objeto deseas usar? ', 'No puedes usar eso.',
                                range(1,len(items) + 1))
    item = items[item - 1]
    items.remove(item)
    use_item(item)

def enemy_turn(enemy_stats):
    '''
        Turno del enemigo
    '''
    global stats
    enemy_dice, dice = dice_roll()
    enemy_attk, enemy_life, enemy_crit = enemy_stats
    attk,life, crit = stats
    color = '\033[91m'

    delayed_print('El enemigo alza su espada.', color=color)
    if enemy_dice > dice:
        if enemy_dice - dice >= 7:
            delayed_print('El enemigo te ha golpeado con un golpe crítico.',color=color)
            life -= enemy_crit
        else:
            delayed_print('El enemigo te ha golpeado.',color=color)
            life -= enemy_attk
    else:
        delayed_print('El enemigo falla el golpe.', color=color)
    stats = [attk, life, crit]
    if life <= 0:
        life = 0
    return enemy_stats

# ------ Items -----
def use_item(item):
    '''
        Usa el item seleccionado
    '''
    global stats
    global items

    all_items = ['Poción de vida', 'Poción de fuerza', 'Poción de crítico']
    item_functions = [potion_of_life, potion_of_strength, potion_of_crit]
    item_index = all_items.index(item)
    item_functions[item_index]()

def potion_of_life():
    '''
        Poción de vida
    '''
    global stats
    stats[1] += 100
    delayed_print('Has usado una poción de vida, recuperas 100 puntos de vida.')

def potion_of_strength():
    '''
        Poción de fuerza
    '''
    global stats
    stats[0] += 10
    delayed_print('Has usado una poción de fuerza, aumentas tu ataque en 10 puntos.')

def potion_of_crit():
    '''
        Poción de critico
    '''
    global stats
    stats[2] += 10
    delayed_print('Has usado una poción de crítico, aumentas tu daño de golpe crítico en 10 puntos.')

# ------ Dados ------
def dice_roll():
    '''
        Funcion que simula el lanzamiento de dados
    '''
    green = '\033[92m'
    red = '\033[91m'
    delayed_print('Lanzando los dados...', color=green)
    dice = dice_roll_simulation(color=green)
    delayed_print('El enemigo lanza los dados...', color=red)
    enemy_dice = dice_roll_simulation(color=red)
    return enemy_dice, dice

def dice_roll_simulation(delay=0.1, color = None):
    """
        Simula una ruleta visual con las tiradas de dados.
    """
    spin_amount = random.randint(10, 20)
    end_color = '\033[0m'
    for _ in range(spin_amount):
        dice = random.randint(1, 20)
        if color:
            print(f"{color}{dice}{end_color} ", end="\r")
        else:
            print(f"{dice} ", end="\r")
        time.sleep(delay)
    print()
    return dice

# ------ Main ------
def main():
    """
    Ejecuta el programa
    """
    start_menu()

def get_random_potion() -> str:
    """
    Selecciona una poción aleatoria de la lista de pociones.
    """
    life_potion = ['Poción de vida'] * 9
    attack_potion = ['Poción de fuerza'] * 3
    critical_potion = ['Poción de crítico'] * 3
    potions = life_potion + attack_potion + critical_potion

    index = random.randint(0, len(potions) - 1)
    return potions[index]


    

# input_with_validation("Ingrese:","int", [1, 4])
game()
#fight('base')
# move_input(['arriba', 'derecha'], [2, 2])
