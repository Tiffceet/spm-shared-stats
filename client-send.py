
from spm_stats import get_stats
import asyncio
import websockets
import json
ws_url = 'ws://localhost:8000'
client_uid = 1


async def main():
    old_stat = {
        "score": 0,
        "coin": 0,
        "atk": 0,
        "lvl": 0,
        "hp": 0,
    }
    while True:
        stats = get_stats()
        for stat, value in stats.items():
            if old_stat[stat] != value:
                async with websockets.connect(ws_url) as ws:
                    await ws.send(json.dumps({"stats": stats, "client_uid": client_uid}))
                break
        old_stat = stats


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
