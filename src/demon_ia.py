import random
from settings import *
from resources import *



def demon_mira_a_knight(knight_rect:pygame.Rect, demon_rect:pygame.Rect, demon_image_flip:bool)->bool:
    """Determina si Demon mira a Knight o no

    Args:
        knight_rect (pygame.Rect): Rect de Knight
        demon_rect (pygame.Rect): Rect de Demon
        demon_image_flip (bool): Bool de la orientacion de la imagen de Demon

    Returns:
        bool: True si mira a Knight, False si no
    """
    retorno = None
    if knight_rect.centerx > demon_rect.centerx and not demon_image_flip:
        retorno = True
    elif knight_rect.centerx > demon_rect.centerx and demon_image_flip:
        retorno = False
    elif knight_rect.centerx < demon_rect.centerx and not demon_image_flip:
        retorno = False
    elif knight_rect.centerx < demon_rect.centerx and demon_image_flip:
        retorno = True
    return retorno

def demon_ia(demon_health:int, knight_health:int, demon_mira_a_knight:bool, lejos_para_atacar:bool, cerca_para_atacar:bool, knight_attacking:bool, knight_rect:pygame.Rect, demon_rect:pygame.Rect, demon_image_flip:bool, knight_alive:bool)->str:
    """IA de Demon

    Args:
        demon_health (int): Valor del health de Demon
        knight_health (int): Valor del health de Knight
        demon_mira_a_knight (bool): Funcion que determina si Demon mira a Knight
        lejos_para_atacar (bool): Bool de la distancia de la imagen de Demon
        cerca_para_atacar (bool): Bool de la distancia de la imagen de Demon
        knight_attacking (bool): Bool que indica si Knight lo esta atacando
        knight_rect (pygame.Rect): Rect de Knight
        demon_rect (pygame.Rect): Rect de Demon
        demon_image_flip (bool): Bool de la orientacion actual de la imagen de Demon
        knight_alive (bool): Bool de la vida de Knight

    Returns:
        str: Devuelve una decision tomada por Demon
    """
    if knight_alive:
        if demon_health >= 30:
            if lejos_para_atacar:
                estado_demon = random.choice(["demon_idle", "demon_walk", "demon_walk_faster"])
            elif cerca_para_atacar:
                if demon_mira_a_knight(knight_rect, demon_rect, demon_image_flip):
                    estado_demon = random.choice(["demon_idle", "demon_attack"])
                else:
                    estado_demon = random.choice(["demon_idle", "demon_turn_around"])
                if knight_attacking:
                    estado_demon = random.choice(["demon_attack"])
        else:
            if knight_health > 30:
                estado_demon = random.choice(["demon_attack", "demon_runaway"])
            else:
                estado_demon = random.choice(["demon_runaway", "demon_jump", "demon_walk"])
    else:
        estado_demon = "demon_idle"
    return estado_demon