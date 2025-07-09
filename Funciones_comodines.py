from Funciones_generales import *
from Constantes import *

def reiniciar_textura_comodines(boton_bomba: dict, boton_doble_oportunidad: dict, boton_pasar_pregunta: dict, boton_duplicador: dict)-> None:
    """Limpia y reestablece la textura de las cajas de los comodines

    Args:
        boton_bomba (dict): boton de bomba
        boton_doble_oportunidad (dict): boton de doble chance
        boton_pasar_pregunta (dict): boton de pasar pregunta
        boton_duplicador (dict): boton de duplicador
    """
    limpiar_superficie(boton_bomba, TEXTURA_BOMBA,ANCHO_BOTON_COMODIN,ALTO_BOTON_COMODIN)
    limpiar_superficie(boton_doble_oportunidad, TEXTURA_DOBLE_CHANCE,ANCHO_BOTON_COMODIN,ALTO_BOTON_COMODIN)
    limpiar_superficie(boton_pasar_pregunta, TEXTURA_PASAR_PREGUNTA,ANCHO_BOTON_COMODIN,ALTO_BOTON_COMODIN)
    limpiar_superficie(boton_duplicador, TEXTURA_DUPLICADOR,ANCHO_BOTON_COMODIN,ALTO_BOTON_COMODIN)    
    


def activar_boton_pasar_pregunta(caja_pregunta, lista_respuestas: list,datos_juego: dict, lista_preguntas: list, estado_comodines: dict, boton_pasar_pregunta:dict) -> dict:
    """Activa el boton de pasar pregunta y ejecuta lo necesario para traer la siguiente pregunta
    y modificar la textura de la caja

    Args:
        caja_pregunta (_type_): Informacion de la pantalla principal
        lista_respuestas (list): lista con las respuestas
        datos_juego (dict): informacion del juego a modificar
        lista_preguntas (list): listado de preguntas a evaluar para pasar a la siguiente
        estado_comodines (dict): diccionario de los estados de comodines, para modificar el "estado_pasar_pregunta"
        boton_pasar_pregunta (dict): diccionario del boton a cambiar la textura

    Returns:
        dict: devuelve el diccionario de la proxima pregunta
    """
    estado_comodines["estdo_pasar_pregunta"] = False
    CLICK_SONIDO.play()
    limpiar_superficie(boton_pasar_pregunta, "Imagenes/Botones/off_Siguiente pregunta.png",ANCHO_BOTON_COMODIN,ALTO_BOTON_COMODIN)

    # pasar a la siguiente pregunta
    datos_juego['indice'] += 1
    if datos_juego['indice'] == len(lista_preguntas):
        mezclar_lista(lista_preguntas)
        datos_juego['indice'] = 0        
      
    datos_juego["estado"] = "jugando"
    datos_juego["temporizador_respuesta"] = 0
    


    return cambiar_pregunta(lista_preguntas, datos_juego['indice'], caja_pregunta, lista_respuestas)

def activcar_boton_duplicador(estado_comodines: dict, boton_duplicador: dict) -> None:
    """Activa el boton "duplicador" y establece las condiciones para que sume el doble de puntos. Tambien
    modifica el boton y la condicion para no reutilizar el boton en la misma partida
    Args:
        estado_comodines (dict): estado de los comodines
        boton_duplicador (dict): boton cambiar la superficie
    """
    estado_comodines["estdo_duplicado"] = False
    estado_comodines["duplica_puntos"] = True
    CLICK_SONIDO.play()
    limpiar_superficie(boton_duplicador, "Imagenes/Botones/off_Doble puntaje.png",ANCHO_BOTON_COMODIN,ALTO_BOTON_COMODIN)

