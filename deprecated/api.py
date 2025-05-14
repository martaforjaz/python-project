import asyncio
import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from game_world import GameWorld

app = FastAPI()
world = GameWorld()  # inicializa o mundo

# Permitir chamadas externas (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/sensors")
def get_sensors():
    return world.agent.get_sensors()

@app.post("/act")
def act(action: dict):
    if action["action"] == "rotate_left":
        world.agent.rotate(-1)
    elif action["action"] == "rotate_right":
        world.agent.rotate(1)
    elif action["action"] == "stop_rotate":
        world.agent.rotate(0)
    elif action["action"] == "thrust":
        world.agent.thrust()
    elif action["action"] == "fire":
        world.fire_bullet()
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Bot connected via WebSocket.")

    try:
        while True:
            # Enviar sensores
            sensors = world.agent.get_sensors()
            await websocket.send_json(sensors)

            # Esperar ação
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
                action = json.loads(data)

                if action.get("rotate") is not None:
                    world.agent.rotate(action["rotate"])
                if action.get("thrust"):
                    world.agent.thrust()
                if action.get("fire"):
                    world.fire_bullet()
                if action.get("mine"):
                    world.drop_mine()
                if action.get("shield"):
                    world.agent.activate_shield()

            except asyncio.TimeoutError:
                pass  # nada recebido este tick

            await asyncio.sleep(1 / 60.0)  # 60 FPS

    except Exception as e:
        print(f"WebSocket connection closed: {e}")
        await websocket.close()

# Loop de simulação em background
@app.on_event("startup")
async def start_simulation_loop():
    async def loop():
        while True:
            world.update(1 / 60.0)
            await asyncio.sleep(1 / 60.0)
    asyncio.create_task(loop())

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
