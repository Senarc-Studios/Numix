from numix_imports import *

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		print('"Help" cog loaded')

	@commands.command(aliases=["h", "elp"])
	async def help(self, ctx, *, command=None):

		embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
		embed.set_author(name="Numix Commands", icon_url=self.config.logo)
		embed.add_field(name="General", value="```invite, about, avatar, server, report```")
		embed.add_field(name="Fun", value="```8ball, urban, supreme, cat, dog, bird, duck, coffee, noticeme, coinflip, rate, slot ```")

		if ctx.author.guild_permissions.administrator:			
			embed.add_field(name="Admin", value="```log, reports, bug```")

		if ctx.author.guild_permissions.manage_messages:
			embed.add_field(name="Moderation", value="```warn, infractions, clear```")

		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Help(bot))