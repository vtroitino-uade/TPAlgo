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
'''

import random
import os
import time

# -------- Variables globales --------------

stats = []

items = ['Poción de vida']

boss_unlocked = False

key_item = []

END = False

riddles = [
    "Soy ligero como una pluma, pero incluso la persona más fuerte no puede sostenerme por mucho tiempo. ¿Qué soy?",
    "Cuanto más me quitas, más grande me vuelvo. ¿Qué soy?",
    "Tengo ciudades, pero no casas. Tengo montañas, pero no árboles. Tengo agua, pero no peces. ¿Qué soy?",
    "Caminamos sin pies, volamos sin alas, y te seguimos a todas partes. ¿Qué somos?",
    "Puedes romperme fácilmente sin tocarme ni usar fuerza. ¿Qué soy?",
    "Cuanto más tienes de mí, menos ves. ¿Qué soy?",
    "Tengo llaves, pero no cerraduras. Tengo espacio, pero no habitaciones. Puedes entrar, pero no salir. ¿Qué soy?",
    "Me puedes sostener sin usar las manos, puedes partirme y compartirme, pero si me pierdes, nadie puede ayudarte. ¿Qué soy?",
    "Soy algo que puedes atrapar pero nunca lanzar. ¿Qué soy?",
    "Tengo un cuello pero no cabeza, y siempre uso un sombrero. ¿Qué soy?"
]

riddles_options = [
    [["Aire", "Sombra", "Tu aliento", "Agua"], 2],  # Respuesta correcta: C
    [["Un agujero", "Una sombra", "El tiempo", "Arena"], 0],  # Respuesta correcta: A
    [["Un mapa", "Un espejo", "Un río", "Un libro"], 0],  # Respuesta correcta: A
    [["Nubes", "Una sombra", "Una idea", "El viento"], 1],  # Respuesta correcta: B
    [["Un secreto", "Un espejo", "Una promesa", "El hielo"], 2],  # Respuesta correcta: C
    [["Oscuridad", "Tiempo", "Arena", "Dinero"], 0],  # Respuesta correcta: A
    [["Un teclado", "Un piano", "Una cueva", "Una puerta"], 1],  # Respuesta correcta: B
    [["Una oportunidad", "El corazón", "La confianza", "Una palabra"], 2],  # Respuesta correcta: C
    [["Un sueño", "El resfriado", "Una mentira", "El amor"], 1],  # Respuesta correcta: B
    [["Un jarrón", "Una botella", "Una camisa", "Un reloj"], 1]  # Respuesta correcta: B
]

# -------- Mapa y posiciones --------------
ROOM_WIDTH = 9
ROOM_HEIGHT = 5
MAP_DIMENSION = 5

map_grid = []


LAYOUT_1 = [
    ['.RM','.','X','.P','.B'],
    ['.P','.','.P','.','.'],
    ['X','.P','X','.P','.RM'],
    ['.P','.','.P','.','.'],
    ['+S','.P','X','.P','.RM'],
]
LAYOUT_2 = [
    ['.RM','.','X','.P','.B'],
    ['.P','.','.P','.','.'],
    ['X','.P','+S','.P','.RM'],
    ['.P','.','.P','.','.'],
    ['.RM','.P','X','.P','X'],
]
LAYOUT_3 = [
    ['.RM','.','X','.P','.B'],
    ['.P','.','.P','.','.'],
    ['X','.P','X','.P','.RM'],
    ['.P','.','.P','.','.'],
    ['+S','.P','X','.P','.RM'],
]


def generate_random_map() -> list:
    '''
        Selecciona un diseño de mapa aleatorio y lo prepara para su representación.
    '''

    layouts = [ LAYOUT_1, LAYOUT_2, LAYOUT_3 ]
    selected_layout = layouts[random.randint(0, len(layouts) - 1)]

    possible_rooms = ['.RE', '.RE', '.RE', '.RE', '.RE',
                      '.RP', '.RP', 
                      '.RC', '.RC', 
                      '.REC', '.REC', 
                      '.RPE', '.REE', '.REE', 
                      '.RPC'
                    ]

    for y in range(len(selected_layout)):
        for x in range(len(selected_layout[y])):
            if selected_layout[y][x] == 'X':
                selected_layout[y][x] = possible_rooms[random.randint(0, len(possible_rooms) - 1)]
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
            print(f'{color}{character}\033[0m', end='')
        else:
            print(f'{character}', end='')
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
    '''
        Valida el input segun los parametros
    '''
    while True:
        is_digit = True
        var = input(input_text)
        time.sleep(0.1)
        for character in var:
            if character not in ['0','1','2','3','4','5','6','7','8','9']:
                is_digit = False
        if is_digit and len(var) > 0:
            var = int(var)
            if input_range and var in input_range:
                return var
        delayed_print(error_text)
        time.sleep(1)

def iterate_options(options: list, delay_char: float = 0.03, color=None) -> None:
    '''
        Itera varias opciones en menúes que lo requieran
    '''
    for i in range(len(options)):
        if color:
            delayed_print(f'{i+1}. {options[i]}', color=color, delay_char=delay_char)
        else:
            delayed_print(f'{i+1}. {options[i]}', delay_char)

def menu(options:list, input_text:str, header:str) -> None:
    '''
        Muestra un menú y pide un input
    '''
    response = 'error'
    os.system('cls')
    print(header)
    iterate_options(options)
    time.sleep(0.3)
    response = input_with_validation(input_text,'Error de ingreso, vuelve a intentarlo.',
                                     range(1,len(options) + 1))

    return response

def fake_dictionary(key, key_list, value_list):
    '''
    Devuelve el valor de una lista segun la key
    '''
    index = key_list.index(key)
    return value_list[index]

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
    if '.' in character_pos:
        layout[y][x] = character_pos.replace('.', '+')
    else:
        layout[y][x] = '+' + character_pos

def check_available_ways(current_pos: list) -> list:
    '''
        Revisa las opciones de movimiento disponibles
    '''
    global key_item
    if len(key_item) == 3:
        global boss_unlocked
        boss_unlocked = True

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
        choice = input_with_validation('¿Qué vas a hacer? ', 'Ah, buscando burlar el sendero,' +
                                  ' ¿crees que el destino se distrae tan fácilmente?', 
                                  range(1, len(options)+1))
        if choice == len(options):
            items_menu()
            time.sleep(0.5)
            return current_pos
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

    if 'B' in layout[y][x] and boss_unlocked == False:
        delayed_print('La puerta está cerrada, no puedes pasar. Una ventisca corre por detras de' +
                      ' la puerta, esa es la salida.')
        delayed_print('Una forma circular en el centro de la puerta parece activar un mecanismo.')
        if len(key_item) > 0:
            delayed_print('Parece que ese pedazo de medallón que encontraste podría ser útil aquí.')

        return current_pos

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
    return new_pos

# ----- Habitaciones ------
def check_room_type(current_pos: list) -> str:
    '''
    Devuelve el tipo de habitación en la que se encuentra el personaje.

     possible_rooms = ['.RE', '.RE', '.RE', '.RE', '.RE',
                      '.RP', '.RP', 
                      '.RC', '.RC', 
                      '.REC', '.REC', 
                      '.RPE', '.REE', '.REE', 
                      '.RPC'
                    ]
    '''
    x, y = current_pos
    cell = layout[y][x]
    possible_rooms = ['RE', 'RP', 'RM', 'RC', 'REC', 'RPE', 'REE', 'RPC', 'B']
    possible_rooms_functions = [enemy_room, puzzle_room, midboss_room, chest_room, chest_enemy_room,
                                puzzle_enemy_room, double_enemy_room, puzzle_chest_room, boss_room]
    for room in possible_rooms:
        if '+' + room == cell and '-' not in cell:
            fake_dictionary(room, possible_rooms, possible_rooms_functions)()
def boss_room():
    '''
        Crea una habitación de jefe
    '''
    fight('final')

def enemy_room():
    '''
        Crea una habitación de enemigos
    '''
    fight('base')

def midboss_room():
    '''
        Crea una habitación de jefe intermedio
    '''
    fight('boss')

def puzzle_room():
    '''
        Crea una habitación de puzzle
    '''
    create_puzzle()

def create_puzzle():
    '''
        Crea un puzzle
    '''
    global riddles
    global riddles_options

    index = random.randint(0, len(riddles) - 1)
    riddle = riddles[index]
    options = riddles_options[index][0]
    answer = riddles_options[index][1]
    tries = 3


    delayed_print('Entras en una extraña habitación, y encuentras una placa que reza "A veces, no' +
                  ' saber algo puede resultar fatal". La puerta por la que pasaste se cierra. '+
                  'Estás atrapado y parece que no hay salida.')
    delayed_print('Lees atentamente el resto de la placa y te encuentras con una extraña pregunta:')
    delayed_print(riddle)
    iterate_options(options)
    choice=input_with_validation('¿Cuál es tu respuesta? ', 'Respuesta inválida, intenta de nuevo.',
                                   range(1, len(options) + 1))
    choice = choice - 1
    while choice != answer and tries > 0:
        tries -= 1
        delayed_print(f'Respuesta incorrecta, te quedan {tries} intentos.')
        if tries > 0:
            choice=input_with_validation('¿Cuál es tu respuesta? ',
                                         'Respuesta inválida, intenta de nuevo.',
                                        range(1, len(options) + 1))
    if tries > 0:
        delayed_print('Has acertado la respuesta. ')
        riddles.pop(index)
        riddles_options.pop(index)
    else:
        delayed_print('La placa se rompe, dejandote sin salida. Parece que has fallado, y no queda nada por hacer.')
        time.sleep(1)
        death_menu('Has fallado el puzzle.')

def chest_room():
    '''
        Crea una habitación con un cofre
    '''
    global items
    delayed_print('¡Encuentras un cofre! Veamos que hay dentro...')
    possible_items = ['Poción de vida'] * 5 + ['Poción de fuerza'] * 2 + ['Poción de crítico'] * 2
    random_item = random.randint(0, len(possible_items) - 1)
    items.append(possible_items[random_item])

def chest_enemy_room():
    '''
        Crea una habitación con un cofre y un enemigo
    '''
    fight('base')
    chest_room()

def puzzle_enemy_room():
    '''
        Crea una habitación con un puzzle y un enemigo
    '''
    create_puzzle()
    delayed_print('Un enemigo se escabulle por las puertas recién abiertas', color='\033[91m')
    fight('base')

def puzzle_chest_room():
    '''
        Crea una habitación con un puzzle y un cofre
    '''
    create_puzzle()
    chest_room()

def double_enemy_room():
    '''
        Crea una habitación con dos enemigos'''
    fight('base')
    delayed_print('Un segundo enemigo aparece, parece que no estás solo...')
    fight('base')

def mark_room_as_visited(pos: list) -> None:
    '''
        Marca una habitación como visitada
    '''
    x, y = pos
    if '-' not in layout[y][x]:
        layout[y][x] = layout[y][x] + '-'
# ----- Inicio y controlador de juego ------
def start_menu():
    '''
        Menu de inicio
    '''
    options = ['Jugar', 'Salir']
    selection = menu(options, 'Seleccione una opción: ', 'Bievenido a DnD Rogue si fuera bueno')
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
    while END is False:
        display_map()
        print()
        pos = character_movement()
        check_room_type(pos)
        mark_room_as_visited(pos)
    end_credits()

def end_credits():
    '''
        Muestra los créditos finales
    '''
    os.system('cls')
    delayed_print('Gracias por jugar DnD Rogue si fuera bueno.')
    delayed_print('Desarrollado por: ')
    delayed_print('Aguirre, Simón.')
    delayed_print('Troitiño, Valentín.')
    delayed_print('Este proyecto es ficticio y fue creado con fines educativos. Cualquier similitud con nombres, personajes o eventos reales es pura coincidencia.')
    input('Presiona enter para salir...')


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
    '''
        Crea al jefe de nivel
        stats segun el index = ['base_attack', 'base_hp', 'crit_hit']'''
    enemy_stats = [50, 250, 70]
    return enemy_stats

def final_boss():
    '''
        Crea al jefe final
        stats segun el index = ['base_attack', 'base_hp', 'crit_hit']
    '''
    enemy_stats = [60, 350, 90]
    return enemy_stats

def base_enemy():
    '''
        Crea el enemigo base para la pelea
        stats segun el index = ['base_attack', 'base_hp', 'crit_hit']
    '''
    enemy_stats = [20, 125, 40]
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
    time.sleep(1)
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

def create_enemy_phrase(enemy_type) -> str:
    '''
        Genera un nombre aleatorio para un enemigo
    '''

    enemy_types = ['base', 'boss', 'final']
    enemy_types_functions = [create_base_enemy_name, create_boss_enemy_name, create_final_boss_name]

    enemy_name, enemy_phrase = enemy_types_functions[enemy_types.index(enemy_type)]()


    return enemy_name, enemy_phrase

def create_base_enemy_name():
    '''
        Genera un nombre aleatorio para un enemigo base
    '''
    base_enemy_names = ['zombie', 'esqueleto', 'goblin', 'orco', 'troll', 'cuervo', 'murciélago',
                        'hombre lobo', 'fantasma']
    base_enemy_phrases = [
    'Un olor putrefacto te alcanza al entrar a la habitación, un zombie comiendo un cadáver desde' + 
    ' el piso te mira... tu olor es mucho más delicioso.',
    'El crujir de huesos secos resuena en la oscuridad, un esqueleto emerge arrastrando una' +
    ' espada oxidada.',
    'Unos ojos brillantes te observan desde las sombras, un goblin se relame mientras apunta una' + 
    ' daga a tu dirección.',
    'Un rugido profundo retumba, un orco armado con un garrote gigantesco pisa fuerte mientras te' +
    ' observa con sed de sangre.',
    'El suelo tiembla bajo el peso de un troll enorme que se tambalea hacia ti, su aliento' +
    ' nauseabundo te envuelve.',
    'Un graznido agudo rompe el silencio, un cuervo negro como la noche te observa desde lo alto,'
    +' su pico con restos de su antigua presa.',
    'Unos chillidos agudos te ponen en alerta, un murciélago vuela en círculos, descendiendo' +
    ' rápidamente para atacar.',
    'La luna llena ilumina un par de ojos brillantes y colmillos afilados; un hombre lobo corre' +
    ' hacia ti a una velocidad inhumana.',
    'Un susurro helado recorre la habitación; un fantasma translúcido flota hacia ti, su rostro' +
    ' deformado por una eterna agonía.'
    ]
    index = random.randint(0, len(base_enemy_names) - 1)
    return base_enemy_names[index], base_enemy_phrases[index]

def create_boss_enemy_name():
    '''
    Genera un nombre aleatorio para un boss
    '''
    boss_enemy_names = ['Dragón', 'Lich', 'Demonio', 'Gigante', 'Vampiro']
    boss_enemy_phrases = [
            'Un rugido ensordecedor sacude la habitación, un Dragón emerge de las sombras, sus ojos llenos de furia.',
            'Una figura esquelética envuelta en túnicas oscuras aparece, un Lich levanta su báculo y te observa con desprecio.',
            'El aire se llena de azufre y fuego, un Demonio de piel roja y cuernos afilados se materializa ante ti.',
            'El suelo tiembla bajo el peso de un Gigante, su sombra cubre toda la habitación mientras te mira con ojos hambrientos.',
            'Una figura elegante y pálida se desliza en la oscuridad, un Vampiro te sonríe mostrando sus colmillos afilados.'
        ]
    index = random.randint(0, len(boss_enemy_names) - 1)
    return boss_enemy_names[index], boss_enemy_phrases[index]

def create_final_boss_name():
    '''
        Genera al boss final
    '''
    final_boss_name = 'Viajero sin nombre'
    red = '\033[91m'
    delayed_print("Una figura encapuchada se alza ante ti, su rostro oculto por las sombras.")
    delayed_print("Hay algo inquietantemente familiar en su postura, en las desgastadas marcas de batalla de sus ropas.")
    delayed_print("Alzas tu espada, decidido a no retroceder, pero una risa amarga resuena en la sala.")
    delayed_print("'¿Crees que puedes salir?' murmura, su voz cargada de cansancio y resentimiento.", color=red)
    delayed_print("Finalmente, baja la capucha, revelando un rostro humano, surcado de cicatrices y un par de ojos que alguna vez conocieron la esperanza.")
    delayed_print("'Yo también pensé que podía hacerlo. Yo también me enfrenté al guardián… y gané. Pero aquí estoy.'", color=red)
    delayed_print("'Esperando.'", delay_char=0.06, color=red)
    delayed_print("'Luchando.'", delay_char=0.06, color=red)
    delayed_print("'Atrapado.'", delay_char=0.06, color=red)
    delayed_print("El peso de sus palabras te golpea. Este guerrero fue el último viajero que logró escapar.")
    delayed_print("Alguien que venció, pero nunca se liberó. Ahora, es el nuevo juez de quienes buscan la salida.")
    delayed_print("Perpetuando un ciclo de sufrimiento que asegura que solo los más fuertes puedan cargar con la pesada ilusión de la libertad.")
    delayed_print("'Ven, libéranos a ambos.' dice mientras desenfunda su arma, su mirada cargada de pena y furia.", color=red)
    delayed_print("'o muere intentándolo.'", color=red)

    return final_boss_name, "El Viajero sin nombre te observa con ojos cansados, su arma lista para el combate."


# ------ Combate -----
def fight(enemy_type):
    '''
        Ejecuta la pelea
    '''
    global stats
    global key_item
    global END
    green = '\033[92m'
    red = '\033[91m'
    enemy_name, spawn_phrase = create_enemy_phrase(enemy_type)
    delayed_print(spawn_phrase, color=red)
    turn_choice = who_attacks_first()
    turn_functions = [player_turn, enemy_turn]
    enemy_stats = create_enemy(enemy_type)

    while enemy_stats[1] > 0 and stats[1] > 0:
        enemy_stats = turn_functions[turn_choice](enemy_stats)
        turn_choice = 1 - turn_choice
        os.system('cls')
        delayed_print(f'El enemigo tiene {enemy_stats[1]} de vida.', color=red)
        delayed_print(f'Tienes {stats[1]} de vida.', color=green)

    if stats[1] <= 0:
        death_menu(death_phrase(enemy_type))
        time.sleep(1)

    if enemy_type == 'boss':
        key_item.append('parte del medallón')
        delayed_print('Revisas el cadaver de tu enemigo. Era muy fuerte, quizá encuentras' +
                      ' algo importante...')
        delayed_print('Encuentras un pedazo de medallón, parece ser una parte de tres.')
        delayed_print(f'Tienes {len(key_item)} partes del medallón.')
    elif enemy_type == 'final':
        END = True
        final_boss_phrase()
        return
    delayed_print('¡Has vencido al enemigo!', color=green)
    delayed_print('Continuemos...')

    time.sleep(1)

def final_boss_phrase():
    delayed_print('El Viajero sin nombre cae al suelo, su arma resbalando de sus dedos.')
    delayed_print('Sombras lo envuelven, el alivio cruza su rostro.')
    delayed_print('Empiezas a correr hacia la salida que se abre, pero algo te detiene.')
    delayed_print('Esas mismas sombras se extienden hacia ti, envolviéndote en un abrazo frío.')
    delayed_print('El viajero no mentía.')

def death_phrase(enemy_type):
    '''
        Frase de muerte
    '''
    enemy_types = ['base', 'boss', 'final']
    death_phrases = ['Asesinado a manos de un simple esbirro... que vergüenza.',
                     'Tu vida se desvanece, el enemigo te ha vencido. Nunca tuviste una chance.',
                     'A las puertas de la salvación, caes derrotado. Todo fue en vano. Nunca' +
                    ' fuiste lo suficientemente fuerte.']
    return death_phrases[enemy_types.index(enemy_type)]

def who_attacks_first():
    '''
        Determina quien ataca primero
    '''
    global stats
    delayed_print('Probemos tu suerte...')
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
    quit(0)

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
    choice = 0
    objeto = 'Salir'
    enemy_attk, enemy_life,  enemy_crit = enemy_stats
    attk, life, crit = stats
    color = '\033[92m'
    options = ['Atacar', 'Objeto']
    while choice != 1 and objeto == 'Salir':
        os.system('cls')
        delayed_print('Es tu turno.', color=color)
        iterate_options(options, color=color)
        choice = input_with_validation('¿Qué deseas hacer? ', 'No puedes huir de tu destino.',
                                    range(1,len(options) + 1))
        if choice == 1:
            enemy_stats = player_attack(enemy_stats)
        elif choice == 2:
           objeto = items_menu()
    return enemy_stats

def items_menu():
    '''
        menu de items
    '''
    os.system('cls')
    global items
    items_options = list_copy(items)

    items_options.append('Salir')
    iterate_options(items_options)
    item = input_with_validation('¿Qué objeto deseas usar? ', 'No puedes usar eso.',
                                range(1,len(items_options) + 1))
    item_name = items_options[item - 1]
    if item_name != 'Salir':
        item = items[item - 1]
        use_item(item)
        items.remove(item)
    return item_name

def list_copy(array):
    '''
        Copia una lista
    '''
    array_copy = []
    for element in array:
        array_copy.append(element)
    return array_copy

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
        time.sleep(0.5)
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

def get_random_potion() -> str:
    '''
    Selecciona una poción aleatoria de la lista de pociones.
    '''
    life_potion = ['Poción de vida'] * 9
    attack_potion = ['Poción de fuerza'] * 3
    critical_potion = ['Poción de crítico'] * 3
    potions = life_potion + attack_potion + critical_potion

    index = random.randint(0, len(potions) - 1)
    return potions[index]

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
    '''
        Simula una ruleta visual con las tiradas de dados.
    '''
    spin_amount = random.randint(10, 20)
    end_color = '\033[0m'
    for _ in range(spin_amount):
        dice = random.randint(1, 20)
        if color:
            print(f'{color}{dice}{end_color} ', end='\r')
        else:
            print(f'{dice} ', end='\r')
        time.sleep(delay)
    print()
    return dice

# ------ Main ------
def main():
    '''
    Ejecuta el programa
    '''
    start_menu()


main()
