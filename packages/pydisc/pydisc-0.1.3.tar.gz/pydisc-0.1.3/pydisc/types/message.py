from .user import User


class Message:
    def __init__(self, message) -> None:
        self.type = message["type"]
        self.id = message["id"]
        self.channel_id = message["channel_id"]
        self.guild_id = message["guild_id"]
        self.author = User(message["author"])
        self.content = message["content"]
        self.timestamp = message["timestamp"]
        self.edited_timestamp = message["edited_timestamp"]
        self.tts = message["tts"]
        self.mention_everyone = message["mention_everyone"]
        self.mentions = message["mentions"]
        self.mention_roles = message["mention_roles"]
        self.attachments = message["attachments"]
        self.embeds = message["embeds"]
        try:
            self.reactions = message["reactions"]
        except KeyError:
            self.reactions = []
        self.nonce = message["nonce"]
        self.pinned = message["pinned"]
