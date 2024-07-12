import pygame
from funciones import cargar_datos_desde_json

try:
    paths = cargar_datos_desde_json("paths.json")
except FileNotFoundError:
    print("No se encontró el archivo paths.json")

fondos = paths["fondos"]
fuentes = paths["fuentes"]
musica = paths["musica"]
sonidos = paths["sonidos"]
botones = paths["botones"]
sprites_knight_path = paths["sprites_knight"]
sprites_demon_path = paths["sprites_demon"]

sprites_knight = {
    "idle" : pygame.image.load(sprites_knight_path["idle"]),
    "walk" : pygame.image.load(sprites_knight_path["walk"]),
    "attack" : pygame.image.load(sprites_knight_path["attack"]),
    "hurt" : pygame.image.load(sprites_knight_path["hurt"]),
    "death" : pygame.image.load(sprites_knight_path["death"])
}

sprites_demon = {
    "idle" : pygame.image.load(sprites_demon_path["idle"]),
    "walk" : pygame.image.load(sprites_demon_path["walk"]),
    "attack" : pygame.image.load(sprites_demon_path["attack"]),
    "hurt" : pygame.image.load(sprites_demon_path["hurt"]),
    "death" : pygame.image.load(sprites_demon_path["death"])
}
fondo_menu = pygame.image.load(fondos["fondo_menu"])
boton_green = pygame.image.load(botones["green"])
boton_yellow = pygame.image.load(botones["yellow"])
boton_gray = pygame.image.load(botones["gray"])
fondo_menu_juego = pygame.image.load(fondos["fondo_menu_juego"])