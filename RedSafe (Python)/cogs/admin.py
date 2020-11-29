import time
import aiohttp
import discord
import importlib
import os
import sys
import json

from discord_webhook import DiscordWebhook, DiscordEmbed
from discord.ext import commands
from utils import permissions, default, http, dataIO
from discord.utils import get

#meta data
redsafelogo = 'https://cdn.discordapp.com/avatars/545230136669241365/af33e499779a7f1f8dfad17b4bf72497.png?size=1024'
bversion = '2.2.0'
devs = '`Benitz Original#1317` and `MythicalKitten#0001`'
botname = 'RedSafe'
cmd = '27'
events = '9'
#meta data

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self._last_result = None

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
    async def bug(self, ctx, *, reason: commands.clean_content = None):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefox = prefixes[str(ctx.guild.id)]
        if reason == None:
            ctx.message.delete()
            nos = discord.Embed(title=f'{botname} Bugs', description=f"You have to do `{prefox}bug <bugreport>` to send a bug, `{prefox}bug` doesn't do anything.\n No report has been sent to the Developers.", color=0xF26A72)
            nos.set_footer(text=f'{botname}', icon_url=redsafelogo)
            await ctx.send(embed=nos, delete_after=10)
        else:
            ctx.message.delete()
            webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/758644853441298462/VTSA8bQ797HENYiQnhphnWpalE3UJHmod4tu27HjThs6HZl6pgIQLvtxCE1h1AyaJqMu')
            embed = DiscordEmbed(title=f'New Bug | {ctx.author.name}', description=f'Reporter Name: **{ctx.author.name}** \n Reporter ID: **{ctx.author.id}** \n Guild Name: **{ctx.guild.name}** \n Guild ID: **{ctx.guild.id}** \nGuild Owner ID: **{ctx.guild.owner_id}** \n\n **Bug** - {reason}', color=0xF26A72)
            embed.set_footer(text=f'{botname} Bugs', icon_url=redsafelogo)
            embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
            webhook.add_embed(embed)
            webhook.execute()
            rs = discord.Embed(title=f'{botname} Bugs', description=f'The bug has been reported to {botname} Developers. Thank you for reporting the bug.\n You can join {botname} support with `{prefox}invite`', color=0xF26A72)
            rs.set_footer(text=f'{botname}', icon_url=redsafelogo)
            await ctx.send(embed=rs, delete_after=10)

    @commands.command()
    async def say(self, ctx, *, msg):
        if ctx.message.author.id == 529499034495483926:
            await ctx.message.delete()
            await ctx.send(msg)
        elif ctx.message.author.id == ctx.guild.owner_id:
            await ctx.message.delete()
            await ctx.send(msg)
        else:
            await ctx.send("<:c:771005703849902151> You don't have permission to do that.")

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
