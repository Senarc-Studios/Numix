from numix_imports import *

class Config(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.mongo_moderation_url = f"{self.config.mongo1}Moderation{self.config.mongo2}"
		self.moderation_db = MongoClient(self.mongo_moderation_url)
		self.mongo_DB1_url = f"{self.config.mongo1}DataBase_1{self.config.mongo2}"
		self.db1 = MongoClient(self.mongo_DB1_url)
		print('"Config" cog loaded')

	@commands.command(alisases=["logs", "set-logs", "audit-log"])
	@commands.has_permissions(administrator=True)
	async def reports(self, ctx, log: discord.TextChannel):
		await ctx.send(f'{self.config.success} Report Channel set to "<#{log.id}>"')
		try:
			collection = self.db1.DataBase_1.settings
			
			collection.insert_one({ "_id": int(ctx.guild.id), "report": int(log.id) })

		except Exception as e:
			print(e)
			myquery = { "_id": int(ctx.guild.id) }

			newvalues = { "$set": { "_id": int(ctx.guild.id), "report": int(log.id) } }

			collection.update_one(myquery, newvalues)

	@commands.command(alisases=["logs", "set-logs", "audit-log"])
	@commands.has_permissions(administrator=True)
	async def log(self, ctx, log: discord.TextChannel):
		await ctx.send(f'{self.config.success} Log Channel set to "<#{log.id}>"')
		try:
			collection = self.db1.DataBase_1.settings
			
			collection.insert_one({ "_id": int(ctx.guild.id), "log": int(log.id) })

		except Exception as e:
			print(e)
			myquery = { "_id": int(ctx.guild.id) }

			newvalues = { "$set": { "_id": int(ctx.guild.id), "log": int(log.id) } }

			collection.update_one(myquery, newvalues)

	@commands.command()
	async def filter(self, ctx, type=None, *, option=None):

		links = ["link", "links"]
		invites = ["invite", "invites"]

		premium = self.db1.DataBase_1.premium

		for guilds in premium.find({ "_id": f"{ctx.guild.id}" }):
			trf = guilds["premium"]

		if trf == "False":
			return await ctx.send(f"{self.config.forbidden} You need Numix Premium to use filters.")

		elif trf == "True":
			if type is None:
				embed = discord.Embed(timestamp=ctx.message.created_at, title="Filter", description="You have to specify the Type of filter you want to enable or disable.", color=242424)
				embed.set_footer(text="Numix Premium", icon_url=f"{self.config.logo}")
				await ctx.send(embed=embed)

			elif type == "profanity" or "Profanity":
				if option == "enable" or "Enable":

					try:
						collection = self.db1.DataBase_1.filter
			
						collection.insert_one({ "_id": int(ctx.guild.id), "Profanity": "True" })

					except Exception as e:
						print(e)
						myquery = { "_id": int(ctx.guild.id) }

						newvalues = { "$set": { "_id": int(ctx.guild.id), "Profanity": "True" } }

						collection.update_one(myquery, newvalues)

					success = discord.Embed(timestamp=ctx.message.created_at, title="Profanity Filter", description=f"Your Profanity filter has been `Enabled` for {ctx.guild.name}, all messages that contain profanity will be filtered on **non-NSFW** channels.", color=242424)
					success.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=success)

				elif option == "Disable" or "disable":
					try:
						collection = self.db1.DataBase_1.filter
			
						collection.insert_one({ "_id": int(ctx.guild.id), "Profanity": "False" })

					except Exception as e:
						print(e)
						myquery = { "_id": int(ctx.guild.id) }

						newvalues = { "$set": { "_id": int(ctx.guild.id), "Profanity": "False" } }

						collection.update_one(myquery, newvalues)
					success = discord.Embed(timestamp=ctx.message.created_at, title="Profanity Links Filter", description=f"Your Profanity filter has been `Disabled` for {ctx.guild.name}, all messages that contain Profanity will be allowed on every channel.", color=242424)
					success.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=success)

				else:
					collection = self.db1.DataBase_1.filter
					success = discord.Embed(timestamp=ctx.message.created_at, title="Profanity Filter", description=f"No change has been done, please specify if you'd like to `Enable`, or `Disable` Profanity Filter.", color=242424)
					success.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=success)

			elif type == "link" or "Link":
				if option == "Enable" or "enable":
					
					try:
						collection = self.db1.DataBase_1.filter
			
						collection.insert_one({ "_id": int(ctx.guild.id), "Link": "True" })

					except Exception as e:
						print(e)
						myquery = { "_id": int(ctx.guild.id) }

						newvalues = { "$set": { "_id": int(ctx.guild.id), "Link": "True" } }

						collection.update_one(myquery, newvalues)

					success = discord.Embed(timestamp=ctx.message.created_at, title="External Links Filter", description=f"Your Link filter has been `Enabled` for {ctx.guild.name}, all messages that contain Links will be filtered on every channel.", color=242424)
					success.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=success)

				elif option == "Disable" or "disable":
					try:
						collection = self.db1.DataBase_1.filter
			
						collection.insert_one({ "_id": int(ctx.guild.id), "Link": "False" })

					except Exception as e:
						print(e)
						myquery = { "_id": int(ctx.guild.id) }

						newvalues = { "$set": { "_id": int(ctx.guild.id), "Link": "False" } }

						collection.update_one(myquery, newvalues)
					success = discord.Embed(timestamp=ctx.message.created_at, title="External Links Filter", description=f"Your Link filter has been `Disabled` for {ctx.guild.name}, all messages that contain Links will be allowed on every channel.", color=242424)
					success.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=success)

				else:
					collection = self.db1.DataBase_1.filter
					success = discord.Embed(timestamp=ctx.message.created_at, title="External Links Filter", description=f"No change has been done, please specify if you'd like to `Enable`, or `Disable` Link Filter.", color=242424)
					success.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=success)

			elif type == "invite" or "Invite":
				if option == "Enable" or "enable":
					try:
						collection = self.db1.DataBase_1.filter
			
						collection.insert_one({ "_id": int(ctx.guild.id), "Invite": "True" })

					except Exception as e:
						print(e)
						myquery = { "_id": int(ctx.guild.id) }

						newvalues = { "$set": { "_id": int(ctx.guild.id), "Invite": "True" } }

						collection.update_one(myquery, newvalues)

					success = discord.Embed(timestamp=ctx.message.created_at, title="Invite Filter", description=f"Your Link filter has been `Enabled` for {ctx.guild.name}, all messages that contain Invites will be filtered on every channel.", color=242424)
					success.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=success)

				elif option == "Disable" or "disable":

					try:
						collection = self.db1.DataBase_1.filter
			
						collection.insert_one({ "_id": int(ctx.guild.id), "Invite": "False" })

					except Exception as e:
						print(e)
						myquery = { "_id": int(ctx.guild.id) }

						newvalues = { "$set": { "_id": int(ctx.guild.id), "Invite": "False" } }

						collection.update_one(myquery, newvalues)

					success = discord.Embed(timestamp=ctx.message.created_at, title="Invite Filter", description=f"Your Link filter has been `Disabled` for {ctx.guild.name}, all messages that contain Invites will be allowed on every channel.", color=242424)
					success.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=success)

				else:
					success = discord.Embed(timestamp=ctx.message.created_at, title="Invite Filter", description=f"No change has been done, please specify if you'd like to `Enable`, or `Disable` Invite Filter.", color=242424)
					success.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=success)

		else:
			return await ctx.send(f"{self.config.forbidden} You need Numix Premium to use filters.")

def setup(bot):
	bot.add_cog(Config(bot))