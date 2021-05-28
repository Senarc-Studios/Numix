from numix_imports import *

class CustomCommand(commands.Command):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.perms = kwargs.get("perms", None)
		self.syntax = kwargs.get("syntax", None)

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
		try:
			collection = self.db1.DataBase_1.settings
			for data in collection({ "_id": int(ctx.guild.id) }):
				channel = data["cbc"]

			if ctx.channel.id == channel:
				premium = self.db1.DataBase_1.premium

				premium_list = premium
				premium_validation_check = premium_list.count_documents({ "_id": f"{ctx.guild.id}" })

				if premium_validation_check == 0:
					return

				for guilds in premium.find({ "_id": f"{ctx.guild.id}" }):
					trf = guilds["premium"]
					trf = f"{trf}"

				if trf == "False":
					return

				elif trf == "True":		
					url = requests.get('http://api.brainshop.ai/get?bid=155653&key=odFCsAutc2kb5BO5&uid=[uid]&msg='+msgAI)
					decode = json.loads(url.text)
					await ctx.send(decode['cnt'])
		except Exception:
			pass

def setup(bot):
	bot.add_cog(ChatBot(bot))