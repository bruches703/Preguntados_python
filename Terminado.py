import pygame
import json
from Constantes import *
from Funciones_generales import *
from datetime import datetime
from Rankings import ordenar_rankings
pygame.init()
cuadro_texto = crear_elemento_juego("Imagenes/Botones/boton_a.png",450,ALTO_CUADRO,120,200)
cuadro_guardar_nombre = crear_elemento_juego("Imagenes/Botones/boton_v.png",140,60,280,260)
cuadro_cancelar_guardado = crear_elemento_juego("Imagenes/Botones/boton_g.png",140,60,50,700)

def mostrar_fin_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict,lista_rankings:list) -> str:
    """ Muestra la pantalla de fin de juego, permitiendo al usuario ingresar su nombre y ver su puntuación.
    Args:
        pantalla (pygame.Surface): Superficie donde se dibuja la pantalla de fin de juego.
        cola_eventos (list[pygame.event.Event]): Lista de eventos de Pygame.
        datos_juego (dict): Diccionario que contiene los datos del juego, incluyendo la puntuación y el nombre del jugador.
        lista_rankings (list): Lista de rankings para mostrar las puntuaciones más altas.
    Returns:
        str: Retorna "terminado" si se permanece en la pantalla de fin de juego, "salir" si se cierra el juego.
    """
    retorno = "terminado"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            
            #Cuando ingrese el nombre deberian haber botones que me permitan guardar los cambios
            if evento.button == 1 and datos_juego["estado"] == "terminado":
                CLICK_SONIDO.play()
                if cuadro_guardar_nombre["rectangulo"].collidepoint(evento.pos):
                    
                    nuevo_ranking = {
                                    "nombre": datos_juego["nombre"],
                                    "puntuacion": datos_juego["puntuacion"],
                                    "fecha": datetime.now().isoformat()
                                    }
                    guardar_nuevo_ranking(lista_rankings, nuevo_ranking)

                    retorno = "menu"
                elif cuadro_cancelar_guardado["rectangulo"].collidepoint(evento.pos):
                    retorno = "menu"

        elif evento.type == pygame.KEYDOWN:
            tecla_presionada = pygame.key.name(evento.key)    
            bloc_mayus = pygame.key.get_mods()
            manejar_texto(cuadro_texto,tecla_presionada,bloc_mayus,datos_juego)   
    
    #Metanle un fondo de pantalla al game over
    pantalla.fill(COLOR_BLANCO)
    pantalla.blit(cuadro_texto["superficie"],cuadro_texto["rectangulo"])
    pantalla.blit(cuadro_guardar_nombre["superficie"],cuadro_guardar_nombre["rectangulo"])
    pantalla.blit(cuadro_cancelar_guardado["superficie"],cuadro_cancelar_guardado["rectangulo"])

    mostrar_texto(pantalla,f"Usted obtuvo: {datos_juego["puntuacion"]} puntos",(250,100),FUENTE_TEXTO,COLOR_NEGRO)
    mostrar_texto(cuadro_cancelar_guardado["superficie"], "Salir", (16,16), FUENTE_TEXTO, COLOR_NEGRO)
    mostrar_texto(cuadro_guardar_nombre["superficie"], "Guardar", (16,16), FUENTE_TEXTO, COLOR_NEGRO)

    
    
    if datos_juego["nombre"] != "":
        limpiar_superficie(cuadro_texto,"Imagenes/Botones/boton_a.png",450,ALTO_CUADRO)
        mostrar_texto(cuadro_texto["superficie"],f"{datos_juego["nombre"]}",(10,0),FUENTE_CUADRO_TEXTO,COLOR_BLANCO)
        
        if random.randint(1,2) == 1:
            mostrar_texto(cuadro_texto["superficie"],f"{datos_juego["nombre"]}|",(10,0),FUENTE_CUADRO_TEXTO,COLOR_BLANCO)
        
    else:
        mostrar_texto(cuadro_texto["superficie"],"INGRESE SU NOMBRE",(10,15),FUENTE_RESPUESTA,"#736767")

    return retorno 

def guardar_nuevo_ranking(lista_ranking: list, nuevo_ranking: dict):
    """Guarda el nuevo ranking, el jugador debe estar entre los primeros 10
    en caso contrario no se guardara
    Args:
        lista_ranking (list): _description_
        nuevo_ranking (dict): _description_
    """
    
    if len(lista_ranking) == 10:
        lista_ranking = ordenar_rankings(lista_ranking)
        if lista_ranking [len(lista_ranking)-1]["puntuacion"] < nuevo_ranking["puntuacion"]:
            lista_ranking[len(lista_ranking)-1] = nuevo_ranking
    else:
        lista_ranking.append(nuevo_ranking)
        if os.path.exists ("Ranking.json"):
            with open("Ranking.json", "w") as archivo:
                json.dump(lista_ranking, archivo, indent=4)