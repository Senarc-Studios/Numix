from numix_imports import *
import string
import random

MONGO = "mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority"

class CustomCommand(commands.Command):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.perms = kwargs.get("perms", None)
        self.syntax = kwargs.get("syntax", None)

class moderation(commands.Cog, name='moderation'):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.s = self.config.success
		print('"Moderation" cog loaded')

	"""

	Warn Sample Document

	{
		"_id": 000000000000000000,
		"users": {
			"000000000000000000": {
				"warn_count": 0
				"warn_id": {
					"reason": "Testing Sample",
					"time": "00-00-0000",
					"moderator": "Moderator#0000(`000000000000000000`)"
				}
			}
		}
	}

	"""

	@commands.command(cls=CustomCommand, perms="KICK_MEMBERS", syntax="n!warn <member> <reason>", description="Warns a mentioned user with a reason.", name="warn")
	@commands.has_permissions(kick_members=True)
	async def warn(self, ctx, user: discord.Member=None, *, reason=None):

		date_1 = f"{ctx.message.created_at.__format__('%d-%B-%Y @ %H:%M:%S')}"
		date_2 = date_1.replace("January", "01")
		date_3 = date_2.replace("February", "02")
		date_4 = date_3.replace("March", "03")
		date_5 = date_4.replace("April", "04")
		date_6 = date_5.replace("May", "05")
		date_7 = date_6.replace("June", "06")
		date_8 = date_7.replace("July", "07")
		date_9 = date_8.replace("August", "08")
		date_10 = date_9.replace("September", "09")
		date_11 = date_10.replace("October", "10")
		date_12 = date_11.replace("November", "11")
		date_13 = date_12.replace("December", "12")
		Today = date_13
		
		cluster = MongoClient(f"{self.config.mongo1}Moderation{self.config.mongo2}")
		collection = cluster.Moderation.warns
		guild = ctx.guild	
		
		if user is None:
			await ctx.send(f"{self.config.forbidden} You have to specify a user to warn them.")
		
		elif reason is None:
			await ctx.send(f"{self.config.forbidden} You have to specify a reason to warn user.")	

		elif ctx.author.top_role <= user.top_role:
			return await ctx.send(f"{self.config.forbidden} You can't warn a user higher you.")	
		
		else:

			try:

				for data in collection.find({ "_id": int(ctx.guild.id) }):
					
					chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
					token_id = ''.join(random.choice(chars) for _ in range(6))
					token_id_string = str(token_id)

					current_count = data["users"][user.id]["warn_count"]
					warn = { 
					"_id": int(ctx.guild.id),
					"users": { 
						f"{token_id_string}": {
							"reason": reason,
							"time": f"{Today}",
							"moderator": f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)"
							}
						}
					}
					collection.insert_one(warn)
					collection.update_one({ "_id": int(ctx.guild.id), "users": { "warn_id": { "warn_count": current_count + 1 } } })
					
					Moderator = f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)"
					if reason.endswith("-s"):
						Moderator = "*Information Disclosed*"

					try:

						embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
						embed.set_author(name=f"Warn from {ctx.guild.name}", icon_url=ctx.guild.icon_url)
						embed.add_field(name="Reason:", value=f"{reason}")
						embed.add_field(name="Total Warns:", value=f"{current_count}", inline=False)
						embed.add_field(name="Moderator:", value=f"{Moderator}", inline=False)
						embed.add_field(name="Date:", value=f"`{Today}`", inline=False)
						embed.add_field(name="Warn ID:", value=f"`{token_id_string}`", inline=False)
						embed.set_footer(text="Numix", icon_url=self.config.logo)
						
						await user.send(embed=embed)
						
						await ctx.send(f"{user.name}#{user.discriminator} has been warned *(user was notified)*")

					except:

						await ctx.send(f"{user.name}#{user.discriminator} has been warned *(user was not notified)*")

			except:

				warn = {
				"_id": int(ctx.guild.id),
				"users": { 
					f"{token_id_string}": {
						"warn_count": 1,
						"reason": reason,
						"time": f"{Today}",
						"moderator": f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)"
						}
					}
				}
				collection.insert_one(warn)

				try:

					embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
					embed.set_author(name=f"Warn from {ctx.guild.name}", icon_url=ctx.guild.icon_url)
					embed.add_field(name="Reason:", value=f"{reason}")
					embed.add_field(name="Total Warns:", value=f"{current_count}", inline=False)
					embed.add_field(name="Moderator:", value=f"{Moderator}", inline=False)
					embed.add_field(name="Date:", value=f"`{Today}`", inline=False)
					embed.add_field(name="Warn ID:", value=f"`{token_id_string}`", inline=False)
					embed.set_footer(text="Numix", icon_url=self.config.logo)
					
					await user.send(embed=embed)
					
					await ctx.send(f"{self.config.success} {user.name}#{user.discriminator} has been warned *(user was notified)*")

				except:

					await ctx.send(f"{self.config.success} {user.name}#{user.discriminator} has been warned *(user was not notified)*")

	@commands.command(cls=CustomCommand, perms="MANAGE_MESSAGES", syntax="n!clear <ammount>", description="Clears the specified amount of messages", name="clear")
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, *, amount: int=None):
		
		if amount is None:
			await ctx.send(f"{self.config.forbidden} Specify the number of messages you	 deleted.")	
		
		else:

			await ctx.message.delete()
			await ctx.channel.purge(limit=amount)
			await asyncio.sleep(1)
			await ctx.send(f"{self.config.s} Deleted **{int(amount)}** Messages", delete_after=3)

	@commands.command(cls=CustomCommand, perms="BAN_MEMBERS", syntax="n!ban <member> <reason>", description="Bans a mentioned user.", name="ban")
	@commands.guild_only()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user:discord.Member=None, *, reason=None):

		date_1 = f"{ctx.message.created_at.__format__('%d-%B-%Y @ %H:%M:%S')}"
		date_2 = date_1.replace("January", "01")
		date_3 = date_2.replace("February", "02")
		date_4 = date_3.replace("March", "03")
		date_5 = date_4.replace("April", "04")
		date_6 = date_5.replace("May", "05")
		date_7 = date_6.replace("June", "06")
		date_8 = date_7.replace("July", "07")
		date_9 = date_8.replace("August", "08")
		date_10 = date_9.replace("September", "09")
		date_11 = date_10.replace("October", "10")
		date_12 = date_11.replace("November", "11")
		date_13 = date_12.replace("December", "12")
		Today = date_13

		if user is None:
			await ctx.send(f"{self.config.forbidden} Specify a user.")

		elif reason is None:
			await ctx.send(f"{self.config.forbidden} Specify a reason.")

		else:
			guild = ctx.guild
			if user.top_role >= guild.me.top_role:
				await ctx.send(f"{self.config.forbidden} Unable to ban user.")

			elif user.top_role >= ctx.author.top_role:
				await ctx.send(f"{self.config.forbidden} Unable to ban user.")

			else:
				try:

					Moderator = f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)"
					if reason.endswith("-s"):
						Moderator = "*Information Disclosed*"

					embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
					embed.set_author(name=f"Banned from {ctx.guild.name}", icon_url=ctx.guild.icon_url)
					embed.add_field(name="Reason:", value=f"{reason}")
					embed.add_field(name="Moderator:", value=f"{Moderator}", inline=False)
					embed.add_field(name="Date:", value=f"`{Today}`", inline=False)
					embed.set_footer(text="Numix", icon_url=self.config.logo)
					await user.send(embed=embed)

					await ctx.send(f"{self.s} {user.name}#{user.discriminator} was banned *(User was notified)*")

				except discord.Forbidden:
					await ctx.send(f"{self.s} {user.name}#{user.discriminator} was banned *(User was not notified)*")

				try:
					await ctx.guild.ban(user, reason=f"{reason}")

				except discord.Forbidden:
					return await ctx.send(f"{self.config.forbidden} Unable to ban user.")

				cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
				collection = cluster.DataBase_1.settings

				for x in collection.find({"_id":ctx.guild.id}):

					logid = x["log"]

					guild = ctx.guild
					log = get(guild.text_channels, id=logid)

					log_message = discord.Embed(timestamp=ctx.message.created_at, color=242424)
					log_message.set_author(name=f"{user.name} Banned", icon_url=user.avatar_url)
					log_message.add_field(name="User:", value=f"{user.name}#{user.discriminator}(`{user.id}`)", inline=False)
					log_message.add_field(name="Moderator:", value=f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", inline=False)
					log_message.add_field(name='Account Creation:', value=user.created_at.__format__('%A, %d. %B %Y on %H:%M:%S'), inline=False)
					log_message.add_field(name='Joined At:', value=user.joined_at.__format__('%A, %d. %B %Y on %H:%M:%S'), inline=False)
					log_message.set_footer(text="Numix", icon_url=self.config.logo)

					await log.send(embed=log_message)

	@commands.command(cls=CustomCommand, perms="KICK_MEMBERS", syntax="n!kick <member> <reason>", description="Kicks a mentioned user.", name="kick")
	@commands.guild_only()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, user: discord.Member=None, *, reason=None):

		date_1 = f"{ctx.message.created_at.__format__('%d-%B-%Y @ %H:%M:%S')}"
		date_2 = date_1.replace("January", "01")
		date_3 = date_2.replace("February", "02")
		date_4 = date_3.replace("March", "03")
		date_5 = date_4.replace("April", "04")
		date_6 = date_5.replace("May", "05")
		date_7 = date_6.replace("June", "06")
		date_8 = date_7.replace("July", "07")
		date_9 = date_8.replace("August", "08")
		date_10 = date_9.replace("September", "09")
		date_11 = date_10.replace("October", "10")
		date_12 = date_11.replace("November", "11")
		date_13 = date_12.replace("December", "12")
		Today = date_13

		if user is None:
			await ctx.send(f"{self.config.forbidden} Specify a user.")

		elif reason is None:
			await ctx.send(f"{self.config.forbidden} Specify a reason.")

		else:

			guild = ctx.guild
			if user.top_role >= guild.me.top_role:
				await ctx.send(f"{self.config.forbidden} Unable to kick user.")

			elif user.top_role >= ctx.author.top_role:
				await ctx.send(f"{self.config.forbidden} Unable to kick user.")

			else:

				try:
					
					Moderator = f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)"
					if reason.endswith("-s"):
						Moderator = "*Information Disclosed*"

					embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
					embed.set_author(name=f"Kicked from {ctx.guild.name}", icon_url=ctx.guild.icon_url)
					embed.add_field(name="Reason:", value=f"{reason}")
					embed.add_field(name="Moderator:", value=f"{Moderator}", inline=False)
					embed.add_field(name="Date:", value=f"`{Today}`", inline=False)
					embed.set_footer(text="Numix", icon_url=self.config.logo)
					await user.send(embed=embed)

					await ctx.send(f"{self.s} kicked {user.name}#{user.discriminator} *(User was notified)*")

				except discord.Forbidden:

					await ctx.send(f"{self.s} {user.name}#{user.discriminator} was kicked *(User was not notified)*")

				try:
					await ctx.guild.kick(user, reason=f"{reason}")

				except discord.Forbidden:
					return await ctx.send(f"{self.config.forbidden} Unable to kick user.")

				cluster = MongoClient(' +srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true w=majority')
				collection = cluster.DataBase_1.settings	
				for x in collection.find({"_id":ctx.guild.id}):
					logid = x["log"]	
					guild = ctx.guild
					log = get(guild.text_channels, id=logid)	
					log_message = discord.Embed(timestamp=ctx.message.created_at, color=242424)
					log_message.set_author(name=f"{user.name} Kicked", icon_url=user.avatar_url)
					log_message.add_field(name="User:", value=f"{user.name}#{user.discriminator} {user.id}`)", inline=False)
					log_message.add_field(name="Moderator:", value=f"{ctx.author.name} {ctx.author.discriminator}(`{ctx.author.id}`)", inline=False)
					log_message.add_field(name='Account Creation:', value=user.created_at.strftime("%A, %d. %B %Y on %H:%M:%S"), inline=False)
					log_message.add_field(name='Joined At:', value=user.joined_at.__format__('%A	%d. %B %Y on %H:%M:%S'), inline=False)
					log_message.set_footer(text="Numix", icon_url=self.config.logo)
					await log.send(embed=log_message)

	@commands.command(cls=CustomCommand, perms="MANAGE_MESSAGES", syntax="n!infractions <member>", description="Shows all the warning a user has.")
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	async def infractions(self, ctx, user: discord.Member=None):
		cluster = MongoClient(MONGO)
		collection = cluster.Moderation.warns

		if user is None:
			user = ctx.author

		for data in collection.find({ "_id": int(ctx.guild.id) }):
			
			warn_count = data["users"][user.id]["warn_count"]
			warns = json.load(data["users"][user.id])

			embed = discord.Embed(timestamp=ctx.message.created_at, colour=242424)
			embed.set_author(name=f"{user.name}'s Infractions", icon_url=user.avatar_url)
			embed.add_field(name="Warn Count:", value=f"`{warn_count}`")

			for warn_ids in warns:
				embed.add_field(name="**Warn ID:**", value=f"{warn_ids}", inline=False)
				for _data in warn_ids:
					embed.add_field(name="Reason:", value=f"{_data['reason']}", inline=False)
					embed.add_field(name="Date:", value=f"`{_data['time']}`", inline=False)
					embed.add_field(name="Moderator:", value=f"`{_data['moderator']}`", inline=False)

	"""

	Warn Sample Document

	{
		"_id": 000000000000000000,
		"users": {
			"000000000000000000": {
				"warn_count": 0
				"AAA000": {
					"reason": "Testing Sample",
					"time": "00-00-0000",
					"moderator": "Moderator#0000(`000000000000000000`)"
				}
			}
		}
	}

	"""


def setup(bot):
	bot.add_cog(moderation(bot))