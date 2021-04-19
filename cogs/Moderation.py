from numix_imports import *

MONGO = "mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority"

class Moderation(commands.Cog, name='Moderation'):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.s = self.config.success
		print('"Moderation" cog loaded')		

	@commands.command()
	async def report(self, ctx, member: discord.Member = None, *, reason = None):
		cluster = MongoClient(f"{self.config.mongo1}DataBase_1{self.config.mongo2}")
		collection = cluster.DataBase_1.settings
		MONGO_GUILD_SETTINGS = collection.find_one({ "_id": member.guild.id })
		ReportChannel = self.bot.get_channel(MONGO_GUILD_SETTINGS["report"])
		channel = ctx.message.channel
		embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
		embed.set_author(name="Member Reported", icon_url=ctx.author.avatar_url)
		embed.add_field(name="Reported User:", value=f"{member.name}#{member.discriminator}(`{member.id}`)", inline = False)
		embed.add_field(name="Reported By:", value=f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", inline = False)
		embed.add_field(name="Reason:", value=f"{reason}", inline = False)
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_footer(text="Numix", icon_url=self.config.logo)

		if member is None:
			await ctx.send(f"{self.config.forbidden} speficy a user.")
		elif reason is None:
			await ctx.send(f"{self.config.forbidden} speficy a reason.")
		else:
			await ReportChannel.send(embed=embed)
			await channel.send(f"{self.config.success} This member has been reported.")


	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def warn(self, ctx, user: discord.Member=None, *, reason=None):
		cluster = MongoClient(f"{self.config.mongo1}Moderation{self.config.mongo2}")
		collection = cluster.Moderation.warns
		guild = ctx.guild	
		if user is None:
			await ctx.send(f"{self.config.forbidden} You have to specify a user to warn them.")
		
		elif reason is None:
			await ctx.send(f"{self.config.forbidden} You have to specify a reason to warn	 user.")	
		elif ctx.author.top_role <= user.top_role:
			return await ctx.send(f"{self.config.forbidden} You can't warn a user higher	 you.")	
		else:
			try:	
				warn = {"_id":ctx.guild.id, f"{user.id}":[reason]}	
				collection.insert_one(warn)
				collection.insert_one(count)
				
			except Exception as e:
				print(e)
				myquery = { "_id": int(ctx.guild.id) }	
				newvalues = { "$addToSet": { f"{user.id}": f"{reason}" } }	
				collection.update_one(myquery, newvalues)	
				try:
					add_count = { f"{user.id}_count": 1 }
					collection.insert_one(add_count)	
				except Exception as e:
					print(e)	
					for count in collection.find({ "_id": ctx.guild.id }):
						warns = count[f'{user.id}_count']	
						addition = 1	
						warn_count = warns + addition
						
						old_count = { "_id": (ctx.guild.id) }
						new_count = { "$set": { f"{user.id}_count": warn_count } }	
						collection.update_one(old_count, new_count)	
			try:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"**Type	Warn\n**Reason: **{reason}", color=0xFC6700)
				embed.set_author(name="Infraction Information", icon_url=ctx.guild.icon_url)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await user.send(embed=embed)
				await ctx.send(f"{self.s} {user.name}#{user.discriminator} warned *User	 notified*")
			except discord.Forbidden:
				await ctx.send(f"{self.s} {user.name}#{user.discriminator} warned *User was	 notified*")

	@commands.command()
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

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user:discord.Member=None, *, reason=None):
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
					notify_user = discord.Embed(description=f"\n**Type:** Ban\n**Expires:** N/A\n**Reason:** `{reason}`", color=242424)
					notify_user.set_author(name=f"Infraction Information", icon_url=ctx.guild.icon_url)
					notify_user.set_footer(text="Numix", icon_url=self.config.logo)
					await user.send(embed=notify_user)

					await ctx.send(f"{self.s} banned {user.name}#{user.discriminator} *User was notified*")
				except discord.Forbidden:
					await ctx.send(f"{self.s} banned {user.name}#{user.discriminator} *User was not notified*")

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

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, user: discord.Member=None, *, reason=None):
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
					notify_user = discord.Embed(description=f"\n**Type:** Kick\n**Reason:**`{reason	}`", color=242424)
					notify_user.set_author(name=f"Infraction Information	icon_url=ctx.guild.icon_url")
					notify_user.set_footer(text="Numix", icon_url=self.config.logo)
					await user.send(embed=notify_user)	
					await ctx.send(f"{self.s} kicked {user.name}#{user.discriminator} *User	 notified*")
				except discord.Forbidden:
					await ctx.send(f"{self.s} kicked {user.name}#{user.discriminator} *User was	 notified*") 
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

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	async def infractions(self, ctx, user: discord.Member=None):
		cluster = MongoClient(MONGO)
		collection = cluster.Moderation.warns	
		if user is None:
			user = ctx.author	
		finder = collection.find({"_id": ctx.guild.id})
		if collection.find({ "_id": ctx.guild.id }) == 0:
			return await ctx.send(f"{self.config.forbidden} No Infractions Found.")	
		for result in finder:
			infractions = result[f'{user.id}']
			count = result[f'{user.id}_count']
			warns = f"{infractions}"
			infraction_fix_1 = warns.replace("['", "")
			infraction_fix_2 = infraction_fix_1.replace("']", "")
			infraction = infraction_fix_2.replace("', '", "\n")
			embed = discord.Embed(description=f"This user has **{count}** warns.\nTop ten		of this user below.\n\n{infraction}", timestamp=ctx.message.created_at, color=242424)
			embed.set_author(name=f"{user.name}'s Warns", icon_url=user.avatar_url)
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Moderation(bot))