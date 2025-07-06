import pygame
from Constantes import *
from Funciones_generales import *

pygame.init()

boton_suma = crear_elemento_juego("Imagenes/Iconos/sonido_mas.png",60,60,420,200)
boton_resta = crear_elemento_juego("Imagenes/Iconos/sonido_menos.png",60,60,20,200)
boton_volver = crear_elemento_juego("Imagenes/Botones/boton_g.png",100,40,10,10)
boton_silenciado = crear_elemento_juego("Imagenes/Iconos/sonido_cero.png",60,60,600,0)

def mostrar_ajustes(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    """Muestra la pantalla de ajustes del juego, permitiendo al usuario modificar el volumen de la música.

    Args:
        pantalla (pygame.Surface): Superficie donde se dibuja la pantalla de ajustes.
        cola_eventos (list[pygame.event.Event]): Lista de eventos de Pygame.
        datos_juego (dict): Diccionario que contiene los datos del juego, incluyendo el volumen de la música.
    Returns:
        str: Retorna "ajustes" si se permanece en la pantalla de ajustes, " 
    """
    retorno = "ajustes"
    
    for evento in cola_eventos:
        if datos_juego["volumen_musica"] <= 0:
            pantalla.blit(boton_silenciado["superficie"],(600,0))

        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_suma["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] <= 95:
                        datos_juego["volumen_musica"] += 5
                        CLICK_SONIDO.play()
                    else:
                        ERROR_SONIDO.play()
                elif boton_resta["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] > 0:
                        datos_juego["volumen_musica"] -= 5
                        CLICK_SONIDO.play()
                    else: 
                        ERROR_SONIDO.play()
                elif boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"


    pantalla.fill(COLOR_BLANCO)
    
    pantalla.blit(boton_suma["superficie"],boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"],boton_resta["rectangulo"])
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])

    
    mostrar_texto(pantalla,f"{datos_juego["volumen_musica"]} %",(200,200),FUENTE_VOLUMEN,COLOR_NEGRO)
    mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_RESPUESTA,COLOR_BLANCO)

    return retorno