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
    try:
        obj = json.loads(data)
        print(f"[{obj["client_uid"]}] {obj["stats"]}")
        clients.remove(websocket)
    except:
        pass

    print(f"Total Clients: {len(clients)}")

    for websocket in clients:
        asyncio.create_task(send(websocket, data))

start_server = websockets.serve(handler, "0.0.0.0", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
