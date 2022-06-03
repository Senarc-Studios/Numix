"""
BSD 3-Clause License

Copyright (c) 2021-present, BenitzCoding
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import motor.motor_asyncio
import discord
import canvacord

from numix_imports import *

mongo_url = "mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority"
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
level = cluster["DataBase_1"]['Leveling']

class Leveling(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.db1 = MongoClient(self.config.db1)
		print('"Leveling" cog loaded')
		self.cooldown = []

	async def confirm_task(self, ctx):
		collection = self.db1.DataBase_1.settings

		if collection.count_documents({ "_id": int(ctx.guild.id) }) == 0:
			return collection.insert_one({ "_id": int(ctx.guild.id) })
		else:
			return "Pass"

	@commands.Cog.listener()
	async def on_message(self, message):
		try:
			await self.confirm_task(message)
			mong_col = self.db1.DataBase_1.settings
			for greeting in mong_col.find({ "_id": int(message.guild.id) }):
				toggle = greeting["level_message_toggle"]
				greet = greeting["greeting"]
				try:
					if "{" not in greet:
						greet = greet
					else:
						if "bot." in greet or "guild." in greet or "os." in greet or "self." in greet or "eval(" in greet:
							return
						else:
							greet = greet
				except:
					pass
				
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
					return await level.update_one({ "_id": message.author.id }, { "$set": { "_id": message.author.id, f"{message.guild.id}": "ENABLED", f"{message.guild.id}_XP": len(message.content), f"{message.guild.id}_LEVEL": 1, "TOTAL_XP": author_data[f'TOTAL_XP'] + len(message.content), f"{message.guild.id}_TOTAL_XP": len(message.content)}})

				await level.update_one({ "_id": message.author.id }, { "$set": { "_id": message.author.id, f"{message.guild.id}_XP": author_data[f'{message.guild.id}_XP'] + len(message.content), f"GLOBAL_XP": author_data[f'GLOBAL_XP'] + len(message.content), "TOTAL_XP": author_data[f'TOTAL_XP'] + len(message.content), f"{message.guild.id}_TOTAL_XP": len(message.content) } })

				if author_data[f"{message.guild.id}_XP"] >= int((50 * (author_data[f"{message.guild.id}_LEVEL"] ** 2)) + (50 * author_data[f"{message.guild.id}_LEVEL"])):
					await level.update_one({ "_id": message.author.id }, { "$set": { "_id": message.author.id,  f"{message.guild.id}_XP": 0, f"{message.guild.id}_LEVEL": author_data[f"{message.guild.id}_LEVEL"] + 1 }})
					if message.guild.id != 336642139381301249:
						if toggle == "disabled":
							greet = ""
							if greet == None:
								greet = f"<:confetti:854263610284441600> <@!{message.author.id}> You've Leveled up! Now, you're in level {author_data[f'{message.guild.id}_LEVEL']}!"
							await message.channel.send(greet)

				if author_data[f"GLOBAL_XP"] >= int((50 * (author_data[f"GLOBAL_LEVEL"] ** 2)) + (50 * author_data[f"GLOBAL_LEVEL"])):
					await level.update_one({ "_id": message.author.id }, { "$set": { "_id": message.author.id, f"GLOBAL_XP": 0, f"GLOBAL_LEVEL": author_data["GLOBAL_LEVEL"] + 1 } })

				self.cooldown.append(message.author.id)
				time.sleep(1.2)
				self.cooldown.remove(message.author.id)
		except:
			mong_col = self.db1.DataBase_1.settings
			mong_col.update_one({ "_id": int(message.guild.id) }, { "$set": { "_id": int(message.guild.id), "level_message_toggle": "enabled", "greeting": None } })
		

async def setup(bot):
	await bot.add_cog(Leveling(bot))