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
    ['RM','.','X','P','B'],
    ['P','.','P','.','.'],
    ['X','P','+S','P','RM'],
    ['P','.','P','.','X'],
    ['RM','P','X','P','P'],
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
    layout = LAYOUT_2
    for row in layout:
        for cell in row:
            if '+' in cell:
                actual_row = layout.index(row)
                actual_cell = row.index(cell)
    return actual_cell, actual_row

def check_available_ways(current_pos):
    '''
        Revisa las opciones de movimiento disponibles
    '''
    actual_cell = current_pos[0]
    actual_row = current_pos[1]

    move_options = []
    layout = LAYOUT_2
    bottom_row_index = len(layout) - 1
    rightmost_cell_index = len(layout[actual_row])
    
    if actual_row < bottom_row_index:
        if layout[actual_row + 1][actual_cell] != '.':
            move_options.append('abajo')
    if actual_row > 0:
        if layout[actual_row - 1][actual_cell] != '.':
            move_options.append('arriba')
    if actual_cell > 0:
        if layout[actual_row][actual_cell + 1] != '.':
            move_options.append('derecha')
    if actual_cell > rightmost_cell_index:
        if layout[actual_row][actual_cell - 1] != '.':
            move_options.append('izquierda')
    print(move_options)
    
    return move_options

def move_input(options, current_pos):
    '''
    Input para moverse
    '''
    for i in range(len(options)):
        print(str(i+1) + '. ' + options[i])
    choice= input_with_validation('¿Para donde vas? ', 'Ah, buscando burlar el sendero, ¿crees que el destino se distrae tan fácilmente?',range(1,len(options)+1))
    index = options[choice-1]
    new_pos = character_movement(index, current_pos)
    return new_pos

def character_movement(index, current_pos):
    '''
        Funcion que mueve al personaje
    '''
    
    x_change = [0, 0, -2, 2]
    y_change = [2, -2, 0, 0]
    x, y = current_pos[0], current_pos[1]
    x += x_change[index]
    y += y_change[index]

    current_pos = [x, y]

    return current_pos

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
    while True:

        current_pos = check_current_pos()
        new_pose = move_input(check_available_ways(current_pos), current_pos)

# ------ Combate -----
def spawn():
    '''a'''
    character = [crit_hit]

def crit_hit():
    '''a'''

def main():
    """
    main qcyo
    """
    start_menu()


main()
#check_available_ways()

# input_with_validation("Ingrese:","int", [1, 4])
#game()
