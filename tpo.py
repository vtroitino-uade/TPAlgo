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

def delayed_print(values, delay_char=0.03):
    '''
        Imprime caracteres uno a la vez.
    '''
    for character in "".join(values):
        print(
            character, end=""
        )
        time.sleep(delay_char)
    print()


def story(chapter):
    '''
        Textos relevantes para la historia
    '''
    text = [
        f"Atrapado en las profundidades de unas catacumbas ancestrales, el viajero despertó sin recordar cómo había llegado allí. La única salida estaba sellada por una magia oscura y antigua. En la penumbra, una voz resonó advirtiendo que tres seres poderosos custodiaban su libertad. Para escapar, debía encontrarlos y enfrentarse a sus pruebas.",


    ]
    delayed_print(text[chapter])

def input_with_validation(input_text: str, input_range=None) -> any:
    """
        Valida el input segun los parametros
    """

    while True:
        var = input(input_text)
        if not var.isdigit():
            print("Ingreso invalido. Intente de nuevo.")
            time.sleep(1)
            os.system("cls")
            continue
        if not input_range and var not in range(input_range[0], input_range[1]):
            print("Ingreso invalido. Intente de nuevo.")
            continue

        return int(var)


def iterate_options(options):
    """
        Itera varias opciones en menúes que lo requieran
    """
    for i in range(len(options)):
        print(f"{i+1}. {options[i]}")


def menu(options, input_text, header) -> None:
    """
        Muestra el menú de inicio y pide un input
    """
    response = "error"

    os.system("cls")
    print(header)
    iterate_options(options)
    time.sleep(0.3)
    response = input_with_validation(input_text, [1, len(options)])

    return response

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

    #create_map()
def create_map():
    layout = random.choice(LAYOUTS)
    return layout



def main():
    """
    main qcyo
    """
    start_menu()


main()
# input_with_validation("Ingrese:","int", [1, 4])
#game()
