import random
import pygame
import csv
import os

from Constantes import *
from Funciones_generales import *
def sumar_bonus(datos_juego: dict, contador_correctas: int) -> int:
    """Suma una vida si las respuestas consecutivas llegan a 5 y devuelve 0. Si no llega a 5
    devuelve el mismo numero

    Args:
        datos_juego (dict): diccionario del jugador actual
        contador_correctas (int): cantidad de respuestas correctas consecutivas que tuvo el jugador

    Returns:
        int: retorna 0 para reiniciar las respuestas consecutivas y aumenta en 1 las vidas, o devuelve las
        respuestas consecutivas
    """
    if contador_correctas == 5 and datos_juego["dificultad"] == "facil":
        datos_juego["tiempo_restante"] += 3
        return 0
    elif contador_correctas == 5 and datos_juego["dificultad"] == "normal":
        datos_juego["vidas"] += 1
        datos_juego["tiempo_restante"] += 3
        return 0
    elif contador_correctas == 3 and datos_juego["dificultad"] == "dificil":
        datos_juego["vidas"] += 1
        datos_juego["tiempo_restante"] += 7
        return 0
    else:
        return contador_correctas
    
def ejecutar_respuesta_correcta(datos_juego: dict, lista_respuestas: list, estado_comodines: dict, pregunta_actual: dict)-> None:
    """Al responder correctamente suma 1 en las respuestas consecutivas, y sumara una vida si hay 5 respuestas consecutivas correctas.
    tambien cambia la textura de los botones

    Args:
        datos_juego (dict): diccionario con datos del juego
        lista_respuestas (list): lista de pregunta
        estado_comodines (dict): diccionario de estado de comodines
        pregunta_actual (dict): pregunta actual para evaluar condiciones
    """
    CLICK_SONIDO.play()
    datos_juego["respuestas_consecutivas"] += 1
    datos_juego["respuestas_consecutivas"] = sumar_bonus(datos_juego, datos_juego["respuestas_consecutivas"])
    for i in range(len(lista_respuestas)):
        if i + 1 == pregunta_actual["respuesta_correcta"]:
            limpiar_superficie(lista_respuestas[i], "Imagenes/Botones/boton_v.png", ANCHO_BOTON, ALTO_BOTON)
        else:
            limpiar_superficie(lista_respuestas[i], "Imagenes/Botones/boton_r.png", ANCHO_BOTON, ALTO_BOTON)
    datos_juego["estado"] = "esperando"
    datos_juego["temporizador_respuesta"] = pygame.time.get_ticks()
    

