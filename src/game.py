import pygame
from settings import *
from demon_ia import *
from funciones import *
from pygame.locals import *

pygame.init()

pygame.display.set_icon(pygame.image.load("./src/assets/img/icon.png"))
boton_green = pygame.image.load(botones["green"])
sprite_boton_green = obtener_frames_escalados_sin_bordes(boton_green, 3,5)
boton_gray = pygame.image.load(botones["gray"])
sprite_boton_gray = obtener_frames_escalados_sin_bordes(boton_gray, 3,5)
fuente_botones_medianos = pygame.font.Font(fuentes["fuente_texto"], size_botones_medianos)


def game_loop(SCREEN: pygame.Surface, flag_mute: bool):
    """Loop del juego

    Args:
        SCREEN (pygame.Surface): Pantalla del juego
        flag_mute (bool): Bandera de silencio
    """
    # Variables generales
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)   
    clock = pygame.time.Clock()
    pygame.display.set_caption("Heaven Conquest")
    fondo_juego = pygame.image.load(fondos["fondo_juego"]).convert_alpha()
    COUNTDOWNEVENT = USEREVENT + 1
    COUNTDOWNEVENTROUND = USEREVENT + 2
    DEADTIMER = USEREVENT + 3
    pygame.time.set_timer(COUNTDOWNEVENT, 1000)
    pygame.time.set_timer(COUNTDOWNEVENTROUND, 1000)
    pygame.time.set_timer(DEADTIMER, 1000)
    jugando = True
    game_over = False
    width_fondo_juego = 5120
    scroll_x = width_fondo_juego // 2
    tiempo_de_espera = 3
    countdown_activada = True
    countdown = 3
    # Knight
    knight_alive = True
    knight_attacking = False
    knight_image_flip = False
    knight_velocity_y = 0
    area_ataque_knight = 3
    estado_knight = "idle"
    frame_knight = 0
    health_knight = 100
    jump_speed_knight = -25
    lifes_knight = 3
    limite_izquierdo_screen = SCREEN_WIDTH * 0.25
    speed_knight = 20
    gravity_knight = 1
    gravedad_knight = False

    # Demon
    decision_demon = "demon_idle"
    estado_demon = "idle"
    demon_alive = True
    demon_image_flip = False
    demon_velocity_y = 0
    area_ataque_demon = 0.5
    damage_done_to_demon = False
    frame_demon = 0
    health_demon = 100
    jump_speed_demon = -25
    lifes_demon = 3
    limite_derecho_screen = SCREEN_WIDTH * 0.75
    speed_demon = 2
    gravity_demon = 1
    gravedad_demon = False

    # Otros
    damage_done_to_knight = False
    flag_pause = False
    fuente_countdown = pygame.font.Font(fuentes["fuente_texto"], size_countdown)
    fuente_score = pygame.font.Font(fuentes["fuente_texto"], size_score)
    fuente_texto = pygame.font.Font(fuentes["fuente_texto"], size_texto)
    last_attack_demon = 0
    nuevo_round = False
    score_demon = 0
    score_knight = 0
    ultima_actualizacion = pygame.time.get_ticks()
    ultima_actualizacion_demon = pygame.time.get_ticks()
    countdown_round = 5
    frames_speed = {
        "idle": 1000,
        "walk": 100,
        "attack": 40,
        "hurt": 70,
        "death": 40
    }

    knight_data = {
        "escala" : 5,
        "frames" : {
                "idle" : 3,
                "walk" : 8,
                "attack" : 7,
                "jump" : 1,
                "hurt" : 3,
                "death" : 9
        }
    }

    knight_sprites = {
        "idle": obtener_frames_escalados_sin_bordes(sprites_knight["idle"], knight_data["frames"]["idle"], knight_data["escala"]),
        "walk": obtener_frames_escalados_sin_bordes(sprites_knight["walk"], knight_data["frames"]["walk"], knight_data["escala"]),
        "attack": obtener_frames_escalados_sin_bordes(sprites_knight["attack"], knight_data["frames"]["attack"], knight_data["escala"]),
        "walk": obtener_frames_escalados_sin_bordes(sprites_knight["walk"], knight_data["frames"]["walk"], knight_data["escala"]),
        "hurt": obtener_frames_escalados_sin_bordes(sprites_knight["hurt"], knight_data["frames"]["hurt"], knight_data["escala"]),
        "death": obtener_frames_escalados_sin_bordes(sprites_knight["death"], knight_data["frames"]["death"], knight_data["escala"]),
    }
    knight_height = knight_sprites["idle"][0].get_height()
    knight_rect = knight_sprites["idle"][0].get_rect(topleft=(200, piso - knight_height))
    knight_image = knight_sprites["idle"][frame_knight]

    #  Demon -------------------------------------------------------
    demon_data = {
        "escala" : 2,
        "frames" : {
            "idle" : 3,
            "walk" : 6,
            "attack" : 4,
            "hurt" : 2,
            "death" : 6}
    }

    demon_sprites = {
        
        "idle": obtener_frames_escalados_sin_bordes(sprites_demon["idle"], demon_data["frames"]["idle"], demon_data["escala"]),
        "walk": obtener_frames_escalados_sin_bordes(sprites_demon["walk"], demon_data["frames"]["walk"], demon_data["escala"]),
        "attack": obtener_frames_escalados_sin_bordes(sprites_demon["attack"], demon_data["frames"]["attack"], demon_data["escala"]),
        "hurt": obtener_frames_escalados_sin_bordes(sprites_demon["hurt"], demon_data["frames"]["hurt"], demon_data["escala"]),
        "death": obtener_frames_escalados_sin_bordes(sprites_demon["death"], demon_data["frames"]["death"], demon_data["escala"]),
    }

    demon_height = demon_sprites["idle"][0].get_height()
    demon_rect = demon_sprites["idle"][0].get_rect(topleft=(SCREEN_WIDTH - 200, piso - demon_height))
    demon_image = demon_sprites["idle"][frame_demon]
    posicion_inicial_knight = (200, piso - knight_height)
    posicion_inicial_demon = (SCREEN_WIDTH - 200, piso - demon_height)


    

    pygame.mixer.music.load(musica["fight_music"])
    pygame.mixer.music.play(-1)
    # Bucle del juego
    while jugando:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        # Eventos
        for event in pygame.event.get():
            if event.type == QUIT: # Salir
                quit_game()
            if event.type == COUNTDOWNEVENT: # Countdown
                countdown -= 1
                if countdown == -1:
                    countdown_activada = False
            if event.type == COUNTDOWNEVENTROUND: # Countdown
                if nuevo_round:
                    countdown_round -= 1
                    if countdown_round == 0:
                        nuevo_round = False
                        demon_alive = True
                        knight_alive = True
                        countdown_round = 5
            if event.type == DEADTIMER:
                if not knight_alive or not demon_alive:
                    tiempo_de_espera -= 1
                    if tiempo_de_espera == 0:
                        tiempo_de_espera = 3
                        if not game_over:
                            nuevo_round = True

            keys = pygame.key.get_pressed()
            if keys[K_m]:
                    flag_mute = not flag_mute
            if keys[K_ESCAPE]:
                escape_screen(SCREEN, flag_mute)
        if not countdown_activada and not nuevo_round and not flag_pause:
        # Movimiento Knight
            if knight_alive:
                knight_velocity_y, gravedad_knight, knight_rect = gravedad(gravedad_knight, knight_velocity_y, gravity_knight, knight_rect)
                if estado_knight == "idle":
                    frame_knight, ultima_actualizacion, knight_image = actualizar_frame(current_time, ultima_actualizacion, frames_speed["idle"], frame_knight,"idle", knight_data["frames"]["idle"], knight_sprites)
                if keys[K_UP] and not gravedad_knight:
                    estado_knight = "walk"
                    knight_velocity_y = jump_speed_knight
                    gravedad_knight = True
                    if gravedad_knight:
                        knight_image = knight_sprites["walk"][2]
                    else:
                        knight_image = knight_sprites["walk"][0]
                if keys[K_LEFT] and knight_rect.left > 0:
                    estado_knight = "walk"
                    knight_rect.x -= speed_knight
                    if knight_rect.left <= limite_izquierdo_screen and scroll_x > 0:
                        scroll_x -= speed_knight
                        knight_rect.x += speed_knight
                    frame_knight, ultima_actualizacion, knight_image = actualizar_frame(current_time, ultima_actualizacion, frames_speed["walk"], frame_knight,"walk", knight_data["frames"]["walk"], knight_sprites)
                    knight_image_flip = True
                    knight_image = knight_sprites["walk"][frame_knight]
                if keys[K_RIGHT] and knight_rect.right < SCREEN_WIDTH:
                    estado_knight = "walk"
                    knight_rect.x += speed_knight
                    if knight_rect.right >= limite_derecho_screen and scroll_x < width_fondo_juego - SCREEN_WIDTH:
                        scroll_x += speed_knight
                        knight_rect.x -= speed_knight
                    knight_image_flip = False
                    frame_knight, ultima_actualizacion, knight_image = actualizar_frame(current_time, ultima_actualizacion, frames_speed["walk"], frame_knight,"walk", knight_data["frames"]["walk"], knight_sprites)
                if keys[K_SPACE]:
                    estado_knight = "attack"
                    knight_attacking = True
            else:
                estado_knight = "death"
                knight_height = knight_sprites["death"][frame_knight].get_height()
                knight_rect.topleft = (knight_rect.left, piso - knight_height)
                if current_time - ultima_actualizacion >= frames_speed["death"]:
                    frame_knight += 1
                    if frame_knight >= knight_data["frames"]["death"]:
                        frame_knight = knight_data["frames"]["death"] -1
                    knight_image = knight_sprites["death"][frame_knight]
                    ultima_actualizacion = current_time
                    SCREEN.blit(knight_sprites["death"][frame_knight], knight_rect)

            # Lógica de ataque
            if estado_knight == "attack":
                if knight_attacking:
                    if current_time - ultima_actualizacion >= frames_speed["attack"]:
                        frame_knight += 1
                        if frame_knight >= knight_data["frames"]["attack"]:
                            frame_knight = 0
                            knight_attacking = False
                            estado_knight = "idle"
                        knight_image = knight_sprites["attack"][frame_knight]
                        ultima_actualizacion = current_time
                if frame_knight == knight_data["frames"]["attack"] - 1 and not damage_done_to_demon and demon_alive:
                    if atacar(knight_rect, knight_image_flip, demon_rect, area_ataque_knight):
                        damage_done_to_demon = True
                        health_demon -= 1
                        score_knight += 10

                        if health_demon <= 0:
                            demon_alive = False

                            lifes_demon -= 1
                            score_knight += 50
                else:
                    damage_done_to_demon = False

    # ------------------------------------------------------------------------------

        # Movimiento Demon
            if demon_alive:
                distancia_entre_personajes = abs(knight_rect.centerx - demon_rect.centerx)
                
                lejos_para_atacar = distancia_entre_personajes > area_ataque_demon * demon_image.get_width()
                
                cerca_para_atacar = distancia_entre_personajes <= area_ataque_demon * demon_image.get_width()
                
                demon_velocity_y, gravedad_demon, demon_rect = gravedad(gravedad_demon, demon_velocity_y, gravity_demon, demon_rect)

                decision_demon = demon_ia(health_demon, health_knight, demon_mira_a_knight, lejos_para_atacar, cerca_para_atacar, knight_attacking, knight_rect, demon_rect, demon_image_flip, knight_alive)
                match decision_demon:
                    case "demon_idle":
                        estado_demon = "idle"
                        if current_time - ultima_actualizacion_demon >= frames_speed["idle"]:
                            frame_demon += 1
                            if frame_demon >= demon_data["frames"]["idle"]:
                                frame_demon = 0
                            demon_image = demon_sprites["idle"][frame_demon]
                            ultima_actualizacion_demon = current_time
                    case "demon_turn_around":
                        demon_image_flip = True
                    case "demon_walk":
                        if knight_rect.x < demon_rect.x:
                            demon_rect.x -= speed_demon
                            demon_image_flip = True
                        else:
                            demon_rect.x += speed_demon
                            demon_image_flip = False
                        frame_demon, ultima_actualizacion, demon_image = actualizar_frame(current_time, ultima_actualizacion, frames_speed["walk"], frame_demon,"walk", demon_data["frames"]["walk"], demon_sprites)
                            
                    case "demon_walk_faster":
                        faster_speed_demon = speed_demon * 1.5
                        if knight_rect.x < demon_rect.x:
                            demon_rect.x -= faster_speed_demon
                            demon_image_flip = True
                        else:
                            demon_rect.x += faster_speed_demon
                            demon_image_flip = False
                        frame_demon, ultima_actualizacion, demon_image = actualizar_frame(current_time, ultima_actualizacion, frames_speed["walk"], frame_demon,"walk", demon_data["frames"]["walk"], demon_sprites)
                    case "demon_runaway":
                        if knight_rect.x < demon_rect.x and demon_rect.right < SCREEN_WIDTH:
                            demon_rect.x += speed_demon
                            demon_image_flip = False
                        else:
                            demon_rect.x -= speed_demon
                            demon_image_flip = True
                        if knight_rect.x > demon_rect.x and demon_rect.left > 0:
                            demon_rect.x -= speed_demon
                            demon_image_flip = True
                        else:
                            demon_rect.x += speed_demon
                            demon_image_flip = False
                        frame_demon, ultima_actualizacion, demon_image = actualizar_frame(current_time, ultima_actualizacion, frames_speed["walk"], frame_demon,"walk", demon_data["frames"]["walk"], demon_sprites)

                    case "demon_jump":
                        if not gravedad_demon:
                            demon_velocity_y = jump_speed_demon
                            gravedad_demon = True
                        demon_velocity_y += gravity_demon
                        demon_rect.y += demon_velocity_y
                        if demon_rect.bottom >= piso:
                            demon_rect.bottom = piso
                            demon_velocity_y = 0
                            gravedad_demon = False
                    case "demon_attack":
                        if knight_alive and current_time - last_attack_demon > 1000:
                            if current_time - ultima_actualizacion_demon >= frames_speed["attack"]:
                                frame_demon += 1
                                if frame_demon >= demon_data["frames"]["attack"]:
                                    frame_demon = 0
                                    last_attack_demon = current_time
                                demon_image = demon_sprites["attack"][frame_demon]
                                ultima_actualizacion_demon = current_time
                            if frame_demon == demon_data["frames"]["attack"] - 1 and not damage_done_to_knight:
                                if atacar(demon_rect, demon_image_flip, knight_rect, area_ataque_demon):
                                    damage_done_to_knight = True
                                    health_knight -= 1
                                    score_demon += 10
                                    estado_knight = "hurt"
                                    if health_knight <= 0:
                                        knight_alive = False
                                        estado_knight = "death"
                                        lifes_knight -= 1
                                        score_demon += 50
                            else:
                                damage_done_to_knight = False
            else:
                if current_time - ultima_actualizacion >= frames_speed["death"]:
                    frame_demon += 1
                    if frame_demon >= demon_data["frames"]["death"]:
                        frame_demon = demon_data["frames"]["death"] -1
                    demon_image = demon_sprites["death"][frame_demon]
                    ultima_actualizacion = current_time
                    SCREEN.blit(demon_sprites["death"][frame_demon], demon_rect)
        if lifes_knight == 0 or lifes_demon == 0:
            game_over = True
        if not knight_alive or not demon_alive and tiempo_de_espera <= 0 :
            health_knight = 100
            health_demon = 100
        if game_over:
            if lifes_knight == 0:
                winner = "demon"
            if lifes_demon == 0:
                winner = "knight"
            game_over_screen(SCREEN, score_knight, winner)

        pygame.mixer.music.pause() if flag_mute else pygame.mixer.music.unpause()
    # ------------------------------------------------------------------------------
    # Actualizar pantalla
        SCREEN.blit(fondo_juego, (-scroll_x, 0))

    # Countdown
        if countdown_activada:
            if countdown > 0:
                mostrar_texto(str(countdown), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN, fuente_countdown)
            if countdown == 0:
                mostrar_texto("FIGHT!!!", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN, fuente_countdown)

    # Mostrar Knight
        imagen = pygame.transform.flip(knight_image, knight_image_flip, False)
        SCREEN.blit(imagen, knight_rect)

    # Mostrar Demon
        if decision_demon != "demon_jump":
            demon_height = demon_image.get_height()
            demon_rect.topleft = (demon_rect.left, piso - demon_height)
        imagen = pygame.transform.flip(demon_image, demon_image_flip, False)
        SCREEN.blit(imagen, demon_rect)
    # Mostrar health bar
        draw_health_bars(SCREEN, fuente_score, score_knight, lifes_knight, score_demon, lifes_demon, health_knight, health_demon)
        if nuevo_round:
            SCREEN.fill((0,0,0))
            estado_knight = "idle"
            decision_demon = "demon_idle"
            knight_rect.topleft = posicion_inicial_knight
            demon_rect.topleft = posicion_inicial_demon
            health_knight = 100
            health_demon = 100
            if countdown_round > 0:
                mostrar_texto("Nuevo Round", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SCREEN, fuente_texto)
                mostrar_texto(f"En {countdown_round} segundos...", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), SCREEN, fuente_texto)
        pygame.display.flip()
    pygame.quit()

