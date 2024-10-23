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

# Definimos el rectángulo que se mueve con el mouse
rangeRect = Rectangle(Vector2(125, 125), Vector2(125, 125))
rangeRect.color = (0, 255, 0)  # Color inicial del rectángulo (verde)
rangeRect.lineThickness = 3

boundary = Rectangle(Vector2(0, 0), Vector2(Width, Height))
MXquadtree = MXQuadTree(boundary)

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
            if MXquadtree.insert(particle):
                particles.append(particle) 

    # Mostrar el quadtree
    MXquadtree.Show(screen)

    for particle in particles:
        if moveParticle:
            particle.move()
        
        # Cambiar color a amarillo si la partícula está dentro del rango
        if rangeRect.containsParticle(particle):
            particle.color = (255, 255, 0)  # Amarillo
        else:
            particle.color = (255, 255, 255)  # Blanco (color original)

        particle.draw(screen)

    # Actualizar la posición del rectángulo basado en la posición del mouse
    rangeRect.position.x, rangeRect.position.y = pygame.mouse.get_pos()
    rangeRect.position.x -= rangeRect.scale.x // 2
    rangeRect.position.y -= rangeRect.scale.y // 2

    # Si mostrar rango es verdadero, dibujar el rectángulo y resaltar las partículas dentro
    if showRange:
        points = MXquadtree.queryRange(rangeRect)
        for point in points:
            point.Highlight((255, 0, 255))  # Resaltar en magenta
            point.draw(screen, RADIUS + 2)
        rangeRect.Draw(screen)

    pygame.display.flip()

pygame.quit()
