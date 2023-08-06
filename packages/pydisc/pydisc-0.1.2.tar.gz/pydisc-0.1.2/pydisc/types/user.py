class User:
    def __init__(self, user):
        self.username = user["username"]
        self.id = user["id"]
        self.discriminator = user["discriminator"]
        self.avatar = user["avatar"]
        try:
            self.bot = user["bot"]
        except KeyError:
            self.bot = False
        self.discriminator = user["discriminator"]
        # self.roles = user['roles']

    @property
    def avatar_url(self):
        return "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.jpg".format(self)

    @property
    def mention(self):
        return "<@{0.id}>".format(self)

    @property
    def display_name(self):
        return self.username + "#" + self.discriminator

    def __str__(self):
        return self.display_name

    def __repr__(self):
        return self.display_name
