import pygame

# Pantalla
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
FPS = 60
piso = 640
maximo_salto = 200
# Tamaño de fuentes
size_titulo = 80
size_texto = 35
size_countdown = 70
size_score = 20
size_botones_medianos = 25
size_botones_grandes = 35
antialiasing = True

# Colores
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
color_letras = BLACK
color_fondo_letras = (252, 198, 100)



# Flags generales
is_running = True
gravedad_knight = False
gravedad_demon = False
flag_mute = False
flag_pausa = False
countdown_activada = False
countdown = 3

ultima_actualizacion = pygame.time.get_ticks()
ultima_actualizacion_demon = pygame.time.get_ticks()

frames_speed = {
    "idle": 1000,
    "walk": 100,
    "attack": 40,
    "hurt": 70,
    "death": 40
}
