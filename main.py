import pygame
import threading
import asyncio
from bot_server import BotController
from game_world import GameWorld
from visualizer import draw_world

def show_instructions(screen):
    font = pygame.font.SysFont("consolas", 32, bold=True)
    small_font = pygame.font.SysFont("consolas", 24)
    clock = pygame.time.Clock()

    while True:
        bg_image = pygame.image.load("IMG_2863.jpg").convert()
        bg_image = pygame.transform.scale(bg_image, screen.get_size())
        screen.blit(bg_image, (0, 0))

        # Painel transparente
        panel = pygame.Surface((600, 400), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))
        screen.blit(panel, (100, 100))

        # Título
        title = font.render("INSTRUCTIONS", True, (0, 255, 255))
        screen.blit(title, (400 - title.get_width() // 2, 130))

        # Lista de controlos
        lines = [
            "← Rotate Left",
            "→ Rotate Right",
            "↑ Thrust Forward",
            "SPACE Fire",
            "ESC Quit"
        ]
        for i, line in enumerate(lines):
            text = small_font.render(line, True, (255, 255, 255))
            screen.blit(text, (250, 200 + i * 40))

        esc_text = small_font.render("Press ESC to go back", True, (200, 200, 200))
        screen.blit(esc_text, (250, 400))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

def show_menu(screen):
    font_button = pygame.font.SysFont("consolas", 36, bold=True)
    font_title = pygame.font.SysFont("consolas", 72, bold=True)

    options = ["Start Game", "Instructions", "Exit"]
    selected = 0
    clock = pygame.time.Clock()

    while True:
        bg_image = pygame.image.load("IMG_2863.jpg").convert()
        bg_image = pygame.transform.scale(bg_image, screen.get_size())
        screen.blit(bg_image, (0, 0))

        screen_width, screen_height = screen.get_size()

        # Título "XPilot" no topo
        title_text = font_title.render("XPilot", True, (0, 255, 255))
        screen.blit(title_text, (
            screen_width // 2 - title_text.get_width() // 2,
            80
        ))

        # Botões
        for i, option in enumerate(options):
            rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 60 + i * 80, 300, 60)
            color = (255, 255, 255, 200) if i == selected else (200, 200, 200, 100)
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            s.fill(color)
            pygame.draw.rect(s, color, s.get_rect(), border_radius=30)
            screen.blit(s, rect.topleft)

            text = font_button.render(option, True, (0, 0, 0))
            screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected].lower()

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("XPilot Game")
    clock = pygame.time.Clock()

    world = None
    bot_controller = None
    
    while True:
        choice = show_menu(screen)
        if choice == "exit":
            break
        elif choice == "instructions":
            result = show_instructions(screen)
            if result == "exit":
                break
            continue
        elif choice == "start game":
            world = GameWorld()
            bot_controller = BotController(world.bot_agent)
            
            # Iniciar WebSocket do bot numa thread separada
            threading.Thread(
                target=lambda: asyncio.run(bot_controller.start_server()),
                daemon=True
            ).start()
            
            space_was_pressed = False

            running = True
            while running:
                dt = clock.tick(60) / 1000.0

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    world.agent.rotate(-1)
                elif keys[pygame.K_RIGHT]:
                    world.agent.rotate(1)
                else:
                    world.agent.rotate(0)

                if keys[pygame.K_UP]:
                    world.agent.thrust()

                if keys[pygame.K_SPACE]:
                    if not space_was_pressed:
                        world.fire_bullet(world.agent)
                    space_was_pressed = True
                else:
                    space_was_pressed = False

                if keys[pygame.K_ESCAPE]:
                    running = False
                    
                if keys[pygame.K_m]:
                    world.drop_mine()
                    
                if keys[pygame.K_s]:
                    world.agent.activate_shield()

                #while not bot_controller.queue.empty():
                #    action = bot_controller.queue.get_nowait()
                #    bot_controller.apply_action(action)
                 
                world.update(dt)   
                
                if world.agent.health <= 0:
                    draw_world(screen, world)
                    font = pygame.font.SysFont("consolas", 60, bold=True)
                    text = font.render("GAME OVER", True, (255, 0, 0))
                    screen.blit(text, (400 - text.get_width() // 2, 300 - text.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    running = False
                    continue
                
                draw_world(screen, world)
                pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
