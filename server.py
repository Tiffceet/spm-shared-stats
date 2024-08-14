import asyncio
import websockets
import json

clients = set()


async def send(websocket, message):
    try:
        await websocket.send(message)
    except websockets.ConnectionClosed:
        pass

# create handler for each connection


async def handler(websocket, path):
    clients.add(websocket)
    data = await websocket.recv()

    print(f"Total Clients: {len(clients)}")

    await websocket.send(json.dumps({
        "score": 6969,
        "coin": 999,
        "atk": 69,
        "lvl": 2,
        "hp": 2,
        "maxhp": 3
    }))

start_server = websockets.serve(handler, "0.0.0.0", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
