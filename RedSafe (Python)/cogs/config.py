import time
import discord
import psutil
import os
import json
import pymongo

from discord.utils import get
from datetime import datetime
from discord.ext import commands
from utils import default
from pymongo import MongoClient

#DB
cluster = MongoClient('mongodb+srv://RedSafe-Bot:F0H5XARYJt69SD9l@redsafe.hoqeu.mongodb.net/RedSafe?retryWrites=true&w=majority')
db = cluster['RedSafe']
#DB

#meta data
redsafelogo = 'https://cdn.discordapp.com/avatars/545230136669241365/af33e499779a7f1f8dfad17b4bf72497.png?size=1024'
bversion = '2.2.1'
devs = '`Danoxzilla-X#7003`, `Benitz Original#1317` and `MythicalKittens#0001`'
botname = 'RedSafe'
cmd = '27'
events = '9'
#meta data

class Config(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
#prefix = {f"{message.guild.id}": .}
#                               ^
#SyntaxError: invalid syntax
#
#The above exception was the direct cause of the following exception:

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.guild.id is None:
			return
		else:
			try:
				prefix_from_db = db['Prefixes']
				test = prefix_from_db.find(message.guild.id)
				print(test)
			except AttributeError:
				prefix_from_db = db['Prefixes']
				pr = {f"{message.guild.id}": .}
				prefix_from_db.insert(pr)
				await bot.process_command(message) 

	@commands.command()# It's on session details in the Live Share Tab
	@commands.has_permissions(administrator=True)
	async def linkfilter(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)

		prefix = prefixes[str(ctx.guild.id)]
		
		if ctx.invoked_subcommand is None:
			embed = discord.Embed(title='Link Filter', description=f'You can turn **on**, **off**, or **set** the link filter \n Usage: \n \n `{prefix}swearfilter off` - Turns off link filter and allows people to post links. \n `{prefix}linkfilter on` - Turns on the link filter and avoids people from posting links.', color=0x00ff00)
			embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
			await ctx.send(embed=embed)
		elif ctx.invoked_subcommand == "on":
			with open('linkset.json', 'r') as f:
				filterconfig = json.load(f)

			filterconfig[str(ctx.guild.id)] = "enabled"

			with open('linkset.json', 'w') as f:
				json.dump(filterconfig, f, indent=4)

			embed = discord.Embed(title='Link Filter', description=f'The Link Filter has been **Enabled**', color=0x00ff00)
			embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
			await ctx.send(embed=embed)
		elif ctx.invoked_subcommand == "off":
			with open('linkset.json', 'r') as f:
				filterconfig = json.load(f)

			filterconfig[str(ctx.guild.id)] = "disabled"

			with open('linkset.json', 'w') as f:
				json.dump(filterconfig, f, indent=4)
			
			embed = discord.Embed(title='Link Filter', description=f'The Link Filter has been **Disabled**', color=0xff0000)
			embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
			await ctx.send(embed=embed)

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def swearfilter(self, ctx):
		with open('rspremium.json', 'r') as f:
			premium = json.load(f)

		rspremium = premium[str(ctx.guild.id)]

		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)

		prefix = prefixes[str(ctx.guild.id)]
		
		if rspremium == "enabled":
			if ctx.invoked_subcommand is None:
				embed = discord.Embed(title='Swear Filter', description=f'You can turn **on**, **off**, or **set** the swear filter \n Usage: \n \n `{prefix}swearfilter off` - Turns off swearfilter and allows people to swear. \n `{prefix}swearfilter on` - Turns on the swear filter and avoids people from swearing..', color=0x00ff00)
				embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
				await ctx.send(embed=embed)
			elif ctx.invoked_subcommand == "on":
				with open('sfilter.json', 'r') as f:
					filterconfig = json.load(f)

				filterconfig[str(ctx.guild.id)] = "enabled"

				with open('sfilter.json', 'w') as f:
					json.dump(filterconfig, f, indent=4)

				embed = discord.Embed(title='Swear Filter', description=f'The Swear Filter has been **Enabled**', color=0x00ff00)
				embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
				await ctx.send(embed=embed)
			elif ctx.invoked_subcommand == "off":
				with open('sfilter.json', 'r') as f:
					filterconfig = json.load(f)

				filterconfig[str(ctx.guild.id)] = "disabled"

				with open('sfilter.json', 'w') as f:
					json.dump(filterconfig, f, indent=4)
			
				embed = discord.Embed(title='Swear Filter', description=f'The Swear Filter has been **Disabled**', color=0xff0000)
				embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
				await ctx.send(embed=embed)

		else:
			embed = discord.Embed(title=f'{botname} Premium', description=f"Hello there, so uhm... It looks like you don't have **{botname} Premium**, for swear filter to work, you need **RedSafe Premium** activated on your server, you can get RedSafe Premium by requesting and paying on the [Support Server](https://discord.gg/cRTnVaQ).", color=0xF26A72)
			embed.set_footer(text=f'{botname}', icon_url=redsafelogo)

	@commands.group()
	async def prefix(self, ctx):
		if ctx.invoked_subcommand is None:
			with open('prefixes.json', 'r') as f:
				prefixes = json.load(f)

			embed = discord.Embed(title='> Prefix', description=f"""The current prefix for this server is set to `{prefixes[str(ctx.guild.id)]}`""", color=0x00ff00)
			embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
			await ctx.send(embed=embed)

	@prefix.command(name="set")
	@commands.has_permissions(administrator=True)
	async def prefix_set(self, ctx, *, prefix):
		
		collection = db['Prefixes']
		
		new_prefix = {f"{ctx.guild.id}": prefix}
		collection.update(new_prefix)

		embed = discord.Embed(title='Prefix', description=f'The bot prefix has been set to `{prefix}`', color=0x00ff00)
		embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
		await ctx.send(embed=embed)

	@commands.group()
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def verification(self, ctx):
		if ctx.invoked_subcommand is None:
			with open('prefixes.json', 'r') as f:
				prefixes = json.load(f)

			prefix = prefixes[str(ctx.guild.id)]
			embed = discord.Embed(title='Verification', description=f'You can turn **on**, **off**, or **set** verified roles \n Usage: \n \n `{prefix}verification on` - Turns the verification system on. \n `{prefix}verification off` - Turns off the verification system. \n `{prefix}verification set <@role>` - sets a role that is given after verification.', color=0x00ff00)
			embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
			await ctx.send(embed=embed)

	@verification.command(name="on")
	@commands.has_permissions(administrator=True)
	async def verification_on(self, ctx):

		with open('verifysetting.json', 'r') as f:
			verify = json.load(f)

		verify[str(ctx.guild.id)] = "enabled"

		with open('verifysetting.json', 'w') as f:
			json.dump(verify, f, indent=4)

		embed = discord.Embed(title='Verification', description=f'The Verification System has been **Enabled**', color=0x00ff00)
		embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
		await ctx.send(embed=embed)

	@verification.command(name="off")
	@commands.has_permissions(administrator=True)
	async def verification_on(self, ctx):

		with open('verifysetting.json', 'r') as f:
			verify = json.load(f)

		verify[str(ctx.guild.id)] = "disabled"

		with open('verifysetting.json', 'w') as f:
			json.dump(verify, f, indent=4)

		embed = discord.Embed(title='Verification', description=f'The Verification System has been **Disabled**', color=0x00ff00)
		embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
		await ctx.send(embed=embed)

	@verification.command(name="set")
	@commands.has_permissions(administrator=True)
	async def verification_set(self, ctx, role: discord.Role):

		with open('verify.json', 'r') as f:
			verify = json.load(f)

		verify[str(ctx.guild.id)] = role.id

		with open('verify.json', 'w') as f:
			json.dump(verify, f, indent=4)

		embed = discord.Embed(title='Verification', description=f'The Verification System role been set to `{role}`', color=0x00ff00)
		embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	async def verify(self, ctx):
		with open('verifysetting.json', 'r') as f:
			verifysett = json.load(f)
		settingverify = verifysett[str(ctx.guild.id)]


		with open('verify.json', 'r') as f:
			verifi = json.load(f)
		verifyrole = verifi[str(ctx.guild.id)]

		if "enabled" == settingverify:
			for role in ctx.author.roles:
				if role.name == verifyrole:
					print("BOI ALREADY VERIFIED")
				print(role.name)
			role = get(ctx.guild.roles, id=verifyrole)
			await ctx.author.add_roles(role, reason="Verification System. User Verified")
			embed = discord.Embed(title='Verified', description=f'You have been verified on **{ctx.guild.name}**', color=0xF26A72)
			embed.set_footer(text=f'{botname}', icon_url=redsafelogo)

			user = ctx.author
			await user.send(embed=embed)


			channel = get(guild.text_channels, name='redsafe-logs')
			logem = discord.Embed(title='User Verified', color=0x00ff00)
			logem.add_field(name='User ID:', value=f'{ctx.author.id}')
			logem.add_field(name='Name & Tag:', value=f'{ctx.author.name}#{ctx.author.discriminator}')
			logem.add_field(name='Account Creation Date:', value=user.creation_at.__format__('%A %d %B %Y'))
			logem.set_footer(text='RedSafe Logs', icon_url=redsafelogo)
			await channel.send(embed=logem)

		else:
			return 
def setup(bot):
	bot.add_cog(Config(bot))
