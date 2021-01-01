from numix_imports import *

class Tests(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		print('"Tests" cog loaded')


def setup(bot):
	bot.add_cog(Tests(bot))