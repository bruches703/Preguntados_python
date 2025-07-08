import random
from Constantes import *
import pygame
import csv
import os
def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    """Muestra un texto en una superficie, permitiendo saltos de línea y ajuste automático.

    Args:
        surface (_type_): Superficie donde se dibuja el texto.
        text (_type_): Texto a mostrar, puede contener saltos de línea.
        pos (_type_): Posición (x, y) donde se dibuja el texto.
        font (_type_): Fuente a utilizar para el texto.
        color (_type_, optional): Color del texto. Color por defecto pygame.Color('black').
    """
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def mezclar_lista(lista_preguntas:list) -> None:
    """Mezcla una lista de preguntas en su lugar.
    Args:
        lista_preguntas (list): Lista de preguntas a mezclar.
    """
    random.shuffle(lista_preguntas)

def reiniciar_estadisticas(datos_juego:dict, estado_comodines : dict) -> None:
    """Reinicia las estadísticas del juego a sus valores iniciales.
    Args:
        datos_juego (dict): Diccionario que contiene los datos del juego.
    """
    # estadisticas del juego
    if datos_juego["dificultad"] == "facil":
        datos_juego["vidas"] = CANTIDAD_VIDAS
        datos_juego["tiempo_restante"] = 50
        datos_juego["puntos_por_acierto"] = PUNTUACION_ACIERTO -25
    elif datos_juego["dificultad"] == "normal":
        datos_juego["vidas"] = CANTIDAD_VIDAS - 1
        datos_juego["tiempo_restante"] = 40
        datos_juego["puntos_por_acierto"] = PUNTUACION_ACIERTO
    elif datos_juego["dificultad"] == "dificil":
        datos_juego["vidas"] = CANTIDAD_VIDAS - 2
        datos_juego["tiempo_restante"] = 30
        datos_juego["puntos_por_acierto"] = PUNTUACION_ACIERTO + 25

    datos_juego["puntuacion"] = 0
    datos_juego["nombre"] = ""
    datos_juego["respuestas_descartadas"] = []
    datos_juego["estado"] = "jugando"
    datos_juego["respuestas_consecutivas"] = 0
    
    # estadisticas de los comodines
    estado_comodines["comodin_activo"] = False
    estado_comodines["estdo_pasar_pregunta"] = True
    estado_comodines["estdo_bomba"] = True
    estado_comodines["duplica_puntos"] = False
    estado_comodines["estado_doble_chance"] = None
    estado_comodines["estdo_duplicado"] = True

def verificar_respuesta(datos_juego:dict, pregunta:dict, respuesta:int, estado_comodines: dict) -> bool:
    """Verifica si la respuesta dada es correcta y actualiza las estadísticas del juego.
    Args:
        datos_juego (dict): Diccionario que contiene los datos del juego.
        pregunta (dict): Pregunta a verificar.
        respuesta (int): Respuesta dada por el jugador.
        estado_comodines (dict): diccionario con el estado a evaluar.
    Returns:
        bool: True si la respuesta es correcta, False en caso contrario.
    """
    
    if estado_comodines["duplica_puntos"]:
        puntos_a_sumar = datos_juego["puntos_por_acierto"] * 2
        estado_comodines["duplica_puntos"] = False
        print(puntos_a_sumar)
    else:
        puntos_a_sumar = datos_juego["puntos_por_acierto"]
        
    print(puntos_a_sumar)
    
    if respuesta == pregunta["respuesta_correcta"]:
        datos_juego["puntuacion"] += puntos_a_sumar
        retorno = True
    else:

        if estado_comodines["estado_doble_chance"] != "activo" and datos_juego["puntuacion"] > 0:
            datos_juego["puntuacion"] -= PUNTUACION_ERROR
            retorno = False    
        else:
            retorno = False
    return retorno

