import pygame

def apply_camera(pos, camera_pos):
    return pos - camera_pos + pygame.Vector2(400, 300)  # centro da tela

def draw_world(screen, world):
    screen.fill((10, 10, 10))
    camera_pos = world.agent.body.position

    for entity in world.entities:
        if hasattr(entity, "draw"):
            entity.draw(screen, camera_pos)

    draw_hud(screen, world)

def draw_key_icon(screen, pos, text):
    font = pygame.font.SysFont("consolas", 16)
    pygame.draw.rect(screen, (255, 255, 255), (*pos, 30, 20), 1)
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, (pos[0] + 5, pos[1] + 2))

def draw_hud(screen, world):
    pygame.draw.rect(screen, (0, 0, 150), (0, 0, 200, 600))
    font = pygame.font.SysFont("consolas", 20)
    agent = world.agent

    screen.blit(font.render("PLAYER 1", True, (255, 255, 255)), (20, 20))
    screen.blit(font.render(f"Score: {agent.score}", True, (255, 255, 255)), (20, 50))

    screen.blit(font.render("Health:", True, (255, 255, 255)), (20, 80))
    pygame.draw.rect(screen, (255, 255, 255), (20, 105, 120, 15), 1)
    pygame.draw.rect(screen, (255, 0, 0), (21, 106, max(0, int(118 * agent.health / 100)), 13))

    screen.blit(font.render(f"Ammo: {agent.ammo}", True, (255, 255, 255)), (20, 135))

    screen.blit(font.render("Controls:", True, (255, 255, 255)), (20, 170))
    draw_key_icon(screen, (20, 200), "↑")
    screen.blit(font.render("Thrust", True, (255, 255, 255)), (55, 200))

    draw_key_icon(screen, (20, 230), "←")
    draw_key_icon(screen, (60, 230), "→")
    screen.blit(font.render("Rotate", True, (255, 255, 255)), (100, 230))

    draw_key_icon(screen, (20, 260), "SPACE")
    screen.blit(font.render("Fire", True, (255, 255, 255)), (90, 260))

    draw_key_icon(screen, (20, 290), "M")
    screen.blit(font.render("Drop Mine", True, (255, 255, 255)), (60, 290))

    draw_key_icon(screen, (20, 320), "S")
    screen.blit(font.render("Shield", True, (255, 255, 255)), (60, 320))

    screen.blit(font.render("Legend:", True, (255, 255, 255)), (20, 370))

    pygame.draw.circle(screen, (0, 255, 0), (30, 400), 8)
    screen.blit(font.render("= Health Pickup", True, (255, 255, 255)), (50, 393))

    pygame.draw.circle(screen, (255, 0, 0), (30, 430), 8, 2)
    screen.blit(font.render("= Mine", True, (255, 255, 255)), (50, 423))

    pygame.draw.circle(screen, (0, 150, 255), (30, 460), 8)
    screen.blit(font.render("= Ammo Pickup", True, (255, 255, 255)), (50, 453))
