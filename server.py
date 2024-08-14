import asyncio
import websockets
import json
from datetime import datetime
import os

global_stats = {
    "score": 0,
    "coin": 0,
    "atk": 1,
    "lvl": 1,
    "hp": 10,
    "maxhp": 10
}


def apply_changes(changes):
    global_stats["score"] = max(global_stats["score"] + changes["score"], 0)
    global_stats["coin"] = max(global_stats["coin"] + changes["coin"], 0)
    global_stats["atk"] = max(global_stats["atk"] + changes["atk"], 0)
    global_stats["lvl"] = max(global_stats["lvl"] + changes["lvl"], 0)
    global_stats["hp"] = max(global_stats["hp"] + changes["hp"], 0)
    global_stats["maxhp"] = max(global_stats["maxhp"] + changes["maxhp"], 0)


async def send(websocket, message):
    try:
        await websocket.send(message)
    except websockets.ConnectionClosed:
        pass


async def handler(websocket, path):
    '''
    Create handler for each connection
    '''
    message = await websocket.recv()
    data = json.loads(message)
    action = data["action"]
    client_uid = data["client_uid"]
    ts = data["ts"]

    print(f"[{datetime.fromtimestamp(ts).strftime("%Y%m%d %H:%M:%S")}] <{
          client_uid}:{action}> {data}")

    if action == "get_stats":
        # Force override player stats if client_uid = 1
        if data["client_uid"] == 1:
            global_stats["score"] = data["stats"]["score"]
            global_stats["coin"] = data["stats"]["coin"]
            global_stats["atk"] = data["stats"]["atk"]
            global_stats["lvl"] = data["stats"]["lvl"]
            global_stats["hp"] = data["stats"]["hp"]
            global_stats["maxhp"] = data["stats"]["maxhp"]
        await websocket.send(json.dumps(global_stats))
        return

    if action == "report_stats":
        changes = data["changes"]
        apply_changes(changes)
        await websocket.send(json.dumps(global_stats))
        return

    await websocket.send(json.dumps(global_stats))

port = 8000 if not hasattr(os.environ, 'PORT') else os.environ["PORT"]
start_server = websockets.serve(handler, "0.0.0.0", port)
print(f"Listening ws://0.0.0.0:{port}")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
