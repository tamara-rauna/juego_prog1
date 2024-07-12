import pygame
from settings import *
import sys
from os import path
import json
pygame.init()

def is_button_hovered(hove:tuple, button_rect:pygame.Rect)->bool:
    """Comprueba si el mouse esta sobre el boton

    Args:
        hove (tuple): Posicion del mouse
        button_rect (pygame.Rect): Posicion del boton

    Returns:
        bool: True si el mouse esta sobre el boton
    """
    if hove != None:
        return punto_en_rectangulo(hove, button_rect)

def is_button_clicked(click:tuple, button_rect:pygame.Rect)->bool:
    """Comprueba si el mouse ha presionado el boton

    Args:
        click (tuple): Posicion del mouse
        button_rect (pygame.Rect): Posicion del boton

    Returns:
        bool: True si el mouse ha presionado el boton
    """
    if click != None:
        return punto_en_rectangulo(click, button_rect)

def draw_button_imagen(hove:tuple, click:tuple, superficie:pygame.Surface, posicion:tuple, sprite_boton:list, texto:str, fuente:pygame.font.Font, color_letras:tuple)->tuple:
    """Dibuja un boton

    Args:
        hove (tuple): posicion del mouse
        click (tuple): posicion del mouse
        superficie (pygame.Surface): Pantalla
        posicion (tuple): Posicion del boton
        sprite_boton (list): Sprites
        texto (str): Texto del boton
        fuente (pygame.font.Font): Fuente
        color_letras (tuple): Color

    Returns:
        tuple: Devuelve una tupla de dos valores, el primero indica si el mouse esta sobre el boton y el segundo si el mouse ha presionado el boton
    """
    
    sprites = sprite_boton
    button_rect = sprites[0].get_rect(topleft=posicion)
    hovered = is_button_hovered(hove, button_rect)
    clicked = is_button_clicked(click, button_rect)
    if clicked:
        superficie.blit(sprites[1], posicion)
    elif hovered:
        superficie.blit(sprites[2], posicion)
    else:
        superficie.blit(sprites[0], posicion)

    text_surface = fuente.render(texto, True, color_letras)
    text_rect = text_surface.get_rect(center=button_rect.center)
    superficie.blit(text_surface, text_rect)

    return hovered, clicked

def mostrar_fondo(superficie:pygame.Surface, imagen:pygame.Surface)->None:
    """Muestra el fondo de la pantalla

    Args:
        superficie (pygame.Surface): Pantalla
        imagen (pygame.Surface): Fondo
    """
    imagen = pygame.transform.scale(imagen, (SCREEN_WIDTH, SCREEN_HEIGHT))
    superficie.blit(imagen, (0,0))

def punto_en_rectangulo(punto:tuple, rect:pygame.Rect) -> bool:
    """Comprueba si un punto se encuentra en un rectangulo

    Args:
        punto (tuple): Punto
        rect (pygame.Rect): Rectangulo

    Returns:
        bool: True si el punto se encuentra en el rectangulo
    """
    x, y = punto
    return rect.left <= x <= rect.right and rect.top <= y <= rect.bottom

def eliminar_bordes_transparentes(imagen:pygame.Surface) -> pygame.Surface:
    """Elimina los bordes transparentes de una imagen

    Args:
        imagen (pygame.Surface): Imagen

    Returns:
        pygame.Surface: Imagen
    """
    rect = imagen.get_bounding_rect()
    imagen_recortada = imagen.subsurface(pygame.Rect(rect))
    return imagen_recortada
def mostrar_imagen(superficie:pygame.Surface, imagen:pygame.Surface, coordenadas:tuple) -> None:
    """Muestra una imagen

    Args:
        superficie (pygame.Surface): Pantalla
        imagen (pygame.Surface): Imagen
        coordenadas (tuple): Posicion
    """

    rect_imagen = imagen.get_rect(center=coordenadas)
    superficie.blit(imagen, rect_imagen.topleft)

def escalar_imagen(imagen:pygame.Surface, escala:float) -> pygame.Surface:
    """Escala una imagen    

    Args:
        imagen (pygame.Surface): Imagen
        escala (float): Escala

    Returns:
        pygame.Surface: Imagen escalada
    """
    size = (int(imagen.get_width() * escala), int(imagen.get_height() * escala))
    imagen = pygame.transform.scale(imagen,size)
    return imagen

def obtener_frame(imagen:pygame.Surface, frames:int) -> list:
    """Devuelve una lista de frames a partir de un SpriteSheet

    Args:
        imagen (pygame.Surface): SpriteSheet
        frames (int): Total de frames

    Returns:
        list: Lista de frames
    """
    lista_animacion = []
    cant_frames = frames
    alto_frame = imagen.get_height()
    ancho_frame = imagen.get_width() / frames
    for frame in range (cant_frames):
        frame = imagen.subsurface(pygame.Rect(frame * ancho_frame, 0, ancho_frame, alto_frame))
        lista_animacion.append(frame)
    return lista_animacion

