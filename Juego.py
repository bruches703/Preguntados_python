import pygame
from Constantes import *
from Funciones_generales import *
from Funciones_comodines import *
from Funciones_juego import *

pygame.init()

pygame.display.set_caption("PREGUNTADOS")
icono = pygame.image.load("Imagenes/Iconos/Lapiz.png")
pygame.display.set_icon(icono)

pantalla = pygame.display.set_mode(PANTALLA)
datos_juego = {"puntuacion":0,"vidas":CANTIDAD_VIDAS,"nombre":"","tiempo_restante":30}
fondo_pantalla = pygame.transform.scale(pygame.image.load("Imagenes/Fondos/fondo.png"),PANTALLA)

#Elemento del juego
caja_pregunta = crear_elemento_juego("Imagenes/Fondos/Fondo_caja_preguntas.png",ANCHO_PREGUNTA,ALTO_PREGUNTA,140,140)
boton_rendirse = crear_elemento_juego("Imagenes/Botones/boton_g.png",120,40,10,750)
lista_respuestas = crear_respuestas("Imagenes/Botones/boton_g.png",ANCHO_BOTON,ALTO_BOTON,40,380,4)

# Boton comodines
boton_bomba = crear_elemento_juego(TEXTURA_BOMBA,ALTO_BOTON_COMODIN,ANCHO_BOTON_COMODIN,150,650)
boton_doble_oportunidad = crear_elemento_juego(TEXTURA_DOBLE_CHANCE,ALTO_BOTON_COMODIN,ANCHO_BOTON_COMODIN,250,650)
boton_pasar_pregunta = crear_elemento_juego(TEXTURA_PASAR_PREGUNTA,ALTO_BOTON_COMODIN,ANCHO_BOTON_COMODIN,350,650)
boton_duplicador = crear_elemento_juego(TEXTURA_DUPLICADOR,ALTO_BOTON_COMODIN,ANCHO_BOTON_COMODIN,450,650)


# lista_preguntas = cargar_preguntas_csv("preguntas.csv")
lista_preguntas = cargar_preguntas_csv("test.csv")
mezclar_lista(lista_preguntas)

corriendo = True
reloj = pygame.time.Clock()
evento_tiempo = pygame.USEREVENT
pygame.time.set_timer(evento_tiempo,1000)

def mostrar_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict, estado_comodines: dict) -> str:
    """ Muestra la ventana del juego y ejecuta el juego mismo

    Args:
        pantalla (pygame.surface.Surface): Superficie donde se dibuja el programa
        cola_eventos (list[pygame.event.Event]): cola de eventos que ocurren en el programa
        datos_juego (dict): diccionario con informacion del juego
        estado_comodines (dict): diccionario con los estados del comodin

    Returns:
        str: devuelve una cadena que identifica el estado del juego
    """
    retorno = "juego"
    contador_correctas = 0
    # manejar pregunta actual
    pregunta_actual = lista_preguntas[datos_juego['indice']]

    # Control para manejar el tiempo a la hora de mostrar los cuadros rojos y verdes
    if datos_juego.get("estado") is None:
        datos_juego["estado"] = "jugando"
        datos_juego["temporizador_respuesta"] = 0
    
    if datos_juego["vidas"] == 0 or datos_juego["tiempo_restante"] == 0:
        reiniciar_textura_comodines(boton_bomba,boton_doble_oportunidad, boton_pasar_pregunta,boton_duplicador)
        datos_juego["estado"] = "terminado"
        retorno = "terminado"

    for evento in cola_eventos:
        respuesta = None        
    
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and datos_juego["estado"] == "jugando" :

#----------------------------------------------------------------------

                # Comodin pasar pregunta
                if boton_pasar_pregunta["rectangulo"].collidepoint(evento.pos) and estado_comodines["estdo_pasar_pregunta"]:
                    # modular preguntas
                    pregunta_actual = activar_boton_pasar_pregunta(caja_pregunta, lista_preguntas,datos_juego, lista_preguntas, estado_comodines, boton_pasar_pregunta)
                    for boton in lista_respuestas:
                        limpiar_superficie(boton, "Imagenes/Botones/boton_g.png", ANCHO_BOTON, ALTO_BOTON)  
                    
                # Comodin Bomba
                elif boton_bomba["rectangulo"].collidepoint(evento.pos) and estado_comodines["estdo_bomba"] and not estado_comodines["comodin_activo"]:
                    activar_boton_bomba(boton_bomba, estado_comodines, lista_respuestas, pregunta_actual)

                # Comodin duplicador
                elif boton_duplicador["rectangulo"].collidepoint(evento.pos) and not estado_comodines["duplica_puntos"] and estado_comodines["estdo_duplicado"]:
                    activcar_boton_duplicador(estado_comodines, boton_duplicador)
                # Comodin Doble chance
                elif boton_doble_oportunidad["rectangulo"].collidepoint(evento.pos) and estado_comodines["estado_doble_chance"] is None and not estado_comodines["comodin_activo"]:
                    activar_boton_doble_chance(estado_comodines, boton_doble_oportunidad)
