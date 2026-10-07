import sys, pygame, math, random

pygame.init()

size = width, height = 1080, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SPACE_INVADERS")
running = True
clock = pygame.time.Clock()

font_state = pygame.font.Font(None, 50)

red = 255, 0, 0
white = 255, 255, 255

SEPARATION_X = 10
SEPARATION_Y = 10
START_X = 100
START_Y = 80
ALIEN_DROP = 20
ENEMY_SPEED = 2
BLACK = 0, 0, 0
NAVE_PIXEL_SIZE = 6
ALIEN_PIXEL_SIZE = 4
BULLET_WIDTH = 4
BULLET_HEIGHT = 8
BULLET_SPEED = 8
ENEMY_BULLET_SPEED = 8

nave = (
    (0, 0, 0, 0, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 0, 0, 0, 0),
    (0, 0, 0, 1, 1, 1, 0, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 1, 0, 1, 1, 1, 0, 1, 1),
    (0, 0, 0, 1, 1, 1, 0, 0, 0),
)

alien_sprite = (
    (0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1),
    (0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0),
    (0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0),
)

PLAYER_WIDTH = len(nave[0]) * NAVE_PIXEL_SIZE
PLAYER_HEIGHT = len(nave) * NAVE_PIXEL_SIZE
ALIEN_WIDTH = len(alien_sprite[0]) * ALIEN_PIXEL_SIZE
ALIEN_HEIGHT = len(alien_sprite) * ALIEN_PIXEL_SIZE

class Alien:
    def __init__(self, fila, columna, alien_rect):
        self.fila = fila
        self.columna = columna
        self.rect = alien_rect
        self.vivo = True

class Player:
    def __init__(self, player_rect, speed):
        self.rect = player_rect
        self.speed = speed
        self.vivo = True

class Bullet:
    def __init__(self, player_rect, speed):
        self.rect = pygame.Rect(0, 0, BULLET_WIDTH, BULLET_HEIGHT)
        self.rect.centerx = player_rect.centerx
        self.rect.bottom = player_rect.top
        self.speed = speed

class EnemyBullet:
    def __init__(self, alien_rect, speed):
        self.rect = pygame.Rect(0, 0, BULLET_WIDTH, BULLET_HEIGHT)
        self.rect.centerx = alien_rect.centerx
        self.rect.top = alien_rect.bottom
        self.speed = speed

def crear_nave(speed):
    player_x = (width - PLAYER_WIDTH) // 2
    player_y = height - PLAYER_HEIGHT - 20

    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    player = Player(player_rect, speed)
    return player

def dibujar_nave(player):
    for indice_fila, fila in enumerate(nave):
        for indice_col, pixel in enumerate(fila):
            if pixel == 1:
                x = NAVE_PIXEL_SIZE * indice_col + player.rect.x
                y = NAVE_PIXEL_SIZE * indice_fila + player.rect.y
                pygame.draw.rect(screen, white,(x, y, NAVE_PIXEL_SIZE, NAVE_PIXEL_SIZE))

def dibujar_alien(alien):
    for indice_fila, fila in enumerate(alien_sprite):
        for indice_columna, pixel in enumerate(fila):
            if pixel == 1:
                x = ALIEN_PIXEL_SIZE * indice_columna + alien.rect.x
                y = ALIEN_PIXEL_SIZE * indice_fila + alien.rect.y
                pygame.draw.rect(screen, red,(x, y, ALIEN_PIXEL_SIZE, ALIEN_PIXEL_SIZE))    

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

def edge_detection(enemigos, screen):
    edge_right = False
    edge_left = False
    for alien in enemigos:
        if alien.rect.right >= screen.get_width():
            edge_right = True
        if alien.rect.left <= 0:
            edge_left = True
    return edge_right, edge_left

def alien_move(edge_right, edge_left, direction, enemigos):
    if edge_right:
        direction = -1
        for alien in enemigos:
            alien.rect.y += ALIEN_DROP
            
    elif edge_left:
        direction = 1
        for alien in enemigos:
            alien.rect.y += ALIEN_DROP

    return direction

