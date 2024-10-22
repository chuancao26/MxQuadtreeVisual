import pygame
from pygame.math import Vector2
from range import *

class QuadTree:
    MIN_SIZE = 10  # Tamaño mínimo del cuadrante para detener la subdivisión

    def __init__(self, capacity, boundary):
        self.capacity = capacity
        self.boundary = boundary
        self.particles = []
        self.color = (255, 255, 255)

        self.northWest = None
        self.northEast = None
        self.southWest = None
        self.southEast = None

    def subdivide(self):
        parent = self.boundary

        # Calculamos los nuevos límites para los cuadrantes hijos
        half_scale = parent.scale / 2

        boundary_nw = Rectangle(
            Vector2(parent.position.x, parent.position.y),
            half_scale
        )
        boundary_ne = Rectangle(
            Vector2(parent.position.x + half_scale.x, parent.position.y),
            half_scale
        )
        boundary_sw = Rectangle(
            Vector2(parent.position.x, parent.position.y + half_scale.y),
            half_scale
        )
        boundary_se = Rectangle(
            Vector2(parent.position.x + half_scale.x, parent.position.y + half_scale.y),
            half_scale
        )

        # Creamos las subregiones
        self.northWest = QuadTree(self.capacity, boundary_nw)
        self.northEast = QuadTree(self.capacity, boundary_ne)
        self.southWest = QuadTree(self.capacity, boundary_sw)
        self.southEast = QuadTree(self.capacity, boundary_se)

    def insert(self, particle):
        # Verificamos si la partícula está dentro de los límites actuales
        if not self.boundary.containsParticle(particle):
            return False

        # Si el tamaño del cuadrante es el mínimo permitido, almacenamos la partícula en la hoja
        if self.boundary.scale.x <= self.MIN_SIZE and self.boundary.scale.y <= self.MIN_SIZE:
            self.particles.append(particle)
            return True

        # Si aún no se ha subdividido, lo hacemos ahora
        if self.northWest is None:
            self.subdivide()

        # Insertamos en los cuadrantes correspondientes
        if self.northWest.insert(particle):
            return True
        if self.northEast.insert(particle):
            return True
        if self.southWest.insert(particle):
            return True
        if self.southEast.insert(particle):
            return True

        return False

    def queryRange(self, _range):
        particlesInRange = []

        # Verificamos si hay intersección entre el rango y el cuadrante actual
        if isinstance(_range, Circle):
            if _range.intersects(self.boundary) == False:
                return particlesInRange
        elif isinstance(_range, Rectangle):
            if _range.intersects(self.boundary) == True:
                return particlesInRange

        # Verificamos las partículas dentro del cuadrante actual
        for particle in self.particles:
            if _range.containsParticle(particle):
                particlesInRange.append(particle)

        # Consultamos las subregiones si existen
        if self.northWest is not None:
            particlesInRange += self.northWest.queryRange(_range)
            particlesInRange += self.northEast.queryRange(_range)
            particlesInRange += self.southWest.queryRange(_range)
            particlesInRange += self.southEast.queryRange(_range)

        return particlesInRange

    def Show(self, screen):
        self.boundary.Draw(screen)
        if self.northWest is not None:
            self.northWest.Show(screen)
            self.northEast.Show(screen)
            self.southWest.Show(screen)
            self.southEast.Show(screen)
