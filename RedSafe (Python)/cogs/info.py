import time
import discord
import psutil
import os
import json

from datetime import datetime
from discord.ext import commands
from utils import default

#meta data
redsafelogo = 'https://cdn.discordapp.com/avatars/545230136669241365/af33e499779a7f1f8dfad17b4bf72497.png?size=1024'
bversion = '2.2.0'
devs = '`Benitz Original#1317` and `Kittens#3154`'
botname = 'RedSafe'
cmd = '27'
events = '9'
#meta data

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong", delete_after=0)
        ping = (time.monotonic() - before) * 1000
        p = discord.Embed(title=f"{botname}'s Ping", description=f'WebShock Ping: `{before_ws}m/s` | Rest Ping: `{int(ping)}m/s`', color=0xF26A72)
        p.set_footer(text=f'{botname}', icon_url=f'{redsafelogo}')
        p.timestamp = datetime.utcnow()
        await ctx.send(embed=p)

    @commands.command(aliases=['invites', 'invite', 'supportserver', 'feedbackserver'])
    async def support(self, ctx):
        embed = discord.Embed(title=f'{botname} Invites', description=f'Here are all the links related to **{botname}** \n\n > [Bot Invite](http://{botname}.bot.nu) \n > [Support Server](https://discord.com/cRTnVaQ) \n > [Website](https://google.com) \n\n This bot is **created**, **managed**, and **developed** by {devs}', color=0xF26A72)
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
        await ctx.send(embed=embed)

    @commands.command(aliases=['info', 'stats', 'status'])
    async def about(self, ctx):
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = round(len(self.bot.users) / len(self.bot.guilds))

        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefox = prefixes[str(ctx.guild.id)]

        embed = discord.Embed(title=f"<:i:768732098097446915> About {botname}", description=f'Your bot prefix is `{prefox}`', colour=0xF26A72)
        embed.set_thumbnail(url=redsafelogo)
        embed.add_field(name='Developers', value=f'{devs}', inline=False)
        embed.add_field(name='Bot Version', value=f'{bversion}', inline=False)
        embed.add_field(name="Library", value="discord.py", inline=False)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers} users/server )", inline=False)
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]), inline=False)
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=False)
        embed.set_footer(text=f'{botname}', icon_url=f'{redsafelogo}')
        embed.timestamp = datetime.utcnow()

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
