import pygame, math, sys, time, random
import sys
from math import cos, sin, sqrt
from pygame.locals import *

#TODO: 1) handle blitting with pygame.Sprite.Group.draw() (optional)
#      2) load images for all sprites and use sprite.Group.draw()
#      3) make somewhat game menu and sign in the end "You won" or "You lost"

pygame.init()

WIDTH = 800
HEIGHT = 600
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Triangle')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

colors = [RED, GREEN, BLUE]

sideLen = 60
heightLen = round(sideLen*math.sin(math.pi/3))

colors = [RED, GREEN, BLUE]

PLAYER_BULLET_VELOCITY = 2
ENEMY_BULLET_VELOCITY = -2

MAX_HEALTH = 100

def playAgain():
    print("Do you want to play again?(y/n)")
    s = input()
    if s == 'y':
        return True
    else:
        return False
    
#start Bullet class
class Bullet(pygame.sprite.Sprite):
    size = 10
    def __init__(self, Tx, Ty, player):
        pygame.sprite.Sprite.__init__(self)
         
        self.image = pygame.Surface((2*self.size, 2*self.size))

        self.rect = self.image.get_rect()
        self.rect.center = (Tx, Ty)

        self.player = player

    def move(self):
        if self.player:
            self.rect.centerx += PLAYER_BULLET_VELOCITY
        else:
            self.rect.centerx += ENEMY_BULLET_VELOCITY
        
    def draw(self):
        pygame.draw.circle(windowSurface, (200, 50, 50), self.rect.center, self.size)
    def is_out(self):
        return (self.rect.centerx <= 0 or self.rect.centerx >= WIDTH or self.rect.centery <= 0 or self.rect.centery >= HEIGHT)
    def collide(self, sprite):
        if pygame.sprite.collide_rect(self, sprite):
            return True
        else:
            return False
#end class

#start Triangle(game subject) class
class Triangle(pygame.sprite.Sprite):
    def __init__(self, startpos = (round(WIDTH/2), round(HEIGHT/2)), radius = 30, player = False):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([radius*sqrt(3), 1.5*radius])
        self.image.set_colorkey((0,0,0)) 

        self.rect = self.image.get_rect()
        
        self.radius = radius
        
        self.color = random.choice(colors)
        self.rect.center = [startpos[0], startpos[1]]

        self.bulletsGroup = pygame.sprite.Group()

        self.health = MAX_HEALTH

        self.player = player #принадлежность

    def move(self, direction):
        if direction == "left":
            self.rect.centerx-=1
        if direction == "right":
            self.rect.centerx+=1
        if direction == "bottom":
            self.rect.centery+=1
        if direction == "up":
            self.rect.centery-=1
    def get_points(self):
        return [(0, self.rect.h), (self.rect.w, self.rect.h), (round(self.rect.w/2), 0)]
    def draw(self):
        vertices = self.get_points()
        pygame.draw.polygon(self.image, self.color, vertices)
        windowSurface.blit(self.image, self.rect)
    def shoot(self):
        b = Bullet(self.rect.centerx, self.rect.centery, self.player)
        self.bulletsGroup.add(b)
    def getDamage(self):
        self.health-=10
    def rehealth(self):
        self.health = 100
    def update(self):
        self.draw()
        TGroup.remove(self)
        for b in self.bulletsGroup:
            b.draw()
            b.move()
            for sprite in TGroup:
                if b.collide(sprite):
                    sprite.getDamage()
                    self.bulletsGroup.remove(b)
                    
            if b.is_out():
                self.bulletsGroup.remove(b)
        TGroup.add(self)
#end class


clock = pygame.time.Clock()
FPS = 120

ENEMY_SHOOT_PERIOD = 100
enemy_shoot_latency = ENEMY_SHOOT_PERIOD

#start init game objects
def start_init(group):
    global T
    T = Triangle((100, 100), player = True)
    global T_enemy
    T_enemy = Triangle((WIDTH-100, round(HEIGHT/2)))
    group.add(T)
    group.add(T_enemy)

TGroup = pygame.sprite.Group()

start_init(TGroup)
#end init

def drawHealthBars(playerHealth, enemyHealth):
    playerHealthFull = pygame.Surface((MAX_HEALTH, 50))
    enemyHealthFull = pygame.Surface((MAX_HEALTH, 50))

    playerHealthCurrent = pygame.Surface((playerHealth, 50))
    enemyHealthCurrent = pygame.Surface((enemyHealth, 50))   

    playerHealthFull.fill(RED)
    enemyHealthFull.fill(RED)

    playerHealthCurrent.fill(GREEN)
    enemyHealthCurrent.fill(GREEN)
  
    playerHealthFull.blit(playerHealthCurrent, (0,0))
    enemyHealthFull.blit(enemyHealthCurrent, (0,0))
    
    windowSurface.blit(playerHealthFull, (20,20))
    windowSurface.blit(enemyHealthFull, (WIDTH-(MAX_HEALTH+20),20))

    
gameLoop = True

while gameLoop:
    clock.tick(FPS)
    
    windowSurface.fill((240, 240, 240))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                T.shoot()
    
    keys = pygame.key.get_pressed()
    if keys[K_a]:
        T.move("left")
    if keys[K_d]:
        T.move("right")
    if keys[K_w]:
        T.move("up")
    if keys[K_s]:
        T.move("bottom")

    if (enemy_shoot_latency > 0):
        enemy_shoot_latency -= 1
    else:
        T_enemy.shoot()
        enemy_shoot_latency = ENEMY_SHOOT_PERIOD
    
    for sprite in TGroup:
        sprite.update()

    drawHealthBars(T.health, T_enemy.health)
    
    #check for health
    if T.health <= 0:
        print("You lost!")
        if not playAgain():
            print("Goodbye! :)")
            gameLoop = False
        else:
            TGroup.empty()
            start_init(TGroup)

    if T_enemy.health <= 0:
        print("You won!")
        if not playAgain():
            print("Goodbye! :)")
            gameLoop = False
        else:
            TGroup.empty()
            start_init(TGroup)    
         
    pygame.display.update()

sys.exit()

    

