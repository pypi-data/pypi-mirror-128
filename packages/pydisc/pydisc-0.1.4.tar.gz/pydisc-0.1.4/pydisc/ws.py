import json, asyncio, websockets
from .api import api


class ws:
    def __init__(self):
        self.url = "wss://gateway.discord.gg/?v=6&encording=json"

    async def send(self, request):
        await self.ws.send(json.dumps(request))

    async def heartbeat(self):
        while True:
            await asyncio.sleep(self.heartbeat_interval)
            heartbeatJSON = {"op": 1, "d": "null"}
            await self.send(heartbeatJSON)

    async def recv(self):
        response = await self.ws.recv()
        if response:
            return json.loads(response)

    async def start(self, token, intents=None):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = None
        if token == None:
            if config != None:
                token = config["token"]
            else:
                raise Exception("No token provided and no config.json found")
                
        if not intents:
            if config != None:
                try:
                    intents = config["intents"]
                except KeyError:
                    intents = None
            else:
                intents = None
        async with websockets.connect(self.url) as self.ws:
            payload = {
                "op": 2,
                "d": {
                    "token": token,
                    "properties": {
                        "$os": "dispy",
                        "$browser": "Discord iOS",
                        "$device": "dispy",
                    },
                    "intents": intents,
                },
            }
            await self.send(payload)
            event = await self.recv()
            self.heartbeat_interval = event["d"]["heartbeat_interval"] / 1000
            asyncio.create_task(self.heartbeat())
            while True:
                event = await self.recv()
                await self.event_handler(event)

    def run(self, token=None, intents=None):
        self.api = api(token)
        asyncio.run(self.start(token, intents))
