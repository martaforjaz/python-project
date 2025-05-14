from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

connected_bots = []

@app.websocket("/ws/{bot_id}")
async def websocket_endpoint(websocket: WebSocket, bot_id: str):
    await websocket.accept()
    connected_bots.append(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            # Ex: data = {"action": "turn_left"}
            # Processa a ação do bot e envia perceção de volta
            perception = get_perception_for_bot(bot_id)
            await websocket.send_json(perception)
    except WebSocketDisconnect:
        connected_bots.remove(websocket)

def get_perception_for_bot(bot_id):
    # Aqui tu vais integrar com o teu jogo
    return {
        "enemy_seen": True,
        "enemy_position": [100, 200],
        "health": 80
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
