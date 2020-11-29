import discord
import re
import asyncio
import json

from discord.ext import commands
from utils import permissions, default

#meta data
redsafelogo = 'https://cdn.discordapp.com/avatars/545230136669241365/af33e499779a7f1f8dfad17b4bf72497.png?size=1024'
bversion = '2.2.1'
devs = '`Danoxzilla-X#7003`, `Benitz Original#1317` and `MythicalKittens#0001`'
botname = 'RedSafe'
cmd = '27'
events = '9'
#meta data

# Source: https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/mod.py
class MemberID(commands.Converter):
	async def convert(self, ctx, argument):
		try:
			m = await commands.MemberConverter().convert(ctx, argument)
		except commands.BadArgument:
			try:
				return int(argument, base=10)
			except ValueError:
				raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
		else:
			return m.id


class ActionReason(commands.Converter):
	async def convert(self, ctx, argument):
		ret = argument

		if len(ret) > 512:
			reason_max = 512 - len(ret) - len(argument)
			raise commands.BadArgument(f'reason is too long ({len(argument)}/{reason_max})')
		return ret


class Moderator(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("config.json")

	@commands.command(case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
	@commands.bot_has_permissions(attach_files = True, embed_links = True)
	async def reminder(ctx, time, *, reminder):
		print(time)
		print(reminder)
		user = ctx.message.author
		embed = discord.Embed(color=0xF26A72)
		embed.set_footer(text="Discord.py For Beginners", icon_url=f"{logo}")
		seconds = 0
		if reminder is None:
			embed.add_field(name='Warning', value=' Run the command again but specify what do you want me to remind you about.') # Error message
		if time.lower().endswith("d"):
			seconds += int(time[:-1]) * 60 * 60 * 24
			counter = f"{seconds // 60 // 60 // 24} days"
		if time.lower().endswith("h"):
			seconds += int(time[:-1]) * 60 * 60
			counter = f"{seconds // 60 // 60} hours"
		elif time.lower().endswith("m"):
			seconds += int(time[:-1]) * 60
			counter = f"{seconds // 60} minutes"
		elif time.lower().endswith("s"):
			seconds += int(time[:-1])
			counter = f"{seconds} seconds"
		if seconds == 0:
			embed.add_field(name='Warning',
							value='Please specify a proper duration, do `!help reminder` for more information.')
		elif seconds < 300:
			embed.add_field(name='Warning',
							value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
		elif seconds > 7776000:
			embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
		else:
			beforermd = discord.Embed(title='Reminder Set', description=f'You will be reminded in {counter}', color=0xF26A72)
			beforermd.set_footer(text='Discord.py For Beginners', icon_url=logo)
			afterrmd = discord.Embed(title='Reminder', description=f'**Your reminder:** \n {reminder} \n\n *reminder set {counter} ago*', color=0xF26A72)
			afterrmd.set_footer(text='Discord.py For Beginners', icon_url=logo)
			await ctx.send(embed=beforermd)
			await asyncio.sleep(seconds)
			await ctx.send(embed=afterrmd)
			return
		await ctx.send(embed=embed)

	@commands.command(case_insensitive = True, aliases = ["temp-mute", "temp_mute"])
	@commands.bot_has_permissions(manage_messages = True)
	async def tempmute(ctx, user: discord.Member, time, *, reason):
		user = ctx.message.author
		seconds = 0
		if reason is None:
			await ctx.send('<:F:780326063120318465> User was not muted, because no reason was specified.') # Error message
		if time.lower().endswith("y"):
			seconds += int(time[:-1]) * 60 * 60 * 24 * 365
			counter = f"{seconds // 60 // 60 // 24 // 365} years"
		if time.lower().endswith("d"):
			seconds += int(time[:-1]) * 60 * 60 * 24
			counter = f"{seconds // 60 // 60 // 24} days"
		if time.lower().endswith("h"):
			seconds += int(time[:-1]) * 60 * 60
			counter = f"{seconds // 60 // 60} hours"
		elif time.lower().endswith("m"):
			seconds += int(time[:-1]) * 60 * 60 * 24 * 30
			counter = f"{seconds // 60 // 60 // 24 // 30} months"
		elif time.lower().endswith("s"):
			seconds += int(time[:-1])
			counter = f"{seconds} seconds"
		if seconds == 0:
			await ctx.send('<:F:780326063120318465> User was not muted, because no time was specified.')
		else:
			audit = get(guild.text_channels, name='redsafe-logs')
			beforermd = discord.Embed(title='Muted User', description=f'User has been muted for {counter} \n\n **reason:**\n{reason}', color=0xF26A72)
			beforermd.set_footer(text=f'{botname}', icon_url=redsafelogo)

			log = discord.Embed(title='User Temp-Unmuted', description=f'**User:**\n<@!{user.id}>({user.name}#{user.discriminator}) \n\n **Moderator:**\n<@!{ctx.author.id}>({ctx.author.name}#{ctx.author.discriminator}) \n\n **Reason:**\n{reason}', color=0xF26A72)
			log.set_footer(text=f'{botname}', icon_url=redsafelogo)

			afterrmd = discord.Embed(title='User Unmuted', description=f'**User:**\n{user} \n\n **Unmuted after:**\n{counter}', color=0xF26A72)
			afterrmd.set_footer(title=f'{botname}', icon_url=redsafelogo)

			banned = discord.Embed(title=f'[Muted] {ctx.guild.name}', description=f'You have been muted on **{ctx.guild.name}** for **{counter}**', color=0xF26A72)
			banned.set_footer(text=f'{botname}', icon_url=redsafelogo)

			await ctx.send(embed=beforermd)
			await user.send(embed=banned)
			role = get(ctx.guild.roles, name="Muted")
			await user.add_roles(role, reason=f"User has been muted by {ctx.author.name} for {counter}")
			await audit.send(embed=log)
			await asyncio.sleep(seconds)
			await audit.send(embed=afterrmd)
			await user.remove_roles(role, reason=f"User has been unmuted after {counter}")
			return
		await ctx.send(embed=embed)

	@commands.command(case_insensitive = True, aliases = ["temp-ban", "temp_ban"])
	@commands.bot_has_permissions(ban_members = True)
	async def tempban(ctx, user: discord.Member, time, *, reason):
		user = ctx.message.author
		seconds = 0
		if reason is None:
			await ctx.send('<:F:780326063120318465> User was not banned, because no reason was specified.') # Error message
		if time.lower().endswith("y"):
			seconds += int(time[:-1]) * 60 * 60 * 24 * 365
			counter = f"{seconds // 60 // 60 // 24 // 365} years"
		if time.lower().endswith("d"):
			seconds += int(time[:-1]) * 60 * 60 * 24
			counter = f"{seconds // 60 // 60 // 24} days"
		if time.lower().endswith("h"):
			seconds += int(time[:-1]) * 60 * 60
			counter = f"{seconds // 60 // 60} hours"
		elif time.lower().endswith("m"):
			seconds += int(time[:-1]) * 60 * 60 * 24 * 30
			counter = f"{seconds // 60 // 60 // 24 // 30} months"
		elif time.lower().endswith("s"):
			seconds += int(time[:-1])
			counter = f"{seconds} seconds"
		if seconds == 0:
			await ctx.send('<:F:780326063120318465> User was not banned, because no time was specified.')
		else:
			audit = get(guild.text_channels, name='redsafe-logs')
			beforermd = discord.Embed(title='Banned User', description=f'User has been banned for {counter} \n\n **reason:**\n{reason}', color=0xF26A72)
			beforermd.set_footer(text=f'{botname}', icon_url=redsafelogo)

			log = discord.Embed(title='User Temp-Banned', description=f'**User:**\n<@!{user.id}>({user.name}#{user.discriminator}) \n\n **Moderator:**\n<@!{ctx.author.id}>({ctx.author.name}#{ctx.author.discriminator}) \n\n **Reason:**\n{reason}', color=0xF26A72)
			log.set_footer(text='Discord.py For Beginners', icon_url=logo)

			afterrmd = discord.Embed(title='User Unbanned', description=f'**User:**\n{user} \n\n **Unbanned after:**\n{counter}', color=0xF26A72)
			afterrmd.set_footer(title='Discord.py For Beginners', icon_url=logo)

			banned = discord.Embed(title=f'[Banned] {ctx.guild.name}', description=f'You have been banned on **{ctx.guild.name}** for **{counter}**', color=0xF26A72)
			banned.set_footer(text=f'{botname}', icon_url=redsafelogo)

			await audit.send(embed=log)
			await ctx.send(embed=beforermd)
			await user.send(embed=banned)
			await ctx.guild.unban(user, reason=reason)
			await asyncio.sleep(seconds)
			await ctx.guild.unban(user)
			await audit.send(embed=afterrmd)
			return
		await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, *, search: int):
		await ctx.message.delete()
		if search == None:
			embed = discord.Embed(title='0 Messages Clear', description='No messages were clear, because you did not spesify the ammount of messages to be deleted.', color=0xff0000)
			embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
			await ctx.send(embed=embed, delete_after=5)
		else:
			await ctx.channel.purge(limit=int(search))
			embed2 = discord.Embed(title=f'{int(search)} Messages Cleared', description=f'{int(search)} messages has been deleted.', color=0xF26A72)
			embed2.set_footer(text=f'{botname}', icon_url=redsafelogo)
			await ctx.send(embed=embed2, delete_after=5)


	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member : discord.Member, reason=None):
		await member.kick(reason=f"Moderator:{ctx.message.author.name} Reason:" + reason)

	@commands.command(aliases=["nick"])
	@commands.guild_only()
	@permissions.has_permissions(manage_nicknames=True)
	async def nickname(self, ctx, member: discord.Member, *, name: str = None):
		""" Nicknames a user from the current server. """
		if await permissions.check_priv(ctx, member):
			return

		try:
			await member.edit(nick=name, reason=default.responsible(ctx.author, "Changed by command"))
			message = f"Changed **{member.name}'s** nickname to **{name}**"
			if name is None:
				message = f"Reset **{member.name}'s** nickname"
			await ctx.send(message)
		except Exception as e:
			await ctx.send(e)

	@commands.command()
	@commands.guild_only()
	@permissions.has_permissions(ban_members=True)
	async def ban(self, ctx, member: MemberID, *, reason: str = None):
		""" Bans a user from the current server. """
		m = ctx.guild.get_member(member)
		if m is not None and await permissions.check_priv(ctx, m):
			return

		try:
			await ctx.guild.ban(discord.Object(id=member), reason=default.responsible(ctx.author, reason))
			await ctx.send(default.actionmessage("banned"))
		except Exception as e:
			await ctx.send(e)

	@commands.command()
	@commands.guild_only()
	@commands.max_concurrency(1, per=commands.BucketType.user)
	@permissions.has_permissions(ban_members=True)
	async def massban(self, ctx, reason: ActionReason, *members: MemberID):
		""" Mass bans multiple members from the server. """
		try:
			for member_id in members:
				await ctx.guild.ban(discord.Object(id=member_id), reason=default.responsible(ctx.author, reason))
			await ctx.send(default.actionmessage("massbanned", mass=True))
		except Exception as e:
			await ctx.send(e)

	@commands.command()
	@commands.guild_only()
	@permissions.has_permissions(ban_members=True)
	async def unban(self, ctx, member: MemberID, *, reason: str = None):
		""" Unbans a user from the current server. """
		try:
			await ctx.guild.unban(discord.Object(id=member), reason=default.responsible(ctx.author, reason))
			await ctx.send(default.actionmessage("unbanned"))
		except Exception as e:
			await ctx.send(e)

	@commands.command()
	@commands.guild_only()
	@permissions.has_permissions(manage_roles=True)
	async def mute(self, ctx, member: discord.Member, *, reason: str = None):
		""" Mutes a user from the current server. """
		if await permissions.check_priv(ctx, member):
			return

		muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)

		if not muted_role:
			return await ctx.send("Are you sure you've made a role called **Muted**? Remember that it's case sensetive too...")

		try:
			await member.add_roles(muted_role, reason=default.responsible(ctx.author, reason))
			await ctx.send(default.actionmessage("muted"))
		except Exception as e:
			await ctx.send(e)

	@commands.command()
	@commands.guild_only()
	@permissions.has_permissions(manage_roles=True)
	async def unmute(self, ctx, member: discord.Member, *, reason: str = None):
		""" Unmutes a user from the current server. """
		if await permissions.check_priv(ctx, member):
			return

		muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)

		if not muted_role:
			return await ctx.send("Are you sure you've made a role called **Muted**? Remember that it's case sensetive too...")

		try:
			await member.remove_roles(muted_role, reason=default.responsible(ctx.author, reason))
			await ctx.send(default.actionmessage("unmuted"))
		except Exception as e:
			await ctx.send(e)

	@commands.group()
	@commands.guild_only()
	@permissions.has_permissions(ban_members=True)
	async def find(self, ctx):
		""" Finds a user within your search term """
		if ctx.invoked_subcommand is None:
			await ctx.send_help(str(ctx.command))

	@find.command(name="playing")
	async def find_playing(self, ctx, *, search: str):
		loop = []
		for i in ctx.guild.members:
			if i.activities and (not i.bot):
				for g in i.activities:
					if g.name and (search.lower() in g.name.lower()):
						loop.append(f"{i} | {type(g).__name__}: {g.name} ({i.id})")

		await default.prettyResults(
			ctx, "playing", f"Found **{len(loop)}** on your search for **{search}**", loop
		)

	@find.command(name="username", aliases=["name", "find"])
	async def find_name(self, ctx, *, search: str):
		loop = [f"{i} ({i.id})" for i in ctx.guild.members if search.lower() in i.name.lower() and not i.bot]
		await default.prettyResults(
			ctx, "name", f"Found **{len(loop)}** on your search for **{search}**", loop
		)

	@find.command(name="nickname", aliases=["nick"])
	async def find_nickname(self, ctx, *, search: str):
		loop = [f"{i.nick} | {i} ({i.id})" for i in ctx.guild.members if i.nick if (search.lower() in i.nick.lower()) and not i.bot]
		await default.prettyResults(
			ctx, "name", f"Found **{len(loop)}** on your search for **{search}**", loop
		)

	@find.command(name="id")
	async def find_id(self, ctx, *, search: int):
		loop = [f"{i} | {i} ({i.id})" for i in ctx.guild.members if (str(search) in str(i.id)) and not i.bot]
		await default.prettyResults(
			ctx, "name", f"Found **{len(loop)}** on your search for **{search}**", loop
		)

	@find.command(name="discriminator", aliases=["discrim", "disc"])
	async def find_discriminator(self, ctx, *, search: str):
		if not len(search) == 4 or not re.compile("^[0-9]*$").search(search):
			return await ctx.send("You must provide exactly 4 digits")

		loop = [f"{i} ({i.id})" for i in ctx.guild.members if search == i.discriminator]
		await default.prettyResults(
			ctx, "discriminator", f"Found **{len(loop)}** on your search for **{search}**", loop
		)

	@commands.group()
	@commands.guild_only()
	@commands.max_concurrency(1, per=commands.BucketType.guild)
	@permissions.has_permissions(manage_messages=True)
	async def prune(self, ctx):
		""" Removes messages from the current server. """
		if ctx.invoked_subcommand is None:
			return

	async def do_removal(self, ctx, limit, predicate, *, before=None, after=None, message=True):
		if limit > 2000:
			return await ctx.send(f'Too many messages to search given ({limit}/2000)')

		if before is None:
			before = ctx.message
		else:
			before = discord.Object(id=before)

		if after is not None:
			after = discord.Object(id=after)

		try:
			deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate)
		except discord.Forbidden:
			return await ctx.send('I do not have permissions to delete messages.')
		except discord.HTTPException as e:
			return await ctx.send(f'Error: {e} (try a smaller search?)')

		deleted = len(deleted)
		if message is True:
			await ctx.send(f'🚮 Successfully removed {deleted} message{"" if deleted == 1 else "s"}.')

	@prune.command()
	async def embeds(self, ctx, search=100):
		"""Removes messages that have embeds in them."""
		await self.do_removal(ctx, search, lambda e: len(e.embeds))

	@prune.command()
	async def files(self, ctx, search=100):
		"""Removes messages that have attachments in them."""
		await self.do_removal(ctx, search, lambda e: len(e.attachments))

	@prune.command()
	async def mentions(self, ctx, search=100):
		"""Removes messages that have mentions in them."""
		await self.do_removal(ctx, search, lambda e: len(e.mentions) or len(e.role_mentions))

	@prune.command()
	async def images(self, ctx, search=100):
		"""Removes messages that have embeds or attachments."""
		await self.do_removal(ctx, search, lambda e: len(e.embeds) or len(e.attachments))

	@prune.command(name='all')
	async def _remove_all(self, ctx, search=100):
		"""Removes all messages."""
		await self.do_removal(ctx, search, lambda e: True)

	@prune.command()
	async def user(self, ctx, member: discord.Member, search=100):
		"""Removes all messages by the member."""
		await self.do_removal(ctx, search, lambda e: e.author == member)

	@prune.command()
	async def contains(self, ctx, *, substr: str):
		"""Removes all messages containing a substring.
		The substring must be at least 3 characters long.
		"""
		if len(substr) < 3:
			await ctx.send('The substring length must be at least 3 characters.')
		else:
			await self.do_removal(ctx, 100, lambda e: substr in e.content)

	@prune.command(name='bots')
	async def _bots(self, ctx, search=100, prefix=None):
		"""Removes a bot user's messages and messages with their optional prefix."""

		getprefix = prefix if prefix else self.config.prefix

		def predicate(m):
			return (m.webhook_id is None and m.author.bot) or m.content.startswith(tuple(getprefix))

		await self.do_removal(ctx, search, predicate)

	@prune.command(name='users')
	async def _users(self, ctx, prefix=None, search=100):
		"""Removes only user messages. """

		def predicate(m):
			return m.author.bot is False

		await self.do_removal(ctx, search, predicate)

	@prune.command(name='emojis')
	async def _emojis(self, ctx, search=100):
		"""Removes all messages containing custom emoji."""
		custom_emoji = re.compile(r'<a?:(.*?):(\d{17,21})>|[\u263a-\U0001f645]')

		def predicate(m):
			return custom_emoji.search(m.content)

		await self.do_removal(ctx, search, predicate)

	@prune.command(name='reactions')
	async def _reactions(self, ctx, search=100):
		"""Removes all reactions from messages that have them."""

		if search > 2000:
			return await ctx.send(f'Too many messages to search for ({search}/2000)')

		total_reactions = 0
		async for message in ctx.history(limit=search, before=ctx.message):
			if len(message.reactions):
				total_reactions += sum(r.count for r in message.reactions)
				await message.clear_reactions()

		await ctx.send(f'Successfully removed {total_reactions} reactions.')


def setup(bot):
	bot.add_cog(Moderator(bot))
