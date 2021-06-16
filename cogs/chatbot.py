from numix_imports import *

class ChatBot(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.mongo_moderation_url = f"{self.config.mongo1}Moderation{self.config.mongo2}"
		self.moderation_db = MongoClient(self.mongo_moderation_url)
		self.mongo_DB1_url = f"{self.config.mongo1}DataBase_1{self.config.mongo2}"
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
				if data["cb"] == "Disabled":
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
		except Exception as e:
			print(e)

def setup(bot):
	bot.add_cog(ChatBot(bot))