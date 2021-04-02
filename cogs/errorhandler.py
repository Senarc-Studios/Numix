from numix_imports import *
from discord_webhook import DiscordWebhook
import sys
import traceback
import datetime

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
			e = "`"
			webhook = DiscordWebhook(url="https://ptb.discord.com/api/webhooks/827098788295606283/MdIajYdY98zaEM8DrygakRceR0XBQimMIBdU4kOJq4ogCo3Ur7TgwsJc85dnkkgsjTgP")
			embed = DiscordEmbed(title="An Error has occurred", description=f"Error:\n {e}{e}{e}Ignoring exception in command {ctx.command}:\n{type(err), err, err.__traceback__}{e}{e}{e}", color=242424)
			embed.set_thumbnail(url=config.logo)
			embed.set_footer(text="Numix Developers", icon_url=config.logo)
			webhook.add_embed(embed)
			response = webhook.execute()
			print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
			traceback.print_exception(type(err), err, err.__traceback__, file=sys.stderr)


def setup(bot):
	bot.add_cog(ErrorHandler(bot))
