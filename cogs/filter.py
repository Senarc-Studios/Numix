from numix_imports import *
from profanity_filter import ProfanityFilter

class Filter(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.mongo_moderation_url = f"{self.config.db1}"
		self.moderation_db = MongoClient(self.mongo_moderation_url)
		self.mongo_DB1_url = f"{self.config.db1}"
		self.db1 = MongoClient(self.mongo_DB1_url)
		self.pf = ProfanityFilter()
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

			if premium.count_documents({ "_id": f"{message.guild.id}" }) == 0:
				return

			if trf == "False":
				return

			elif trf == "True":
				
				guild = message.guild
				user = message.author
				blocked_invites = ["discord.gg", "discord.com/invite"]
				blocked_links = [".qp", ".cp", ".gp", ".pq", "http://", "https://", "www.", ".com", ".net", ".tk", ".uk", ".un", ".gov", ".us", ".cf", ".ml", ".bn", ".in", ".tech", ".bot", ".nu", ".gg", ".chat", ".xyz", ".ga", ".gp", ".org", ".eu", ".name", ".me", ".nl", ".tv", ".info", ".biz", ".cc", ".mobi", ".actor", ".academy", ".agency", ".accountant", ".ws", ".garden", ".cafe", ".ceo", ".care", ".art"]
				
				# Checks active filters
				filter = self.db1.DataBase_1.filter

				for modules in filter.find({ "_id": f"{message.guild.id}" }):
					invite_filter = modules["Invite"]
					link_filter = modules["Link"]
					profanity_filter = modules["Profanity"]

					if invite_filter == None:
						invite_filter = "False"
					
					if link_filter == None:
						link_filter = "False"

					if profanity_filter == None:
						profanity_filter = "False"

					# Whitelists
					invite_whitelisted_channels = [""]
					link_whitelisted_channels = [""]
					word_whitelisted_channels = [""]

					msg = message.content.lower().replace("[", "")
					msg = msg.replace("]", "")
					msg = msg.replace("{", "")
					msg = msg.replace("}", "")
					msg = msg.replace(" ", "")
					msg = msg.replace("<", "")
					msg = msg.replace(",", "")
					msg = msg.replace(">", "")
					msg = msg.replace(".", "")
					msg = msg.replace(";", "")
					msg = msg.replace(":", "")
					msg = msg.replace("~", "")
					msg = msg.replace("`", "")
					msg = msg.replace(")", "")
					msg = msg.replace("(", "")
					msg = msg.replace("*", "")
					msg = msg.replace("&", "")
					msg = msg.replace("%", "")
					msg = msg.replace("\\", "")
					msg = msg.replace("/", "")
					msg = msg.replace("=", "")
					msg = msg.replace("+", "")
					msg = msg.replace("_", "")
					msg = msg.replace("-", "")
					msg = msg.replace('"', "")
					msg = msg.replace("'", "")

					if invite_filter == "True":
						for x in blocked_invites:
							if x in msg:
								if message.channel.id not in invite_whitelisted_channels:
									await message.delete()
									blocked_invite = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained a Discord Invite, you may delete the blocked link and send the message again.', color=242424)
									blocked_invite.set_footer(text='Numix Premium', icon_url=self.config.logo)
									await user.send(embed=blocked_invite)

					if link_filter == "True":
						for x in blocked_links:
							if x in msg:
								if message.channel.id not in link_whitelisted_channels:
									await message.delete()
									blocked_word = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained blocked Links, you may delete the blocked link and send the message again.', color=242424)
									blocked_word.set_footer(text='Numix Premium', icon_url=self.config.logo)
									await user.send(embed=blocked_word)

					if profanity_filter == "True":
						check = self.pf.censor(f"{msg}")

						if msg != check:
							await message.delete()
							blocked_word = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained Blocked Words, you may delete the blocked word and send the message again.', color=242424)
							blocked_word.set_footer(text='Numix Premium', icon_url=self.config.logo)
							await user.send(embed=blocked_word)

			else:
				return

def setup(bot):
	bot.add_cog(Filter(bot))