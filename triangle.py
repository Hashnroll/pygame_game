import pygame, math, sys, time, random
from math import cos, sin
from pygame.locals import *

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
heightLen = math.ceil(sideLen*math.sin(math.pi/3))

colors = [RED, GREEN, BLUE]

#Cx, Cy = math.ceil(WIDTH/2), math.ceil(HEIGHT/2)

#start class
class Bullet:
    def __init__(self, Tx, Ty):
        self.size = 10
        self.x, self.y = Tx, Ty

    def move(self, velocity):
        self.x += velocity["horizontal"]
        self.y += velocity["vertical"]
    def draw(self, surface):
        pygame.draw.circle(surface, (100, 0, 255), (self.x, self.y), self.size)
    def is_out(self):
        return (self.x <= 0 or self.x >= WIDTH or self.y <= 0 or self.y >= HEIGHT)
#end class

#start class
class Triangle:
    def __init__(self):
        self.radius = 30
        self.angles = [-math.pi/2, -(math.pi*7)/6, (math.pi/6)]
        self.color = random.choice(colors)
        self.Cx, self.Cy = math.ceil(WIDTH/2), math.ceil(HEIGHT/2)

        self.bullets = []

        self.health = 100
        
    def rotate(self, Phi):
        self.angles = [(t + Phi) for t in self.angles]
        self.angles = [(t - 2*math.pi) if t > 2*math.pi else t for t in self.angles]
    def move(self, direction):
        if direction == "left":
            self.Cx-=1
        if direction == "right":
            self.Cx+=1
        if direction == "bottom":
            self.Cy+=1
        if direction == "up":
            self.Cy-=1
    def get_points(self):
        points = []
        for t in self.angles:
            x = self.Cx + self.radius * math.cos(t)
            y = self.Cy + self.radius * math.sin(t)
            points.append((x, y))
        return points
    def draw(self, surface):
        vertices = self.get_points()
        pygame.draw.polygon(surface, self.color, vertices)
        for b in self.bullets:
            b.draw(surface)
    def shoot(self):
        b = Bullet(self.Cx, self.Cy)
        self.bullets.append(b)
    def update_bullets(self):
        for b in self.bullets:
            b.move({"horizontal":2, "vertical":0})
            if b.is_out():
                self.bullets.remove(b)
#end class

windowSurface.fill((255, 255, 255))

T = Triangle()
T.draw(windowSurface)

pygame.display.update()

clock = pygame.time.Clock()
FPS = 120

while True:
    clock.tick(FPS)
    
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
    if keys[K_q]:
        T.rotate(-(1/100)*math.pi)
    if keys[K_r]:
        T.rotate((1/100)*math.pi)
            
    T.update_bullets()
    
    windowSurface.fill((255, 255, 255))
    T.draw(windowSurface)
    pygame.display.update()

    

#TODO: make an enemy with health, who can shoot. Arrange a duel between player and enemy. In the of this duel sign "You won" or "You lost" 


    