# ---------------------------------------------------------------------
                elif boton_rendirse["rectangulo"].collidepoint(evento.pos):
                    reiniciar_textura_comodines(boton_bomba,boton_doble_oportunidad, boton_pasar_pregunta,boton_duplicador)
                    retorno = "menu"
                else:
                    # detectar click sobre las respuestas normalmente
                    respuesta = obtener_respuesta_click(lista_respuestas, evento.pos)
                    if respuesta is not None:
                        es_correcta = verificar_respuesta(datos_juego, pregunta_actual, respuesta,  estado_comodines)
                            # Ejecucion normal sin doble chance
                        if es_correcta:
                            ejecutar_respuesta_correcta(datos_juego, lista_respuestas, estado_comodines, pregunta_actual)
                        else:
                            # Ejecucion de doble chance
                            ejecucion_doble_chance(estado_comodines,datos_juego,lista_respuestas,pregunta_actual,respuesta)
            
        elif evento.type == evento_tiempo:
            datos_juego["tiempo_restante"] -= 1
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and datos_juego["estado"] == "jugando" :
                CLICK_SONIDO.play()
                pregunta_actual = cambiar_pregunta(lista_preguntas, datos_juego['indice'], caja_pregunta, lista_respuestas)
                # Sobre comodines
                estado_comodines["comodin_activo"] = False
                
    # manejar el temporizador de espera
    if datos_juego["estado"] == "esperando":
        tiempo_ahora = pygame.time.get_ticks()
        # Luego de un segundo continua el juego, volviendo los botones a su color estandar
        # y cambiando la pregunta y respuestas
        if tiempo_ahora - datos_juego["temporizador_respuesta"] >= 1000:
            datos_juego['indice'] += 1
            if datos_juego['indice'] == len(lista_preguntas):
                datos_juego['indice'] = 0
            pregunta_actual = cambiar_pregunta(lista_preguntas, datos_juego['indice'], caja_pregunta, lista_respuestas)
            datos_juego["estado"] = "jugando"
            estado_comodines["comodin_activo"] = False

            # Desactiva la doble chance si estaba activa y escogio la respuesta correcta
            if estado_comodines.get("estado_doble_chance", False) == "activo":
                estado_comodines["estado_doble_chance"] = "desactivado"
    
    ejecutar_blits(fondo_pantalla, [caja_pregunta,boton_bomba,boton_duplicador,boton_doble_oportunidad,boton_pasar_pregunta,boton_rendirse],pantalla)

    # mostrar las respuestas
    for i in range(len(lista_respuestas)):
        pantalla.blit(lista_respuestas[i]["superficie"], lista_respuestas[i]["rectangulo"])

    mostrar_texto(caja_pregunta["superficie"], pregunta_actual["pregunta"], (20, 20), FUENTE_PREGUNTA, COLOR_NEGRO)

    for i in range(len(lista_respuestas)):
        parametro_respuesta = f"respuesta_{i+1}"
        mostrar_texto(lista_respuestas[i]["superficie"], pregunta_actual[parametro_respuesta], (20, 20), FUENTE_RESPUESTA, COLOR_NEGRO)

    mostrar_texto(pantalla,"RENDIRSE",(boton_rendirse["rectangulo"].x + 10, boton_rendirse["rectangulo"].y + 10),FUENTE_RESPUESTA,COLOR_NEGRO)
    mostrar_texto(pantalla, f"VIDAS: {datos_juego['vidas']}", (10, 10), FUENTE_TEXTO)
    mostrar_texto(pantalla, f"PUNTUACION: {datos_juego['puntuacion']}", (10, 40), FUENTE_TEXTO)
    mostrar_texto(pantalla, f"TIEMPO: {datos_juego['tiempo_restante']} s", (300, 10), FUENTE_TEXTO)
    mostrar_texto(pantalla, f"Dificultad: {datos_juego['dificultad']}", (300, 40), FUENTE_TEXTO)

    return retorno
