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

class Boton:
    def __init__(self, x, y, ancho, alto, color, texto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
        self.texto = texto

    def dibujar(self, pantalla, contorno=False):
        pygame.draw.rect(pantalla, self.color, self.rect)
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(self.texto, True, white)
        texto_rect = texto.get_rect(center=self.rect.center)
        pantalla.blit(texto, texto_rect)

        if contorno:
            pygame.draw.rect(pantalla, white, self.rect, 2)

    def clic_en_boton(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(evento.pos)
        return False

initW = 450
initH = 360
superTime = 0
segment = Segment(initW, initH, white, player_size)
player = []
player.append(segment)
for i in range (10):
    initW += player_size
    segment = Segment(initW, initH, white, player_size)
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

def actualizar_posicion_serpiente(orAnterior):
    for i in range(len(player) - 1, 0, -1):
        player[i].x = player[i - 1].x
        player[i].y = player[i - 1].y

    if orientation == 2 and orAnterior != 4:
        player[0].x += player_size
    elif orientation == 4 and orAnterior != 2:
        player[0].x -= player_size
    elif orientation == 3 and orAnterior != 1:
        player[0].y += player_size
    elif orientation == 1 and orAnterior != 3:
        player[0].y -= player_size

    if player[0].x > width:
        player[0].x = 0
    if player[0].x < 0:
        player[0].x = width
    if player[0].y < 0:
        player[0].y = height
    if player[0].y > height:
        player[0].y = 0



food = generarComida()
comidas = 0
superCom = random.randint(5, 15)
superPoints = False
xPlayer = 0
yPlayer = 0
iters = 0
boton = Boton(width // 2 - 100, height // 2 + 20, 200, 50, red, "Jugar")
while True:
    while True:
        iters += 1
        jugar = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if boton.clic_en_boton(event):
                jugar = True

        orAnterior = orientation
        if iters % 10 == 0:
            orientation = random.randint(1, 4)
    # Actualizar la posición de la serpiente
        actualizar_posicion_serpiente(orAnterior)
        
        # Limpiar la pantalla
        screen.fill(black)

        # Dibujar la serpiente
        for i in range(len(player)):
            pygame.draw.rect(screen, white, [player[i].x, player[i].y, player_size, player_size])


        # Draw the title text and button
        text_surface = fontTitle.render(f'SNAKE', True, yellow)
        text_rect_title = text_surface.get_rect()
        text_rect_title.center = (width // 2, height // 2 - 10)
        screen.blit(text_surface, text_rect_title)

        boton.dibujar(screen, contorno=True)
        


        keys = pygame.key.get_pressed()

        if jugar:
            inGame = True
            alive = True
            segment = Segment(initW, initH, white, player_size)
            player = []
            player.append(segment)
            break
        
        

        pygame.display.flip()
        pygame.time.Clock().tick(60)


        if keys[pygame.K_ESCAPE]:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                screen.fill(black)

                text_surface = fontPuntos.render(f'¿Deseas salir? (s/n)', True, white)
                text_rect_info = text_surface.get_rect()
                text_rect_info.center = (width // 2, height // 2)
                screen.blit(text_surface, text_rect_info)

                pygame.display.flip()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_s]:
                    pygame.quit()
                    sys.exit()

                if keys[pygame.K_n]:
                    break
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
                superTime = 0

            if superPoints:
                superTime += 1
            
            if superPoints and superTime > 50:
                superPoints = False
                food = generarComida()

            


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
                    if puntos > record:
                        record = puntos
                        newRecord = True
                        try:
                            arch = open(file_record,"w")
                            arch.write(str(record))
                            arch.close()
                        except FileNotFoundError:
                            print(f"El archivo no existe.")
                        except Exception as e:
                            print(f"Ocurrió un error: {e}")
                    break


            if keys[pygame.K_ESCAPE]:
                    paused = True

                    while paused:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                        text_surface = fontPuntos.render('PAUSA', True, yellow)
                        text_rect_info = text_surface.get_rect()
                        text_rect_info.center = (width // 2, height // 2)
                        screen.blit(text_surface, text_rect_info)

                        text_surface = font2.render('Pulsa [m] para salir', True, yellow)
                        text_rect_info = text_surface.get_rect()
                        text_rect_info.center = (width // 2, height // 2 + 20)
                        screen.blit(text_surface, text_rect_info)

                        keys = pygame.key.get_pressed()

                        if keys[pygame.K_SPACE]:
                            paused = False
                        

                        if keys[pygame.K_m]:
                            paused = False
                            alive = False
                            inGame = False
                            orientation = 1
                            newRecord = False
                            enemies = []
                            food = generarComida()
                            puntos = 0
                            initW = 450
                            initH = 360
                            segment = Segment(initW, initH, white, player_size)
                            player = []
                            player.append(segment)
                            for i in range (6):
                                initW += player_size
                                segment = Segment(initW, initH, white, player_size)
                                player.append(segment)


                        pygame.display.flip()
            


            

                # Actualizar la pantalla
            pygame.display.flip()

            

                # Controlar la velocidad del bucle
            pygame.time.Clock().tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        
        text_surface = fontGameOver.render(f'GAME OVER', True, red)
        text_rect = text_surface.get_rect()
        text_rect.center = (width // 2, height // 2)
        screen.blit(text_surface, text_rect)

        if newRecord:
            text_surface = fontGameOver.render(f'Nuevo record!', True, red)
            text_rect = text_surface.get_rect()
            text_rect.center = (width // 2, 50)
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

    

    