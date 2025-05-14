import pymunk
import pygame
from visualizer import apply_camera

class HealthPickup:
    def __init__(self, position, space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.collision_type = 3
        self.shape.sensor = True
        self.shape.object = self
        space.add(self.body, self.shape)

    def draw(self, screen, camera_pos):
        pos = apply_camera(self.body.position, camera_pos)
        pygame.draw.circle(screen, (0, 255, 0), (int(pos.x), int(pos.y)), 10)

class AmmoPickup:
    def __init__(self, position, space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.collision_type = 5
        self.shape.sensor = True
        self.shape.object = self
        space.add(self.body, self.shape)

    def draw(self, screen, camera_pos):
        pos = apply_camera(self.body.position, camera_pos)
        pygame.draw.circle(screen, (0, 150, 255), (int(pos.x), int(pos.y)), 10)
