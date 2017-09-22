import pygame, math, sys, time, random
import sys
from math import cos, sin, sqrt
from pygame.locals import *

#TODO: 

#done: 1) implement death function for Entity(some funny animation)

pygame.init()

WIDTH = 800
HEIGHT = 600
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simple game')

sideLen = 60
heightLen = round(sideLen*math.sin(math.pi/3))

MAX_HEALTH = 100
ENEMY_HEALTH = 30

def playAgain():
    drawText("Press any if you want to play again", font, windowSurface, (WIDTH / 4), (HEIGHT / 2))
    drawText("Press ESC if you want to quit", font, windowSurface, (WIDTH / 4), (3 * HEIGHT / 4))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return True
    
#start Bullet class
class Bullet(pygame.sprite.Sprite):
    size = 10
    def __init__(self, Tx, Ty, velocity):
        pygame.sprite.Sprite.__init__(self)
         
        self.image = pygame.Surface((2*self.size, 2*self.size))

        self.rect = self.image.get_rect()
        self.rect.center = (Tx, Ty)

        self.velocity = velocity

    def move(self):
        self.rect.centerx += self.velocity
        
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

#start common class
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.bulletsGroup = pygame.sprite.Group()

        self.health = MAX_HEALTH

    def draw(self):
        windowSurface.blit(self.image, self.rect)

    def getDamage(self):
        self.health -= 10
        
    def rehealth(self):
        self.health = 100
        
    def update(self):
        self.draw()
        EntityGroup.remove(self)
        for b in self.bulletsGroup:
            b.draw()
            b.move()
            for sprite in EntityGroup:
                if b.collide(sprite):
                    sprite.getDamage()
                    self.bulletsGroup.remove(b)
                    
            if b.is_out():
                self.bulletsGroup.remove(b)
        EntityGroup.add(self)

    def death(self, image):
        width = self.rect.width
        height = self.rect.height
        for i in range(3):
            width, height = round(0.7*width), round(0.7*height)
            self.image = pygame.transform.scale(pygame.image.load(image),(width, height))
            windowSurface.fill((240, 240, 240))
            for sprite in EntityGroup:
                sprite.draw()
            pygame.display.update()
            time.sleep(0.5)

class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        
        self.image = pygame.transform.scale(pygame.image.load('ironman.png'), (40, 60))

        self.image.set_colorkey((0,0,0)) 

        self.rect = self.image.get_rect()

        self.rect.center = (100, 100)
        
    def move(self, direction):
        if direction == "left":
            self.rect.centerx-=1
        if direction == "right":
            self.rect.centerx+=1
        if direction == "bottom":
            self.rect.centery+=1
        if direction == "up":
            self.rect.centery-=1

    def shoot(self):
        b = Bullet(self.rect.centerx, self.rect.centery, 2)
        self.bulletsGroup.add(b)

class Enemy(Entity):
    def __init__(self, startpos):
        Entity.__init__(self)
        
        self.image = pygame.image.load('leviathan.png')

        self.image.set_colorkey((0,0,0)) 

        self.rect = self.image.get_rect()

        self.rect.center = startpos

        self.health = ENEMY_HEALTH
        
    def shoot(self):
        b = Bullet(self.rect.centerx, self.rect.centery, -2)
        self.bulletsGroup.add(b)

#end class


clock = pygame.time.Clock()
FPS = 120

ENEMY_SHOOT_PERIOD = 100
enemy_shoot_latency = ENEMY_SHOOT_PERIOD

#set up font
font = pygame.font.SysFont(None, 48)

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, (255,255,255))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

#start init game objects
def start_init():
    global player
    player = Player()
    global enemy
    enemy = Enemy((WIDTH-100, round(HEIGHT/2)))
    EntityGroup.add(player)
    EntityGroup.add(enemy)

EntityGroup = pygame.sprite.Group()

#end init

def terminate():
    pygame.quit()
    sys.exit()

def drawHealthBars(playerHealth, enemyHealth):
    playerHealthFull = pygame.Surface((MAX_HEALTH, 50))
    enemyHealthFull = pygame.Surface((MAX_HEALTH, 50))

    playerHealthCurrent = pygame.Surface((playerHealth, 50))
    enemyHealthCurrent = pygame.Surface((enemyHealth, 50))   

    playerHealthFull.fill((255, 0, 0))
    enemyHealthFull.fill((255, 0, 0))

    playerHealthCurrent.fill((0, 255, 0))
    enemyHealthCurrent.fill((0, 255, 0))
  
    playerHealthFull.blit(playerHealthCurrent, (0,0))
    enemyHealthFull.blit(enemyHealthCurrent, (0,0))
    
    windowSurface.blit(playerHealthFull, (20,20))
    windowSurface.blit(enemyHealthFull, (WIDTH-(MAX_HEALTH+20),20))


drawText('Ironman', font, windowSurface, (WIDTH / 3), (HEIGHT /3))
drawText('Press a key to start.', font, windowSurface, (WIDTH / 3) - 30, (HEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

start_init()

gameLoop = True

while gameLoop:
    clock.tick(FPS)
    
    windowSurface.fill((240, 240, 240))

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_ESCAPE:
                terminate()
            
    
    keys = pygame.key.get_pressed()
    if keys[K_a]:
        player.move("left")
    if keys[K_d]:
        player.move("right")
    if keys[K_w]:
        player.move("up")
    if keys[K_s]:
        player.move("bottom")

    if (enemy_shoot_latency > 0):
        enemy_shoot_latency -= 1
    else:
        enemy.shoot()
        enemy_shoot_latency = ENEMY_SHOOT_PERIOD
    
    for sprite in EntityGroup:
        sprite.update()

    drawHealthBars(player.health, enemy.health)
    
    #check for health
    if player.health <= 0:
        player.death('ironman.png')
        windowSurface.fill((0,0,0))
        drawText('You lost!', font, windowSurface, (WIDTH / 3), (HEIGHT /3))
        if not playAgain():
            gameLoop = False
        else:
            EntityGroup.empty()
            start_init()

    if enemy.health <= 0:
        enemy.death('leviathan.png')
        windowSurface.fill((0,0,0))
        drawText('You won!', font, windowSurface, (WIDTH / 3), (HEIGHT /3))
        if not playAgain():
            gameLoop = False
        else:
            EntityGroup.empty()
            start_init()    
         
    pygame.display.update()

terminate()

    

