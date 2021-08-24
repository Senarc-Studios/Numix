from numix_imports import *
from discord_webhook import DiscordWebhook
import sys
import traceback
import datetime
import os

# Define Cogs

config = default.get("config.json")

class CustomCommand(commands.Command):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.perms = kwargs.get("perms", None)
        self.syntax = kwargs.get("syntax", None)

class ErrorHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config
		print('"ErrorHandler" cog loaded')

	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):

		if isinstance(err, errors.CommandOnCooldown):
			timeout_duration = int(err.retry_after)
			embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You're currently in cooldown, you won't be able to execute/run/use that command until the cooldown is over. \n\nThe Cooldown ends in `{timeout_duration}`", color=242424)
			embed.set_author(name="Cooldown", icon_url="https://discord.com/assets/11d800c7b4c405d96e8e412163727a89.svg")
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=embed)

		elif isinstance(err, errors.CommandNotFound):
			pass

		else:
			e = "`"
			webhook = DiscordWebhook(url="https://ptb.discord.com/api/webhooks/827098788295606283/MdIajYdY98zaEM8DrygakRceR0XBQimMIBdU4kOJq4ogCo3Ur7TgwsJc85dnkkgsjTgP")
			embed = DiscordEmbed(title="An Error has occurred", description=f"Error:\n {e}{e}{e}Ignoring exception in command {ctx.command}:\n{type(err), err, err.__traceback__}{e}{e}{e}\n\n**Server:**\n{ctx.guild.name}(`{ctx.guild.id}`)\n\n**Command Author:**\n{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", color=242424)
			embed.set_thumbnail(url=config.logo)
			embed.set_footer(text="Numix Developers", icon_url=config.logo)
			webhook.add_embed(embed)
			response = webhook.execute()
			print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
			traceback.print_exception(type(err), err, err.__traceback__, file=sys.stderr)


def setup(bot):
	bot.add_cog(ErrorHandler(bot))
