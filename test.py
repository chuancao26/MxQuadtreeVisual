import pygame

from random import randint
from MXQuadtree import *
from Particle import Particle
from pygame.math import Vector2
from range import *

Width, Height = 1000, 1000
screen = pygame.display.set_mode((Width, Height))

pygame.display.set_caption("MXQuadtree")
clock = pygame.time.Clock()
fps = 60

Background = (0, 0, 0)
particles = []
RADIUS = 10

rangeRect = Rectangle(Vector2(125, 125), Vector2(125, 125))
rangeRect.color = (0, 255, 0)
rangeRect.lineThickness = 3

boundary = Rectangle(Vector2(0, 0), Vector2(Width, Height))

MXquadtree = MXQuadTree(boundary)

# print(points)
moveParticle = False
particleCollision = False
showRange = True
run = True
while run:
    screen.fill(Background)
    pygame.display.set_caption("MXQuadTree Fps: " + str(int(clock.get_fps())))
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
            x = round(x)  
            y = round(y) 
            particle = Particle(Vector2(x, y), RADIUS, (255, 255, 255))
            particles.append(particle)
            MXquadtree.insert(particle)


    MXquadtree.Show(screen)

    for particle in particles:
        if moveParticle:
            particle.move()
        particle.draw(screen)

    rangeRect.position.x, rangeRect.position.y = pygame.mouse.get_pos()
    rangeRect.position.x -= rangeRect.scale.x // 2
    rangeRect.position.y -= rangeRect.scale.y // 2
    points = MXquadtree.queryRange(rangeRect)


    if showRange == True:
        for point in points:
            point.Highlight((255, 0, 255))
            point.draw(screen, RADIUS + 2)
        rangeRect.Draw(screen)
    pygame.display.flip()

pygame.quit()
