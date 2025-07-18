import pygame
from Constantes import *
from Funciones_generales import *

pygame.init()
lista_botones = crear_botones_menu()
print(lista_botones)
fondo_menu = pygame.transform.scale(pygame.image.load("Imagenes/Fondos/fondo.png"),PANTALLA)

def mostrar_menu(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event]) -> str:
    """Muestra el menu principal y da acceso a las otras ventanas

    Args:
        pantalla (pygame.surface.Surface): Superficie donde se dibuja el programa
        cola_eventos (list[pygame.event.Event]): eventos que ocurren en la ejecucion

    Returns:
        str: devuelve el proximo acceso a ventana
    """
    retorno = "menu"
    #Gestionar Eventos
    for evento in cola_eventos:
        #Actualizaciones
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                for i in range(len(lista_botones)):
                    if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                        if i == BOTON_JUGAR:
                            retorno = "juego"
                        elif i == BOTON_PUNTUACIONES:
                            retorno = "rankings"
                        elif i == BOTON_CONFIG:
                            retorno = "ajustes"
                        else:
                            retorno = "salir"
        
    
    #Dibujar en pygame
    pantalla.blit(fondo_menu,(0,0))
    for i in range(len(lista_botones)):
        pantalla.blit(lista_botones[i]["superficie"],lista_botones[i]["rectangulo"])
    mostrar_texto(lista_botones[BOTON_JUGAR]["superficie"],"JUGAR",(80,15),FUENTE_TEXTO,COLOR_NEGRO)
    mostrar_texto(lista_botones[BOTON_PUNTUACIONES]["superficie"],"RANKINGS",(75,15),FUENTE_TEXTO,COLOR_NEGRO)
    mostrar_texto(lista_botones[BOTON_CONFIG]["superficie"],"AJUSTES",(75,15),FUENTE_TEXTO,COLOR_NEGRO)
    mostrar_texto(lista_botones[BOTON_SALIR]["superficie"],"SALIR",(80,15),FUENTE_TEXTO,COLOR_NEGRO)


    return retorno