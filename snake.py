from contextlib import redirect_stdout
import pygame
import sys
import time
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 930, 750
b_width, b_height = 10, 20
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SNAKE")

# Configuración del personaje
player_size = 30
food_size = 15
player_x = width // 2 - player_size // 2
player_y = height // 2 - player_size // 2
player_speed = 25
orientation = 1

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255,255,0) 


#Inicialización de valores
puntos = 0
nivel = 1
dificultad = 7
maxDifficulty = 25
alive = True
inGame = True
newRecord = False
record = 0
file_record = "max_score.txt"
try:
    arch = open(file_record,"r")
    if (arch):
        for line in arch:
            record = int(line)
    arch.close()
except FileNotFoundError:
    print(f"El archivo no existe.")
except Exception as e:
    print(f"Ocurrió un error: {e}")

#Fuentes
font = pygame.font.Font(None, 31)
font2 = pygame.font.Font(None, 28)
fontPuntos = pygame.font.Font(None, 36)
fontGameOver = pygame.font.Font(None, 43)
fontTitle = pygame.font.Font(None, 55)

class Segment:
    def __init__(self, x, y, color, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


segment = Segment(450, 360, white, player_size)
player = []
player.append(segment)

def generarComida():
    valido = False
    while not valido:
        valido = True
        # Generar coordenadas x e y múltiplos del tamaño del jugador
        xFood = random.randint(1, (width // player_size) - 1) * player_size
        yFood = random.randint(1, (height // player_size) - 1) * player_size
        food = Segment(xFood, yFood, yellow, food_size)
        for i in range(len(player)):
            if player[i].x == food.x and player[i].y == food.y:
                valido = False
                break
    return food




food = generarComida()
comidas = 0
superCom = random.randint(5, 15)
superPoints = False
xPlayer = 0
yPlayer = 0

while inGame:
    while alive:
        comio = False
        screen.fill(black)

        
        if comidas == superCom:
            superPoints = True
            comidas = 0
            superCom = random.randint(5, 15)
            food.color = red
            food.rect = pygame.Rect(food.x, food.y, 20, 20)


    # Verificar colisión entre la cabeza de la serpiente y la comida
        if player[0].x == food.x and player[0].y == food.y:
            comio = True
            food = generarComida()
            comidas += 1

            if superPoints:
                puntos += 100
                superPoints = False
            else:
                puntos += 50
        
            
        if orientation == 2:
            xPlayer = player[0].x + player_size
            yPlayer = player[0].y
        if orientation == 4:
            xPlayer = player[0].x - player_size
            yPlayer = player[0].y
        if orientation == 3:
            yPlayer = player[0].y + player_size
            xPlayer = player[0].x
        if orientation == 1:
            yPlayer = player[0].y - player_size
            xPlayer = player[0].x
        

        if comio:
    # Agregar un nuevo segmento al principio de la lista de segmentos
            nuevo_segmento = Segment(xPlayer, yPlayer, white, player_size)
            player.insert(0, nuevo_segmento)
        else:
            # Actualizar la posición de los segmentos existentes
            for i in range(len(player) - 1, 0, -1):
                player[i].x = player[i - 1].x
                player[i].y = player[i - 1].y

            # Mover la cabeza de la serpiente según la orientación actual
            if orientation == 2:
                player[0].x += player_size
            elif orientation == 4:
                player[0].x -= player_size
            elif orientation == 3:
                player[0].y += player_size
            elif orientation == 1:
                player[0].y -= player_size
            
        food.draw()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        """if orientation == 2:
            player[0].x += player_size
        if orientation == 4:
            player[0].x -= player_size
        if orientation == 3:
            player[0].y += player_size
        if orientation == 1:
            player[0].y -= player_size"""

        if player[0].x > width:
            player[0].x = 0
        
        if player[0].x < 0:
            player[0].x = width

        if player[0].y < 0:
            player[0].y = height

        if player[0].y > height:
            player[0].y = 0

        
        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and orientation != 2:
            orientation = 4
        if keys[pygame.K_d] and orientation != 4:
            orientation = 2
        if keys[pygame.K_w] and orientation != 3:
            orientation = 1
        if keys[pygame.K_s] and orientation != 1:
            orientation = 3


        if keys[pygame.K_LEFT] and orientation != 2:
            orientation = 4
        if keys[pygame.K_RIGHT] and orientation != 4:
            orientation = 2
        if keys[pygame.K_UP] and orientation != 3:
            orientation = 1
        if keys[pygame.K_DOWN] and orientation != 1:
            orientation = 3

        #Mostrar textos
        text_surface = fontPuntos.render(f'Puntos: {puntos}', True, white)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (width // 2, 10)
        screen.blit(text_surface, text_rect)
       
        level_text = font.render(f'Record: {record}', True, white)
        screen.blit(level_text, (10, 18))

        # Dibujar al jugador
        for i in range(len(player)):  
            pygame.draw.rect(screen, white, [player[i].x, player[i].y, player_size, player_size])

        for i in range(1, len(player)): 
            if player[i].x == player[0].x and player[i].y == player[0].y:
                alive = False
                break
        


        

            # Actualizar la pantalla
        pygame.display.flip()

        

            # Controlar la velocidad del bucle
        pygame.time.Clock().tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    
    text_surface = fontGameOver.render(f'GAME OVER', True, red)
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

        # Controlar la velocidad del bucle
    pygame.time.Clock().tick(60)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and not alive:
        alive = True
        orientation = 1
        newRecord = False
        enemies = []
        food = generarComida()
        puntos = 0

        segment = Segment(450, 360, white, player_size)
        player = []
        player.append(segment)

    

    