def obtener_frames_escalados(imagen:pygame.Surface, frames:int, escala:float) -> list:
    """Devuelve una lista de frames escalados a partir de un SpriteSheet

    Args:
        imagen (pygame.Surface): SpriteSheet
        frames (int): Total de frames
        escala (float): Escala

    Returns:
        list: Lista de frames escalados
    """
    lista_animacion = []
    lista_animacion = obtener_frame(imagen, frames)
    for frame in range(len(lista_animacion)):
        lista_animacion[frame] = escalar_imagen(lista_animacion[frame], escala)
    return lista_animacion

def cargar_datos_desde_json(nombre_archivo_json:str) -> list:
    """Obtiene los datos de un archivo json y lo asigna a una lista

    Args:
        nombre_archivo_json (str): Nombre del archivo que contiene los datos

    Returns:
        list: Devuelve una lista con los datos que se obtuvieron del archivo
    """
    with open(get_path_actual(nombre_archivo_json), "r", encoding = "UTF-8") as archivo:
        return json.load(archivo)

def escribir_json(nombre_archivo_destino:str, lista_origen:list) -> None:
    """Escribe los datos en un archivo json, si no existe lo crea, y si existe lo sobreescribe

    Args:
        nombre_archivo_destino (str): Nombre del archivo a crear o modificar
        lista_origen (list): Lista que contine los datos a escribir
    """
    with open(get_path_actual(nombre_archivo_destino), "w", encoding ="utf-8") as archivo:
        json.dump(lista_origen, archivo, indent = 4)
def obtener_frames_escalados_sin_bordes(imagen:pygame.Surface, frames:int, escala:float) -> list:
    """Obtiene una lista de frames escalados sin bordes transparentes

    Args:
        imagen (pygame.Surface): SpriteSheet
        frames (int): Total de frames
        escala (float): Escala

    Returns:
        list: Lista de frames escalados sin bordes
    """
    lista_animacion = obtener_frames_escalados(imagen, frames, escala)
    for frame in range(len(lista_animacion)):
        lista_animacion[frame] = eliminar_bordes_transparentes(lista_animacion[frame])
    return lista_animacion
def quit_game()->None:
    """Finaliza el juego
    """
    pygame.quit()
    sys.exit()

def punto_en_rectangulo(punto:tuple, rect:pygame.Rect)->bool:
    """Comprueba si un punto se encuentra dentro de un rectangulo

    Args:
        punto (tuple): Punto
        rect (pygame.Rect): Rectangulo

    Returns:
        bool: True si el punto se encuentra en el rectangulo
    """
    x, y = punto
    return rect.left <= x <= rect.right and rect.top <= y <= rect.bottom

def detectar_colision(rect_1: pygame.Rect, rect_2: pygame.Rect) -> bool:
    """Comprueba si dos rectangulos colisionan

    Args:
        rect_1 (pygame.Rect): Rectangulo 1
        rect_2 (pygame.Rect): Rectangulo 2

    Returns:
        bool: True si colisionan
    """

    return punto_en_rectangulo(rect_1.topleft, rect_2) or punto_en_rectangulo(rect_1.topright, rect_2) or punto_en_rectangulo(rect_1.bottomleft, rect_2) or punto_en_rectangulo(rect_1.bottomright, rect_2)


def atacar(personaje_rect:pygame.Rect,flip:bool, enemigo_rect:pygame.Rect, size_area:int) -> bool:
    """Crea un area de ataque para el personaje y comprueba si hay colision

    Args:
        personaje_rect (pygame.Rect): Personaje
        flip (bool): Flag de flip
        enemigo_rect (pygame.Rect): Enemigo
        size_area (int): Tamaño del area de ataque

    Returns:
        bool: True si logro herir al enemigo
    """
    if flip:
        area_ataque_personaje = pygame.Rect(personaje_rect.centerx - personaje_rect.width * size_area, personaje_rect.top, personaje_rect.width * size_area, personaje_rect.height)
    else:
        area_ataque_personaje = pygame.Rect(personaje_rect.centerx, personaje_rect.top, personaje_rect.width * size_area, personaje_rect.height)

    return detectar_colision(area_ataque_personaje, enemigo_rect)

