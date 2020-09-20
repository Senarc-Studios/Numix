import discord
import asyncio
from discord.ext import commands

client = discord.Client()
TOKEN = "NTQ1MjMwMTM2NjY5MjQxMzY1.XGQXIg.FSmA_URgc0pT71aGfLPtOaoaSXM"
client = commands.Bot(command_prefix = '.')

status4 = 'You type ".help"'
status2 = 'Discord API'
status3 = 'RedSafe Premium'
status1 = f"{len(client.guilds)} Servers"

async def status_task():
    while True:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status1))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status2))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status3))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status4))
        await asyncio.sleep(10)

@client.event
async def on_ready():
    client.loop.create_task(status_task())
    print('Bot ready')

client.run(TOKEN)
