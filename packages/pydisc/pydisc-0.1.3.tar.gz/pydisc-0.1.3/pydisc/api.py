import requests
from requests.structures import CaseInsensitiveDict


class api:
    def __init__(self, token) -> None:
        self.base_url = "https://discord.com/api/v9"
        self.headers = CaseInsensitiveDict()
        self.headers["Authorization"] = f"Bot {token}"
        self.headers["Content-Type"] = "application/json"

    def get(self, path):

        url = f"{self.base_url}/{path}"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.text)

    def post(self, path, json):
        url = f"{self.base_url}/{path}"

        response = requests.post(url, headers=self.headers, json=json)
        try:
            return response.json()
        except:
            return response.text

    def get_guild(self, guild_id):
        return self.get(f"guilds/{guild_id}")

    def get_user(self, user_id):
        return self.get(f"users/{user_id}")

    def get_channel(self, channel_id):
        return self.get(f"channels/{channel_id}")

    def get_channel_message(self, channel_id, message_id):
        return self.get(f"channels/{channel_id}/messages/{message_id}")

    def send_message(self, channel_id, content):

        return self.post(f"channels/{channel_id}/messages", json={"content": content})

    def slash_reply(self, id, token, content):
        self.post(
            f"interactions/{id}/{token}/callback",
            {"type": 4, "data": {"content": content}},
        )
