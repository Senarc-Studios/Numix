from numix_imports import *

class Filter(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.mongo_moderation_url = f"{self.config.mongo1}Moderation{self.config.mongo2}"
		self.moderation_db = MongoClient(self.mongo_moderation_url)
		self.mongo_DB1_url = f"{self.config.mongo1}DataBase_1{self.config.mongo2}"
		self.db1 = MongoClient(self.mongo_DB1_url)
		print('"Filter" cog loaded')

	@commands.Cog.listener()
	async def on_message(self, message):

		if message.guild.id is None:
			return

		elif message.author.bot:
			return

		else:

			premium = self.db1.DataBase_1.premium

			for guilds in premium.find({ "_id": f"{message.guild.id}" }):
				trf = guilds["premium"]

			if trf == "False":
				return

			elif trf == "True":
				
				guild = message.guild
				user = message.author
				blocked_invites = ["discord.gg", "discord.com/invite"]
				blocked_links = [".qp", ".cp", ".gp", ".pq", "http://", "https://", "www.", ".com", ".net", ".tk", ".uk", ".un", ".gov", ".us", ".cf", ".ml", ".bn", ".in", ".tech", ".bot", ".nu", ".gg", ".chat", ".xyz", ".ga", ".gp", ".org", ".eu", ".name", ".me", ".nl", ".tv", ".info", ".biz", ".cc", ".mobi", ".actor", ".academy", ".agency", ".accountant", ".ws", ".garden", ".cafe", ".ceo", ".care", ".art"]
				blocked_words = ["f**k", "fuk", "fuc", "fuck", "f*ck", "bitch", "b*tch", "n*gga", "ni**a", "nigga", "vegina", "fag", "f*g", "dick", "d*ck", "penis", "porn", "xnxx", "xxnx", "xxx", "sex", "s*x", "hentai", "henti", "pxrn", "p*rn", "a$$", "cunt", "c*nt", "boob", "tits", "cock", "f u c k", "s h i t", "b i t c h", "h e n t a i", "p o r n", "d!ck"]

				# Checks active filters
				filter = self.db1.DataBase_1.filter

				for modules in filter.find({ "_id": f"{message.guild.id}" }):
					invite_filter = modules["Invite"]
					link_filter = modules["Link"]
					profanity_filter = modules["Profanity"]

					# Whitelists
					invite_whitelisted_channels = [""]
					link_whitelisted_channels = [""]
					word_whitelisted_channels = [""]

					if invite_filter == "True":
						for x in blocked_invites:
							if x in message.content.lower():
								if message.channel.id not in invite_whitelisted_channels:
									await message.delete()
									blocked_invite = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained a Discord Invite, you may delete the blocked link and send the message again.', color=242424)
									blocked_invite.set_footer(text='Numix Premium', icon_url=logo)
									await user.send(embed=blocked_invite)

					if link_filter == "True":
						for x in blocked_links:
							if x in message.content.lower():
								if message.channel.id not in link_whitelisted_channels:
									await message.delete()
									blocked_word = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained blocked Links, you may delete the blocked link and send the message again.', color=242424)
									blocked_word.set_footer(text='Numix Premium', icon_url=logo)
									await user.send(embed=blocked_word)

					if profanity_filter == "True":
						for x in blocked_words:
							if x in message.content.lower():
								if message.channel.id not in word_whitelisted_channels:
									await message.delete()
									blocked_word = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained Blocked Words, you may delete the blocked word and send the message again.', color=242424)
									blocked_word.set_footer(text='Numix Premium', icon_url=logo)
									await user.send(embed=blocked_word)

			else:
				return

def setup(bot):
	bot.add_cog(Filter(bot))