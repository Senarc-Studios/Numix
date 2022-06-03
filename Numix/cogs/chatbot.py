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
from numix_imports import *

class ChatBot(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.mongo_moderation_url = f"{self.config.db1}"
		self.moderation_db = MongoClient(self.mongo_moderation_url)
		self.mongo_DB1_url = f"{self.config.db1}"
		self.db1 = MongoClient(self.mongo_DB1_url)
		print('"ChatBot" cog loaded')

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return
		try:
			collection = self.db1.DataBase_1.settings
			for data in collection.find({ "_id": int(message.guild.id) }):
				channel = data["cbc"]
				if data["cb"] == "disabled":
					return

				if message.channel.id == channel:
					premium = self.db1.DataBase_1.premium

					premium_list = premium
					premium_validation_check = premium_list.count_documents({ "_id": f"{message.guild.id}" })

					if premium_validation_check == 0:
						return

					for guilds in premium.find({ "_id": f"{message.guild.id}" }):
						trf = guilds["premium"]
						trf = f"{trf}"

					if trf == "False":
						return

					elif trf == "True":		
						url = requests.get('http://api.brainshop.ai/get?bid=155653&key=odFCsAutc2kb5BO5&uid=[uid]&msg='+message.content)
						decode = json.loads(url.text)
						await message.channel.send(decode['cnt'])

					else:
						return
		except:
			pass

async def setup(bot):
	await bot.add_cog(ChatBot(bot))