from .user import User


class Embed:
    def __init__(self, embed):
        try:
            embed = embed[0]
        except IndexError:
            return None
        try:
            self.title = embed["title"]
        except KeyError:
            self.title = None
        try:
            self.description = embed["description"]
        except KeyError:
            self.description = None
        try:
            self.type = embed["type"]
        except KeyError:
            self.type = None
        try:
            self.author = embed["author"]
        except KeyError:
            self.author = None
        try:
            self.color = embed["color"]
        except KeyError:
            self.color = None
        try:
            self.footer = embed["footer"]
        except KeyError:
            self.footer = None
        self.embed = embed


class Message:
    def __init__(self, message, api) -> None:
        self.guild_id = message["guild_id"]
        self.channel_id = message["channel_id"]

        self.api = api
        message = self.api.get_channel_message(message["channel_id"], message["id"])
        self.type = message["type"]
        self.id = message["id"]
        self.author = User(message["author"])
        self.content = message["content"]
        self.timestamp = message["timestamp"]
        self.edited_timestamp = message["edited_timestamp"]
        self.tts = message["tts"]
        self.mention_everyone = message["mention_everyone"]
        self.mentions = message["mentions"]
        self.mention_roles = message["mention_roles"]
        self.attachments = message["attachments"]
        self.embeds = Embed(message["embeds"])
        try:
            self.reactions = message["reactions"]
        except KeyError:
            self.reactions = []
        self.pinned = message["pinned"]
