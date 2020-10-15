# Zombie-Game-With-Python

import pygame
from pygame import mixer
import random
import math

# initialise Pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((1024, 700))

# bg
background = pygame.image.load('Background image.jpg')

# bg sound
mixer.music.load('Background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Zombie Shooter')
icon = pygame.image.load('Icon.png')
pygame.display.set_icon(icon)

# ready- can't see bullet
# fire = can see the bullet
# bullet
bullet = pygame.image.load('Bullet.png')
bulletx = 660
bullety = 0
bullet_x_change = 10
bullet_y_change = 0
bullet_state = 'ready'

# firebullet function
def firebullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet, (x, y))


# player
playerImg = pygame.image.load('Shooter.png')
playerx = 660
playery = 372
playery_change = 0
playerx_change = 0

#player function
def player(x, y):
    screen.blit(playerImg, (x, y))

# enemy
enemyImg = []

#multiple enemies
enemyImg.append(pygame.image.load('enemy1.png'))
enemyImg.append(pygame.image.load('enemy2.png'))
enemyImg.append(pygame.image.load('enemy3.png'))
enemyImg.append(pygame.image.load('enemy4.png'))
enemyImg.append(pygame.image.load('enemy5.png'))
enemyImg.append(pygame.image.load('enemy2.png'))
#enemyImg.append(pygame.image.load('enemy(n).png'))


enemy_x = []
enemy_y = []
enemy_y_change = []
enemy_x_change = []
number_of_enemies = 6

# Assigning same features to multiple enemies

for i in range(number_of_enemies):
    # enemyImg.append(pygame.image.load('enemy(n).png'))
    enemy_x.append(random.randint(0, 100))
    enemy_y.append(random.randint(310, 600))
    # speed of enemy (y-axis)
    enemy_y_change.append(2)
    # speed of enemy (x-axis)
    enemy_x_change.append(10)

# Enemy function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# collison detection function
def isCollison(enemyx, enemyy, bullet_x, bullet_y):
    enemyy += 35
    distance = math.sqrt(math.pow(enemyx - bullet_x, 2) + math.pow(enemyy - bullet_y, 2))

    if distance < 45:
        return True
    else:
        return False


# score display
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 50

# Game over text
game_font = pygame.font.Font('freesansbold.ttf', 40)

# Score display function
def showscore(x, y):
    score_value = font.render('Score : ' + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))

# function to display game over text
def game_over_text():
    text = game_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(text, (300, 350))

# Game loop
running = True
while running:
    # R-G-B value
    screen.fill((0, 0, 0))

    # bg image
    screen.blit(background, (0, 0))

    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed then check whether the key pressed is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playery_change -= 3
            if event.key == pygame.K_DOWN:
                playery_change += 3
            if event.key == pygame.K_LEFT:
                playerx_change -= 3
            if event.key == pygame.K_RIGHT:
                playerx_change += 3

            # Gun control
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('Bullet.wav')
                    bullet_sound.set_volume(0.3)
                    bullet_sound.play()
                    bullety = playery
                    bulletx = playerx
                    firebullet(bulletx, bullety)

        # when key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playery_change = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # player movement
    playery += playery_change
    if playery < 310:
        playery = 310
    if playery > 624:
        playery = 624
    playerx += playerx_change
    if playerx < 0:
        playerx = 0
    if playerx > 635:
        playerx = 635

    # player function call
    player(playerx, playery)

    # enemy movement
    for i in range(number_of_enemies):

        # Game over
        if enemy_x[i] > 700:
            for j in range(number_of_enemies):
                enemy_x[j] = 2000
            game_over_text()
            break

        enemy_y[i] += enemy_y_change[i]
        if enemy_y[i] < 300:
            enemy_y_change[i] += 1
            enemy_x[i] += enemy_x_change[i]
        if enemy_y[i] > 600:
            enemy_y_change[i] -= 1
            enemy_x[i] += enemy_x_change[i]

        # collision check
        collision = isCollison(enemy_x[i], enemy_y[i], bulletx, bullety)
        if collision:
            bulletx = playerx
            bullet_state = 'ready'
            score += 1
            enemy_x[i] = random.randint(-40, 10)
            enemy_y[i] = random.randint(310, 350)
            hit_sound = mixer.Sound('collision.wav')
            hit_sound.set_volume(0.8)
            hit_sound.play()

        # enemy function call
        enemy(enemy_x[i], enemy_y[i], i)

    # bullet movement
    if bulletx <= 0:
        bulletx = playerx
        bullet_state = 'ready'
    if bullet_state == 'fire':
        firebullet(bulletx - 10, bullety + 7)
        bulletx -= bullet_x_change

    # score function call
    showscore(textx, texty)

    # update
    pygame.display.update()
