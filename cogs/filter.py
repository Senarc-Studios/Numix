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

		else:
			guild = message.guild
			user = message.author
			blocked_invites = ["discord.gg", "discord.com/invite"]
			blocked_links = [".qp", ".cp", ".gp", ".pq", "http://", "https://", "www.", ".com", ".net", ".tk", ".uk", ".un", ".gov", ".us", ".cf", ".ml", ".bn", ".in", ".tech", ".bot", ".nu", ".gg", ".chat", ".xyz", ".ga", ".gp", ".org", ".eu", ".name", ".me", ".nl", ".tv", ".info", ".biz", ".cc", ".mobi", ".actor", ".academy", ".agency", ".accountant", ".ws", ".garden", ".cafe", ".ceo", ".care", ".art"]
			blocked_words = ["f**k", "fuk", "fuc", "fuck", "f*ck", "bitch", "b*tch", "n*gga", "ni**a", "nigga", "vegina", "fag", "f*g", "dick", "d*ck", "penis", "porn", "xnxx", "xxnx", "xxx", "sex", "s*x", "hentai", "henti", "pxrn", "p*rn", "a$$", "cunt", "c*nt", "boob", "tits", "cock", "f u c k", "s h i t", "b i t c h", "h e n t a i", "p o r n", "d!ck"]
			
			# Whitelists
			
			
			for x in blocked_invites:
				if x in message.content.lower():
					if message.channel.id not in invite_whitelisted_channels:
						await message.delete()
						blocked_invite = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained a Discord Invite, you may delete the blocked link and send the message again.', color=242424)
						blocked_invite.set_footer(text='Discord.py For Beginners', icon_url=logo)
						await user.send(embed=blocked_invite)

			for x in blacklisted_links:
				if x in message.content.lower():
					if message.channel.id not in link_whitelisted_channels:
						await message.delete()
						blocked_word = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained blocked Links, you may delete the blocked link and send the message again.', color=242424)
						blocked_word.set_footer(text='Discord.py For Beginners', icon_url=logo)
						await user.send(embed=blocked_word)

			for x in blocked_words:
				if x in message.content.lower():
					if message.channel.id not in word_whitelisted_channels:
						await message.delete()
						blocked_word = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained Blocked Words, you may delete the blocked word and send the message again.', color=242424)
						blocked_word.set_footer(text='Numix Premium', icon_url=logo)
						await user.send(embed=blocked_word)

def setup(bot):
	bot.add_cog(Filter(bot))