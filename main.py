import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("space invaders")
pygame.display.set_icon(pygame.image.load('player.png'))
background = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player icon
playerimg = pygame.image.load('player.png')
playerx = 370
playery = 480
player_x = 0
player_y = 0

# Enemy icon
enemyimg = []
enemyx = []
enemyy = []
enemy_x = []
enemy_y = []
noofenemies = 6
for i in range(noofenemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemy_x.append(2.2)
    enemy_y.append(20)

# Bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bullet_x = 0
bullet_y = 10
bullet_state = 'ready'

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
gamefont = pygame.font.Font('freesansbold.ttf', 64)


def gameover():
    gamerover1 = gamefont.render('GAME OVER', True, (255, 255, 255))
    screen.blit(gamerover1, (200, 250))


def scorevalue():
    scorevalue1 = font.render("Score: " + str(score), True, (255, 225, 255))
    screen.blit(scorevalue1, (10, 10))


# Player function
def player(x, y):
    screen.blit(playerimg, (round(x), round(y)))


# Enemy function
def enemy(x, y, i):
    screen.blit(enemyimg[i], (round(x), round(y)))


# Bullet function
def bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (round(x + 16), round(y + 10)))


# collision
def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            player_x = +4
        if event.key == pygame.K_LEFT:
            player_x = -4
        if event.key == pygame.K_SPACE:
            if bullet_state == 'ready':
                bullet(playerx, bullety)
                bulletx = playerx
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
            player_x = 0

    playerx += player_x

    # Player Boundary
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # Enemy movement
    for i in range(noofenemies):
        if enemyy[i] > 400:
            for j in range(noofenemies):
                enemy_y[j] = 2000
                gameover()
            break

        enemyx[i] += enemy_x[i]
        if enemyx[i] <= 0:
            enemy_x[i] += 2.2
            enemyy[i] += enemy_y[i]
        elif enemyx[i] >= 736:
            enemy_x[i] += -2.2
            enemyy[i] += enemy_y[i]

        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullety = 480
            bullet_state = 'ready'
            score += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i], i)

    # Bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        bullet(bulletx, bullety)
        bullety -= bullet_y

    player(playerx, playery)
    scorevalue()
    pygame.display.update()
