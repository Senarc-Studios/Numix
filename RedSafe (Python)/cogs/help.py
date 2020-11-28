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

#meta data
redsafelogo = 'https://cdn.discordapp.com/avatars/545230136669241365/af33e499779a7f1f8dfad17b4bf72497.png?size=1024'
bversion = '2.2.0'
devs = '`Benitz Original#1317` and `Kittens#3154`'
botname = 'RedSafe'
cmd = '27'
events = '9'
#meta data

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            with open('prefixes.json', 'r') as f:
                prefixes = json.load(f)
            prefox = prefixes[str(ctx.guild.id)]
            embed = discord.Embed(title="> Command Categories", description=f'`config` - Config Commands \n `moderation` - Moderation Commands \n `general` - General commands anyone can use. \n `staff` - Commands that will help the staff members. \n `music` - Music Commands! \n `premium` - **Premium** Commands that will only work if you get **premium**. \n \n *You can do "{prefox}help <category>" to view the commands.*', color=0xF26A72)
            embed.set_footer(text=botname, icon_url=redsafelogo)
            await ctx.send(embed=embed)

    @help.command(name="config")
    async def help_config(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefox = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title='> Config Commands', description=f'`{prefox}set-welcome` - Sets the welcome channel and notifies when someone joins. \n \n `{prefox}set-mute` - Sets the mute role which is used in {prefox}mute \n \n `{prefox}set-report` - Sets the report log channel, Usage - **{prefox}set-report <#channel>** \n \n `{prefox}set-suggestion` - Sets the suggestion channel. \n \n `{prefox}links off` - Turns **off** all links and denies links to be sent. \n \n `{prefox}links on` - Turns **on** and allows links to be sent. \n \n `{prefox}verification <on/off/set>` - **On/Off/Set** a verification system. \n \n `{prefox}welcome <on/off/set>` - **On/Off/Set** Welcome Message. \n \n `{prefox}leave <on/off/set>` - **On/Off/Set** Leave Message. \n \n `{prefox}prefix` - Changes the **prefix** of RedSafe on that server.', color=0xF26A72)
        embed.set_footer(text=botname, icon_url=redsafelogo)
        await ctx.send(embed=embed)

    @help.command(name="moderation")
    async def help_moderation(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefox = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title='> Moderation Commands', description=f'`{prefox}kick` - **kicks** and **notifies** the mentioned User. \n\n `{prefox}ban` - **Bans** and **notifes** the mentioned User. \n\n `{prefox}mute` - Mutes the mentioned user permanently *(still in progress)*', color=accent)
        embed.set_footer(text=botname, icon_url=redsafelogo)
        help = await ctx.send(embed=embed)

    @help.command(name="general")
    async def help_general(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefox = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title='> General Commands', descrition=f'`{prefox}ping` - Shows the Webshock and Rest latency of the bot. \n\n `{prefox}invite` - Provides all the **links** that is related to {botname}. \n \n ', color=0xF26A72)
        embed.set_footer(text=botname, icon_url=redsafelogo)
        await ctx.send(embed=embed)

    @help.command(name="staff")
    async def help_staff(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefox = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title='> Staff Commands', description=f'`{prefox}notify` - Notifies the user with the message sent by the staff. \n\n `{prefox}clear` - Clears a specified ammount of messages. \n\n ', color=0xF26A72)
        embed.set_footer(text=botname, icon_url=redsafelogo)
        await ctx.send(embed=embed)

    @help.command(name="music")
    async def help_music(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefox = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title='> Music Commands', description=f"Sorry, {botname}'s Music Commands aren't ready.", color=0xF26A72)
        embed.set_footer(text=botname, icon_url=redsafelogo)
        await ctx.send(embed=embed)

    @help.command(name="premium")
    async def help_premium(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefox = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title='> Premium Commands', description=f"Sorry, {botname}'s Premium Commands aren't ready.", color=0xF26A72)
        embed.set_footer(text=botname, icon_url=redsafelogo)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(help(bot))
