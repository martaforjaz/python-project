import pymunk
import pygame
from visualizer import apply_camera

BLUE = (80, 160, 255)

class Wall:
    def __init__(self, position, size, space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position

        w, h = size
        points = [(-w//2, -h//2), (w//2, -h//2), (w//2, h//2), (-w//2, h//2)]
        self.shape = pymunk.Poly(self.body, points)
        self.shape.collision_type = 2
        space.add(self.body, self.shape)

    def draw(self, screen, camera_pos):
        points = [apply_camera(self.body.local_to_world(v), camera_pos) for v in self.shape.get_vertices()]
        pygame.draw.polygon(screen, BLUE, points, width=2)
