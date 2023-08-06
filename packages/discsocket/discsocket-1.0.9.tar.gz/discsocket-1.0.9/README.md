# discsocket

Python framework for Discord interactions.

# Installation
`pip install discsocket`

# Introduction
This is the code needed for a minimal application with an on_ready event
```py
import discsocket

socket = discsocket.Socket()

# Event names go in the event decorator
# The function can be named whatever
@socket.event('ready')
async def ready():
  print(f"{socket.user.username} is connected")
 
socket.run('token')
```
# Extensions (Cogs)
If you're familiar with discord.py then you know about cogs. However in discsockets extensions don't inherit from a cog class.

```py
import discsocket

@discsocket.command('boop', 1)
async def boop_command(ctx):
    await ctx.callback('https://tenor.com/view/boop-gif-18601298')

```
Lets pretend that the file is called boop.py and is in a folder called extensions

```py
# It would be loaded into the client like this
socket.add_extension('extensions.boop')
```
