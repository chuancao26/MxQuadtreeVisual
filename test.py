import pygame

from random import randint
from Quadtree import *
from Particle import Particle
from pygame.math import Vector2
from range import *

Width, Height = 500, 500
screen = pygame.display.set_mode((Width, Height))

pygame.display.set_caption("Quadtree")
clock = pygame.time.Clock()
fps = 60

Background = (0, 0, 0)
particles = []
RADIUS = 10

NODE_CAPACITY = 1

rangeRect = Rectangle(Vector2(125, 125), Vector2(125, 125))
rangeRect.color = (255, 0, 0)
rangeRect.lineThickness = 2

boundary = Rectangle(Vector2(0, 0), Vector2(Width, Height))

quadtree = QuadTree(NODE_CAPACITY, boundary)

moveParticle = False
particleCollision = False
showRange = True
run = True
while run:
    screen.fill(Background)
    pygame.display.set_caption("QuadTree Fps: " + str(int(clock.get_fps())))
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                showRange = not showRange
            if event.key == pygame.K_e:
                moveParticle = not moveParticle
                particleCollision = moveParticle
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            particle = Particle(Vector2(x, y), RADIUS, (255, 255, 255))
            particles.append(particle)
            a=4
            while(a!=0):
                quadtree.insert(particle)
                a=a-1


    quadtree.Show(screen)

    for particle in particles:
        if moveParticle:
            particle.move()
        particle.draw(screen)

    rangeRect.position.x, rangeRect.position.y = pygame.mouse.get_pos()
    rangeRect.position.x -= 60 
    rangeRect.position.y -= 60
    points = quadtree.queryRange(rangeRect)
    
    if showRange == True:
        for point in points:
            point.Highlight((234, 210, 43))
            point.draw(screen, RADIUS + 2)
        rangeRect.Draw(screen)
    pygame.display.flip()

pygame.quit()
