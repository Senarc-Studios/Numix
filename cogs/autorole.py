from numix_imports import *
from validation import *

class AutoRole(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.mongo_moderation_url = f"{self.config.mongo1}Moderation{self.config.mongo2}"
		self.moderation_db = MongoClient(self.mongo_moderation_url)
		self.mongo_DB1_url = f"{self.config.mongo1}DataBase_1{self.config.mongo2}"
		self.db1 = MongoClient(self.mongo_DB1_url)
		print('"AutoRole" cog loaded')

	@commands.Cog.listener()
	async def on_member_join(self, member):
		if await self.premium(member.guild.id) is True:
			collection = self.db1.DataBase_1.settings
			for data in collection.find({ "_id": int(member.guild.id) }):
				if data["ar"] == "disabled":
					return
				elif data["ar"] == "enabled":
					for roles in data["roles"]:
						role = discord.utils.get(member.guild.roles, id=roles)
						await member.add_roles(role, reason="Auto-Role")
				else:
					return					

def setup(bot):
	bot.add_cog(AutoRole(bot))