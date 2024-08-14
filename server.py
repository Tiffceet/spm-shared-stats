import asyncio
import websockets
import json
from operator import itemgetter
from datetime import datetime
global_stats = {
    "score": 0,
    "coin": 0,
    "atk": 1,
    "lvl": 1,
    "hp": 10,
    "maxhp": 10
}


def apply_changes(changes):
    global_stats["score"] += changes["score"]
    global_stats["coin"] += changes["coin"]
    global_stats["atk"] += changes["atk"]
    global_stats["lvl"] += changes["lvl"]
    global_stats["hp"] += changes["hp"]
    global_stats["maxhp"] += changes["maxhp"]


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

    print(f"[{datetime.fromtimestamp(ts).strftime("%Y%m%d %H:%M:%S")}] <{client_uid}:{action}> {data}")

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

start_server = websockets.serve(handler, "0.0.0.0", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
