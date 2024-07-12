import pygame
from funciones import *
from settings import *
from resources import *
from game import game_loop
from pygame.locals import *
# Inicializar Pygame
pygame.init()
pygame.display.set_icon(pygame.image.load("./src/assets/img/icon.png"))


# Configuración de pantalla

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Heaven Conquest")
clock = pygame.time.Clock()


sprite_boton_green = obtener_frames_escalados_sin_bordes(boton_green, 3,6)
sprite_boton_yellow = obtener_frames_escalados_sin_bordes(boton_yellow, 3,5)
sprite_boton_yellow_grande = obtener_frames_escalados_sin_bordes(boton_yellow, 3,6)
sprite_boton_gray = obtener_frames_escalados_sin_bordes(boton_gray, 3,5)

pygame.mixer.music.load(musica["menu_music"])
pygame.mixer.music.play(-1)

fuente_titulo = pygame.font.Font(fuentes["fuente_titulo"], size_titulo)
titulo = fuente_titulo.render(f"Heaven Conquest", antialiasing, color_letras)
fuente_texto = pygame.font.Font(fuentes["fuente_texto"], size_texto)
fuente_botones_grandes = pygame.font.Font(fuentes["fuente_texto"], size_botones_grandes)
fuente_botones_medianos = pygame.font.Font(fuentes["fuente_texto"], size_botones_medianos)
fuente_botones_chicos = pygame.font.Font(fuentes["fuente_texto"], 20)
fuente_score = pygame.font.Font(fuentes["fuente_texto"], size_score)

posicion_boton_start = (SCREEN_WIDTH // 2 - sprite_boton_green[0].get_width() // 2, 290)
posicion_boton_settings = (SCREEN_WIDTH // 2 - sprite_boton_yellow[0].get_width() // 2, 400)
posicion_boton_quit = (SCREEN_WIDTH // 2 - sprite_boton_gray[0].get_width() // 2, 510)
posicion_boton_scores = (950, 600)

# Pantalla principal
def main_menu(SCREEN: pygame.Surface, flag_mute: bool):
    """Pantalla principal

    Args:
        SCREEN (pygame.Surface): Pantalla
        flag_mute (bool): Flag de silencio
    """
    click, hove = None, None
    hovered, clicked, flag_mute = False, False, False


    while is_running:
        mouse_over_button = False
        mostrar_fondo(SCREEN, fondo_menu)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            if event.type == KEYDOWN:
                if event.key == K_m:
                    flag_mute = not flag_mute

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = event.pos
            if event.type == MOUSEMOTION:
                hove = event.pos
                    

        hovered, clicked = draw_button_imagen(hove, click, SCREEN, posicion_boton_start, sprite_boton_green, "Start", fuente_botones_grandes, BLACK)
        if hovered:
            mouse_over_button = True
        if clicked:
            pygame.mixer.music.unload()
            game_loop(SCREEN, flag_mute)

        hovered, clicked = draw_button_imagen(hove, click, SCREEN, posicion_boton_settings, sprite_boton_yellow, "Settings", fuente_botones_medianos, BLACK)
        if hovered:
            mouse_over_button = True
        if clicked:
            config_screen(SCREEN, flag_mute)

        hovered, clicked = draw_button_imagen(hove, click, SCREEN, posicion_boton_quit, sprite_boton_gray, "Quit", fuente_botones_medianos, BLACK)
        if hovered:
            mouse_over_button = True
        if clicked:
            quit_game()

        hovered, clicked = draw_button_imagen(hove, click, SCREEN, posicion_boton_scores, sprite_boton_yellow, "Scores", fuente_botones_medianos, BLACK)
        if hovered:
            mouse_over_button = True
        if clicked:
            score_screen(SCREEN, flag_mute)

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) if mouse_over_button else pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.mixer.music.pause() if flag_mute else pygame.mixer.music.unpause()

        SCREEN.blit(titulo, (150, 50))
        pygame.display.flip()
        clock.tick(FPS)


def score_screen(SCREEN: pygame.Surface, flag_mute: bool):
    """Pantalla de Scores

    Args:
        SCREEN (pygame.Surface): Pantalla
        flag_mute (bool): Flag de silencio
    """
    click, hove = None, None
    hovered, clicked = False, False

    while True:
        mostrar_fondo(SCREEN, fondo_menu)
        mouse_over_button = False
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            if event.type == KEYDOWN:
                if event.key == K_m:
                    flag_mute = not flag_mute

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = event.pos
            if event.type == MOUSEMOTION:
                hove = event.pos
        hovered, clicked = draw_button_imagen(hove, click, SCREEN, (SCREEN_WIDTH // 2 - sprite_boton_gray[0].get_width() // 2, 600), sprite_boton_gray, "Volver", fuente_botones_medianos, BLACK)
        if hovered:
            mouse_over_button = True
        if clicked:
            main_menu(SCREEN, flag_mute)
            break
        mostrar_high_scores(SCREEN, fuente_score)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) if mouse_over_button else pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.mixer.music.pause() if flag_mute else pygame.mixer.music.unpause()
        pygame.display.flip()

def config_screen(SCREEN: pygame.Surface, flag_mute: bool):
    """Pantalla de configuracion

    Args:
        SCREEN (pygame.Surface): Pantalla
        flag_mute (bool): Flag de silencio
    """
    click, hove = None, None
    hovered, clicked = False, False
    music_off = False
    while True:
        mostrar_fondo(SCREEN, fondo_menu)
        mouse_over_button = False

        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            if event.type == KEYDOWN:
                if event.key == K_m:
                    flag_mute = not flag_mute

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = event.pos
            if event.type == MOUSEMOTION:
                hove = event.pos

        if music_off:
            hovered, clicked = draw_button_imagen(hove, click, SCREEN, (SCREEN_WIDTH // 2 - sprite_boton_yellow[0].get_width() // 2, 200), sprite_boton_yellow, "Music:ON", fuente_botones_medianos, BLACK)
            mouse_over_button = True if hovered else False
            if clicked:
                pygame.mixer.music.stop()
                music_off = False
                click = None
                
        else:
            hovered, clicked = draw_button_imagen(hove, click, SCREEN, (SCREEN_WIDTH // 2 - sprite_boton_yellow[0].get_width() // 2, 200), sprite_boton_yellow, "Music:OFF", fuente_botones_medianos, BLACK)
            mouse_over_button = True if hovered else False
            if clicked:
                pygame.mixer.music.play(-1)
                music_off = True
                click = None

        hovered, clicked = draw_button_imagen(hove, click, SCREEN, (SCREEN_WIDTH // 2 - sprite_boton_yellow_grande[0].get_width() // 2, 300), sprite_boton_yellow_grande, "Borrar Scores", fuente_botones_chicos, BLACK)
        mouse_over_button = True if hovered else False
        if clicked:
            borrar_scores_csv("scores.csv")
            click = None


        hovered, clicked = draw_button_imagen(hove, click, SCREEN, (SCREEN_WIDTH // 2 - sprite_boton_gray[0].get_width() // 2, 600), sprite_boton_gray, "Volver", fuente_botones_medianos, BLACK)
        mouse_over_button = True if hovered else False
        main_menu(SCREEN, flag_mute) if clicked else None
        if clicked:
            main_menu(SCREEN, flag_mute)
            break

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) if mouse_over_button else pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.mixer.music.pause() if flag_mute else pygame.mixer.music.unpause()
        pygame.display.flip()

if __name__ == "__main__":
    main_menu(SCREEN, flag_mute)
