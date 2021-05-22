from numix_imports import *

class ADS_Plugin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		print('"ADS_Plugin" cog loaded')

	@commands.Cog.listener()
	async def on_ready(self):
		print("Running ADS Script.")
		blocked_users = self.config.ads
		for guild in self.bot.guilds:
			if guild.owner_id in blocked_users:
				await guild.leave()
				ss = get(self.bot.guilds, id=791553406266245121)
				log = get(ss.text_channels, id=791556611951820801)
				await log.send(f":no_entry_sign: Blocked Server by **Anti-Dummy Server** Module, **Server_Name:** {guild.name}, **Server_ID:** {guild.id}")
		print("ADS Script Ended after on_ready.")

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		if guild.owner_id in self.config.ads:
			await guild.leave()
			ss = get(self.bot.guilds, id=791553406266245121)
			log = get(ss.text_channels, id=791556611951820801)
			await log.send(f":no_entry_sign: Blocked Server by **Anti-Dummy Server** Module, **Server_Name:** {guild.name}, **Server_ID:** {guild.id}")
		else:
			return

	@commands.command(hidden=True, aliases=["run ads"])
	@commands.is_owner()
	async def run_ads(self, ctx):
		await ctx.send("Running ADS Script.")
		blocked_users = self.config.ads
		for guild in self.bot.guilds:
			if guild.owner_id in blocked_users:
				await guild.leave()
				
				log = get(ss.text_channels, id=791556611951820801)
				await log.send(f":no_entry_sign: Blocked Server by **Anti-Dummy Server** Module, **Server_Name:** {guild.name}, **Server_ID:** {guild.id}")
		await ctx.send("ADS Script Ended.")

def setup(bot):
	bot.add_cog(ADS_Plugin(bot))