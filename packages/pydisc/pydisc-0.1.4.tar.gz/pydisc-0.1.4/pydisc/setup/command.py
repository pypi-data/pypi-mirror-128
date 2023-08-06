import requests, json


class Command:
    def __init__(self, app_id=None, token=None) -> None:
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
        if app_id == None:
            if config != None:
                app_id = config["app_id"]
            else:
                raise Exception("No app_id provided and no config.json found")
        self.app_id = app_id
        self.url = f"https://discord.com/api/v8/applications/{app_id}/commands"
        self.token = token
        self.headers = {
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
        }

    def create(self, name, description):
        res = {"name": name, "type": 1, "description": description}
        r = requests.post(self.url, headers=self.headers, json=res)
        return r.json()

    def delete(self, command_id):
        url = f"{self.url}/{command_id}"
        r = requests.delete(url, headers=self.headers)
        return r.text
