# DEPRECATE: dont use
import asyncio
from spm_stats import write_stats
import websockets
import json
client_uid = 1
ws_url = 'ws://localhost:8000'


async def main():
    async with websockets.connect(ws_url) as ws:
        while True:
            response = await ws.recv()
            stats = json.loads(response)
            write_stats(stats)


asyncio.get_event_loop().run_until_complete(main())
