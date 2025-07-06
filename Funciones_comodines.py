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
    return cambiar_pregunta(lista_preguntas, datos_juego['indice'], caja_pregunta, lista_respuestas)

def activcar_boton_duplicador(estado_comodines: dict, boton_duplicador: dict) -> None:
    """Activa el boton "duplicador" y establece las condiciones para que sume el doble de puntos. Tambien
    modifica el boton y la condicion para no reutilizar el boton en la misma partida
    Args:
        estado_comodines (dict): estado de los comodines
        boton_duplicador (dict): boton cambiar la superficie
    """
    estado_comodines["comodin_activo"] = False
    estado_comodines["estdo_duplicado"] = False
    estado_comodines["duplica_puntos"] = True
    CLICK_SONIDO.play()
    limpiar_superficie(boton_duplicador, "Imagenes/Botones/off_Doble puntaje.png",ANCHO_BOTON_COMODIN,ALTO_BOTON_COMODIN)