def activar_boton_bomba(boton_bomba: dict, estado_comodines: dict, lista_respuestas: list, pregunta_actual: dict) -> None:

    """Ejecuta todo lo necesario al activar el boton "Bomba", cambia las texturas de dos
    de las respuestas incorrectas, cambia la textura del boton "bomba"

    Args:
        boton_bomba (dict): boton cambiar la superficie
        estado_comodines (dict): diccionarios de los estados de los comodines
    """
    CLICK_SONIDO.play()
    estado_comodines["comodin_activo"] = True
    estado_comodines["estdo_bomba"] = False
    limpiar_superficie(boton_bomba, "Imagenes/Botones/off_Bomba.png", ANCHO_BOTON_COMODIN, ALTO_BOTON_COMODIN)

    bloqueadas = set()
    while len(bloqueadas) < 2:
        candidata = random.randint(1, 4)
        if candidata != pregunta_actual["respuesta_correcta"] and candidata not in bloqueadas:
            bloqueadas.add(candidata)
            limpiar_superficie(lista_respuestas[candidata - 1], "Imagenes/Botones/boton_r.png", ANCHO_BOTON, ALTO_BOTON)

def activar_boton_doble_chance(estado_comodines: dict, boton: dict) -> None:
    """Se establecen los parametros para poder tener una segunda 
    chance si se responde mal en la pregunta actual

    Args:
        estado_comodines (dict): diccionario de los estados de los comodines
        boton (dict): boton a editar para 
    """
    estado_comodines["estado_doble_chance"] = False  # Se desactiva si estaba activ
    estado_comodines["comodin_activo"] = True
    estado_comodines["estado_doble_chance"] = "activo"
    CLICK_SONIDO.play()
    limpiar_superficie(boton,"Imagenes/Botones/off_Doble oportunidad.png",ANCHO_BOTON_COMODIN,ALTO_BOTON_COMODIN)

def ejecucion_doble_chance(estado_comodines: dict, datos_juego: dict, lista_respuestas: list, pregunta_actual: dict, respuesta: int) -> None:
    """Ejecucion de los comandos para que pueda tener una doble chance al fallar

    Args:
        estado_comodines (dict): diccionario con los estados de los comodines
        datos_juego (dict): datos del juego a editar
        lista_respuestas (list): lista de respuestas a analizar
    """
    ERROR_SONIDO.play()
    if estado_comodines.get("estado_doble_chance", False) == "activo":
        # Al tener "doble chance" al fallar solo pinta de rojo la respuesta incorrecta y continua
        for i in range(len(lista_respuestas)):
            if i + 1 == respuesta:
                limpiar_superficie(lista_respuestas[i], "Imagenes/Botones/boton_r.png", ANCHO_BOTON, ALTO_BOTON)
        estado_comodines["estado_doble_chance"] = "usada"  # Marca que ya usó la primera chance

    elif estado_comodines.get("estado_doble_chance", False) == "usada":
        datos_juego["vidas"] -= 1
        # Sin depender del resultado, el juego continuara 
        for i in range(len(lista_respuestas)):
            if i + 1 == pregunta_actual["respuesta_correcta"]:
                limpiar_superficie(lista_respuestas[i], "Imagenes/Botones/boton_v.png", ANCHO_BOTON, ALTO_BOTON)
            else:
                limpiar_superficie(lista_respuestas[i], "Imagenes/Botones/boton_r.png", ANCHO_BOTON, ALTO_BOTON)
        datos_juego["estado"] = "esperando"
        datos_juego["temporizador_respuesta"] = pygame.time.get_ticks()
        estado_comodines["estado_doble_chance"] = False  # Se desactiva definitivamente
    else:
        # Ejecucion normal sin doble chance activa
        datos_juego["vidas"] -= 1
        for i in range(len(lista_respuestas)):
            if i + 1 == pregunta_actual["respuesta_correcta"]:
                limpiar_superficie(lista_respuestas[i], "Imagenes/Botones/boton_v.png", ANCHO_BOTON, ALTO_BOTON)
            else:
                limpiar_superficie(lista_respuestas[i], "Imagenes/Botones/boton_r.png", ANCHO_BOTON, ALTO_BOTON)
        datos_juego["estado"] = "esperando"
        datos_juego["temporizador_respuesta"] = pygame.time.get_ticks()
               