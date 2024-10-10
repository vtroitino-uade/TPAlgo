"""
hola
"""

import random
import os
import time


def DelayedPrint(*values, delayChar=0.03, delayLine=0.3):
    '''
        Imprime caracteres uno a la vez.
    '''
    for character in "".join(values):
        print(
            character, end=""
        )
        time.sleep(delayChar)

    # time.sleep(``
    #     delayLine
    # )
    print()


def story(chapter):
    '''
        Textos relevantes para la historia
    '''
    text = [
        f"Atrapado en las profundidades de unas catacumbas ancestrales, el viajero despertó sin recordar cómo había llegado allí. La única salida estaba sellada por una magia oscura y antigua. En la penumbra, una voz resonó advirtiendo que tres seres poderosos custodiaban su libertad. Para escapar, debía encontrarlos y enfrentarse a sus pruebas.",


    ]
    DelayedPrint(text[chapter])

def input_with_validation(input_text: str, convert_to="", input_range=None) -> any:
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
        var = eval(f"{convert_to}({var})")
        if not input_range and var not in range(input_range[0], input_range[1]):
            print("Ingreso invalido. Intente de nuevo.")
            continue

        return var


def iterate_options(options):
    """
        Itera varias opciones en menúes que lo requieran
    """
    for i, option in enumerate(options, 1):
        time.sleep(0.3)
        print(f"{i}. {option}")


def menu(options, input_text, header) -> None:
    """
        Muestra el menú de inicio y pide un input
    """
    response = "error"

    os.system("cls")
    print(header)
    iterate_options(options)
    time.sleep(0.3)
    while response == "error":
        response = input_with_validation(input_text, "int", [1, len(options)])
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

    create_map()
def create_available_rooms():
    '''
    Crea las habitaciones disponibles
    '''
    room_events = ['chest', 'enemy', 'puzzle']
    room_numbers = range(1,10)
def create_map():
    '''
    Crea el mapa
    '''
    available_rooms = create_available_rooms()


def main():
    """
    main qcyo
    """
    start_menu()


# main()
# input_with_validation("Ingrese:","int", [1, 4])
game()
