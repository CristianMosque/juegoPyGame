import pygame
import random
import sys
import os

# Inicializar PyGame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piedra, Papel o Tijera")

# Colores
FONDO_COLOR = (240, 240, 240)  # Gris claro
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (100, 149, 237)
ROJO = (255, 69, 0)
VERDE = (34, 139, 34)

# Fuentes
font = pygame.font.Font(None, 50)
font_grande = pygame.font.Font(None, 100)  # Fuente grande para el resultado

# Cargar y redimensionar imágenes
piedra_img = pygame.transform.scale(pygame.image.load("imagenes/piedra.png"), (100, 100))
papel_img = pygame.transform.scale(pygame.image.load("imagenes/papel.png"), (100, 100))
tijera_img = pygame.transform.scale(pygame.image.load("imagenes/tijera.png"), (100, 100))

# Opciones del juego
opciones = ["Piedra", "Papel", "Tijera"]

# Variables de estado
jugador1_victorias = 0
enemigo_victorias = 0
jugador_eleccion = None
enemigo_eleccion = None
resultado = ""
nombre_jugador = ""

# Coordenadas para las imágenes
area_piedra = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 150, 100, 100)
area_papel = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 150, 100, 100)
area_tijera = pygame.Rect(WIDTH // 2 + 50, HEIGHT - 150, 100, 100)

# Estados del juego
ESTADO_REGISTRO = 0
ESTADO_JUEGO = 1
ESTADO_RESULTADO = 2

def dibujar_texto(texto, color, x, y, fuente):
    """Dibuja texto en la pantalla con la fuente dada."""
    render = fuente.render(texto, True, color)
    screen.blit(render, (x, y))

def generar_eleccion_enemigo():
    """Genera una elección aleatoria para el enemigo (PC)."""
    return random.choice(opciones)

def determinar_ganador(jugador):
    """Determina el ganador del juego."""
    global jugador1_victorias, enemigo_victorias

    if jugador == enemigo_eleccion:
        return "Empate!"
    elif (jugador == "Piedra" and enemigo_eleccion == "Tijera") or \
         (jugador == "Papel" and enemigo_eleccion == "Piedra") or \
         (jugador == "Tijera" and enemigo_eleccion == "Papel"):
        jugador1_victorias += 1
        if jugador1_victorias == 3:
            return "¡Ganaste el juego!"
        return "¡Ganaste!"
    else:
        enemigo_victorias += 1
        if enemigo_victorias == 3:
            return "Perdiste el juego!"
        return "Perdiste!"

def dibujar_menu():
    """Dibuja el menú inicial con la opción de ingresar el nombre del jugador."""
    screen.fill(FONDO_COLOR)
    
    # Título
    dibujar_texto("Bienvenido al juego", NEGRO, WIDTH // 2 - 200, 100, font)
    dibujar_texto("Piedra, Papel o Tijera", NEGRO, WIDTH // 2 - 200, 160, font)

    # Ingreso de nombre del jugador
    dibujar_texto("Ingresa tu nombre: ", NEGRO, WIDTH // 2 - 200, 300, font)

    # Cuadro de texto para el nombre
    pygame.draw.rect(screen, NEGRO, (WIDTH // 2 - 150, 350, 350, 40), 2)

    # Placeholder, el texto que aparece antes de que el usuario escriba
    if not nombre_jugador:
        dibujar_texto("Escribe tu nombre", AZUL, WIDTH // 2 - 140, 355, font)

    # Dibujar el nombre del jugador si ya se ha ingresado algo
    dibujar_texto(nombre_jugador, NEGRO, WIDTH // 2 - 140, 355, font)

    # Opciones para empezar
    dibujar_texto("Presiona Enter para comenzar", NEGRO, WIDTH // 2 - 180, 420, font)

def dibujar_juego():
    """Dibuja la interfaz del juego."""
    screen.fill(FONDO_COLOR)
    
    # Título y marcador
    dibujar_texto(f"Jugador: {nombre_jugador}", NEGRO, 10, 30, font)
    # Dibujar el marcador del jugador
    dibujar_texto(f"Victorias: {jugador1_victorias}", AZUL, WIDTH - 200, 30, font)

    # Dibujar el marcador del PC debajo del marcador del jugador
    dibujar_texto(f"PC: {enemigo_victorias}", ROJO, WIDTH - 200, 30 + font.get_height(), font)

    # Mostrar elecciones
    dibujar_texto(f"Tu elección: {jugador_eleccion}", VERDE, WIDTH // 2 - 150, HEIGHT // 2 - 100, font)
    dibujar_texto(f"Elección de la PC: {enemigo_eleccion}", ROJO, WIDTH // 2 - 150, HEIGHT // 2, font)

    # Opciones de juego
    screen.blit(piedra_img, area_piedra)
    screen.blit(papel_img, area_papel)
    screen.blit(tijera_img, area_tijera)

    # Mostrar el resultado en el juego (empate, ganaste o perdiste)
    if resultado:
        dibujar_texto(f"{resultado}", NEGRO, WIDTH // 2 - 150, HEIGHT // 2 + 100, font)

def dibujar_resultado():
    """Dibuja el resultado final del juego."""
    screen.fill(FONDO_COLOR)
    
    # Mostrar resultado final (centrado y en grande)
    resultado_texto = "¡Ganaste!" if jugador1_victorias > enemigo_victorias else "¡Perdiste!"
    dibujar_texto(resultado_texto, VERDE if jugador1_victorias > enemigo_victorias else ROJO, WIDTH // 2 - font_grande.size(resultado_texto)[0] // 2, HEIGHT // 3, font_grande)

    # Mostrar el marcador final
    dibujar_texto(f"Victorias: {jugador1_victorias}", AZUL, WIDTH // 2 - font_grande.size(f"Victorias: {jugador1_victorias}")[0] // 2, HEIGHT // 2, font_grande)
    dibujar_texto(f"PC: {enemigo_victorias}", ROJO, WIDTH // 2 - font_grande.size(f"PC: {enemigo_victorias}")[0] // 2, HEIGHT // 2 + 100, font_grande)

    # Esperar para reiniciar el juego
    dibujar_texto("Presiona 'r' para reiniciar", NEGRO, WIDTH // 2 - 150, HEIGHT // 2 + 200, font)

def main():
    """Función principal del juego."""
    global jugador1_victorias, enemigo_victorias  # Corregir: declarar globales
    global jugador_eleccion
    global enemigo_eleccion
    global resultado
    global nombre_jugador
    global estado_actual

    running = True
    jugando = False
    estado_actual = ESTADO_REGISTRO

    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

            if evento.type == pygame.KEYDOWN:
                if estado_actual == ESTADO_RESULTADO:
                    if evento.key == pygame.K_r:
                        # Reiniciar el juego
                        jugador_eleccion = None
                        enemigo_eleccion = None
                        resultado = ""
                        jugador1_victorias = 0
                        enemigo_victorias = 0
                        jugando = False
                        estado_actual = ESTADO_REGISTRO
                elif jugando:
                    if evento.key == pygame.K_r:
                        # Reiniciar el juego
                        jugador_eleccion = None
                        enemigo_eleccion = None
                        resultado = ""
                        jugador1_victorias = 0
                        enemigo_victorias = 0
                        jugando = False
                        estado_actual = ESTADO_REGISTRO
                    elif evento.key == pygame.K_ESCAPE:
                        running = False
                else:
                    # Ingreso del nombre del jugador
                    if evento.key == pygame.K_BACKSPACE:
                        nombre_jugador = nombre_jugador[:-1]
                    elif evento.key == pygame.K_RETURN:
                        # Comienza el juego
                        jugando = True
                        estado_actual = ESTADO_JUEGO
                    else:
                        nombre_jugador += evento.unicode

            if evento.type == pygame.MOUSEBUTTONDOWN and jugando:
                x, y = evento.pos

                # Comprobamos si el clic ocurrió sobre alguna de las imágenes
                if area_piedra.collidepoint(x, y):
                    jugador_eleccion = "Piedra"
                elif area_papel.collidepoint(x, y):
                    jugador_eleccion = "Papel"
                elif area_tijera.collidepoint(x, y):
                    jugador_eleccion = "Tijera"

                if jugador_eleccion:
                    enemigo_eleccion = generar_eleccion_enemigo()
                    resultado = determinar_ganador(jugador_eleccion)
                    if jugador1_victorias == 3 or enemigo_victorias == 3:
                        estado_actual = ESTADO_RESULTADO

        # Dibujar la pantalla según el estado actual
        if estado_actual == ESTADO_REGISTRO:
            dibujar_menu()
        elif estado_actual == ESTADO_JUEGO:
            dibujar_juego()
        elif estado_actual == ESTADO_RESULTADO:
            dibujar_resultado()

        pygame.display.flip()

# Ejecutar el juego
if __name__ == "__main__":
    main()

pygame.quit()
