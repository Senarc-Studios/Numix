import ast
import discord
import asyncio
import traceback
from discord.ext import commands, tasks
import time
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from utils import permissions, default
from discord.utils import get
import re
import os
import youtube_dl
import shutil
from discord.ext.commands import has_permissions, MissingPermissions, errors
import pymongo
from pymongo import MongoClient

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    redsafelogo = 'https://cdn.discordapp.com/avatars/545230136669241365/3f00cd933cf382a9f06212367676e4af.png?size=1024'
    TOKEN = "NTQ1MjMwMTM2NjY5MjQxMzY1.XGQXIg.PFzVQMJXvyGK9aWt25k9Qb7ky_8"
    bversion = '1.6.2'
    devs = '`Benitz Original#1317` and `Kittens#3154`'
    botname = 'RedDead'
    cmd = '27'
    events = '9'

    #status

    status4 = 'You type ".help"'
    status2 = 'the Discord API'
    status3 = f'{botname} Premium'

    async def status_task():
        while True:
            global count
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status4))
            await asyncio.sleep(10)
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=status2))
            await asyncio.sleep(10)
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status3))
            await asyncio.sleep(10)
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{count} Servers"))
            await asyncio.sleep(10)



    @commands.Cog.listener()
    async def on_ready():
        before_ws = int(round(client.latency * 1000, 1))
        webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/760023398838960129/xYvZWgjgv5FpJAjUxaRCmnDovrtECKqSR5MCr-W607QdZ4qmxaAqvegRvQuh5n_U2LjT')
        embed = DiscordEmbed(title='Start-Up', description=f'{client.user} is Online.', color=0x00ff00)
        embed.add_embed_field(name='Bot Name:', value=f'**{client.user}**', inline=True)
        embed.add_embed_field(name='Logged In with ID:', value=f'`{client.user.id}`', inline=True)
        embed.add_embed_field(name='Ping:', value=f'**{before_ws}**ms', inline=True)
        embed.add_embed_field(name=':warning: NOTE! :warning:', value='This Bot is still in **beta stage** and will take a while to release.', inline=False)
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()
        client.loop.create_task(status_task())
        global count

        print('Bot ready')
        print(f"{botname} Active!")
        count = 0
        for guild in client.guilds:
            print("Connected to server: {}".format(guild))
            count +=1

        client.loop.create_task(status_task())

    @commands.Cog.listener()
    async def on_member_join(member):
        with open('onjoinconfigset.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(member.guild.id)]
        with open('onjoinconfig.json', 'r') as f:
            joe = json.load(f)
        joes = joe[str(member.guild.id)]
        print(joes)
        if joes == "enabled":
            channel = client.get_channel(prefix)
            embed = discord.Embed(title=f'{member.name} Joined', description=f'Hey {member.name}, Welcome to **{member.guild.name}** \n Have a nice stay!', color=242424)
            embed.set_image(url='https://cdn.discordapp.com/attachments/731716869576327201/744818377461071952/Welcome-Black-Text-White-BG.gif')
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f'{Guild.member_count}th Member', icon_url=f'{guild.icon_url}')
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(member):
        with open('onleaveconfigset.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(member.guild.id)]
        with open('onleaveconfig.json', 'r') as f:
            joe = json.load(f)
        joes = joe[str(member.guild.id)]
        print(joes)
        if joes == "enabled":
            channel = client.get_channel(prefix)
            embed = discord.Embed(title=f'{member.name} Left', description=f'{member.name} Left **{member.guild.name}** Bye! \n Hope you join back.', color=0xff0000)
            embed.set_image(url='https://media.giphy.com/media/3o6ZtcOxQ9vi8vb9Cg/giphy.gif')
            embed.set_footer(text=f'{Guild.member_count} Members left', icon_url=f'{guild.icon_url}')
            embed.set_thumbnail(url=member.avatar_url)
            await channel.send(embed=embed)


def setup(client):
    client.add_cog(Events(client))
