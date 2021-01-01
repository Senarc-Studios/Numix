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

	@commands.command(alisases=["set-logs", "audit-log"])
	async def log(self, ctx, log: discord.Text_Channel):
		collection = self.db1.DataBase_1.settings

		update = {"_id": ctx.guild.id, "log": log.id}

		collection.update_one(update)

	@commands.command()
	async def filter(self, ctx, type, *, enodi):

		links = ["link", "Link", "links", "Links", "invite", "invites", "Invite", "Invites"]

		if type is None:
			embed = discord.Embed(timestamp=ctx.message.created_at, title="Filter", description="You have to specify the Type of filter you want to enable or disable.", color=242424)
			embed.set_footer(title="Numix", icon_url=f"{self.config.logo}")
			await ctx.send(embed=embed)

		elif type == "profanity" or "Profanity":
			if enodi == "enable" or "Enable":
				collection = self.db1.DataBase_1.settings
				success = discord.Embed(timestamp=ctx.message.created_at, title="Profanity Filter", description=f"Your Profanity filter has been `Enabled` for {ctx.guild.name}, all messages that contain profanity will be filtered on **non-NSFW** channels.", color=242424)
				success.set_footer(text="Numix Premium", icon_url=self.config.logo)
				await ctx.send(embed=success)

			elif enodi == "Disable" or "disable":
				collection = self.db1.DataBase_1.settings
				success = discord.Embed(timestamp=ctx.message.created_at, title="Profanity Links Filter", description=f"Your Profanity filter has been `Disabled` for {ctx.guild.name}, all messages that contain Profanity will be allowed on every channel.", color=242424)
				success.set_footer(text="Numix Premium", icon_url=self.config.logo)
				await ctx.send(embed=success)

			else:
				collection = self.db1.DataBase_1.settings
				success = discord.Embed(timestamp=ctx.message.created_at, title="Profanity Filter", description=f"No change has been done, please specify if you'd like to `Enable`, or `Disable` Profanity Filter.", color=242424)
				success.set_footer(text="Numix Premium", icon_url=self.config.logo)
				await ctx.send(embed=success)

		elif type in links:
			if enodi == "Enable" or "enable":
				collection = self.db1.DataBase_1.settings
				success = discord.Embed(timestamp=ctx.message.created_at, title="External Links Filter", description=f"Your Link filter has been `Enabled` for {ctx.guild.name}, all messages that contain Links or Invites will be filtered on every channel.", color=242424)
				success.set_footer(text="Numix Premium", icon_url=self.config.logo)
				await ctx.send(embed=success)

			elif enodi == "Disable" or "disable":
				collection = self.db1.DataBase_1.settings
				success = discord.Embed(timestamp=ctx.message.created_at, title="External Links Filter", description=f"Your Link filter has been `Disabled` for {ctx.guild.name}, all messages that contain Links or Invites will be allowed on every channel.", color=242424)
				success.set_footer(text="Numix Premium", icon_url=self.config.logo)
				await ctx.send(embed=success)

			else:
				collection = self.db1.DataBase_1.settings
				success = discord.Embed(timestamp=ctx.message.created_at, title="External Links Filter", description=f"No change has been done, please specify if you'd like to `Enable`, or `Disable` Link Filter.", color=242424)
				success.set_footer(text="Numix Premium", icon_url=self.config.logo)
				await ctx.send(embed=success)

def setup(bot):
	bot.add_cog(Config(bot))