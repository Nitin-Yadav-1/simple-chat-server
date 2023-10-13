

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

import websocket_connection_manager as manager


app = FastAPI()


@app.get("/")
async def home():
  html = '''<h1>Simple Chat Server</h1>'''
  return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await manager.connect(websocket)
  try:
    while True:
      text = await websocket.receive_text()
      await manager.broadcast_to_others(websocket, text)
  except WebSocketDisconnect:
    await manager.disconnect(websocket)
    await manager.broadcast("Someone disconnected")


