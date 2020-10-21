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

class filter(commands.Cog):
    def __init__(self, client):
        self.client = client

    redsafelogo = 'https://cdn.discordapp.com/avatars/545230136669241365/3f00cd933cf382a9f06212367676e4af.png?size=1024'
    TOKEN = "NTQ1MjMwMTM2NjY5MjQxMzY1.XGQXIg.PFzVQMJXvyGK9aWt25k9Qb7ky_8"
    bversion = '1.6.2'
    devs = '`Benitz Original#1317` and `Kittens#3154`'
    botname = 'RedDead'
    cmd = '27'
    events = '9'

    with open('badwords.txt','r') as f:
        bad_words = '|'.join(s for l in f for s in l.split(', '))
        bad_word_checker = re.compile(bad_words).search

    @commands.Cog.listener()
    async def on_message(message):
        if not message.author.bot:
            with open('swearfilterboi.json', 'r') as f:
                prefixes = json.load(f)
            if prefixes[str(message.guild.id)] == "enabled":
                if bad_word_checker(message.content):

                    with open('prefixes.json', 'r') as f:
                        prefixes = json.load(f)
                    prefox = prefixes[str(message.guild.id)]

                    await message.delete()
                    embed = discord.Embed(title=f'{message.guild.name}', description=f"Hey! You aren't allowed swear on **{message.guild.name}** \n\n *If swearing is allowed on this server, please contact a staff member to turn off the swear filter with `{prefox}swear off`*", color=0xff0000)
                    embed.set_footer(text=botname, icon_url=redsafelogo)
                    await message.author.send(embed=embed)
            else:
                print('')
                await client.process_commands(message)

def setup(client):
    client.add_cog(filter(client))
