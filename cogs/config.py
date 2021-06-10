from numix_imports import *

class CustomCommand(commands.Command):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.perms = kwargs.get("perms", None)
		self.syntax = kwargs.get("syntax", None)

class admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.mongo_moderation_url = f"{self.config.mongo1}Moderation{self.config.mongo2}"
		self.moderation_db = MongoClient(self.mongo_moderation_url)
		self.mongo_DB1_url = f"{self.config.mongo1}DataBase_1{self.config.mongo2}"
		self.db1 = MongoClient(self.mongo_DB1_url)
		print('"Config" cog loaded')

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.content == "<@!744865990810271785>":
			collection = self.db1.DataBase_1.prefixes

			guild_prefix = { "_id": int(message.guild.id) }

			prefix_validation_check = collection.count_documents(guild_prefix)

			if prefix_validation_check == 0:
				return await message.channel.send("The assigned prefix for this Server is `n!`")

			for info in collection.find(guild_prefix):
				prefix = info['prefix']
				await message.channel.send(f"The assigned prefix for this Server is `{prefix}`")

	@commands.command(cls=CustomCommand, perms="ADMINISTRATOR", syntax="n!cb <option> [channel]", description="Manage ChatBots on premium servers.", aliases=["chat-bot", "chat", "bot", "ai"])
	@commands.has_permissions(administrator=True)
	async def cb(self, ctx, option=None, channel: discord.TextChannel=None):
		premium = self.db1.DataBase_1.premium

		premium_list = premium
		premium_validation_check = premium_list.count_documents({ "_id": f"{ctx.guild.id}" })

		if premium_validation_check == 0:
			return await ctx.send(f"{self.config.forbidden} You need Numix Premium to use Chat Bots.")

		for guilds in premium.find({ "_id": f"{ctx.guild.id}" }):
			trf = guilds["premium"]
			trf = f"{trf}"

		if trf == "False":
			return await ctx.send(f"{self.config.forbidden} You need Numix Premium to use Chat Bots.")

		elif trf == "True":
			if option is None:
				return await ctx.send(f"{self.config.forbidden} Please provide an option like `enable`, `disable`, or `set`.")

			elif option == "enable":
				collection = self.db1.DataBase_1.settings
				
				if collection.count_documents({ "_id": int(ctx.guild.id), "cb": "enabled" }) == 0 or collection.count_documents({ "_id": int(ctx.guild.id), "cb": "disabled" }) == 0:
					collection.insert_one({ "_id": int(ctx.guild.id), "cb": "enabled" })
					return await ctx.send(f"{self.config.success} Chat bot has been enabled.")

				for data in collection.find_one({ "_id": int(ctx.guild.id) }):
					
					try:
						if data["cb"] == "enabled":
							return await ctx.send(f"{self.config.forbidden} Chat bot is already enabled.")
					except Exception:
						collection.update_one({ "_id": int(ctx.guild.id) }, { "$set": { "_id": int(ctx.guild.id), "cb": "enabled" } })
						await ctx.send(f"{self.config.success} Chat bot has been enabled.")

					else:
						collection.update_one({ "_id": int(ctx.guild.id) }, { "$set": { "_id": int(ctx.guild.id), "cb": "enabled" } })
					await ctx.send(f"{self.config.success} Chat bot has been enabled.")
			
			elif option == "disable":
				collection = self.db1.DataBase_1.settings

				if collection.count_documents({ "_id": int(ctx.guild.id), "cb": "enabled" }) == 0 or collection.count_documents({ "_id": int(ctx.guild.id), "cb": "disabled" }) == 0:
					collection.insert_one({ "_id": int(ctx.guild.id), "cb": "disabled" })
					await ctx.send(f"{self.config.success} Chat bot has been disabled.")

				for data in collection.find_one({ "_id": int(ctx.guild.id) }):
					try:
						if data["cb"] == "disabled":
							return await ctx.send(f"{self.config.forbidden} Chat bot is not enabled.")
					except Exception:
						collection.update_one({ "_id": int(ctx.guild.id) }, { "$set": { "_id": int(ctx.guild.id), "cb": "disabled" } })
						await ctx.send(f"{self.config.success} Chat bot has been disabled.")

					else:
						collection.update_one({ "_id": int(ctx.guild.id) }, { "$set": { "_id": int(ctx.guild.id), "cb": "disabled" } })
					await ctx.send(f"{self.config.success} Chat bot has been disabled.")

			elif option == "set":
				if channel == None:
					channel = ctx.channel

				collection = self.db1.DataBase_1.settings

				c = 0
				for cnl in ctx.guild.channels:
					count = len(ctx.guild.channels)
					c = c + 1
					i = "Not Found"
					
					if collection.count_documents({ "_id": int(ctx.guild.id), "cbc": int(cnl.id) }) == 1:
						i = "Found"
					
					if i == "Found":
						break

					if c == count:
						collection.insert_one({ "_id": int(ctx.guild.id), "cbc": int(channel.id) })
						return await ctx.send(f"{self.config.success} Chat bot is set to channel <#{channel.id}>")

				for data in collection.find_one({ "_id": int(ctx.guild.id) }):
	
					try:
						if data["cbc"] == int(channel.id):
							return await ctx.send(f"{self.config.forbidden} Chat bot is already set in that channel.")
					except Exception:
						collection.update_one({ "_id": int(ctx.guild.id) }, { "$set": { "_id": int(ctx.guild.id), "cbc": int(channel.id) } })
						await ctx.send(f"{self.config.success} Chat bot is set to channel <#{channel.id}>")

					else:
						collection.update_one({ "_id": int(ctx.guild.id) }, { "$set": { "_id": int(ctx.guild.id), "cbc": int(channel.id) } })
					await ctx.send(f"{self.config.success} Chat bot is set to channel <#{channel.id}>")
		else:
			return

	@commands.command(cls=CustomCommand, perms="ADMINISTRATOR", syntax="n!leavemessages <option> [channel]", description="Change options on leave messages.", aliases=["lm", "leave_message", "leave_msg"])
	@commands.has_guild_permissions(administrator=True)
	async def leavemessages(self, ctx, command=None, channel: discord.TextChannel=None):
		if command is None:
			return await ctx.send(f"{self.config.forbidden} Requirements missing. You can `enable`, `disable`, or `set` a channel.")
		
		elif command == "set":
			if channel is None:
				channel = ctx.channel

			await ctx.send(f'{self.config.success} Leave Channel set to <#{channel.id}>')
			collection = self.db1.DataBase_1.settings

			if collection.count_documents({"_id": ctx.guild.id}) == 0:
				collection.insert_one({ "_id": int(ctx.guild.id), "lm": int(channel.id) })

			else:
				myquery = { "_id": int(ctx.guild.id) }
				newvalues = { "$set": { "_id": int(ctx.guild.id), "lm": int(channel.id) } }
				collection.update_one(myquery, newvalues)

		elif command == "enable":
			collection = self.db1.DataBase_1.settings
			myquery = { "_id": int(ctx.guild.id) }
			newvalues = { "$set": { "_id": int(ctx.guild.id), "lmstatus": "Enabled" } }
			collection.update_one(myquery, newvalues)
			await ctx.send(f"{self.config.success} Leave Messages has been enabled in this server.")

		elif command == "disable":
			collection = self.db1.DataBase_1.settings
			myquery = { "_id": int(ctx.guild.id) }
			newvalues = { "$set": { "_id": int(ctx.guild.id), "lmstatus": "Disabled" } }
			collection.update_one(myquery, newvalues)
			await ctx.send(f"{self.config.success} Leave Messages has been disabled in this server.")

	@commands.command(cls=CustomCommand, perms="ADMINISTRATOR", syntax="n!joinmessages <option> [channel]", description="Change options on join messages.", aliases=["jm", "join-message", "join-msg", "greet", "greetings", "join_message"])
	@commands.has_guild_permissions(administrator=True)
	async def joinmessages(self, ctx, command=None, channel: discord.TextChannel=None):
		if command is None:
			return await ctx.send(f"{self.config.forbidden} Requirements missing. You can `enable`, `disable`, or `set` a channel.")
		
		elif command == "set":
			if channel is None:
				channel = ctx.channel

			await ctx.send(f'{self.config.success} Join Channel set to <#{channel.id}>')
			collection = self.db1.DataBase_1.settings

			if collection.count_documents({"_id": ctx.guild.id}) == 0:
				collection.insert_one({ "_id": int(ctx.guild.id), "jm": int(channel.id) })

			else:
				myquery = { "_id": int(ctx.guild.id) }
				newvalues = { "$set": { "_id": int(ctx.guild.id), "jm": int(channel.id) } }
				collection.update_one(myquery, newvalues)

		elif command == "enable":
			collection = self.db1.DataBase_1.settings
			myquery = { "_id": int(ctx.guild.id) }
			newvalues = { "$set": { "_id": int(ctx.guild.id), "jmstatus": "Enabled" } }
			collection.update_one(myquery, newvalues)
			await ctx.send(f"{self.config.success} Join Messages has been enabled in this server.")

		elif command == "disable":
			collection = self.db1.DataBase_1.settings
			myquery = { "_id": int(ctx.guild.id) }
			newvalues = { "$set": { "_id": int(ctx.guild.id), "jmstatus": "Disabled" } }
			collection.update_one(myquery, newvalues)
			await ctx.send(f"{self.config.success} Join Messages has been disabled in this server.")


		' Change Prefixes '
	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!prefix <option> [prefix]", description="Set and view information about server prefixes.")
	async def prefix(self, ctx, command=None, *, prefix=None):
		if command is None:
			return

		elif command == "set":
			if ctx.author.guild_permissions.administrator:
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

				await ctx.send(f'{self.config.success} Prefix set to `{prefix}`.')
				try:
					collection = self.db1.DataBase_1.prefixes
					
					collection.insert_one({ "_id": int(ctx.guild.id), "prefix": str(prefix), "admin": f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", "time": str(Today) })

				except Exception as e:
					print(e)
					collection = self.db1.DataBase_1.prefixes

					myquery = { "_id": int(ctx.guild.id) }

					newvalues = { "$set": { "_id": int(ctx.guild.id), "prefix": str(prefix), "admin": f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", "time": str(Today) } }

					collection.update_one(myquery, newvalues)
			
			else:
				await ctx.send(f"{self.config.forbidden} You can't use that command.")

		elif command in ("info","log"):
			collection = self.db1.DataBase_1.prefixes

			guild_prefix = { "_id": int(ctx.guild.id) }

			prefix_validation_check = collection.count_documents(guild_prefix)

			if prefix_validation_check == 0:
				embed = discord.Embed(timestamp=ctx.message.created_at, description="You're currently using the Default Prefix which is `n!` you can change the prefix with `n!prefix set <new prefix>`", color=242424)
				embed.set_author(name="Prefix Information", icon_url=self.config.logo)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				return await ctx.send(embed=embed)

			for info in collection.find(guild_prefix):
				prefix = info['prefix']
				admin = info['admin']
				time = info['time']

			embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			embed.set_author(name="Prefix Information", icon_url=self.config.logo)
			embed.add_field(name="Prefix:", value=f"`{prefix}`", inline=False)
			embed.add_field(name="Last Updated By:", value=admin, inline=False)
			embed.add_field(name="Last Updated At:", value=time, inline=False)
			embed.set_footer(text="Numix", icon_url=self.config.logo)

			await ctx.send(embed=embed)

		' Reports Config '

	@commands.command(cls=CustomCommand, perms="ADMINISTRATOR", syntax="n!reports <channel>", description="Sets the channel that reports are sent.", alisases=["set-report", "report-channel"])
	@commands.has_permissions(administrator=True)
	async def reports(self, ctx, log: discord.TextChannel):
		await ctx.send(f'{self.config.success} Report Channel set to <#{log.id}>')
		collection = self.db1.DataBase_1.settings
		if collection.count_documents({"_id": ctx.guild.id}) == 0:
			collection.insert_one({ "_id": int(ctx.guild.id), "report": int(log.id) })
		else:
			myquery = { "_id": int(ctx.guild.id) }
			newvalues = { "$set": { "_id": int(ctx.guild.id), "report": int(log.id) } }
			collection.update_one(myquery, newvalues)

		' Log Config '

	@commands.command(cls=CustomCommand, perms="ADMINISTRATOR", syntax="n!log <channel>", description="Sets the log channel.", alisases=["logs", "set-logs", "audit-log"])
	@commands.has_permissions(administrator=True)
	async def log(self, ctx, log: discord.TextChannel):
		await ctx.send(f'{self.config.success} Log Channel set to <#{log.id}>')
		collection = self.db1.DataBase_1.settings

		if collection.count_documents({"_id": ctx.guild.id}) == 0:
			collection.insert_one({ "_id": int(ctx.guild.id), "log": int(log.id) })

		else:
			myquery = { "_id": int(ctx.guild.id) }
			newvalues = { "$set": { "_id": int(ctx.guild.id), "log": int(log.id) } }
			collection.update_one(myquery, newvalues)

		' Filter Setting '

	@commands.command(cls=CustomCommand, perms="ADMINISTRATOR", syntax="n!filter <type> <option>", description="Customising server filters on premium servers.")
	@commands.has_permissions(administrator=True)
	async def filter(self, ctx, type=None, *, option=None):

		links = ["link", "links"]
		invites = ["invite", "invites"]

		premium = self.db1.DataBase_1.premium

		premium_list = premium
		premium_validation_check = premium_list.count_documents({ "_id": f"{ctx.guild.id}" })

		if premium_validation_check == 0:
			return await ctx.send(f"{self.config.forbidden} You need Numix Premium to use filters.")

		for guilds in premium.find({ "_id": f"{ctx.guild.id}" }):
			trf = guilds["premium"]
			trf = f"{trf}"

		if trf == "False":
			return await ctx.send(f"{self.config.forbidden} You need Numix Premium to use filters.")

		elif trf == "True":
			if type is None:
				embed = discord.Embed(timestamp=ctx.message.created_at, title="Filter", description="You have to specify the Type of filter you want to enable or disable.", color=242424)
				embed.set_footer(text="Numix Premium", icon_url=f"{self.config.logo}")
				await ctx.send(embed=embed)

			elif type in ("profanity","Profanity"):
				if option in ('Enable','enable'):

					try:
						collection = self.db1.DataBase_1.filter
			
						collection.insert_one({ "_id": int(ctx.guild.id), "Profanity": "True" })

					except Exception as e:
						print(e)
						myquery = { "_id": int(ctx.guild.id) }

						newvalues = { "$set": { "_id": int(ctx.guild.id), "Profanity": "True" } }

						collection.update_one(myquery, newvalues)

					profanity_success = discord.Embed(timestamp=ctx.message.created_at, title="Profanity Filter", description=f"Your Profanity filter has been `Enabled` for {ctx.guild.name}, all messages that contain profanity will be filtered on **non-NSFW** channels.", color=242424)
					profanity_success.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=profanity_success)

				elif option in ("Disable","disable"):
					try:
						collection = self.db1.DataBase_1.filter
			
						collection.insert_one({ "_id": int(ctx.guild.id), "Profanity": "False" })

					except Exception as e:
						print(e)
						myquery = { "_id": int(ctx.guild.id) }

						newvalues = { "$set": { "_id": int(ctx.guild.id), "Profanity": "False" } }

						collection.update_one(myquery, newvalues)
					pro_success = discord.Embed(timestamp=ctx.message.created_at, title="Profanity Filter", description=f"Your Profanity filter has been `Disabled` for {ctx.guild.name}, all messages that contain Profanity will be allowed on every channel.", color=242424)
					pro_success.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=pro_success)

				else:
					collection = self.db1.DataBase_1.filter
					pron_success = discord.Embed(timestamp=ctx.message.created_at, title="Profanity Filter", description=f"No change has been done, please specify if you'd like to `Enable`, or `Disable` Profanity Filter.", color=242424)
					pron_success.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=pron_success)

			elif type in links:
				if option in ("Enable","enable"):
					
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

				elif option in ("Disable","disable"):
					try:
						collection = self.db1.DataBase_1.filter
			
						collection.insert_one({ "_id": int(ctx.guild.id), "Link": "False" })

					except Exception as e:
						print(e)
						myquery = { "_id": int(ctx.guild.id) }

						newvalues = { "$set": { "_id": int(ctx.guild.id), "Link": "False" } }

						collection.update_one(myquery, newvalues)
					ssuccess = discord.Embed(timestamp=ctx.message.created_at, title="External Links Filter", description=f"Your Link filter has been `Disabled` for {ctx.guild.name}, all messages that contain Links will be allowed on every channel.", color=242424)
					ssuccess.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=ssuccess)

				else:
					collection = self.db1.DataBase_1.filter
					nsuccess = discord.Embed(timestamp=ctx.message.created_at, title="External Links Filter", description=f"No change has been done, please specify if you'd like to `Enable`, or `Disable` Link Filter.", color=242424)
					nsuccess.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=nsuccess)

			elif type in invites:
				if option in ("Enable","enable"):
					try:
						collection = self.db1.DataBase_1.filter
			
						collection.insert_one({ "_id": int(ctx.guild.id), "Invite": "True" })

					except Exception as e:
						print(e)
						myquery = { "_id": int(ctx.guild.id) }

						newvalues = { "$set": { "_id": int(ctx.guild.id), "Invite": "True" } }

						collection.update_one(myquery, newvalues)

					msuccess = discord.Embed(timestamp=ctx.message.created_at, title="Invite Filter", description=f"Your Link filter has been `Enabled` for {ctx.guild.name}, all messages that contain Invites will be filtered on every channel.", color=242424)
					msuccess.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=msuccess)

				elif option in ("Disable","disable"):

					try:
						collection = self.db1.DataBase_1.filter
			
						collection.insert_one({ "_id": int(ctx.guild.id), "Invite": "False" })

					except Exception as e:
						print(e)
						myquery = { "_id": int(ctx.guild.id) }

						newvalues = { "$set": { "_id": int(ctx.guild.id), "Invite": "False" } }

						collection.update_one(myquery, newvalues)

					gsuccess = discord.Embed(timestamp=ctx.message.created_at, title="Invite Filter", description=f"Your Link filter has been `Disabled` for {ctx.guild.name}, all messages that contain Invites will be allowed on every channel.", color=242424)
					gsuccess.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=gsuccess)

				else:
					osuccess = discord.Embed(timestamp=ctx.message.created_at, title="Invite Filter", description=f"No change has been done, please specify if you'd like to `Enable`, or `Disable` Invite Filter.", color=242424)
					osuccess.set_footer(text="Numix Premium", icon_url=self.config.logo)
					await ctx.send(embed=osuccess)

		else:
			return await ctx.send(f"{self.config.forbidden} You need Numix Premium to use filters.")

def setup(bot):
	bot.add_cog(admin(bot))