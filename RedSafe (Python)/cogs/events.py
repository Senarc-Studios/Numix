import discord
import psutil
import os
from discord_webhook import DiscordEmbed, DiscordWebhook

import json
import asyncio
from datetime import datetime
from discord.ext import commands, tasks
from discord.ext.commands import errors
from utils import default

#meta data
redsafelogo = 'https://cdn.discordapp.com/avatars/545230136669241365/af33e499779a7f1f8dfad17b4bf72497.png?size=1024'
bversion = '2.2.1'
devs = '`Danoxzilla-X#7003`, `Benitz Original#1317` and `MythicalKittens#0001`'
botname = 'RedSafe'
cmd = '27'
events = '9'
#meta data

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("config.json")
		self.process = psutil.Process(os.getpid())

	@tasks.loop(seconds=10)
	async def status_task(self):
		status4 = 'You type ".help"'
		status2 = 'Discord API'
		status3 = f'{botname} Premium'
		status5 = f'RedSafe Beta {bversion}'
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(self.bot.guilds)} Servers'))
		await asyncio.sleep(10)
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{status2}'))
		await asyncio.sleep(10)
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{status3}'))
		await asyncio.sleep(10)
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{status4}'))
		await asyncio.sleep(10)
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{status5}'))
		await asyncio.sleep(10)

	@commands.Cog.listener()
	async def on_ready(self):
		print('')
		print(f'Connected to {len(self.bot.guilds)} Servers')
		count = 0
		for guild in self.bot.guilds:
			print("Connected to server:")
			print('{}'.format(self.bot.guilds))
			count +=len(self.bot.guilds)

		self.status_task.start()

	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):

		if isinstance(err, errors.MissingPermissions):
			await ctx.send("<:c:771005703849902151> You don't have permission to perform that command.")

		elif isinstance(err, errors.CheckFailure):
			pass

		elif isinstance(err, errors.MaxConcurrencyReached):
			await ctx.send(f"<:c:771005703849902151> You've used max capacity of command usage at once.")

		elif isinstance(err, errors.CommandOnCooldown):
			await ctx.send(f":stopwatch: Try again in {err.retry_after:.2f} seconds, the command is in cooldown.")

		elif isinstance(err, errors.CommandNotFound):
			pass

		else:
			webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/757575792271294596/JzkFCovOEduKc3zPNlPw_Wvqxb5aPT1eJmwQcB4-Kay7OwetSuoLkuahlLenZm1Y4bMI')
			embed = DiscordEmbed(title='An Error has occurred', description=f'Error: \n ```py\n{err}```', color=0xff0000)
			embed.set_timestamp()
			embed.set_thumbnail(url=f'{redsafelogo}')
			webhook.add_embed(embed)
			webhook.execute()
			print(f'Command Error on {ctx.guild.name} \n\n Error: {err}')

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		joinmsg = discord.Embed(title=f'{botname} Beta', description=f'My default prefix is `.`')
		joinmsg.add_field(name='Server Owner:', value=f'<@!{guild.owner_id}>')
		joinmsg.add_field(name='Bot Description:', value='A Python Discord Bot. Helpful, Thoughtful, Mindful.')
		joinmsg.add_field(name='Support Server:', value='**https://discord.gg/cRTnVaQ**')
		joinmsg.add_field(name='Bot Invite:', value='https://RedSafe.tk/invite')
		joinmsg.set_footer(text=f'{botname}', icon_url=redsafelogo)
		await guild.send(embed=joinmsg)

		with open('swearfilterboi.json', 'r') as f:
			verify = json.load(f)

		verify[str(ctx.guild.id)] = "disabled"

		with open('swearfilterboi.json', 'w') as f:
		   json.dump(verify, f, indent=4)

		with open('onjoinconfig.json', 'r') as f:
			verify = json.load(f)

		verify[str(ctx.guild.id)] = "disabled"

		with open('onjoinconfig.json', 'w') as f:
			json.dump(verify, f, indent=4)

		with open('onleaveconfig.json', 'r') as f:
			verify = json.load(f)

		verify[str(ctx.guild.id)] = "disabled"

		with open('onleaveconfig.json', 'w') as f:
			json.dump(verify, f, indent=4)

		with open('verifysetting.json', 'r') as f:
			verify = json.load(f)

		verify[str(ctx.guild.id)] = "disabled"

		with open('verifysetting.json', 'w') as f:
			json.dump(verify, f, indent=4)

		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)

		prefixes[str(guild.id)] = "."

		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)

		webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/758248651515625503/r4JCjSTWZ9ly3sxnYjzjzF3g1saIgEqGY_cXxg6hmexnnhcokk_IM1qm138li0Judg2p')
		embed = DiscordEmbed(title='New Guild Join!', description=f"Guild : {guild.name} \n \n ID : {guild.id} \n \n Owner : {guild.owner}", color=242424)
		webhook.add_embed(embed)
		webhook.execute()
		embed = discord.Embed(title=f'{botname}', description=f'Hello There, This is {botname}. \n My prefix default is `.` You can change it with `.prefix set {prefix}` \n Have a nice day!', color=0xFFA500)
		embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
		try:
			to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
		except IndexError:
			pass
		else:
			link = await to_send.create_invite(max_age=0)
			webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/758248651515625503/r4JCjSTWZ9ly3sxnYjzjzF3g1saIgEqGY_cXxg6hmexnnhcokk_IM1qm138li0Judg2p')
			embed = DiscordEmbed(title='New Guild Join!', description=f"Guild : {guild.name} \n \n ID : {guild.id} \n \n Owner : {guild.owner} \n \n Invite : {link}", color=242424)
			webhook.add_embed(embed)
			webhook.execute()
			await to_send.send(embed=embed)

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		global count
		count +=1



	@commands.Cog.listener()
	async def on_member_join(self, member):
		audit = get(guild.text_channels, name='redsafe-logs')
		log = discord.Embed(title='Member Left', description=f"**Member:**\n<@!{member.id}>({member.name}#{member.discriminator})\n\n**Member ID:**\n{member.id}\n\n**Account Created At:**\n{member.created_at.__format__('%A, %d. %B %Y, %H:%M:%S')}\n\n**Joined At:**{member.joined_at.__format__('%A, %d. %B %Y, %H:%M:%S')}", color=0xF26A72)
		log.set_thumbnail(url=f'{member.avatar_url}')
		log.set_footer(text=f'{botname}', icon_url=redsafelogo)
		await audit.send(embed=log)

		with open('onjoinconfigset.json', 'r') as f:
			prefixes = json.load(f)
		prefix = prefixes[str(member.guild.id)]
		with open('onjoinconfig.json', 'r') as f:
			joe = json.load(f)
		joes = joe[str(member.guild.id)]
		print(joes)
		if joes == "enabled":
			channel = bot.get_channel(prefix)
			embed = discord.Embed(title=f'{member.name} Joined', description=f'Hey {member.name}, Welcome to **{member.guild.name}** \n Have a nice stay!', color=242424)
			embed.set_image(url='https://cdn.discordapp.com/attachments/731716869576327201/744818377461071952/Welcome-Black-Text-White-BG.gif')
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_footer(text=f'{botname}', icon_url=f'{logo}')
			await channel.send(embed=embed)

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		audit = get(guild.text_channels, name='redsafe-logs')
		log = discord.Embed(title='Member Left', description=f"**Member:**\n<@!{member.id}>({member.name}#{member.discriminator})\n\n**Member ID:**\n{member.id}\n\n**Account Created At:**\n{member.created_at.__format__('%A, %d. %B %Y, %H:%M:%S')}\n\n**Joined At:**{member.joined_at.__format__('%A, %d. %B %Y, %H:%M:%S')}", color=0xF26A72)
		log.set_thumbnail(url=f'{member.avatar_url}')
		log.set_footer(text=f'{botname}', icon_url=redsafelogo)
		await audit.send(embed=log)

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
			mbed.set_thumbnail(url=member.avatar_url)
			await channel.send(embed=embed)

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/758248651515625503/r4JCjSTWZ9ly3sxnYjzjzF3g1saIgEqGY_cXxg6hmexnnhcokk_IM1qm138li0Judg2p')
		embed = DiscordEmbed(title='Left Guild!', description=f"Guild : {guild.name} \n \n ID : {guild.id} \n \n Owner : {guild.owner}", color=242424)
		webhook.add_embed(embed)
		webhook.execute()

	@commands.Cog.listener()
	async def on_command(self, ctx):
		try:
			print(f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}")
		except AttributeError:
			print(f"Private message > {ctx.author} > {ctx.message.clean_content}")

def setup(bot):
	bot.add_cog(Events(bot))
