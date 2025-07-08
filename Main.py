import pygame 
from Constantes import *
from Menu import *
from Juego import *
from Configurtacion import *
from Rankings import *
from Terminado import *
from Playlist import *
from Funciones_comodines import *
import random


pygame.init()
pygame.display.set_caption("PREGUNTADOS")
icono = pygame.image.load("Imagenes/Iconos/Lapiz.png")
pygame.display.set_icon(icono)
pantalla = pygame.display.set_mode(PANTALLA)

datos_juego = {"puntuacion":0,
               "vidas":CANTIDAD_VIDAS,
               "nombre":"",
               "tiempo_restante":CANTIDAD_TIEMPO,
               "indice":0,
               "volumen_musica":20,
               "estado_musica" : "activo",
               "respuesta_descartada" : [],
                "estado": ""}

estado_comodines ={ "comodin_activo": False,
                    "estdo_pasar_pregunta" : True,
                    "estdo_bomba" : True,
                    "estdo_duplicado" : False, #No esta duplicando
                    "duplica_puntos" : False,
                    "estado_doble_chance": None
                   } 
corriendo = True
reloj = pygame.time.Clock()
bandera_musica = False
ventana_actual = "menu"

#Ustedes la van a cargar del json
lista_rankings = []
lista_rankings = generar_lista_ranking()
while corriendo:
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()


    # ---------------- MENU -----------------
    if ventana_actual == "menu":
        porcentaje_volumen = datos_juego["volumen_musica"] / 100
        
        if not bandera_musica and datos_juego["estado_musica"]:
            pygame.mixer.music.load("Sonidos/music_menu.mp3")
            pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
            pygame.mixer.music.set_volume(porcentaje_volumen)
            pygame.mixer.music.play(-1)
            bandera_musica = True
        
        reiniciar_estadisticas(datos_juego, estado_comodines)
        datos_juego["indice"] = 0
        cambiar_pregunta(lista_preguntas, datos_juego["indice"], caja_pregunta, lista_respuestas)
        ventana_actual = mostrar_menu(pantalla, cola_eventos)

    # --------------- JUEGO -----------------
    elif ventana_actual == "juego":
        porcentaje_volumen = datos_juego["volumen_musica"] / 100

        if bandera_musica and datos_juego["estado_musica"]:
            pygame.mixer.music.stop()  # Detenemos la música del menú
            bandera_musica = False     # Permitimos cargar otra pista
            pista = playlist[random.randint(0, len(playlist) - 1)]
            pygame.mixer.music.load(pista)
            pygame.mixer.music.set_volume(porcentaje_volumen)
            pygame.mixer.music.play(-1)
            bandera_musica = False

        ventana_actual = mostrar_juego(pantalla, cola_eventos, datos_juego, estado_comodines)

    # ------------- OTRAS VENTANAS ----------
    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "rankings":
        ventana_actual = mostrar_rankings(pantalla, cola_eventos, datos_juego, lista_rankings)
    elif ventana_actual == "terminado":
        ventana_actual = mostrar_fin_juego(pantalla, cola_eventos, datos_juego, lista_rankings)
    elif ventana_actual == "salir":
        corriendo = False

    pygame.display.flip()