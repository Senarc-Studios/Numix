from numix_imports import *
import discord_webhook
from discord_webhook import *
import random

class April(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")

	@commands.Cog.listener()
	async def on_command(self, ctx):
		chances = [True, False, False, False, False, False, False, False]
		roll = random.choice(chances)
		if roll == False:
			return

		msg = f":tada: {ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`) Just got the april fool prank! :tada:"
		webhook = discord.Webhook(url="https://ptb.discord.com/api/webhooks/827081143802789919/mzECxSjyx3mtb6JnX6me36CCCcwM0AB-S74krLQkHIoBUqYRexgL5tHgrEVDgLLGSmXb", content=msg)
		response = webhook.execute()

		embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
		embed.set_author(name="Reward!", icon_url=self.config.logo)
		embed.add_field(name="You got a reward!", value="Since you've been using Numix for a while, you can redeem the premium version for free! We're giving this away to users who are using numix often, or new to Numix.", inline=False)
		embed.add_field(name="How to claim reward?", value="You just need to go in https://numix.xyz/premiumreward-6879 and login with your discord account to claim the reward.", inline=False)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.author.send(embed=embed)

def setup(bot):
	bot.add_cog(April(bot))