def mostrar_texto(texto:str, cordenada:tuple, superficie:pygame.Surface, fuente:pygame.font.Font, color:tuple = color_letras, color_fondo:tuple = color_fondo_letras)->None:
    """Muestra un texto

    Args:
        texto (str): Texto
        cordenada (tuple): Posicion
        superficie (pygame.Surface): Pantalla
        fuente (pygame.font.Font): Fuente
        color (tuple, optional): Color del texto. Defaults to color_letras.
        color_fondo (tuple, optional): Color del fondo. Defaults to color_fondo_letras.
    """
    sticker = fuente.render(texto, True, color, color_fondo)
    rect = sticker.get_rect()
    rect.center = cordenada
    superficie.blit(sticker, rect)

def draw_health_bar(surface: pygame.Surface, health: int, x: int, y: int):
    """Dibuja una barra de vida

    Args:
        surface (pygame.Surface): Pantalla
        health (int): Salud
        x (int): Posicion X
        y (int): Posicion Y
    """
    ratio = health / 100
    pygame.draw.rect(surface, BLACK, (x-2, y-2, 400+4, 30+4))
    pygame.draw.rect(surface, RED, (x, y, 400, 30))
    pygame.draw.rect(surface, GREEN, (x, y, 400 * ratio, 30))

def draw_health_bars(SCREEN: pygame.Surface, fuente_score: pygame.font, score_knight: int, lifes_knight: int, score_demon: int, lifes_demon: int, health_knight: int, health_demon: int) -> None:
    """Dibuja las barras de vida, los scores y las vidas

    Args:
        SCREEN (pygame.Surface): Pantalla
        fuente_score (pygame.font): Fuente del score
        score_knight (int): Puntaje del Knight
        lifes_knight (int): Vidas del Knight
        score_demon (int): Puntaje del Demon
        lifes_demon (int): Vidas del Demon
        health_knight (int): Salud del Knight
        health_demon (int): Salud del Demon
    """
    mostrar_texto(f"Knight", (110, 20), SCREEN, fuente_score)
    draw_health_bar(SCREEN,health_knight, 50, 35)
    mostrar_texto(f"Score: {score_knight} | Lifes: {lifes_knight}", (240, 80), SCREEN, fuente_score)
    
    mostrar_texto(f"Demon", (1190, 20), SCREEN, fuente_score)
    draw_health_bar(SCREEN,health_demon, 840, 35)
    mostrar_texto(f"Score: {score_demon} | Lifes: {lifes_demon}", (1050, 80), SCREEN, fuente_score)


def swap_lista(lista: list, i: int, j: int) -> None:
    """Intercambia dos elementos de una lista

    Args:
        lista (list): Una lista
        i (int): Indice i
        j (int): Indice j
    """
    aux = lista[i]
    lista[i] = lista[j]
    lista[j] = aux

