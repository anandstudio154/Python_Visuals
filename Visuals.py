
import pygame
from math import *
import random
# Values
HEIGHT = 600
WIDTH = 1200
max_speed = 0.3
particle_num = 200
trail_length = 1 #Lower value means longer trails
#------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Glare")
fade = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
fade.set_alpha(trail_length)
fade.fill((0,0,0))
# Glow
glow_surface = pygame.Surface((WIDTH,HEIGHT))
glow_surface.set_colorkey((0,0,0))
running = True
class Particle:
    def __init__(self):
        self.x = random.randint(0,WIDTH)
        self.y = random.randint(0,HEIGHT)
        self.vx = random.uniform(-0.2,0.2)
        self.vy = random.uniform(-0.2,0.2)
    def update(self):
        mx,my = pygame.mouse.get_pos()
        if mx>0 and mx<WIDTH and my>0 and my<HEIGHT:
            dist = ((mx-self.x)**2 + (my-self.y)**2)**0.5
            if dist!=0:
                if dist<120:
                    self.vx += ((self.x-mx)/dist)*0.05
                    self.vy += ((self.y-my)/dist)*0.05
                elif dist<250:
                    self.vx += ((mx-self.x)/dist)*0.01
                    self.vy += ((my-self.y)/dist)*0.01
            self.x += self.vx
            self.y += self.vy
            speed = sqrt(self.vx**2 + self.vy**2)
            if speed > max_speed:
                self.vx = (self.vx/speed)*max_speed
                self.vy = (self.vy/speed)*max_speed
        else:
            self.x += self.vx
            self.y += self.vy
        if self.x<0: self.x=WIDTH
        if self.x>WIDTH: self.x=0
        if self.y<0: self.y=HEIGHT
        if self.y>HEIGHT: self.y=0
    def draw(self):
        speed = ((self.vx)**2 + (self.vy)**2)**0.5
        min_s = 0.03
        max_s = 0.25
        t = (speed-min_s)/(max_s-min_s)
        t = max(0,min(1,t))
#        t = t**0.5
        r = int(255*t)
        g = int(255*(1-t))
        b = 150
        pygame.draw.circle(glow_surface,(r,g,b),(int(self.x),int(self.y)),10)
        pygame.draw.circle(glow_surface,(b,r,g),(int(self.x),int(self.y)),5)
        pygame.draw.circle(glow_surface,(g,b,r),(int(self.x),int(self.y)),3)
particles = []
for _ in range(particle_num):
    particles.append(Particle())
while running:
    screen.blit(fade,(0,0))
    glow_surface.fill((0,0,0))
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_r:
                max_speed = 0.3
        if event.type==pygame.QUIT:
            running = False
    for p in particles:
        p.update()
        p.draw()
    
    max_speed += 0.0001
    screen.blit(glow_surface,(0,0),special_flags=pygame.BLEND_ADD)
    pygame.display.update()
pygame.quit()
