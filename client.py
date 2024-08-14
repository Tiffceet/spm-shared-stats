
from spm_stats import get_stats, write_stats
import asyncio
import websockets
import json
import time
import uuid
ws_url = 'ws://spm.looz.online:8000'
client_uid = str(uuid.uuid4())

def get_changes(old_stat, new_stat):
    changes = {
        "score": 0,
        "coin": 0,
        "atk": 0,
        "lvl": 0,
        "hp": 0,
        "maxhp": 0,
    }
    for key, value in old_stat.items():
        if new_stat[key] != old_stat[key]:
            changes[key] = new_stat[key] - old_stat[key]
    return changes


def format_response(data):
    response = json.loads(json.dumps(data))
    response["client_uid"] = client_uid
    response["ts"] = time.time()
    return json.dumps(response)


async def main():
    # Get initial stats
    async with websockets.connect(ws_url) as ws:
        stats = get_stats()
        await ws.send(format_response({"action": "get_stats", "stats": stats}))
        response = await ws.recv()
        write_stats(json.loads(response))

    old_stats = get_stats()
    print("Status: Connected")
    print(f"Client UID: {client_uid}")
    while True:
        async with websockets.connect(ws_url) as ws:
            stats = get_stats()
            changes = get_changes(old_stats, stats)
            print(changes)
            await ws.send(format_response({"action": "report_stats", "changes": changes}))
            response = await ws.recv()
            write_stats(json.loads(response))
            old_stats = get_stats()
        time.sleep(1)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())