def crear_elemento_juego(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int) -> dict:
    """Crea un elemento del juego con una textura, tamaño y posición específicos.
    Args:
        textura (str): Ruta de la textura del elemento.
        ancho (int): Ancho del elemento.
        alto (int): Alto del elemento.
        pos_x (int): Posición x del elemento en la pantalla.
        pos_y (int): Posición y del elemento en la pantalla.
    Returns:
        dict: Diccionario que contiene la superficie del elemento y su rectángulo de colisión
    """
    elemento_juego = {}
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))
    elemento_juego["rectangulo"] = elemento_juego["superficie"].get_rect()
    elemento_juego["rectangulo"].x = pos_x
    elemento_juego["rectangulo"].y = pos_y
    
    return elemento_juego

def limpiar_superficie(elemento_juego:dict,textura:str,ancho:int,alto:int) -> None:
    """Limpia la superficie de un elemento del juego y le asigna una nueva textura.
    Args:
        elemento_juego (dict): Diccionario que contiene el elemento del juego.
        textura (str): Ruta de la nueva textura del elemento.
        ancho (int): Nuevo ancho del elemento.
        alto (int): Nuevo alto del elemento.
    """
    elemento_juego["superficie"] =  pygame.transform.scale(pygame.image.load(textura),(ancho,alto))

def obtener_respuesta_click(lista_respuestas:list,pos_click:tuple) -> int | None:
    """Obtiene la respuesta seleccionada por el usuario al hacer clic en una de las respuestas.
    Args:
        lista_respuestas (list): Lista de respuestas, cada una con un rectángulo de colisión.
        pos_click (tuple): Posición del clic del usuario en la pantalla.
    Returns:
        int: Número de la respuesta seleccionada (1, 2, 3, o 4), o None si no se seleccionó ninguna respuesta.
    """
    respuesta = None
    
    for i in range(len(lista_respuestas)):
        if lista_respuestas[i]["rectangulo"].collidepoint(pos_click):
            respuesta = i + 1
    return respuesta
 
def cambiar_pregunta(lista_preguntas:list,indice:int,caja_pregunta:dict,lista_respuestas:list) -> dict:
    """Cambia la pregunta actual y limpia las superficies de la pregunta y respuestas.
    Args:
        lista_preguntas (list): Lista de preguntas del juego.
        indice (int): Índice de la pregunta actual en la lista.
        caja_pregunta (dict): Diccionario que contiene la superficie y el rectángulo de la pregunta.
        lista_respuestas (list): Lista de respuestas, cada una con su superficie y rectángulo.
    Returns:
        dict: Pregunta actual con su texto y respuestas.
    """
    pregunta_actual = lista_preguntas[indice]
    limpiar_superficie(caja_pregunta,"Imagenes/Fondos/Fondo_caja_preguntas.png",ANCHO_PREGUNTA,ALTO_PREGUNTA)
    for i in range(len(lista_respuestas)):
        limpiar_superficie(lista_respuestas[i],"Imagenes/Botones/boton_g.png",ANCHO_BOTON,ALTO_BOTON)
    
    return pregunta_actual

def crear_botones_menu() -> list:
    """Crea una lista de botones para el menú principal del juego.
    Returns:
        list: Lista de diccionarios, cada uno representando un botón del menú.
    """
    lista_botones = []
    pos_y = 120

    for i in range(4):
        boton = crear_elemento_juego("Imagenes/Botones/boton_a.png",ANCHO_BOTON + 30,ALTO_BOTON + 10 ,70,pos_y)
        pos_y += 130
        lista_botones.append(boton)
        
    return lista_botones

