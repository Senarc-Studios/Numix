from numix_imports import *

config = default.get('./config.json')

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config
		self.process = psutil.Process(os.getpid())
		print('"Info" cog loaded')

	@commands.command(aliases=["info", "dev"])
	async def about(self, ctx):
		ram = self.process.memory_full_info().rss / 1024**2

		embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		embed.set_author(name="Numix Bot", icon_url=self.config.logo)
		embed.add_field(name="Developers:", value=f"{self.config.devs}", inline=False)
		embed.add_field(name="Bot Version:", value=f"{self.config.botversion}", inline=False)
		embed.add_field(name="Support Server:", value=f"{self.config.supportserver}", inline=False)
		embed.add_field(name="Loaded Commands:", value=len([x.name for x in self.bot.commands]), inline=False)
		embed.add_field(name="Ram Usage:", value=f"{ram} MB", inline=False)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Info(bot))