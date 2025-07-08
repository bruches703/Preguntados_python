import pygame
from Constantes import *
from Funciones_generales import *

pygame.init()

boton_suma = crear_elemento_juego("Imagenes/Iconos/sonido_mas.png",60,60,550,150)
boton_resta = crear_elemento_juego("Imagenes/Iconos/sonido_menos.png",60,60,120,150)
rect_barra_fondo = pygame.Rect(BARRA_POS_X, BARRA_POS_Y, BARRA_ANCHO_MAX, BARRA_ALTO)
boton_volver = crear_elemento_juego("Imagenes/Botones/boton_g.png",100,40,10,750)
boton_audio_off = crear_elemento_juego("Imagenes/Iconos/sonido_off.png",60,60,180,250)
boton_audio_on = crear_elemento_juego("Imagenes/Iconos/sonido_on.png",60,60,480,250)
boton_cambiar_dificultad = crear_elemento_juego("Imagenes/Botones/boton_g.png",400,80,150,400)

fondo_pantalla = pygame.transform.scale(pygame.image.load("Imagenes/Fondos/Fondo_Configuracion.png"),PANTALLA)

def mostrar_ajustes(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    """Muestra la pantalla de ajustes con control de volumen."""
    retorno = "ajustes"
    

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_suma["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                subir_volumen(datos_juego)

            elif boton_resta["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                bajar_volumen(datos_juego)

            elif boton_audio_on["rectangulo"].collidepoint(evento.pos) and datos_juego["estado_musica"] != "activo":
                CLICK_SONIDO.play()
                pygame.mixer.music.load("Sonidos/music_menu.mp3")
                pygame.mixer.music.play(-1)
                datos_juego["estado_musica"] = "activo"

            elif boton_audio_off["rectangulo"].collidepoint(evento.pos) and datos_juego["estado_musica"] != "inactivo":
                CLICK_SONIDO.play()
                pygame.mixer.music.stop()
                datos_juego["estado_musica"] = "inactivo"
            
            elif boton_cambiar_dificultad["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                retorno = "configurar_dificultad"

            elif boton_volver["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                retorno = "menu"

        # Dibujar botones de audio según el estado actual

    ejecucion_de_pantalla_configuracion(pantalla, datos_juego)
    
    
    return retorno

def ejecucion_de_pantalla_configuracion(pantalla: pygame.surface.Surface, datos_juego: dict) -> None:

    mostrar_texto(boton_volver["superficie"], "VOLVER", (10, 10), FUENTE_PREGUNTA , COLOR_NEGRO)
    mostrar_texto(boton_cambiar_dificultad["superficie"], "CAMBIAR DIFICULTAD", (30, 25), FUENTE_PREGUNTA, COLOR_NEGRO)

    ejecutar_blits(fondo_pantalla,[boton_suma,boton_resta,boton_volver,boton_audio_off,boton_cambiar_dificultad],pantalla)

    texto_volver = FUENTE_PREGUNTA.render("VOLVER", True, COLOR_NEGRO)
    texto_rect = texto_volver.get_rect(center=boton_volver["rectangulo"].center)
    pantalla.blit(texto_volver, texto_rect)

    # --- BARRA DE VOLUMEN ---
    ajustar_volumen(pantalla, datos_juego)

    #  Dibujar botón con fondo según estado del audio
    if datos_juego["estado_musica"] == "activo":
        color_boton_on = COLOR_VERDE
        color_boton_off = COLOR_ROJO
    else: 
        color_boton_off = COLOR_VERDE
        color_boton_on = COLOR_ROJO
    
    pygame.draw.rect(pantalla, color_boton_on, boton_audio_on["rectangulo"], border_radius=10)
    pygame.draw.rect(pantalla, color_boton_off, boton_audio_off["rectangulo"], border_radius=10)
    pantalla.blit(boton_audio_on["superficie"], boton_audio_on["rectangulo"])
    pantalla.blit(boton_audio_off["superficie"], boton_audio_off["rectangulo"])

def ajustar_volumen(pantalla: pygame.Surface, datos_juego: dict) -> None:
    """ajusta el volumen y ejecuta los comandos para la interaccion de la
    barra de volumen

    Args:
        pantalla (pygame.Surface): informacion de la pantalla
        datos_juego (dict): diccionario con los datos del juego
    """
    pygame.draw.rect(pantalla, COLOR_AZUL, rect_barra_fondo, 2)
    volumen_proporcion = datos_juego["volumen_musica"] / 100
    ancho_barra_actual = BARRA_ANCHO_MAX * volumen_proporcion
    rect_barra_actual = pygame.Rect(BARRA_POS_X, BARRA_POS_Y, ancho_barra_actual, BARRA_ALTO)
    pygame.draw.rect(pantalla, COLOR_VERDE, rect_barra_actual)
    texto_vol = FUENTE_VOLUMEN.render(f"{datos_juego['volumen_musica']}%", True, COLOR_NEGRO)
    texto_vol_rect = texto_vol.get_rect(center=(BARRA_POS_X + BARRA_ANCHO_MAX // 2, 180))
    pantalla.blit(texto_vol, texto_vol_rect)

