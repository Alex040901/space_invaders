import sys, pygame, math

pygame.init()

size = width, height = 1080, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SPACE_INVADERS")
running = True
clock = pygame.time.Clock()

red = 255, 0, 0

ALIEN_WIDTH = 40
ALIEN_HEIGHT = 40
SEPARATION_X = 10
SEPARATION_Y = 10
START_X = 100
START_Y = 80
ALIEN_DROP = 20
SPEED = 2
BLACK = 0, 0, 0

class Alien:
    def __init__(self, fila, columna, alien_rect):
        self.fila = fila
        self.columna = columna
        self.rect = alien_rect
        self.vivo = True

def crear_enemigos(filas, columnas):
    enemigos = []
    for fila in range(filas):
        for columna in range(columnas):
            x = START_X + columna * (ALIEN_WIDTH + SEPARATION_X)
            y = START_Y + fila * (ALIEN_HEIGHT + SEPARATION_Y)

            alien_rect = pygame.Rect(x, y, ALIEN_WIDTH, ALIEN_HEIGHT)
            alien = Alien (fila, columna, alien_rect)
            enemigos.append(alien)    
    return enemigos

def edge_detection(enemigos, screen, direction):
    edge_right = False
    edge_left = False
    for alien in enemigos:
        if alien.rect.right >= screen.get_width():
            edge_right = True
        if alien.rect.left <= 0:
            edge_left = True

    if edge_right:
        direction = -1
        for alien in enemigos:
            alien.rect.y += ALIEN_DROP
            
    elif edge_left:
        direction = 1
        for alien in enemigos:
            alien.rect.y += ALIEN_DROP

    for alien in enemigos:
        alien.rect.x += SPEED * direction
            
    return edge_right, edge_left, direction
    


enemigos = crear_enemigos(3, 4)
direction = 1
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False   

    edge_right, edge_left, direction = edge_detection(enemigos, screen, direction)
    screen.fill(BLACK)
    for alien in enemigos:
        pygame.draw.rect(screen, red, alien.rect)
    pygame.display.flip()
pygame.quit()
sys.exit()