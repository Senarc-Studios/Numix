from numix_imports import *
from numix_log import *

class AntiNuker(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.Mongo_connection = MongoClient(self.config.db1)
		self.guild_bans = []

	def basic_checks(self, guild):
		premium = self.db1.DataBase_1.premium

		premium_list = premium
		premium_validation_check = premium_list.count_documents({ "_id": f"{guild.id}" })

		if premium_validation_check == 0:
			return

		for guilds in premium.find({ "_id": f"{guild.id}" }):
			trf = guilds["premium"]
			trf = f"{trf}"

		if trf == "False":
			return "Fail"

		elif trf == "True":
			return "Pass"

		else:
			return "Fail"

	async def register_and_nuker_check(self, guild, member):
		col = self.Mongo_collection.DataBase_1.nukeban
		logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
		logs = logs[0]
		if logs.reason == None:
			reason = "Unspecified"
		else:
			reason = logs.reason
		info = { "_id": guild.id, "banned_user": member.id, "moderator": logs.user.id, "reason": reason }
		col.insert_one(info)
		await log("ban", guild, member, logs.user, reason)

		if guild.id in self.guild_bans:
			try:
				for i in col.find({ "_id": f"{guild.id}_ban" }):
					count = i["ban_count"]
					col.update_one({ "_id": f"{guild.id}_ban" }, { "_id": f"{guild.id}_ban", "ban_count": count + 1 })
					if count >= 3:
						print("Anti-Nuker Executed")
						await guild.ban(member, reason=f"User was raiding the server.")
			except:
				count = 2
				col.insert_one({ "_id": f"{guild.id}_ban", "ban_count": count })

		self.guild_bans.append(guild.id)
		await asyncio.sleep(3)
		self.guild_bans.remove(guild.id)

	def check_toggle(self, guild):
		cluster = self.Mongo_connection
		collection = cluster.DataBase_1.settings
		for i in collection.find({ "_id": guild.id }):
			toggle = i["anuker"]
			if toggle == "False":
				return "False"
			if toggle == "True":
				return "True"
			else:
				return "False"

	@commands.Cog.listener()
	async def on_member_ban(guild, member):
		self.check_toggle(guild)
		if self.basic_checks() == "Fail":
			return
		await self.register_and_nuker_check(guild, member)

def setup(bot):
	bot.add_cog(AntiNuker(bot))