from numix_imports import *

# Define Cogs

config = default.get("config.json")

class Logs(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config
		print('"Logs" cog loaded')
	
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		support_server = get(self.bot.guilds, id=791553406266245121)
		join_log_channel = get(support_server.text_channels, id=791556611151626261)
		log_message = discord.Embed(title=f"Joined **{guild.name}**", color=242424)
		log_message.add_field(name="Server ID:", value=f"{guild.id}", inline=False)
		log_message.add_field(name="Owner's ID:", value=f"{guild.owner_id}", inline=False)
		log_message.add_field(name="Owner Mention:", value=f"<@!{guild.owner_id}>", inline=False)
		log_message.set_footer(text="Numix Developers", icon_url=self.config.logo)
		log_message.set_thumbnail(url=guild.avatar_url)
		await join_log_channel.send(embed=log_message)

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		support_server = get(self.bot.guilds, id=791553406266245121)
		leave_log_channel = get(support_server.text_channels, id=791556611151626261)
		log_message = discord.Embed(title=f"Joined **{guild.name}**", color=242424)
		log_message.add_field(name="Server ID:", value=f"{guild.id}", inline=False)
		log_message.add_field(name="Owner's ID:", value=f"{guild.owner_id}", inline=False)
		log_message.add_field(name="Owner Mention:", value=f"<@!{guild.owner_id}>", inline=False)
		log_message.set_footer(text="Numix Developers", icon_url=self.config.logo)
		log_message.set_thumbnail(url=guild.avatar_url)
		await leave_log_channel.send(embed=log_message)

def setup(bot):
	bot.add_cog(Logs(bot))