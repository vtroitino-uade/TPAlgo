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

TILE_SIZE = 5

LAYOUT_1 = [
    ['RM','.','X','P','B'],
    ['P','.','P','.','.'],
    ['X','P','X','P','RM'],
    ['P','.','P','.','.'],
    ['S','P','X','P','RM'],
]
LAYOUT_2 = [
    ['+RM','.','X','P','B'],
    ['P','.','P','.','.'],
    ['X','P','S','P','RM'],
    ['P','.','P','.','X'],
    ['RM','P','X','P','RM'],
]
LAYOUT_3 = [
    ['RM','.','X','P','B'],
    ['P','.','P','.','.'],
    ['X','P','X','P','RM'],
    ['P','.','P','.','.'],
    ['+S','P','X','P','RM'],
]

LAYOUTS = [ LAYOUT_1, LAYOUT_2, LAYOUT_3 ]

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

def iterate_options(options: list, delay_char: float = 0.03) -> None:
    """
        Itera varias opciones en menúes que lo requieran
    """
    for i in range(len(options)):
        delayed_print(f"{i+1}. {options[i]}", delay_char)

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

def fake_dictionary(key_array, key, value_array):
    '''
        Busca una key en un array con palabras para asociarlo a través de un index a un array
        con valores y devolver el valor buscado.
    '''
    dict_index = key_array.index(key)
    return value_array[dict_index]

# ------ Movimiento del jugador ------

def check_current_pos():
    '''
        Devuelve la posición actual del personaje
    '''
    actual_cell = 0
    actual_row = 0
    layout = LAYOUT_2

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
    layout = LAYOUT_2
    x,y = old_pos
    character_pos = layout[y][x]
    layout[y][x] = character_pos.replace('+', '')

    x,y = new_pos
    character_pos = layout[y][x]
    layout[y][x] += '+'

def check_available_ways(current_pos):
    '''
        Revisa las opciones de movimiento disponibles
    '''
    actual_cell = current_pos[0]
    actual_row = current_pos[1]

    move_options = []
    layout = LAYOUT_2
    bottom_row_index = len(layout) - 1
    rightmost_cell_index = len(layout[actual_row] )- 1

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

def move_input(options, current_pos):
    '''
        Input para moverse
    '''
    for i in range(len(options)):
        print(str(i+1) + '. ' + options[i])
    choice= input_with_validation('¿Para donde vas? ', 'Ah, buscando burlar el sendero, ¿crees ' +
                                  'que el destino se distrae tan fácilmente?', 
                                  range(1, len(options)+1))
    new_pos = move_character(choice-1, current_pos, options)
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
    print('Empecemos...')
    time.sleep(1)
    story(0)
    combat_stats = create_character()
    os.system('cls')
    while True:
        character_movement()

# ------- Clases y creacion de personaje y enemigos ----
def knight():
    '''
        Se crean los stats para el personaje caballero

    '''
    global stats
    dice_weights = [1] * 20
    stats = [['base_attack', 'base_hp', 'luck', 'crit_hit'],
            [50, 500, dice_weights, 75]]

def mage():
    '''
        Se crean los stats para el personaje mago

    '''
    global stats
    dice_weights = [1] * 9 + [3] * 11
    stats = [['base_attack', 'base_hp', 'luck', 'crit_hit'],
            [35, 400, dice_weights, 75]]

def assassin():
    '''
        Se crean los stats para el personaje mago
    '''
    global stats
    dice_weights = [1] * 20
    stats = [['base_attack', 'base_hp', 'luck', 'crit_hit'],
            [50, 500, dice_weights, 110]]

def boss():
    pass

def final_boss():
    pass

def base_enemy():
    dice_weights = [1] * 20
    enemy_stats = [['base_attack', 'base_hp', 'luck', 'crit_hit'],
                   [20, 200, dice_weights, 40]]
    return enemy_stats

def create_character():
    '''
        Crea el personaje
    '''
    global stats
    confirmation = 2
    options = ['Un caballero marcado por las sombras de aquellos sacrificios hechos en nombre de ' +
                'su rey.', 'Un erudito que rompió las reglas buscando la magia que mueve el mundo.', 
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
    stats = create_character_class(character_class - 1)


def create_character_class(character):
    '''
    Se selecciona una clase de las disponibles
    '''
    classes = [knight, mage, assassin]
    return classes[character]()
# ------ Combate -----
def fight(enemy_type):
    '''
        Ejecuta la pelea
    '''
    # ---- Creacion del enemigo para la pelea ------
    enemy_stats = create_enemy(enemy_type)
    enemy_life = fake_dictionary(enemy_stats[0], 'base_hp', enemy_stats[1])
    enemy_attk = fake_dictionary(enemy_stats[0], 'base_attack', enemy_stats[1])
    enemy_luck = fake_dictionary(enemy_stats[0], 'luck', enemy_stats[1])
    enemy_crit  = fake_dictionary(enemy_stats[0], 'crit_hit', enemy_stats[1])

    # ---- Creacion del personaje para la pelea ----
    life = fake_dictionary(stats[0], 'base_hp', stats[1])
    attk = fake_dictionary(stats[0], 'base_attack', stats[1])
    luck = fake_dictionary(stats[0], 'luck', stats[1])
    crit  = fake_dictionary(stats[0], 'crit_hit', stats[1])

    delayed_print('¡Un enemigo salvaje ha aparecido! que vas a hacer?')
    iterate_options(['atacar', 'irse'])
    input_with_validation('Elije rapido!', 'No, no, eso no se puede hacer.', range(1, 3))

def create_enemy(enemy_type):
    '''
        Crea a los enemigos segun el tipo requerido por la pelea
    '''
    enemy_types = ['base', 'boss', 'final']
    enemy_classes = [base_enemy, boss, final_boss]

    enemy = fake_dictionary(enemy_types, enemy_type, enemy_classes)
    return enemy()

def main():
    """
    main qcyo
    """
    start_menu()

#game()
fight('base')

