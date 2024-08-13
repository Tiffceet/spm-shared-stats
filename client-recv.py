import asyncio
from spm_stats import write_stats
import websockets
import json
client_uid = 1
ws_url = 'ws://localhost:8000'


async def main():
    async with websockets.connect(ws_url) as ws:
        while True:
            msg = await ws.recv()
            print(f"Received {msg}")

            msg_obj = json.loads(msg)
            if client_uid == msg_obj["client_uid"]:
                print("Received message from self, ignoring...")
                continue
            write_stats(msg_obj["stats"])


asyncio.get_event_loop().run_until_complete(main())
