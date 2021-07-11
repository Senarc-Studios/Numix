from numix_imports import *

config = default.get("./config.json")
mongo_DB1_url = f"{config.mongo1}DataBase_1{config.mongo2}"
db1 = MongoClient(mongo_DB1_url)

async def premium(self, guild_id):
	guild = discord.utils.get(self.bot.guilds, id=guild_id)
	premium = db1.DataBase_1.premium

	premium_list = premium
	premium_validation_check = premium_list.count_documents({ "_id": f"{guild.id}" })

	if premium_validation_check == 0:
		raise RuntimeError("PREMIUM CHECK FAILURE")

	for guilds in premium.find({ "_id": f"{guild.id}" }):
		trf = guilds["premium"]
		trf = f"{trf}"

	if trf == "False":
		raise RuntimeError("PREMIUM CHECK FAILURE")

	elif trf == "True":
		return True

	else:
		raise RuntimeError("PREMIUM CHECK FAILURE")

def authorize(self, ctx):
		if ctx.author.id in self.config.owners:
			return True
		else:
			return False