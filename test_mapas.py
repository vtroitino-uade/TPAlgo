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

ANCHO_HABITACION = 9
ALTO_HABITACION = 5
DIMENSION_PLANO = 5

mapa = []
for _ in range(ALTO_HABITACION * DIMENSION_PLANO):
    mapa.append([' '] * (ANCHO_HABITACION * DIMENSION_PLANO))

def generar_plano_aleatorio() -> list:
    '''
        Selecciona un plano aleatorio y lo prepara para su representación.
    '''
    plano_1 = [
        ['.RM','.','X','.P','.B'],
        ['.P','.','.P','.','.'],
        ['X','.P','X','.P','.RM'],
        ['.P','.','.P','.','.'],
        ['+S','.P','X','.P','.RM'],
    ]
    plano_2 = [
        ['.RM','.','X','.P','.B'],
        ['.P','.','.P','.','.'],
        ['X','.P','+S','.P','.RM'],
        ['.P','.','.P','.','X'],
        ['.RM','.P','X','.P','.P'],
    ]
    plano_3 = [
        ['.RM','.','X','.P','.B'],
        ['.P','.','.P','.','.'],
        ['X','.P','X','.P','.RM'],
        ['.P','.','.P','.','.'],
        ['+S','.P','X','.P','.RM'],
    ]

    planos = [ plano_1, plano_2, plano_3 ]
    plano_seleccionado = random.choice(planos)

    posibles_habitaciones = ['.RE', '.RP', '.RC', '.REC', '.RPE', '.REE', '.RPC']

    for y, fila in enumerate(plano_seleccionado):
        for x, casilla in enumerate(fila):
            if casilla == 'X':
                plano_seleccionado[y][x] = random.choices(posibles_habitaciones,
                                              weights=[0.5, 0.1, 0.1, 0.1, 0.05, 0.1, 0.05],
                                              k=1)[0]
    return plano_seleccionado

plano = generar_plano_aleatorio()

def generar_mapa():
    '''
        Genera el mapa completo.
    '''
    for y, fila in enumerate(plano):
        for x, _ in enumerate(fila):
            crear_habitacion(plano[y][x], x, y)

def crear_habitacion(tipo_casilla: str, plano_x: int, plano_y: int) -> list:
    '''
        Crea una habitación dentro del mapa.
    '''
    mapa_x = plano_x * ANCHO_HABITACION
    mapa_y = plano_y * ALTO_HABITACION

    pared_horizontal = ' '
    pared_vertical = ' '
    borde = ' '

    if tipo_casilla.startswith('.'):
        pared_horizontal = ' '
        pared_vertical = ' '
        borde = ' '
    elif tipo_casilla.count('S'):
        pared_horizontal = '-'
        pared_vertical = '|'
        borde = '@'
    elif tipo_casilla.count('B'):
        pared_horizontal = '%'
        pared_vertical = '%'
        borde = '6'
    elif tipo_casilla.count('RM'):
        pared_horizontal = '-'
        pared_vertical = '|'
        borde = 'M'
    elif tipo_casilla.count('R'):
        pared_horizontal = '-'
        pared_vertical = '|'
        borde = '°'

    if tipo_casilla.startswith('+'):
        mapa[mapa_y + 2][mapa_x + 4] = '8'
    else:
        mapa[mapa_y + 2][mapa_x + 4] = ' '


    mapa[mapa_y][mapa_x] = borde
    mapa[mapa_y][(mapa_x + ANCHO_HABITACION) - 1] = borde
    mapa[(mapa_y + ALTO_HABITACION) - 1][mapa_x] = borde
    mapa[(mapa_y + ALTO_HABITACION) - 1][(mapa_x + ANCHO_HABITACION) - 1] = borde

    for x in range(mapa_x + 1, mapa_x + ANCHO_HABITACION - 1):
        mapa[mapa_y][x] = pared_horizontal
        mapa[mapa_y + (ALTO_HABITACION - 1)][x] = pared_horizontal

    for y in range(mapa_y + 1, mapa_y + ALTO_HABITACION - 1):
        mapa[y][mapa_x] = pared_vertical
        mapa[y][(mapa_x + ANCHO_HABITACION) - 1] = pared_vertical

def mostrar_mapa() -> None:
    '''
        Muestra el mapa en la pantalla.
    '''
    generar_mapa()
    for fila in mapa:
        for casilla in fila:
            print(casilla, end='')
        print()

mostrar_mapa()
