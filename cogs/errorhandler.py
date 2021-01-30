from numix_imports import *

# Define Cogs

config = default.get("config.json")

class ErrorHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config
		print('"ErrorHandler" cog loaded')
	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):
		if isinstance(err, errors.CommandOnCooldown):
			await ctx.send(f":stopwatch: Command is on Cooldown for **{err.retry_after:.2f}** seconds.")
		elif isinstance(err, errors.MissingPermissions):
			await ctx.send(f"{self.config.forbidden} You can't use that command.")
		elif isinstance(err, errors.CommandNotFound):
			pass
		else:
			ss = get(self.bot.guilds, id=791553406266245121)
			report = get(ss.text_channels, id=791556612715708448)
			embed = discord.Embed(title='An Error has occurred', description=f'Error: \n ```py\n{err}```', timestamp=ctx.message.created_at, color=242424)
			embed.set_thumbnail(url=self.config.logo)
			embed.set_footer(text="Numix Developers", icon_url=self.config.logo)
			await report.send(embed=embed)
			print(err)

def setup(bot):
	bot.add_cog(ErrorHandler(bot))