def mostrar_high_scores(SCREEN: pygame.Surface, fuente: pygame.font.Font)-> None:
    """Muestra el ranking de puntajes

    Args:
        SCREEN (pygame.Surface): Pantalla
        fuente (pygame.font.Font): Fuente del texto
    """
    
    ranking = cargar_datos_desde_csv("scores.csv")
    tam = len(ranking)
    posicion_score_y = 100
    for i in range(tam):
        ranking[i]["score"] = int(ranking[i]["score"])
    for i in range(tam - 1):
        for j in range(i + 1, tam):
            if ranking[i]["score"] > ranking[j]["score"]:
                swap_lista(ranking, i, j)
    pygame.draw.rect(SCREEN, color_fondo_letras, (SCREEN_WIDTH//2 - 250, 20, 500, 500))
    
    titulo_tabla = ["Nombre", "Puntaje"]
    mostrar_texto(f"{titulo_tabla[0]:^10}   {titulo_tabla[1]:^7}", (SCREEN_WIDTH // 2, 50), SCREEN, fuente)
    for i in range(len(ranking)):
        mostrar_texto(f"{ranking[i]["nombre_jugador"]:^10}    {ranking[i]["score"]:^7}", (SCREEN_WIDTH // 2, posicion_score_y + (40 * i)), SCREEN, fuente)
    pygame.draw.rect(SCREEN, (BLACK), (SCREEN_WIDTH//2-250, 70, 500, 4))
    pygame.draw.rect(SCREEN, (BLACK), (SCREEN_WIDTH//2, 20, 4, 500))

def show_winner(SCREEN: pygame.Surface, fuente_texto: pygame.font.Font, winner: str, score: int):
    """Pantalla de fin de juego

    Args:
        SCREEN (pygame.Surface): Pantalla
        fuente_texto (pygame.font.Font): Fuente del texto
        winner (str): Ganador
        score (int): Puntaje
    """

    if winner == "demon":
        mostrar_texto("Game over", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN, fuente_texto)
        mostrar_texto(f"Score: {score}", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN, fuente_texto)
        mostrar_texto(f"Ingrese su nombre en la consola", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN, fuente_texto)
    else:
        mostrar_texto("Congrats", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN, fuente_texto)
        mostrar_texto(f"Score: {score}", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN, fuente_texto)
        mostrar_texto(f"Ingrese su nombre en la consola", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN, fuente_texto)

def get_path_actual(nombre_archivo:str) -> str:
    """Obtiene el directorio actual y el concatena con el nombre que se le quiere dar al archivo

    Args:
        nombre_archivo (str): nombre que se le quiere dar al archivo 

    Returns:
        str: Devuelve la ruta del archivo
    """
    directorio_actual = path.dirname(__file__)
    return path.join(directorio_actual, nombre_archivo)

def cargar_datos_desde_csv(nombre_archivo_csv:str) -> list:
    """Obtiene los datos de un archivo csv y lo asigna a una lista

    Args:
        nombre_archivo_csv (str): Nombre del archivo que contiene los datos

    Returns:
        list: Devuelve una lista con los datos que se obtuvieron del archivo
    """
    with open(get_path_actual(nombre_archivo_csv), "r", encoding = "UTF-8") as archivo:
        lista = []
        encabezado = archivo.readline().strip("\n").split(",")
        for linea in archivo.readlines():
            diccionario = {}
            linea = linea.strip("\n").split(",")
            for i in range(len(encabezado)):
                diccionario[encabezado[i]] = linea[i]
            lista.append(diccionario)
    return lista

def escribir_csv(nombre_archivo_destino:str, lista_origen:list) -> None:
    """Escribe los datos en un archivo csv, si no existe lo crea, y si existe lo sobreescribe

    Args:
        nombre_archivo_destino (str): Nombre del archivo a crear o modificar
        lista_origen (list): Lista que contine los datos a escribir
    """
    with open(get_path_actual(nombre_archivo_destino), "w", encoding ="utf-8") as archivo:
        keys = list(lista_origen[0].keys())
        encabezado = ",".join(keys) + "\n"
        archivo.write(encabezado)
        for diccionario in lista_origen:
            linea = []
            for key in keys:
                linea.append(diccionario[key])
            linea = ",".join(linea) + "\n"
            archivo.write(linea)

def borrar_scores_csv(nombre_archivo_destino:str="scores.csv") -> None:
    """Borra el contenido del archivo "scores.csv" y coloca el encabezado

    Args:
        nombre_archivo_destino (str): Nombre del archivo al que se le quiere borrar el contenido
    """
    with open(get_path_actual(nombre_archivo_destino), "w", encoding ="utf-8") as archivo:
        encabezado = "nombre_jugador,score" + "\n"
        archivo.write(encabezado)

def actualizar_frame(current_time:int, ultima_actualizacion:int, frames_speed:int, frame_actual:int, estado:str, total_de_frames:int, personaje_sprites:dict) -> tuple:
    """Actualiza el frame del personaje

    Args:
        current_time (int): Tiempo actual
        ultima_actualizacion (int): Tiempo de la ultima actualizaciòn
        frames_speed (int): Velocidad de actualizaciòn
        frame_actual (int): Frame actual
        estado (str): Estado del personaje
        total_de_frames (int): Total de frames
        personaje_sprites (dict): Sprites del personaje

    Returns:
        tuple: Devuelve el frame actual, la ultima actualizaciòn y la imagen del personaje
    """
    if current_time - ultima_actualizacion >= frames_speed:
        frame_actual += 1
        ultima_actualizacion = current_time
        if frame_actual >= total_de_frames - 1:
            frame_actual = 0
    personaje_image = personaje_sprites[estado][frame_actual]
    return frame_actual, ultima_actualizacion, personaje_image


def gravedad(gravedad_personaje:bool, personaje_velocity_y:int, gravity_personaje:int, personaje_rect:pygame.Rect)->tuple:
    """Controla el movimiento vertical de un personaje

    Args:
        gravedad_personaje (bool): Flag de gravedad
        personaje_velocity_y (int): Posicion del personaje en el eje y
        gravity_personaje (int): Velocidad del personaje en el eje y
        personaje_rect (pygame.Rect): Rect del personaje

    Returns:
        tuple: Devuelve la velocidad del personaje, la flag gravedad y el rect del personaje
    """
    if gravedad_personaje:
        personaje_velocity_y += gravity_personaje
        personaje_rect.y += personaje_velocity_y
        if personaje_rect.bottom >= piso:
            personaje_rect.bottom = piso
            personaje_velocity_y = 0
            gravedad_personaje = False
    return personaje_velocity_y, gravedad_personaje, personaje_rect