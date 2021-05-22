from numix_imports import *

class App(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.mongo_connection = MongoClient(f"{self.config.db1}")
		self.settings_db = self.mongo_connection.DataBase_1.settings
		self.application_db = self.mongo_connection.DataBase_1.application

	@commands.command(hidden=True, aliases=["application", "app", "staff"])
	async def apply(self, ctx):
		if self.settings_db.find({ "_id": f"{ctx.guild.id}" }) == 0:
			return await ctx.send(f"{self.config.forbidden} Applications aren't set-up in this server.")

		if self.settings_db.find({ "_id": f"{ctx.guild.id}", "apps": "True" }) == 0:
			return await ctx.send(f"{self.config.forbidden} Applications aren't set-up in this server.")

		if self.settings_db.find({ "_id": f"{ctx.guild.id}", "apps": "False" }) == 1:
			return await ctx.send(f"{self.config.forbidden} Applications are closed or disabled.")
		
		application_config_check = self.settings_db.find({ "_id": f"{ctx.guild.id}" })

		for pending_check in self.application_db.find({ "_id": f"{ctx.author.id}" }):
			pending_check = pending_check['action_number']
			if pending_check == "Pending":
				embed = discord.Embed(timestamp=ctx.message.created_at, description="You already have a pending application that you applied before, wait for a server administrator to clear your submittion.", color=242424)
				embed.set_author(name="Denied", icon_url=ctx.guild.icon_url)
				embed.set_footer(text="Numix Premium", icon_url=self.config.logo)

				await ctx.send(embed=embed)

			else:
				for settings in application_config_check:
					status = settings['apps']
					
					for entries in self.application_db.find({ "_id": f"{ctx.guild.id}" }):
						question = entries['1']

						if status == "False":
							return await ctx.send(f"{self.config.forbidden} Applications are closed or disabled.")

						if status == "True":
							if self.application_db.find({ "_id": ctx.author.id, "action_number": 0 }) == 0:

								self.application_db.insert_one({ "_id": ctx.author.id, "action_number": 2, "guild_id": f"{ctx.guild.id}" })
								author = ctx.author

								embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
								embed.set_author(name="Staff Application", icon_url=ctx.guild.icon_url)
								embed.add_field(name="Question 1:", value=f"{question}")
								embed.set_footer(text="Numix Premium", icon_url=self.config.logo)

								await author.send(embed=embed)
							
							elif self.application_db.find({ "_id": ctx.author.id }) >= 1:
								await ctx.send(f"{self.config.forbidden} You're currently in a Application Proccess.")

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.guild is not None:
			return

		guild_id = questions['guild_id']
		guild = get(self.bot.guilds, id=guild_id)

		if self.settings_db.find({ "_id": f"{message.guild.id}" }) == 0:
			return

		elif self.settings_db.find({ "_id": f"{message.guild.id}", "apps": "True" }) == 0:
			return

		elif self.settings_db.find({ "_id": f"{message.guild.id}", "apps": "False" }) == 1:
			return

		for action_number in self.application_db.find({ "_id": message.author.id }):
			action_number = action_number['action_number']
			for questions in self.application_db.find({ "_id": guild_id }):
				question = questions[f'{action_number}']
				author = message.author

				embed = discord.Embed(timestamp=message.created_at, color=242424)
				embed.set_author(name="Staff Application", icon_url=guild.icon_url)
				embed.add_field(name=f"Question {action_number}:", value=f"{question}")
				embed.set_footer(text="Numix Premium", icon_url=self.config.logo)

				await author.send(embed=embed)

				if self.settings_db.find({ "_id": guild_id, "action_number": int(action_number+1) }) == 1:

					fetch_user = { "_id": message.author.id }
					update_action_number = { "$set": { "action_number": int(action_number+1) } }

					self.application_db.update_one(fetch_user, update_action_number)

				else:
					embed = discord.Embed(timestamp=message.created_at, description="That's it, You in the application, you're application has been sent to the Server Administrators.", color=242424)
					embed.set_author(name="Staff Application", icon_url=guild.icon_url)
					embed.set_footer(text="Numix Premium", icon_url=self.config.logo)
					
					await author.send(embed=embed)

					fetch_user = { "_id": message.author.id }
					update_action_number = { "$set": { "action_number": "Pending" } }

					self.application_db.update_one(fetch_user, update_action_number)

def setup(bot):
	bot.add_cog(App(bot))