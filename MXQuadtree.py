import pygame
from pygame.math import Vector2
from range import *

class MXQuadTree:
    MIN_SIZE = 4
    MIN_DISTANCE = 10  # Distancia mínima permitida entre partículas

    def __init__(self, boundary):
        self.boundary = boundary
        self.particles = []
        self.color = (255, 255, 255)

        self.northWest = None
        self.northEast = None
        self.southWest = None
        self.southEast = None

    def subdivide(self):
        parent = self.boundary
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

        self.northWest = MXQuadTree(boundary_nw)
        self.northEast = MXQuadTree(boundary_ne)
        self.southWest = MXQuadTree(boundary_sw)
        self.southEast = MXQuadTree(boundary_se)

    def insert(self, particle):
        if not self.boundary.containsParticle(particle):
            return False

        # Verificar si hay una partícula existente en la misma ubicación o cerca
        if self._exists_near(particle):
            return False

        if self.boundary.scale.x <= self.MIN_SIZE and self.boundary.scale.y <= self.MIN_SIZE:
            self.particles.append(particle)
            return True

        if self.northWest is None:
            self.subdivide()

        if self.northWest.insert(particle):
            return True
        if self.northEast.insert(particle):
            return True
        if self.southWest.insert(particle):
            return True
        if self.southEast.insert(particle):
            return True

        return False


    def _exists_near(self, particle):
        """Método auxiliar para verificar si una partícula ya existe cerca"""
        # Verificar si hay partículas cercanas en la lista actual
        for p in self.particles:
            if p.position.distance_to(particle.position) < self.MIN_DISTANCE:
                return True

        # Verificar si hay partículas cercanas en las subdivisiones (si existen)
        if self.northWest is not None:
            if self.northWest._exists_near(particle):
                return True
            if self.northEast._exists_near(particle):
                return True
            if self.southWest._exists_near(particle):
                return True
            if self.southEast._exists_near(particle):
                return True

        return False

    def queryRange(self, _range):
        particlesInRange = []

        if isinstance(_range, Circle):
            if not _range.intersects(self.boundary):
                return particlesInRange
        elif isinstance(_range, Rectangle):
            if not _range.intersects(self.boundary):
                return particlesInRange

        for particle in self.particles:
            if _range.containsParticle(particle):
                particlesInRange.append(particle)

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
