from numix_imports import *

class Leveling(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		print('"Leveling" cog loaded')


	@commands.Cog.listener()
	async def on_message(self, message):
		mongo_url = "mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority"
		cluster = MongoClient(mongo_url)
		db = cluster["DataBase_1"]
		collection = db["Leveling"]
		author_id = message.author.id
		guild_id = message.guild.id

		user_id = {"_id": author_id, "GuildID": guild_id}

		if message.author.bot:
			return

		if collection.count_documents({ "_id": author_id, "GuildID": guild_id }) == 0:
			user_info = {"_id": author_id, "GuildID": guild_id, "Level": 1, "XP": 0}
			collection.insert_one(user_info)

		exp = collection.find(user_id)
		for xp in exp:
			cur_xp = xp['XP']

			new_xp = cur_xp + 5

			collection.update_one({ "_id": author_id }, { "$set": { "XP":new_xp } }, upsert=True)

			lvl_start = xp['Level']

			new_level = lvl_start + 1

			if cur_xp >= round(lvl_start * 2 * 100):

				collection.update_one({ "_id": author_id, "GuildID": guild_id }, { "$set": { "Level": new_level } }, upsert=True)
				await message.channel.send(f":tada: {message.author.mention} You leveled up to **Level {new_level}** :tada:")

def setup(bot):
	bot.add_cog(Leveling(bot))