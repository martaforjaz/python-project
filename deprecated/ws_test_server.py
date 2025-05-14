#Only used for tests
import asyncio
import websockets

async def echo(websocket):
    print("Bot conectado")
    while True:
        msg = await websocket.recv()
        print("Recebido:", msg)

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        print("Servidor WebSocket no ar")
        await asyncio.Future()

asyncio.run(main())
