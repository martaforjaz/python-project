import pymunk
import pygame
import math
import time
from visualizer import apply_camera

WHITE = (255, 255, 255)
SHIP_SIZE = 15
ROTATION_SPEED = 2.0
THRUST_FORCE = 200
TRAIL_LENGTH = 30

class Agent:
    def __init__(self, space, world=None):
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, SHIP_SIZE))
        self.body.position = (400, 300)

        self.shape = pymunk.Circle(self.body, SHIP_SIZE)
        self.shape.elasticity = 0.5
        self.shape.collision_type = 0
        space.add(self.body, self.shape)

        self.trail = []
        self.health = 100
        self.score = 0
        self.world = world

        # Carregar imagem da nave
        original_image = pygame.image.load("assets/ship.png")
        scaled = pygame.transform.smoothscale(original_image, (40, 40))
        self.ship_image = pygame.transform.rotate(scaled, -90)

        # Escudo
        self.shield_active = False
        self.shield_activated_at = 0
        self.shield_duration = 3
        self.shield_cooldown = 5
        self.last_shield_time = -999

        # Disparo
        self.ammo = 5
        self.last_fire_time = 0
        self.fire_cooldown = 0.5

    def update(self):
        self.trail.append(self.body.position)
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)

        if self.shield_active and time.time() - self.shield_activated_at > self.shield_duration:
            self.shield_active = False
            
        # Limitar movimento da nave aos limites do mundo
        if self.world and hasattr(self.world, "world_bounds"):
            bounds = self.world.world_bounds
            x = max(bounds["x_min"], min(bounds["x_max"], self.body.position.x))
            y = max(bounds["y_min"], min(bounds["y_max"], self.body.position.y))
            self.body.position = (x, y)

    def thrust(self):
        direction = pymunk.Vec2d(1, 0).rotated(self.body.angle)
        self.body.apply_force_at_world_point(direction * THRUST_FORCE, self.body.position)

    def rotate(self, direction):
        self.body.angular_velocity = direction * ROTATION_SPEED

    def activate_shield(self):
        now = time.time()
        if now - self.last_shield_time >= self.shield_cooldown:
            self.shield_active = True
            self.shield_activated_at = now
            self.last_shield_time = now

    #def can_fire(self):
    #    return self.ammo > 0 and time.time() - self.last_fire_time >= self.fire_cooldown
    
    def can_fire(self):
        now = time.time()
        return self.ammo > 0 and (now - self.last_fire_time) > 1.0

    def draw(self, screen, camera_pos):
        for i, pos in enumerate(self.trail):
            pos_screen = apply_camera(pos, camera_pos)
            alpha = int(255 * (i / TRAIL_LENGTH))
            color = (255 - alpha, 255 - alpha, 255 - alpha)
            pygame.draw.circle(screen, color, (int(pos_screen.x), int(pos_screen.y)), 2)

        pos = self.body.position
        angle_degrees = -math.degrees(self.body.angle)
        rotated_image = pygame.transform.rotate(self.ship_image, angle_degrees)
        rect = rotated_image.get_rect(center=apply_camera(pos, camera_pos))
        screen.blit(rotated_image, rect.topleft)

        if self.shield_active:
            pos_screen = apply_camera(self.body.position, camera_pos)
            pygame.draw.circle(screen, (0, 120, 255), (int(pos_screen.x), int(pos_screen.y)), 28, width=2)

    def radar_scan(self, radius=200):
        if not self.world:
            return []

        results = []
        for entity in self.world.entities:
            if entity is self:
                continue

            try:
                pos = entity.body.position
            except AttributeError:
                continue

            dist = self.body.position.get_distance(pos)
            if dist <= radius:
                # rotula qualquer outra nave como \"Player\"
                if isinstance(entity, type(self)) and entity != self:
                    label = "Player"
                else:
                    label = type(entity).__name__
                
                results.append({
                    "type": label,
                    "position": tuple(pos),
                    "distance": dist
                })
        return results

    def get_sensors(self):
        return {
            "position": (self.body.position.x, self.body.position.y),
            "angle": self.body.angle,
            "velocity": (self.body.velocity.x, self.body.velocity.y),
            "health": self.health,
            "ammo": self.ammo,
            "can_fire": self.can_fire(),
            "shield": self.shield_active,
            "radar": self.radar_scan()
        }
