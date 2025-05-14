import asyncio
import math

class BotController:
    def __init__(self, agent):
        self.agent = agent

    async def start_server(self):
        print("🟢 Bot ativo (sem WebSocket)")
        while True:
            sensors = self.agent.get_sensors()
            action = self.decide_action(sensors)
            self.apply_action(action)
            await asyncio.sleep(1 / 20.0)

    def decide_action(self, sensors):
        radar = sensors.get("radar", [])
        my_pos = sensors["position"]
        my_angle = sensors["angle"]

        def angle_to(pos1, angle, pos2):
            dx = pos2[0] - pos1[0]
            dy = pos2[1] - pos1[1]
            desired = math.atan2(dy, dx)
            diff = desired - angle
            return (diff + math.pi) % (2 * math.pi) - math.pi

        for entity in radar:
            if entity["type"] == "Player":
                diff = angle_to(my_pos, my_angle, entity["position"])
                rotate = 1 if diff > 0.1 else -1 if diff < -0.1 else 0
                return {
                    "rotate": rotate,
                    "thrust": True,
                    "fire": sensors["can_fire"]
                }

        # Se não vê o jogador, anda e roda à procura
        return {
            "rotate": 1,
            "thrust": True,
            "fire": False
        }

    def apply_action(self, action):
        if action.get("rotate") is not None:
            self.agent.rotate(action["rotate"])
        if action.get("thrust"):
            self.agent.thrust()
        if action.get("fire") and self.agent.can_fire():
            self.agent.world.fire_bullet(self.agent)
