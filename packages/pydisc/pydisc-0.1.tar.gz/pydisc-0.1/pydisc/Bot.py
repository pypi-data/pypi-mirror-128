from .ws import ws
from .types import User, Message, Interaction
import asyncio


class Bot(ws):
    def __init__(self):
        self.events = {}
        self.commands = {}
        super().__init__()

    async def event_handler(self, event):
        type = event["t"]
        if type == "READY" and ("READY" in self.events):
            self.user = User(event["d"]["user"])
            asyncio.create_task(self.events["READY"]())
        elif type == "MESSAGE_CREATE" and ("MESSAGE_CREATE" in self.events):
            asyncio.create_task(self.events["MESSAGE_CREATE"](Message(event["d"])))
        elif type == "MESSAGE_UPDATE" and ("MESSAGE_UPDATE" in self.events):
            asyncio.create_task(self.events["MESSAGE_UPDATE"](event["d"]))
        elif type == "INTERACTION_CREATE":
            if "INTERACTION_CREATE" in self.events:
                asyncio.create_task(self.events["INTERACTION_CREATE"](event["d"]))
            if event["d"]["data"]["name"] in self.commands:
                asyncio.create_task(
                    self.commands[event["d"]["data"]["name"]](
                        Interaction(event["d"], self.api)
                    )
                )

    def event(self, func):
        if func.__name__ in self.events:
            raise Exception("event already exists")
        if func.__name__ == "ready":
            self.events["READY"] = func
        elif func.__name__ == "message_create":
            self.events["MESSAGE_CREATE"] = func
        elif func.__name__ == "message_update":
            self.events["MESSAGE_UPDATE"] = func
        elif func.__name__ == "interaction_create":
            self.events["INTERACTION_CREATE"] = func
        else:
            raise Exception("event not found")

    def command(self, func):
        if func.__name__ in self.commands:
            raise Exception("command already exists")
        else:
            self.commands[func.__name__] = func
