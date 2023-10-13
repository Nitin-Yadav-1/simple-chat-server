
import asyncio
from fastapi import WebSocket


connected_sockets: set[WebSocket] = set()
lock: asyncio.Lock = asyncio.Lock()


async def connect(ws: WebSocket):
  async with lock:
    await ws.accept()
    connected_sockets.add(ws)


async def disconnect(ws: WebSocket):
  async with lock:
    connected_sockets.remove(ws)


async def broadcast_to_others(ws: WebSocket, msg: str):
  to_send = [socket.send_text(msg) for socket in connected_sockets if ws != socket]
  await asyncio.gather(*to_send)


async def broadcast(msg: str):
  to_send = [socket.send_text(msg) for socket in connected_sockets]
  await asyncio.gather(*to_send)

