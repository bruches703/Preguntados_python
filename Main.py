import pygame 
from Constantes import *
from Menu import *
from Juego import *
from Configurtacion import *
from Rankings import *
from Terminado import *
from Playlist import *
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
               "respuesta_descartada" : [],
                "estado": ""}

estado_comodines ={ "comodin_activo": False,
                    "estdo_pasar_pregunta" : True,
                    "estdo_bomba" : True,
                    "estdo_duplicado" : False, #No esta duplicando
                    "estdo_doble_chance" : True,
                    "duplica_puntos" : False
                   } 
corriendo = True
reloj = pygame.time.Clock()
bandera_musica = True
ventana_actual = "menu"

#Ustedes la van a cargar del json
lista_rankings = []
lista_rankings = generar_lista_ranking()
while corriendo:
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()
    
    if datos_juego["volumen_musica"] <= 0:
        pantalla.blit(boton_silenciado["superficie"],(600,0))
    
    

    if ventana_actual == "menu":
        if bandera_musica == True:
            pygame.mixer.music.stop()
            bandera_musica = False
        reiniciar_estadisticas(datos_juego, estado_comodines)
        datos_juego["indice"] = 0
        cambiar_pregunta(lista_preguntas, datos_juego["indice"], caja_pregunta, lista_respuestas)
        ventana_actual = mostrar_menu(pantalla, cola_eventos)

    elif ventana_actual == "juego":
        porcentaje_volumen = datos_juego["volumen_musica"] / 100
        
        if bandera_musica == False:
            pygame.mixer.music.load(playlist[random.randint(0,len(playlist)-1)])
            pygame.mixer.music.set_volume(porcentaje_volumen)
            pygame.mixer.music.play(-1)
            bandera_musica = True
            
        ventana_actual = mostrar_juego(pantalla,cola_eventos,datos_juego, estado_comodines)
    elif ventana_actual == "salir":
        corriendo = False
    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla,cola_eventos,datos_juego)
    elif ventana_actual == "rankings":
        ventana_actual = mostrar_rankings(pantalla,cola_eventos,datos_juego,lista_rankings)
    elif ventana_actual == "terminado":
        ventana_actual = mostrar_fin_juego(pantalla,cola_eventos,datos_juego,lista_rankings)

    # print(ventana_actual)
    pygame.display.flip()

pygame.quit()