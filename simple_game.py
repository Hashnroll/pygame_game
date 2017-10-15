import pygame, math, sys, time, random
import sys
from pygame.locals import *

#TODO: 

#done: 1) implement death function for Entity(some funny animation)

pygame.init()

WIDTH = 800
HEIGHT = 600
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simple game')


MAX_HEALTH = 100
ENEMY_HEALTH = 30


clock = pygame.time.Clock()
FPS = 60

ENEMY_SHOOT_PERIOD = 50
enemy_shoot_latency = ENEMY_SHOOT_PERIOD

ENEMY_ADDITION_FREQUENCY = 100
enemy_addition_latency = ENEMY_ADDITION_FREQUENCY

DEFAULTVELOCITY = 4

def playAgain():
    drawText("Press any if you want to play again", font, windowSurface, (WIDTH / 4), (HEIGHT / 2))
    drawText("Press ESC if you want to quit", font, windowSurface, (WIDTH / 4), (3 * HEIGHT / 4))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: 
                    terminate()
                return True

def terminate():
    pygame.quit()
    sys.exit()
    
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

    def move(self, direction, velocity = DEFAULTVELOCITY):
        if direction == "left":
            self.rect.centerx -= velocity
        if direction == "right":
            self.rect.centerx += velocity
        if direction == "bottom":
            self.rect.centery += velocity
        if direction == "up":
            self.rect.centery -= velocity

    def collide(self, sprite):
        if pygame.sprite.collide_rect(self, sprite):
            return True
        else:
            return False

class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        
        self.image = pygame.transform.scale(pygame.image.load('ironman.png'), (40, 60))

        self.image.set_colorkey((0,0,0)) 

        self.rect = self.image.get_rect()

        self.rect.center = (100, 100)

        self.invincible = False

    def shoot(self):
        b = Bullet(self.rect.centerx, self.rect.centery, 2)
        self.bulletsGroup.add(b)

    def getDamage(self):
        if not player.invincible:
            self.health -= 10

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

    def getInvincibility(self, time):
        self.invincible = True
        self.image = pygame.transform.scale(pygame.image.load('ironman_invin.png'), (40, 60))
        startTime = pygame.time.get_ticks()
        return (startTime + time*1000)
        

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
    textobj = font.render(text, 1, (255, 255, 255))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def drawScore(text, font, surface, x, y):
    textobj = font.render(text, 1, (0, 0, 0))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    
#start init game objects
EntityGroup = pygame.sprite.Group()

def start_init():
    global player
    player = Player()
    EntityGroup.add(player)
#end init

def drawHealthBar(playerHealth):
    playerHealthFull = pygame.Surface((MAX_HEALTH, 50))
    playerHealthCurrent = pygame.Surface((playerHealth, 50))
    playerHealthFull.fill((255, 0, 0))
    playerHealthCurrent.fill((0, 255, 0))
    playerHealthFull.blit(playerHealthCurrent, (0,0))
    windowSurface.blit(playerHealthFull, (20,20))
    
drawText('Ironman', font, windowSurface, (WIDTH / 3), (HEIGHT /3))
drawText('Press a key to start.', font, windowSurface, (WIDTH / 3) - 30, (HEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

start_init()

gameLoop = True

score = 0

background = pygame.image.load('background.png')

while gameLoop:
    clock.tick(FPS)

    windowSurface.blit(background, background.get_rect())

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

    if (enemy_addition_latency > 0):
        enemy_addition_latency -= 1
    else:
        e = Enemy((random.randint(round(2*WIDTH/3), WIDTH - 50), random.randint(0, HEIGHT)))
        EntityGroup.add(e)
        enemy_addition_latency = ENEMY_ADDITION_FREQUENCY
    
    for sprite in EntityGroup:
        sprite.update()

    drawHealthBar(player.health)

    if player.invincible:
        curTime = pygame.time.get_ticks()
        if curTime > invincibleTime:
            player.invincible = False
            player.image = pygame.transform.scale(pygame.image.load('ironman.png'), (40, 60))
        
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

    EntityGroup.remove(player)

    for enemy in EntityGroup:
        if enemy.collide(player):
            if not player.invincible:
                player.getDamage()
                invincibleTime = player.getInvincibility(3)
        if enemy.rect.center[0] > WIDTH or enemy.rect.center[1] < 0 or enemy.rect.center[0] < 0 or enemy.rect.center[1] > HEIGHT:
            EntityGroup.remove(enemy)
        elif enemy.health <= 0:
            EntityGroup.remove(enemy)
            score += 10
        else:
            if (random.random() > 0.99):
                enemy.shoot()
            if random.random() > 0.5:
                enemy.move('up', 3)
            enemy.move('left', 3)
                
    EntityGroup.add(player)

    drawScore('Счет ' + str(score), font, windowSurface, WIDTH - 300, 20)
    
    pygame.display.update()

terminate()

    

