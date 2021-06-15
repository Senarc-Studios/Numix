from numix_imports import *
import motor.motor_asyncio
import discord

mongo_url = "mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority"
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
level = cluster["DataBase_1"]['Leveling']

class Leveling(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		print('"Leveling" cog loaded')
		self.cooldown = []

	@commands.Cog.listener()
	async def on_message(self, message):
		greet = None
		if message.author.id in self.cooldown:
			return

		if message.content[2:].startswith("!") or message.content[1:].startswith("!") or message.content.startswith("!") or message.content[2:].startswith("?") or message.content[1:].startswith("?") or message.content.startswith("?") or message.content[2:].startswith(">") or message.content[1:].startswith(">") or message.content.startswith(">") or message.content[2:].startswith(".") or message.content[1:].startswith(".") or message.content.startswith(".") or message.content[2:].startswith("$") or message.content[1:].startswith("$") or message.content.startswith("$") or message.content.startswith("<@!"):
			return

		if message.author.bot:
			return

		if message.guild.id == None:
			return
	
		if await level.count_documents({ "_id": message.author.id }) == 0:
			return await level.insert_one({ "_id": message.author.id, f"{message.guild.id}": "ENABLED", f"{message.guild.id}_XP": len(message.content), f"{message.guild.id}_LEVEL": 1, "GLOBAL_XP": len(message.content), "GLOBAL_LEVEL": 1, "TOTAL_XP": len(message.content), f"{message.guild.id}_TOTAL_XP": len(message.content) })
		
		author_data = await level.find_one({ "_id": message.author.id })

		if await level.count_documents({ "_id": message.author.id, f"{message.guild.id}": "ENABLED" }) == 0:
			return await level.update_one({ "_id": message.author.id }, { "_id": message.author.id, f"{message.guild.id}": "ENABLED", f"{message.guild.id}_XP": len(message.content), f"{message.guild.id}_LEVEL": 1, "TOTAL_XP": author_data[f'TOTAL_XP'] + len(message.content), f"{message.guild.id}_TOTAL_XP": len(message.content)})

		await level.update({ "_id": message.guild.id }, { "_id": message.guild.id, f"{message.guild.id}_XP": author_data[f'{message.author.id}_XP'] + len(message.content), f"GLOBAL_XP": author_data[f'GLOBAL_XP'] + len(message.content), "TOTAL_XP": author_data[f'TOTAL_XP'] + len(message.content), f"{message.guild.id}_TOTAL_XP": len(message.content) })

		if author_data[f"{message.author.id}_XP"] >= int((50 * (author_data[f"{message.guild.id}_LEVEL"] ** 2)) + (50 * author_data[f"{message.guild.id}_LEVEL"])):
			await level.update_one({ "_id": message.author.id }, { "_id": message.author.id,  f"{message.author.id}_XP": 0, f"{message.guild.id}_LEVEL": author_data[f"{message.guild.id}_LEVEL"] + 1 })
			if message.guild.id != 336642139381301249:
				if greet == None:
					greet = f"<:confetti:854263610284441600> You've Leveled up! Now, you're in level {author_data[f'{message.author.id}_LEVEL']}!"
				await message.channel.send(greet)

		if author_data[f"GLOBAL_XP"] >= int((50 * (author_data[f"GLOBAL_LEVEL"] ** 2)) + (50 * author_data[f"GLOBAL_LEVEL"])):
			await level.update_one({ "_id": message.author.id }, { "_id": message.author.id, f"GLOBAL_XP": 0, f"GLOBAL_LEVEL": author_data["GLOBAL_LEVEL"] + 1 })

		self.cooldown.append(message.author.id)
		time.sleep(1.2)
		self.cooldown.pop(message.author.id)
		

def setup(bot):
	bot.add_cog(Leveling(bot))