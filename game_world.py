import pymunk
import random
import time
from agent import Agent
from bullet import Bullet
from wall import Wall
from pickup import HealthPickup, AmmoPickup
from mine import Mine

class GameWorld:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)

        self.agent = Agent(self.space, world=self)
        self.bot_agent = Agent(self.space, world=self)
        # definir manualmente a posição do bot
        self.bot_agent.body.position = (1020, 300)  
        self.agent.body.position = (1000, 300)

        
        self.bullets = []
        self.score = 0

        self.entities = [self.agent, self.bot_agent]
        self.pickups = []
        self.mines = []

        self._create_map()
        self._create_initial_pickups()
        self._setup_collisions()

        self.world_bounds = {
            "x_min": 0,
            "x_max": 8500,
            "y_min": 0,
            "y_max": 2800
        }

        self.pickup_timer = 0
        self.pickup_interval = 5

    def _create_map(self):
        wall_size = (100, 40)
        spacing_x = 400
        spacing_y = 250
        rows = 10
        cols = 20
        base_x = 300
        base_y = 100

        for row in range(rows):
            for col in range(cols):
                x = base_x + col * spacing_x
                y = base_y + row * spacing_y

                pattern = (row * 3 + col) % 5

                if pattern == 0:
                    wall = Wall((x, y), wall_size, self.space)
                    self.entities.append(wall)
                elif pattern == 1:
                    wall = Wall((x, y), (40, 100), self.space)
                    self.entities.append(wall)
                elif pattern == 2:
                    wall1 = Wall((x - 30, y), (60, 20), self.space)
                    wall2 = Wall((x, y + 30), (20, 60), self.space)
                    self.entities.extend([wall1, wall2])
                elif pattern == 3:
                    wall = Wall((x, y), (80, 20), self.space)
                    self.entities.append(wall)

    def _create_initial_pickups(self):
        for i in range(1, 9):  # de 1000px a 8000px
            x_base = i * 1000
            for offset in [0, 100, 200, 300]:
                x = x_base + offset
                y = random.choice([200, 300, 400, 500, 600])
                kind = random.choice(["health", "ammo"])

                if kind == "health":
                    pickup = HealthPickup((x, y), self.space)
                else:
                    pickup = AmmoPickup((x, y), self.space)

                self.pickups.append(pickup)
                self.entities.append(pickup)

    def drop_mine(self):
        mine = Mine(self.agent.body.position, self.space)
        self.mines.append(mine)
        self.entities.append(mine)

    def fire_bullet(self, agent):
        if agent.can_fire():
            bullet = Bullet(agent.body.position, agent.body.angle, self.space)
            self.bullets.append(bullet)
            self.entities.append(bullet)  
            agent.ammo -= 1
            agent.last_fire_time = time.time()

    def update(self, dt):
        self.space.step(dt)
        self.agent.update()
        self.bullets = [b for b in self.bullets if b.update(dt)]

        self.pickup_timer += dt
        if self.pickup_timer >= self.pickup_interval:
            self.spawn_random_pickup()
            self.pickup_timer = 0

    def spawn_random_pickup(self):
        x = random.randint(300, self.world_bounds["x_max"] - 300)
        y = random.randint(100, self.world_bounds["y_max"] - 100)
        kind = random.choice(["health", "ammo"])

        if kind == "health":
            pickup = HealthPickup((x, y), self.space)
        else:
            pickup = AmmoPickup((x, y), self.space)

        self.pickups.append(pickup)
        self.entities.append(pickup)
        print(f"Spawned {kind} pickup at {(x, y)}")

    def _setup_collisions(self):
        handler_wall = self.space.add_collision_handler(0, 2)
        handler_wall.post_solve = self._on_agent_hit_wall

        handler_bullet = self.space.add_collision_handler(1, 0)
        handler_bullet.post_solve = self._on_bullet_hit_agent

        handler_health = self.space.add_collision_handler(0, 3)
        handler_health.begin = self._on_agent_pickup

        handler_ammo = self.space.add_collision_handler(0, 5)
        handler_ammo.begin = self._on_agent_pickup

        handler_mine = self.space.add_collision_handler(0, 4)
        handler_mine.begin = self._on_agent_hit_mine

    def _on_agent_hit_wall(self, arbiter, space, data):
        if not self.agent.shield_active:
            self.agent.health -= 1
        return True

    def _on_bullet_hit_agent(self, arbiter, space, data):
        for agent in [self.agent, self.bot_agent]:
            if arbiter.shapes[1] == agent.shape and not agent.shield_active:
                agent.health -= 10

    def _on_agent_pickup(self, arbiter, space, data):
        shape = arbiter.shapes[1]
        pickup = getattr(shape, "object", None)
        if pickup:
            if isinstance(pickup, HealthPickup):
                self.agent.health = min(100, self.agent.health + 30)
            elif isinstance(pickup, AmmoPickup):
                self.agent.ammo += 3
            self.space.remove(pickup.body, pickup.shape)
            if pickup in self.entities:
                self.entities.remove(pickup)
            if pickup in self.pickups:
                self.pickups.remove(pickup)
        return False

    def _on_agent_hit_mine(self, arbiter, space, data):
        shape = arbiter.shapes[1]
        mine = getattr(shape, "object", None)
        if mine and not mine.exploded and mine.is_armed():
            if not self.agent.shield_active:
                self.agent.health -= 40
            mine.explode(space)
            if mine in self.entities:
                self.entities.remove(mine)
            if mine in self.mines:
                self.mines.remove(mine)
        return False
