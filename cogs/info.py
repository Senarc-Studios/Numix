from numix_imports import *

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = discord.utils.get('./config.json')

	@commands.command(aliases=["info", "dev"])
	async def about(self, ctx):
		embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
		embed.set_footer(text="Numix", logo=self.config.logo)
		embed.set_author(name="Numix Bot", icon_url=self.config.logo)
		embed.add_field(name="Developers:", value=f"{self.config.devs}")
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Info(bot))