def crear_respuestas(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int,cantidad_respuestas:int) -> list:
    """Crea una lista de botones de respuesta para el juego.

    Args:
        textura (str): Ruta de la textura de los botones de respuesta.
        ancho (int): Ancho de cada botón de respuesta.
        alto (int): Alto de cada botón de respuesta.
        pos_x (int): Posición x inicial de los botones de respuesta.
        pos_y (int): Posición y inicial de los botones de respuesta.    
        cantidad_respuestas (int): Cantidad de botones de respuesta a crear.

    Returns:
        list: Lista de diccionarios, cada uno representando un botón de respuesta.
    """
    lista_respuestas = []
    
    # Se crean los botones de respuesta en una cuadrícula de 2x2
    # con un espacio de 200 píxeles entre ellos en el eje x y
    # 80 píxeles en el eje y.
    contador = 0
    for i in range(cantidad_respuestas):
        if contador == 0:
            x = pos_x
            y = pos_y
        elif contador == 1:
            x = pos_x + 350
            y = pos_y
        elif contador == 2:
            x = pos_x
            y = pos_y + 80
        elif contador == 3:
            x = pos_x + 350
            y = pos_y + 80

        boton_respuesta = crear_elemento_juego(textura,ancho,alto,x,y)
        lista_respuestas.append(boton_respuesta)
        contador += 1
    
    return lista_respuestas

def manejar_texto(cuadro_texto:dict,tecla_presionada:str,bloc_mayus:int,datos_juego:dict) -> None:
    #Cuando se toca un espacio
    if tecla_presionada == "space":
        CLICK_SONIDO.play()
        datos_juego["nombre"] += " "
    
    #Cuando se toca el boton borrar
    if tecla_presionada == "backspace" and len(datos_juego["nombre"]) > 0:
        datos_juego["nombre"] = datos_juego["nombre"][0:len(datos_juego["nombre"]) - 1]
        limpiar_superficie(cuadro_texto,"Imagenes/Botones/boton_a.png",450,ALTO_CUADRO)
    
    #Cuando se toca un caracter
    if len(tecla_presionada) == 1: 
        CLICK_SONIDO.play()
        #ESTA ACTIVO EL BLOC MAYUSCULA
        if bloc_mayus == 8192 or bloc_mayus == 1 or bloc_mayus == 2:          
            datos_juego["nombre"] += tecla_presionada.upper()
        else:
            datos_juego["nombre"] += tecla_presionada

def cargar_preguntas_csv(ruta: str, separador:str = ',') -> list:
    """
    Carga las preguntas desde un archivo CSV y las almacena en una lista.

    Returns:
        list: Lista de preguntas cargadas desde el archivo.
    """
    preguntas = []
    with open(ruta, mode='r', encoding='utf-8') as archivo:
        archivo.readline()

        for linea in archivo:
            if linea.strip():
                pregunta = crear_diccionario_pregunta(linea, separador)
                preguntas.append(pregunta)
    return preguntas

def crear_diccionario_pregunta(fila:str, separador:str = ',') -> dict:
    """
    Crea un diccionario a partir de una fila del archivo CSV.

    Args:
        fila (str): Fila del archivo CSV que contiene los datos de la pregunta.
        separador (str): Carácter utilizado para separar los campos en la fila.

    Returns:
        dict: Diccionario con los datos de la pregunta.
    """
    fila = fila.replace('\n', '')  # Eliminar saltos de línea al final
    datos = fila.split(separador)
    return {
        "pregunta": datos[0],
        "respuesta_1": datos[1],
        "respuesta_2": datos[2],
        "respuesta_3": datos[3],
        "respuesta_4": datos[4],
        "respuesta_correcta": int(datos[5])
    }

def subir_volumen(datos_juego: dict) -> None:
    """Bajar el volumen de musica

    Args:
        datos_juego (dict): diccionario con los datos del juego
    """
    if datos_juego["volumen_musica"] <= 95:
        datos_juego["volumen_musica"] += 5
        pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
        CLICK_SONIDO.play()
    else:
        ERROR_SONIDO.play()

def bajar_volumen(datos_juego: dict) -> None:
    """Bajar el volumen de musica

    Args:
        datos_juego (dict): diccionario con los datos del juego
    """
    if datos_juego["volumen_musica"] > 0:
        datos_juego["volumen_musica"] -= 5
        pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
        CLICK_SONIDO.play()
    else: 
        ERROR_SONIDO.play()

def reproducir_musica(pista: str, porcentaje_volumen, bandera_musica: bool):
    if bandera_musica:
        bandera_musica = False
    else:
        bandera_musica = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load(pista)
    pygame.mixer.music.play(-1)
    return bandera_musica