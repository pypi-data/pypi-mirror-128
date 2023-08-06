import json, os
from pathlib import Path


class Project:
    def __init__(self, name, token, intents=None, app_id=None) -> None:
        self.name = name
        
        Path(name).mkdir(parents=True, exist_ok=True)
        with open(f"{name}/config.json", "w") as f:
            json.dump(
                {"name": name, "token": token, "intents": intents, "app_id": app_id}, f
            )
        with open(f"{name}/__main__.py", "w") as f:
            f.write(
                """
import pydisc

bot = pydisc.Bot()

@bot.event
async def ready():
    print(bot.user.username)
    print(bot.user.id)
    print(bot.user)
bot.run()
"""
            )
        if app_id != None:
            with open(f"{name}/display_command.py", "w") as f:
                f.write(
                    """
from pydisc import setup
command = setup.Command()
command.create('name','description')
"""
                )
    def __str__(self) -> str:
        return f"Project {self.name}"