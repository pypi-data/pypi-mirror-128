from .user import User

class Interaction:
    def __init__(self, interaction,api):
        self.id = interaction["id"]
        self.type = interaction["type"]
        self.channel_id = interaction["channel_id"]
        self.name = interaction["data"]["name"]
        self.application_id = interaction["application_id"]
        self.guild_id = interaction["guild_id"]
        self.user = User(interaction["member"]["user"])
        self.api = api
        self.token = interaction["token"]
    def send(self, content):
        return self.api.slash_reply(self.id,self.token,content)