def game_over_screen(SCREEN: pygame.Surface, score: int, winner:str):
    """Pantalla de Game Over

    Args:
        SCREEN (pygame.Surface): Pantalla
        score (int): Puntaje del protagonista
        winner (str): Ganador
    """
    SCREEN.fill((0,0,0))
    fuente_texto = pygame.font.Font("./src/assets/fonts/fuente_texto.ttf", 20)
    scores = []
    try:
        scores = cargar_datos_desde_csv("scores.csv")
    except FileNotFoundError:
        print("No se encontró el archivo scores.csv")
    clock = pygame.time.Clock()
    running = True
    nombre_jugador = ""
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        show_winner(SCREEN, fuente_texto, winner, score)
        pygame.display.flip()
        clock.tick(60)

        if nombre_jugador == "":
            nombre_jugador = input("Ingrese su nombre: ")
            if len(nombre_jugador) > 10:
                nombre_jugador = input("Ingrese su nombre: ")
            else:
                running = False
    nuevo_score = {"nombre_jugador": nombre_jugador, "score": str(score)}
    scores.append(nuevo_score)
    escribir_csv("scores.csv", scores)
    from main import main_menu
    main_menu(SCREEN, flag_mute)

def escape_screen(SCREEN: pygame.Surface, flag_mute: bool):
    """Pantalla de escape

    Args:
        SCREEN (pygame.Surface): Pantalla
        flag_mute (bool): Flag de silencio
    """
    click, hove = None, None
    hovered, clicked = False, False
    
    fuente_texto = pygame.font.Font("./src/assets/fonts/fuente_texto.ttf", 20)
    while True:
        mostrar_fondo(SCREEN, fondo_menu_juego)
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
        hovered, clicked = draw_button_imagen(hove, click, SCREEN, (SCREEN_WIDTH // 2 - sprite_boton_green[0].get_width() // 2, 500), sprite_boton_green, "Resume", fuente_botones_medianos, BLACK)
        if hovered:
            mouse_over_button = True
        if clicked:
            break
        hovered, clicked = draw_button_imagen(hove, click, SCREEN, (SCREEN_WIDTH // 2 - sprite_boton_gray[0].get_width() // 2, 600), sprite_boton_gray, "Quit", fuente_botones_medianos, BLACK)
        if hovered:
            mouse_over_button = True
        if clicked:
            pygame.mixer.music.unload()
            from main import main_menu
            main_menu(SCREEN, flag_mute)
        mostrar_texto("Pause", (SCREEN_WIDTH // 2, 300), SCREEN, fuente_texto)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) if mouse_over_button else pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.mixer.music.pause() if flag_mute else pygame.mixer.music.unpause()
        pygame.display.flip()