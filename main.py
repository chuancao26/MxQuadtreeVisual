import pygame
from random import randint
from MXQuadtree import *
from Particle import Particle
from pygame.math import Vector2
from range import *

# Configuración de pantalla
Width, Height = 1000, 1000
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("MXQuadtree")
clock = pygame.time.Clock()
fps = 60

# Variables y configuración de partículas
Background = (0, 0, 0)
RADIUS = 10
particles = []

# Generar partículas iniciales y agregarlas al sistema
for i in range(10):
    offset = 50
    x = randint(offset, Width - offset)
    y = randint(offset, Height - offset)
    col = (255, 255, 255)
    particle = Particle(Vector2(x, y), RADIUS, col)
    particles.append(particle)

# Configuración de ejecución del programa
moveParticle = True
showRange = False
showQuadtree = True
run = True

# Loop principal del programa
while run:
    screen.fill(Background)
    pygame.display.set_caption("MXQuadTree Fps: " + str(int(clock.get_fps())))
    clock.tick(fps)

    # Crear un nuevo MXQuadTree cada frame
    boundary = Rectangle(Vector2(0, 0), Vector2(Width, Height))
    MXquadtree = MXQuadTree(boundary)

    # Manejar eventos de teclado y ratón
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_e:
                moveParticle = not moveParticle
            if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                showRange = not showRange
            if event.key == pygame.K_RETURN or event.key == pygame.K_q:
                showQuadtree = not showQuadtree
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            particle = Particle(Vector2(x, y), RADIUS, (255, 255, 255))
            if MXquadtree.insert(particle):
                particles.append(particle)

    # Mover partículas e insertarlas en el nuevo MXQuadTree
    for particle in particles:
        if moveParticle:
            particle.move()
        MXquadtree.insert(particle)

    # Verificar colisiones y resaltarlas
    for particle in particles:
        rangeCircle = Circle(particle.position, RADIUS * 3)
        otros = MXquadtree.queryRange(rangeCircle)
        for other in otros:
            if particle != other and particle.collide(other):
                particle.Highlight((255, 0, 0))

    # Dibujar partículas
    for particle in particles:
        particle.draw(screen)

    # Mostrar el MXQuadTree si está habilitado
    if showQuadtree:
        MXquadtree.Show(screen)

    pygame.display.flip()

pygame.quit()
