
from spm_stats import get_stats, write_stats
import asyncio
import websockets
import json
import time
ws_url = 'ws://localhost:8000'
client_uid = 1


async def main():
    while True:
        async with websockets.connect(ws_url) as ws:
            stats = get_stats()
            await ws.send(json.dumps({"stats": stats, "client_uid": client_uid, "ts": time.time()}))
            response = await ws.recv()
            write_stats(json.loads(response))
        time.sleep(1)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
