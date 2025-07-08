import pygame 
from Constantes import *
from Menu import *
from Juego import *
from Configurtacion import *
import random

pygame.display.set_caption("PREGUNTADOS")
icono = pygame.image.load("Imagenes/Iconos/Lapiz.png")
pygame.display.set_icon(icono)

fondo_pantalla = pygame.transform.scale(pygame.image.load("Imagenes/Fondos/Fondo_Configuracion.png"),PANTALLA)
caja_datos_facil = crear_elemento_juego("Imagenes/Botones/boton_g.png",400,200,260,70)
caja_datos_normal = crear_elemento_juego("Imagenes/Botones/boton_g.png",400,200,260,300)
caja_datos_dificil = crear_elemento_juego("Imagenes/Botones/boton_g.png",400,200,260,530)

boton_facil = crear_elemento_juego("Imagenes/Botones/boton_a.png",ANCHO_BOTON_DIFICULTAD,ALTO_BOTON_DIFICULTAD,POS_X_BOTON_DIF,POS_Y_BOTON_DIF)
boton_normal = crear_elemento_juego("Imagenes/Botones/boton_a.png",ANCHO_BOTON_DIFICULTAD,ALTO_BOTON_DIFICULTAD,POS_X_BOTON_DIF, POS_Y_BOTON_DIF + 200)
boton_dificil = crear_elemento_juego("Imagenes/Botones/boton_a.png",ANCHO_BOTON_DIFICULTAD,ALTO_BOTON_DIFICULTAD,POS_X_BOTON_DIF, (POS_Y_BOTON_DIF + 200) + 200)
boton_volver = crear_elemento_juego("Imagenes/Botones/boton_g.png",110,45,10,750)

def mostrar_cambiar_difucultad(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    """Muestra el menu de cambiar dificultad con las opciones de facil, normal y dificil
    Facil: 5 vidas, 60 seg de juego, 
    Normal:
    Dificil:

    Args:
        pantalla (pygame.Surface): informacion de la pantalla
        cola_eventos (list[pygame.event.Event]): cola de eventos del programa
        datos_juego (dict): diccionario con los datos del juego

    Returns:
        str: retorna como caden la ventana a mostrarse
    """
    retorno = "configurar_dificultad"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            if boton_volver["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                return "ajustes"
            
            elif boton_facil["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                datos_juego["dificultad"] = "facil"
            elif boton_normal["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                datos_juego["dificultad"] = "normal"
            elif boton_dificil["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                datos_juego["dificultad"] = "dificil"

                
            print(datos_juego["dificultad"])
    pantalla.blit(fondo_menu, (0, 0))
    pantalla.blit(boton_facil["superficie"], boton_facil["rectangulo"])
    pantalla.blit(boton_normal["superficie"], boton_normal["rectangulo"])
    pantalla.blit(boton_dificil["superficie"], boton_dificil["rectangulo"])
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])

    pantalla.blit(caja_datos_facil["superficie"],caja_datos_facil["rectangulo"])
    pantalla.blit(caja_datos_normal["superficie"],caja_datos_normal["rectangulo"])
    pantalla.blit(caja_datos_dificil["superficie"],caja_datos_dificil["rectangulo"])

    mostrar_texto(caja_datos_facil["superficie"], "50 segundos de partida", (20,30), FUENTE_TEXTO)
    mostrar_texto(caja_datos_facil["superficie"], "Comienzas con 3 vidas", (20,60), FUENTE_TEXTO)
    mostrar_texto(caja_datos_facil["superficie"], "Con 5 respuestas consecutivas obtendras bonus de + 3 segundos", (20,90), FUENTE_TEXTO)     

    mostrar_texto(caja_datos_normal["superficie"], "40 segundos de partida", (20,30), FUENTE_TEXTO)
    mostrar_texto(caja_datos_normal["superficie"], "Comienzas con 4 vidas", (20,60), FUENTE_TEXTO)
    mostrar_texto(caja_datos_normal["superficie"], "Con 5 respuestas consecutivas obtendras bonus de +1 vida, + 3 segundos", (20,90), FUENTE_TEXTO)     

    mostrar_texto(caja_datos_dificil["superficie"], "30 segundos de partida", (20,30), FUENTE_TEXTO)
    mostrar_texto(caja_datos_dificil["superficie"], "Comienzas con 3 vidas", (20,60), FUENTE_TEXTO)
    mostrar_texto(caja_datos_dificil["superficie"], "Con 3 respuestas consecutivas obtendras bonus de +1 vida, + 7 segundos", (20,90), FUENTE_TEXTO)

    mostrar_texto(pantalla, "FACIL", (POS_X_BOTON_DIF + 50,POS_Y_BOTON_DIF + 25), FUENTE_TEXTO)
    mostrar_texto(pantalla, "NORMAL", (POS_X_BOTON_DIF + 50,POS_Y_BOTON_DIF + 225), FUENTE_TEXTO)
    mostrar_texto(pantalla, "DIFICIL", (POS_X_BOTON_DIF + 50,(POS_Y_BOTON_DIF + 225) + 200), FUENTE_TEXTO)
    mostrar_texto(pantalla, "VOLVER", (12,760), FUENTE_TEXTO)
    return retorno


