import time
import aiohttp
import discord
import importlib
import os
import sys
from discord_webhook import DiscordWebhook, DiscordEmbed

from discord.ext import commands
from utils import permissions, default, http, dataIO
from discord.utils import get

#meta data
redsafelogo = 'https://cdn.discordapp.com/avatars/545230136669241365/af33e499779a7f1f8dfad17b4bf72497.png?size=1024'
bversion = '2.0.1'
devs = '`Benitz Original#1317` and `Kittens#3154`'
botname = 'RedSafe'
cmd = '27'
events = '9'
accent = '0xF26A72'
#meta data

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self._last_result = None

    @commands.command()
    @commands.check(permissions.is_owner)
    async def say(self, ctx, str):
        message.delete()
        await ctx.send(str)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def remove(self, ctx, server: int):
        toleave = await self.bot.fetch_guild(server)
        left = discord.Embed(title='Removed Guild', description=f'Bot has been removed from Guild "{toleave.name}" by {ctx.author.name} \n\n **Note : Bot can only added back to guild by admins and Owners of removed guild.**', color=0xF26A72)
        left.set_footer(text=f'{botname} Developers', icon_url=redsafelogo)
        left.set_thumbnail(url=f'{toleave.avatar_url}')
        await ctx.send(embed=left)
        await toleave.leave()

    @commands.command()
    @commands.check(permissions.is_owner)
    async def guilds(self, ctx):
        embed = discord.Embed(title="Bot Guild Info", description='Information about all the guilds seen by the bot. \n\n ```{}```'.format(self.bot.guilds), color=0xF26A72)
        embed.set_footer(text=f'{botname} Developers', icon_url=redsafelogo)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def load(self, ctx, name: str):
        """ Loads an extension. """
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        em = discord.Embed(title='Cog Loaded', description=f'**{name}** cog has been loaded.', color=0xF26A72)
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def unload(self, ctx, name: str):
        """ Unloads an extension. """
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        em = discord.Embed(title='Cog Unloaded', description=f'**{name}** cog has been unloaded.', color=0xF26A72)
        em.set_footer(text=f'{botname} Developers', icon_url=redsafelogo)
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def reload(self, ctx, name: str):
        """ Reloads an extension. """
        try:
            self.bot.reload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        em = discord.Embed(title='Cog Reloaded', description=f'**{name}** cog has been reloaded.', color=0xF26A72)
        em.set_footer(text=f'{botname} Developers', icon_url=redsafelogo)
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
                    self.bot.reload_extension(f"cogs.{name}")
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

        em = discord.Embed(title='Cogs Reloaded', description=f'all cogs has been reloaded.', color=0xF26A72)
        em.set_footer(text=f'{botname} Developers', icon_url=redsafelogo)
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
        em = discord.Embed(title='Reloaded Module', description=f'{name_maker} Module has been loaded.', color=0xF26A72)
        em.set_footer(text=f'{botname} Developers', icon_url=redsafelogo)
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def reboot(self, ctx):
        """ Reboot the bot """
        em = discord.Embed(title='Bot Reboot', description=f'Bot is being rebooted by {botname} Developers.', color=0xF26A72)
        em.set_footer(text=f'{botname} Developers', icon_url=redsafelogo)
        await ctx.send(embed=em)
        time.sleep(1)
        sys.exit(0)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def notify(self, ctx, user_id: int, *, message: str):
        """ DM the user of your choice """
        user = self.bot.get_user(user_id)
        if not user:
            return await ctx.send(f'User ID "{user_id}" is invalid.')

        try:
            await user.send(message)
            await ctx.send(f"Notified User!")
        except discord.Forbidden:
            await ctx.send("Unable to notify user.")

def setup(bot):
    bot.add_cog(Admin(bot))
