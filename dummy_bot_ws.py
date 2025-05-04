import asyncio
import websockets
import json

async def run_bot():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            # Receber estado
            state = await websocket.recv()
            sensors = json.loads(state)
            print("Received:", sensors)

            # Enviar ação (exemplo aleatório)
            action = {
                "rotate": 1,
                "thrust": True,
                "fire": True
            }
            await websocket.send(json.dumps(action))
            await asyncio.sleep(1 / 10.0)

if __name__ == "__main__":
    asyncio.run(run_bot())
