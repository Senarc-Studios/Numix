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


class load(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = default.get("config.json")
        self._last_result = None

    redsafelogo = 'https://cdn.discordapp.com/avatars/545230136669241365/3f00cd933cf382a9f06212367676e4af.png?size=1024'
    TOKEN = "NTQ1MjMwMTM2NjY5MjQxMzY1.XGQXIg.PFzVQMJXvyGK9aWt25k9Qb7ky_8"
    bversion = '1.6.2'
    devs = '`Benitz Original#1317` and `Kittens#3154`'
    botname = 'RedDead'
    cmd = '27'
    events = '9'

    @commands.command()
    @commands.check(permissions.is_owner)
    async def load(self, ctx, name: str):
        """ Loads an extension. """
        try:
            self.client.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        em = discord.Embed(title='Cog Loaded', description=f'{name} cog has been loaded.', color=242424)
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def unload(self, ctx, name: str):
        """ Unloads an extension. """
        try:
            self.client.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        em = discord.Embed(title='Cog Unloaded', description=f'{name} cog has been unloaded.', color=242424)
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def reload(self, ctx, name: str):
        """ Reloads an extension. """
        try:
            self.client.reload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        em = discord.Embed(title='Cog Reloaded', description=f'{name} cog has been reloaded.', color=242424)
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def reloadall(self, ctx):
        """ Reloads all extensions. """
        error_collection = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.client.reload_extension(f"cogs.{name}")
                except Exception as e:
                    error_collection.append(
                        [file, default.traceback_maker(e, advance=False)]
                    )

        if error_collection:
            output = "\n".join([f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection])
            return await ctx.send(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{output}"
            )

        em = discord.Embed(title='Cogs Reloaded', description=f'all cogs has been reloaded.', color=242424)
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def reloadutils(self, ctx, name: str):
        """ Reloads a utils module. """
        name_maker = f"utils/{name}.py"
        try:
            module_name = importlib.import_module(f"utils.{name}")
            importlib.reload(module_name)
        except ModuleNotFoundError:
            return await ctx.send(f"Couldn't find module named **{name_maker}**")
        except Exception as e:
            error = default.traceback_maker(e)
            return await ctx.send(f"Module **{name_maker}** returned error and was not reloaded...\n{error}")
        em = discord.Embed(title='Reloaded Module', description=f'{name_maker} Module has been loaded.', color=242424)
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def reboot(self, ctx):
        """ Reboot the bot """
        await ctx.send('Rebooting Client')
        time.sleep(1)
        sys.exit(0)

def setup(client):
    client.add_cog(load(client))
