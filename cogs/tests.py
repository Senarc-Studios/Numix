from numix_imports import *

mydb = mysql.connector.connect(
  host="freedb.tech",
  user="freedbtech_Benitz",
  password="wNJbg8lpM$VS^$#A"
)

class Tests(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		print('"Tests" cog loaded')

	@commands.command()
	@commands.is_owner()
	async def dbtest(self, ctx):
		mycursor = mydb.cursor()

		mycursor.execute("CREATE DATABASE test")
		return

def setup(bot):
	bot.add_cog(Tests(bot))