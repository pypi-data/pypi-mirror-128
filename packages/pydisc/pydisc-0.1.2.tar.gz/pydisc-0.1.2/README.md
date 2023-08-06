# pydisc

## a discord bot wrapper for python have slash command

#### 🚧 this project stell in Alpha now and is very unstable 🚧

# install

```bash
pip install pydisc
```

# usage

## create a slash_command

```python
from pydisc import setup
command=setup.Command('applications_id','token')
command.create('command','description')
```

## create a bot

```python
import pydisc

bot = pydisc.Bot()


@bot.event
async def ready():
    print(bot.user.username)
    print(bot.user.id)
    print(bot.user)

#slash command
@bot.command
async def ping(ctx):
    ctx.send("pong")

bot.run('token')
```

#todo:

- [ ] all events
- [ ] slash option
- [ ] slash permission
- [ ] config
- [ ] Components
- [ ] embed
- [ ] error
- [ ] asynchronous request
- [ ] docs
- [ ] example
- [ ] website
- [ ] support server
- [ ] a logo