def game_over(surface):
    texto = font_state.render("Game Over", True, white)
    text_rect = texto.get_rect()
    text_rect.center = (width // 2, height // 2)
    surface.blit(texto, text_rect)

def game_win(surface):
    texto = font_state.render("Game Win!", True, white)
    text_rect = texto.get_rect()
    text_rect.center = (width // 2, height // 2)
    surface.blit(texto, text_rect)

enemigos = crear_enemigos(10, 10)
player = crear_nave(5)
direction = 1
bullets = []
enemy_bullets = []
last_enemy_shot = 0
game_won = False
game_won_pending = False
game_over_pending = False
while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()
    
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False   

        if player.vivo and not game_won:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect, BULLET_SPEED)
                    bullets.append(bullet)

    if game_won_pending:
        game_won = True
    if game_over_pending:
        player.vivo = False
        pygame.draw.rect(screen, BLACK, player.rect)
    if player.vivo and not game_won:
        if keys[pygame.K_LEFT]:
            player.rect.x -= player.speed

            if player.rect.left < 0:
                player.rect.left = 0
        
        if keys[pygame.K_RIGHT]:
            player.rect.x += player.speed

            if player.rect.right > screen.get_width():
                player.rect.right = screen.get_width()

    elif game_won:
        game_win(screen)

    else:
        game_over(screen)

    bullet_hit = []
    for bullet in bullets:
        for alien in enemigos:
            if bullet.rect.colliderect(alien.rect):
                bullet_hit.append(bullet)
                alien.vivo = False
                break
    enemigos = [alien for alien in enemigos if alien.vivo]
    bullets = [bullet for bullet in bullets if bullet not in bullet_hit]

    if not enemigos:
        game_won_pending = True

    enemy_bullet_hit = []
    for enemy_bullet in enemy_bullets:
        if enemy_bullet.rect.colliderect(player.rect):
            enemy_bullet_hit.append(enemy_bullet)
            game_over_pending = True
            break
    enemy_bullets = [enemy_bullet for enemy_bullet in enemy_bullets if enemy_bullet not in enemy_bullet_hit]


    if current_time - last_enemy_shot >= 2000 and not game_won and player.vivo:
        alien_mas_bajo = {}
        for alien in enemigos:
            if alien.columna not in alien_mas_bajo:
                alien_mas_bajo[alien.columna] = alien
            elif alien.rect.y > alien_mas_bajo[alien.columna].rect.y:
                alien_mas_bajo[alien.columna] = alien
        alien_elegidos = random.sample(list(alien_mas_bajo.values()), min(3, len(alien_mas_bajo)))
        for alien in alien_elegidos:
            enemy_bullet = EnemyBullet(alien.rect, ENEMY_BULLET_SPEED)
            enemy_bullets.append(enemy_bullet)
        last_enemy_shot = current_time

    if player.vivo and not game_won:
        edge_right, edge_left = edge_detection(enemigos, screen)
        direction = alien_move(edge_right, edge_left, direction, enemigos)
        for alien in enemigos:
            alien.rect.x += ENEMY_SPEED * direction
        screen.fill(BLACK)
        for alien in enemigos:
            dibujar_alien(alien)
        for bullet in bullets:
            pygame.draw.rect(screen, white, bullet.rect)
        for bullet in bullets:
            bullet.rect.y -= BULLET_SPEED
        bullets = [bullet for bullet in bullets if bullet.rect.bottom > 0]
        for enemy_bullet in enemy_bullets:
            enemy_bullet.rect.y += enemy_bullet.speed
        enemy_bullets = [enemy_bullet for enemy_bullet in enemy_bullets if enemy_bullet.rect.top < height]
        for enemy_bullet in enemy_bullets:
            pygame.draw.rect(screen, white, enemy_bullet.rect)
    if player.vivo:
        dibujar_nave(player)
    pygame.display.flip()
pygame.quit()
sys.exit()