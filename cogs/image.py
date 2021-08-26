from numix_imports import *
from discord.utils import _URL_REGEX
from aiohttp import request
import requests
import numix_encrypt

config = default.get("./config.json")

def permission(permission):

	async def predicate(ctx):
		if ctx.author.id in config.owners:
			return True

		elif permission == "administrator":
			if ctx.author.guild_permissions.administrator:
				return True

			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)

		elif permission == "manage_messages":
			if ctx.author.guild_permissions.manage_messages:
				return True

			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)

		elif permission == "kick":
			if ctx.author.guild_permissions.kick:
				return True

			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)

		elif permission == "ban":
			if ctx.author.guild_permissions.ban:
				return True
				
			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)

		elif permission == "manage_guild":
			if ctx.author.guild_permissions.manage_guild:
				return True

			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)
		

	return commands.check(predicate)

class CustomCommand(commands.Command):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.perms = kwargs.get("perms", None)
		self.syntax = kwargs.get("syntax", None)

class Image(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.alex_api_token = self.config.alexflipnote_api
		self.discordrep_api = self.config.discordrep_api_token
		print('"Fun" cog loaded')

	async def developers(ctx):
		devs = [529499034495483926, 727365670395838626, 526711399137673232]
		if ctx.author.id in devs:
			return True

		else:
			await ctx.send(f"{self.config.forbidden} You can't use that command.")
			return False

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!triggered [user]", description="Triggers user profile picture.")
	async def triggered(self, ctx, user: discord.Member=None):
		if user is None:
			user = ctx.author
		image = await canvacord.trigger(user)
		file = discord.File(filename="triggered.gif", fp=image)
		await ctx.send(file=file)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!jail [user]", description="Profile picture in jail.")
	async def jail(self, ctx, user: discord.Member=None):
		if user is None:
			user = ctx.author
		image = await canvacord.jail(user)
		file = discord.File(filename="jail.png", fp=image)
		await ctx.send(file=file)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!aborted [user]", description="Image manipulates **aborted**")
	async def aborted(self, ctx, user: discord.Member=None):
		if user is None:
			user = ctx.author
		image = await canvacord.aborted(user)
		file = discord.File(filename="aborted.png", fp=image)
		await ctx.send(file=file)
    
	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!airpods [user]", description="Adds you airpods.")
	async def airpods(self, ctx, user: discord.Member=None):
		if user is None:
			user = ctx.author
		image = await canvacord.airpods(user)
		file = discord.File(filename="airpods.gif", fp=image)
		await ctx.send(file=file)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!america [user]", description="America")
	async def america(self, ctx, user: discord.Member=None):
		if user is None:
			user = ctx.author
		image = await canvacord.america(user)
		file = discord.File(filename="america.gif", fp=image)
		await ctx.send(file=file)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!wanted [user]", description="wanted")
	async def wanted(self, ctx, user: discord.Member=None):
		if user is None:
			user = ctx.author
		image = await canvacord.wanted(user)
		file = discord.File(filename="wanted.png", fp=image)
		await ctx.send(file=file)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!spank [user1] [user2]", description="spank")
	async def spank(self, ctx, user1: discord.Member=None, , user2: discord.Member=None):
		if user1 is None and user2 is None:
			await ctx.send(f"{self.config.forbidden} You need to specify 2 user to spank.")
			return
		if user2 is None:
			user2 = user1
			user1 = ctx.author
		image = await canvacord.spank(user1, user2)
		file = discord.File(filename="spank.png", fp=image)
		await ctx.send(file=file)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!bed [user]", description="bed")
	async def bed(self, ctx, user: discord.Member=None):
		if user is None:
			user = ctx.author
		image = await canvacord.bed(user)
		file = discord.File(filename="bed.png", fp=image)
		await ctx.send(file=file)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!jokeoverhead [user]", description="jokeoverhead")
	async def jokeoverhead(self, ctx, user: discord.Member=None):
		if user is None:
			user = ctx.author
		image = await canvacord.jokeoverhead(user)
		file = discord.File(filename="jokeoverhead.png", fp=image)
		await ctx.send(file=file)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!affect [user]", description="affect")
	async def affect(self, ctx, user: discord.Member=None):
		if user is None:
			user = ctx.author
		image = await canvacord.affect(user)
		file = discord.File(filename="affect.png", fp=image)
		await ctx.send(file=file)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!hitler [user]", description="hitler")
	async def hitler(self, ctx, user: discord.Member=None):
		if user is None:
			user = ctx.author
		image = await canvacord.hitler(user)
		file = discord.File(filename="hitler.png", fp=image)
		await ctx.send(file=file)

def setup(bot):
	bot.add_cog(Image(bot))
