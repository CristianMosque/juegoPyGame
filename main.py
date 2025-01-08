import pygame
import random
import sys

# Inicializar PyGame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piedra, Papel o Tijera")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (100, 149, 237)
ROJO = (255, 69, 0)
VERDE = (34, 139, 34)

# Fuentes
font = pygame.font.Font(None, 50)

# Cargar y redimensionar imágenes
def cargar_imagen(ruta):
    """Carga y redimensiona una imagen."""
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, (100, 100))

# Rutas de imágenes
ruta_piedra = "C:\\Users\\MacOS\\Desktop\\INGENIERÍA EN CONTROL Y AUTOMATIZACIÓN\\VIII\\Multiplataforma\\KODLAND\\ProyectoPrueba\\imagenes\\piedra.png"
ruta_papel = "C:\\Users\\MacOS\\Desktop\\INGENIERÍA EN CONTROL Y AUTOMATIZACIÓN\\VIII\\Multiplataforma\\KODLAND\\ProyectoPrueba\\imagenes\\papel.png"
ruta_tijera = "C:\\Users\\MacOS\\Desktop\\INGENIERÍA EN CONTROL Y AUTOMATIZACIÓN\\VIII\\Multiplataforma\\KODLAND\\ProyectoPrueba\\imagenes\\tijera.png"

# Cargar imágenes
piedra_img = cargar_imagen(ruta_piedra)
papel_img = cargar_imagen(ruta_papel)
tijera_img = cargar_imagen(ruta_tijera)

# Opciones del juego
opciones = ["Piedra", "Papel", "Tijera"]

# Variables de estado
jugador1_victorias = 0
jugador2_victorias = 0
jugador_eleccion = None
enemigo_eleccion = None
resultado = ""

# Coordenadas para las imágenes
area_piedra = (WIDTH // 2 - 150, HEIGHT - 150, 100, 100)
area_papel = (WIDTH // 2 - 50, HEIGHT - 150, 100, 100)
area_tijera = (WIDTH // 2 + 50, HEIGHT - 150, 100, 100)

def dibujar_texto(texto, color, x, y):
    """Dibuja texto en la pantalla."""
    render = font.render(texto, True, color)
    screen.blit(render, (x, y))

def generar_eleccion_enemigo():
    """Genera una elección aleatoria para el enemigo."""
    return random.choice(opciones)

def determinar_ganador(jugador):
    """Determina el ganador del juego."""
    global jugador1_victorias, jugador2_victorias
    
    if jugador == enemigo_eleccion:
        return "Empate!"
    elif (jugador == "Piedra" and enemigo_eleccion == "Tijera") or \
         (jugador == "Papel" and enemigo_eleccion == "Piedra") or \
         (jugador == "Tijera" and enemigo_eleccion == "Papel"):
        jugador1_victorias += 1
        return "Ganaste Jugador 1!"
    else:
        jugador2_victorias += 1
        return "Ganaste Jugador 2!"

def dibujar_menu():
    """Dibuja el menú inicial."""
    screen.fill(BLANCO)
    
    # Título y marcador
    dibujar_texto("Piedra, Papel o Tijera", NEGRO, WIDTH // 2 - 200, 300)
    dibujar_texto(f"Jugador 1: {jugador1_victorias}", AZUL, WIDTH - 300, 80)
    dibujar_texto(f"Jugador 2: {jugador2_victorias}", ROJO, 20, 80)

    # Dibujar las imágenes de las opciones en la parte inferior central
    screen.blit(piedra_img, (WIDTH // 2 - 150 , HEIGHT - 150))
    screen.blit(papel_img, (WIDTH // 2 - 50 , HEIGHT - 150))
    screen.blit(tijera_img, (WIDTH // 2 + 50 , HEIGHT - 150))

def dibujar_resultado():
    """Dibuja el resultado del juego."""
    screen.fill(BLANCO)

    # Mostrar elecciones y resultados
    dibujar_texto(f"Tu elección: {jugador_eleccion}", VERDE, WIDTH // 2 - 100 , HEIGHT // 2 -50 )
    dibujar_texto(f"Elección del enemigo: {enemigo_eleccion}", ROJO ,WIDTH //2 -150 ,HEIGHT //2 )
    
    # Mostrar marcador al lado derecho
    dibujar_texto(f"Jugador 1: {jugador1_victorias}", AZUL ,WIDTH -200 ,80 )
    dibujar_texto(f"Jugador 2: {jugador2_victorias}", ROJO ,20 ,80 )

def anunciar_ganador():
    """Anuncia al ganador si llega a tres victorias."""
    if jugador1_victorias >= 3:
        dibujar_texto("¡Ganaste Jugador 1!", VERDE ,WIDTH //2 -150 ,HEIGHT //2 +100 )
        pygame.display.flip()
        pygame.time.delay(3000) # Espera por tres segundos antes de reiniciar el juego.
        return True

    elif jugador2_victorias >= 3:
        dibujar_texto("¡Ganaste Jugador 2!", ROJO ,WIDTH //2 -150 ,HEIGHT //2 +100 )
        pygame.display.flip()
        pygame.time.delay(3000) # Espera por tres segundos antes de reiniciar el juego.
        return True

    return False

def main():
    """Función principal del juego."""
    
    global jugador_eleccion
    global enemigo_eleccion
    global resultado

    running = True
    menu_activo = True

    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

            if evento.type == pygame.MOUSEBUTTONDOWN and menu_activo:
                x, y = evento.pos

                if area_piedra[0] <= x <= area_piedra[0] + area_piedra[2] and area_piedra[1] <= y <= area_piedra[1] + area_piedra[3]:
                    jugador_eleccion = "Piedra"
                elif area_papel[0] <= x <= area_papel[0] + area_papel[2] and area_papel[1] <= y <= area_papel[1] + area_papel[3]:
                    jugador_eleccion = "Papel"
                elif area_tijera[0] <= x <= area_tijera[0] + area_tijera[2] and area_tijera[1] <= y <= area_tijera[1] + area_tijera[3]:
                    jugador_eleccion = "Tijera"

                if jugador_eleccion:
                    enemigo_eleccion = generar_eleccion_enemigo()
                    resultado = determinar_ganador(jugador_eleccion)
                    menu_activo = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    # Reiniciar el juego si se presiona R
                    jugador_eleccion = None
                    enemigo_eleccion = None
                    resultado = ""
                    menu_activo = True

        # Dibujar pantalla según estado
        if menu_activo:
            dibujar_menu()
        else:
            dibujar_resultado()
            if anunciar_ganador():
                # Reiniciar contadores al finalizar el juego.
                global jugador1_victorias 
                global jugador2_victorias 
                jugador1_victorias = 0 
                jugador2_victorias = 0 

        pygame.display.flip()

# Ejecutar el juego
if __name__ == "__main__":
    main()

pygame.quit()
