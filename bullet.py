import pymunk
import pygame
import math
from visualizer import apply_camera

WHITE = (255, 255, 255)
BULLET_RADIUS = 2
BULLET_SPEED = 600
BULLET_LIFETIME = 1.5

class Bullet:
    def __init__(self, position, angle, space):
        mass = 0.1
        radius = BULLET_RADIUS
        inertia = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, inertia)
        
        self.body.position = position
        self.body.angle = angle

        # Direção baseada no pico (→ direita)
        direction = pymunk.Vec2d(1, 0).rotated(angle)

        # Começa no pico do triângulo
        offset = direction.normalized() * 15
        self.body.position = position + offset
        self.body.angle = angle
        self.body.velocity = direction * BULLET_SPEED

        self.shape = pymunk.Circle(self.body, radius)
        self.shape.collision_type = 1
        self.shape.sensor = False
        space.add(self.body, self.shape)

        self.lifetime = BULLET_LIFETIME
        self.space = space

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.space.remove(self.body, self.shape)
            return False
        return True

    def draw(self, screen, camera_pos):
        pos = apply_camera(self.body.position, camera_pos)
        pygame.draw.circle(screen, WHITE, (int(pos.x), int(pos.y)), BULLET_RADIUS)
