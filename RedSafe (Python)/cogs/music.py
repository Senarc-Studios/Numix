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

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    redsafelogo = 'https://cdn.discordapp.com/avatars/545230136669241365/3f00cd933cf382a9f06212367676e4af.png?size=1024'
    TOKEN = "NTQ1MjMwMTM2NjY5MjQxMzY1.XGQXIg.PFzVQMJXvyGK9aWt25k9Qb7ky_8"
    bversion = '1.6.2'
    devs = '`Benitz Original#1317` and `Kittens#3154`'
    botname = 'RedDead'
    cmd = '27'
    events = '9'

    @commands.command(pass_context=True)
    async def join(ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(client.voice.clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await ctx.send(f'{botname} has Joined {channel}')

    @commands.command()
    async def leave(ctx):
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f'{botname} has disconnected from {channel}')
        else:
            await ctx.send(f"{botname} isn't connected to any Voice Channels.")

def setup(client):
    client.add_cog(music(client))
