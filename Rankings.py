import pygame
import os
import json
from Constantes import *
from Funciones_generales import *

pygame.init()

boton_volver = crear_elemento_juego("Imagenes/Botones/boton_g.png",100,ANCHO_BOTON_VOLVER,ALTO_BOTON_VOLVER,750)


def generar_podios() -> list:
    lista =[]
    pos_y_actual = 200
    pos_x_actual = 220
    ruta_fondo = ""
    for i in range(10):
        if i == 0:
            ruta_fondo = "Imagenes/Fondos/Fondo_podio_uno.png"
        elif i == 1:
            ruta_fondo = "Imagenes/Fondos/Fondo_podio_dos.png"
        elif i == 2:
            ruta_fondo = "Imagenes/Fondos/Fondo_podio_tres.png"
        else:
            ruta_fondo = "Imagenes/Fondos/Fondo_podio.png"
        lista.append(crear_elemento_juego(ruta_fondo,ANCHO_CUADRADO_PODIO,ALTO_CUADRO_PODIO,pos_x_actual,pos_y_actual))
        pos_y_actual +=55
    return lista
    
def generar_lista_ranking() -> list:
    """Genera la lista de ranking a partir del archivo

    Returns:
        list: devuelve la lista de ranking
    """
    lista_rankings = cargar_ranking_json("Ranking.json", ",")
    lista_rankings = ordenar_rankings(lista_rankings)

    return lista_rankings

def mostrar_rankings(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict, lista_ranking: list) -> str:
    lista_ranking = ordenar_rankings(lista_ranking)
    boton_volver = crear_elemento_juego("Imagenes/Botones/boton_g.png",100,40,10,750)
    retorno = "rankings"
    fondo_pantalla = pygame.transform.scale(pygame.image.load("Imagenes/Fondos/Fondo de podios.png"), PANTALLA)

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"

    pantalla.fill(COLOR_BLANCO)
    pantalla.blit(fondo_pantalla, (0, 0))
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    mostrar_texto(pantalla,"Volver",(boton_volver["rectangulo"].x + 10, boton_volver["rectangulo"].y + 10),FUENTE_RESPUESTA,COLOR_NEGRO)
    mostrar_podios(pantalla,lista_ranking)

    return retorno
    
def cargar_ranking_json(ruta: str, separador:str = ',') -> list:
    """
    Carga las preguntas desde un archivo CSV y las almacena en una lista.

    Returns:
        list: Lista de preguntas cargadas desde el archivo.
    """
    lista_ranking = []
    if os.path.exists("Ranking.json"):
        with open("Ranking.json", "r") as archivo:
            lista_ranking = json.load(archivo)
    return lista_ranking


def ordenar_rankings(lista_rankings: list) -> list:
    """
    Ordena la lista de rankings por puntuación de mayor a menor.

    Args:
        lista_rankings (list): Lista de diccionarios con los rankings.

    Returns:
        list: Lista ordenada de rankings.
    """
    n = len(lista_rankings)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_rankings[j]["puntuacion"] < lista_rankings[j + 1]["puntuacion"]:
                aux = lista_rankings[j]
                lista_rankings[j] = lista_rankings[j + 1]
                lista_rankings[j + 1] = aux
    return lista_rankings


def mostrar_podios(pantalla: pygame.Surface, lista_rankings: list):
    lista_podios = generar_podios()
    for i, podio in enumerate(lista_podios):
        if i < len(lista_rankings):
            pantalla.blit(podio["superficie"], podio["rectangulo"])
            nombre = lista_rankings[i]["nombre"]
            puntuacion = lista_rankings[i]["puntuacion"]
            # Centramos el texto dentro del podio
            mostrar_texto(
                pantalla,
                f"{i+1}. {nombre} - {puntuacion}",
                (podio["rectangulo"].x + 10, podio["rectangulo"].y + 20),
                FUENTE_RESPUESTA,
                COLOR_NEGRO
            )