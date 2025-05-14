import pymunk
import pygame
import time
from visualizer import apply_camera

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

ACTIVATION_DELAY = 2.0  # segundos até mina ficar ativa

class Mine:
    def __init__(self, position, space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position

        self.shape = pymunk.Circle(self.body, 12)
        self.shape.collision_type = 4
        self.shape.sensor = True
        self.shape.object = self

        space.add(self.body, self.shape)

        self.spawn_time = time.time()
        self.exploded = False

    def is_armed(self):
        return time.time() - self.spawn_time >= ACTIVATION_DELAY

    def explode(self, space):
        if not self.exploded:
            space.remove(self.body, self.shape)
            self.exploded = True

    def draw(self, screen, camera_pos):
        if self.exploded:
            return

        pos = apply_camera(self.body.position, camera_pos)
        pygame.draw.circle(screen, RED, (int(pos.x), int(pos.y)), 12)

        elapsed = time.time() - self.spawn_time
        time_left = max(0, ACTIVATION_DELAY - elapsed)

        if not self.is_armed():
            font = pygame.font.SysFont("consolas", 14)
            timer_text = font.render(str(int(time_left + 1)), True, (255, 255, 255))
            screen.blit(timer_text, (
                int(pos.x) - timer_text.get_width() // 2,
                int(pos.y) - timer_text.get_height() // 2
            ))

        # Contorno cinzento antes, amarelo depois
        color = YELLOW if self.is_armed() else GRAY
        pygame.draw.circle(screen, color, (int(pos.x), int(pos.y)), 18, width=1)
